// =====================
// INITIALISATION DE LA CARTE
// =====================
var map = L.map('map', {
    center: [46.603354, 1.888334],
    zoom: 6,
    maxBounds: [[-90, -Infinity], [90, Infinity]],
    worldCopyJump: true,
    maxBoundsViscosity: 1.0,
    minZoom: 3,
    maxZoom: 20,
    zoomControl: false
});

// Tuiles Google Maps
L.tileLayer('https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}', {
    attribution: '© Google',
    maxZoom: 20,
    keepBuffer: 20,
}).addTo(map);

// Contrôle de zoom
L.control.zoom({ position: 'topright' }).addTo(map);

// =====================
// VARIABLES GLOBALES
// =====================
var markersDict = {};             // Marqueurs par organisme ID
var formationItemsDict = {};      // Éléments HTML de formation par ID de formation
var currentlyHighlighted = null;  // Formation actuellement en surbrillance
var allFormations = [];           // Toutes les formations chargées
var allOrganismes = {};           // Tous les organismes chargés

// Variables pour les filtres
var currentFilters = {
    types: new Set(['initiale', 'continue']),
    labels: new Set(),
    financement: '',
    prixMin: null,
    prixMax: null,
    duree: '',
    region: '', // Ajouter la région aux filtres actuels
};

// Ajouter aux variables globales
var organismeRegions = {};  // Pour stocker les régions des organismes
let currentRegionLayer = null; // Pour stocker le layer de la région actuelle

// =====================
// HIGHLIGHT D'UNE FORMATION
// =====================
function highlightFormationItem(formationId, isClick = false) {
    resetAllFormationItems();

    if (!formationId) {
        currentlyHighlighted = null;
        return;
    }

    const item = formationItemsDict[formationId];
    if (!item) return;

    item.style.transform = 'scale(1.02)';
    item.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)';
    item.style.borderColor = '#1e90a2';
    item.style.borderWidth = '1px';

    if (isClick) {
        const container = document.getElementById('formations-container');
        if (container.firstChild !== item) {
            if (container.contains(item)) {
                container.removeChild(item);
                container.insertBefore(item, container.firstChild);
            }
        }
        item.scrollIntoViewIfNeeded({ behavior: 'smooth', block: 'start' });    
        
    }

    currentlyHighlighted = formationId;
}

// =====================
// RÉINITIALISE TOUS LES ÉLÉMENTS FORMATION
// =====================
function resetAllFormationItems() {
    document.querySelectorAll('.formation-item').forEach(item => {
        item.style.transform = '';
        item.style.boxShadow = '';
        item.style.borderColor = '#b6c6c4';
        item.style.borderWidth = '1px';
    });
}

// =====================
// GÉOCODAGE D'ADRESSE
// =====================
function geocodeAddress(address, callback) {
    const cleanedAddress = address.replace(/,/g, '');
    const url = `https://data.geopf.fr/geocodage/search?q=${encodeURIComponent(cleanedAddress)}&limit=1`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data && data.features && data.features.length > 0) {
                const coords = data.features[0].geometry.coordinates;
                callback({
                    lat: coords[1],
                    lng: coords[0]
                });
            } else {
                console.error('Adresse non trouvée:', cleanedAddress);
                callback(null);
            }
        })
        .catch(error => {
            console.error('Erreur de géocodage:', error);
            callback(null);
        });
}


// Nouvelle fonction pour récupérer la région
function getRegionFromAddress(address, callback) {
    const cleanedAddress = address.replace(/,/g, '');
    const url = `https://data.geopf.fr/geocodage/search?q=${encodeURIComponent(cleanedAddress)}&limit=1`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.features && data.features.length > 0) {
                const context = data.features[0].properties.context;
                const contextParts = context.split(',');
                const region = contextParts[contextParts.length - 1]?.trim();
                
                callback(region);
            } else {
                console.log('❌ Aucune région trouvée pour:', address);
                console.log('--------------------------------');
                callback(null);
            }
        })
        .catch(error => {
            console.error('🚨 Erreur lors de la récupération de la région:', error);
            console.error('Pour l\'adresse:', address);
            console.log('--------------------------------');
            callback(null);
        });
}

