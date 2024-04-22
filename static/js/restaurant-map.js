document.addEventListener('DOMContentLoaded', function() {
    var mapLocation = document.getElementById('restaurant-map').dataset.location;
    var map = L.map('restaurant-map').setView([mapLocation], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    var marker = L.marker([mapLocation]).addTo(map);
    marker.bindPopup("<b>" + "{{ restaurant.name }}" + "</b>").openPopup();
});
