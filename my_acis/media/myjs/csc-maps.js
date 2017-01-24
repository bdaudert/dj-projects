//Function to determine if variable is in list
String.prototype.inList=function(list){
   return ( list.indexOf(this.toString()) != -1)
}



function printMapControl(controlDiv,map_div){
  // Set CSS for the control border.
  var controlUI = document.createElement('div');
  controlUI.style.backgroundColor = '#fff';
  controlUI.style.border = '2px solid #fff';
  controlUI.style.borderRadius = '3px';
  controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
  controlUI.style.cursor = 'pointer';
  controlUI.style.marginBottom = '22px';
  controlUI.style.textAlign = 'center';
  controlUI.title = 'Print Map';
  controlDiv.appendChild(controlUI);
  // Set CSS for the control interior.
  var controlText = document.createElement('div');
  controlText.style.color = 'rgb(25,25,25)';
  controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
  controlText.style.fontSize = '14px';
  controlText.style.lineHeight = '15px';
  controlText.style.paddingLeft = '5px';
  controlText.style.paddingRight = '5px';
  controlText.innerHTML = 'Print Map';
  controlUI.appendChild(controlText);
  
  controlUI.addEventListener('click', function() {
      var content = $('#' + map_div); //has to be first.
      var win = window.open();
      win.document.write(content);
      win.print();
      win.close();
 });
}

function downloadMapControl(controlDiv,map) {
  // Set CSS for the control border.
  var controlUI = document.createElement('div');
  controlUI.style.backgroundColor = '#fff';
  controlUI.style.border = '2px solid #fff';
  controlUI.style.borderRadius = '3px';
  controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
  controlUI.style.cursor = 'pointer';
  controlUI.style.marginBottom = '22px';
  controlUI.style.textAlign = 'center';
  controlUI.title = 'Download Map';
  controlDiv.appendChild(controlUI);
  // Set CSS for the control interior.
  var controlText = document.createElement('div');
  controlText.style.color = 'rgb(25,25,25)';
  controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
  controlText.style.fontSize = '16px';
  controlText.style.lineHeight = '20px';
  controlText.style.paddingLeft = '5px';
  controlText.style.paddingRight = '5px';
  controlText.innerHTML = 'Download Map';
  controlUI.appendChild(controlText);
  // Setup the click event listeners: simply set the map to Chicago.
  controlUI.addEventListener('click', function() {
      html2canvas(map, {
        useCORS: true,
        onrendered: function(canvas) {
            var dataUrl= canvas.toDataURL("image/png");
            //var dataUrl = canvas.toDatatURL("/csc/scenic/download_map/") 
            //write it to the page
            document.write('<img src="' + dataUrl + '"/>');
        }
      });
  });
}


function initialize_grid_point_map(loc) {
    //optional argument location
    switch (arguments.length - 0) { // <-- 0 is number of required arguments
        case 0:  loc = '-111,40';
    } 
    var map;
    var zoom_level = '5';
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
    window.map = map; 
    infowindow = new google.maps.InfoWindow({
        content: '<div id="MarkerWindow" style="line-height:1.35;overflow:hidden;white-space:nowrap;">'+
            '<p><b>Lat: </b>' + lat + '<br/>'+
            '<b>Lon: </b>' + lon + '<br/>' +
            '</div>',
         maxWidth: 100
    });
    window.infowindow = infowindow;
    var marker = new google.maps.Marker({
        draggable: true,
        position: myLatlng,
        //animation: google.maps.Animation.DROP,
        map: map,
        title: "Your location"
    });
    infowindow.open(map, marker);
    window.marker = marker;
    //Listeners
    //Panning, zoom changed
    google.maps.event.addListener(map,'center_changed',function(){
        //If marker out of map bounds, re-center 
        var newCenter = map.getCenter();
        var myCenterLat = newCenter.lat().toFixed(4);
        var myCenterLong = newCenter.lng().toFixed(4);
        var LongLat = String(myCenterLong)+','+String(myCenterLat);
        var latlong = new google.maps.LatLng(myCenterLat,myCenterLong);
        if ( !map.getBounds().contains(marker.getPosition())) {
            marker.position = latlong;
            marker.setMap(map);
        }
    });
    google.maps.event.addListener(map,'zoom_changed',function(){
        //If marker out of map bounds, re-center 
        var newCenter = map.getCenter();
        var myCenterLat = newCenter.lat().toFixed(4);
        var myCenterLong = newCenter.lng().toFixed(4);
        var LongLat = String(myCenterLong)+','+String(myCenterLat);
        var latlong = new google.maps.LatLng(myCenterLat,myCenterLong);
        if ( !map.getBounds().contains(marker.getPosition())) {
            marker.position = latlong;
            marker.setMap(map);
        }
    });
    //Marker drag
    google.maps.event.addListener(marker, 'dragend', function (event) {
        infowindow.close();
        var new_lat = precise_round(event.latLng.lat(),2).toString();
        var new_lon = precise_round(event.latLng.lng(),2).toString();
        var loc = new_lon + ',' + new_lat
        document.getElementById("location").value = loc;
        var contentString = '<div id="MarkerWindow" style="line-height:1.35;overflow:hidden;white-space:nowrap;">'+
            '<p><b>Lat: </b>' + new_lat + '<br/>'+
            '<b>Lon: </b>' + new_lon + '<br/>' +

            '</div>';
        infowindow.setContent(contentString);
        infowindow.open(map, marker);
        var myLatlng = new google.maps.LatLng(parseFloat(new_lat),parseFloat(new_lon));
        map.panTo(myLatlng);
    });
    //Map click
    google.maps.event.addListener(map, 'click', function (event) {
        infowindow.close();
        var new_lat = precise_round(event.latLng.lat(),2).toString();
        var new_lon = precise_round(event.latLng.lng(),2).toString();
        var loc = new_lon + ',' + new_lat
        document.getElementById("location").value = loc;
        var contentString = '<div id="MarkerWindow" style="line-height:1.35;overflow:hidden;white-space:nowrap;">'+
            '<p><b>Lat: </b>' + new_lat + '<br/>'+
            '<b>Lon: </b>' + new_lon + '<br/>' +

            '</div>';
        infowindow.setContent(contentString);
        myLatlng = new google.maps.LatLng(parseFloat(new_lat),parseFloat(new_lon));
        marker.setPosition(myLatlng);
        infowindow.open(map, marker);
        map.panTo(myLatlng);
    });
    //Resize to show map
    var h = $(window).height();
    $('#GridpointMap').css('display','block');
    $('#GridpointMap').css('height', (h*0.55));
    $('#map-gridpoint').css('height', (h*0.55));
    google.maps.event.trigger(map, 'resize');
}//close initialize_grid_point_map

