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
    region: '',
    financement: ''
};

// =====================
// HIGHLIGHT D'UNE FORMATION
// =====================
function highlightFormationItem(formationId, isClick = false) {
    resetAllFormationItems(); // Nettoie tous les effets

    if (!formationId) {
        currentlyHighlighted = null;
        return;
    }

    const item = formationItemsDict[formationId];
    if (!item) return;

    // Applique le style de surbrillance
    item.style.transform = 'scale(1.02)';
    item.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)';
    item.style.borderColor = '#1e90a2';
    item.style.borderWidth = '1px';

    // Si c'est un clic (et non un hover), on déplace l'élément en haut
    if (isClick) {
        const container = document.getElementById('formations-container');
        if (container.firstChild !== item) {
            // Vérifier que l'élément est bien dans le container avant de le déplacer
            if (container.contains(item)) {
                container.removeChild(item);
                container.insertBefore(item, container.firstChild);
            }
        }
        container.scrollTo({ top: 0, behavior: 'smooth' });
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
    fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`)
        .then(response => response.json())
        .then(data => {
            if (data && data.length > 0) {
                callback({
                    lat: parseFloat(data[0].lat),
                    lng: parseFloat(data[0].lon)
                });
            } else {
                console.error('Adresse non trouvée:', address);
                callback(null);
            }
        })
        .catch(error => {
            console.error('Erreur de géocodage:', error);
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

    // Gestion du clic sur la barre de recherche
    searchInput.addEventListener('click', function(e) {
        const suggestionsContainer = document.getElementById('searchSuggestions');
        if (this.value.trim() === '') {
            // Si la barre est vide, afficher toutes les suggestions au clic
            const suggestions = getSearchSuggestions('');
            if (suggestions.length > 0) {
                displaySuggestions(suggestions);
            }
        } else {
            // Sinon, afficher les suggestions correspondant au texte actuel
            handleSearchInput({target: this});
        }
    });
    
    document.addEventListener('click', function(e) {
        const suggestionsContainer = document.getElementById('searchSuggestions');
        const searchInput = document.getElementById('searchInput');
        
        // Fermer les suggestions si on clique ailleurs que sur la barre de recherche ou les suggestions
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
        applyFilters(); // Appliquer juste les filtres quand la recherche est vide
        return;
    }
    
    // Filtrer les formations qui correspondent à la recherche
    const searchFiltered = allFormations.filter(f => 
        f.nom.toLowerCase().includes(query) || 
        (allOrganismes[f.id_organisme]?.nom.toLowerCase().includes(query)) ||
        (allOrganismes[f.id_organisme]?.adresse.toLowerCase().includes(query))
    );
    
    // Appliquer les filtres sur les résultats de recherche
    const filteredFormations = applyFiltersToFormations(searchFiltered);
    updateDisplayedFormations(filteredFormations);
    
    // Afficher les suggestions
    const suggestions = getSearchSuggestions(query);
    if (suggestions.length > 0) {
        displaySuggestions(suggestions);
    } else {
        suggestionsContainer.style.display = 'none';
    }
}

function getSearchSuggestions(query) {
    const suggestions = [];
    
    // Suggestions par nom de formation
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
    
    // Suggestions par nom d'organisme et par adresse
    Object.values(allOrganismes).forEach(organisme => {
        const orgNameMatch = organisme.nom.toLowerCase().includes(query);
        const orgAddressMatch = organisme.adresse.toLowerCase().includes(query);
        
        if (orgNameMatch || orgAddressMatch) {
            suggestions.push({
                type: 'organisme',
                id: organisme.id,
                text: organisme.nom,
                adresse: organisme.adresse,
                isAddressMatch: orgAddressMatch && !orgNameMatch // Flag pour savoir si c'est une correspondance d'adresse
            });
        }
    });
    
    // Trier les suggestions pour mettre les correspondances exactes en premier
    return suggestions
        .sort((a, b) => {
            // Priorité aux noms exacts
            if (a.text.toLowerCase() === query) return -1;
            if (b.text.toLowerCase() === query) return 1;
            return 0;
        })
        .slice(0, 10); // Limiter à 10 suggestions
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
                zoomToFormation(suggestion.id); // Zoom + popup + surbrillance formation
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
                searchOrganisme(suggestion.id); // Zoom + popup + surbrillance 1re formation
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
        map.setView(marker.getLatLng(), 14);
        
        // Mettre à jour le contenu du popup
        let popupContent = `
            <b>${organisme.nom}</b><br>
            ${organisme.adresse}<br>
            Tél: ${organisme.telephone}<br>
            Email: <a href="mailto:${organisme.email}">${organisme.email}</a>
            <hr><b>Formations proposées:</b><br>
        `;
        
        const orgFormations = allFormations.filter(f => f.id_organisme === organisme.id);
        orgFormations.forEach(ff => {
            popupContent += `- ${ff.nom} (${ff.type})<br>`;
        });
        
        marker.setPopupContent(popupContent);
        marker.openPopup();
        
        // Filtrer les formations de cet organisme
        const container = document.getElementById('formations-container');
        container.innerHTML = '';
        
        orgFormations.forEach(f => {
            if (formationItemsDict[f.id]) {
                container.appendChild(formationItemsDict[f.id]);
            }
        });
        
        // Mettre en surbrillance la formation sélectionnée
        highlightFormationItem(formationId, true);
        
        // Déplacer la formation en haut de la liste
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
        map.setView(marker.getLatLng(), 14);
        
        // Mettre à jour le contenu du popup
        let popupContent = `
            <b>${organisme.nom}</b><br>
            ${organisme.adresse}<br>
            Tél: ${organisme.telephone}<br>
            Email: <a href="mailto:${organisme.email}">${organisme.email}</a>
            <hr><b>Formations proposées:</b><br>
        `;
        
        const orgFormations = allFormations.filter(f => f.id_organisme === organisme.id);
        orgFormations.forEach(ff => {
            popupContent += `- ${ff.nom} (${ff.type})<br>`;
        });
        
        marker.setPopupContent(popupContent);
        marker.openPopup();
        
        // Filtrer les formations de cet organisme
        const container = document.getElementById('formations-container');
        container.innerHTML = '';
        
        orgFormations.forEach(f => {
            if (formationItemsDict[f.id]) {
                container.appendChild(formationItemsDict[f.id]);
            }
        });
        
        // Mettre en surbrillance la première formation
        if (orgFormations.length > 0) {
            const firstFormationId = orgFormations[0].id;
            highlightFormationItem(firstFormationId, true);
            
            // Déplacer la formation en haut de la liste
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
    applyFilters(); // Réappliquer juste les filtres quand on efface la recherche
    
    // Afficher toutes les suggestions quand on efface la recherche
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
    document.getElementById('regionFilter').addEventListener('change', function() {
        currentFilters.region = this.value;
        applyFilters();
    });
    
    document.getElementById('financementFilter').addEventListener('change', function() {
        currentFilters.financement = this.value;
        applyFilters();
    });
}

function applyFiltersToFormations(formations) {
    return formations.filter(formation => {
        // Filtre par type
        if (!currentFilters.types.has(formation.type)) return false;
        
        // Filtre par label (seulement si au moins un label est sélectionné)
        if (formation.label && currentFilters.labels.size > 0) {
            if (!currentFilters.labels.has(formation.label)) return false;
        }
        
        // Filtre par région
        if (currentFilters.region) {
            const organisme = allOrganismes[formation.id_organisme];
            if (!organisme || !organisme.region) return false;
            if (organisme.region !== currentFilters.region) return false;
        }
        
        // Filtre par financement
        if (currentFilters.financement) {
            if (!formation.financement) return false;
            if (!formation.financement.includes(currentFilters.financement)) return false;
        }
        
        return true;
    });
}
function applyFilters() {
    const searchInput = document.getElementById('searchInput');
    const query = searchInput.value.trim().toLowerCase();
    
    let filteredFormations = allFormations;
    
    // Si une recherche est en cours, filtrer d'abord par recherche
    if (query.length > 0) {
        filteredFormations = allFormations.filter(f => 
            f.nom.toLowerCase().includes(query) || 
            (allOrganismes[f.id_organisme]?.nom.toLowerCase().includes(query)) ||
            (allOrganismes[f.id_organisme]?.adresse.toLowerCase().includes(query))
        );
    }
    
    // Puis appliquer les autres filtres
    filteredFormations = applyFiltersToFormations(filteredFormations);
    
    updateDisplayedFormations(filteredFormations);
}

function resetFilters() {
    // Réinitialiser les valeurs
    currentFilters = {
        types: new Set(['initiale', 'continue']),
        labels: new Set(), // Vide lors de la réinitialisation
        region: '',
        financement: ''
    };
    
    // Mettre à jour l'UI
    document.querySelectorAll('input[name="type"]').forEach(checkbox => {
        checkbox.checked = true;
    });
    
    document.querySelectorAll('input[name="label"]').forEach(checkbox => {
        checkbox.checked = false; // Décocher les labels
    });
    
    document.getElementById('regionFilter').value = '';
    document.getElementById('financementFilter').value = '';
    
    // Réappliquer les filtres
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
    
    formationItemsDict = {}; // Réinitialiser le dictionnaire

    filteredFormations.forEach(f => {
        const org = allOrganismes[f.id_organisme];
        if (!org) return;

        // Créer l'élément si nécessaire
        if (!formationItemsDict[f.id]) {
            const item = document.createElement('div');
            item.className = 'formation-item';
            item.dataset.formationId = f.id;

            const typeClass = f.type === 'initiale' ? 'type-initiale' : 'type-continue';
            item.innerHTML = `
                <div class="organisme-name">${org.nom}</div>
                <div class="formation-name">${f.nom}</div>
                <div class="formation-details">
                    <strong>Lieu:</strong> ${f.lieu}<br>
                    <strong>Dates:</strong> ${f.dates}<br>
                    <strong>Durée:</strong> ${f.duree}<br>
                    <strong>Adresse:</strong> ${org.adresse}
                </div>
                <span class="formation-type ${typeClass}">${f.type}</span>
            `;

            item.addEventListener('mouseenter', () => highlightFormationItem(f.id));
            item.addEventListener('mouseleave', () => resetAllFormationItems());
            item.addEventListener('click', () => {
                const marker = markersDict[org.id];
                if (marker) {
                    map.setView(marker.getLatLng(), 14);
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
    // D'abord cacher tous les marqueurs
    Object.values(markersDict).forEach(marker => {
        map.removeLayer(marker);
    });
    
    // Puis afficher seulement ceux qui correspondent aux filtres
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
    organismes.forEach(org => { allOrganismes[org.id] = org; });
    
    // Initialiser la recherche et les filtres
    initSearch();
    initFilters();
    
    // Afficher toutes les formations initialement
    updateDisplayedFormations(allFormations);
    
    // Créer les marqueurs pour chaque organisme
    organismes.forEach(org => {
        if (!org.adresse || markersDict[org.id]) return;
        
        geocodeAddress(org.adresse, coords => {
            if (!coords) return;

            const marker = L.marker([coords.lat, coords.lng]).addTo(map);
            markersDict[org.id] = marker;

            let popupContent = `
                <b>${org.nom}</b><br>
                ${org.adresse}<br>
                Tél: ${org.telephone}<br>
                Email: <a href="mailto:${org.email}">${org.email}</a>
                <hr><b>Formations proposées:</b><br>
            `;
            
            const orgFormations = allFormations.filter(f => f.id_organisme === org.id);
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