// =====================
// GESTION DE LA RECHERCHE
// =====================
function initSearch() {
    const searchInput = document.getElementById('searchInput');
    const clearSearchBtn = document.getElementById('clearSearch');
    
    searchInput.addEventListener('input', handleSearchInput);
    clearSearchBtn.addEventListener('click', clearSearch);

    searchInput.addEventListener('click', function(e) {
        const suggestionsContainer = document.getElementById('searchSuggestions');
        if (this.value.trim() === '') {
            const suggestions = getSearchSuggestions('');
            if (suggestions.length > 0) {
                displaySuggestions(suggestions);
            }
        } else {
            handleSearchInput({target: this});
        }
    });
    
    document.addEventListener('click', function(e) {
        const suggestionsContainer = document.getElementById('searchSuggestions');
        const searchInput = document.getElementById('searchInput');
        
        if (e.target !== searchInput && !suggestionsContainer.contains(e.target)) {
            suggestionsContainer.style.display = 'none';
        }
    });
}

function handleSearchInput(e) {
    const query = e.target.value.trim().toLowerCase();
    const suggestionsContainer = document.getElementById('searchSuggestions');
    
    if (query.length === 0) {
        suggestionsContainer.style.display = 'none';
        applyFilters();
        return;
    }
    
    const searchFiltered = allFormations.filter(f => 
        f.nom.toLowerCase().includes(query) || 
        (allOrganismes[f.id_organisme]?.nom.toLowerCase().includes(query)) ||
        (allOrganismes[f.id_organisme]?.adresse.toLowerCase().includes(query))
    );
    
    const filteredFormations = applyFiltersToFormations(searchFiltered);
    updateDisplayedFormations(filteredFormations);
    
    const suggestions = getSearchSuggestions(query);
    if (suggestions.length > 0) {
        displaySuggestions(suggestions);
    } else {
        suggestionsContainer.style.display = 'none';
    }
}

function getSearchSuggestions(query) {
    const suggestions = [];
    
    allFormations.forEach(formation => {
        if (formation.nom.toLowerCase().includes(query)) {
            suggestions.push({
                type: 'formation',
                id: formation.id,
                text: formation.nom,
                organisme: allOrganismes[formation.id_organisme]?.nom || '',
                formationType: formation.type
            });
        }
    });
    
    Object.values(allOrganismes).forEach(organisme => {
        const orgNameMatch = organisme.nom.toLowerCase().includes(query);
        const orgAddressMatch = organisme.adresse.toLowerCase().includes(query);
        
        if (orgNameMatch || orgAddressMatch) {
            suggestions.push({
                type: 'organisme',
                id: organisme.id,
                text: organisme.nom,
                adresse: organisme.adresse,
                isAddressMatch: orgAddressMatch && !orgNameMatch
            });
        }
    });
    
    return suggestions
        .sort((a, b) => {
            if (a.text.toLowerCase() === query) return -1;
            if (b.text.toLowerCase() === query) return 1;
            return 0;
        })
        .slice(0, 10);
}

function displaySuggestions(suggestions) {
    const container = document.getElementById('searchSuggestions');
    container.innerHTML = '';

    suggestions.forEach(suggestion => {
        const item = document.createElement('div');
        item.className = 'search-suggestion-item';

        if (suggestion.type === 'formation') {
            item.innerHTML = `
                <i class="fas fa-graduation-cap suggestion-icon"></i>
                <div class="suggestion-text">
                    <strong>${suggestion.text}</strong>
                    <div class="suggestion-detail">${suggestion.organisme}</div>
                </div>
                <span class="suggestion-type ${suggestion.formationType === 'initiale' ? 'initiale' : 'continue'}">
                    ${suggestion.formationType === 'initiale' ? 'I' : 'C'}
                </span>
            `;

            item.addEventListener('click', () => {
                zoomToFormation(suggestion.id);
                document.getElementById('searchInput').value = suggestion.text;
                container.style.display = 'none';
            });
        } else if (suggestion.type === 'organisme') {
            const displayText = suggestion.isAddressMatch ?
                `${suggestion.adresse} (${suggestion.text})` : suggestion.text;

            item.innerHTML = `
                <i class="fas fa-school suggestion-icon"></i>
                <div class="suggestion-text">
                    <strong>${displayText}</strong>
                    ${suggestion.isAddressMatch ? '' : `<div class="suggestion-detail">${suggestion.adresse}</div>`}
                </div>
            `;

            item.addEventListener('click', () => {
                searchOrganisme(suggestion.id);
                document.getElementById('searchInput').value = suggestion.isAddressMatch ?
                    suggestion.adresse : suggestion.text;
                container.style.display = 'none';
            });
        }

        container.appendChild(item);
    });

    container.style.display = 'block';
}

