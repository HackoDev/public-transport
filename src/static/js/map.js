var map, forwardDirection, backwardDirection, markers = [];

function loadMap() {
    map = L.map("demoMap", {center: [47.2317896, 39.7162282], zoom: 12});
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZ2V0ZnJlc2hiYWtlZCIsImEiOiJjaXBzbjdoZGUwM3oxZnZtMmltazJ0eHU4In0.B9Vu_0d7ZJlCXfwP5V_s5A', {
        maxZoom: 20,
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a>',
        id: 'mapbox.streets'
    }).addTo(map);

    forwardDirection = L.polyline([], {
        color: 'green',
        opacity: 0.5
    }).addTo(map);
    backwardDirection = L.polyline([], {
        color: 'blue',
        opacity: 0.5
    }).addTo(map);
}


function selectRoute(obj) {
    var selectedValue = obj.value,
        forwardDirectionLngLats = mainData[selectedValue].forward_direction,
        backwardDirectionLngLats = mainData[selectedValue].backward_direction,
        stations = mainData[selectedValue].stations;
    console.log(stations);
    forwardDirection.setLatLngs(forwardDirectionLngLats);
    backwardDirection.setLatLngs(backwardDirectionLngLats);
    map.fitBounds([forwardDirection.getBounds()._northEast, forwardDirection.getBounds()._southWest])
    markers.forEach(function (elem) {
        elem.remove();
    });
    for (let i = 0; i < stations.length; i++) {
        let marker = L.marker(stations[i].coord).addTo(map);
        marker.bindPopup('Ост. <b>' + stations[i].name + '</b>');
        markers.push(marker);
    }
}

window.onload = loadMap;
