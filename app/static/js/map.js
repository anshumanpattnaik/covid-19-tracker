'use strict'

loadMap();

function loadMap() {
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
