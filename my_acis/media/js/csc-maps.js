//function precise_round(num,decimals){
//return Math.round(num*Math.pow(10,decimals))/Math.pow(10,decimals);
//}

function initialize_grid_point_map(loc) {
    //optional argument location
    switch (arguments.length - 0) { // <-- 0 is number of required arguments
        case 0:  loc = '-111,40';
    } 
    var map;
    var zoom_level = '5';
    var GRID_DATA_URL = document.getElementById("GRID_DATA_URL").value;
    var GRID_TOOLS_URL = document.getElementById("GRID_TOOLS_URL").value;
    var lat = loc.replace(' ','').split(',')[1];
    var lon = loc.replace(' ','').split(',')[0];
    var myLatlng = new google.maps.LatLng(parseFloat(lat),parseFloat(lon));
    var mapOptions = {
    //center: ll,
    center: myLatlng,
    zoom: 4,
    mapTypeId: google.maps.MapTypeId.HYBRID
    };
    map = new google.maps.Map(document.getElementById("map-gridpoint"),mapOptions);
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
        var new_lat = precise_round(event.latLng.lat(),2).toString();
        var new_lon = precise_round(event.latLng.lng(),2).toString();
        var loc = new_lon + ',' + new_lat
        document.getElementById("location").value = loc;
        var href = GRID_DATA_URL +'?loc=' + new_lon + ',' + new_lat;
        var contentString = '<div id="MarkerWindow" style="line-height:1.35;overflow:hidden;white-space:nowrap;">'+
            '<p><b>Lat: </b>' + new_lat + '<br/>'+
            '<b>Lon: </b>' + new_lon + '<br/>' +

            '</div>';
        infowindow.setContent(contentString);
        infowindow.open(map, marker);
        myLatlng = google.maps.LatLng(parseFloat(new_lat),parseFloat(new_lon));
    });

}//close initialize_grid_point_map

