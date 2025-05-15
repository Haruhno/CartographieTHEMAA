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
var formationItemsDict = {};      // Éléments HTML de formation par organisme ID
var currentlyHighlighted = null;  // Organisme actuellement en surbrillance

// =====================
// HIGHLIGHT D'UNE FORMATION
// =====================
function highlightFormationItem(organismeId, isClick = false) {
    resetAllFormationItems(); // Nettoie tous les effets

    if (!organismeId) {
        currentlyHighlighted = null;
        return;
    }

    const item = formationItemsDict[organismeId];
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
            container.removeChild(item);
            container.insertBefore(item, container.firstChild);
        }
        container.scrollTo({ top: 0, behavior: 'smooth' });
    }

    currentlyHighlighted = organismeId;
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
// CHARGEMENT DES DONNÉES
// =====================
Promise.all([
    fetch('/organismes/all').then(res => res.json()),
    fetch('/formations/valides').then(res => res.json())
])
.then(([organismes, formations]) => {
    const organismesDict = {};
    organismes.forEach(org => { organismesDict[org.id] = org; });

    const container = document.getElementById('formations-container');

    formations.forEach(f => {
        const org = organismesDict[f.id_organisme];
        if (!org) return;

        // Création de l’élément HTML pour chaque formation
        const item = document.createElement('div');
        item.className = 'formation-item';
        item.dataset.organismeId = org.id;

        const typeClass = f.type === 'initiale' ? 'type-initiale' : 'type-continue';
        item.innerHTML = `
            <div class="organisme-name">${org.nom}</div>
            <div class="formation-name">${f.nom}</div>
            <div class="formation-details">
                <strong>Lieu:</strong> ${f.lieu}<br>
                <strong>Dates:</strong> ${f.dates}<br>
                <strong>Durée:</strong> ${f.duree}
            </div>
            <span class="formation-type ${typeClass}">${f.type}</span>
        `;

        // Hover : juste effet visuel
        item.addEventListener('mouseenter', () => highlightFormationItem(org.id));
        item.addEventListener('mouseleave', () => resetAllFormationItems());

        // Clic : zoom, popup, scroll et déplacer
        item.addEventListener('click', () => {
            const marker = markersDict[org.id];
            if (marker) {
                map.setView(marker.getLatLng(), 14);
                marker.openPopup();
                highlightFormationItem(org.id, true);
            }
        });

        container.appendChild(item);
        formationItemsDict[org.id] = item;

        // Ajout du marqueur si pas déjà géolocalisé
        if (!markersDict[org.id] && org.adresse) {
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
                formations.filter(ff => ff.id_organisme === org.id).forEach(ff => {
                    popupContent += `- ${ff.nom} (${ff.type})<br>`;
                });

                marker.bindPopup(popupContent);

                // Clic sur le marqueur = même effet qu’un clic sur la formation
                marker.on('click', () => {
                    highlightFormationItem(org.id, true);
                    const item = formationItemsDict[org.id];
                    if (item) {
                        if (container.firstChild !== item) {
                            container.removeChild(item);
                            container.insertBefore(item, container.firstChild);
                        }
                        container.scrollTo({ top: 0, behavior: 'smooth' });
                    }
                });

                marker.on('popupopen', () => highlightFormationItem(org.id));
                marker.on('popupclose', () => {
                    if (currentlyHighlighted === org.id) highlightFormationItem(null);
                });
            });
        }
    });

    // Clic vide sur la carte = reset
    map.on('click', () => {
        highlightFormationItem(null);
        Object.values(markersDict).forEach(marker => {
            if (marker.isPopupOpen()) marker.closePopup();
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
