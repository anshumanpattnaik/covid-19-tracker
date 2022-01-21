'use strict'

mapboxgl.accessToken = 'pk.eyJ1IjoiaGFja2JvdG9uZSIsImEiOiJjanVvdHVkdWUzNmt1NDNwZ24zdGV5Nzl1In0.81ERUqNnNquLDLCB4IRLnA';

const map = (window.map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v10',
    center: [-73.93324, 40.80877],
    zoom: 14
}));