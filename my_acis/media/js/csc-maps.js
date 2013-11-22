
//function precise_round(num,decimals){
//return Math.round(num*Math.pow(10,decimals))/Math.pow(10,decimals);
//}

function initialize_grid_point_map() {
    var map;
    // Since this map is used in multiple locations in slightly
    //different ways, we need to specify the app. possible values: gp_ts,grid_data 
    var app = document.getElementById("app").value; // Since this map is used in multiple locations
    var lat = document.getElementById("initial_lat").value;
    var lon = document.getElementById("initial_lon").value;
    var zoom_level = document.getElementById("zoom_level").value;
    var DATA_URL = document.getElementById("DATA_URL").value;
    var TOOLS_URL = document.getElementById("TOOLS_URL").value;
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
            var href = TOOLS_URL +'gridded/grid_point_time_series/?lat=' +
                   lat + '&lon=' + lon;
        }
        else if (app == 'grid_data'){
            document.getElementById("location").value = loc;
            var href = DATA_URL +'gridded/?loc=' +
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
    var DATA_URL = document.getElementById("DATA_URL").value;
    var TOOLS_URL = document.getElementById("TOOLS_URL").value;
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
    //Read in stn data json file
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
        //Sort network_codes according to Kelly's preference and append to legend:
        for (var key in data.network_codes) {
            var name = data.network_codes[key];
            var icon = 'http://maps.google.com/mapfiles/ms/icons/' + data.network_icons[key] + '.png';
            var div = document.createElement('div');
            if (data.network_codes[key] == "COOP"){
                div.innerHTML = '<input type="checkbox" id="'+ name +
                                '" onclick="my_boxclick(this,\''+ name +'\')" checked /> ' + ' <img alt="Icon" title="Icon" src="' + icon + '"> ' + name;
            }
            else {
                div.innerHTML = '<input type="checkbox" id="'+ name +
                '" onclick="my_boxclick(this,\''+ name +'\')"/>' + '<img alt="Icon" title="Icon" src="' + icon + '"> ' + name;
            }
            legend.appendChild(div);
        }
        //Create 'show all networks' button first
        var name = 'All Networks';
        var icon = 'http://thydzik.com/thydzikGoogleMap/markerlink.php?text=A&color=FC6355';
        var div = document.createElement('div');
        div.innerHTML = '<input type="checkbox" id="all" onclick="my_boxclick(this,\'all\')"/>' + ' <img alt="Icon" title="Icon" src="' + icon + '"><b> ' + name + '</b><br /><p class="error">Please be patient while map is loading!</p>';
        legend.appendChild(div);
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

            var data_portal_link = '<a target="_blank" href="' + DATA_URL + 'station/?stn_id=' + c.sids[0];
            var app_portal_link = '<a target="_blank" href="' + TOOLS_URL + 'station/?stn_id=' + c.sids[0]; 
            if (start_date != null){ 
                data_portal_link = data_portal_link + '&start_date=' + start_date;
                app_portal_link = app_portal_link + '&start_date=' + start_date; 
            }
            if (end_date != null){ 
                data_portal_link = data_portal_link + '&end_date=' + end_date;
                app_portal_link = app_portal_link + '&end_date=' + end_date; 
            }
            if (elements != null && elements != 'Any climate element'){ 
                data_portal_link = data_portal_link + '&elements=' + elements;
                app_portal_link = app_portal_link + '&elements=' + elements;
            }
            data_portal_link = data_portal_link + '">Obtain Raw Data for this Station </a>'
            app_portal_link = app_portal_link + '">Find Tools/Applications for this Station</a>'
            var contentString = '<div id="MarkerWindow">'+
                wrcc_info_link + '<br />' +
                data_portal_link + '<br />' +
                app_portal_link + '<br />' +
                '<b>Name: </b><font color="#FF007F">' + c.name + '</font><br/>'+
                '<b>Station IDs: </b>' + c.sids + '<br/>' +
                '<b>NETWORKS: </b>' + c.stn_networks + '<br/>' +
                '<b>State, Elev ft, Lat, Lon: </b>' + c.state + ', ' + c.elevation + ', ' + c.lat + ', ' +c.lon +'<br/>' +
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
                if (category == 'all') {
                    markers[i].setVisible(true);
                    station_list.appendChild(tbl_rows[i]);
                    for (var key in data.network_codes) {
                        // == check all the checkboxes ==
                        document.getElementById(data.network_codes[key]).checked = true;
                    }
                    document.getElementById('all').checked = true;
                }
                else if (markers[i].category == category) {
                    markers[i].setVisible(true);
                    station_list.appendChild(tbl_rows[i]);
                    document.getElementById(category).checked = true;
                }
            }
        };

        // == hides all markers of a particular category, and ensures the checkbox is cleared and delete station_list ==
        hide = function(category) {
            //remove all rows that belong to category
            var station_list = document.getElementById('station_list');
            for (var i=0; i<markers.length; i++) {
                if (category == 'all') {
                    markers[i].setVisible(false);
                    station_list.removeChild(tbl_rows[i]);
                    for (var key in data.network_codes) {
                        // == clear all the checkboxes ==
                        document.getElementById(data.network_codes[key]).checked = false;
                    }
                    document.getElementById('all').checked = false;
                }
                else if (markers[i].category == category) {
                    markers[i].setVisible(false);
                    station_list.removeChild(tbl_rows[i]);
                    // == clear the checkbox ==
                    document.getElementById(category).checked = false;
                    //Clear 'show all networks' button
                    document.getElementById('all').checked = false;
                }
            }
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
            div.innerHTML = '<p><img alt="Icon" title="Icon" class="icon" src="' + icon + '"> ' + type +'<input type="checkbox" id="'+ type + '" onclick="my_networkclick(this,\''+ type +'\')" checked /></p>';
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
                '<p class="error"><b>' + c.type + 
                ' <img alt="Icon" title="Icon" class="icon" src=' + MEDIA_URL + 'img/' + c.icon + '>' +
                '</p><p>' + c.name + '</b><br/>'+
                c.name_long + '<br/>' +
                '<b>Location</b>: ' + c.location +
                '</p>' +'</div>';
                infowindow.setContent(contentString);
                infowindow.open(map, marker);
                //Load longer documentation on right of page
                $("#network_docu").load(MEDIA_URL + "html/commons.html #" + c.docu_long);
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
     var bbox_list = ','.split(document.getElementById("bbox").value)
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
            document.getElementById("bbox").value = w + ',' + s + ',' + e + ',' + n;
        }
        if (event.type == google.maps.drawing.OverlayType.CIRCLE) {
            var radius = event.overlay.getRadius();
        }
    });
}   

