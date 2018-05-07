var map, forwardDirection, backwardDirection;

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

    $.ajax({
        url: '/api/load-stations/',
        type: 'get',
        success: function (response) {
            for (let i = 0; i < response.length; i++) {
                console.log(response[i].coord);
                let marker = L.marker(response[i].coord).addTo(map);
                marker.bindPopup('Ост. <b>' + response[i].name + '</b>')
            }
        },
        error: function (response) {
            console.log('error', response);
        }
    })
}


function selectRoute(obj) {
    var selected = obj.selectedOptions[0];
    var forwardDirectionLngLats = $(selected).data('forward-direction'),
        backwardDirectionLngLats = $(selected).data('backward-direction');
    console.log(forwardDirectionLngLats);
    console.log(backwardDirectionLngLats);
    forwardDirection.setLatLngs(forwardDirectionLngLats);
    backwardDirection.setLatLngs(backwardDirectionLngLats);
    map.fitBounds([forwardDirection.getBounds()._northEast, forwardDirection.getBounds()._southWest])
}

window.onload = loadMap;