/*
//Multiple gridpoints
function initialize_grid_points_map(locs) {
    //optional argument location
    switch (arguments.length - 0) { // <-- 0 is number of required arguments
        case 0:  locs = '-111,40,-111.1,40.5';
    }
    var map,mapOptions,zoom_level = '5';
    var GRID_DATA_URL = document.getElementById("GRID_DATA_URL").value;
    var GRID_TOOLS_URL = document.getElementById("GRID_TOOLS_URL").value;
    var lons = [],lats = [],locs_list, myLatlng;
    locs_list = locs.replace(' ','').split(',');
    for (idx=0;idx<locs;idx++){
        if (idx % 2 == 0){
            lons.push(locs[idx]);
        }
        else {
            lats.push(locs[idx]);
        }
    }
    myLatLng = new google.maps.LatLng(parseFloat(lats[0]),parseFloat(lons[0]));
    mapOptions = {
        center: myLatlng,
        zoom: 4,
        mapTypeId: google.maps.MapTypeId.HYBRID
    };
    map = new google.maps.Map(document.getElementById("map-gridpoint"),mapOptions);
    for (idx=0;idx<lons;idx++){
        myLatlng = new google.maps.LatLng(parseFloat(lat),parseFloat(lon));
        infowindow = new google.maps.InfoWindow({
            content: 'oi'
        });

        var marker = new google.maps.Marker({
            draggable: true,
            position: myLatlng,
            map: map,
            title: "Your locations"
        });
    }
    google.maps.event.addListener(marker, 'dragend', function (event) {
        infowindow.close();
        var new_lat = precise_round(event.latLng.lat(),2).toString();
        var new_lon = precise_round(event.latLng.lng(),2).toString();
        var locs = new_lon + ',' + new_lat
        document.getElementById("location").value = loc;
        var href = GRID_DATA_URL +'?loc=' + new_lon + ',' + new_lat;
        var contentString = '<div id="MarkerWindow" style="line-height:1.35;overflow:hidden;white-space:nowrap;">'+
            '<p><b>Lat: </b>' + new_lat + '<br/>'+
            '<b>Lon: </b>' + new_lon + '<br/>' +

            '</div>';
        infowindow.setContent(contentString);
        infowindow.open(map, marker);
        myLatlng = google.maps.LatLng(parseFloat(new_lat),parseFloat(new_lon));
    });
}//close initialize_grid_points_map
*/
var stnclick;
var boxclick;
var show;
var hide;
function initialize_station_finder() {
    var geocoder = new google.maps.Geocoder();
    var STATION_DATA_URL = document.getElementById("STATION_DATA_URL").value;
    var STATION_TOOLS_URL = document.getElementById("STATION_TOOLS_URL").value;
    var JSON_URL = document.getElementById("JSON_URL").value;
    var TMP_URL = document.getElementById("TMP_URL").value;
    var j_f = document.getElementById("station_json").value;
    if (j_f == "NV_stn.json"){
        //var station_json = '/csc/media/json/' + j_f 
        var station_json = JSON_URL + j_f 
    }
    else {
        //var station_json = '/csc/media/tmp/' + j_f
        var station_json = TMP_URL + j_f
    }

    if (document.getElementById("start_date")) {
        var start_date = document.getElementById("start_date").value;
    } 
    else { var start_date = null }
    if (document.getElementById("end_date")) {
        var end_date = document.getElementById("end_date").value;
    }
    else { var end_date = null }
    if (document.getElementById("elements_str")) {
        var elements = document.getElementById("elements_str").value;
        var el_list = elements.split(',');
    }
    else { var elements = null }
    //Read in stn data json file
    $.getJSON(station_json, function(data) {

        //for (first in data.stations) var ll = new google.maps.LatLng(first.lat,first.lon);
        var ll = new google.maps.LatLng(data.stations[0].lat, data.stations[0].lon);
        var mapOptions = {
        center:ll,
        zoom:7,
        mapTypeId:google.maps.MapTypeId.HYBRID
        };

        var map = new google.maps.Map(document.getElementById("map"),mapOptions);
        
        var legend_table = document.getElementById('map_legend');
        //Sort network_codes according to Kelly's preference and append to legend:
        count = 0;
        var tr = document.createElement('tr');
        for (var key in data.network_codes) {
            count = count + 1;
            var name = data.network_codes[key];
            var icon = 'http://maps.google.com/mapfiles/ms/icons/' + data.network_icons[key] + '.png';
            var td = document.createElement('td');
            //Omit RCC/Misc/Threadex
            if (['RCC','Misc'].indexOf(data.network_codes[key]) >= 0){
                //div.setAttribute("style", "display:none");
                continue
            }
            td.innerHTML = '<input type="checkbox" id="' + name + '"' +
            '" onclick="my_boxclick(this,\''+ name +'\')" checked /> ' +
            '<img style="cursor:pointer;" onclick="ShowNetworkDocu(\'Docu_' + name + '\')" alt="Icon" title="Icon" src="' + icon + '">' + 
            '<div style="cursor:pointer;" onclick="ShowNetworkDocu(\'Docu_' + name + '\')" >' + 
            name + '</div>';
            tr.appendChild(td);
            if (count == 5){
                legend_table.appendChild(tr);
                tr =  document.createElement('tr');

            }
            if (count == 9){
                name = 'All';
                icon = 'http://thydzik.com/thydzikGoogleMap/markerlink.php?text=A&color=FC6355';
                td = document.createElement('td');
                td.innerHTML = '<input type="checkbox" id="all" onclick="my_boxclick(this,\'all\')" checked />' + 
                '<img alt="Icon" title="Icon" src="' + icon  + '">' + name;
                tr.appendChild(td);
                legend_table.appendChild(tr);
            }
        }
        //Adjust map bounds
        var bounds=new google.maps.LatLngBounds();

        //Create info window
        infowindow = new google.maps.InfoWindow({
            content: 'oi'
        });
        var markers = [];
        var tbl_rows = [];
        //for bounds_changed function
        //we need to keep track what markers/stations appear
        var markers_showing = [];
        var tbl_rows_showing = [];
        //Define markers and table rows
        var name_unique = '';
        var marker_count =0;
        $.each(data.stations, function(index, c) {
            //Define markers
            marker_count+=1;
            var latlon = new google.maps.LatLng(c.lat,c.lon);
            var marker = new google.maps.Marker({
                map: map,
                position: latlon,
                title:'Name:'+c.name,
                icon: new google.maps.MarkerImage(
                //'http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_' + c.marker_icon + '.png'
                'http://maps.google.com/mapfiles/ms/icons/' + c.marker_icon + '.png',
                null,
                null, 
                null,
                new google.maps.Size(20,20)
                )
            });
            marker.category = c.marker_category;
            marker.name = c.name;
            marker.state = c.state;
            marker.lat = c.lat;
            marker.lon = c.lon;
            marker.elevation = c.elevation;
            marker.networks = c.stn_networks;
            marker.network = c.stn_network;
            marker.sids = c.sids;
            marker.sid = c.sid;
            //Fit map to encompass all markers
            bounds.extend(latlon);

            var avbl_elements = '<br /><b>' + c.available_elements[0][1] + '</b><br />';
            //var avbl_elements = '<br />'
            var greg_flag = false;
            var dr = c.available_elements[0][1];
            for (var i=0;i<c.available_elements.length;i++){
                if (c.available_elements[i][1].toString() != dr.toString()){
                    dr = c.available_elements[i][1];
                    avbl_elements += '<b>' + c.available_elements[i][1] + '</b><br />';
                }
                avbl_elements += c.available_elements[i][0] + '<br />'     
            }

            var data_portal_link = '<a target="_blank" href="' + STATION_DATA_URL + 
            '?select_stations_by=station_id&station_id=' + c.name + ',' + c.sid; 
            var app_portal_link = '<a target="_blank" href="' + STATION_TOOLS_URL + 
            '?select_stations_by=station_id&station_id=' + c.name + ',' + c.sid;
            var sodsumm_portal_link = '<a target="_blank" href="' + STATION_TOOLS_URL +
            'sodsumm?select_stations_by=station_id&station_id=' + c.name + ',' + c.sid +
            '&start_date=POR&end_date=POR';
            //var metagraph_portal_link = '<a target="_blank" href="' + STATION_TOOLS_URL +
            //'metagraph?select_stations_by=station_id&station_id=' + c.name + ',' + c.sid; 
            if (elements != null){
                data_portal_link = data_portal_link + '&elements=' + elements;
                app_portal_link = app_portal_link + '&elements=' + elements;
            }
            if (start_date != null){ 
                data_portal_link = data_portal_link + '&start_date=' + start_date;
                app_portal_link = app_portal_link + '&start_date=' + start_date; 
            }
            if (end_date != null){ 
                data_portal_link = data_portal_link + '&end_date=' + end_date;
                app_portal_link = app_portal_link + '&end_date=' + end_date; 
            }
            data_portal_link = data_portal_link + '">Obtain data for this station </a>'
            sodsumm_portal_link = sodsumm_portal_link + '">Generate Station Climatology </a>'
            app_portal_link = app_portal_link + '">Run custom data analysis</a>'
            //metagraph_portal_link = data_portal_link + '">Completeness of data collection for maxt/mint/pcpn/snow/snwd</a>'
            var contentString = '<div id="MarkerWindow">'+
                data_portal_link + '<br />' +
                sodsumm_portal_link + '<br />' +
                app_portal_link + '<br />' +
                '<b>Name: </b><font color="#FF007F">' + c.name + '</font><br/>'+
                '<b>Station ID: </b>' + c.sid + '<br/>' +
                //'<b>Other Station IDs: </b>' + c.sids + '<br/>' +
                '<b>Network: </b>' + c.stn_network + '<br/>' +
                //'<b>Other Networks: </b>' + c.stn_networks + '<br/>' +
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
            //Define table row, one entry per station
            var tbl_row = document.createElement('tr');
            tbl_row.cString = contentString;
            tbl_row.name = c.name;
            tbl_row.onclick = function(){
                infowindow.close();
                infowindow.setContent(this.cString);
                infowindow.open(map, marker);
                bound.extend(new google.maps.LatLng(c.lat,c.lon));
            };
            tbl_row.onmouseover = function(){
                tbl_row.style.backgroundColor = "#8FBC8F";
            };
            tbl_row.onmouseout = function(){
                tbl_row.style.backgroundColor = "#FFEFD5";
            };
            var t_data = '<td>';
            tbl_row.innerHTML = t_data + c.name + '</td>' + t_data +
            c.sid + '</td>' + t_data +
            c.state + '</td>' + t_data + c.lat + '</td>' + t_data +
            c.lon + '</td>' + t_data + c.elevation + '</td>' + t_data +
            c.stn_networks +'</td>';
            if (c.name != name_unique){
                name_unique = c.name;
                var station_list = document.getElementById('station_list');
                station_list.appendChild(tbl_row);
            }
            //Complete table row list for on and off switch
            tbl_rows.push(tbl_row);
            tbl_rows_showing.push(tbl_row);
            //Set Initial markers
            marker.setVisible(true);
            document.getElementById(c.marker_category).checked = true;
            //Push markers
            markers.push(marker);
            markers_showing.push(marker);
        }); //end each
        /*
        On zoom change reset the markers
        Note: zoom_changed event fires before the bounds have been recalculated. 
        To bind bounds_changed and work with markers/map stuff we need to work with both, 
        zoom_changed and bounds_changed  
        */
        google.maps.event.addListener(map,"zoom_changed",function() {
            this.zoomChanged = true;
        });
        google.maps.event.addListener(map,"bounds_changed",function() {
            if (this.zoomChanged) {
                this.zoomChanged = false;
            }
            /*
            Reset station_ids_str for link to data finder and table rows:
            Look through currently showing markers and see if they lie within bounds
            of zoomed map
            */
            var station_ids_str = '';
            var station_list = document.getElementById('station_list');
            //var table_rows = station_list.getElementsByTagName('tr'); 
            station_list.innerHTML = ' <thead>' + 
            '<tr><th>Name</th>' +
            '<th>ID</th>' +
            '<th>State</th>' +
            '<th>Lat</th>' +
            '<th>Lon</th>' +
            '<th>Elev</th>' +
            '<th>Networks</th>' +
            '</tr>' +
            '</thead>'; 
            var mapBounds = map.getBounds();
            var name_unique = ''
            for (var i=0; i<markers.length; i++) {
                markers[i].setVisible(false);
                if (mapBounds.contains(new google.maps.LatLng(markers[i].lat, markers[i].lon))) {
                    if (document.getElementById(markers[i].category).checked == true){
                        markers[i].setVisible(true);
                    }
                    // marker is within new bounds
                    //Check if it is currently showing on map
                    if (markers_showing.indexOf(markers[i]) >= 0){
                        if (markers[i].name != name_unique){            
                            station_ids_str+=markers[i].name + ',';
                            station_list.appendChild(tbl_rows[i]);
                            name_unique = markers[i].name;
                        }
                    }
                }
            }
            //Remove trailing comma and set html element
            if (station_ids_str){
                station_ids_str = station_ids_str.substring(0,station_ids_str.length - 2);
            }
            document.getElementById('station_ids_str').value = station_ids_str;
            /*
            //Check  if we should link to data lister (if station_ids_str contains less than 6 stations)
            var stn_list = station_ids_str.split(',');
            var links = document.getElementsByClassName('link_to_datafind');
            if (stn_list.length > 5){
                for (i=0;i<links.length;i++) {
                    links[i].style.display = 'none';
                }
            }
            else {
                for (i=0;i<links.length;i++) {
                    links[i].style.display = 'block';
                }                
            }
            */
        });  
        // == shows all markers of a particular category, and ensures the checkbox is checked and write station_list==
        show = function(category) {
            //Delete old station_list table rows
            var station_list = document.getElementById('station_list');
            station_list.innerHTML = ' <thead>' + 
            '<tr><th>Name</th>' +
            '<th>ID</th>' +
            '<th>State</th>' +
            '<th>Lat</th>' +
            '<th>Lon</th>' +
            '<th>Elev</th>' +
            '<th>Networks</th>' +
            '</tr>' +
            '</thead>';
            var station_ids_str = '';
            var name_unique = '';
            markers_showing = [];
            tbl_rows_showing = [];
            var mapBounds = map.getBounds();
            for (var i=0; i<markers.length; i++) {
                if (category == 'all') {
                    markers[i].setVisible(true);
                    if (mapBounds.contains(new google.maps.LatLng(markers[i].lat, markers[i].lon))){
                    markers_showing.push(markers[i]);
                    tbl_rows_showing.push(tbl_rows[i]);
                    if (markers[i].name != name_unique){
                        station_list.appendChild(tbl_rows[i]);
                        name_unique = markers[i].name;
                        station_ids_str+=markers[i].name + ',';
                    }
                    }
                    for (var key in data.network_codes) {
                        // == check all the checkboxes ==
                        document.getElementById(data.network_codes[key]).checked = true;
                    }
                    //document.getElementById('all').checked = true;
                }
                else if (markers[i].category == category) {
                    markers[i].setVisible(true);
                    markers_showing.push(markers[i]);
                    tbl_rows_showing.push(tbl_rows[i]);
                    station_list.appendChild(tbl_rows[i]);
                    name_unique = markers[i].name;
                    if (mapBounds.contains(new google.maps.LatLng(markers[i].lat, markers[i].lon))){
                        station_list.appendChild(tbl_rows[i]);
                        station_ids_str+=markers[i].name + ',';
                    }
                    document.getElementById(category).checked = true;
                }
                else if (markers[i].category != category && document.getElementById(markers[i].category).checked){
                    markers[i].setVisible(true);
                    if (markers[i].name != name_unique){
                        markers_showing.push(markers[i]);
                        tbl_rows_showing.push(tbl_rows[i]);
                        if (mapBounds.contains(new google.maps.LatLng(markers[i].lat, markers[i].lon))) {
                            station_list.appendChild(tbl_rows[i]);
                            station_ids_str+=markers[i].name + ',';
                        }
                    }
                }
            }
            //Remove trailing comma and set html element
            station_ids_str = station_ids_str.substring(0,station_ids_str.length - 1);
            document.getElementById('station_ids_str').value = station_ids_str;
        };

        // == hides all markers of a particular category, and ensures the checkbox is cleared and delete station_list ==
        hide = function(category) {
            //remove all rows that belong to category
            var station_list = document.getElementById('station_list');
            station_list.innerHTML = ' <thead>' + 
            '<tr><th>Name</th>' +
            '<th>ID</th>' +
            '<th>State</th>' +
            '<th>Lat</th>' +
            '<th>Lon</th>' +
            '<th>Elev</th>' +
            '<th>Networks</th>' +
            '</tr>' +
            '</thead>';;
            var station_ids_str = '';
            name_unique = '';
            markers_showing = [];
            tbl_rows_showing = [];
            var mapBounds = map.getBounds();
            for (var i=0; i<markers.length; i++){
                var name = markers[i].name;
                var cat =markers[i].category;
                station_ids_str+=name + ',';
                var l = (name + ',').length;
                if (category == 'all') {
                    station_ids_str = ''
                    markers[i].setVisible(false);
                    for (var key in data.network_codes) {
                        // == clear all the checkboxes ==
                        document.getElementById(data.network_codes[key]).checked = false;
                    }
                    document.getElementById('all').checked = false;
                }
                else if (cat == category) {
                    markers[i].setVisible(false);
                    station_ids_str = station_ids_str.substring(0,station_ids_str.length - l);
                    // == clear the checkbox ==
                    document.getElementById(category).checked = false;
                    //Clear 'show all networks' button
                    document.getElementById('all').checked = false;
                }
                else if (cat != category && mapBounds.contains(new google.maps.LatLng(markers[i].lat, markers[i].lon))) {
                    if (document.getElementById(cat).checked){
                        markers_showing.push(markers[i]);
                        tbl_rows_showing.push(tbl_rows[i]);
                        station_list.appendChild(tbl_rows[i]);
                        name_unique = markers[i].name;
                    }
                }
            }
            //Remove trailing comma and set html element
            if (station_ids_str){
                station_ids_str = station_ids_str.substring(0,station_ids_str.length - 1);
            }
            document.getElementById('station_ids_str').value = station_ids_str;

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
        //var Center = new google.maps.LatLng(39.5, -98.35);
        var Center =new google.maps.LatLng(37.0, -114.05);
        var mapOptions = {
        center: Center,
        zoom: 5,
        mapTypeId: google.maps.MapTypeId.HYBRID
        };

        map = new google.maps.Map(document.getElementById("map"),mapOptions);

        var legend = document.getElementById('resource_legend');
        var type;
        var icon;
        var div;
        for (var i=0; i<data.Types.length; i++) {
            type = data.Types[i].type;
            icon = MEDIA_URL + 'img/' + data.Types[i].icon;
            div = document.createElement('div');
            div.innerHTML = '<p><img alt="Icon" title="Icon" class="icon" src="' + icon + '"> ' + type +'<input type="checkbox" id="'+ type + '" onclick="my_networkclick(this,\''+ type +'\')" checked /></p>';
            legend.appendChild(div);
        }
        //Create show all
        type = 'All';
        icon = MEDIA_URL + 'img/ALLIcon.png'
        div = document.createElement('div');
        div.innerHTML = '<p><img alt="Icon" title="Icon" class="icon" src="' + icon + '"> ' + type +'<input type="checkbox" id="all" onclick="my_networkclick(this,\''+ 'all' +'\')" checked /></p>';
        legend.appendChild(div);

        var bounds=new google.maps.LatLngBounds();
        infowindow = new google.maps.InfoWindow({
            content: 'oi'
        });
        var markers = [];
        //var checked_categories = document.getElementById('checked_categories').split(',');
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
                $("#network_docu").load(MEDIA_URL + "html/Docu_External_Resources.html #" + c.docu_long);
            });
        });//close each

        //var markerCluster = new MarkerClusterer(map, markers);
        map.fitBounds(bounds);

        // == shows all markers of a particular category, and ensures the checkbox is checked and write station_list==
        show = function(category) {
            for (var i=0; i<markers.length; i++) {
                if (category == 'all'){
                    markers[i].setVisible(true);
                }
                else{
                    if (markers[i].type == category) {
                        markers[i].setVisible(true);
                    }
                }
            }
            // == check the checkbox ==
            if (category == 'all'){
                for (var i=0; i<data.Types.length; i++) {
                    document.getElementById(data.Types[i].type).checked = true;
                }
            }
            else {
                document.getElementById(category).checked = true;
            }
        };

        // == hides all markers of a particular category, and ensures the checkbox is cleared and delete station_list ==
        hide = function(category) {
            for (var i=0; i<markers.length; i++) {
                if (category == 'all'){
                     markers[i].setVisible(false);
                }
                else {
                    if (markers[i].type == category) {
                        markers[i].setVisible(false);
                    }
                }
            }
            // == clear the checkbox ==
            if (category == 'all'){
                for (var i=0; i<data.Types.length; i++) {
                    document.getElementById(data.Types[i].type).checked = false;
                }
            }
            else {
                document.getElementById(category).checked = false;
            }
        };

        networkclick = function(box, category){
            if (box.checked){
                //checked_categories.push(category);
                //document.getElementById('checked_categories').value = checked_categories.join();
                show(category);
            }
            else {
                //remove category form checked list
                /*
                for(var i =0;i<checked_categories.length;i++) {
                    if (checked_categories[i] == category){
                        checked_categories.splice(i,1);
                    }
                }
                document.getElementById('checked_categories').value = checked_categories.join();
                */
                hide(category);
            }
        };
    });//close getjson
}//close initialize_info_map

