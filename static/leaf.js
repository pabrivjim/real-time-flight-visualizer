var mymap = L.map('mapid').setView([47.505, 10.00], 4);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(mymap);

// Create a custom airplane icon
var airplaneIcon = L.icon({
    iconUrl: '/static/airplane-icon.svg',  // Replace with the path to your airplane icon image
    iconSize: [32, 32],  // Adjust the size of the icon as needed
    iconAnchor: [16, 16],  // Adjust the anchor point if necessary
    popupAnchor: [0, -16]  // Adjust the popup anchor if needed
});

var mapMarkers = {}; // Object to store markers for each bus line

var source = new EventSource('/topic/flight_map_topic'); // ENTER YOUR TOPICNAME HERE

source.addEventListener('message', function(e) {
    console.log('Message');
    var data = JSON.parse(e.data);
    console.log(data);

    // Loop through each item in the array
    data.forEach(function(obj) {
        // Check if the bus line property exists in the mapMarkers object
        if (!(obj.hex in mapMarkers)) {
            mapMarkers[obj.hex] = []; // If not, create an empty array for that bus line
        }

        // Check if lat and lng properties are defined and are valid numbers
        if (
            typeof obj.lat === 'number' && !isNaN(obj.lat) &&
            typeof obj.lng === 'number' && !isNaN(obj.lng)
        ) {
            // Remove existing markers for the bus line
            for (var i = 0; i < mapMarkers[obj.hex].length; i++) {
                mymap.removeLayer(mapMarkers[obj.hex][i]);
            }

            // Add a new marker for the bus line with the custom airplane icon
            var marker = L.marker([obj.lat, obj.lng], {icon: airplaneIcon}).addTo(mymap);
            mapMarkers[obj.hex].push(marker);
        } else {
            console.error('Invalid latitude or longitude values:', obj.lat, obj.lng);
        }
    });
}, false);
