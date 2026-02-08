(function () {
  const data = window.TRAVEL_MAP_DATA;
  if (!data) {
    return;
  }

  const map = L.map('map').setView(data.center, data.zoom);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  const categoryStyles = {
    places: { color: '#2f6f6d', fillColor: '#2f6f6d' },
    parks: { color: '#5a8f3b', fillColor: '#5a8f3b' },
    museums: { color: '#325a9b', fillColor: '#325a9b' },
    restaurants: { color: '#c7682f', fillColor: '#c7682f' },
    cafes: { color: '#b58a5a', fillColor: '#b58a5a' },
    bars: { color: '#7a4a2f', fillColor: '#7a4a2f' },
    clubs: { color: '#6b3fa0', fillColor: '#6b3fa0' }
  };

  data.points.forEach((point) => {
    const style = categoryStyles[point.type] || categoryStyles.places;
    const marker = L.circleMarker(point.coordinates, {
      radius: 7,
      weight: 2,
      color: style.color,
      fillColor: style.fillColor,
      fillOpacity: 0.9
    }).addTo(map);

    const popup = `
      <div class="popup">
        <strong>${point.name}</strong><br/>
        <span>${point.category}</span><br/>
        <a href="${point.url}">Obrir fitxa</a>
      </div>
    `;
    marker.bindPopup(popup);
  });
})();
