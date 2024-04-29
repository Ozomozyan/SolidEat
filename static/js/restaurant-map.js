function initMap() {
    var restaurantLocation = {lat: 48.866667, lng: 2.333333}; // Remplacez par vos coordonnées
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 8,
        center: restaurantLocation
    });
    var marker = new google.maps.Marker({
        position: restaurantLocation,
        map: map
    });
}