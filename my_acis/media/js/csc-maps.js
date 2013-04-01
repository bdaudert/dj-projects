var MEDIA_URL = document.getElementById("MEDIA_URL").value;
var base_dir = '/csc/sw_ckn/'

function precise_round(num,decimals){
return Math.round(num*Math.pow(10,decimals))/Math.pow(10,decimals);
}

function initialize_grid_point_map() {
    var map;
    // Since this map is used in multiple locations in slightly
    //different ways, we need to specify the app. possible values: gp_ts,grid_data 
    var app = document.getElementById("app").value; // Since this map is used in multiple locations
    var lat = document.getElementById("initial_lat").value;
    var lon = document.getElementById("initial_lon").value;
    var zoom_level = document.getElementById("zoom_level").value;
    var myLatlng = new google.maps.LatLng(lat,lon);
    var mapOptions = {
    //center: ll,
    center: myLatlng,
    zoom: 4,
    mapTypeId: google.maps.MapTypeId.HYBRID
    };
    map = new google.maps.Map(document.getElementById("map"),mapOptions);
    infowindow = new google.maps.InfoWindow({
        content: 'oi'
    });

    var marker = new google.maps.Marker({
        draggable: true,
        position: myLatlng,
        map: map,
        title: "Your location"
    });

    google.maps.event.addListener(marker, 'dragend', function (event) {
        infowindow.close();
        var lat = precise_round(event.latLng.lat(),2);
        var lon = precise_round(event.latLng.lng(),2);
        var loc = lon + ',' + lat
        if (app == 'gp_ts'){
            document.getElementById("lat").value = lat;
            document.getElementById("lon").value = lon;
            var href = base_dir +'apps/gridded/grid_point_time_series/?lat=' +
                   lat + '&lon=' + lon;
        }
        else if (app == 'grid_data'){
            document.getElementById("location").value = loc;
            var href = base_dir +'data/gridded/?loc=' +
                   lon + ',' + lat;
        }
        var contentString = '<div id="MarkerWindow">'+
            '<p><b>Lat: </b>' + lat + '<br/>'+
            '<b>Lon: </b>' + lon + '<br/>' +

            '</div>';
        infowindow.setContent(contentString);
        infowindow.open(map, marker);
        myLatlng = google.maps.LatLng(lat,lon);
    });

}//close initialize_grid_point_map

