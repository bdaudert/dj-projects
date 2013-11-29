function set_autofill(datalist){
    dl = document.createElement('datalist');
    dl.setAttribute('id',datalist);
    dl.setAttribute('class', datalist.replace('US_',''));
    $.getJSON('/csc/media/json/' + datalist + '.json', function(metadata) {
        for (idx=0;idx<metadata.length;idx++){
            var name = metadata[idx].name;
            var id = metadata[idx].id;
            if (id == '' || !id ){
                continue
            }
            var opt = document.createElement('option');
            opt.value = name + ', ' + id;
            opt.setAttribute('class','name')
            //opt.innerHTML = id;
            dl.appendChild(opt);
            /*
            opt = document.createElement('option');
            opt.value = id;
            opt.setAttribute('class','id')
            opt.innerHTML = name;
            dl.appendChild(opt);
            */
        }
    });
    document.body.appendChild(dl);
}

//Dynamic form functions
function highlight_form_field(td_id, err){
    //var td = $('table#tableSodxtrmts td#' + td_id);
    var td = document.getElementById(td_id);
    //td.setAttribute("style","color:red");
    //Grab form field and add error message
    ff = td.nextSibling.nextSibling;
    ff.innerHTML+='<br /><font color="red">' + err + '</font>';

}


function set_threshes(element){
    var threshes = '0.1,0.01,0.01,0.1';
    if (element == 'avgt' || element == 'dtr'){
        threshes = '65,65,40,65';
    }
    if (element == 'maxt'){
        threshes = '40,90,65,80';
    }
    if (element == 'mint'){
        threshes = '32,70,32,40';
    }
    if (element == 'hdd' || element == 'gdd' || element == 'cdd'){
        threshes = '10,30,10,30';
    }
    if (element == 'wdmv'){
        threshes = '100,200,100,200';
    }
    return threshes;
}

function set_BaseTemp(table_id,node){
    //Delete old base temp
    if ($('#base_temp').length){
        $('table#tableSodxtrmts tr#base_temp').remove();
    }
    var table = document.getElementById(table_id);
    var element = document.getElementById("element").value;
    if (element =='hdd' || element =='cdd' || element=='gdd'){
        if (!$('#base_temp').length){
            idx = node.parentNode.parentNode.rowIndex + 1;
            var row=table.insertRow(parseInt(idx));
            row.setAttribute('id', 'base_temp');
            var cell0=row.insertCell(0);
            var cell1=row.insertCell(1);
            var cell2 = row.insertCell(2);
            cell0.innerHTML='Base Temperature';
            cell1.innerHTML='<input type="text" name="base_temperature" value="65">';
            cell2.innerHTML = '<img alt="QMark" title="QMark" src="/csc/media/img/QMark.png" class="icon_small" onClick="ShowHelpText(\'ht_element\')">';
        }
    }
}