function my_networkclick(box, category){
    networkclick(box, category);
}

function initialize_bbox_map(bbox) {
    //optional argument location
    switch (arguments.length - 0) { // <-- 0 is number of required arguments
        case 0:  bbox = '-115,34,-114,35';
    }
    var bbox_list = bbox.replace(' ','').split(','); 
    function clearRect() {
        if (rect) {
          rect.setEditable(false);
          rect.setMap(null);
          rect = null;
        }
    }
    var Center=new google.maps.LatLng(parseFloat(bbox_list[1]),parseFloat(bbox_list[0]));
    var mapOptions = {
        zoom: 7,
        center: Center,
        mapTypeId: google.maps.MapTypeId.HYBRID
    }
    map = new google.maps.Map(document.getElementById('map-bbox'), mapOptions);
    var rectangleOptions = {
        editable: true,
        draggable: true,
        fillColor: "#0000FF",
        fillOpacity: 0.1,
        strokeColor: "#0000FF",
        strokeWeight: 1
    }
    rect_initialOptions = {
        bounds:new google.maps.LatLngBounds(
            new google.maps.LatLng(parseFloat(bbox_list[1]),parseFloat(bbox_list[0])),
            new google.maps.LatLng(parseFloat(bbox_list[3]),parseFloat(bbox_list[2]))
        )
    }
    var rect = new google.maps.Rectangle($.extend({},rectangleOptions,rect_initialOptions));
    rect.setMap(map);
    var drawingManager = new google.maps.drawing.DrawingManager({
        drawingModes: [
            google.maps.drawing.OverlayType.RECTANGLE
        ],
        drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_LEFT,
            drawingModes: [
            google.maps.drawing.OverlayType.RECTANGLE
            ]
        },
        rectangleOptions: rectangleOptions,
    });
    drawingManager.setMap(map);
    var bounds = rect.getBounds();
    map.fitBounds(bounds);      
    //Event handlers
    google.maps.event.addListener(map, 'click', clearRect);
    google.maps.event.addListener(drawingManager, 'drawingmode_changed', clearRect);
    google.maps.event.addListener(drawingManager, 'overlaycomplete', function(e) {
        if (rect){
            rect.setMap(null);
        }
        rect = e.overlay;
        var bounds=e.overlay.getBounds();
        //set new bounding box
        var w = precise_round(bounds.getSouthWest().lng(),2);
        var s = precise_round(bounds.getSouthWest().lat(),2);
        var e = precise_round(bounds.getNorthEast().lng(),2);
        var n = precise_round(bounds.getNorthEast().lat(),2);
        //document.getElementById("bbox").value = w + ',' + s + ',' + e + ',' + n;
        document.getElementById("bounding_box").value = w + ',' + s + ',' + e + ',' + n; 
    });
    google.maps.event.addListener(rect, 'bounds_changed', function() {
        var bounds=rect.getBounds();
        //set new bounding box
        var w = precise_round(bounds.getSouthWest().lng(),2);
        var s = precise_round(bounds.getSouthWest().lat(),2);
        var e = precise_round(bounds.getNorthEast().lng(),2);
        var n = precise_round(bounds.getNorthEast().lat(),2);
        document.getElementById("bounding_box").value = w + ',' + s + ',' + e + ',' + n;
    });
}   

