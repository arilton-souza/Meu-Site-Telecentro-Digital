<script>
  // Inicializa o mapa no container com ID 'map'
  const map = L.map('map').setView([-23.5505, -46.6333], 11); // São Paulo

  // Camada base do OpenStreetMap
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
  }).addTo(map);

  // Locais dos cursos presenciais
  const locaisCursosPresenciais = {
      'CEU Vila Atlântica': [-23.4878, -46.7022],
      'CEU Perus': [-23.4628, -46.7633],
      'CEU Parque Anhanguera': [-23.4419, -46.7458],
      'CEU São Mateus': [-23.5714, -46.4875]
  };

  // Calcula o centro do mapa
  let latSum = 0;
  let lngSum = 0;
  for (const local in locaisCursosPresenciais) {
      const [lat, lng] = locaisCursosPresenciais[local];
      latSum += lat;
      lngSum += lng;
  }
  const latCenter = latSum / Object.keys(locaisCursosPresenciais).length;
  const lngCenter = lngSum / Object.keys(locaisCursosPresenciais).length;

  map.setView([latCenter, lngCenter], 12); // Reposiciona o centro do mapa

  // Adiciona os marcadores com popups
  for (const nome in locaisCursosPresenciais) {
      const [lat, lng] = locaisCursosPresenciais[nome];
      L.marker([lat, lng]).addTo(map)
          .bindPopup(`<strong>${nome}</strong><br>Endereço: Em breve`);
  }
</script>