//Multiple gridpoints
function initialize_grid_points_map(locs) {
    //optional argument location
    switch (arguments.length - 0) { // <-- 0 is number of required arguments
        case 0:  locs = '-111,40,-111.1,40.5';
    }
    var map,mapOptions,zoom_level = '5',
        lons = [],lats = [],locs_list, myLatLng,
        locs_list = locs.replace(' ','').split(','), idx, mkrLatLng;
    myLatLng = new google.maps.LatLng(parseFloat(locs_list[1]),parseFloat(locs_list[0]));
    mapOptions = {
        center: myLatLng,
        zoom: 4,
        mapTypeId: google.maps.MapTypeId.HYBRID
    };
    map = new google.maps.Map(document.getElementById("map-gridpoints"),mapOptions);
    window.markers = [];
    for (idx=0;idx<locs_list;idx+=2){
        mkrLatLng = new google.maps.LatLng(parseFloat(locs_list[idx+1]),parseFloat(locs_list[idx]));
        infowindow = new google.maps.InfoWindow({
            content: 'oi'
        });
        var marker = new google.maps.Marker({
            draggable: true,
            id:idx + 1,
            name: 'marker_' + String(idx + 1),
            position: mkrLatLng,
            map: map,
            title: 'Marker_' + String(idx + 1)
        });
        google.maps.event.addListener(marker, 'dragend', function (event) {
            infowindow.close();
            var new_lat = precise_round(event.latLng.lat(),2).toString(),
                new_lon = precise_round(event.latLng.lng(),2).toString(),
                ll_list =  $('locations').val().replace(', ',',').split(',');
            //Replace old lat, lon with new
            ll_list[(marker.id - 1)*2] = new_lon;
            ll_list[(marker.id - 1)*2 + 1] = new_lat;
            $("locations").val(ll_list.join());
            var contentString = '<div id="MarkerWindow" style="line-height:1.35;overflow:hidden;white-space:nowrap;">'+
            '<p><b>Lat: </b>' + new_lat + '<br/>'+
            '<b>Lon: </b>' + new_lon + '<br/>' +
            '</div>';
            infowindow.setContent(contentString);
            infowindow.open(map, marker);
            myLatlng = google.maps.LatLng(parseFloat(new_lat),parseFloat(new_lon));
            window.markers.push(marker);
        });
    }//marker loop
}//close initialize_grid_points_map
var stnclick;
var boxclick;
var show;
var hide;
function initialize_station_finder() {
    var geocoder = new google.maps.Geocoder(),
        JSON_URL = $("#JSON_URL").val(),TMP_URL = $("#TMP_URL").val(),
        j_f = $("#station_json").val(),
        metadata_keys_str = $('#metadata_keys_str').val(),
        metadata_keys = String(metadata_keys_str).split(','),
        station_json = TMP_URL + j_f,
        start_date = $('#start_date').val(),end_date = $('#end_date').val(),
        el_list = $('#variables').val(), el_string = el_list.join(','),
        dataTable, dataTableInfo, L, header, l_short; 
    if ( $.fn.dataTable.isDataTable( '#station_list' ) ) {
        dataTable = $('#station_list').DataTable();
    }
    else {
        dataTableInfo = $.trim(String($('.dataTableInfo').text()).replace('/^\s*\n/gm', ''));
        L = dataTableInfo.split('\n'), newL = [];
        header = '';
        for (var k =0;k<L.length;k++){
            l_short = $.trim(L[k]).replace(/;/g, ' ');
            newL.push(l_short);
            header += l_short;
        }
        dataTableInfo = newL.join(' ');
        dataTable = $('#station_list').DataTable({
            'dom': 'Bfrtip',
            'paging': false,
            'scrollY': 400,
            'bScrollCollapse': true,
            'sScrollX':'100%',
            'scrollX':true,
            'sScrollXInner': '99.2%',
            'aaSorting':[],
            'oLanguage': {
                'sSearch': 'Filter:',
            },
            'buttons': [
                {
                    'extend':'csvHtml5',
                    'title':dataTableInfo,
                    'exportOptions': {
                        'columns': ':visible'
                    },
                    'customize': function(doc){
                        return dataTableInfo + '\n' + doc;
                    }
                },
                {
                    'extend':'excelHtml5',
                    'title':dataTableInfo,
                    'exportOptions': {
                        'columns': ':visible'
                    },
                    'customize': function(xlsx){
                        var sheet = xlsx.xl.worksheets['sheet1.xml'];
                        var first_row = $('c[r=A1] t', sheet).text();
                        $('c[r=A1] t', sheet).text(header);
                    }
                },
                {
                    'extend':'pdfHtml5',
                    'title':dataTableInfo,
                    'exportOptions': {
                        'columns': ':visible'
                    }
                },
                {
                    'extend':'print',
                    'title':dataTableInfo,
                    'exportOptions': {
                        'columns': ':visible'
                    }
                },
                {
                    'extend':'copy',
                    'title':dataTableInfo,
                    'exportOptions': {
                        'columns': ':visible'
                    }
                },
                'colvis'
            ]
        });
    };
 
    //Read in stn data json file
    $.getJSON(station_json, function(data) {
        //for (first in data.stations) var ll = new google.maps.LatLng(first.lat,first.lon);
        var ll = new google.maps.LatLng(data.stations[0].lat, data.stations[0].lon);
        var mapOptions = {
            center:ll,
            zoom:7,
            mapTypeId:google.maps.MapTypeId.HYBRID
        };
        var map_div = 'map-station-finder';
        var sf_map = new google.maps.Map(document.getElementById(map_div),mapOptions);

        /*
        //Add control to print the map
        var printMapControlDiv = document.createElement('div');
        var printControl = new printMapControl(printMapControlDiv, map_div);
        printMapControlDiv.index = 1;
        map.controls[google.maps.ControlPosition.TOP_CENTER].push(printMapControlDiv); 
        */

        /*
        // Add control to Download the map
        var downloadMapControlDiv = document.createElement('div');
        var downloadControl = new downloadMapControl(downloadMapControlDiv, window.map);
        downloadMapControlDiv.index = 1;
        map.controls[google.maps.ControlPosition.TOP_CENTER].push(downloadMapControlDiv);        
        */
        
        //Add overlay to map
        var area_type = $('#area_type').val();
        add_overlay_to_map(sf_map, $('#' + area_type)); 
        //Sort network_codes according to Kelly's preference and append to legend:
        count = 0;
        var tr = $('<tr>'), td;
        for (var key in data.network_codes) {
            count = count + 1;
            var name = data.network_codes[key];
            var icon = 'http://maps.google.com/mapfiles/ms/icons/' + data.network_icons[key] + '.png';
            td = $('<td>');
            //Omit RCC/Misc/Threadex
            if (['RCC','Misc'].indexOf(data.network_codes[key]) >= 0){
                //tr.setAttribute("style", "display:none");
                td.css('display','none');
                //continue;
            }
            var html_text = '<input type="checkbox" id="' + name + '"' +
            '" onclick="my_boxclick(this,\''+ name +'\')" checked /> ' +
            '<img style="cursor:pointer;" onclick="ShowNetworkDocu(\'Docu_' + name + '\')" alt="Icon" title="Icon" src="' + icon + '">' + 
            '<div style="cursor:pointer;" onclick="ShowNetworkDocu(\'Docu_' + name + '\')" >' + 
            name + '</div>';
            td.html(html_text)
            tr.append(td);
            if (count == 11){
                name = 'All';
                icon = 'http://thydzik.com/thydzikGoogleMap/markerlink.php?text=A&color=FC6355';
                td = $('<td>');
                html_text = '<input type="checkbox" id="all" onclick="my_boxclick(this,\'all\')" checked />' + 
                '<img alt="Icon" title="Icon" src="' + icon  + '"><br />' + name;
                td.html(html_text);
                tr.append(td);
            }
        }

        $('#map_legend').append(tr);
        //Adjust map bounds
        var map_bounds = new google.maps.LatLngBounds();

        //Create info window
        infowindow = new google.maps.InfoWindow({
            content: 'oi'
        });
        var markers = [], markers_showing = [];
        var tbl_rows = [];
        //tbl_rows_showing = [];
        var tableDataRows = [], tableDataAttrs = [];
        //for bounds_changed function
        //we need to keep track what markers/stations appear
        //Define markers and table rows
        var name_unique = '', marker_count = 0;
        $.each(data.stations, function(index, c) {
            //Sanity check on coords
            try{
                var latF = parseFloat(c.lat);
                var lonF = parseFloat(c.lon);
                if (!inrange(-90,latF,90) || !inrange(-180,lonF,180)) {
                    return;
                }
            }
            catch(e){return;}
            /*
            //Omit Misc stations
            if (['RCC','Misc'].indexOf(c.stn_network) >= 0){
                return;
            }
            */
            //Define marker
            marker_count+=1;
            var latlon = new google.maps.LatLng(c.lat,c.lon);
            var marker = new google.maps.Marker({
                map: sf_map,
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
            if (!marker){return;}
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
            map_bounds.extend(latlon);

            var avbl_variables = '<br /><b>' + c.available_variables[0][1] + '</b><br />';
            //var avbl_variables = '<br />'
            var greg_flag = false;
            var dr = c.available_variables[0][1];
            for (var i=0;i<c.available_variables.length;i++){
                if (c.available_variables[i][1].toString() != dr.toString()){
                    dr = c.available_variables[i][1];
                    avbl_variables += '<b>' + c.available_variables[i][1] + '</b><br />';
                }
                avbl_variables += c.available_variables[i][0] + '<br />'     
            }
            var metadict = {
                'name':String(c.name),
                'state':String(c.state),
                'ids':String(c.sids),
                'sids':String(c.sids),
                'networks':String(c.stn_networks),
                'll':String(c.ll),
                'elev':String(c.elevation),
                'valid_daterange':String(avbl_variables)
            }
            var data_portal_href = '/csc/scenic/data/climate_data/single/lister/'+
            '?area_type=station_id&station_id=' + encodeURIComponent(c.name) + ',' + c.sid; 
            var app_portal_href = '/csc/scenic/data/climate_data/single/'+
            '?area_type=station_id&station_id=' + encodeURIComponent(c.name) + ',' + c.sid;
            for (var k =0;k<el_list.length;k++){
                data_portal_href = data_portal_href + '&variables=' + el_list[k];
                app_portal_href = app_portal_href + '&variables=' + el_list[k];
            }
            /*
            data_portal_href = data_portal_href + '&variables=' + el_string;
            app_portal_href = app_portal_href + '&variables=' + el_string;
            */

            data_portal_href = data_portal_href + '&start_date=' + start_date;
            app_portal_href = app_portal_href + '&start_date=' + start_date; 
            data_portal_href = data_portal_href + '&end_date=' + end_date;
            app_portal_href = app_portal_href + '&end_date=' + end_date; 
            var data_portal_link = '<button class="btn-info" onclick="window.open(\'' + data_portal_href + '\')">Get Data</button>';
            var app_portal_link = '<button class="btn-info"onclick="window.open(\'' + app_portal_href + '\')">Run Analysis</button>';
            var contentString = '<div id="MarkerWindow" class="row">'+
                '<div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">' + 
                data_portal_link + '</div>' +
                '<div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">' +
                app_portal_link + '</div><br />' +
                '<b>Name: </b><font color="#FF007F">' + c.name + '</font><br/>'+
                '<b>Station ID: </b>' + c.sid + '<br/>' +
                '<b>Network: </b>' + c.stn_network + '<br/>' +
                '<b>State, Elev ft, Lon, Lat: </b>' + c.state + ', ' + c.elevation + ', ' + c.lon + ', ' +c.lat +'<br/>' +
                '<b>Available variables with date range: </b>' + avbl_variables + '<br />' +
                '</div>';
            marker.contentString = contentString;

           //Open info window when user clicks on marker
            google.maps.event.addListener(marker, 'click', function() {
                infowindow.close();
                infowindow.setContent(contentString);
                infowindow.open(sf_map, marker);
            });
            //Define table row, one entry per station
            var tbl_row = $('<tr>');
            tbl_row.attr('cString', contentString);
            tbl_row.attr('name', c.name);
            tbl_row.attr('id', marker_count - 1);
            tbl_row.attr('lat',c.lat);
            tbl_row.attr('lon',c.lon);
            var td, tdArray=[], rowNode,row_attrs; tableDataRow = [];
            //tableDataRow = {};
            if ( metadata_keys && metadata_keys.length >0){
                for (var m=0;m<metadata_keys.length;m++){
                    try{
                        tdArray.push(metadict[metadata_keys[m]]);
                    }
                    catch(e){continue;} 
                }
            }
            else{
                tdArray = [
                String(c.name), String(c.state), 
                String(c.sid), String(c.lat), String(c.lon), 
                String(c.elevation), String(c.stn_network)
                ];
            }
            for (var k=0;k<tdArray.length;k++){
                td = $('<td>');
                html_text = String(tdArray[k]);
                td.html(html_text);
                tbl_row.append(td); 
                //tableDataRow[station_finder_metadata[metadata_keys[k]]] = tdArray[k];
                tableDataRow.push(tdArray[k])
            }
            //Complete table row list for on and off switch
            tbl_rows.push(tbl_row);
            //tbl_rows_showing.push(tbl_row);
            tableDataRows.push(tableDataRow);
            //tableDataRows_showing.push(tableDataRow);
            row_attrs = {
                'cString':contentString,
                'name':c.name,
                'id':marker_count - 1,
                'lat':c.lat,
                'lon':c.lon
            };
            tableDataAttrs.push(row_attrs);
            //Set Initial markers
            marker.setVisible(true);
            $('#' + c.marker_category).prop('checked', true);
            //Push markers
            markers.push(marker);
            markers_showing.push(marker);
            if (c.name != name_unique){
                name_unique = c.name;
                rowNode = dataTable.row.add(tableDataRow).node();
                //Set necessary attributes
                for (var key in row_attrs){
                    $(rowNode).attr(key,row_attrs[key]);
                }
            }
        }); //end each
        sf_map.fitBounds(map_bounds);
        //dataTable.draw();
        google.maps.event.addListener(sf_map, 'tilesloaded', function() {
            // Called on initial map load.
            this.zoomChanged = false;
            google.maps.event.clearListeners(sf_map, 'tilesloaded');
        });
        /*
        On zoom change reset the markers
        Note: zoom_changed event fires before the bounds have been recalculated. 
        To bind bounds_changed and work with markers/map stuff we need to work with both, 
        zoom_changed and bounds_changed  
        */
        google.maps.event.addListenerOnce(sf_map,"bounds_changed",function() {
            //Do nothing
            this.zoomChanged = false;
        });
        google.maps.event.addListener(sf_map,"zoom_changed",function() {
            this.zoomChanged = true;
        });

        google.maps.event.addListener(sf_map,"idle",function() {
            if (this.zoomChanged) {
                this.zoomChanged = false;
            }
            /*
            Reset station_ids_str for link to data finder and table rows:
            Look through currently showing markers and see if they lie within bounds
            of zoomed map
            */
            var station_ids_str = '';
            //Delete old station_list table rows except header (th)
            //$('#station_list tr').has('td').remove();
            dataTable.rows().remove();
            var mapBounds = sf_map.getBounds();
            var name_unique = '', count_stns = 0;
            for (var i=0; i<markers.length; i++) {
                markers[i].setVisible(false);
                if (mapBounds.contains(new google.maps.LatLng(markers[i].lat, markers[i].lon))) {
                    if (document.getElementById(markers[i].category).checked == true){
                        markers[i].setVisible(true);
                    }
                    count_stns+=1;
                    // marker is within new bounds
                    //Check if it is currently showing on map
                    if (markers_showing.indexOf(markers[i]) >= 0){
                        if (markers[i].name != name_unique){            
                            station_ids_str+=markers[i].name + ',';
                            //$('#station_list').append(tbl_rows[i]);
                            rowNode = dataTable.row.add(tableDataRows[i]).node();
                            //Set necessary attributes
                            for (var key in tableDataAttrs[i]){
                                $(rowNode).attr(key,tableDataAttrs[i][key]);
                            }
                            name_unique = markers[i].name;
                        }
                    }
                }
            }
            //Remove trailing comma and set html variable
            station_ids_str = station_ids_str.replace(/,\s*$/, "");
            //Update hidden var inf formDownload of sttaion_finder.html
            $('#station_ids_string').val(station_ids_str);
            try {
                dataTable.draw();
            }catch(e){};
        });  
        // == shows all markers of a particular category, and ensures the checkbox is checked and write station_list==
        show = function(category) {
            //Delete old station_list table rows except header (th)
            //$('#station_list tr').has('td').remove();
            dataTable.rows().remove();
            var station_ids_str = '';
            var name_unique = '';
            markers_showing = [];
            var mapBounds = sf_map.getBounds();
            for (var i=0; i<markers.length; i++) {
                if (category == 'all') {
                    markers[i].setVisible(true);
                    if (mapBounds.contains(new google.maps.LatLng(markers[i].lat, markers[i].lon))){
                        markers_showing.push(markers[i]);
                        if (markers[i].name != name_unique){
                            rowNode = dataTable.row.add(tableDataRows[i]).node();
                            //Set necessary attributes
                            for (var key in tableDataAttrs[i]){
                                $(rowNode).attr(key,tableDataAttrs[i][key]);
                            } 
                            name_unique = markers[i].name;
                            station_ids_str+=markers[i].name + ',';
                        }
                    }
                    for (var key in data.network_codes) {
                        // == check all the checkboxes ==
                        $( '#' + data.network_codes[key]).prop('checked',true);
                    }
                }
                else if (markers[i].category == category) {
                    markers[i].setVisible(true);
                    //markers_showing.push(markers[i]);
                    //rowNode = dataTable.row.add(tableDataRows[i]).node();
                    //Set necessary attributes
                    for (var key in tableDataAttrs[i]){
                        $(rowNode).attr(key,tableDataAttrs[i][key]);
                    }
                    //name_unique = markers[i].name;
                    if (mapBounds.contains(new google.maps.LatLng(markers[i].lat, markers[i].lon))){
                        //$('#station_list tbody').append(tbl_rows[i]);
                        markers_showing.push(markers[i]);
                        if (markers[i].name != name_unique){
                            rowNode = dataTable.row.add(tableDataRows[i]).node();
                            //Set necessary attributes
                            for (var key in tableDataAttrs[i]){
                                $(rowNode).attr(key,tableDataAttrs[i][key]);
                            }
                            name_unique = markers[i].name;
                            station_ids_str+=markers[i].name + ',';
                        }
                    }
                    $('#' + category).prop('checked',true);
                }
                else if (markers[i].category != category && $( '#' + markers[i].category).prop('checked')){
                    markers[i].setVisible(true);
                    if (markers[i].name != name_unique){
                        markers_showing.push(markers[i]);
                        if (mapBounds.contains(new google.maps.LatLng(markers[i].lat, markers[i].lon))) {
                            rowNode = dataTable.row.add(tableDataRows[i]).node();
                            //Set necessary attributes
                            for (var key in tableDataAttrs[i]){
                                $(rowNode).attr(key,tableDataAttrs[i][key]);
                            }  
                            station_ids_str+=markers[i].name + ',';
                        }
                    }
                }
                try {
                    dataTable.draw();
                }catch(e){};
            }
            //Remove trailing comma and set html variable
            station_ids_str = station_ids_str.replace(/,\s*$/, "");
            //station_ids_str = station_ids_str.substring(0,station_ids_str.length - 1);
            $('#station_ids').val(station_ids_str);
        };

        // == hides all markers of a particular category, and ensures the checkbox is cleared and delete station_list ==
        hide = function(category) {
            //clear station list
            dataTable.rows().remove();
            //remove all rows that belong to category
            var station_ids_str = '';
            name_unique = '';
            markers_showing = [];
            var mapBounds = sf_map.getBounds();
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
                        $('#' + data.network_codes[key]).prop('checked',false);
                    }
                    $('#all').prop('checked',false);
                }
                else if (cat == category) {
                    markers[i].setVisible(false);
                    station_ids_str = station_ids_str.substring(0,station_ids_str.length - l);
                    // == clear the checkbox ==
                    $('#' + category).prop('checked',false);
                    //Clear 'show all networks' button
                    $('#all').prop('checked',false);
                }
                else if (cat != category && mapBounds.contains(new google.maps.LatLng(markers[i].lat, markers[i].lon))) {
                    if ($('#' + cat).prop('checked')){
                        markers_showing.push(markers[i]);
                        rowNode = dataTable.row.add(tableDataRows[i]).node();
                        //Set necessary attributes
                        for (var key in tableDataAttrs[i]){
                            $(rowNode).attr(key,tableDataAttrs[i][key]);
                        }  
                        name_unique = markers[i].name;
                    }
                }
            }
            try {
                dataTable.draw();
            }catch(e){};
            //Remove trailing comma and set html variable
            /*
            if (station_ids_str){
                station_ids_str = station_ids_str.substring(0,station_ids_str.length - 1);
            }
            */
            station_ids_str = station_ids_str.replace(/,\s*$/, "");
            $('#station_ids').val(station_ids_str);
        };

        boxclick = function(box, category){
            if (box.checked){
                show(category);
            }
            else {
                hide(category);
            }
        };
        //var markerCluster = new MarkerClusterer(sf_map, markers);
        //google.maps.event.trigger(window.sf_map, 'resize');
        window.markers = markers;
        window.sf_map = sf_map;
    });//close getjson
    //Resize to show map
    var h = $(window).height(); 
    $('#map-station-finder').css('height', (h*0.55));
    //Prevent misalignment of header/footer on  show/hide
    $('.dataTable').wrap('<div class="dataTables_scroll" />');
}//close initialize_station_finder

