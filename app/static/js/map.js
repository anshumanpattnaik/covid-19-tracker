'use strict'

mapboxgl.accessToken = 'pk.eyJ1IjoiaGFja2JvdG9uZSIsImEiOiJjanVvdHVkdWUzNmt1NDNwZ24zdGV5Nzl1In0.81ERUqNnNquLDLCB4IRLnA';

loadMap();

function loadMap() {
    const MAP_ID = 'covidStatistics'
    const map = (window.map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/light-v10',
        center: [-73.93324, 40.80877],
        zoom: 2
    }));
    map.on("load", function() {
        map.addSource(MAP_ID, {
            type: "geojson",
            data: geoJSON
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
                [0, 0],
                [100, 1],
                [10000, 10],
                [100000, 25],
                [10000000, 50]
              ]
            },
            "circle-opacity": 0.8,
            "circle-color": {
              "property": "confirmed",
              "stops": [
                [100, "#fca311"],
                [10000, "#ff5400"],
                [100000, "#e5383b"],
                [10000000, "#e63946"]
              ]
            },
            "circle-stroke-color": {
              "property": "confirmed",
              "stops": [
                [100, "#fca311"],
                [10000, "#ff5400"],
                [100000, "#e5383b"],
                [10000000, "#e63946"]
              ]
            },
            "circle-stroke-width": 2
          }
        });
    });
    const popup = new mapboxgl.Popup({
          closeButton: false,
          closeOnClick: false
    });
    map.on("mouseenter", MAP_ID, function(e) {
          map.getCanvas().style.cursor = "pointer";

          let coordinates = e.features[0].geometry.coordinates.slice();
          let name = e.features[0].properties.name;
          let confirmed = e.features[0].properties.confirmed;

          while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
            coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
          }
          popup
            .setLngLat(coordinates)
            .setHTML(name+" == "+confirmed)
            .addTo(map);
    });
    map.on("mouseleave", MAP_ID, function() {
          map.getCanvas().style.cursor = "";
          popup.remove();
    });
}
