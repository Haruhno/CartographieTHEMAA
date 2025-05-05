// Initialisation de la carte
var map = L.map('map', {
    center: [46.603354, 1.888334],
    zoom: 6,
    maxBounds: [[-90, -Infinity], [90, Infinity]], // Limites verticales seulement
    worldCopyJump: true, // Active la réinitialisation horizontale (comme Google Maps)
    maxBoundsViscosity: 1.0, // Règle les bords "élastiques"
    minZoom: 3,  // Limite de zoom minimal
    maxZoom: 18  // Limite de zoom maximal
});

// Tuiles de type Google Maps (d'autres sources plus adaptées si besoin)
L.tileLayer('https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}', {
    attribution: '&copy; Google',
    maxZoom: 20,
    keepBuffer: 7, // plus large pour éviter les tuiles grises
}).addTo(map);


// Vous pouvez ajouter des marqueurs ici plus tard
L.marker([48.8566, 2.3522]).addTo(map).bindPopup("Paris");
