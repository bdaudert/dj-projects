//Clean functions

//Needed fo indexOf to work in IE
Array.prototype.indexOf = function(obj, start) {
     for (var i = (start || 0), j = this.length; i < j; i++) {
         if (this[i] === obj) { return i; }
     }
     return -1;
}

//Function to determine if element is in list
String.prototype.inList=function(list){
   return ( list.indexOf(this.toString()) != -1)
}

function showLargeRequestForm(){
    if ($('#app_name').val() == 'multi_lister'){
        if ($('#data_summary').val().inList(['none','windowed_data'])){
            $('.out_format').css('display','table-row');
        }
        else{
            $('.out_format').css('display','none');
        }
    }
    else{
        $('.out_format').css('display','none');
    }
    if ($('.data_format').val().inList(['xl','html'])){
        $('.delim').css('display','none');

    }
    else{
        $('.delim').css('display','table-row');
    }
    ShowPopupDocu('largeRequestForm');
}

// [client side code for showing/hiding content]
function ShowHideTopOfPage(){
    /*
    Deals with google map issue in hidden elements
    Maps in hidden elements get mangled
    when the hidden property changes to visible
    If div is shown and contains map, 
    the map needs to be re-initialized
    */
    if ($('#top_of_page').is(':hidden')){
        if ($('#shape').length){
            update_maps(document.getElementById('shape'));
        }
        if ($('#location').length ){
            update_maps(document.getElementById('location'));
        }
        if ($('#basin').length ){
            update_maps(document.getElementById('basin'));
        }
        if ($('#county_warning_area').length ){
            update_maps(document.getElementById('county_warning_area'));
        }
        if ($('#county').length ){
            update_maps(document.getElementById('county'));
        }
        if ($('#climate_division').length ){
            update_maps(document.getElementById('climate_division'));
        }
        if ($('#bounding_box').length ){
            update_maps(document.getElementById('bounding_box'));
        }
    }
     $('#top_of_page').toggle();
     if (window.map){
        google.maps.event.trigger(window.map, 'resize');
     }
}

function set_back_date(date_string,number){
    /*
    Advances or sets back date by number.
    If number < 0, we go back number days
    If number > 0, we go forward number dauys 
    */
    var d, new_d, year, mm,dd;
    d = new Date(date_string);
    d.setDate(d.getDate() + number);
    year = String(d.getFullYear());
    mm = ('0' + (d.getMonth()+1).toString()).slice(-2);
    dd = ('0' + d.getDate().toString()).slice(-2);
    return year + '-' + mm + '-' + dd;
}

function set_dates_for_station(area_type,start_date,end_date,year_or_date){
    var today = new Date();
    var today_string = convertDateToString(today,'-');
    var s = DateStringToJSDateString(start_date);
    var e = DateStringToJSDateString(end_date);
    var new_dates;
    /*
    if (area_type == 'station_id'){
        s = 'POR', e = 'POR';
    }
    */
    if (area_type != 'station_id'){
        if (end_date.toLowerCase() == 'por'){
            e = set_back_date(today_string,0);
        }
        if (start_date.toLowerCase() == 'por'){
            s = set_back_date(e,-14);
        }   
        if (year_or_date == 'year'){
            s = s.slice(0,4);
            e = e.slice(0,4);
        }
    }
    new_dates = {
        'start': s,
        'end': e
    } 
    return new_dates;
}

