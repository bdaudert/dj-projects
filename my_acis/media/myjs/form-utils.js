//Clean functions

//Needed fo indexOf to work in IE
Array.prototype.indexOf = function(obj, start) {
     for (var i = (start || 0), j = this.length; i < j; i++) {
         if (this[i] === obj) { return i; }
     }
     return -1;
}

//Function to determine if variable is in list
String.prototype.inList=function(list){
   return ( list.indexOf(this.toString()) != -1)
}


function set_vd_variables(no_vd_els){
    /*Disables all variables that are
    in the list no_vd_els*/
    var el_list = all_vd_elements; //dataStore.js
    var var_el_name, opt, i, user_vars;
    if ($('#variables').length){
        user_vars = $('#variables').val();
        var_el_name = 'variables';
    }
    if ($('#variable').length){
        user_vars = [$('#variable').val()];
        var_el_name = 'variable';
    }
    for (i = 0; i < el_list.length; i++){
        if (el_list[i] == 'dtr'){

            $(opt).attr('disabled',true);   
        }
        else if (el_list[i] == 'pet' && $('#app_name').val() != 'monthly_summary'){
            $(opt).attr('disabled',true);
        }
        else{
            opt = '#' + var_el_name + ' option[value="' + el_list[i] + '"]';
            if (el_list[i].inList(no_vd_els)){
                $(opt).attr('disabled',true);
                if (el_list[i].inList(user_vars)){
                    $(opt).prop("selected", false);
                }
            }
            else{
                $(opt).attr('disabled',false);
            }
        }
    }
}


function set_max_min_dates(vd,vd_fut=['9999-99-99','9999-99-99']){
    var max_date = '9999-99-99', min_date = '9999-99-99',
        max_year = '9999', min_year = '9999';
    //Set new min max dates and dates
    //Min max dates
    $('#min_date').val(vd[0]), $('#max_date').val(vd[1]);
    $('#min_year').val(vd[0].slice(0,4)), $('#max_year').val(vd[1].slice(0,4));
    $('#min_date_fut').val(vd_fut[0]), $('#max_date_fut').val(vd_fut[1]);
    $('#min_year_fut').val(vd_fut[0].slice(0,4)), $('#max_year_fut').val(vd_fut[1].slice(0,4));
}

function set_vd(vd, vd_fut=['9999-99-99','9999-99-99']){
    var min_date='9999-99-99', max_date='9999-99-99';
    if (vd !=['9999-99-99','9999-99-99']){
        min_date = vd[0], max_date = vd[1];
    }
    else{
        if ($('#min_date').length){min_date = $('#min_date').val();}
        if ($('#max_date').length){max_date = $('#max_date').val();}
        if (!$('#min_date').length && $('#min_year').length){min_date = $('#min_year').val();}
        if (!$('#max_date').length && $('#max_year').length){max_date = $('#max_year').val();}
    }
    if (vd[0] != '9999-99-99' &&  vd[1] != '9999-99-99'){
        $('#valid_daterange').css('display','block');
        $('#valid_daterange').html('Available: ' + min_date + ' - ' + max_date);
    }
    else{
        $('#valid_daterange').css('display','none');
    }
    //Furture dates
    if (vd_fut[0] != '9999-99-99' && vd_fut[1] != '9999-99-99'){
        var min_date_fut = vd_fut[0], max_date_fut = vd_fut[1];
    }
    else{
        if ($('#min_date_fut').length){min_date_fut = $('#min_date_fut').val();}
        if ($('#max_date_fut').length){min_date_fut = $('#max_date_fut').val();}
        if (!$('#min_date_fut').length && $('#min_year_fut').length){min_date_fut = $('#min_year_fut').val();}
        if (!$('#max_date_fut').length && $('#max_year_fut').length){max_date_fut = $('#max_year_fut').val();}
    }
    if (min_date_fut.inList(['9999-99-99','9999']) || max_date_fut.inList(['9999-99-99','9999'])){
        $('#valid_daterange_fut').css('display','none');
    }
    else{
        if ($('#app_name').val() == 'data_comparison'){
            //Future dateranges do not make sense when comparing to 
            //station data
            $('#valid_daterange_fut').css('display','none');
        }
        else {
            $('#valid_daterange_fut').css('display','block');
            $('#valid_daterange_fut').html('And: ' + min_date_fut + ' - ' + max_date_fut);
        }
    }
}