function initialize_polygon_map() {
      var drawingManager;
      var selectedShape;
      var colors = ['#1E90FF', '#FF1493', '#32CD32', '#FF8C00', '#4B0082'];
      var selectedColor;
      var colorButtons = {};

      function clearSelection() {
        if (selectedShape) {
          selectedShape.setEditable(false);
          selectedShape = null;
        }
      }

      function setSelection(shape) {
        clearSelection();
        selectedShape = shape;
        shape.setEditable(true);
        selectColor(shape.get('fillColor') || shape.get('strokeColor'));
      }

      function deleteSelectedShape() {
        if (selectedShape) {
          selectedShape.setMap(null);
        }
      }

      function selectColor(color) {
        selectedColor = color;
        for (var i = 0; i < colors.length; ++i) {
          var currColor = colors[i];
          colorButtons[currColor].style.border = currColor == color ? '2px solid #789' : '2px solid #fff';
        }

        // Retrieves the current options from the drawing manager and replaces the
        // stroke or fill color as appropriate.
        var polylineOptions = drawingManager.get('polylineOptions');
        polylineOptions.strokeColor = color;
        drawingManager.set('polylineOptions', polylineOptions);

        var rectangleOptions = drawingManager.get('rectangleOptions');
        rectangleOptions.fillColor = color;
        drawingManager.set('rectangleOptions', rectangleOptions);

        var circleOptions = drawingManager.get('circleOptions');
        circleOptions.fillColor = color;
        drawingManager.set('circleOptions', circleOptions);

        var polygonOptions = drawingManager.get('polygonOptions');
        polygonOptions.fillColor = color;
        drawingManager.set('polygonOptions', polygonOptions);
      }

      function setSelectedShapeColor(color) {
        if (selectedShape) {
          if (selectedShape.type == google.maps.drawing.OverlayType.POLYLINE) {
            selectedShape.set('strokeColor', color);
          } else {
            selectedShape.set('fillColor', color);
          }
        }
      }

      function makeColorButton(color) {
        var button = document.createElement('span');
        button.className = 'color-button';
        button.style.backgroundColor = color;
        google.maps.event.addDomListener(button, 'click', function() {
          selectColor(color);
          setSelectedShapeColor(color);
        });

        return button;
      }

       function buildColorPalette() {
         var colorPalette = document.getElementById('color-palette');
         for (var i = 0; i < colors.length; ++i) {
           var currColor = colors[i];
           var colorButton = makeColorButton(currColor);
           colorPalette.appendChild(colorButton);
           colorButtons[currColor] = colorButton;
         }
         selectColor(colors[0]);
       }

      function initialize() {
        var lat = document.getElementById("initial_lat").value;
        var lon = document.getElementById("initial_lon").value;
        var myLatlng = new google.maps.LatLng(lat,lon);
        var map = new google.maps.Map(document.getElementById('polymap'), {
          zoom: 4,
          center: myLatlng,
          mapTypeId: google.maps.MapTypeId.HYBRID,
          disableDefaultUI: true,
          zoomControl: true
        });

        var polyOptions = {
          strokeWeight: 0,
          fillOpacity: 0.45,
          editable: true
        };
        // Creates a drawing manager attached to the map that allows the user to draw
        // markers, lines, and shapes.
        drawingManager = new google.maps.drawing.DrawingManager({
          drawingMode: google.maps.drawing.OverlayType.POLYGON,
          markerOptions: {
            draggable: true
          },
          polylineOptions: {
            editable: true
          },
          rectangleOptions: polyOptions,
          circleOptions: polyOptions,
          polygonOptions: polyOptions,
          map: map
        });

        google.maps.event.addListener(drawingManager, 'overlaycomplete', function(e) {
            var newShape = e.overlay;
            newShape.type = e.type;
            if (e.type != google.maps.drawing.OverlayType.MARKER) {
            // Switch back to non-drawing mode after drawing a shape.
            drawingManager.setDrawingMode(null);

            // Add an event listener that selects the newly-drawn shape when the user
            // mouses down on it.
            if (e.type == google.maps.drawing.OverlayType.POLYGON || e.type == google.maps.drawing.OverlayType.POLYLINE) {
                var polygon = newShape.getPath();
                polCoords = [];
                for (var j = 0;j<polygon.length;j++) {
                    var lat = precise_round(polygon.getAt(j).lat(),2);
                    var lon = precise_round(polygon.getAt(j).lng(),2);
                    polCoords.push(lon);
                    polCoords.push(lat);
                }
                document.getElementById("shape").value = polCoords;
            }
            if (e.type == google.maps.drawing.OverlayType.RECTANGLE){
                var bounds=newShape.getBounds();
                //set new bounding box
                var w = precise_round(bounds.getSouthWest().lng(),2);
                var s = precise_round(bounds.getSouthWest().lat(),2);
                var e = precise_round(bounds.getNorthEast().lng(),2);
                var n = precise_round(bounds.getNorthEast().lat(),2);
                document.getElementById("shape").value = w + ',' + s + ',' + e + ',' + n;
            }
            if (e.type == google.maps.drawing.OverlayType.CIRCLE){
                var center = newShape.getCenter();
                var radius = newShape.getRadius();
                document.getElementById("shape").value = precise_round(center.lng(),2) + ',' + precise_round(center.lat(),2) + ',' + precise_round(radius,2);
            }
          }
          else{ //MARKER
            pos = newShape.position;
            document.getElementById("shape").value = precise_round(pos.lng(),2) + ',' + precise_round(pos.lat(),2);
          }
        google.maps.event.addListener(newShape, 'click', function() {
              setSelection(newShape);
            });
        setSelection(newShape);
        });

        // Clear the current selection when the drawing mode is changed, or when the
        // map is clicked.
        google.maps.event.addListener(drawingManager, 'drawingmode_changed', clearSelection);
        google.maps.event.addListener(map, 'click', clearSelection);
        google.maps.event.addDomListener(document.getElementById('delete-button'), 'click', deleteSelectedShape);

        buildColorPalette();
      }
      google.maps.event.addDomListener(window, 'load', initialize);
}

