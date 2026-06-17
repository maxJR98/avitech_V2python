let map;
let marker;

function initMap() {
    const defaultPos = { lat: -17.3895, lng: -66.1568 }; // Ejemplo: Cochabamba
    map = new google.maps.Map(document.getElementById('map'), {
        center: defaultPos,
        zoom: 13
    });
    marker = new google.maps.Marker({
        position: defaultPos,
        map: map,
        draggable: true
    });
    marker.addListener('dragend', function() {
        const pos = marker.getPosition();
        document.getElementById('latitude').value = pos.lat();
        document.getElementById('longitude').value = pos.lng();
    });
}