function set_station_dates(){
    /*
    Sets dates for all multi station request
    Set max/min dates and valid dateranges
    and checks that form dates lie within valid daterange
    */
    var today = new Date(),
        today_string = convertDateToString(today,'-')
    set_max_min_dates(['1850-01-01',today_string]);
    set_vd(['1850-01-01',today_string]);
    if ($('#start_year').length && $('#end_year').length){
        set_year_range();
    }
    check_form_dates();
}

function set_grid_dates(){
     /*
    Sets dates for all multi station request
    Set max/min dates and valid dateranges
    and checks that form dates lie within valid daterange
    */
    var grid = String($('#grid').val()),
        vd = grid_vd[grid][0],
        tr = 'dly';
    if ($('#temporal_resolution').length){
        tr = $('#temporal_resolution').val();
    }
    if (grid == '21'){
        if (tr != 'dly'){
            vd[0] = '1895-01-01';
        }
        else{
            vd[0] = '1981-01-01';
        }
    }
    vd_fut= ['9999-99-99','9999-99-99'];
    if (grid_vd[grid].length > 1 && grid_vd[grid][1].length > 0){
        vd_fut = grid_vd[grid][1];
    }
    set_max_min_dates(vd,vd_fut);
    set_vd(vd,vd_fut);
    if ($('#start_year').length && $('#end_year').length){
        set_year_range();
    }
    check_form_dates();
}

function ajax_set_station_vd(){
    /*
    Sets dates for single station requests
    Executes ajax call to find station valid daterange
    Sets max/min dates and valid daterange
    Checks that form dates lie in valid daterange
    */
    //Check if the station vd has already been computed in this session
    var vd = ['9999-99-99','9999-99-99'];
    if (window.vd_stations.indexOf($('#station_id').val()) != -1){
        //vd was already computed
        var idx =  window.vd_stations.indexOf($('#station_id').val()),
            vd = window.vd_stations_vds[idx],
            no_vd_vars = window.no_vd_vars[idx]
        set_max_min_dates(vd);
        set_vd(vd);
        set_vd_variables(no_vd_vars)
        check_form_dates();
        return;
    }
    var vd = ['9999-99-99','9999-99-99']
    $('.ajax_error').html();
    var msg = 'Finding date range and variables for station';
    waitingDialog.show(msg, {dialogSize: 'sm', progressType: 'warning'});
    var el_list = [], el_tupe = null, 
        response, station_id, station_finder_link; 
    el_list = all_vd_elements
    el_tuple = el_list + ""
    var form_data = 'station_id_change=True';
    form_data+='&csrfmiddlewaretoken=' + $("[name=csrfmiddlewaretoken]").val();
    form_data+='&station_id=' + $('#station_id').val();
    form_data+='&el_tuple=' + el_tuple;
    form_data+='&max_or_min=max';
   
    var new_url = window.location.href.split('?')[0] + form_data;
    $.ajax({
        url:'',
        method: "POST",
        data: form_data,
    })
    .done(function(response) {
        response = JSON.parse(response);
        station_id = response['station_id'];
        set_max_min_dates(response['vd']);
        set_vd(response['vd']);
        set_vd_variables(response['no_vd_els'])
        if ($('#start_year').length && $('#end_year').length){
            set_year_range();
        }
        check_form_dates(); 
        //Update global vars that hold station valid dateranges comoputed in this session
        window.vd_stations.push($('#station_id').val());
        window.vd_stations_vds.push(response['vd']);
        waitingDialog.hide();
        //Notify the user if no vd
        if (response['vd'][0] == '9999-99-99' || response['vd'][1] == '9999-99-99'){
            div_id = create_ajax_no_vd_response(station_id);
            ShowPopupDocu(div_id);
        }
        
    })
    .fail(function(jqXHR) {
        $('.ajax_error').html(get_ajax_error(jqXHR.status));
        set_max_min_dates(['9999-99-99','9999-99-99']);
        set_vd(['9999-99-99','9999-99-99']);
        //Update global vars that hold station valid dateranges comoputed in this session
        vd_stations.push($('#station_id').val());
        vd_stations_vds.push(['9999-99-99','9999-99-99']);
        waitingDialog.hide();
   })
}

