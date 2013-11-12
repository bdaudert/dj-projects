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
        cell2.innerHTML = '<img alt="QMark" title="QMark" src="/csc/media/img/QMark.png" class="icon_small" onClick="ShowHelpText(\'ht_element\')">';

        //Set up thresholds
        var row = table.insertRow(idx + 1);
        row.setAttribute('id', 'threshold');
        var cell0=row.insertCell(0);
        var cell1=row.insertCell(1);
        var cell2 = row.insertCell(2);
        var lgb = document.getElementById("less_greater_or_between").value;
        var threshes = set_threshes(document.getElementById("element").value).split(",");
        set_NDays_threshold_cells(lgb, threshes,cell0, cell1);
        cell2.innerHTML= '<img alt="QMark" title="QMark" src="/csc/media/img/QMark.png" class="icon_small" onClick="ShowHelpText(\'ht_element\')">'

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

