// ... (código JavaScript anterior) ...

// Mapa Interativo com Leaflet
const map = L.map('map').setView([-23.5505, -46.6333], 11); // Coordenadas de São Paulo

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
}).addTo(map);

const locaisCursosPresenciais = {
    'ceu-vila-atlantica': [-23.4878, -46.7022],
    'ceu-perus': [-23.4628, -46.7633],
    'ceu-parque-anhanguera': [-23.4419, -46.7458],
    'ceu-sao-mateus': [-23.5714, -46.4875]
};

// Calcula o centroide dos locais
let latSum = 0;
let lngSum = 0;
for (const local in locaisCursosPresenciais) {
    const [lat, lng] = locaisCursosPresenciais[local];
    latSum += lat;
    lngSum += lng;
}
const latCenter = latSum / Object.keys(locaisCursosPresenciais).length;
const lngCenter = lngSum / Object.keys(locaisCursosPresenciais).length;

// Centraliza o mapa no centroide
map.setView([latCenter, lngCenter], 12); // Ajuste o nível de zoom conforme necessário

// Adiciona marcadores para os locais dos cursos presenciais
for (const local in locaisCursosPresenciais) {
    const [lat, lng] = locaisCursosPresenciais[local];
    L.marker([lat, lng]).addTo(map)
        .bindPopup(`<strong>${local}</strong><br>Endereço: ...`); // Adicione o endereço
}

// ... (resto do código JavaScript) ...