
function initialize_grid_point_map() {
    var URL_PREFIX = document.getElementById("URL_PREFIX").value;
    var MEDIA_URL = document.getElementById("MEDIA_URL").value;
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
            '<a href="' + URL_PREFIX + '/csc/my_data/apps/climate/grid_point_time_series/?lat=' + 
            event.latLng.lat() + '&lon=' + event.latLng.lng() + 
            '">Use this location</a></div>';
        infowindow.setContent(contentString);
        infowindow.open(map, marker);
        document.getElementById("latbox").value = event.latLng.lat();
        document.getElementById("lonbox").value = event.latLng.lng();
        myLatlng = google.maps.LatLng(event.latLng.lat(),event.latLng.lng());
    });
}//close initialize_grid_point_map 


function initialize_station_finder() {
    var URL_PREFIX = document.getElementById("URL_PREFIX").value;
    var MEDIA_URL = document.getElementById("MEDIA_URL").value;
    var json_file = document.getElementById("json_file").value;
    $.getJSON(MEDIA_URL + 'json/' + json_file, function(data) {


        //for (first in data.stations) var ll = new google.maps.LatLng(first.lat,first.lon);
        var ll = new google.maps.LatLng(data.stations[0].lat, data.stations[0].lon);
        var mapOptions = {
        center: ll,
        //center: new google.maps.LatLng(39.8282, -98.5795),
        zoom: 7,
        mapTypeId: google.maps.MapTypeId.HYBRID
        };

        map = new google.maps.Map(document.getElementById("map"),mapOptions);
        var bounds=new google.maps.LatLngBounds();
        infowindow = new google.maps.InfoWindow({
            content: 'oi'
        });
        var markers = [];
        $.each(data.stations, function(index, c) {
            var latlon = new google.maps.LatLng(c.lat,c.lon);
            var marker = new google.maps.Marker({
                map: map,
                position: latlon,
                title:'Name:'+c.name
            });

            markers.push(marker)
            bounds.extend(latlon);

            google.maps.event.addListener(marker, 'click', function() {
                infowindow.close();
                var contentString = '<div id="MarkerWindow">'+
                '<p><b>Name: </b>' + c.name + '<br/>'+
                '<b>State: </b>' + c.state + '<br/>' +
                '<b>UID: </b>' + c.uid + '<br/>' +
                '<b>SIDS: </b>' + c.sids + '<br/>' +
                '<b>Elevation: </b>' + c.elevation + '<br/>' +
                '</p>' +
                '<a href="' + URL_PREFIX + 'my_data/data/historic/?stn_id=' + c.sids[0] + 
                '">Get Data for this Station</a> <br/>'+
                '<a href="' + URL_PREFIX + '/csc/my_data/apps/climate/?stn_id=' + c.sids[0] + 
                '">Run a climate application for this Station</a>'+ 
                '</div>';
                infowindow.setContent(contentString);
                infowindow.open(map, marker);
                });
        });//close each
    
        var markerCluster = new MarkerClusterer(map, markers);
        map.fitBounds(bounds);
    });//close getjson
}//close initialize_station_finder

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
}//close initialize_finder_map


function load_script() {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = "http://maps.googleapis.com/maps/api/js?key=AIzaSyDIdA3G_Mv7P7OV9jqX2rzChCFu-ut23n0&sensor=false&callback=initialize_map";
  $(".center").append(script);
  //document.body.appendChild(script)
  //document.getElementById("map_js").appendChild(script)
}