function set_dates_for_grid(grid,start_date,end_date,year_or_date){
    /*
    Function that checks if start/end_date lie within
    valid daterange for grid. If not, new dates are set.
    Args: 
        grid, start_date, end_date, year_or_date
    Returns: 
        new_dates.start: new start date or start year
        new_dates.end: new end date or end year
    */
    var today = new Date();
    var today_string = convertDateToString(today,'-');
    var s = start_date, e = end_date;
    if (s.toLowerCase() == 'por'){s = grid_vd[grid][0][0];}
    if (e.toLowerCase() == 'por'){e = grid_vd[grid][0][1];} 
    if (s.length == 4){s = s + '-01-01';}
    if (e.length == 4){e = e + today_string.slice(4,today_string.length);}
    var new_dates = {
        'start': s,
        'end': e
    }
    //Set new min/max_years for grid
    var ds = new Date(s), de = new Date(e);
    //Funkyness with js dates
    //lag in data
    var ds_past = new Date(grid_vd[grid][0][0]);
    $('#min_year').val(grid_vd[grid][0][0].slice(0,4));
    //Update hidden var
    $('#max_year').val(grid_vd[grid][0][1].slice(0,4));
    var de_past = new Date(grid_vd[grid][0][1]);
    de_past.setDate(de_past.getDate() + 1);
    if (grid_vd[grid][1].length == 2){
        var ds_fut = new Date(grid_vd[grid][1][0]);
        //Update hidden var
        $('#min_year_fut').val(grid_vd[grid][1][0].slice(0,4));
        ds_fut.setDate(ds_fut.getDate() + 1);
        var de_fut = new Date(grid_vd[grid][1][1]);
        //Update hidden var
        $('#max_year_fut').val(grid_vd[grid][1][1].slice(0,4));
        de_fut.setDate(de_fut.getDate() + 1);
    }
    else{
        //Set bogus future dates for easy coding of checks
        var ds_fut = ds_past, de_fut = de_past;
        $('#max_year_fut').val("");
        $('#min_year_fut').val("");
    }
    //Special case prism monthly/yearly
    if (grid == '21'){
        if ($('#temp_res').length && ($('#temporal_resolution').val == 'mly' || $('#temporal_resolution').val == 'yly')){
            ds_past = new Date('1895-01-01');
            ds_past.setDate(ds_past.getDate() + 1);
            de_past = today;
            ds_fut = new Date('1895-01-01');
            ds_fut.setDate(ds_fut.getDate() + 1);
            de_fut = today;
        }
    }
    if ((ds_past <= ds && de <= de_past) || (ds_fut <= ds && de <= de_fut)){
        //Don't change start/end dates
        if (year_or_date == 'year'){
            new_dates.start = new_dates.start.slice(0,4);
            new_dates.end = new_dates.end.slice(0,4);
            return new_dates;
        }    
        else{
            return new_dates;
        }
    }
    else{
        //Set new start date
        if (ds < ds_past){
            new_dates.start = grid_vd[grid][0][0]; 
        }
        if (ds > de_past &&  ds < ds_fut){
            new_dates.start = grid_vd[grid][0][0];
        }
        if (ds > de_fut){
            new_dates.start = grid_vd[grid][0][0];
        }
        var new_ds = new Date(new_dates.start);
        new_ds.setDate(new_ds.getDate() + 1);
        
        //Set new end date to one year later than start date
        if (year_or_date == 'year'){
            if (ds_past <= new_ds <= de_past){
                var d = grid_vd[grid][0][1];
            }
            else {
                var d = grid_vd[grid][1][1];
            }
        }
        else{
            var d = String(parseInt(new_dates.start.slice(0,4)) + 1) + new_dates.start.slice(4,new_dates.start.length);
        }
        if (d == 'today'){
            d = convertDateToString(today,'-');
        }
        if (de < ds_past){
            new_dates.end = d; 
        }
        if (de > de_past && de < ds_fut){
            new_dates.end = d;
        }
        if (de > de_fut){
            new_dates.end = d;
        }
    }
    //Check if we only want to return years
    if (year_or_date == 'year'){
        new_dates.start = new_dates.start.slice(0,4);
        new_dates.end = new_dates.end.slice(0,4);
        return new_dates;
    }
    else {
        return new_dates;
    }
}

function set_year_range(){
    /*Set date range for drop downs for year range*/
    var today = new Date();
    var today_str = convertDateToString(today, '-')
    var today_yr = today_str.slice(0,4); 
    var max_year, min_year, min_year_fut = null, max_year_fut = null;
    if ($('#area_type').val() == 'location'){
        var grid = $('#grid').val();
        min_year = grid_vd[grid][0][0].slice(0,4);
        max_year = grid_vd[grid][0][1].slice(0,4);
        var min_year_fut = min_year, max_year_fut = min_year;
        //Check for projections and set future dates
        if (grid_vd[grid][1].length == 2){
            min_year_fut = grid_vd[grid][1][0].slice(0,4);
            max_year_fut = grid_vd[grid][1][1].slice(0,4);
        }
        //Set new year dropdowns
        $('#start_year > option').remove();
        $('#end_year > option').remove();
    }
    if ($('#area_type').val() == 'station_id'){
        //AJAX call to get vd of stations
        min_year = '1850';
        max_year = today_yr;
    }
    //Set new year dropdowns
    $('#start_year > option').remove();
    $('#end_year > option').remove();
    var opt, i;
    for (i=parseInt(min_year);i<=parseInt(max_year);i++){
        opt = '<option value="' + String(i) + '">' + String(i) + '</option>';
        $('#start_year').append(opt);
        $('#end_year').append(opt);
    }
    if (min_year_fut && max_year_fut){
        for (i=parseInt(min_year_fut);i<=parseInt(max_year_fut);i++){
            opt = '<option value="' + String(i) + '">' + String(i) + '</option>';
            $('#start_year').append(opt);
            $('#end_year').append(opt);
        }  
    }
    if ($('#area_type').val() == 'station_id'){
        opt = '<option value="POR">POR</option>';
            $('#start_year').append(opt);
            $('#end_year').append(opt);
    }
}

function showHideTableRowClass(class_name, show_or_hide){
    $('.' + class_name).each(function(){
        if (show_or_hide == 'hide'){
            $(this).css('display','none');
        }
        if (show_or_hide == 'show'){
            $(this).css('display','table-row');
        }
    });
}

function showHideTableRowId(id_name,show_or_hide){
    if (show_or_hide == 'hide'){
        $('#' + id_name).css('display','none');
    }
    if (show_or_hide == 'show'){
            $('#' + id_name).css('display','table-row');
    }
}

function update_value(val){
    /*
    Dynamic forms are not updated in browser cache
    This function updates the values upon user change
    Needed when two different forms are present in page
    and form fields of one form should be 
    preserved upon submit of the other
    */
    this.value = val;
}