function zoomToFormation(formationId) {
    const formation = allFormations.find(f => f.id === formationId);
    if (!formation) return;
    
    const organisme = allOrganismes[formation.id_organisme];
    if (!organisme) return;
    
    const marker = markersDict[organisme.id];
    if (marker) {
        const originalLatLng = marker.getLatLng();

        // Décalage en latitude (vers le haut sur la carte)
        const offsetLat = 0.01; // À ajuster selon ton niveau de zoom et le rendu visuel
        const offsetLatLng = L.latLng(originalLatLng.lat + offsetLat, originalLatLng.lng);

        map.setView(offsetLatLng, 14);
        
        const orgFormations = allFormations.filter(f => f.id_organisme === organisme.id);
        let popupContent = `
            <div class="popup-container">
                <h3 class="popup-title">${organisme.nom}</h3>
                <div class="popup-info">
                    <p><i class="fas fa-map-marker-alt"></i> ${organisme.adresse}</p>
                    <p><i class="fas fa-phone"></i> ${organisme.telephone}</p>
                    <p><i class="fas fa-envelope"></i> <a href="mailto:${organisme.email}">${organisme.email}</a></p>
                </div>
                <div class="popup-formations-count">
                    ${orgFormations.length} formation(s) disponible(s)
                </div>
                <a href="/formations/informations/${organisme.id}" class="popup-button">
                    <i class="fas fa-graduation-cap"></i> Découvrir
                </a>
            </div>
        `;
        
        orgFormations.forEach(ff => {
            popupContent += `- ${ff.nom} (${ff.type})<br>`;
        });
        
        marker.setPopupContent(popupContent);
        marker.openPopup();
        
        const container = document.getElementById('formations-container');
        container.innerHTML = '';
        
        orgFormations.forEach(f => {
            if (formationItemsDict[f.id]) {
                container.appendChild(formationItemsDict[f.id]);
            }
        });
        
        highlightFormationItem(formationId, true);
        
        const item = formationItemsDict[formationId];
        if (item && container.firstChild !== item) {
            container.removeChild(item);
            container.insertBefore(item, container.firstChild);
            container.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }
}

function searchOrganisme(organismeId) {
    const organisme = allOrganismes[organismeId];
    if (!organisme) return;

    const marker = markersDict[organisme.id];
    if (marker) {
        const originalLatLng = marker.getLatLng();

        // Décalage en latitude (vers le haut sur la carte)
        const offsetLat = 0.01; // À ajuster selon ton niveau de zoom et le rendu visuel
        const offsetLatLng = L.latLng(originalLatLng.lat + offsetLat, originalLatLng.lng);

        map.setView(offsetLatLng, 14);
        const orgFormations = allFormations.filter(f => f.id_organisme === organisme.id);
        
        let popupContent = `
            <div class="popup-container">
                <h3 class="popup-title">${organisme.nom}</h3>
                <div class="popup-info">
                    <p><i class="fas fa-map-marker-alt"></i> ${organisme.adresse}</p>
                    <p><i class="fas fa-phone"></i> ${organisme.telephone}</p>
                    <p><i class="fas fa-envelope"></i> <a href="mailto:${organisme.email}">${organisme.email}</a></p>
                </div>
                <div class="popup-formations-count">
                    ${orgFormations.length} formation(s) disponible(s)
                </div>
                <a href="/formations/informations/${organisme.id}" class="popup-button">
                    <i class="fas fa-graduation-cap"></i> Découvrir
                </a>
            </div>
        `;
        
        orgFormations.forEach(ff => {
            popupContent += `- ${ff.nom} (${ff.type})<br>`;
        });
        
        marker.setPopupContent(popupContent);
        marker.openPopup();
        
        const container = document.getElementById('formations-container');
        container.innerHTML = '';
        
        orgFormations.forEach(f => {
            if (formationItemsDict[f.id]) {
                container.appendChild(formationItemsDict[f.id]);
            }
        });
        
        if (orgFormations.length > 0) {
            const firstFormationId = orgFormations[0].id;
            highlightFormationItem(firstFormationId, true);
            
            const item = formationItemsDict[firstFormationId];
            if (item && container.firstChild !== item) {
                container.removeChild(item);
                container.insertBefore(item, container.firstChild);
                container.scrollTo({ top: 0, behavior: 'smooth' });
            }
        }
    }
}

function clearSearch() {
    const searchInput = document.getElementById('searchInput');
    const suggestionsContainer = document.getElementById('searchSuggestions');
    
    searchInput.value = '';
    applyFilters();
    
    const suggestions = getSearchSuggestions('');
    if (suggestions.length > 0) {
        displaySuggestions(suggestions);
    } else {
        suggestionsContainer.style.display = 'none';
    }
    
    searchInput.focus();
}

// =====================
// GESTION DES FILTRES
// =====================
function initFilters() {
    // Écouteurs pour les filtres
    document.getElementById('filterToggleBtn').addEventListener('click', toggleFiltersPanel);
    document.getElementById('closeFiltersBtn').addEventListener('click', toggleFiltersPanel);
    document.getElementById('applyFiltersBtn').addEventListener('click', applyFilters);
    document.getElementById('resetFiltersBtn').addEventListener('click', resetFilters);
    
    // Écouteurs pour les cases à cocher
    document.querySelectorAll('input[name="type"]').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                currentFilters.types.add(this.value);
            } else {
                currentFilters.types.delete(this.value);
            }
            applyFilters();
        });
    });
    
    document.querySelectorAll('input[name="label"]').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                currentFilters.labels.add(this.value);
            } else {
                currentFilters.labels.delete(this.value);
            }
            applyFilters();
        });
    });
    
    // Écouteurs pour les selects
    document.getElementById('financementFilter').addEventListener('change', function() {
        currentFilters.financement = this.value;
        applyFilters();
    });
    
    document.getElementById('dureeFilter').addEventListener('change', function() {
        currentFilters.duree = this.value;
        applyFilters();
    });
    
    
    // Écouteurs pour les filtres de prix
    document.getElementById('prixMin').addEventListener('change', function() {
        currentFilters.prixMin = this.value ? parseFloat(this.value) : null;
        applyFilters();
    });
    
    document.getElementById('prixMax').addEventListener('change', function() {
        currentFilters.prixMax = this.value ? parseFloat(this.value) : null;
        applyFilters();
    });
    
    // Écouteurs pour le filtre de région
    document.getElementById('regionFilter').addEventListener('change', function() {
        currentFilters.region = this.value;
        showRegionBoundaries(this.value);
        applyFilters();
    });
}

