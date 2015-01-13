//Clean functions

//Function to determine if element is in list
String.prototype.inList=function(list){
   return ( list.indexOf(this.toString()) != -1)
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

function set_area_defaults(area_type){
    var lv = {
        'label':'Station ID',
        'value':'RENO TAHOE INTL AP, 266779',
        'autofill_list':'US_' + area_type
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
        lv.value ='Churchill, 32001';
    }
    if (area_type == 'climate_division'){
        lv.label ='Climate Division';
        lv.value ='Northwestern, NV01';
    }
    if (area_type == 'county_warning_area'){
        lv.label ='County Warning Area';
        lv.value ='Las Vegas, NV, VEF';
    }
    if (area_type == 'basin'){
        lv.label ='Basin';
        lv.value ='Hot Creek-Railroad Valleys, 16060012';
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
    return lv;
}

function set_autofill(datalist){
    /*
    Sets autofill lists
    */
    //Grab env var JSON_URL (defined in templates/csc_base.html)
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


function set_form(node_value){
    /*
    Sets additional station or grid from elements
    for single/multi requests: set on select_area element (value: station_id(s) or location(s))
    for area requests: set on data_type element (value station or grid)
    */
    var form_rows_to_show = [], form_rows_to_hide = [];
    if (node_value.inList(['station','station_id','station_ids'])){
        //NOTE: querySelectorAll only works in modern browsers:
        //https://developer.mozilla.org/en-US/docs/Web/API/Document.querySelectorAll
        //form_rows_to_show  = document.querySelectorAll('.station_grid, .station');
        form_rows_to_show = document.getElementsByClassName('station');
        form_rows_to_hide = document.getElementsByClassName('grid');
    }
    if (node_value.inList(['grid','location','locations'])){
        form_rows_to_show = document.getElementsByClassName('grid');
        //form_rows_to_show = Array.prototype.slice.call(form_rows_to_show1).concat(Array.prototype.slice.call(form_rows_to_show2));
        form_rows_to_hide = document.getElementsByClassName('station');
    }
    
    for (idx = 0;idx<form_rows_to_hide.length;idx++) {
        form_rows_to_hide[idx].style.display = 'none';
    } 
    for (idx = 0;idx<form_rows_to_show.length;idx++) {
        form_rows_to_show[idx].style.display = 'table-row';
    }
}

function set_elements(data_type){
    //if data type == grid, disable snow, obst
    //if data type station --> leav all elements enabled
    if (data_type == 'grid' || data_type == 'location' || data_type == 'locations'){
        $("#elements option").each(function(){
            if ($(this).val() == 'obst' || $(this).val() == 'snow' || $(this).val() == 'snwd' || $(this).val() == 'evap'){
                $(this).attr('disabled',true);
            }
        });
    }
    if (data_type == 'station' || data_type == 'station_id' || data_type == 'station_ids'){
        $("#elements option").each(function(){
            if ($(this).val() == 'obst' || $(this).val() == 'snow' || $(this).val() == 'snwd' || $(this).val() == 'evap'){
                $(this).attr('disabled',false);
            }
        });

    }
}

function set_area(row_id,node){
    /*
    Function that updates area row id on user change of node
    node is the area selector element, row_id is the
    row that needs changing, 
    */
    var lv, tbl_row, cell0,cell1,div;
    //Update area default
    lv = set_area_defaults(node.value);
    //Update autofill list
    set_autofill(lv.autofill_list);
    //Update row_id
    tbl_row = document.getElementById(row_id);
    //Override table row
    //cell1 = Label
    cell0 = tbl_row.firstChild.nextSibling;
    cell0.innerHTML= lv.label + ': ';
    //cell2 input
    cell1 = cell0.nextSibling.nextSibling;
    cell1.innerHTML= '<input type="text" id="' + node.value + '" name="'+ 
    node.value +'" value="' +  lv.value + '" list="' + lv.autofill_list + '"' +
    ' onchange="update_value(this.value) & unset_large_request() & set_map(this);" >';
    //Cell3 help text
    pop_id = document.getElementById('area-pop-up');
    pop_id.innerHTML='';
    div = document.createElement('div');
    div.setAttribute('id', 'ht_' + node.value);
    pop_id.appendChild(div); 
    $(div).load(HTML_URL + 'Docu_help_texts.html #ht_' + node.value);
}
//Functions to hide and show maps
//Used in set_map function
function hide_grid_point_map(){
    if ($('#GridpointMap').length){
        document.getElementById('GridpointMap').style.display = "none";
        if ($('#map-gridpoint').length){
            m = document.getElementById('map-gridpoint');
            m.parentNode.removeChild(m);
        }
    }
}

function show_gridpoint_map(){
    //Show gridpoint map
    var gp_map_div = document.getElementById('GridpointMap');
    gp_map_div.style.display = "block";
    if (!$('#map-gridpoint').length){
        var m = document.createElement('div');
        m.setAttribute('id', 'map-gridpoint');
        m.setAttribute('style','width:615px;')
        gp_map_div.appendChild(m);
    }
    //Generate Map
    initialize_grid_point_map();
}

function show_bbox_map() {
    var bb_map_div = document.getElementById('BBoxMap');
    bb_map_div.style.display = "block";
    if (!$('#map-bbox').length){
        var m = document.createElement('div');
        m.setAttribute('id', 'map-bbox');
        m.setAttribute('style','width:600px;');
        bb_map_div.appendChild(m);
    }
    //Generate Map
    initialize_bbox_map();
}

function hide_bbox_map(){
    if ($('#BBoxMap').length){
        var bb_map_div = document.getElementById('BBoxMap');
        bb_map_div.style.display = "none";
        if ($('#map-bbox').length){
            m = document.getElementById('map-bbox');
            m.parentNode.removeChild(m);
        }
    }
}

function hide_overlay_map(){
    var m,w;
    if ($('#OverlayMap').length){
        document.getElementById('OverlayMap').style.display = "none";
        if ($('#map-overlay').length){
            m = document.getElementById('map-overlay');
            m.parentNode.removeChild(m);
        }
        if ($('#content-window').length){
            w = document.getElementById('content-window');
            w.parentNode.removeChild(w);
        }
    }
}

function show_overlay_map(){
    //Show overlay map 
    var host, ol_map_div,kml_file_path,w,m,area_type;
    ol_map_div = document.getElementById('OverlayMap');
    ol_map_div.style.display = "block";
    area_type = document.getElementById('area_type').value;
    host = document.getElementById('host').value;
    kml_file_path = document.getElementById('kml_file_path').value;
    if (!$('#map-overlay').length){
        m = document.createElement('div');
        m.setAttribute('id', 'map-overlay');
        m.setAttribute('style','width:615px;')
        ol_map_div.appendChild(m);
    }
    if (!$('#content-window').length){
        w = document.createElement('div');
        w.setAttribute('id', 'content-window');
        ol_map_div.appendChild(w);
    }
    //Generate Map
    initialize_map_overlays(area_type,host,kml_file_path);
}

function hide_polygon_map(){
    if ($('#PolyMap').length){
        document.getElementById('PolyMap').style.display = "none";
        if ($('#map-polygon').length){
            m = document.getElementById('map-polygon');
            m.parentNode.removeChild(m);
        }
    }
}

function show_polygon_map(){
    //Show polygon map
    var p_map_div = document.getElementById('PolyMap');
    p_map_div.style.display = "block";
    var panel=p_map_div.firstChild;
    if (!$('#map-polygon').length){
        var m = document.createElement('div');
        m.setAttribute('id', 'map-polygon');
        m.setAttribute('style','width:615px;');
        p_map_div.insertBefore(m,panel);
        /*p_map_div.appendChild(m);*/
    }
    //Generate Map
    initialize_polygon_map();
}

function set_map(node){
    /*
    Sets map interfaces for data and applications
    node is the area selector
    */
    //Get TMP env variable (defined in templates/csc_base.html)
    var area_type = node.value;
    var TMP_URL = document.getElementById('TMP_URL').value;
    var state = document.getElementById('overlay_state').value;
    var kml_file_path = TMP_URL + state + '_' + area_type + '.kml';
    document.getElementById('kml_file_path').value=kml_file_path;
    //Update hidden elements
    if (area_type.inList(['basin','county','county_warning_area','climate_division'])) {
        //document.getElementById('select_overlay_by').value= area_type;
        $(".area_type").val(area_type);
    }
    //Set up maps for display
    if (area_type.inList(['basin','county','county_warning_area','climate_division'])) {
        show_overlay_map();
        hide_polygon_map();
        hide_grid_point_map(); 
    } 
    else if (area_type == 'shape') {
        hide_overlay_map();
        show_polygon_map();
        hide_grid_point_map();
    }
    else if (area_type.inList(['location'])){
        hide_overlay_map();
        hide_polygon_map();
        show_gridpoint_map();
    }
    else if (area_type == 'bounding_box'){
        show_bbox_map();
        hide_overlay_map();
        hide_polygon_map();
        hide_grid_point_map();
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


function set_hidden_fields(theForm, mainForm) {
    /*
    Adds the fields of mainForm to 
    theForm as hidden input
    so that user input of mainForm is preserved upon
    theForm submit 
    Used when user updates the overlay map 
    */
    $('#' + mainForm + ' input, #' + mainForm + ' select').each(
    function(index){
        var input = $(this);
        var name = input.attr('name');
        //if (name != "csrfmiddlewaretoken" && name != 'select_stations_by' && name!= 'elements' && name!="overlay_state" && input.attr('type')!="submit"){
        if (name != "csrfmiddlewaretoken" && input.attr('type')!="submit"){
            //Only add visible fields and hidden inputs, omit display:none elements
            if ($(this).is(':visible') || input.attr('type')=="hidden") {
                if (input.attr('name') == 'elements'){
                    //Need to convert elements to list
                    addHidden(theForm, input.attr('name'),input.val().toString());
                }
                else {
                    addHidden(theForm, input.attr('name'), input.val());
                }
            }
        }
    });
    theForm.submit()
}


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

function hide_errors_results_on_change(formID){
    $('#' + formID).find('input,select').change(function(){
        //Hide results
        $('.results').each(function() {
            $(this).css('display','none');
        });

        //Hide appropriate form errors
        //Start and end date may have correlated errors
        $('#form_error').css('display','none');
        if ($('#back_button_error').length){
            $('#back_button_error').css('display','none');
        }
        if ($(this).parent().parent().next().attr('class') == 'form_error'){
            $(this).parent().parent().next().css('display','none');
        }
        if ($(this).attr('id') == 'start_date'){
            if ($('#end_date').parent().parent().next().attr('class') == 'form_error'){
                $('#end_date').parent().parent().next().css('display','none');
            }
        }
        if ($(this).attr('id') == 'end_date'){
            if ($('#start_date').parent().parent().next().attr('class') == 'form_error'){
                $('#start_date').parent().parent().next().css('display','none');
            }
        }
        if ($(this).attr('id') == 'start_year'){
            if ($('#end_year').parent().parent().next().attr('class') == 'form_error'){
                $('#end_year').parent().parent().next().css('display','none');
            }
        }
        if ($(this).attr('id') == 'end_date'){
            if ($('#start_year').parent().parent().next().attr('class') == 'form_error'){
                $('#start_year').parent().parent().next().css('display','none');
            }
        }
    });
}

function reset_area(){
    /*
    select onchange does not fire when user selects same option twice
    Fix for setting area types: add onclick="reset_area()" to each option tag
    NOTE: onclick event for select tag doesn't seem to work in Chrome
    FIX ME!! 
    */
    var timesClicked = $(this).attr('times-clicked') || 0;
    $(this).attr('times-clicked', ++timesClicked);
    if (timesClicked == 1) {
        set_station_grid_select('area',this.parent);
    }
}

function set_degree_days(unit_value){
    if (unit_value == 'metric'){
        if ($('#degree_days').length){
            document.getElementById('degree_days').value = 'gdd13,hdd21';
        }
    }
    else{
       if ($('#degree_days').length){
            document.getElementById('degree_days').value = 'gdd55,hdd70';
        }
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
    }, 9000);
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
    if (element == 'avgt' || element == 'dtr'){
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

function set_BaseTemp(table_id,node){
    /*
    sets sodxtrmts base temperatures for degree day calculations.
    */
    var IMG_URL = document.getElementById('IMG_URL').value;
    var HTML_URL = document.getElementById('HTML_URL').value;
    /*
    if ($('#base_temp').length){
        $('table#tableSodxtrmts tr#base_temp').remove();
    }
    */
    var table = document.getElementById(table_id);
    var element = document.getElementById("element").value;
    if (element =='hdd' || element =='cdd' || element=='gdd'){
        document.getElementById("base_temp").style.display="table-row";
        if (element == 'hdd' || element == 'cdd'){
            document.getElementById("base_temperature").value = '65';
        }
        else{
            document.getElementById("base_temperature").value='50';
        }
    }
    else{document.getElementById("base_temp").style.display="none";}
}

function set_NDay_threshes(){
    /*
    Sets sodxtrmts thersholds for number of days statistics.
    */
    var element = document.getElementById("element").value;
    var threshes = set_threshes(element);
    //Delete old threshes and make new hidded element hidden input
    if ($('#threshes').length){
        document.getElementById("threshes").remove();
    }
    var input = document.createElement('input');
    input.setAttribute('type', 'hidden');
    input.setAttribute('id', 'threshes');
    input.setAttribute('value', threshes);
    document.body.appendChild(input);
    //Check if NDays boxes need to be repopulated
    if ($('#threshold_for_less_or_greater').length){
        var lgb = document.getElementById('less_greater_or_between').value;
        if (lgb == 'l'){
            document.getElementById('threshold_for_less_or_greater').value = threshes.split(',')[0];
        }
        if (lgb == 'g'){
            document.getElementById('threshold_for_less_or_greater').value = threshes.split(',')[1];
        }
    }
    if ($('#threshold_low_for_between').length){
        document.getElementById('threshold_low_for_between').value = threshes.split(',')[2];
    }
    if ($('#threshold_high_for_between').length){
        document.getElementById('threshold_high_for_between').value = threshes.split(',')[3];
    }
}

function set_BaseTemp_and_Threshes(table_id,node){
    /*
    Sets sodxtrmts thresholds and base temperatures
    */
    set_BaseTemp(table_id, node)
    set_NDay_threshes()
}

function set_NDays_threshold_cells(lgb, threshes,cell0, cell1){
    if (lgb == "l"){
        cell0.innerHTML='Less Than';
        cell1.innerHTML ='<input type="text" id="threshold_for_less_or_greater" name="threshold_for_less_or_greater" value='+
        threshes[0] +'>';
    }
    if (lgb == "g"){
        cell0.innerHTML='Greater Than';
        cell1.innerHTML ='<input type="text" id="threshold_for_less_or_greater" name="threshold_for_less_or_greater" value=' +
        threshes[1] + '>';
    }
    if (lgb == "b"){
        cell0.innerHTML='Between<br />And';
        cell1.innerHTML ='<input type="text" id="threshold_low_for_between" name="threshold_low_for_between" value='+
        threshes[2] +'><br />' +
        '<input type="text" id="threshold_high_for_between" name="threshold_high_for_between" value='+
        threshes[3] + '>';
    }
}

function set_NDays_thresholds(table_id,node){
    /*
    sets sodxtrmts thresholds for number of days statisrtics
    */
    IMG_URL = document.getElementById('IMG_URL').value;
    HTML_URL = document.getElementById('HTML_URL').value;
    var table = document.getElementById(table_id);
    //Delete old NDays entries
    if ($('#threshold_type').length){
        $('table#tableSodxtrmts tr#threshold_type').remove();
    }
    if ($('#threshold').length){
        $('table#tableSodxtrmts tr#threshold').remove();
    }
    var stat = document.getElementById('monthly_statistic').value;
    var idx = node.parentNode.parentNode.rowIndex + 1;
    if (stat =='ndays'){
        var row = table.insertRow(parseInt(idx));
        row.setAttribute('id', 'threshold_type');
        var cell0=row.insertCell(0);
        var cell1=row.insertCell(1);
        var cell2 = row.insertCell(2);
        cell0.innerHTML='Number of Days';
        cell1.innerHTML='<select id="less_greater_or_between" name="less_greater_or_between" onchange="change_lgb()">' +
        '<option value="l">Less Than</option>' +
        '<option value="g">Greater Than</option>' +
        '<option value="b">Between</option></select>';
        cell2.innerHTML = '<img alt="Help" title="Help" src="'+ IMG_URL +'QMark.png" class="trigger">' +
        ' <div class="pop-up"><div id="ht_element"></div>' +
        ' <script type="text/javascript">' +
        '$("#ht_element").load("' + HTML_URL + 'Docu_help_texts.html #ht_element");' +
        '</script></div>';

        //Set up thresholds
        var row = table.insertRow(idx + 1);
        row.setAttribute('id', 'threshold');
        var cell0=row.insertCell(0);
        var cell1=row.insertCell(1);
        var cell2 = row.insertCell(2);
        var lgb = document.getElementById("less_greater_or_between").value;
        var threshes = set_threshes(document.getElementById("element").value).split(",");
        set_NDays_threshold_cells(lgb, threshes,cell0, cell1);
        cell2.innerHTML = '<img alt="Help" title="Help" src="' + IMG_URL + 'QMark.png" class="trigger">' +
        ' <div class="pop-up"><div id="ht_element"></div>' +
        ' <script type="text/javascript">' +
        '$("#ht_element").load("' + HTML_URL + 'Docu_help_texts.html #ht_element");' +
        '</script></div>';

        //Set onchange function
        document.getElementById("less_greater_or_between").onchange = function(){
            var lgb = document.getElementById("less_greater_or_between").value;
            var tbl_row = document.getElementById('threshold');
            var cell0 = tbl_row.firstChild;
            var cell1 = cell0.nextSibling;
            set_NDays_threshold_cells(lgb, threshes,cell0, cell1);
        }
    }
}

function change_lgb(){
    /*
    Sets sodxtrmts less than greate or between for number of days statistics
    */
    var lgb = document.getElementById("less_greater_or_between").value;
    var tbl_row = document.getElementById('threshold');
    var cell0 = tbl_row.firstChild;
    cell0 = cell0.nextSibling;
    var cell1 = cell0.nextSibling;
    cell1 =  cell1.nextSibling;
    var threshes = set_threshes(document.getElementById("element").value).split(",");
    set_NDays_threshold_cells(lgb, threshes,cell0, cell1);
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

function set_area_and_map(area_type){
    /*
    Sets area and map interfaces for data and applications
    */
    var TMP_URL = document.getElementById('TMP_URL').value;
    var lv = set_area_defaults(area_type);
    //Change value of hidden var area_type
    document.getElementById('area_type').value = area_type;
    var state = document.getElementById('overlay_state').value;
    var kml_file_path = TMP_URL + state + '_' + area_type + '.kml';
    document.getElementById('kml_file_path').value=kml_file_path;
    if (area_type == 'basin' || area_type == 'county' || area_type == 'county_warning_area' || area_type =='climate_division'){
        document.getElementById('select_overlay_by').value= area_type;
        if ($('#select_stations_by').length){
            document.getElementById('select_stations_by').value=area_type;
        }
        if ($('#select_grid_by').length){
            document.getElementById('select_grid_by').value=area_type;
        }
    }
    //Set up maps for display
    if (area_type =='county' || area_type =='climate_division' || area_type == 'basin' || area_type == 'county_warning_area'){
        show_overlay_map();
        hide_polygon_map();
        hide_grid_point_map(); 
    } 
    else if (area_type == 'shape') {
        hide_overlay_map();
        show_polygon_map();
        hide_grid_point_map();
    }
    else if (area_type == 'location'){
        hide_overlay_map();
        hide_polygon_map();
        show_gridpoint_map();
    }
    else if (area_type == 'bounding_box'){
        show_bbox_map();
        hide_overlay_map();
        hide_polygon_map();
        hide_grid_point_map();
    }
    else {
        hide_overlay_map();
        hide_polygon_map();
        hide_grid_point_map();
        hide_bbox_map();
    }
    return lv;
}

function update_maps(area_field){
    /*
    Updates maps if user uses autofill or 
    or types in area_input field
    */
    var id = area_field.id;
    var val = area_field.value;
    if (id == 'shape'){
        initialize_polygon_map(val);
    }
    else if (id == 'location'){
        initialize_grid_point_map(val);
    }
    else if (id == 'bounding_box'){
        initialize_bbox_map(val);
    }
    else if (id == 'county' || id == 'county_warning_area' || id == 'climate_division' || id == 'basin'){ 
        var json_file = '/csc/media/json/US_' + id + '.json';
        //remove id to just get the name
        var name = val.split(',');
        name.pop();
        name = name.join(',');
        $.getJSON(json_file, function(metadata) {
            for (var i = 0,item; item = metadata[i]; i++){
                if (item.name != name){
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
                        strokeOpacity: 0.8,
                        strokeWeight: 3,
                        coords:poly_path,
                        area_type: id,
                        name: name,
                        id: area_field.value
                    });
                    //Update overlay state
                    var state = 'none';
                    try {
                       var state = item.state.toLowerCase();
                    }
                    catch(e){
                        //Try to find state from name
                        var state = name.split(', ');
                        if (state.length == '1'){
                            state = name.split(',');
                        }
                        try {
                            state = state[1].toLowerCase();
                        }
                        catch(e){
                            state = 'none';
                        }
                    }
                    if (state != 'none' && id != 'basin'){
                        document.getElementById('overlay_state').value = state 
                        document.querySelector('#overlay_state [value="' + state + '"]').selected = true;
                    }
                    else {
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
}

function unset_large_request(){
    //Delete large data request entries
    var large_requests_rows = document.getElementsByClassName('large_request');
    for (i=0;i<large_requests_rows.length;i++) {
        //large_requests_rows[i].style.display = "none";
        large_requests_rows[i].parentNode.removeChild(large_requests_rows[i]);
    }
    //FIX ME: onchange not working correctly when option is not changes
    //Need to delete user name manually
    if ($('#' + 'un').length){
        document.getElementById('un').parentNode.removeChild(document.getElementById('un'));
    }
    //Add html option to data format
    if ($('#data_format').length){
        var df = $('#data_format');
        if (!df.find('option[value=html]').length > 0){
            df.prepend('<option value="html" selected="selected">Html (display on page)</option>')
        }
    }
}


function set_station_grid_select(row_id,node){
    var IMG_URL = document.getElementById('IMG_URL').value;
    var HTML_URL = document.getElementById('HTML_URL').value;
    /*
    Sets area types an maps for data requests and applications
    */
    //hide previous results
    if ($('#' + 'results').length){
        document.getElementById('results').style.display = "none";
    }
    if ($('#' + 'map_legend').length){
        document.getElementById('map_legend').style.display = "none";
    }
    if ($('#' + 'user_params_list').length){
        document.getElementById('user_params_list').style.display = "none";
    }
    if ($('#' + 'datafind').length){
        unset_large_request()
    }
    var lv = set_area_and_map(node.value);
    //Set up autofill if needed
    set_autofill(lv.autofill_list);
    var tbl_row = document.getElementById(row_id);
    //Override table row
    //cell1 = Label
    var cell0 = tbl_row.firstChild.nextSibling;
    cell0.innerHTML= lv.label + ': ';
    //cell2 input
    var cell1 = cell0.nextSibling.nextSibling;
    cell1.innerHTML= '<input type="text" id="' + node.value + '" name="'+ 
    node.value +'" value="' +  lv.value + '" list="' + lv.autofill_list + '"' +
    ' onchange="update_value(this.value) & unset_large_request() & update_maps(this);" >';
    pop_id = document.getElementById('area-pop-up');
    pop_id.innerHTML='';
    var div = document.createElement('div');
    div.setAttribute('id', 'ht_' + node.value);
    pop_id.appendChild(div); 
    $(div).load(HTML_URL + 'Docu_help_texts.html #ht_' + node.value);
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

function set_data_summary(node, rowId_t, rowId_s){
    if (node.value == 'spatial'){
        document.getElementById(rowId_s).style.display = 'table-row';
        document.getElementById(rowId_t).style.display = 'none';
    }
    else if (node.value =='temporal'){
        document.getElementById(rowId_s).style.display = 'none';
        document.getElementById(rowId_t).style.display = 'table-row';
    }
    else{
        document.getElementById(rowId_s).style.display = 'none';
        document.getElementById(rowId_t).style.display = 'none';
    }
}

