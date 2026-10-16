// ============================================================
// Controlador del Mapa Interactivo Leaflet para el TSP España
// ============================================================

let mapInstance = null;
let tileLayer = null;
let currentRouteLayer = null;
let cityMarkersLayer = null;
let activeRouteKey = 'explorador'; // 'explorador' | 'ga' | 'base' | 'todas'

function initMapaTSP() {
  const mapElement = document.getElementById('mapa-espana');
  if (!mapElement) return;

  // Centro peninsular en Madrid [40.2, -3.7], zoom 6
  mapInstance = L.map('mapa-espana', {
    center: [40.2, -3.7],
    zoom: 6,
    zoomControl: true,
    scrollWheelZoom: false // Evita scroll accidental de la página
  });

  // Habilitar scroll zoom al hacer clic en el mapa
  mapInstance.on('focus', () => { mapInstance.scrollWheelZoom.enable(); });
  mapInstance.on('blur', () => { mapInstance.scrollWheelZoom.disable(); });

  updateMapTileLayer();

  // Capa para marcadores de ciudades
  cityMarkersLayer = L.layerGroup().addTo(mapInstance);
  renderCityMarkers();

  // Capa para las polilíneas de las rutas
  currentRouteLayer = L.layerGroup().addTo(mapInstance);

  // Cargar ruta inicial (ACO Explorador)
  switchRoute('explorador');

  // Configurar listeners de botones de ruta
  document.querySelectorAll('.route-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const routeType = btn.getAttribute('data-route');
      document.querySelectorAll('.route-btn').forEach(b => b.classList.remove('active', 'green', 'blue', 'amber'));
      
      if (routeType === 'explorador') btn.classList.add('active', 'green');
      else if (routeType === 'ga') btn.classList.add('active', 'blue');
      else if (routeType === 'base') btn.classList.add('active', 'amber');
      else btn.classList.add('active');

      switchRoute(routeType);
    });
  });
}

function updateMapTileLayer() {
  if (!mapInstance) return;
  const isLight = document.documentElement.getAttribute('data-theme') === 'light';
  
  if (tileLayer) {
    mapInstance.removeLayer(tileLayer);
  }

  const tileUrl = isLight 
    ? 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png'
    : 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';

  tileLayer = L.tileLayer(tileUrl, {
    attribution: '&copy; <a href="https://carto.com/">CARTO</a> &copy; <a href="https://openstreetmap.org">OSM</a>',
    subdomains: 'abcd',
    maxZoom: 18
  }).addTo(mapInstance);
}

function renderCityMarkers() {
  if (!cityMarkersLayer || typeof CAPITALES_ESPAÑA === 'undefined') return;
  cityMarkersLayer.clearLayers();

  for (const [nombre, data] of Object.entries(CAPITALES_ESPAÑA)) {
    const isMadrid = nombre === 'Madrid';
    
    // Marcador estilizado en SVG
    const markerHtml = isMadrid 
      ? `<div style="width:14px;height:14px;background:#f59e0b;border:2px solid #ffffff;border-radius:50%;box-shadow:0 0 10px #f59e0b;"></div>`
      : `<div style="width:10px;height:10px;background:#6366f1;border:1.5px solid #ffffff;border-radius:50%;box-shadow:0 0 6px rgba(99,102,241,0.6);"></div>`;

    const icon = L.divIcon({
      html: markerHtml,
      className: 'custom-city-marker',
      iconSize: isMadrid ? [14, 14] : [10, 10],
      iconAnchor: isMadrid ? [7, 7] : [5, 5]
    });

    const marker = L.marker([data.lat, data.lon], { icon }).addTo(cityMarkersLayer);
    
    marker.bindPopup(`
      <div style="font-family: var(--font-sans); padding: 4px;">
        <strong style="color: var(--text-main); font-size: 1rem;">${nombre} ${isMadrid ? '⭐ (Salida/Retorno)' : ''}</strong><br>
        <span style="font-size: 0.8rem; color: #94a3b8;">Lat: ${data.lat.toFixed(4)}, Lon: ${data.lon.toFixed(4)}</span>
      </div>
    `);

    marker.bindTooltip(nombre, {
      direction: 'top',
      offset: [0, -6],
      className: 'city-tooltip'
    });
  }
}