function my_boxclick(box, category){
    boxclick(box, category);
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
    var Center = new google.maps.LatLng(parseFloat(bbox_list[1]),parseFloat(bbox_list[0]));
    var mapOptions = {
        zoom: 7,
        center: Center,
        mapTypeId: google.maps.MapTypeId.HYBRID
    }
    map = new google.maps.Map(document.getElementById('map-bbox'), mapOptions);

    // Create the DIV to hold the control and call the CenterControl()
    // constructor passing in this DIV.
    function CustomDeleteButton(controlDiv, map) {

        // Set CSS for the control border.
        var controlUI = document.createElement('div');
        controlUI.style.backgroundColor = '#fff';
        controlUI.style.cursor = 'pointer';
        controlUI.style.marginTop = '6px';
        controlUI.title = 'Delete the shape from map';
        controlDiv.appendChild(controlUI);
        // Set CSS for the control interior.
        var controlText = document.createElement('div');
        controlText.style.fontSize = '16px';
        controlText.style.paddingLeft = '5px';
        controlText.style.paddingRight = '5px';
        //controlText.innerHTML ='<span class="glyphicon glyphicon-remove-circle"style="font-size:1.5em;" title="Delete from Map"></span>'
        controlText.innerHTML = '<b><font size="large">X</font></b>';
        controlUI.appendChild(controlText);

        // Setup the click event listeners: simply set the map to Chicago.
        controlUI.addEventListener('click', function() {
            rect.setMap(null);
        });
    }
    var centerControlDiv = document.createElement('div');
    var centerControl = new CustomDeleteButton(centerControlDiv, map);
    centerControlDiv.index = 1;
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(centerControlDiv);

    var rectangleOptions = {
        editable: true,
        draggable: true,
        fillColor: "#0000FF",
        fillOpacity: 0.3,
        strokeColor: "#0000FF",
        strokeWeight: 1
    }
    window.map = map;
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
            position: google.maps.ControlPosition.TOP_CENTER,
            drawingModes: [
            google.maps.drawing.OverlayType.RECTANGLE
            ]
        },
        rectangleOptions: rectangleOptions
    });
    //Event handlers
    google.maps.event.addListener(map, 'click', clearRect);
    google.maps.event.addListener(drawingManager, 'drawingmode_changed', clearRect);
    google.maps.event.addListener(drawingManager, 'overlaycomplete', function(e) {
        if (rect){
            rect.setMap(null);
        }
        rect = e.overlay;
        var rect_bounds=e.overlay.getBounds();
        //set new bounding box
        var w = precise_round(rect_bounds.getSouthWest().lng(),2);
        var s = precise_round(rect_bounds.getSouthWest().lat(),2);
        var e = precise_round(rect_bounds.getNorthEast().lng(),2);
        var n = precise_round(rect_bounds.getNorthEast().lat(),2);
        //document.getElementById("bbox").value = w + ',' + s + ',' + e + ',' + n;
        document.getElementById("bounding_box").value = w + ',' + s + ',' + e + ',' + n; 
    });
    google.maps.event.addListener(rect, 'bounds_changed', function() {
        var rect_bounds=rect.getBounds();
        //set new bounding box
        var w = precise_round(rect_bounds.getSouthWest().lng(),2);
        var s = precise_round(rect_bounds.getSouthWest().lat(),2);
        var e = precise_round(rect_bounds.getNorthEast().lng(),2);
        var n = precise_round(rect_bounds.getNorthEast().lat(),2);
        document.getElementById("bounding_box").value = w + ',' + s + ',' + e + ',' + n;
    });
    drawingManager.setMap(map);
    var rect_bounds = rect.getBounds();
    map.fitBounds(rect_bounds);
    //Resize to show map
    var h = $(window).height();
    $('#map-bbox').css('height', (0.55*h));
    setTimeout(function(){google.maps.event.trigger(map, 'resize');},500);
    if(map.getZoom() == 0){map.setZoom(5);}
    window.map = map
    window.map.fitBounds(rect_bounds);
}   