function set_area_defaults(area_type, kml_file_path){
    var lv = {
        'label':'',
        'value':null,
        'autofill_list':''
    }
    if (area_type.inList(['station_id','basin','county','county_warning_area','climate_division'])) {
        lv.autofill_list = 'US_' + area_type
    }
    //Get first layer of kml_file
    var layer_name = null;
    /*
    if (kml_file_path != null) {
        var myParser = new geoXML3.parser({
            afterParse:getFirstLayer
        });
        myParser.parse(kml_file_path);
        function getFirstLayer(doc) {
            var first_layer = doc[0].placemarks[0].description;
            set_lv_value(first_layer);
        };
        function set_lv_value(v){
            lv.value = v;
        }
    }
    */
    lv.label = area_defaults[area_type][0]
    lv.value = area_defaults[area_type][1]
    /*
    if (area_type == 'station_id'){
        lv.label = 'Station ID';
        lv.value ='RENO TAHOE INTL AP, 266779';
    }
    if (area_type == 'station_ids'){
        lv.label = 'Station IDs';
        lv.value ='266779,050848';
    }
    if (area_type == 'location'){
        lv.label = 'Location (lon,lat)';
        lv.value = '-119,39';
    }
    if (area_type == 'locations'){
        lv.label = 'Locations (lon,lat pairs)';
        lv.value = '-119,39,-119.1,39.1';
    }
    if (area_type == 'county'){
        lv.label ='County';
        if (lv.value == null){
            lv.value ='Churchill County, 32001';
        }
    }
    if (area_type == 'climate_division'){
        lv.label ='Climate Division';
        if (lv.value == null){
            lv.value ='Northwestern, NV01';
        }
    }
    if (area_type == 'county_warning_area'){
        lv.label ='County Warning Area';
        if (lv.value == null){
            lv.value ='Las Vegas, NV, VEF';
        }
    }
    if (area_type == 'basin'){
        lv.label ='Basin';
        if (lv.value == null){
            lv.value ='Hot Creek-Railroad Valleys, 16060012';
        }
    }
    if (area_type == 'state'){
        lv.label ='State';
        lv.value ='nv';
    }
    if (area_type == 'bounding_box'){
        lv.label ='Bounding Box';
        lv.value ='-115,34,-114,35';
    }
    if (area_type == 'shape'){
        lv.label ='Custom Shape';
        lv.value ='-115,34, -115, 35,-114,35, -114, 34';
    }
    if (area_type == 'shape_file'){
        lv.label ='Custom Shape';
        lv.value ='';
    }
    */
    return lv;
}

function set_autofill(datalist){
    /*
    Sets autofill lists
    */
    //Grab env var JSON_URL (defined in templates/csc_base.html)
    if (!datalist){return;}
    var JSON_URL = document.getElementById('JSON_URL').value;
    dl = document.createElement('datalist');
    dl.setAttribute('id',datalist);
    dl.setAttribute('class', datalist.replace('US_',''));
    $.getJSON(JSON_URL + datalist + '.json', function(metadata) {
        for (idx=0;idx<metadata.length;idx++){
            var name = metadata[idx].name;
            var id = metadata[idx].id;
            if (id == '' || !id ){
                continue
            }
            var opt = document.createElement('option');
            if (datalist == "US_CMAP"){
                opt.value = name;
            }
            else {
                opt.value = name + ', ' + id;
            }
            opt.setAttribute('class','name')
            dl.appendChild(opt);
        }
    });
    document.body.appendChild(dl);
}


function set_area(row_id, node){
    var lv, html_text, cell0,cell1,div;
    //Update area default 
    var area_type = node.val()
    kml_file_path = null
    if (area_type.inList(['basin','county','county_warning_area','climate_division'])) {
        TMP_URL = $('#TMP_URL').val();
        state = $('#overlay_state').val();
        kml_file_path = '/tmp/' + state + '_' + area_type + '.kml'; 
    }
    lv = set_area_defaults(area_type, kml_file_path);
    //Update autofill list
    if (area_type.inList(['basin','county','county_warning_area','climate_division','station_id'])) {
        set_autofill(lv.autofill_list);
    }
    //Update row_id
    cell0 = $('#' + row_id +  ' td:first-child');
    html_text = lv.label + ': ';
    cell0.html(html_text);
    cell1 = cell0.next('td');
    if (node.val() != 'state'){
        html_text = '<input type="text" id="' + node.val() + '" name="'+
        node.val() +'" value="' +  lv.value + '"';
        if (lv.autofill_list != '') {
            html_text+=' list="' + lv.autofill_list + '"';
        }
        html_text+=' onchange="update_value(this.value) & update_maps(this)" >';
    }
    else{
        var st, state, selected = ' ';
        html_text = '<select id="' + node.val() + '" name="'+ node.val() + '">';
        for (var i=0;i< state_choices.length;i++){  
            st = state_choices[i];
            state = state_names[st];
            if ($('#overlay_state').length){
                if (st == $('#overlay_state').val()){selected = ' selected';}
                else{selected = ' ';}
            }
            else{
                if (st == 'nv'){selected = ' selected';}
                else {selected = ' ';}
            } 
            html_text= html_text + '<option' + selected + ' value="' + st +'">' + state + '</option>';
        }
        html_text = html_text + '</select>'
    }
    cell1.html(html_text) ;   
    pop_id = $('#area-pop-up');
    pop_id.html('');
    div = $("<div>");
    div.attr('id','ht_' + node.val());
    $(div).load('/csc/media/html/Docu_help_texts.html #ht_' + node.val());
    pop_id.append(div);
}