var stnclick;
var boxclick;
var show;
var hide;
function initialize_station_finder() {
    var geocoder = new google.maps.Geocoder();
    var MEDIA_URL = document.getElementById("MEDIA_URL").value;
    var json_file = document.getElementById("json_file").value;
    if (document.getElementById("start_date")) {
        var start_date = document.getElementById("start_date").value;
    } 
    else { var start_date = null }
    if (document.getElementById("end_date")) {
        var end_date = document.getElementById("end_date").value;
    }
    else { var end_date = null }
    if (document.getElementById("elements")) {
        var elements = document.getElementById("elements").value;
    }
    else { var elements = null } 
    
    $.getJSON(MEDIA_URL + 'tmp/' + json_file, function(data) {

        //for (first in data.stations) var ll = new google.maps.LatLng(first.lat,first.lon);
        var ll = new google.maps.LatLng(data.stations[0].lat, data.stations[0].lon);
        var mapOptions = {
        center:ll,
        zoom:7,
        mapTypeId:google.maps.MapTypeId.HYBRID
        };

        var map = new google.maps.Map(document.getElementById("map"),mapOptions);
        
        var legend = document.getElementById('map_legend');
        for (var key in data.network_codes) {
            var name = data.network_codes[key];
            var icon = 'http://maps.google.com/mapfiles/ms/icons/' + data.network_icons[key] + '.png';
            var div = document.createElement('div');
            if (data.network_codes[key] == "COOP"){
                //show("COOP");
                div.innerHTML = '<img src="' + icon + '"> ' + name +': <input type="checkbox" id="'+ name +
                                '" onclick="my_boxclick(this,\''+ name +'\')" checked />';
            }
            else {
                div.innerHTML = '<img src="' + icon + '"> ' + name +': <input type="checkbox" id="'+ name +
                '" onclick="my_boxclick(this,\''+ name +'\')"/>';
            }
            legend.appendChild(div);
        }

        var bounds=new google.maps.LatLngBounds();

        infowindow = new google.maps.InfoWindow({
            content: 'oi'
        });
        var markers = [];
        var tbl_rows = [];
        //Define markers and table rows
        $.each(data.stations, function(index, c) {
            //Define markers
            var latlon = new google.maps.LatLng(c.lat,c.lon);
            var marker = new google.maps.Marker({
                map: map,
                position: latlon,
                title:'Name:'+c.name,
                icon: new google.maps.MarkerImage(
                'http://maps.google.com/mapfiles/ms/icons/' + c.marker_icon + '.png'
                )
            });
            marker.category = c.marker_category;
            marker.name = c.name;
            marker.state = c.state;
            marker.lat = c.lat;
            marker.lon = c.lon;
            marker.elevation = c.elevation;
            marker.networks = c.stn_networks;
            marker.sids = c.sids;
            //Fit map to encompass all markers
            bounds.extend(latlon);

            var avbl_elements = '<br />';
            var greg_flag = false;
            for (var i=0;i<c.available_elements.length;i++){
                avbl_elements = avbl_elements + c.available_elements[i] + '<br />';
                //Check of we should have link to Greg's climate summary pages
                if (c.available_elements[i][0] == 'Maximum Daily Temperature(F)' || c.available_elements[i][0] == 'Minimum Daily Temperature(F)' || c.available_elements[i][0] == 'Precipitation(In)'){
                    if (parseInt(c.available_elements[i][1][0].slice(0,4)) - parseInt(c.available_elements[i][1][1].slice(0,4)) > 5){
                        var greg_flag = true;
                    }
                }
            }

            var wrcc_info_link = new String();
            //if ( c.sids[0] && c.sids[0].length == 6 && greg_flag && !isNaN(c.sids[0].replace(/^[0]/g,"") * 1)){
            if ( c.marker_category == "COOP"){
                var wrcc_info_link = '<a  target="_blank" href="http://www.wrcc.dri.edu/cgi-bin/cliMAIN.pl?'
                + c.state + c.sids[0].substring(2,6) +
                '">Access Climate Summaries for this Station (by WRCC)</a>'
            }

            var data_portal_link = '<a target="_blank" href="' + base_dir + 'data/station/?stn_id=' + c.sids[0];
            var app_portal_link = '<a target="_blank" href="' + base_dir + 'apps/sw_ckn_station_apps/?stn_id=' + c.sids[0]; 
            if (start_date != null){ 
                data_portal_link = data_portal_link + '&start_date=' + start_date;
                app_portal_link = app_portal_link + '&start_date=' + start_date; 
            }
            if (end_date != null){ 
                data_portal_link = data_portal_link + '&end_date=' + end_date;
                app_portal_link = app_portal_link + '&end_date=' + end_date; 
            }
            if (elements != null){ 
                data_portal_link = data_portal_link + '&elements=' + elements;
                app_portal_link = app_portal_link + '&elements=' + elements;
            }
            data_portal_link = data_portal_link + '">Get Data for this Station </a>'
            app_portal_link = app_portal_link + '">Run an analysis on this Station</a>'
            var contentString = '<div id="MarkerWindow">'+
                wrcc_info_link + '<br />' +
                data_portal_link + '<br />' +
                app_portal_link + '<br />' +
                '<b>Name: </b><font color="#FF007F">' + c.name + '</font><br/>'+
                '<b>Station IDs: </b>' + c.sids + '<br/>' +
                '<b>NETWORKS: </b>' + c.stn_networks + '<br/>' +
                '<b>State, Elevation, Lat, Lon: </b>' + c.state + ', ' + c.elevation + ', ' + c.lat + ', ' +c.lon +'<br/>' +
                '<b>Available elements with date range: </b>' + avbl_elements + '<br />' +
                '</div>';
            marker.contentString = contentString;

           //Open info window when user clicks on marker
            google.maps.event.addListener(marker, 'click', function() {
                infowindow.close();
                infowindow.setContent(contentString);
                infowindow.open(map, marker);
                });

            //Define table row
            var tbl_row = document.createElement('tr');
            tbl_row.cString = contentString;
            tbl_row.marker = marker;
            tbl_row.onclick = function(){
                infowindow.close();
                infowindow.setContent(this.cString);
                infowindow.open(map, this.marker);
            };
            var t_data = '<td>';
            tbl_row.innerHTML = t_data + c.name + '</td>' + t_data +
                c.state + '</td>' + t_data + c.lat + '</td>' + t_data +
                c.lon + '</td>' + t_data + c.elevation + '</td>' + t_data +
                c.stn_networks +'</td>';

            //Set Initial markers and station list
            if (c.marker_category == "COOP"){
                marker.setVisible(true);
                document.getElementById(c.marker_category).checked = true;
                var station_list = document.getElementById('station_list');
                station_list.appendChild(tbl_row);
            }
            else {
                marker.setVisible(false);
            }
            //Push markesr and table rows into list
            tbl_rows.push(tbl_row);
            markers.push(marker);

        }); //end each

        
        // == shows all markers of a particular category, and ensures the checkbox is checked and write station_list==
        show = function(category) {
            var station_list = document.getElementById('station_list');
            for (var i=0; i<markers.length; i++) {
                if (markers[i].category == category) {
                    markers[i].setVisible(true);
                    station_list.appendChild(tbl_rows[i]);
                    //station_list.sort()
                }
            }
            // == check the checkbox ==
            document.getElementById(category).checked = true;
        };

        // == hides all markers of a particular category, and ensures the checkbox is cleared and delete station_list ==
        hide = function(category) {
            //remove all rows that belong to category
            var station_list = document.getElementById('station_list');
            for (var i=0; i<markers.length; i++) {
                if (markers[i].category == category) {
                    markers[i].setVisible(false);
                    station_list.removeChild(tbl_rows[i]);
                }

            }
            // == clear the checkbox ==
            document.getElementById(category).checked = false;
        };

        boxclick = function(box, category){
            if (box.checked){
                show(category);
            }
            else {
                hide(category);
            }
        };
        //var markerCluster = new MarkerClusterer(map, markers);
        map.fitBounds(bounds);
    });//close getjson


}//close initialize_station_finder