function initialize_polygon_map(poly) {
    //optional argument location
    switch (arguments.length - 0) { // <-- 0 is number of required arguments
        case 0:  poly = '-115,34,-115,35,-114,35,-114,34';
    }
    var poly_list = poly.replace(' ','').split(','); 
    var drawingManager, selectedShape;
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
            //drawingMode: google.maps.drawing.OverlayType.POLYGON,
            drawingControl: true
        });
    }
    function set_form_field(ev){
        if (ev.type != google.maps.drawing.OverlayType.MARKER) {
            if (ev.type == google.maps.drawing.OverlayType.POLYGON || ev.type == google.maps.drawing.OverlayType.POLYLINE || ev.type == 'polygon') {
                var polygon = ev.overlay.getPath();
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
                var r_bounds = ev.overlay.getBounds();
                //set new bounding box
                var w = precise_round(r_bounds.getSouthWest().lng(),2);
                var s = precise_round(r_bounds.getSouthWest().lat(),2);
                var e = precise_round(r_bounds.getNorthEast().lng(),2);
                var n = precise_round(r_bounds.getNorthEast().lat(),2);
                document.getElementById("shape").value = w + ',' + s + ',' + e + ',' + n;
            }
            if (ev.type == google.maps.drawing.OverlayType.CIRCLE){
                var center = ev.overlay.getCenter();
                var radius = ev.overlay.getRadius();
                document.getElementById("shape").value = precise_round(center.lng(),2) + ',' + precise_round(center.lat(),2) + ',' + precise_round(radius,2);
            }
        }
        else{ //MARKER
            pos = ev.overlay.position;
            document.getElementById("shape").value = precise_round(pos.lng(),2) + ',' + precise_round(pos.lat(),2);
        }
    }

    function set_event_handlers(ev){
        //If a vertex is right clicked, remove it from polygon and update form
        ev.overlay.addListener('rightclick', function(mev){
            if(mev.vertex != null && this.getPath().getLength() > 3){
                this.getPath().removeAt(mev.vertex);
            }
        });
        //If a point is dragged, update the form fiels
        if (ev.type == google.maps.drawing.OverlayType.POLYGON || ev.type == google.maps.drawing.OverlayType.POLYLINE) {
            ev.overlay.getPaths().forEach(function(path, index){
                google.maps.event.addListener(path, 'set_at', function(){
                    // Point was moved
                    set_form_field(ev);
                });
            
            });
            
        }
        if (ev.type == google.maps.drawing.OverlayType.RECTANGLE){
            google.maps.event.addListener(ev.overlay, 'bounds_changed', function(){
                // Polygon was dragged
                set_form_field(ev);
            });
        }
        if (ev.type == google.maps.drawing.OverlayType.CIRCLE){
            google.maps.event.addListener(ev.overlay, 'radius_changed', function(){
                // Polygon was dragged
                set_form_field(ev);
            });
            google.maps.event.addListener(ev.overlay, 'center_changed', function(){
                // Polygon was dragged
                set_form_field(ev);
            });
        }
        if (ev.type == google.maps.drawing.OverlayType.MARKER) {
            google.maps.event.addListener(ev.overlay, 'dragend', function () {
                set_form_field(ev);
            });
        }
    }
    //MAP
    var myLatlng = new google.maps.LatLng(parseFloat(poly_list[1]),parseFloat(poly_list[0]));
    var h = $(window).height();
    $('#map-polygon').css('height', (h*0.55));
    var map = new google.maps.Map(document.getElementById('map-polygon'), {
        zoom: 6,
        center: myLatlng,
        mapTypeId: google.maps.MapTypeId.HYBRID,
        //disableDefaultUI: true,
        zoomControl: true
    });
    // Create the DIV to hold the control and call the CenterControl()
    // constructor passing in this DIV.
    function CustomDeleteButton(controlDiv, map) {

        // Set CSS for the control border.
        var controlUI = document.createElement('div');
        controlUI.style.backgroundColor = '#fff';
        controlUI.style.cursor = 'pointer';
        controlUI.style.marginTop = '6px';
        controlUI.title = 'Delete the shape from map';
        controlDiv.appendChild(controlUI);
        // Set CSS for the control interior.
        var controlText = document.createElement('div');
        controlText.style.fontSize = '16px';
        controlText.style.paddingLeft = '5px';
        controlText.style.paddingRight = '5px';
        //controlText.innerHTML ='<span class="glyphicon glyphicon-remove-circle"style="font-size:1.5em;" title="Delete from Map"></span>'
        controlText.innerHTML = '<b><font size="large">X</font></b>';
        controlUI.appendChild(controlText);

        // Setup the click event listeners: simply set the map to Chicago.
        controlUI.addEventListener('click', function() {
            deleteSelectedShape()
        });
    }
    var centerControlDiv = document.createElement('div');
    var centerControl = new CustomDeleteButton(centerControlDiv, map);
    centerControlDiv.index = 1;
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(centerControlDiv);
    
    var polyOptions = {
      strokeWeight: 0,
      fillOpacity: 0.3,
      editable: true,
      draggable:true,
      fillColor: "#1E90FF",
      strokeColor: "#1E90FF"
    };
    var mkrOptions = {draggable: true};
    //Set initial polygon
    var shape_bounds = new google.maps.LatLngBounds();
    var poly_initial = [], point, shape_init_opts, shape_init;
    //Set up initial polygon
    if (poly_list.length == 3  && poly_list[2][1]!= '-'){
        //Circle
        var c_center = new google.maps.LatLng(parseFloat(poly_list[1]), parseFloat(poly_list[0]));
        shape_init_opts = {
            center: c_center,
            radius:parseFloat(poly_list[2])
        }
        shape_init = new google.maps.Circle($.extend({},polyOptions,shape_init_opts));
        shape_bounds = shape_init.getBounds();
    }
    else if (poly_list.length == 4){
        //Rectangle
        shape_bounds = new google.maps.LatLngBounds(
             new google.maps.LatLng(parseFloat(poly_list[1]),parseFloat(poly_list[0])),
             new google.maps.LatLng(parseFloat(poly_list[3]),parseFloat(poly_list[2]))
        );
        shape_init_opts = {
            bounds:shape_bounds
        }
        shape_init = new google.maps.Rectangle($.extend({},polyOptions,shape_init_opts));
    }
    else {
        //Polgygon
        for (var idx=0;idx < poly_list.length ; idx+=2 ){
            point = new google.maps.LatLng(parseFloat(poly_list[idx+1]), parseFloat(poly_list[idx]));
            poly_initial.push(point);
            shape_bounds.extend(point);
        }
        shape_init_opts = {
            path:poly_initial,
            editable: false,
            draggable:false,
            type:google.maps.drawing.OverlayType.POLYGON    
        } 
        shape_init = new google.maps.Polygon($.extend({},polyOptions,shape_init_opts));
    }
    var mz = map.getZoom();
    google.maps.event.addListener(shape_init, "dragend", function(){
        var len = selectedShape.getPath().getLength();
        var htmlStr = '';
        for (var i=0; i<len; i++) {
            htmlStr+= precise_round(shape_init.getPath().getAt(i).lng(),4);
            htmlStr+= ',' + precise_round(shape_init.getPath().getAt(i).lat(),4);
            if (i < len -1 ) {
                htmlStr += ',';
            }
        }
        document.getElementById('shape').value = htmlStr;
    });
    // Creates a drawing manager attached to the map that allows the user to draw
    // markers, lines, and shapes.
    drawingManager = new google.maps.drawing.DrawingManager({
        drawingModes: [
            google.maps.drawing.OverlayType.POLYGON,
            //google.maps.drawing.OverlayType.MARKER,
            google.maps.drawing.OverlayType.CIRCLE,
            google.maps.drawing.OverlayType.RECTANGLE
        ],
        drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_CENTER,
            drawingModes: [
                google.maps.drawing.OverlayType.POLYGON,
                //google.maps.drawing.OverlayType.MARKER,
                google.maps.drawing.OverlayType.CIRCLE,
                google.maps.drawing.OverlayType.RECTANGLE        
            ]
        },
        //markerOptions: mkrOptions,
        rectangleOptions: polyOptions,
        circleOptions: polyOptions,
        polygonOptions: polyOptions
    });
    //drawingManager.setMap(map);
    //Event handlers
     google.maps.event.addListener(map, 'tilesloaded', function() {
        //shape_bounds = map.getBounds();
        google.maps.event.clearListeners(map, 'tilesloaded');
    });
    google.maps.event.addListener(drawingManager, 'overlaycomplete', function(e) {
        deleteSelectedShape();
        // Switch back to non-drawing mode after drawing a shape.
        drawingManager.setDrawingMode(null);
        set_form_field(e);
        set_event_handlers(e)
        setSelection(e.overlay);
    });
    google.maps.event.addListener(drawingManager, 'drawingmode_changed', deleteSelectedShape);

    setSelection(shape_init);
    shape_init.setMap(map);
    map.fitBounds(shape_bounds);
    //FIX ME NOT SURE WHY MAP ZOOM --) on stn finder
    if(map.getZoom() == 0){map.setZoom(mz);}
    //map.panToBounds(shape_bounds); 
    drawingManager.setMap(map);
    //Resize to show map
    //setTimeout(function(){google.maps.event.trigger(map, 'resize');},500);
    window.map = map;
    window.resizeTo($(window).width(), $(window).height());
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
    var bounds = new google.maps.LatLngBounds();
    var paths = poly.getPath()
    for(var i = 0; i < paths.length; i++){
        points = new google.maps.LatLng(paths.getAt(i).lat(), paths.getAt(i).lng());
        bounds.extend(points);                  
    }
    //map.fitBounds(bounds);
    poly.setMap(map);
    var infowindow = new google.maps.InfoWindow({
        content: 'oi'
    });
    google.maps.event.addListener(poly, 'click', function() {
        infowindow.close();
        infowindow.setContent(poly.area_type + ': ' + poly.id);
        infowindow.open(map);
    });
    //Resize to show map
    var h = $(window).height();
    $('#' + map_id).css('height', (0.55*h));
    google.maps.event.trigger(map, 'resize');
    map.setCenter(center);
    map.fitBounds(bounds);
}