function set_NDay_threshes(){
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
    var table = document.getElementById(table_id);
    //Delete old NDays entries
    if ($('#threshold_type').length){
        $('table#tableSodxtrmts tr#threshold_type').remove();
    }
    if ($('#threshold').length){
        $('table#tableSodxtrmts tr#threshold').remove();
    }
    var stat = document.getElementById("monthly_statistic").value;
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
        cell2.innerHTML = '<img alt="QMark" title="QMark" src="/csc/media/img/QMark.png" class="trigger">' +
        ' <div class="pop-up"><div id="ht_element"></div>' +
        ' <script type="text/javascript">' +
        '$("#ht_element").load("{{MEDIA_URL}}html/commons.html #ht_element");' + 
        '</script></div>';
        //cell2.innerHTML = '<img alt="QMark" title="QMark" src="/csc/media/img/QMark.png" class="icon_small" onClick="ShowHelpText(\'ht_element\')">';

        //Set up thresholds
        var row = table.insertRow(idx + 1);
        row.setAttribute('id', 'threshold');
        var cell0=row.insertCell(0);
        var cell1=row.insertCell(1);
        var cell2 = row.insertCell(2);
        var lgb = document.getElementById("less_greater_or_between").value;
        var threshes = set_threshes(document.getElementById("element").value).split(",");
        set_NDays_threshold_cells(lgb, threshes,cell0, cell1);
        cell2.innerHTML = '<img alt="QMark" title="QMark" src="/csc/media/img/QMark.png" class="trigger">' +
        ' <div class="pop-up"><div id="ht_element"></div>' +
        ' <script type="text/javascript">' +
        '$("#ht_element").load("{{MEDIA_URL}}html/commons.html #ht_element");' +
        '</script></div>';
        //cell2.innerHTML= '<img alt="QMark" title="QMark" src="/csc/media/img/QMark.png" class="icon_small" onClick="ShowHelpText(\'ht_element\')">'

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
    if (data_format_node.value == 'clm' ||  data_format_node.value == 'dlm' || data_format_node.value == 'html'){
        document.getElementById(delim_divId).style.display = "table-row";
    }
    else if (data_format_node.value == 'xl'){
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
    //if node.value=true, shows all table rows of class name rowClass
    //if node.value=fals, hides all table rows of class name rowClass
    var trs = document.getElementsByClassName(rowClass);
    if (node.value == 'T'){
        var disp = "table-row";
    }
    else{
        var disp = "none";
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

function hide_gridpoint_map(){
    //Hide gridpoint maip
    document.getElementById('GridpointMap').style.display = "none";
    if ($('#map-gridpoint').length){
        m = document.getElementById('map-gridpoint');
        m.parentNode.removeChild(m);
    }
}

function show_gridpoint_map(){
    //Show gridpoint map
    var gp_map_div = document.getElementById('GridpointMap');
    gp_map_div.style.display = "block";
    if (!$('#map-gridpoint').length){
        var m = document.createElement('div');
        m.setAttribute('id', 'map-gridpoint');
        m.setAttribute('style', 'width:500px;height:400px;');
        gp_map_div.appendChild(m);
    }
    //Generate Map
    initialize_grid_point_map('data_gridded');
}

function hide_overlay_map(){
    //Hide overlay map
    document.getElementById('OverlayMap').style.display = "none";
    if ($('#map-overlay').length){
        var m = document.getElementById('map-overlay');
        m.parentNode.removeChild(m);
    }
    if ($('#content-window').length){
        var w = document.getElementById('content-window');
        w.parentNode.removeChild(w);
    }
}

function show_overlay_map(){
    //Show overlay map 
    var ol_map_div = document.getElementById('OverlayMap');
    ol_map_div.style.display = "block";
    var area_type = document.getElementById('area_type').value;
    var host = document.getElementById('host').value;
    if (!$('#map-overlay').length){
        var m = document.createElement('div');
        m.setAttribute('id', 'map-overlay');
        m.setAttribute('style', 'width:500px;height:400px;')
        ol_map_div.appendChild(m);
    }
    if (!$('#content-window').length){
        var w = document.createElement('div');
        w.setAttribute('id', 'content-window');
        w.setAttribute('style', 'width:100px;height:100px;')
        ol_map_div.appendChild(w);
    }
    //Generate Map
    initialize_map_overlays(area_type,host,kml_file_path);
}

function hide_polygon_map(){
    //Hide poly_map
    document.getElementById('PolyMap').style.display = "none";
    if ($('#map-polygon').length){
        m = document.getElementById('map-polygon');
        m.parentNode.removeChild(m);
    }
}

function show_polygon_map(){
    //Show polygon map
    var p_map_div = document.getElementById('PolyMap');
    p_map_div.style.display = "block";
    if (!$('#map-polygon').length){
        var m = document.createElement('div');
        m.setAttribute('id', 'map-polygon');
        m.setAttribute('style', 'width:500px;height:400px;');
        p_map_div.appendChild(m);
    }
    //Generate Map
    initialize_polygon_map_new();
}

function set_area_defaults(area_type){
    var lv = {
        'label':'Station ID',
        'value':'266779',
        'autofill_list':'US_' + area_type
    }
    if (area_type == 'station_ids'){
        lv.label = 'Station IDs';
        lv.value ='266779,050848';
    }
    if (area_type == 'point'){
        lv.label = 'Location (lon/lat)';
        lv.value = '-119,39';
    }
    if (area_type == 'county'){
        lv.label ='County';
        lv.value ='08051';
    }
    if (area_type == 'climate_division'){
        lv.label ='Climate Division';
        lv.value ='NV01';
    }
    if (area_type == 'county_warning_area'){
        lv.label ='County Warning Area';
        lv.value ='PUB';
    }
    if (area_type == 'basin'){
        lv.label ='Basin';
        lv.value ='10180002';
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

//Station Data
function set_area_and_map(area_type){
    var lv = set_area_defaults(area_type);
    //Change value of hidden var area_type
    document.getElementById('area_type').value = area_type;
    var state = document.getElementById('overlay_state').value;
    var kml_file_path = '/csc/media/tmp/' + state + '_' + area_type + '.kml';
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
        hide_gridpoint_map(); 
    } 
    else if (area_type == 'shape') {
        hide_overlay_map();
        show_polygon_map();
        hide_gridpoint_map();
    }
    else if (area_type == 'point'){
        hide_overlay_map();
        hide_polygon_map();
        show_gridpoint_map();
    }
    else {
        hide_overlay_map();
        hide_polygon_map();
        hide_gridpoint_map();
    }
    return lv;
}

function set_station_grid_select(row_id,node){
    /*
    //Delete existing table row
    if ($('#' + row_id).length){
        $('table#' + table_id + ' tr#' + row_id).remove();
    }
    */
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
    cell1.innerHTML= '<input type="text" id="' + node.value + '" name="'+ node.value +'" value="' +  lv.value + '" list="' + lv.autofill_list +'">'
    //cell3 = helptext
    cell2 = cell1.nextSibling.nextSibling;
    cell2.innerHTML = '<img alt="QMark" title="QMark" src="/csc/media/img/QMark.png" class="trigger">' + 
    ' <div class="pop-up"><div id="ht_' + node.value  + '"></div>' + 
    ' <script type="text/javascript">' +                         
    '$("#ht_' + node.value + '").load("/csc/media/html/commons.html #ht_'+ node.value + '");' + 
    '</script></div>';
}

function set_grid(node, gridRowId){
    var tbl_row_grid = document.getElementById(gridRowId);
    var cell1_grid = tbl_row_grid.firstChild.nextSibling.nextSibling.nextSibling;
    if (node.value == "mly" || node.value == "yly"){
        cell1_grid.innerHTML='<select id="grid" name="grid">' +
            '<option value="21" selected>PRISM(1895-Present)</option>'+ 
            '</select>';
    }
    else{
        cell1_grid.innerHTML='<select id="grid" name="grid">' +
            '<option value="1" {{checkbox_vals.1_selected}}>NRCC Interpolated(1950-Present)</option>' +
            '<option value="3" {{checkbox_vals.2_selected}}>NRCC Int. Hi-Res(2007-Present)</option>' +
            '<option value="4" {{checkbox_vals.4_selected}}>CRCM+NCEP(1970-2000,2040-2070)</option>' +
            '<option value="5" {{checkbox_vals.5_selected}}>CRCM+CCSM(1970-2000,2040-2070)</option>' +
            '<option value="6" {{checkbox_vals.6_selected}}>CRCM+CCSM3(1970-2000,2040-2070)</option>' +
            '<option value="7" {{checkbox_vals.7_selected}}>HRM3+NCEP(1970-2000,2040-2070)</option>' +
            '<option value="8" {{checkbox_vals.8_selected}}>HRM3+HadCM3(1970-2000,2040-2070)</option>' +
            '<option value="9" {{checkbox_vals.8_selected}}>MM5I+NCEP(1970-2000,2040-2070)</option>' +
            '<option value="10" {{checkbox_vals.10_selected}}>MM5I+CCSM(1970-2000,2040-2070)</option>' +
            '<option value="11" {{checkbox_vals.11_selected}}>RCM3+NCEP(1970-2000,2040-2070)</option>' +
            '<option value="12" {{checkbox_vals.12_selected}}>RCM3+CGCM3(1970-2000,2040-2070)</option>' +
            '<option value="13" {{checkbox_vals.13_selected}}>RCM3+GFDL(1970-2000,2040-2070)</option>' +
            '<option value="14" {{checkbox_vals.14_selected}}>WRFG+NCEP(1970-2000,2040-2070)</option>' +
            '<option value="15" {{checkbox_vals.15_selected}}>WRFG+CCSM(1970-2000,2040-2070)</option>' +
            '<option value="16" {{checkbox_vals.16_selected}}>WRFG+CGCM3(1970-2000,2040-2070)</option>' +
            '</select>';
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

