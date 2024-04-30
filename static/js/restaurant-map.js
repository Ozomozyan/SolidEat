document.addEventListener('DOMContentLoaded', function() {
    var mapLocation = document.getElementById('restaurant-map').dataset.location.split(',');
    var location = { lat: parseFloat(mapLocation[0]), lng: parseFloat(mapLocation[1]) };

    var map = new google.maps.Map(document.getElementById('restaurant-map'), {
        center: location,
        zoom: 13
    });

    var marker = new google.maps.Marker({
        position: location,
        map: map,
        title: '{{ restaurant.name }}'
    });

    var infoWindow = new google.maps.InfoWindow({
        content: '<b>{{ restaurant.name }}</b>'
    });

    marker.addListener('click', function() {
        infoWindow.open(map, marker);
    });

    // Open the popup immediately
    infoWindow.open(map, marker);
});