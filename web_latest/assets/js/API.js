
var map;										

// import dummyRestaurants from "../xinyi.json";

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: new google.maps.LatLng(24.9537, 121.2256),
        mapTypeId: 'terrain'
    });

    // map.data.loadGeoJson('xinyi.json');											

    for (var i = 0; i < 10; i++) {
        // const marker = new google.maps.Marker({position: {lat: i.lat, lng: i.lng}, map: map});
        const marker = new google.maps.Marker({position: {lat: i*0.01 + 24.9537, lng: i*0.01 + 121.2256}, map: map});
        const infowindow = new google.maps.InfoWindow({
        content: "kljljl",
        maxWidth: 200
        });

        marker.addListener('click', function() {
        infowindow.open(map, marker);
        });
    }											

}