function initialize_polygon_map(poly) {
    //optional argument location
    switch (arguments.length - 0) { // <-- 0 is number of required arguments
        case 0:  poly = '-115,34,-115,35,-114,35,-114,34';
    }
    var poly_list = poly.replace(' ','').split(','); 
    var drawingManager;
    var selectedShape;
    color = '#1E90FF';
    //var selectedColor;
    //var colorButtons = {};

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
        shape.setDraggable(true);
    }
    function deleteSelectedShape() {
        if (selectedShape) {
            selectedShape.setMap(null);
        }
        drawingManager.setOptions({
            drawingControl: true
        });
    }
    function set_form_field(ev){
        //ev is a map event, e.g. new polygon or circle was drawn
        try {
            var newShape = ev.overlay;
        }
        catch(e) {
            var newShape = ev;
        }
        newShape = ev.overlay;
        newShape.type = ev.type;
        if (ev.type != google.maps.drawing.OverlayType.MARKER) {
            if (ev.type == google.maps.drawing.OverlayType.POLYGON || ev.type == google.maps.drawing.OverlayType.POLYLINE || ev.type == 'polygon') {
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
            if (ev.type == google.maps.drawing.OverlayType.RECTANGLE){
                var bounds=newShape.getBounds();
                //set new bounding box
                var w = precise_round(bounds.getSouthWest().lng(),2);
                var s = precise_round(bounds.getSouthWest().lat(),2);
                var e = precise_round(bounds.getNorthEast().lng(),2);
                var n = precise_round(bounds.getNorthEast().lat(),2);
                document.getElementById("shape").value = w + ',' + s + ',' + e + ',' + n;
            }
            if (ev.type == google.maps.drawing.OverlayType.CIRCLE){
                var center = newShape.getCenter();
                var radius = newShape.getRadius();
                document.getElementById("shape").value = precise_round(center.lng(),2) + ',' + precise_round(center.lat(),2) + ',' + precise_round(radius,2);
            }
        }
        else{ //MARKER
            pos = newShape.position;
            document.getElementById("shape").value = precise_round(pos.lng(),2) + ',' + precise_round(pos.lat(),2);
        }
    }

    function set_event_handlers(ev){
        try {
            var newShape = ev.overlay;
        }
        catch(e) {
            var newShape = ev;
        }
        newShape.type = ev.type;
        //If a vertex is right clicked, remove it from polygon and update form
        newShape.addListener('rightclick', function(mev){
            if(mev.vertex != null && this.getPath().getLength() > 3){
                this.getPath().removeAt(mev.vertex);
            }
        });
        //If a point is dragged, update the form fiels
        if (ev.type == google.maps.drawing.OverlayType.POLYGON || ev.type == google.maps.drawing.OverlayType.POLYLINE) {
            newShape.getPaths().forEach(function(path, index){
                /*
                google.maps.event.addListener(path, 'insert_at', function(){
                    // New point
                    set_form_field(e);
                */
                google.maps.event.addListener(path, 'remove_at', function(){
                    // Point was removed
                    set_form_field(ev);
                });
                google.maps.event.addListener(path, 'set_at', function(){
                    // Point was moved
                    set_form_field(ev);
                });
            });
        }
        if (ev.type == google.maps.drawing.OverlayType.RECTANGLE){
            google.maps.event.addListener(newShape, 'bounds_changed', function(){
                // Polygon was dragged
                set_form_field(ev);
            });
        }
        if (ev.type == google.maps.drawing.OverlayType.CIRCLE){
            google.maps.event.addListener(newShape, 'radius_changed', function(){
                // Polygon was dragged
                set_form_field(ev);
            });
            google.maps.event.addListener(newShape, 'center_changed', function(){
                // Polygon was dragged
                set_form_field(ev);
            });
        }
        if (ev.type == google.maps.drawing.OverlayType.MARKER) {
            google.maps.event.addListener(newShape, 'dragend', function () {
                set_form_field(ev);
            });
        }
    }
    //MAP
    var myLatlng = new google.maps.LatLng(parseFloat(poly_list[1]),parseFloat(poly_list[0]));
    var map = new google.maps.Map(document.getElementById('map-polygon'), {
        zoom: 6,
        center: myLatlng,
        mapTypeId: google.maps.MapTypeId.HYBRID,
        disableDefaultUI: true,
        zoomControl: true
    });
    var polyOptions = {
      strokeWeight: 0,
      fillOpacity: 0.45,
      editable: true,
      draggable:true,
      fillColor: "#1E90FF",
      strokeColor: "#1E90FF",
    };
    var mkrOptions = {draggable: true};
    //Set initial polygon
    var poly_initial = [];
    for (var idx=0;idx < poly_list.length ; idx+=2 ){
        poly_initial.push(new google.maps.LatLng(parseFloat(poly_list[idx+1]),parseFloat(poly_list[idx])))
    }
    var shape_init_opts = {
        path:poly_initial,
        editable: false,
        draggable:false,
        type:google.maps.drawing.OverlayType.POLYGON    
    } 
    var shape_init = new google.maps.Polygon($.extend({},polyOptions,shape_init_opts));
    shape_init.setMap(map);
    setSelection(shape_init);
    try {
        var bounds = selectedShape.getBounds;
        map.fitBounds(bounds);
    }
    catch(e){}
    google.maps.event.addListener(shape_init, "dragend", function(){
        var len=selectedShape.getPath().getLength();
        var htmlStr = '';
        for (var i=0; i<len; i++) {
            htmlStr += shape_init.getPath().getAt(i).toUrlValue(4);
            if (i < len -1 ) {
                htmlStr += ',';
            }
        }
        document.getElementById('shape').value = htmlStr;
    });
    /*
    shape_init.getPaths().forEach(function(path, index){
        google.maps.event.addListener(path, 'remove_at', function(){
            // Point was removed
            set_form_field(shape_init);
        });
        google.maps.event.addListener(path, 'set_at', function(){
            // Point was moved
            set_form_field(shape_init);
        });
    });
    */
    // Creates a drawing manager attached to the map that allows the user to draw
    // markers, lines, and shapes.
    drawingManager = new google.maps.drawing.DrawingManager({
        drawingModes: [
            google.maps.drawing.OverlayType.POLYGON,
            google.maps.drawing.OverlayType.MARKER,
            google.maps.drawing.OverlayType.CIRCLE,
            google.maps.drawing.OverlayType.RECTANGLE
        ],
        drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_LEFT,
            drawingModes: [
                google.maps.drawing.OverlayType.POLYGON,
                google.maps.drawing.OverlayType.MARKER,
                google.maps.drawing.OverlayType.CIRCLE,
                google.maps.drawing.OverlayType.RECTANGLE        
            ]
        },
        markerOptions: mkrOptions,
        rectangleOptions: polyOptions,
        circleOptions: polyOptions,
        polygonOptions: polyOptions
    });
    drawingManager.setMap(map);
    //Event handlers
    google.maps.event.addListener(drawingManager, 'overlaycomplete', function(e) {
        deleteSelectedShape()
        // Switch back to non-drawing mode after drawing a shape.
        drawingManager.setDrawingMode(null);
        set_form_field(e);
        set_event_handlers(e)
        var newShape = e.overlay;
        setSelection(newShape);
    });

    //General event handlers
    google.maps.event.addListener(drawingManager, 'drawingmode_changed', deleteSelectedShape);
    //google.maps.event.addListener(map,'click',clearSelection);
    google.maps.event.addDomListener(document.getElementById('delete-button'), 'click', deleteSelectedShape);
}