function initialize_map_overlays() {
    var area_type = $('#area_type').val();
    var host = $('#HOST').val();
    var kml_file_path = $('#kml_file_path').val();
    //Display map related divs
    $('#OverlayMap').css('display','block');
    $('#map-overlay').css('display','block');
    $('#content-window').css('display','block');
    //type is one of: basin, cwa, climdiv, county
    var myLatLng = new google.maps.LatLng(37.0, -114.05);
    var mapOptions = {
        zoom: 5,
        center: myLatLng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }

    var map = new google.maps.Map(document.getElementById("map-overlay"), mapOptions);
    //Parse the kml file and populate the map and form with layers
    var myParser = new geoXML3.parser({
        afterParse: useTheData,
        singleInfoWindow: true
    });
    myParser.parse(kml_file_path);
    function useTheData(doc) {
        geoXmlDoc = doc[0];
        if (!geoXmlDoc || !geoXmlDoc.placemarks) return;
        var defaultStyle = {fillColor: "#0000FF", strokeColor: "#0000FF", fillOpacity: 0.3};
        var highlightStyle = {fillColor: "#0000FF", strokeColor: "#0000FF", fillOpacity: 0.6};
        var bounds = new google.maps.LatLngBounds();
        for (var i = 0; i < geoXmlDoc.placemarks.length; i++) {
            //get first layer and display in area form filed
            var layer =  geoXmlDoc.placemarks[i];
            var latLng = new google.maps.LatLng(parseFloat(layer.polygon.bounds.f.f),parseFloat(layer.polygon.bounds.b.f));
            bounds.extend(latLng);
            latLng = new google.maps.LatLng(parseFloat(layer.polygon.bounds.f.b),parseFloat(layer.polygon.bounds.b.b));
            bounds.extend(latLng);
            if (i == 0){
                $('#' + area_type).val(layer.description);
                layer.polygon.setOptions(highlightStyle);
            }
            else{
                layer.polygon.setOptions(defaultStyle);
            }
            layer.polygon.description = layer.description;
            google.maps.event.addListener(layer.polygon,"click",function() {
                var l = $(this)[0];
                for (var j = 0; j < geoXmlDoc.placemarks.length; j++) {
                    geoXmlDoc.placemarks[j].polygon.setOptions(defaultStyle);
                }     
                l.setOptions(highlightStyle);
                //Set the area form field 
                $('#' + area_type).val(l.description);
                var contentString = '<div id="LayerWindow">' +
                    l.description + '</div>';
            });
            layer.polygon.setMap(map);
        }
        map.fitBounds(bounds);
    };
    //Resize to show map
    var h = $(window).height();
    $('#map-overlay').css('height', (0.55*h));
    google.maps.event.trigger(map, 'resize');
}