// [client side code for showing/hiding content]
function ShowHideTopOfPage(){
    /*
    Deals with google map issue in hidden variables
    Maps in hidden variables get mangled
    when the hidden property changes to visible
    If div is shown and contains map, 
    the map needs to be re-initialized
    */

    var no_results = false;
    if ($('#no_results').length && $('#no_results').css('display') != 'none'){
        var no_results = true;
    }
    if ($('#top_of_page').is(':hidden') || no_results){
        update_maps();
        $(window).resize();
    }
    if (no_results){
        $('#no_results').css('display','none');
    }
    $('#top_of_page').toggle();
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

function check_form_dates(){
    /*
    Function that checks if start/end_date lie within
    valid daterange.If not, new dates are set.
    Returns: 
        new_dates.start: new start date or start year
        new_dates.end: new end date or end year
    */
    var start_date, end_date, year_or_date, 
        ds_past = de_past = ds_fut = de_fut = '9999-99-99',
        today = new Date(), today_string = convertDateToString(today,'-');
    if ($('#start_year').length && $('#end_year').length){
        start_date = $('#start_year').val();
        end_date = $('#end_year').val();
        year_or_date = 'year';
        ds_past = $('#min_year').val() + '-01-01';
        de_past = $('#max_year').val() + today_string.slice(4,today_string.length);
        ds_fut = $('#min_year_fut').val() + '-01-01';
        de_fut = $('#max_year_fut').val() + today_string.slice(4,today_string.length);
    }
    if ($('#start_date').length && $('#end_date').length){
        start_date = $('#start_date').val();
        end_date = $('#end_date').val();
        year_or_date = 'date';
        ds_past = $('#min_date').val(), de_past = $('#max_date').val();
        ds_fut = $('#min_date_fut').val(), de_fut = $('#max_date_fut').val();
    }
    if ($('#year').length){
        start_date = $('#year').val();
        end_date = $('#year').val();
        year_or_date = 'year';
        ds_past = $('#min_year').val() + '-01-01';
        de_past = $('#max_year').val() + today_string.slice(4,today_string.length);
        ds_fut = $('#min_year_fut').val() + '-01-01';
        de_fut = $('#max_year_fut').val() + today_string.slice(4,today_string.length);
    }
    //Sanity check on form dates
    var s = start_date, e = end_date;
    if ($('station_id').length && (s.toLowerCase() == 'por' && s.toLowerCase() == 'por')){
        return;
    }
    if (s.toLowerCase() == 'por'){s = ds_past;}
    if (e.toLowerCase() == 'por'){e = de_past;} 
    if (s == '9999-99-99' || s == '9999'){s = ds_past;}
    if (e == '9999-99-99' || e == '9999'){e = de_past;}
    if (s.length == 4){s = s + '-01-01';}
    if (e.length == 4){e = e + today_string.slice(4,today_string.length);}
    var new_dates = {
        'start': s,
        'end': e
    }
    //Set new min/max_years
    var j_ds = new Date(s), j_de = new Date(e), 
        j_ds_past = new Date(ds_past), j_de_past = new Date(de_past)
        j_ds_fut = new Date(ds_fut), j_de_fut = new Date(de_fut)
    //Quirkiness in js dates
    j_ds.setDate(j_ds.getDate() + 1), j_de.setDate(j_de.getDate() + 1);
    j_ds_past.setDate(j_ds_past.getDate() + 1), j_de_past.setDate(j_de_past.getDate() + 1);
    j_ds_fut.setDate(j_ds_fut.getDate() + 1), j_de_fut.setDate(j_de_fut.getDate() + 1);
    if (ds_fut != '9999-99-99' || de_fut != '9999-99-99'){
        //Only check past dates
        if ( !(j_ds_past <= j_ds && j_de <= j_de_past) ){
            if (j_ds < j_ds_past || j_ds > j_de_past){new_dates.start = ds_past;}
            if (j_de > j_de_past || j_de < j_ds_past){new_dates.end = de_past;}
        }
    }
    else{
        //Need to check future dates too
        if (!(j_ds_past <= j_ds && j_de <= j_de_past) || (j_ds_fut <= j_ds && j_de <= j_de_fut)){
            //Dates are not in valid daterage
            if (!(j_ds_fut <= j_ds && j_de <= j_de_fut)){
                //Set dates to past dates
                if (j_ds < j_ds_past || j_ds > j_de_past){new_dates.start = ds_past; }
                if (j_de > j_de_past || j_de < j_ds_past){new_dates.end = de_past;}        
            }
            else if (!(j_ds_past <= j_ds && j_de <= j_de_past)){
                //Set dates to future dates
                if (j_ds < j_ds_fut || j_ds > j_de_fut){new_dates.start = ds_fut; }
                if (j_de > j_de_fut || j_de < j_ds_fut){new_dates.end = de_fut;}            
            }
        }
    }
    //Check if we only want to return years
    if (year_or_date == 'year'){
        new_dates.start = new_dates.start.slice(0,4);
        new_dates.end = new_dates.end.slice(0,4);
    }
    //Set the new dates
    $('#start_' + year_or_date).val(new_dates.start);
    $('#end_' + year_or_date).val(new_dates.end);
    if ($('#year').length){
        $('#year').val(new_dates.start);
    } 
}

function set_year_range(){
    /*Set date range for drop downs for year range*/
    var today = new Date();
    var today_str = convertDateToString(today, '-')
    var today_yr = today_str.slice(0,4); 
    var max_year = $('#max_year').val(), min_year = $('#min_year').val(), 
        min_year_fut = $('#min_year_fut').val(), max_year_fut = $('#max_year_fut').val();
    var start_year_val = $('#start_year').val(), end_year_val = $('#end_year').val(); 
    //Sanity check on selected values
    if (start_year_val.toLowerCase() == 'por'){
        start_year_val = min_year;
    }
    else{
        if (parseInt(start_year_val) < parseInt(min_year) || parseInt(start_year_val) > parseInt(max_year)){
            start_year_val = min_year;
        }
    }
    end_year_val = String(parseInt(start_year_val) + 10);
    if (parseInt(end_year_val) > parseInt(max_year) || parseInt(end_year_val) < parseInt(min_year)){
        end_year_val = max_year;
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
    if (min_year_fut != '9999' && max_year_fut != '9999'){
        for (i=parseInt(min_year_fut);i<=parseInt(max_year_fut);i++){
            opt = '<option value="' + String(i) + '">' + String(i) + '</option>';
            $('#start_year').append(opt);
            $('#end_year').append(opt);
        }  
    }
    if ($('#area_type').val() == 'station_id'){
        opt = '<option value="POR">POR</option>';
        $('#start_year').prepend(opt);
        $('#end_year').append(opt);
    }
    $('#start_year').val(start_year_val); 
    $('#end_year').val(end_year_val); 
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
    return lv
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


function set_area(area_type_node){
    /*
    UPDATED
    Sets the label and form content
    of the area form variable
    according to area_type
    Also adjusts autofill list 
    and area form variable helptext
    */
    //Empty the old area option
    $('#area-form-input').empty();
    var lv, html_text, area_type = area_type_node.val(),i, pop_id,
        st, state, is_selected = '', kml_file_path = null;
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
    //Set new area label
    $('#area-type-label').html(lv.label);
    //Set new area form input
    if (area_type != 'state'){
        html_text = '<input type="text" id="' + area_type + '" name="'+
        area_type +'" value="' +  lv.value + '" class="area form-control"';
        if (lv.autofill_list != '') {
            html_text+=' list="' + lv.autofill_list + '"';
        }
        html_text+=' onchange="update_value(this.value) & update_maps()" >';
        $('#area-form-input').html(html_text);
    }
    else{
        var select, opt;
        html_text = '<select id="' + area_type + '" name="'+ area_type + '" class="area form-control">';
        html_text+=' onchange="update_value(this.value) & update_maps()" />';
        select = $(html_text);
        for (i=0;i< state_choices.length;i++){  
            st = state_choices[i];
            state = state_names[st];
            if ($('#overlay_state').length){
                if (st == $('#overlay_state').val()){is_selected = ' selected';}
                else{is_selected = '';}
            }
            else{
                if (st == 'nv'){is_selected = ' selected';}
                else {is_selected = '';}
            } 
            //opt = '<option' + selected + ' value="' + st +'">' + state + '</option>';
            if (is_selected){
                $('<option />', {value: st, text: state}).attr('selected','selected').appendTo(select);
            }
            else{
                $('<option />', {value: st, text: state}).appendTo(select);
            }
        }
        select.appendTo('#area-form-input');
    }
    //Set newq help text
    pop_id = $('#area-pop-up');
    pop_id.html('');
    div = $("<div>");
    div.attr('id','ht_' + area_type);
    $(div).load('/csc/media/html/Docu_help_texts.html #ht_' + area_type);
    pop_id.append(div);
}

function set_variables(){
    var non_prism_els = ['gdd','hdd','cdd'];
    var station_only_els = ['obst','snow','snwd','evap','wdmv','dtr','pet'];
    var el_opts = null,el = null;
    if ($('#variables').length){
        el = $("#variables");
        el_opts = $("#variables option");
    }
    if ($('#variable').length){
        el = $("#variable");
        el_opts = $("#variable option");
    }

    if (el_opts){
        el_opts.each(function(){
            //Check if prism data, disable degree days
            if ($('#data_type').val() == 'station' || $('#area_type').val().inList['station_id','station_ids']){
                if ($(this).val() == 'pet'  || $(this).val() == 'dtr'){
                    if ($('#app_name').val().inList(['monthly_summary'])){
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
}


//Functions to hide and show maps
//Used in set_map function
function hide_gridpoint_map(){
    if ($('#GridpointMap').length){
        $('#GridpointMap').css('display','none');
        $('#map-gridpoint').css('display','none');
        $('#zoom-to-map-gridpoint').css('display','none');
    }
}

function show_gridpoint_map(){
    //Show gridpoint map
    $('#GridpointMap').css('display','block');
    $('#map-gridpoint').css('display','block');
    $('#zoom-to-map-gridpoint').css('display','block');
    if ($('#location').length){
        initialize_grid_point_map($('#location').val());
    }
    else{
        initialize_grid_point_map();
    }

}

function hide_gridpoints_map(){
    if ($('#GridpointsMap').length){
        $('#map-gridpoints').css('display','none');
        $('#GridpointsMap').css('display','none');
        $('#zoom-to-map-gridpoints').css('display','none');
    }
}

function show_gridpoints_map(){
    //Show gridpoint map
    $('#GridpointsMap').css('display','block');
    $('#map-gridpoints').css('display','block');
    $('#zoom-to-map-gridpoints').css('display','block');
    if ($('#locations').length){
        initialize_grid_points_map($('#locations').val());
    }
    else{
        initialize_grid_points_map();
    }
}

function show_bbox_map() {
    $('#BBoxMap').css('display','block');
    $('#map-bbox').css('display','block');
    $('#zoom-to-map-bbox').css('display','block');
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
        $('#map-bbox').css('display','none');
        $('#zoom-to-map-bbox').css('display','none');
    }
}

function hide_overlay_map(){
    if ($('#OverlayMap').length){
        $('#OverlayMap').css('display','none');
        $('#map-overlay').css('display','none');
        $('#zoom-to-map-overlay').css('display','none');
    }
    if ($('#content-window').length){    
        $('#content-window').css('display','none');
    }
}

function show_overlay_map(){
    //Show overlay map 
    $('#OverlayMap').css('display','block');
    $('#map-overlay').css('display','block');
    $('#zoom-to-map-overlay').css('display','block');
    $('#content-window').css('display','block');
    update_overlay_map();
}

function hide_polygon_map(){
    if ($('#PolyMap').length){
        $('#PolyMap').css('display','none');
        $('#map-polygon').css('display','none');
        $('#zoom-to-map-polygon').css('display','none');
    }
}

function show_polygon_map(){
    $('#PolyMap').css('display','block');
    $('#map-polygon').css('display','block');
    $('#zoom-to-map-polygon').css('display','block');
    if ($('#shape').length){
        initialize_polygon_map($('#shape').val());
    }
    else {
        initialize_polygon_map();
    }
}


function set_map(){
    /*
    Sets map interfaces for data and applications
    node is the area selector
    */
    var node = $('#area_type');
    var area_type, TMP_URL,state,kml_file_path;
    //Get TMP env variable (defined in templates/csc_base.html)
    area_type = node.val();
    //Update hidden variables
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
        hide_gridpoint_map();
        //hide_gridpoints_map();
        show_overlay_map();
    } 
    else if (area_type == 'shape') {
        hide_overlay_map();
        hide_gridpoint_map();
        //hide_gridpoints_map();
        show_polygon_map();
    }
    else if (area_type.inList(['location'])){
        hide_overlay_map();
        hide_polygon_map();
        show_gridpoint_map();
        //hide_gridpoints_map();
    }
    else if (area_type.inList(['locations'])){
        hide_overlay_map();
        hide_polygon_map();
        hide_gridpoint_map();
        //show_gridpoints_map();
    }
    else if (area_type == 'bounding_box'){
        hide_overlay_map();
        hide_polygon_map();
        hide_gridpoint_map();
        //hide_gridpoints_map();
        show_bbox_map();
    }
    else {
        hide_overlay_map();
        hide_polygon_map();
        hide_gridpoint_map();
        //hide_gridpoints_map();
        hide_bbox_map();
    }
}

function addHidden(theForm, name, value) {
    /*
    Create a hidden input variable with name and value and append it to theForm
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
        //Only save form variables that do not exists in toForm
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

//Show "Loading image"
function show_loading(msg="Processing"){
    /*
    Shows process bar with custom message msg
    */
    waitingDialog.show(msg, {dialogSize: 'sm', progressType: 'warning'});
}

function hide_loading(){
    waitingDialog.hide();
}

function highlight_form_field(field_id, err){
    // Highlights form field and displays error message err
    //if user fills out form incorrectly
    var err_div = $('<div />', {
        class: 'form_error',
        html: '<font color="red">' + err + '</font>'
    });
    $('#' + field_id).parents('div[class^="form-group"]').append(err_div);
}

function set_threshes(variable){
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
    if (variable == 'avgt' || variable == 'dtr' || variable == 'obst'){
        threshes = '65,65,40,65';
        if ($('#units').length){
            u = document.getElementById('units').value;
            if (u == 'metric'){
                threshes = '18,18,4,18';
            }
        }
    }
    if (variable == 'maxt'){
        threshes = '40,90,65,80';
        if ($('#units').length){
            u = document.getElementById('units').value;
            if (u == 'metric'){
                threshes = '4,32,18,27';
            }
        }
    }
    if (variable == 'mint'){
        threshes = '32,70,32,40';
        if ($('#units').length){
            u = document.getElementById('units').value;
            if (u == 'metric'){
                threshes = '0,21,0,4';
            }
        }
    }
    if (variable == 'hdd' || variable == 'gdd' || variable == 'cdd'){
        threshes = '10,30,10,30';
        if ($('#units').length){
            u = document.getElementById('units').value;
            if (u == 'metric'){
                threshes = '-12,-1,-12,-1';
            }
        }
    }
    if (variable == 'wdmv'){
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

function set_BaseTemp(variable){
    /*
    sets sodxtrmts base temperatures for degree day calculations.
    */
    if (variable =='hdd' || variable =='cdd' || variable=='gdd'){
        $('#base_temp').css('display', 'block');
        if (variable == 'hdd' || variable == 'cdd'){
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
        $('#' + divId).css('display', 'block');
    }
    else if (data_format_node.value == 'xl'){
        $('#' + divId).css('display', 'none');
    }
}

function set_delimiter_and_output_file(data_format_node, delim_divId, out_file_divId){
    if (data_format_node.value == 'clm' ||  data_format_node.value == 'dlm'){
        $('#' + delim_divId).css('display', 'block');
    }
    else if (data_format_node.value == 'xl' || data_format_node.value == 'html'){
        $('#' + delim_divId).css('display', 'none');
    }
    if (data_format_node.value == 'clm' ||  data_format_node.value == 'dlm' || data_format_node.value == 'xl'){
        $('#' + out_file_divId).css('display', 'block');
    }
    else if (data_format_node.value == 'html'){
        $('#' + out_file_divId).css('display', 'none');
    }
}


function show_div_if_true(node, divId){
    if (node.value == 'T'){
        $('#' + divId).css('display', 'block');
    }
    else{
        $('#' + divId).css('display', 'none');
    }
}

/*
Map updates on user changing 
area_input field via autofill or typing
*/
function update_maps(){
    /*
    Updates maps if user uses autofill or 
    or types in area_input field
    */
    var area_type = $('#area_type').val(),
        val = $('#' + area_type).val();
    /*
    var id = area_field.id;
    var val = area_field.value;
    */
    //Hide all maps
    $('.zoom-to').css('display','none');
    if ($('#GridpointMap').length){
        $('#GridpointMap').css('display','none');
    }
    if ($('#GridpointsMap').length){
        $('#GridpointsMap').css('display','none');
    }
    if ($('#PolyMap').length){
        $('#PolyMap').css('display','none');
        $('#map-polygon').css('display','none');
    }
    if ($('#OverlayMap').length){
        $('#OverlayMap').css('display','none');
        $('#map-overlay').css('display','none');
        $('#content-window').css('display','none');

    }
    if ($('#BBoxMap').length && $('#BBoxMap').css('display')!='none'){
        $('#BBoxMap').css('display','none');
    }
    //Now show the appropriate map
    if (area_type == 'shape'){
        $('#zoom-to-map-polygon').css('display','block');
        $('#PolyMap').css('display','block');
        $('#map-polygon').css('display','block');
        setTimeout(function(){initialize_polygon_map(val);},500);
    }
    else if (area_type == 'location'){
        $('#zoom-to-map-gridpoint').css('display','block');
        $('#GridointMap').css('display','block');
        initialize_grid_point_map(val);
    }
    else if (area_type == 'locations'){
        $('#zoom-to-map-gridpoints').css('display','block');
        $('#GridointsMap').css('display','block');
        initialize_grid_point_map(val);
    }
    else if (area_type == 'bounding_box'){
        $('#zoom-to-map-bbox').css('display','block');
        $('#BBoxMap').css('display','block');
        $('#map-bbox').css('display','block');
        initialize_bbox_map(val);
    }
    else if (area_type.inList(['county', 'county_warning_area', 'climate_division', 'basin'])){ 
        $('#zoom-to-map-overlay').css('display','block');
        $('#OverlayMap').css('display','block');
        $('#map-overlay').css('display','block');
        $('#content-window').css('display','block');
        var json_file = '/csc/media/json/US_' + area_type + '.json';
        //remove id to just get the name
        var val_list = val.split(', ');
        if (val_list.length == 1){val_list = val.split(',');}
        var name, idx =  1;
        if (area_type == 'county_warning_area' && val_list.length == "3"){
            idx = 2;
            name = val_list[0] + ', ' + val_list[1]
        }
        else if (area_type == 'county_warning_area' && val_list.length == "2"){
            idx = 1;
            var vl = val_list[0].split(' ')
            name = vl.slice(0,vl.length - 1).join(' ') +  ', ' +vl.slice(vl.length - 1,vl.length);
            //name = val_list[0].split(' ').join(', ');
        }
        else if (area_type == 'county'){
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
                        area_type: area_type,
                        name: name,
                        id: val
                    });
                    //Find state from name and update overlay state
                    var state = 'none';
                    if (area_type.inList(['county','climate_division'])){
                        state = item.state.toLowerCase();
                    }
                    if (area_type == 'county_warning_area'){
                        //var state = val.split(', ')[0].split(' ')[1].slice(0,2).toLowerCase();
                        state = item.name.split(', ')[1].toLowerCase();
                    }
                    if (state && state != 'none'){
                        $('overlay_state').val(state); 
                        document.querySelector('#overlay_state [value="' + state + '"]').selected = true;
                    }
                    /*
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
                    */
                    //Update new map
                    set_single_overlay('map-overlay', poly); 
                    break
                }
            }
        });
        if (window.map){
            google.maps.event.addListenerOnce(window.map, 'idle', function() {
                google.maps.event.trigger(window.map, 'resize');
            });
            //google.maps.event.trigger(window.map, 'resize');
        };
    }
    else{
        //Hide all maps
        $('.zoom-to').css('display','none');
        if ($('#GridpointMap').length){
            $('#GridpointMap').css('display','none');
        }
        if ($('#GridpointsMap').length){
            $('#GridpointsMap').css('display','none');
        }
        if ($('#PolyMap').length){
            $('#PolyMap').css('display','none');
            $('#map-polygon').css('display','none');
        }
        if ($('#OverlayMap').length){
            $('#OverlayMap').css('display','none');
            $('#map-overlay').css('display','none');
            $('#content-window').css('display','none');
            
        }
        if ($('#BBoxMap').length && $('#BBoxMap').css('display')!='none'){
            $('#BBoxMap').css('display','none');
        }
    }
}