function set_elements(){
    var non_prism_els = ['gdd','hdd','cdd'];
    var station_only_els = ['obst','snow','snwd','evap','wdmv','dtr','pet'];
    var el_opts,el;
    if ($('#elements').length){
        el = $("#elements");
        el_opts = $("#elements option");
    }
    if ($('#element').length){
        el = $("#element");
        el_opts = $("#element option");
    }

    el_opts.each(function(){
        //Check if prism data, disable degree days
        if ($('#data_type').val() == 'station' || $('#area_type').val().inList['station_id','station_ids']){
            if ($(this).val() == 'pet'  || $(this).val() == 'dtr'){
                if ($('#app_name').val().inList(['monthly_summary','station_finder'])){
                     $(this).attr('disabled',false);
                }
                else{
                    $(this).attr('disabled',true);
                }
            }
            else{
                $(this).attr('disabled',false);
            }
        }
    
        if ($('#data_type').val() == 'grid' || $('#area_type').val().inList(['location','locations'])){
            if ($('#grid').val() == '21' && $(this).val().inList(non_prism_els)){
                $(this).attr('disabled',true);
                if (el.val() == $(this).val()){
                    el.val('pcpn');
                }
            }
            else{
                if ($(this).val().inList(station_only_els)){
                    $(this).attr('disabled',true);
                    if (el.val() == $(this).val()){
                        el.val('pcpn');
                    }
                }
            }
        }
    });
}


//Functions to hide and show maps
//Used in set_map function
function hide_grid_point_map(){
    if ($('#GridpointMap').length){
        $('#GridpointMap').css('display','none');
    }
    if ($('#map-gridpoint').length){
        $('#map-gridpoint').css('display','none');
    }
    if ($('#address').length){
        $('#address').css('display','none');
    }
    if ($('#zoombutton').length){
        $('#zoombutton').css('display','none');
    }
}

function show_gridpoint_map(){
    //Show gridpoint map
    $('#GridpointMap').css('display','block');
    $('#map-gridpoint').css('display','block');
    $('#address').css('display','inline');
    $('#zoombutton').css('display','inline'); 
    if ($('#location').length){
        initialize_grid_point_map($('#location').val());
    }
    else{
        initialize_grid_point_map();
    }

}

function show_bbox_map() {
    $('#address').css('display','inline');
    $('#zoombutton').css('display','inline');
    $('#BBoxMap').css('display','block');
    $('#map-bbox').css('display','block');
    if ($('#bounding_box').length){
        initialize_bbox_map($('#bounding_box').val());
    }
    else{
        initialize_bbox_map();
    }
}

function hide_bbox_map(){
    if ($('#BBoxMap').length){
        $('#BBoxMap').css('display','none');
    }
    if ($('#map-bbox').length){
        $('#map-bbox').css('display','none');
    }
    $('#address').css('display','none');
    $('#zoombutton').css('display','none');
}

function hide_overlay_map(){
    if ($('#OverlayMap').length){
        $('#OverlayMap').css('display','none');
    }
    if ($('#map-overlay').length){    
        $('#map-overlay').css('display','none');
    }
    if ($('#content-window').length){    
        $('#content-window').css('display','none');
    }
}

function show_overlay_map(){
    //Show overlay map 
    $('#OverlayMap').css('display','block');
    $('#map-overlay').css('display','block');
    $('#content-window').css('display','block');
    initialize_map_overlays();
}

function hide_polygon_map(){
    if ($('#PolyMap').length){
        $('#PolyMap').css('display','none');
    }
    if ($('#map-polygon').length){
        $('#map-polygon').css('display','none');
    }
    $('#address').css('display','none');
    $('#zoombutton').css('display','none');
}

function show_polygon_map(){
    $('#PolyMap').css('display','block');
    $('#map-polygon').css('display','block');
    $('#address').css('display','inline');
    $('#zoombutton').css('display','inline');
    if ($('#shape').length){
        initialize_polygon_map($('#shape').val());
    }
    else {
        initialize_polygon_map();
    }
}


function set_map(node){
    /*
    Sets map interfaces for data and applications
    node is the area selector
    */
    var area_type, TMP_URL,state,kml_file_path;
    //Get TMP env variable (defined in templates/csc_base.html)
    area_type = node.val();
    //Update hidden elements
    if (area_type.inList(['basin','county','county_warning_area','climate_division'])) {
        TMP_URL = $('#TMP_URL').val();
        state = $('#overlay_state').val();
        kml_file_path = TMP_URL + state + '_' + area_type + '.kml';
        //Update template variables 
        $('#kml_file_path').val(kml_file_path);
        $(".area_type").val(area_type);
    }
    //Set up maps for display
    if (area_type.inList(['basin','county','county_warning_area','climate_division'])) {
        hide_polygon_map();
        hide_grid_point_map();
        show_overlay_map();
    } 
    else if (area_type == 'shape') {
        hide_overlay_map();
        hide_grid_point_map();
        show_polygon_map();
    }
    else if (area_type.inList(['location'])){
        hide_overlay_map();
        hide_polygon_map();
        show_gridpoint_map();
    }
    else if (area_type == 'bounding_box'){
        hide_overlay_map();
        hide_polygon_map();
        hide_grid_point_map();
        show_bbox_map();
    }
    else {
        hide_overlay_map();
        hide_polygon_map();
        hide_grid_point_map();
        hide_bbox_map();
    }
}

