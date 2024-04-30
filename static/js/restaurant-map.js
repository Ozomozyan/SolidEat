function initMap() {
    var mapContainer = document.getElementById('restaurant-map');
    if (mapContainer) {
        var location = mapContainer.getAttribute('data-location').split(',');
        var mapOptions = {
            center: new google.maps.LatLng(parseFloat(location[0]), parseFloat(location[1])),
            zoom: 15,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        var map = new google.maps.Map(mapContainer, mapOptions);
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(parseFloat(location[0]), parseFloat(location[1])),
            map: map,
            title: 'Restaurant Location'
        });
    }
}

// Ensure the initMap function is available globally when the Google Maps script calls it
window.initMap = initMap;
