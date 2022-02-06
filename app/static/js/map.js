'use strict'

let mapThemeContainer = document.querySelector('.map-theme-container');
let map;
let popup;
const MAP_ID = 'covidStatistics'
let DEFAULT_STYLE = 'light-v10';
let defaultSelection = true;

let mapStyles = [
    {
        "layer_id": "light-v10",
        "image": "/static/images/light-v10.png"
    },
    {
        "layer_id": "dark-v10",
        "image": "/static/images/dark-v10.png"
    },
    {
        "layer_id": "outdoors-v11",
        "image": "/static/images/outdoors-v11.png"
    }
]
loadMap();

function createMap() {
    mapboxgl.accessToken = 'pk.eyJ1IjoiaGFja2JvdG9uZSIsImEiOiJjanVvdHVkdWUzNmt1NDNwZ24zdGV5Nzl1In0.81ERUqNnNquLDLCB4IRLnA';
    return (window.map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/'+DEFAULT_STYLE,
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
    map.on('idle',function(){
        map.resize();
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
    mapStyleMenu();
}

function mapStyleMenu() {
    for(let i=0; i < mapStyles.length; i++) {
        let container = document.createElement("div");
        container.setAttribute("class", "style-container");
        container.setAttribute("id", "style-container-"+mapStyles[i].layer_id);

        let styleImage = document.createElement("img");
        styleImage.setAttribute("class", "style-thumb");
        styleImage.src = mapStyles[i].image;

        let styleContainer = document.querySelector('#style-container-'+mapStyles[i].layer_id);
        if(styleContainer == null) {
            container.append(styleImage);
            mapThemeContainer.append(container);
        }

        if(defaultSelection) {
            document.querySelector("#style-container-"+mapStyles[0].layer_id).style.border = "3px solid #004e89";
        }
        container.addEventListener("click", function () {
            defaultSelection = false;
            document.querySelectorAll(".style-container").forEach(item => item.style.border = "none");
            document.querySelector("#style-container-"+mapStyles[i].layer_id).style.border = "3px solid #004e89";

            DEFAULT_STYLE = mapStyles[i].layer_id;
            map.setStyle('mapbox://styles/mapbox/' + DEFAULT_STYLE);
            loadMap();
        })
    }
}

function flyToCoordinate(data) {
    /**
     * The below logic is handled for mobile fly to co-ordinate / Map menu selection
     */
    let countryContainer = document.querySelector('.country-container');
    let mapContainer = document.querySelector("#map");
    let mobileNavContainer = document.querySelector('.mobile-nav-container').offsetWidth;
    if(mobileNavContainer > 0) {
        resetMenuSelection();

        // change map item selection
        document.querySelector("#menu-label-"+menu[1].label).style.color = "#407ba7";
        document.querySelector("#menu-label-"+menu[1].label).style.fontWeight = "bold";
        document.querySelector("#menu-icon-"+menu[1].label).style.color = "#FFF";

        countryContainer.style.display = "none";
        mapContainer.style.display = "block";
    }
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
