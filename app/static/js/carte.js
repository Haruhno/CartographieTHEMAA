// Initialisation de la carte
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

// Tuiles de type Google Maps
L.tileLayer('https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}', {
    attribution: '© Google',
    maxZoom: 20,
    keepBuffer: 20,
}).addTo(map);

// Ajouter un contrôle de zoom personnalisé
var zoomControl = L.control.zoom({
    position: 'topright'
}).addTo(map);

// Dictionnaires pour stocker les associations
var markersDict = {}; // Marqueurs par organisme ID
var formationItemsDict = {}; // Éléments de formation par organisme ID
var currentlyHighlighted = null; // Garde en mémoire l'élément actuellement mis en avant

// Fonction pour appliquer l'effet de survol à un élément de formation
function highlightFormationItem(organismeId) {
    // Retirer l'effet de tous les éléments d'abord
    resetAllFormationItems();
    
    if (organismeId) {
        // Appliquer l'effet à l'élément correspondant
        const formationItem = formationItemsDict[organismeId];
        if (formationItem) {
            formationItem.style.transform = 'scale(1.02)';
            formationItem.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)';
            formationItem.style.borderColor = '#1e90a2';
            formationItem.style.borderWidth = '1px';
            
            // Faire défiler jusqu'à l'élément si nécessaire
            formationItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            
            currentlyHighlighted = organismeId;
        }
    } else {
        currentlyHighlighted = null;
    }
}

// Fonction pour réinitialiser tous les éléments de formation
function resetAllFormationItems() {
    document.querySelectorAll('.formation-item').forEach(item => {
        item.style.transform = '';
        item.style.boxShadow = '';
        item.style.borderColor = '#b6c6c4';
        item.style.borderWidth = '1px';
    });
}

// Fonction pour géocoder une adresse
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

// Récupérer les organismes et formations depuis l'API Flask
Promise.all([
    fetch('/organismes/all').then(res => res.json()),
    fetch('/formations/valides').then(res => res.json())  // Changé ici
])
.then(([organismes, formations]) => {
    // Créer un dictionnaire des organismes par ID pour un accès rapide
    const organismesDict = {};
    organismes.forEach(organisme => {
        organismesDict[organisme.id] = organisme;
    });
    
    // Afficher les formations dans la liste
    const formationsContainer = document.getElementById('formations-container');
    
    formations.forEach(formation => {
        const organisme = organismesDict[formation.id_organisme];
        
        if (organisme) {
            const formationItem = document.createElement('div');
            formationItem.className = 'formation-item';
            formationItem.dataset.organismeId = organisme.id;
            
            const typeClass = formation.type === 'initiale' ? 'type-initiale' : 'type-continue';
            
            formationItem.innerHTML = `
                <div class="organisme-name">${organisme.nom}</div>
                <div class="formation-name">${formation.nom}</div>
                <div class="formation-details">
                    <strong>Lieu:</strong> ${formation.lieu}<br>
                    <strong>Dates:</strong> ${formation.dates}<br>
                    <strong>Durée:</strong> ${formation.duree}
                </div>
                <span class="formation-type ${typeClass}">${formation.type}</span>
            `;
            
            // Ajouter un effet de survol pour la formation
            formationItem.addEventListener('mouseenter', function() {
                highlightFormationItem(organisme.id);
            });
            
            formationItem.addEventListener('mouseleave', function() {
                this.style.transform = '';
                this.style.boxShadow = '';
                this.style.borderColor = '#b6c6c4';
                this.style.borderWidth = '1px';
            });
            
            // Gestion du clic sur une formation
            formationItem.addEventListener('click', function() {
                const organismeId = this.dataset.organismeId;
                const marker = markersDict[organismeId];
                
                if (marker) {
                    map.setView(marker.getLatLng(), 14);
                    marker.openPopup();
                    highlightFormationItem(organismeId);
                }
            });
            
            formationsContainer.appendChild(formationItem);
            
            // Stocker l'élément dans le dictionnaire
            if (!formationItemsDict[organisme.id]) {
                formationItemsDict[organisme.id] = formationItem;
            }
        }
        
        // Géocodage et ajout des marqueurs pour les organismes
        if (organisme && organisme.adresse && !markersDict[organisme.id]) {
            geocodeAddress(organisme.adresse, (coords) => {
                if (coords) {
                    const marker = L.marker([coords.lat, coords.lng]).addTo(map);
                    
                    // Stocker le marqueur dans le dictionnaire
                    markersDict[organisme.id] = marker;
                    
                    // Créer le contenu du popup
                    let popupContent = `
                        <b>${organisme.nom}</b><br>
                        ${organisme.adresse}<br>
                        Tél: ${organisme.telephone}<br>
                        Email: <a href="mailto:${organisme.email}">${organisme.email}</a>
                        <hr>
                        <b>Formations proposées:</b><br>
                    `;
                    
                    const organismeFormations = formations.filter(f => f.id_organisme === organisme.id);
                    organismeFormations.forEach(f => {
                        popupContent += `- ${f.nom} (${f.type})<br>`;
                    });
                    
                    marker.bindPopup(popupContent);
                    
                    // Gestion du clic sur le marqueur
                    marker.on('click', function() {
                        highlightFormationItem(organisme.id);
                    });
                    
                    // Gestion de l'ouverture du popup
                    marker.on('popupopen', function() {
                        highlightFormationItem(organisme.id);
                    });
                    
                    // Gestion de la fermeture du popup
                    marker.on('popupclose', function() {
                        if (currentlyHighlighted === organisme.id) {
                            highlightFormationItem(null);
                        }
                    });
                }
            });
        }
    });
    
    // Désélectionner quand on clique sur la carte
    map.on('click', function() {
        if (currentlyHighlighted) {
            highlightFormationItem(null);
            // Fermer tous les popups
            Object.values(markersDict).forEach(marker => {
                if (marker.isPopupOpen()) {
                    marker.closePopup();
                }
            });
        }
    });
})
.catch(error => console.error('Erreur:', error));

// Gestion du bouton de basculement du panneau
document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('toggleBtn');
    const formationsList = document.getElementById('formations-list');
    const container = document.getElementById('container');
    const icon = toggleBtn.querySelector('i');

    toggleBtn.addEventListener('click', function () {
        container.classList.toggle('collapsed');

        if (container.classList.contains('collapsed')) {
            icon.classList.remove('fa-chevron-left');
            icon.classList.add('fa-chevron-right');
        } else {
            icon.classList.remove('fa-chevron-right');
            icon.classList.add('fa-chevron-left');
        }
    });
});

