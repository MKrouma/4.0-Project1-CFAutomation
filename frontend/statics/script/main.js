// map class initialize
var map = L.map('map').setView([map_config["center"]["lat"], 
                                map_config["center"]["lon"]], 
                                map_config["zoom_level"]);
map.zoomControl.setPosition(map_config["zoom_controller"]);

// add osm and google satellite basemap
// var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');

var g_sat = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{
    maxZoom: 20,
    subdomains:['mt0','mt1','mt2','mt3']
}).addTo(map);

// layer
// layer style
// var wdpa_style = {
//     "color": "#ece4db",
//     "weight": 0.5,
//     "opacity": 0.5
// };

// var tony_style = {
//     "color": "#3c096c",
//     "weight": 1.5,
//     "opacity": 0.7
// };
// var field = new L.geoJson(field_data, {
//     style: wdpa_style
// });

// field layer
var field = new L.geoJson(field_data).addTo(map);

// bounds layer
var bounds = new L.geoJson(field_bounds).addTo(map); 