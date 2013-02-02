var MEDIA_URL = document.getElementById("MEDIA_URL").value;
var base_dir = '/csc/sw_ckn/'

function initialize_grid_point_map() {
    var map;
    var center_lat = document.getElementById("center_lat").value;
    var center_lon = document.getElementById("center_lon").value;
    var zoom_level = document.getElementById("zoom_level").value;
    var myLatlng = new google.maps.LatLng(center_lat,center_lon);
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

    google.maps.event.addListener(marker, 'click', function (event) {
        infowindow.close();
        var contentString = '<div id="MarkerWindow">'+
            '<p><b>Lat: </b>' + event.latLng.lat() + '<br/>'+
            '<b>Lon: </b>' + event.latLng.lng() + '<br/>' +
            '<a href="'+ base_dir +'apps/grid_point_time_series/?lat=' +
            event.latLng.lat() + '&lon=' + event.latLng.lng() +
            '">Use this location</a></div>';
        infowindow.setContent(contentString);
        infowindow.open(map, marker);
        document.getElementById("latbox").value = event.latLng.lat();
        document.getElementById("lonbox").value = event.latLng.lng();
        myLatlng = google.maps.LatLng(event.latLng.lat(),event.latLng.lng());
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
        //maxZoom:12,
        mapTypeId:google.maps.MapTypeId.HYBRID
        };

        var map = new google.maps.Map(document.getElementById("map"),mapOptions);
        
        var legend = document.getElementById('map_legend');
        for (var key in data.network_codes) {
          var type = data.network_codes[key];
          var name = data.network_codes[key];
          var icon = 'http://maps.google.com/mapfiles/ms/icons/' + data.network_icons[key] + '.png';
          var div = document.createElement('div');
          div.innerHTML = '<img src="' + icon + '"> ' + name +': <input type="checkbox" id="'+ name + 
          '" onclick="my_boxclick(this,\''+ name +'\')" checked />';
          legend.appendChild(div);
        }

        //map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(legend);
        map.controls.push(legend);

        var bounds=new google.maps.LatLngBounds();

        infowindow = new google.maps.InfoWindow({
            content: 'oi'
        });
        var markers = [];
        //Define markers
        $.each(data.stations, function(index, c) {
            var latlon = new google.maps.LatLng(c.lat,c.lon);
            var marker = new google.maps.Marker({
                map: map,
                position: latlon,
                title:'Name:'+c.name,
                icon: 'http://maps.google.com/mapfiles/ms/icons/' + c.marker_icon + '.png'
                // === Store the category and name info as a marker properties ===
            });
            // === Store the category and name info as a marker properties ===
            marker.category = c.marker_category;
            marker.name = c.name;
            marker.state = c.state;
            marker.lat = c.lat;
            marker.lon = c.lon;
            marker.elevation = c.elevation
            marker.stn_networks = c.stn_networks
            marker.sids = c.sids
            markers.push(marker);
            
            //Fit map to encompass all markers
            bounds.extend(latlon);

            var wrcc_info_link = new String();
            if ( c.sids[0] && c.sids[0].length == 6 && !isNaN(c.sids[0].replace(/^[0]/g,"") * 1)){
                var wrcc_info_link = '<a  target="_blank" href="http://www.wrcc.dri.edu/cgi-bin/cliMAIN.pl?'
                + c.state + c.sids[0].substring(2,6) +
                '">Access Climate Information for this Station</a>'
            }
            var avbl_elements = '<br />';
            for (var i=0;i<c.available_elements.length;i++){
                avbl_elements = avbl_elements + c.available_elements[i] + '<br />';
            }
            var data_portal_link = '<a target="_blank" href="' + base_dir + 'data/historic/?stn_id=' + c.sids[0];
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
            data_portal_link = data_portal_link + '">Get Data for this Station</a>'
            app_portal_link = app_portal_link + '">Run a climate application for this Station</a>'
            var contentString = '<div id="MarkerWindow">'+
                '<p><b>Name: </b>' + c.name + '<br/>'+
                '<b>State: </b>' + c.state + '<br/>' +
                '<b>UID: </b>' + c.uid + '<br/>' +
                '<b>SIDS: </b>' + c.sids + '<br/>' +
                '<b>NETWORKS: </b>' + c.stn_networks + '<br/>' +
                '<b>Elevation: </b>' + c.elevation + '<br/>' +
                '<b>Available Elements: </b>' + avbl_elements +
                '</p>' + wrcc_info_link + '<br />' +
                data_portal_link + '<br />' +
                app_portal_link +
                '</div>';

            //Open info window when user clicks on marker
            google.maps.event.addListener(marker, 'click', function() {
                infowindow.close();
                infowindow.setContent(contentString);
                infowindow.open(map, marker);
                });


            var station_list = document.getElementById('station_list'); 

            if (marker.getVisible()) {
                //tbl_row.onclick = '"my_stnclick(' + infowindow + ',' + marker + ',' + contentString + ')"';
                //t_data = '<td onclick = "my_stnclick(' + infowindow + ',' + marker + ',' + contentString + ')">';
                var tbl_row = document.createElement('tr');
                var t_data = '<td>';
                tbl_row.addEventListener("cick", function(){
                    infowindow.close();
                    infowindow.setContent(contentString);
                    infowindow.open(map, marker);
                }); 
                
                tbl_row.innerHTML = t_data + c.name + '</td>' + t_data + 
                                  c.state + '</td>' + t_data + c.lat + '</td>' + t_data +
                                  c.lon + '</td>' + t_data + c.elevation + '</td>' + t_data + 
                                  c.stn_networks +'</td>';
                station_list.appendChild(tbl_row);
            }
 
        }); //end each
        /*
        //show marker window when station is selected from list
        stnclick = function(i_window, mkr, content_str){
                i_window.close();
                i_window.setContent(content_str);
                i_window.open(map, mkr);
                };
        */
        // == shows all markers of a particular category, and ensures the checkbox is checked ==
        show = function(category) {
            for (var i=0; i<markers.length; i++) {
                if (markers[i].category == category) {
                    markers[i].setVisible(true);
                }
            }
            // == check the checkbox ==
            document.getElementById(category).checked = true;
        };

        // == hides all markers of a particular category, and ensures the checkbox is cleared ==
        hide = function(category) {
            for (var i=0; i<markers.length; i++) {
                if (markers[i].category == category) {
                    markers[i].setVisible(false);
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
        var markerCluster = new MarkerClusterer(map, markers);
        map.fitBounds(bounds);
    });//close getjson


}//close initialize_station_finder

function my_boxclick(box, category){
    boxclick(box, category);
}

/*
function my_stnclick(i_window, mkr, content_str){
    stnclick(i_window, mkr, content_str);
}
*/

function initialize_info_map(node) {

    var MEDIA_URL = document.getElementById("MEDIA_URL").value;
    var json_file = document.getElementById("json_file").value;
    var marker_type = node.id

    $.getJSON(MEDIA_URL + 'json/' + json_file, function(data) {
        //for (first in data.stations) var ll = new google.maps.LatLng(first.lat,first.lon);
        var ll = new google.maps.LatLng(37.0, -114.05);
        var mapOptions = {
        center: ll,
        //center: new google.maps.LatLng(39.8282, -98.5795),
        zoom: 5,
        mapTypeId: google.maps.MapTypeId.HYBRID
        };

        map = new google.maps.Map(document.getElementById("map"),mapOptions);
        var bounds=new google.maps.LatLngBounds();
        infowindow = new google.maps.InfoWindow({
            content: 'oi'
        });
        var markers = [];
        $.each(data.OverLays, function(index, c) {
            if (c.type == marker_type || marker_type == 'all') {
                var image = new google.maps.MarkerImage(MEDIA_URL + 'img/' + c.icon,
                    // This marker is 20 pixels wide by 32 pixels tall.
                    new google.maps.Size(20, 32),
                    // The origin for this image is 0,0.
                    new google.maps.Point(0,0),
                    // The anchor for this image is the base of the flagpole at 0,32.
                    new google.maps.Point(0, 32)
                );
                var latlon = new google.maps.LatLng(c.lat,c.lon);
                var marker = new google.maps.Marker({
                    map: map,
                    icon: image,
                    position: latlon,
                    title:'Name:'+c.name
                });

                markers.push(marker);
                bounds.extend(latlon);
            };//endif

            google.maps.event.addListener(marker, 'click', function() {
                infowindow.close();
                var contentString = '<div id="MarkerWindow">'+
                '<p><b>CSC ' + c.type +': </b>' + c.name + '<br/>'+
                c.name_long + '<br/>' +
                '<b>Latitude: </b>' + c.lat + '<br/>' +
                '<b>Longitude: </b>' + c.lon + '<br/>' +
                '</p>' +'</div>';
                infowindow.setContent(contentString);
                infowindow.open(map, marker);
            });
        });//close each

        //var markerCluster = new MarkerClusterer(map, markers);
        map.fitBounds(bounds);

    });//close getjson
}//close initialize_info_map


function initialize_polygon_map() {
      //create map
     var Center=new google.maps.LatLng(37.0, -114.05);
     var myOptions = {
        zoom: 5,
        center: Center,
        mapTypeId: google.maps.MapTypeId.HYBRID
      }
     map = new google.maps.Map(document.getElementById('map'), myOptions);

     var creator = new PolygonCreator(map);

     //reset
     $('#reset').click(function(){
            creator.destroy();
            creator=null;

            creator=new PolygonCreator(map);
     });


     //show paths
     $('#showData').click(function(){
            $('#dataPanel').empty();
            if(null==creator.showData()){
                $('#dataPanel').append('Please first create a polygon');
            }else{
                $('#dataPanel').append(creator.showData());
            }
     });

     //show color
     $('#showColor').click(function(){
            $('#dataPanel').empty();
            if(null==creator.showData()){
                $('#dataPanel').append('Please first create a polygon');
            }else{
                    $('#dataPanel').append(creator.showColor());
            }
     });
}//close initialize_polygon_map


function load_script() {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = "http://maps.googleapis.com/maps/api/js?key=AIzaSyDIdA3G_Mv7P7OV9jqX2rzChCFu-ut23n0&sensor=false&callback=initialize_map";
  $(".center").append(script);
  //document.body.appendChild(script)
  //document.getElementById("map_js").appendChild(script)
}