function initialize_map_overlay(map_id,poly) {
    //Initializes map with polygon overlay poly
    //Used in form_utils.update maps
    var center = poly.coords[Math.floor(poly.coords.length / 2)];
    var mapOptions = {
        zoom: 7,
        center: center,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    var map = new google.maps.Map(document.getElementById(map_id), mapOptions);
    var bounds = new google.maps.LatLngBounds();;
    var paths = poly.getPath()
    for(var i = 0; i < paths.length; i++){
        points = new google.maps.LatLng(paths.getAt(i).lat(), paths.getAt(i).lng());
        bounds.extend(points);                  
    }
    map.fitBounds(bounds);
    poly.setMap(map);
    var infowindow = new google.maps.InfoWindow({
        content: 'oi'
    });
    google.maps.event.addListener(poly, 'click', function() {
        infowindow.close();
        infowindow.setContent(poly.area_type + ': ' + poly.id);
        infowindow.open(map, marker);
    });    
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
        var text = kmlEvent.featureData.description;
        document.getElementById(type).value = kmlEvent.featureData.description;
        //showInDiv(text);
        //var contentString = '<div id="LayerWindow" style="line-height:1.35;width:200px;overflow:hidden;white-space:nowrap;">'+
        var contentString = '<div id="LayerWindow">' +
            kmlEvent.featureData.description +
            '</div>';
        infowindow.close();
        //infowindow.setContent(contentString);
        infowindow.setOptions({
                //content: kmlEvent.featureData.description,
                content:contentString,
                //position: kmlEvent.position
                position:kmlEvent.latLng 
        });
        //infowindow.open(map, Layer);
        infowindow.open(map);
    });
    //KML layer has no mouseover event!! This is not working 
    google.maps.event.addListener(Layer, 'mouseover', function(kmlEvent) {
        var text = kmlEvent.featureData.description;
        document.getElementById(type).value = kmlEvent.featureData.description;
        //showInDiv(text);
        var contentString = '<div id="LayerWindow" style="line-height:1.35;overflow:hidden;white-space:nowrap;">' +
            kmlEvent.featureData.description +
            '</div>';
        infowindow.close();
        //infowindow.setContent(contentString);
        infowindow.setOptions({
                content:contentString,
                //position: kmlEvent.position
                position:kmlEvent.latLng
        });
        //infowindow.open(map, Layer);
        infowindow.open(map);
    });

    function showInDiv(text) {
        var sidediv = document.getElementById('content-window');
        sidediv.innerHTML = text;
    }
}