function addHidden(theForm, name, value) {
    /*
    Create a hidden input element with name and value and append it to theForm
    */
    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = name;
    input.value = value;
    theForm.appendChild(input);
}
function setHiddenFields(fromFormID, toFormID) {
    /*
    Adds the fields from fromForm to toForm 
    as hidden input so that user input of fromForm is preserved 
    in toForm on submit
    */
    //Make a list of form names in the toForm
    //To avoid overwriting
    var ff = [];
    $('#' + toFormID + ' input, #' + toFormID + ' select').each(
    function(){
        ff.push($(this).attr('name'));
    });
    //Add submit and token entries
    ff.push('submit');
    ff.push('csrfmiddlewaretoken');

    $('#' + fromFormID + ' input, #' + fromFormID + ' select').each(
    function(){
        var name = $(this).attr('name');
        //Only save form elements that do not exists in toForm
        if (!name.inList(ff) && name.substring(0,4) != 'form'){
            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = name;
            input.value = $(this).val();
            document.getElementById(toFormID).appendChild(input);
        }
    });
};   


//Old functions (need cleanup)
function save_form_options(formID,hiddenID){
    /* 
    Saves all input and select field of form
    in hiddenID
    called on form submit in html code
    This is part of solution for backbutton issue:
    Dynamic javascript form fields are not cached
    */
    var vals = [];
    if ($('#' + formID).length){
        /*
        $('#' + formID + ' input[type=text]').each(function(){
            vals.push($(this).val());
            $('#' + hiddenID).val(vals.join(';'));
            //vals.push(encodeURIComponent($(this).val()));
        });
        */
        $('#' + formID + ' select').each(function(){
            vals.push($(this).val());
            $('#' + hiddenID).val(vals.join(';'));
        });
    }
}


function set_form_options(formID, hiddenID){
    /*
    function called on load of page
    to retrieve all cached form fields and repopulate
    form fields
    This is part of solution for backbutton issue:
    Dynamic javascript form fields are not cached
    */
    var form_selects = $('#' + hiddenID).val().split(';');
    if ($('#' + hiddenID).length){
        idx = -1;
        /*
        $('#' + formID + ' input').each(function(){
            idx+=1;
            $(this).val(form_selects[idx]);
        });
        */
        $('#' + formID + ' select').each(function(){
            idx+=1;
            if ($(this).attr('id') == 'elements'){
                $(this).val(form_selects[idx].split(','));
            }
            else{
                $(this).val(form_selects[idx]);
            }
        });
    }
}

function reset_options(){
    /*
    Reset all options on back button press
    was issue in chrome
    implemented in templates/csc_base.html 
    <body onbeforeunload="reset_options()">
    */
    opt_list = ['location', 'station_id', 'station_ids',
        'basin', 'county', 'climate_division',
        'county_warning_area', 'shape'];
    //Not Chrome
    if (navigator.userAgent.search("Chrome")==-1) {
        if ($('#select_stations_by').length){
            var val = $('#select_stations_by').val();
            var select_el = $('#select_stations_by');
        }
        if ($('#select_grid_by').length){
            var val = $('#select_grid_by').val();
            var select_el = $('#select_grid_by');
        }
        if (!$('#' + val).length){
            for (i=0;i<opt_list.length;i++){
                if ($('#' + opt_list[i]).length){
                    select_el.val(opt_list[i]);
                    break
                }
            }
        }
    }
    //Chrome
    else{
        $('select').each(function(){
            $(this).prop('selectedIndex', -1); 
        });
    }  
}


function set_likelihood_thresholds(node){
    var options = node.options;
    var threshes, thresh_low, thresh_high, thresh_id, el, html_el,html_tr;
    for (var idx=0;idx<options.length;idx++) {
        el = options[idx].value;
        threshes = set_threshes(el).split(',');
        thresh_low = threshes[2];
        thresh_high = threshes[3];
        thresh_id = el + '_threshold';
        html_tr = document.getElementById(thresh_id);
        if (options[idx].selected) {
            html_tr.style.display="table-row";
            thresh_id = el + '_threshold_low';
            html_el = document.getElementById(thresh_id);
            html_el.value = thresh_low;
            thresh_id = el + '_threshold_high';
            html_el = document.getElementById(thresh_id);
            html_el.value = thresh_high;
        }
        else {
            html_tr.style.display="none";
        }
    } 
}