function add_polygon_to_map(map, ll_coords){
    var poly_path = [];
    var coords = ll_coords.replace(' ','').split(',');
    var bounds = new google.maps.LatLngBounds();
    //Check for circle
    if (coords.length == 3){
        var circle = new google.maps.Circle({
            strokeColor: '#0000FF',
            strokeOpacity: 0.3,
            strokeWeight: 2,
            fillColor: '#ADD8E6',
            center: {lat: parseFloat(coords[1]), lng: parseFloat(coords[0])},
            radius: parseFloat(coords[2])
        });
        circle.setMap(map);
        bounds = circle.getBounds();    
    }
    else{
        //Check for bbox
        if (coords.length == 4){
            coords = [coords[0],coords[1],coords[0],coords[3],coords[2],coords[3],coords[2],coords[1]];
        }
        for (var j=0;j<coords.length - 1; j=j+2){
            var latLng = new google.maps.LatLng(parseFloat(coords[j+1]),parseFloat(coords[j]))
            poly_path.push(latLng);
            bounds.extend(latLng);
        }

        var poly = new google.maps.Polygon({
            paths: poly_path,
            strokeColor: '#0000FF',
            strokeOpacity: 0.3,
            strokeWeight: 2,
            coords:poly_path,
            fillColor:'#ADD8E6',
            area_type: 'shape',
            name: 'polygon',
            id: ll_coords
        });
        poly.setMap(map);
    } 
    map.fitBounds(bounds);
    google.maps.event.trigger(map, 'resize');
}