// Normalisation simple de la durée sélectionnée
function normalizeDuree(duree) {
    switch (duree) {
        case 'jour': return ['jour', 'jours', 'journée', 'journées'];
        case 'heure': return ['heure', 'heures'];
        case 'mois': return ['mois']; // mois est invariant
        case 'an': return ['an', 'ans', 'année', 'années'];
        default: return [];
    }
}


function applyFiltersToFormations(formations) {
    return formations.filter(formation => {
        // Filtre par type
        if (!currentFilters.types.has(formation.type)) return false;
        
        // Filtre par label
        if (formation.label && currentFilters.labels.size > 0) {
            if (!currentFilters.labels.has(formation.label)) return false;
        }
        
        // Filtre par financement
        if (currentFilters.financement) {
            if (!formation.financement) return false;
            if (!formation.financement.includes(currentFilters.financement)) return false;
        }
        
        // Filtre par prix
        if (currentFilters.prixMin !== null && formation.prix !== null) {
            if (formation.prix < currentFilters.prixMin) return false;
        }
        
        if (currentFilters.prixMax !== null && formation.prix !== null) {
            if (formation.prix > currentFilters.prixMax) return false;
        }
        
        // Filtre par durée
        if (currentFilters.duree) {
            const dureeVariantes = normalizeDuree(currentFilters.duree);
            if (!formation.duree) return false;
            const dureeFormation = formation.duree.toLowerCase();
            if (!dureeVariantes.some(variant => dureeFormation.includes(variant))) return false;
        }

        // Filtre par région
        if (currentFilters.region && organismeRegions[formation.id_organisme]) {
            if (organismeRegions[formation.id_organisme] !== currentFilters.region) {
                return false;
            }
        }

        
        return true;
    });
}

