var MAP_APP = MAP_APP || {};
MAP_APP.Utils = {
    update_marker_on_map: function(loc){
        var lat = loc.replace(' ','').split(',')[1];
        var lon = loc.replace(' ','').split(',')[0];
        var mkr_ll = new google.maps.LatLng(parseFloat(lat),parseFloat(lon));
        window.marker.setPosition(mkr_ll);
        window.infowindow = new google.maps.InfoWindow({
            content: '<div id="MarkerWindow" style="line-height:1.35;overflow:hidden;white-space:nowrap;">'+
            '<p><b>Lat: </b>' + lat + '<br/>'+
            '<b>Lon: </b>' + lon + '<br/>' +
            '</div>',
             maxWidth: 100
        });
        window.infowindow.open(window.map, window.marker);
    }
}