function add_state_to_map(map,val) {
    var json_file =  '/csc/media/json/US_states.json';
    var bounds=new google.maps.LatLngBounds();
    $.getJSON(json_file, function(metadata) {
        for (var i = 0; i < metadata['features'].length; i++){
            if (metadata['features'][i].properties.abbr.toLowerCase() == val.toLowerCase()){
                var coords = metadata['features'][i].geometry.coordinates[0];
                var poly_path = [];
                for (var j=0,ll=coords[j];j<coords.length;j++){i
                    if (j == 0){
                        var last_latLng = new google.maps.LatLng(ll[1],ll[0]);
                    }
                    latLng = new google.maps.LatLng(ll[1],ll[0]);
                    bounds.extend(latLng);
                    poly_path.push(latLng);
                }
                poly_path.push(last_latLng);
                var poly = new google.maps.Polygon({
                    paths: poly_path,
                    strokeColor: '#0000FF',
                    strokeOpacity: 0.3,
                    strokeWeight: 3,
                    coords:poly_path,
                    area_type: 'state',
                    name: val,
                    id: val
                });

                //poly.setMap(poly);
                //map.fitBounds(bounds);
                break;
            }
        }
    })    
}
function add_kml_layer_to_map(map, id, val){
        var json_file = '/csc/media/json/US_' + id + '.json';
        //remove id to just get the name
        var val_list = val.split(', ');
        if (val_list.length == 1){val_list = val.split(',');}
        var name, idx =  1;
        if (id == 'county_warning_area' && val_list.length == "3"){
            idx = 2;
            name = val_list[0] + ', ' + val_list[1]
        }
        else if (id == 'county_warning_area' && val_list.length == "2"){
            idx = 1;
            name = val_list[0].split('  ').join(', ');
        }
        else{
            name = val_list[0];
            idx = 1;
        }

        try {
            var ol_id = val_list[idx];
        }
        catch(e){var ol_id = 'none'}
        $.getJSON(json_file, function(metadata) {
            for (var i = 0,item; item = metadata[i]; i++){

                //if (item.name.toLowerCase() != name.toLowerCase() || item.id != ol_id){
                if (item.id != ol_id){
                    continue
                }
                else {
                    //Generate polygon overlay
                    var coords = item.geojson.coordinates[0][0];
                    var poly_path = [];
                    for (var j=0,ll;ll=coords[j]; j++){
                        poly_path.push(new google.maps.LatLng(ll[1],ll[0]));
                    }
                    var poly = new google.maps.Polygon({
                        paths: poly_path,
                        strokeColor: '#0000FF',
                        strokeOpacity: 0.3,
                        strokeWeight: 3,
                        coords:poly_path,
                        area_type: id,
                        name: name,
                        id: val
                    });
                    //Find state from name and update overlay state
                    var state = 'none';
                    if (id == 'county' || id == 'climate_division') {
                        state = item.state.toLowerCase();
                    }
                    if (id == 'county_warning_area'){
                        //var state = val.split(', ')[0].split(' ')[1].slice(0,2).toLowerCase();
                        state = item.name.split(', ')[1].toLowerCase();
                    }
                    if (id == 'basin'){ 
                        state = $('#overlay_state').val().toLowerCase();
                    }
                    if (state != 'none'){
                        $('#overlay_state').val(state);
                        document.querySelector('#overlay_state [value="' + state + '"]').selected = true;
                    }
                    
                    else {
                        //Can't find the state
                        ols = document.getElementsByName('overlay_state');
                        for (idx =0;idx < ols.length;idx++){
                            try {
                                ols[idx].selectedIndex = "-1";
                            }
                            catch(e){}
                        }
                    }
                    //Update new map
                    poly.setMap(map);
                    break
                }
            }
        });
}

function add_overlay_to_map(map, area_field){
    /*
    Adds overlay defined by area_filed to map
    */
    
    var id = area_field.attr('id');
    var val = area_field.val();
    if (id == 'shape'){
        add_polygon_to_map(map, val);
    }
    else if (id == 'county' || id == 'county_warning_area' || id == 'climate_division' || id == 'basin'){ 
        add_kml_layer_to_map(map, id, val);

    }
    else if (id == 'state'){
        add_state_to_map(map, val);
    }
}