function update_elements(node){
    /*
    Dynamic forms are not updated in browser cache
    This function updates the elements field
    which is a multiple select field list that
    behaves in ways that can't be caught by the udate_value function above, 
    which only deals with string variables
    The passing of variables from/to html, django views and javascript
    is done via strings. 
    To deal with element lists, we need to use an element_strings object
    and convert accordingly.
    */
    var els = []
    var options = node.options;
    for (var idx=0;idx<options.length;idx++) {
        if (options[idx].selected) {
            els.push(options[idx].value);
            //document.getElementById('elements').options[idx].selected = true;
            /*
            el_nodes = document.getElementsByName('elements');
            for (i=0;i<el_nodes.length;i++){
                el_nodes[i].options[idx].selected = true;
            }
            */
        }
    }
    if ($('#elements_string').length){
        var elements_string = els.join();
        var el_strings = document.getElementsByClassName('elements_string');
        for (idx=0;idx<el_strings.length;idx++){
            el_strings[idx].value = elements_string;
        }
    }
}

//Show "Loading image"
function show_loading(){
    /*
    Shows moving loading gif after form submit
    */
    var IMG_URL = document.getElementById('IMG_URL').value;
    $("#loading-image").attr("src",IMG_URL +"LoadingGreen.gif");
    $("#loading").show("fast");
    //this.preventDefault();
    var form = $(this).unbind('submit');
    setTimeout(function(){
        form.submit();
        $("#loading").hide();
    }, 27000);
}

function show_loading_gif(){
   $("#loading-image").attr("src","/csc/media/img/LoadingGreen.gif");
   $("#loading").show("fast"); 
}

function hide_loading_gif() {
    $("#loading-image").attr("src","/csc/media/img/LoadingGreen.gif");
   $("#loading").hide();
}

function show_hide_opts(rowClass){
    /*
    displays all rowClass table rows
    */
    var trs = document.getElementsByClassName(rowClass);
    //Show all or none
    if (trs[0].style.display == 'none'){
        var disp = "table-row";
        if ($('#show_plot_opts').length){
            document.getElementById('show_plot_opts').value = 'T';
        }
    }
    else{
        var disp = "none";
        if ($('#show_plot_opts').length){
            document.getElementById('show_plot_opts').value = 'F';
        }
    }
    for (idx=0;idx<trs.length;idx++){
        trs[idx].style.display = disp;
    }
}

function show_opts(rowClass){
    /*
    displays all rowClass table rows
    */
    var trs = document.getElementsByClassName(rowClass);
    if ($('#show_plot_opts').length){
        document.getElementById('show_plot_opts').value = 'T';
    }
    //Show all or none
    for (idx=0;idx<trs.length;idx++){
        trs[idx].style.display = 'table-row';
    }
}

function hide_opts(rowClass){
    /*
    hide all rowClass table rows
    */
    var trs = document.getElementsByClassName(rowClass);
    if ($('#show_plot_opts').length){
        document.getElementById('show_plot_opts').value = 'T';
    }
    //Show all or none
    for (idx=0;idx<trs.length;idx++){
        trs[idx].style.display = 'none';
        if ($('#show_plot_opts').length){
            document.getElementById('show_plot_opts').value = 'T';
        }
    }
}


function highlight_form_field(td_id, err){

    // Highlights form field and displays error message err
    //if user fills out form incorrectly
    var td = document.getElementById(td_id);
    var tr = td.parentNode;
    var new_tr = document.createElement('tr');
    new_tr.setAttribute('class','form_error');
    new_tr.innerHTML = '<td></td><font color="red">' + err + '</font><td></td><td></td>';
    tr.parentNode.insertBefore(new_tr, tr.nextSibling);
}

function set_threshes(element){
    /*
    Sets sodxtrmts thresholds
    */
    var threshes = '0.1,0.01,0.01,0.1';
    if ($('#units').length){
        u = document.getElementById('units').value;
        if (u == 'metric'){
            threshes = '2.5,0.25, 0.25,2.5';
        }
    }
    if (element == 'avgt' || element == 'dtr' || element == 'obst'){
        threshes = '65,65,40,65';
        if ($('#units').length){
            u = document.getElementById('units').value;
            if (u == 'metric'){
                threshes = '18,18,4,18';
            }
        }
    }
    if (element == 'maxt'){
        threshes = '40,90,65,80';
        if ($('#units').length){
            u = document.getElementById('units').value;
            if (u == 'metric'){
                threshes = '4,32,18,27';
            }
        }
    }
    if (element == 'mint'){
        threshes = '32,70,32,40';
        if ($('#units').length){
            u = document.getElementById('units').value;
            if (u == 'metric'){
                threshes = '0,21,0,4';
            }
        }
    }
    if (element == 'hdd' || element == 'gdd' || element == 'cdd'){
        threshes = '10,30,10,30';
        if ($('#units').length){
            u = document.getElementById('units').value;
            if (u == 'metric'){
                threshes = '-12,-1,-12,-1';
            }
        }
    }
    if (element == 'wdmv'){
        threshes = '100,200,100,200';
        if ($('#units').length){
            u = document.getElementById('units').value;
            if (u == 'metric'){
                threshes = '160.9,321.9,160.9,321.9';
            }
        }
    }
    return threshes;
}

