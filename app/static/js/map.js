'use strict'

mapboxgl.accessToken = 'pk.eyJ1IjoiaGFja2JvdG9uZSIsImEiOiJjanVvdHVkdWUzNmt1NDNwZ24zdGV5Nzl1In0.81ERUqNnNquLDLCB4IRLnA';

let map;
let popup;

loadMap();

function createMap() {
    return (window.map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/light-v10',
        center: [-73.93324, 40.80877],
        zoom: 2
    }));
}

function createPopup() {
    return new mapboxgl.Popup({
        closeButton: false,
        closeOnClick: false
    });
}

function loadMap() {
    const MAP_ID = 'covidStatistics'
    map = createMap();
    popup = createPopup();

    map.on("load", function() {
        map.addSource(MAP_ID, {
            type: "geojson",
            data: geoJSON,
            generateId: true
        });
        map.addLayer({
          id: MAP_ID,
          type: "circle",
          source: MAP_ID,
          opacity: 10,
          paint: {
            "circle-radius": {
              "property": "confirmed",
              "stops": [
                [10, 0.5],
                [500, 1],
                [1000, 2],
                [5000, 2.5],
                [10000, 5],
                [100000, 10],
                [500000, 20],
                [1000000, 25],
                [5000000, 50],
                [10000000, 60]
              ]
            },
            "circle-opacity": 0.8,
            "circle-color": "#4993c7",
            "circle-stroke-color": "#58ade8",
            "circle-stroke-width": 1.5
          }
        });
    });
    map.on("mouseenter", MAP_ID, function(e) {
          map.getCanvas().style.cursor = "pointer";

          let coordinates = e.features[0].geometry.coordinates.slice();
          let popup_view = e.features[0].properties.popup_view;

          popup
            .setLngLat(coordinates)
            .setHTML(popup_view)
            .addTo(map);
    });
    map.on("mouseleave", MAP_ID, function() {
          map.getCanvas().style.cursor = "";
          popup.remove();
    });
}

function flyToCoordinate(data) {
    // remove existing popup
    popup.remove();

    let ZOOM_LEVEL = 4;
    let COUNTRY_BOUNDARIES = 'country-boundaries';

    map.flyTo({
        center: data.coordinates,
        zoom: ZOOM_LEVEL,
        bearing: 0,
        speed: 1,
        curve: 2,
        easing: (t) => t,
        essential: true
    });

    let mapCountryLayer = map.getLayer(COUNTRY_BOUNDARIES);
    if(typeof mapCountryLayer == 'undefined') {
        map.addLayer({
            id: COUNTRY_BOUNDARIES,
            source: {
                type: 'vector',
                url: 'mapbox://mapbox.country-boundaries-v1',
            },
            'source-layer': 'country_boundaries',
            type: 'fill',
            paint: {
                'fill-color': '#e63946',
                'fill-opacity': 0.4,
            },
        }, 'country-label');
    }
    map.setFilter(COUNTRY_BOUNDARIES, [
        "==",
        "iso_3166_1_alpha_3",
        data.code
    ]);
    let lastZoomOffset = map.getZoom();
    map.on('zoom', () => {
        const currentZoomOffset = map.getZoom();
        if (currentZoomOffset === ZOOM_LEVEL) {
            let coordinates = data.coordinates.slice();
            let popup_view = renderPopupView(data.name, data.flag, data.statistics.edges[0].node.confirmed, data.statistics.edges[0].node.deaths);
            popup
                .setLngLat(coordinates)
                .setHTML(popup_view)
                .addTo(map);
        }
        lastZoomOffset = currentZoomOffset;
    });
}