function my_boxclick(box, category){
    boxclick(box, category);
}



function initialize_network_map() {

    var MEDIA_URL = document.getElementById("MEDIA_URL").value;
    var json_file = document.getElementById("json_file").value;
    var marker_type='all';
    $.getJSON(MEDIA_URL + 'json/' + json_file, function(data) {
        //for (first in data.stations) var ll = new google.maps.LatLng(first.lat,first.lon);
        var ll = new google.maps.LatLng(39.5, -98.35);
        var mapOptions = {
        center: ll,
        zoom: 3,
        mapTypeId: google.maps.MapTypeId.HYBRID
        };

        map = new google.maps.Map(document.getElementById("map"),mapOptions);

        var legend = document.getElementById('map_legend');
        for (var i=0; i<data.Types.length; i++) {
            var type = data.Types[i].type;
            var icon = MEDIA_URL + 'img/' + data.Types[i].icon;
            var div = document.createElement('div');
            div.innerHTML = '<p><img class="icon" src="' + icon + '"> ' + type +': <input type="checkbox" id="'+ type + '" onclick="my_networkclick(this,\''+ type +'\')" checked /></p>';
            legend.appendChild(div);
        }

        var bounds=new google.maps.LatLngBounds();
        infowindow = new google.maps.InfoWindow({
            content: 'oi'
        });
        var markers = [];
        $.each(data.OverLays, function(index, c) {
            if (c.type == marker_type || marker_type == 'all') {
                var image = new google.maps.MarkerImage(MEDIA_URL + 'img/' + c.icon,
                    // This marker is 20 pixels wide by 32 pixels tall.
                    new google.maps.Size(30, 30)
                    // The origin for this image is 0,0.
                    //new google.maps.Point(0,0),
                    // The anchor for this image is the base of the flagpole at 0,32.
                    //new google.maps.Point(0, 30)
                );
                var latlon = new google.maps.LatLng(c.lat,c.lon);
                var marker = new google.maps.Marker({
                    map: map,
                    icon: image,
                    position: latlon,
                    title:'Name:'+c.name
                });
                marker.type = c.type;
                markers.push(marker);
                bounds.extend(latlon);
            };//endif

            google.maps.event.addListener(marker, 'click', function() {
                infowindow.close();
                var contentString = '<div id="MarkerWindow">'+
                '<img class="icon" src=' +  MEDIA_URL + 'img/' + c.icon + '>' +
                '<p class="error"><b>' + c.type +'</p><p>' + c.name + '</b><br/>'+
                c.name_long + '<br/>' +
                '<b>Location</b>: ' + c.location +
                '</p>' +'</div>';
                infowindow.setContent(contentString);
                infowindow.open(map, marker);
                //Load longer documentation on right of page
                $("#network_docu").load("/csc/media/html/commons.html #" + c.docu_long);
            });
        });//close each

        //var markerCluster = new MarkerClusterer(map, markers);
        map.fitBounds(bounds);

        // == shows all markers of a particular category, and ensures the checkbox is checked and write station_list==
        show = function(category) {
            for (var i=0; i<markers.length; i++) {
                if (markers[i].type == category) {
                    markers[i].setVisible(true);
                }
            }
            // == check the checkbox ==
            document.getElementById(category).checked = true;
        };

        // == hides all markers of a particular category, and ensures the checkbox is cleared and delete station_list ==
        hide = function(category) {
            for (var i=0; i<markers.length; i++) {
                if (markers[i].type == category) {
                    markers[i].setVisible(false);
                }
            }
            // == clear the checkbox ==
            document.getElementById(category).checked = false;
        };

        networkclick = function(box, category){
            if (box.checked){
                show(category);
            }
            else {
                hide(category);
            }
        };

    });//close getjson
}//close initialize_info_map