function applyFilters() {
    const searchInput = document.getElementById('searchInput');
    const query = searchInput.value.trim().toLowerCase();
    
    let filteredFormations = allFormations;
    
    if (query.length > 0) {
        filteredFormations = allFormations.filter(f => 
            f.nom.toLowerCase().includes(query) || 
            (allOrganismes[f.id_organisme]?.nom.toLowerCase().includes(query)) ||
            (allOrganismes[f.id_organisme]?.adresse.toLowerCase().includes(query))
        );
    }
    
    filteredFormations = applyFiltersToFormations(filteredFormations);
    
    updateDisplayedFormations(filteredFormations);
}

function resetFilters() {
    // Réinitialiser les valeurs
    currentFilters = {
        types: new Set(['initiale', 'continue']),
        labels: new Set(),
        financement: '',
        prixMin: null,
        prixMax: null,
        duree: '',
        region: '', // Réinitialiser le filtre de région
    };
    
    // Mettre à jour l'UI
    document.querySelectorAll('input[name="type"]').forEach(checkbox => {
        checkbox.checked = true;
    });
    
    document.querySelectorAll('input[name="label"]').forEach(checkbox => {
        checkbox.checked = false;
    });
    
    document.getElementById('financementFilter').value = '';
    document.getElementById('dureeFilter').value = '';
    document.getElementById('prixMin').value = '';
    document.getElementById('prixMax').value = '';
    document.getElementById('regionFilter').value = ''; // Réinitialiser le select de région
    
    // Supprimer le contour de la région
    if (currentRegionLayer) {
        map.removeLayer(currentRegionLayer);
        currentRegionLayer = null;
    }
    
    applyFilters();
}

function toggleFiltersPanel() {
    document.getElementById('filtersPanel').classList.toggle('active');
    document.querySelector('.filters-overlay')?.classList.toggle('active');
}

// =====================
// MISE À JOUR DE L'AFFICHAGE
// =====================
function updateDisplayedFormations(filteredFormations) {
    const container = document.getElementById('formations-container');
    container.innerHTML = '';
    
    formationItemsDict = {};

    filteredFormations.forEach(f => {
        const org = allOrganismes[f.id_organisme];
        if (!org) return;

        if (!formationItemsDict[f.id]) {
            const item = document.createElement('div');
            item.className = 'formation-item';
            item.dataset.formationId = f.id;

            const typeClass = f.type === 'initiale' ? 'type-initiale' : 'type-continue';
            const prixDisplay = f.prix !== null ? `${f.prix} €` : 'Non renseigné';
            
            item.innerHTML = `
                <div class="organisme-name">${org.nom}</div>
                <div class="formation-name">${f.nom}</div>
                <div class="formation-details">
                    <strong>Lieu:</strong> ${f.lieu}<br>
                    <strong>Dates:</strong> ${f.dates}<br>
                    <strong>Durée:</strong> ${f.duree}<br>
                    <strong>Prix:</strong> ${prixDisplay}<br>
                    <strong>Adresse:</strong> ${org.adresse}
                </div>
                <span class="formation-type ${typeClass}">${f.type}</span>
            `;

            item.addEventListener('mouseenter', () => highlightFormationItem(f.id));
            item.addEventListener('mouseleave', () => resetAllFormationItems());
            item.addEventListener('click', () => {
                const marker = markersDict[org.id];
                if (marker) {
                    const originalLatLng = marker.getLatLng();

                    // Décalage en latitude (vers le haut sur la carte)
                    const offsetLat = 0.01; // À ajuster selon ton niveau de zoom et le rendu visuel
                    const offsetLatLng = L.latLng(originalLatLng.lat + offsetLat, originalLatLng.lng);

                    map.setView(offsetLatLng, 14);
                

                    marker.openPopup();
                    highlightFormationItem(f.id, true);
                }
            });

            formationItemsDict[f.id] = item;
        }

        container.appendChild(formationItemsDict[f.id]);
    });
    
    updateMapMarkers(filteredFormations);
}

function updateMapMarkers(filteredFormations) {
    Object.values(markersDict).forEach(marker => {
        map.removeLayer(marker);
    });
    
    const organismesWithFormations = new Set();
    filteredFormations.forEach(f => organismesWithFormations.add(f.id_organisme));
    
    Object.entries(markersDict).forEach(([organismeId, marker]) => {
        if (organismesWithFormations.has(parseInt(organismeId))) {
            marker.addTo(map);
        }
    });
}

