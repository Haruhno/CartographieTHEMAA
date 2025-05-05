// Initialisation de la carte
var map = L.map('map', {
    center: [46.603354, 1.888334],
    zoom: 6,
    maxBounds: [[-90, -Infinity], [90, Infinity]],
    worldCopyJump: true,
    maxBoundsViscosity: 1.0,
    minZoom: 3,
    maxZoom: 20,
});

// Tuiles de type Google Maps
L.tileLayer('https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}', {
    attribution: '© Google',
    maxZoom: 20,
    keepBuffer: 7,
}).addTo(map);

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

// Récupérer les organismes depuis l'API Flask
fetch('/organismes/all')
    .then(response => response.json())
    .then(organismes => {
        organismes.forEach(organisme => {
            if (organisme.adresse) {
                geocodeAddress(organisme.adresse, (coords) => {
                    if (coords) {
                        const marker = L.marker([coords.lat, coords.lng]).addTo(map);
                        marker.bindPopup(`
                            <b>${organisme.nom}</b><br>
                            ${organisme.adresse}<br>
                            Tél: ${organisme.telephone}<br>
                            Email: <a href="mailto:${organisme.email}">${organisme.email}</a>
                        `);
                    }
                });
            }
        });
    })
    .catch(error => console.error('Erreur:', error));