function set_BaseTemp(element){
    /*
    sets sodxtrmts base temperatures for degree day calculations.
    */
    if (element =='hdd' || element =='cdd' || element=='gdd'){
        $('#base_temp').css('display', 'table-row');
        if (element == 'hdd' || element == 'cdd'){
            $('#base_temperature').val('65');
        }
        else{
            $('#base_temperature').val('50');
        }
    }
    else{$('#base_temp').css('display', 'none');}
}

function set_delimiter(data_format_node, divId){
    if (data_format_node.value == 'clm' ||  data_format_node.value == 'dlm' || data_format_node.value == 'html'){ 
        document.getElementById(divId).style.display = "table-row";
    }
    else if (data_format_node.value == 'xl'){
        document.getElementById(divId).style.display = "none";
    }
}

function set_delimiter_and_output_file(data_format_node, delim_divId, out_file_divId){
    if (data_format_node.value == 'clm' ||  data_format_node.value == 'dlm'){
        document.getElementById(delim_divId).style.display = "table-row";
    }
    else if (data_format_node.value == 'xl' || data_format_node.value == 'html'){
        document.getElementById(delim_divId).style.display = "none";
    }
    if (data_format_node.value == 'clm' ||  data_format_node.value == 'dlm' || data_format_node.value == 'xl'){
        document.getElementById(out_file_divId).style.display = "table-row";
    }
    else if (data_format_node.value == 'html'){
        document.getElementById(out_file_divId).style.display = "none";
    }
}

function show_if_true(node, rowClass){
    /*
    if node.value=true, shows all table rows of class name rowClass
    if node.value=fals, hides all table rows of class name rowClass
    */
    var trs = document.getElementsByClassName(rowClass);
    if (node.value == 'T'){
        var disp = "table-row";
        if ($('#Arrow').length){ 
            //Hide Sodxtrmts downarrow
            document.getElementById('Arrow').style.display="none"; 
        }      
    }
    else{
        var disp = "none";
        //Show Sodxtrmts downarrow
        if ($('#Arrow').length){       
            document.getElementById('Arrow').style.display="block";
        }
    }
    for (idx=0;idx<trs.length;idx++){
        trs[idx].style.display = disp;
    }
}


function show_div_if_true(node, divID){
    if (node.value == 'T'){
        document.getElementById(divID).style.display = "table-row";
    }
    else{
        document.getElementById(divID).style.display = "none";
    }
}

//Sodxtrmts util hide or show formGraph
function show_formGraph(TF, rowClass) {
    var trs = document.getElementsByClassName(rowClass);
    if (TF == 'T'){
        var disp = "table-row";
    }
    else{
        var disp = "none";
    }
    for (idx=0;idx<trs.length;idx++){
        trs[idx].style.display = disp;
    }
}

//Sodxtrmts util hide or show formGraph
function hide_formGraph(rowClass) {
    var trs = document.getElementsByClassName(rowClass);
    for (idx=0;idx<trs.length;idx++){
        trs[idx].style.display = "none";
    }
    if ($('#generate_graph_row').length){
        document.getElementById('generate_graph_row').style.display = "none";
    }
}

/*
Map updates on user changing 
area_input field via autofill or typing
*/
function update_maps(area_field){
    /*
    Updates maps if user uses autofill or 
    or types in area_input field
    */
    var id = area_field.id;
    var val = area_field.value;
    if (id == 'shape'){
        $('#PolyMap').css('display','block');
        $('#map-polygon').css('display','block');
        initialize_polygon_map(val);
    }
    else if (id == 'location'){
        $('#GridointMap').css('display','block');
        $('#map-gridpoint').css('display','block');
        initialize_grid_point_map(val);
    }
    else if (id == 'bounding_box'){
        $('#BBoxMap').css('display','block');
        $('#map-bbox').css('display','block');
        initialize_bbox_map(val);
    }
    else if (id == 'county' || id == 'county_warning_area' || id == 'climate_division' || id == 'basin'){ 
        $('#OverlayMap').css('display','block');
        $('#map-overlay').css('display','block');
        $('#content-window').css('display','block');
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
            var vl = val_list[0].split(' ')
            name = vl.slice(0,vl.length - 1).join(' ') +  ', ' +vl.slice(vl.length - 1,vl.length);
            //name = val_list[0].split(' ').join(', ');
        }
        else if (id == 'county'){
            name = val_list[0].replace(' County','');
            idx = 1;
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
                if (item.name.toLowerCase() != name.toLowerCase() || item.id != ol_id){
                    continue;
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
                        strokeOpacity: 0.8,
                        strokeWeight: 3,
                        coords:poly_path,
                        area_type: id,
                        name: name,
                        id: area_field.value
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
                    if (state != 'none'){
                        document.getElementById('overlay_state').value = state 
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
                    initialize_map_overlay('map-overlay', poly); 
                    break
                }
            }
        });
    }
    else{
        //Hide all maps
        if ($('#GridpointMap').length && $('#GridpointMap').css('display')!='none'){
            $('#GridpointMap').css('display','none');
            $('#map-gridpoint').css('display','none');
        }
        if ($('#PolyMap').length && $('#PolyMap').css('display')!='none'){
            $('#PolytMap').css('display','none');
            $('#map-polygon').css('display','none');
        }
        if ($('#OverlayMap').length && $('#OverlayMap').css('display')!='none'){
            $('#OverlayMap').css('display','none');
            $('#map-overlay').css('display','none');
            $('#content-window').css('display','none');
            
        }
        if ($('#BBoxMap').length && $('#BBoxMap').css('display')!='none'){
            $('#BBoxMap').css('display','none');
            $('#map-bbox').css('display','none');
        }
    }
}