function initialize_polygon_map_new() {
      var drawingManager;
      var selectedShape;
      var colors = ['#1E90FF', '#FF1493', '#32CD32', '#FF8C00', '#4B0082'];
      var selectedColor;
      var colorButtons = {};

      function clearSelection() {
        if (selectedShape) {
          selectedShape.setEditable(false);
          selectedShape = null;
        }
      }

      function setSelection(shape) {
        clearSelection();
        selectedShape = shape;
        shape.setEditable(true);
        selectColor(shape.get('fillColor') || shape.get('strokeColor'));
      }

      function deleteSelectedShape() {
        if (selectedShape) {
          selectedShape.setMap(null);
        }
      }

      function selectColor(color) {
        selectedColor = color;
        for (var i = 0; i < colors.length; ++i) {
          var currColor = colors[i];
          colorButtons[currColor].style.border = currColor == color ? '2px solid #789' : '2px solid #fff';
        }

        // Retrieves the current options from the drawing manager and replaces the
        // stroke or fill color as appropriate.
        var polylineOptions = drawingManager.get('polylineOptions');
        polylineOptions.strokeColor = color;
        drawingManager.set('polylineOptions', polylineOptions);
        
        var rectangleOptions = drawingManager.get('rectangleOptions');
        rectangleOptions.fillColor = color;
        drawingManager.set('rectangleOptions', rectangleOptions);

        var circleOptions = drawingManager.get('circleOptions');
        circleOptions.fillColor = color;
        drawingManager.set('circleOptions', circleOptions);

        var polygonOptions = drawingManager.get('polygonOptions');
        polygonOptions.fillColor = color;
        drawingManager.set('polygonOptions', polygonOptions);
      }

      function setSelectedShapeColor(color) {
        if (selectedShape) {
          if (selectedShape.type == google.maps.drawing.OverlayType.POLYLINE) {
            selectedShape.set('strokeColor', color);
          } else {
            selectedShape.set('fillColor', color);
          }
        }
      }

      function makeColorButton(color) {
        var button = document.createElement('span');
        button.className = 'color-button';
        button.style.backgroundColor = color;
        google.maps.event.addDomListener(button, 'click', function() {
          selectColor(color);
          setSelectedShapeColor(color);
        });

        return button;
      }
       function buildColorPalette() {
         var colorPalette = document.getElementById('color-palette');
         for (var i = 0; i < colors.length; ++i) {
           var currColor = colors[i];
           var colorButton = makeColorButton(currColor);
           colorPalette.appendChild(colorButton);
           colorButtons[currColor] = colorButton;
         }
         selectColor(colors[0]);
       }
    var lat = document.getElementById("initial_lat").value;
    var lon = document.getElementById("initial_lon").value;
    var myLatlng = new google.maps.LatLng(lat,lon);
    var map = new google.maps.Map(document.getElementById('polymap'), {
      zoom: 4,
      center: myLatlng,
      mapTypeId: google.maps.MapTypeId.HYBRID,
      disableDefaultUI: true,
      zoomControl: true
    });

    var polyOptions = {
      strokeWeight: 0,
      fillOpacity: 0.45,
      editable: true
    };
    // Creates a drawing manager attached to the map that allows the user to draw
    // markers, lines, and shapes.
    drawingManager = new google.maps.drawing.DrawingManager({
      drawingMode: google.maps.drawing.OverlayType.POLYGON,
      markerOptions: {
        draggable: true
      },
      polylineOptions: {
        editable: true
      },
      rectangleOptions: polyOptions,
      circleOptions: polyOptions,
      polygonOptions: polyOptions,
      map: map
    });

    google.maps.event.addListener(drawingManager, 'overlaycomplete', function(e) {
        var newShape = e.overlay;
        newShape.type = e.type;
        if (e.type != google.maps.drawing.OverlayType.MARKER) {
        // Switch back to non-drawing mode after drawing a shape.
        drawingManager.setDrawingMode(null);

        // Add an event listener that selects the newly-drawn shape when the user
        // mouses down on it.
        if (e.type == google.maps.drawing.OverlayType.POLYGON || e.type == google.maps.drawing.OverlayType.POLYLINE) {
            var polygon = newShape.getPath();
            polCoords = [];
            for (var j = 0;j<polygon.length;j++) {
                var lat = precise_round(polygon.getAt(j).lat(),2);
                var lon = precise_round(polygon.getAt(j).lng(),2);
                polCoords.push(lon);
                polCoords.push(lat);
            }
            document.getElementById("shape").value = polCoords;
        }
        if (e.type == google.maps.drawing.OverlayType.RECTANGLE){
            var bounds=newShape.getBounds();
            //set new bounding box
            var w = precise_round(bounds.getSouthWest().lng(),2);
            var s = precise_round(bounds.getSouthWest().lat(),2);
            var e = precise_round(bounds.getNorthEast().lng(),2);
            var n = precise_round(bounds.getNorthEast().lat(),2);
            document.getElementById("shape").value = w + ',' + s + ',' + e + ',' + n;
        }
        if (e.type == google.maps.drawing.OverlayType.CIRCLE){
            var center = newShape.getCenter();
            var radius = newShape.getRadius();
            document.getElementById("shape").value = precise_round(center.lng(),2) + ',' + precise_round(center.lat(),2) + ',' + precise_round(radius,2);
        }
      }
      else{ //MARKER
        pos = newShape.position;
        document.getElementById("shape").value = precise_round(pos.lng(),2) + ',' + precise_round(pos.lat(),2);
      }
    google.maps.event.addListener(newShape, 'click', function() {
          setSelection(newShape);
        });
    setSelection(newShape);
    });

    // Clear the current selection when the drawing mode is changed, or when the
    // map is clicked.
    google.maps.event.addListener(drawingManager, 'drawingmode_changed', clearSelection);
    google.maps.event.addListener(map, 'click', clearSelection);
    google.maps.event.addDomListener(document.getElementById('delete-button'), 'click', deleteSelectedShape);
    /*
    if ($('#color-palette').html() == '') {
        buildColorPalette();
    }
    */
    document.getElementById("color-palette").innerHTML = '';
    buildColorPalette();
}

function initialize_map_overlays(type, host, kml_file_path) {
    //type is one of: basin, cwa, climdiv, county
    var myLatLng = new google.maps.LatLng(37.0, -114.05);
    var mapOptions = {
        zoom: 5,
        center: myLatLng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }

    var map = new google.maps.Map(document.getElementById("map-overlay"), mapOptions);
    var infowindow = new google.maps.InfoWindow({
        content: 'oi'
    });
    var Layer = new google.maps.KmlLayer({
        url: 'http://'+ host + kml_file_path,
        suppressInfoWindows: true,
        map: map
    });
    Layer.setMap(map);
    google.maps.event.addListener(Layer, 'click', function(kmlEvent) {
        //var text = kmlEvent.featureData.description;
        document.getElementById(type).value = kmlEvent.featureData.name;
        //showInDiv(text);
        var contentString = '<div id="LayerWindow">'+
            kmlEvent.featureData.description +
            '</div>';
        infowindow.close();
        infowindow.setContent(contentString);
        infowindow.open(map, Layer);
    });

    function showInDiv(text) {
        var sidediv = document.getElementById('content-window');
        sidediv.innerHTML = text;
    }
}