function my_networkclick(box, category){
    networkclick(box, category);
}

function initialize_bbox_map() {
      //create map
     var bbox_list = ','.split(document.getElementById("bounding_box").value)
     var west = new google.maps.LatLng(bbox_list[3],bbox_list[0]);
     var south = new google.maps.LatLng(bbox_list[1],bbox_list[0]);
     var east = new google.maps.LatLng(bbox_list[1],bbox_list[2]);
     var north = new google.maps.LatLng(bbox_list[3],bbox_list[2]);
     var initial_rect = [west, south, east, north];

     var Center=new google.maps.LatLng(37.0, -114.05);
     var myOptions = {
        zoom: 5,
        center: Center,
        mapTypeId: google.maps.MapTypeId.HYBRID
      }
     map = new google.maps.Map(document.getElementById('map'), myOptions);
     var rect = new google.maps.Polygon({
         path:initial_rect,
         fillColor: "black",
         fillOpacity: 0.1,
         strokeColor: "black",
         strokeWeight: 1
     });
    rect.setMap(map);

     var drawingManager = new google.maps.drawing.DrawingManager({
        drawingMode: google.maps.drawing.OverlayType.RECTANGLE,
        drawingControl: true,
        drawingControlOptions: {
        position: google.maps.ControlPosition.TOP_CENTER,
        drawingModes: [
            google.maps.drawing.OverlayType.RECTANGLE
            ]
        }, 
        rectangleOptions: {
            editable: true,
            fillColor: "black",
            fillOpacity: 0.1,
            map: map,
            strokeColor: "black",
            strokeWeight: 1
        }
    });
    drawingManager.setMap(map);
    google.maps.event.addListener(drawingManager, 'overlaycomplete', function(event) {
        if (event.type == google.maps.drawing.OverlayType.RECTANGLE) {
            if (rect){
                rect.setMap(null);
            }
            rect = event.overlay;
            var bounds=event.overlay.getBounds();
            //set new bounding box
            var w = precise_round(bounds.getSouthWest().lng(),2);
            var s = precise_round(bounds.getSouthWest().lat(),2);
            var e = precise_round(bounds.getNorthEast().lng(),2);
            var n = precise_round(bounds.getNorthEast().lat(),2);
            document.getElementById("bounding_box").value = w + ',' + s + ',' + e + ',' + n;
        }
        if (event.type == google.maps.drawing.OverlayType.CIRCLE) {
            var radius = event.overlay.getRadius();
        }
    });
}   