// =====================
// CHARGEMENT DES DONNÉES
// =====================
Promise.all([
    fetch('/organismes/all').then(res => res.json()),
    fetch('/formations/valides').then(res => res.json())
])
.then(([organismes, formations]) => {
    allFormations = formations;
    organismes.forEach(org => { 
        allOrganismes[org.id] = org;
        // Récupérer la région pour chaque organisme
        if (org.adresse) {
            getRegionFromAddress(org.adresse, region => {
                if (region) {
                    organismeRegions[org.id] = region;
                }
            });
        }
    });
    
    initSearch();
    initFilters();
    
    updateDisplayedFormations(allFormations);
    
    organismes.forEach(org => {
        if (!org.adresse || markersDict[org.id]) return;
        
        geocodeAddress(org.adresse, coords => {
            if (!coords) return;

            const marker = L.marker([coords.lat, coords.lng]).addTo(map);
            markersDict[org.id] = marker;
            
            const orgFormations = allFormations.filter(f => f.id_organisme === org.id);

            let popupContent = `
                <div class="popup-container">
                    <h3 class="popup-title">${org.nom}</h3>
                    <div class="popup-info">
                        <p><i class="fas fa-map-marker-alt"></i> ${org.adresse}</p>
                        <p><i class="fas fa-phone"></i> ${org.telephone}</p>
                        <p><i class="fas fa-envelope"></i> <a href="mailto:${org.email}">${org.email}</a></p>
                    </div>
                    <div class="popup-formations-count">
                        ${orgFormations.length} formation(s) disponible(s)
                    </div>
                    <a href="/formations/informations/${org.id}" class="popup-button">
                        <i class="fas fa-graduation-cap"></i> Découvrir
                    </a>
                </div>
            `;

            orgFormations.forEach(ff => {
                popupContent += `- ${ff.nom} (${ff.type})<br>`;
            });

            marker.bindPopup(popupContent);

            marker.on('click', () => {
                const firstFormation = orgFormations[0];
                if (firstFormation) {
                    highlightFormationItem(firstFormation.id, true);
                    const container = document.getElementById('formations-container');
                    const item = formationItemsDict[firstFormation.id];
                    if (item && container.firstChild !== item) {
                        container.removeChild(item);
                        container.insertBefore(item, container.firstChild);
                        container.scrollTo({ top: 0, behavior: 'smooth' });
                    }
                }
            });

            marker.on('popupopen', () => {
                const firstFormation = orgFormations[0];
                if (firstFormation) highlightFormationItem(firstFormation.id);
            });
            
            marker.on('popupclose', () => {
                if (currentlyHighlighted) highlightFormationItem(null);
            });
        });
    });
})
.catch(error => console.error('Erreur:', error));

// =====================
// GESTION DU PANNEAU LATERAL (Toggle)
// =====================
document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('toggleBtn');
    const container = document.getElementById('container');
    const icon = toggleBtn.querySelector('i');

    toggleBtn.addEventListener('click', function () {
        container.classList.toggle('collapsed');
        icon.classList.toggle('fa-chevron-left');
        icon.classList.toggle('fa-chevron-right');
    });
});

// Ajouter cette fonction dans carte.js
function showRegionBoundaries(regionName) {
    // Si un layer existe déjà, on le supprime
    if (currentRegionLayer) {
        map.removeLayer(currentRegionLayer);
        currentRegionLayer = null;
    }

    if (!regionName) return;

    // Charger les données GeoJSON des régions
    fetch('/static/data/regions-france.geojson')
        .then(response => response.json())
        .then(data => {
            const region = data.features.find(f => 
                f.properties.nom === regionName || 
                f.properties.nom.includes(regionName)
            );

            if (region) {
                currentRegionLayer = L.geoJSON(region, {
                    style: {
                        color: '#1e90a2', // Couleur du contour
                        weight: 3, // Épaisseur du contour
                        fillOpacity: 0, // Transparence du remplissage
                        opacity: 1 // Opacité du contour
                    }
                }).addTo(map);

                // Ajuster la vue de la carte pour montrer toute la région
                map.fitBounds(currentRegionLayer.getBounds());
            }
        });
}