function switchRoute(type) {
  if (!currentRouteLayer) return;
  currentRouteLayer.clearLayers();
  activeRouteKey = type;

  const statCostEl = document.getElementById('stat-cost-display');
  const statTitleEl = document.getElementById('stat-title-display');
  const statDiffEl = document.getElementById('stat-diff-display');
  const tramosListEl = document.getElementById('tramos-list-container');

  let activeTramos = [];

  if (type === 'explorador') {
    activeTramos = ITINERARIO_ACO_EXPLORADOR;
    drawRoutePolyline(activeTramos, '#10b981', 3.5, 'solid', 'ACO Explorador');
    if (statCostEl) statCostEl.innerHTML = '1.421,54 €';
    if (statTitleEl) statTitleEl.innerText = 'Colonia de Hormigas (Caso Explorador)';
    if (statDiffEl) statDiffEl.innerText = 'Óptimo Global ACO | 50 hormigas, ρ=0.05, β=2.5';
  } else if (type === 'ga') {
    activeTramos = ITINERARIO_GA;
    drawRoutePolyline(activeTramos, '#6366f1', 3.5, 'solid', 'Algoritmo Genético');
    if (statCostEl) statCostEl.innerHTML = '1.421,04 €';
    if (statTitleEl) statTitleEl.innerText = 'Algoritmo Genético (Cruce OX + Elitismo)';
    if (statDiffEl) statDiffEl.innerText = 'Mejor Solución Absoluta (0.50 € menor que ACO)';
  } else if (type === 'base') {
    activeTramos = ITINERARIO_ACO_BASE;
    drawRoutePolyline(activeTramos, '#f59e0b', 3, '5, 5', 'ACO Base');
    if (statCostEl) statCostEl.innerHTML = '1.474,63 €';
    if (statTitleEl) statTitleEl.innerText = 'Colonia de Hormigas (Caso Base)';
    if (statDiffEl) statDiffEl.innerText = '+53,09 € respecto al óptimo | Parada temprana it. 34';
  } else if (type === 'todas') {
    drawRoutePolyline(ITINERARIO_ACO_EXPLORADOR, '#10b981', 3, 'solid', 'ACO Explorador');
    drawRoutePolyline(ITINERARIO_GA, '#6366f1', 3, 'solid', 'Algoritmo Genético');
    drawRoutePolyline(ITINERARIO_ACO_BASE, '#f59e0b', 2, '5, 5', 'ACO Base');
    if (statCostEl) statCostEl.innerHTML = 'Comparativa';
    if (statTitleEl) statTitleEl.innerText = 'Visualización Simultánea de Rutas';
    if (statDiffEl) statDiffEl.innerText = 'Verde: ACO Explorador | Azul: AG | Naranja: ACO Base';
    activeTramos = ITINERARIO_ACO_EXPLORADOR;
  }

  // Renderizar la lista de los 47 tramos
  renderTramosList(activeTramos, tramosListEl);
}

function drawRoutePolyline(tramos, color, weight, dashArray, label) {
  const latlngs = [];

  tramos.forEach((tr) => {
    const origen = CAPITALES_ESPAÑA[tr.origen];
    const destino = CAPITALES_ESPAÑA[tr.destino];
    if (origen && destino) {
      if (latlngs.length === 0) latlngs.push([origen.lat, origen.lon]);
      latlngs.push([destino.lat, destino.lon]);
    }
  });

  const polyline = L.polyline(latlngs, {
    color: color,
    weight: weight,
    dashArray: dashArray === 'solid' ? null : dashArray,
    opacity: 0.9,
    lineJoin: 'round'
  }).addTo(currentRouteLayer);

  polyline.bindTooltip(label, { sticky: true });
}

function renderTramosList(tramos, container) {
  if (!container) return;
  container.innerHTML = '';

  tramos.forEach(tr => {
    const item = document.createElement('div');
    item.className = 'tramo-item';
    item.innerHTML = `
      <div>
        <strong>#${tr.paso}</strong> ${tr.origen} &rarr; ${tr.destino}
      </div>
      <div style="font-family: var(--font-mono); font-weight: 600; color: var(--accent-emerald);">
        ${tr.costo_tramo.toFixed(2)} €
      </div>
    `;

    item.addEventListener('click', () => {
      const orig = CAPITALES_ESPAÑA[tr.origen];
      const dest = CAPITALES_ESPAÑA[tr.destino];
      if (orig && dest && mapInstance) {
        const bounds = L.latLngBounds([orig.lat, orig.lon], [dest.lat, dest.lon]);
        mapInstance.fitBounds(bounds, { padding: [50, 50], maxZoom: 9 });
      }
    });

    container.appendChild(item);
  });
}

// Escuchar cambios de tema claro/oscuro para actualizar los tiles del mapa
window.addEventListener('themeChanged', () => {
  updateMapTileLayer();
});