function set_grid_and_els(node, gridRowId){
    /*
    sets grid type and elements.
    If temporal resolution is monthly or yearly, only allow PRISM data grid and PRISM elements
    else allow all
    */
    var tbl_row_grid = document.getElementById(gridRowId);
    var tbl_row_els = document.getElementById('Els');
    var cell1_grid = tbl_row_grid.firstChild.nextSibling.nextSibling.nextSibling;
    var cell1_els = tbl_row_els.firstChild.nextSibling.nextSibling.nextSibling;
    var maxt_selected = '';
    var mint_selected = '';
    var pcpn_selected = '';
    var els_select = document.getElementById('elements');
    for (i=0;i<els_select.options.length;i++) {
        if (els_select.options[i].selected) {
            el_name = els_select.options[i].value;
            if (el_name == "maxt"){maxt_selected ='selected';}
            if (el_name == "mint"){mint_selected ='selected';}
            if (el_name == "pcpn"){pcpn_selected ='selected';}
        }
    }
    if (node.value == "mly" || node.value == "yly"){
        cell1_grid.innerHTML='<select id="grid" name="grid">' +
        '<option value="21" selected>PRISM(1895-Present)</option>'+ 
        '</select>';
        cell1_els.innerHTML = '<select id="elements" name="elements"' + 
        ' multiple onchange="update_elements(this)">' +
        '<option value="maxt" ' + maxt_selected +'>Maximum Temperature</option>' + 
        '<option value="mint" ' + mint_selected + '>Minimum Temperature</option>' +
        '<option value="pcpn" ' + pcpn_selected +'>Precipitation</option>' +
        '</select>';
        //hide degree day rows and setadd_degree_days to 'F'
        document.getElementById('add_degree_days').value='F'
        //document.getElementById('add_degree_days').options[1].selected = true;
        document.getElementById('add').style.display = "none";
        document.getElementById('dd').style.display = "none"; 
    }
    else{
        cell1_grid.innerHTML='<select id="grid" name="grid">' +
        '<option value="1" selected>NRCC Interpolated(1950-Present)</option>' +
        '<option value="3">NRCC Int. Hi-Res(2007-Present)</option>' +
        '<option value="21">PRISM(1981-Present)</option>' +
        '<option value="4">CRCM+NCEP(1970-2000,2040-2070)</option>' +
        '<option value="5">CRCM+CCSM(1970-2000,2040-2070)</option>' +
        '<option value="6">CRCM+CCSM3(1970-2000,2040-2070)</option>' +
        '<option value="7">HRM3+NCEP(1970-2000,2040-2070)</option>' +
        '<option value="8">HRM3+HadCM3(1970-2000,2040-2070)</option>' +
        '<option value="9">MM5I+NCEP(1970-2000,2040-2070)</option>' +
        '<option value="10">MM5I+CCSM(1970-2000,2040-2070)</option>' +
        '<option value="11">RCM3+NCEP(1970-2000,2040-2070)</option>' +
        '<option value="12">RCM3+CGCM3(1970-2000,2040-2070)</option>' +
        '<option value="13">RCM3+GFDL(1970-2000,2040-2070)</option>' +
        '<option value="14">WRFG+NCEP(1970-2000,2040-2070)</option>' +
        '<option value="15">WRFG+CCSM(1970-2000,2040-2070)</option>' +
        '<option value="16">WRFG+CGCM3(1970-2000,2040-2070)</option>' +
        '</select>';
        cell1_els.innerHTML = '<select id="elements" name="elements"' +  
        ' multiple onchange="update_elements(this)">' +
        '<option value="maxt" ' + maxt_selected +'>Maximum Temperature</option>' +
        '<option value="mint" ' + mint_selected +'>Minimum Temperature</option>' +
        '<option value="avgt">Average Temperature</option>' +
        '<option value="pcpn" ' + maxt_selected +'>Precipitation</option>' +
        '<option value="avgt">Average Temperature</option>' +
        '<option value="hdd">Heating Degree Days(65F/18.3C)</option>' +
        '<option value="cdd">Cooling Degree Days(65F/18.3C)</option>' +
        '<option value="gdd">Growing Degree Days(50F/10C)</option>' +
        '</select>';
        //Show degree day row
        document.getElementById('add').style.display = "table-row";
    }
}
//Delete? replaced by set_smry
function set_data_summary(node, rowId_t, rowId_s){
    if (node.value == 'spatial_summary'){
        document.getElementById(rowId_s).style.display = 'table-row';
        document.getElementById(rowId_t).style.display = 'none';
    }
    else if (node.value =='temporal_summary'){
        document.getElementById(rowId_s).style.display = 'none';
        document.getElementById(rowId_t).style.display = 'table-row';
    }
    else{
        document.getElementById(rowId_s).style.display = 'none';
        document.getElementById(rowId_t).style.display = 'none';
    }
}
