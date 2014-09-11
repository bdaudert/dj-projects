/*
function set_href_to_datafind(anchor){
    var href_pre = anchor.href;
    stn_ids = document.getElementById('station_ids_str').value;
    anchor.href = href_pre + '&station_ids=' + stn_ids;
}
*/


function form_change(formID){ 
    $('#' + formID).find('input,select').change(function(){
        //Hide results
        $('.results').each(function() {
            $(this).css('display','none');
        });
        //Hide appropriate form errors
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
    });
}


$(function() {
    $('#link_to_datafind').click(function(event){
        event.preventDefault();
        var href_pre = this.href;
        stn_ids = document.getElementById('station_ids_str').value;
        stn_id_list = stn_ids.split(',');
        stn_ids_html =''
        /*
        for (i=5;i<stn_id_list.length;i+5){
            stn_id_list.splice(i,0,'<br />');
        }
        */
        stn_ids_html = stn_id_list.join(', ');
        //href_pre+='&station_ids=' + stn_ids;
        href_pre+='&station_ids=Multiple Stations';
        dataWindow = window.open(href_pre,'_blank');
        dataWindow.onload = function(){
            dataWindow.document.getElementById('station_ids').value = stn_ids;
            dataWindow.document.getElementById('stn_list').innerHTML = stn_ids_html;
        }
        return dataWindow;
    });
});

function populateFormField(form_name, form_id, label, value){
    //var formFields = document.getElementById(form_name).getElementsByTagName('input');
    var formFields = document.getElementById(form_id).getElementsByTagName('input');
    for (i=0;i<formFields.length;i++){
        if (formFields[i].name == label) {
            formFields[i].value =value;
        }
    }   
}


function precise_round(num,decimals){
    return Math.round(num*Math.pow(10,decimals))/Math.pow(10,decimals);
}

function printNode(ID){
  var NodeToPrint=document.getElementById(ID);
  newWin= window.open("Print_Table_Date");
  newWin.document.write(NodeToPrint.outerHTML);
  newWin.print();
  newWin.close();
}


//Highlights node by setting border, hides  all elements of class DivClass
//and unsets the boder of all other nodes of same class type
function HighLight(node,DivClass,DivId) {
    //node is qmark, divclass is 'docu', DivId is corresponding docu;
    var div_to_show = document.getElementById(DivId)
    var divs_to_hide = document.getElementsByClassName(DivClass);
    var NodeClassName = node.className
    var nodes_to_blur= document.getElementsByClassName(NodeClassName);
    if (node.style.border != "none"){
        //HIDE
        //turn off this qmark
        node.style.border = "none";
        //turn off of the corresponding div
        div_to_show.style.display = "none";
    }
    else {
        //SHOW
        node.style.border ="4px solid #006666";
        //Unborder all other nodes of same class name
        for (i=0;i<nodes_to_blur.length;i++){     
            if (nodes_to_blur[i] != node){
                //qmarks_to_turn_off[i].blur();
                nodes_to_blur[i].style.border="none";
            }
            else{
                nodes_to_blur[i].style.border="4px solid #006666";
            }
        }
        //Hide all divs with class name DivClass except show the one of id=DivId 
        for (i=0;i<divs_to_hide.length;i++){
            if (divs_to_hide[i] != div_to_show){
                divs_to_hide[i].style.display ="none";
            }
            else{
                if (divs_to_hide[i].style.display == "none"){
                    divs_to_hide[i].style.display ="block";
                }
                else{
                    divs_to_hide[i].style.display ="block";
                }
            }
        }
    }
}

function ShowPopupDocu(DivId){
    $( '#' + DivId ).dialog({
        title:'You can move and resize me!',
        resizable: true,
        modal: false,
        width:'auto',
        open: function () {
            $(this).scrollTop(0);
        }
    });
}

function ShowNetworkDocu(NetWork){
    $( '#' + NetWork ).dialog({
        title:NetWork
    });
}

function HideNetworkDocu(NetWork){
    $(".ui-dialog-content").dialog("close");
}



function Toggle(node){
    IMG_URL = document.getElementById('IMG_URL').value;
    // Unfold the branch if it isn't visible
    if (node.nextSibling.style.display == 'none')
    {
        // Change the image (if there is an image)
        if (node.children.length > 0)
        {
            if (node.children.item(0).tagName == "img")
            {
                node.children.item(0).src = IMG_URL + "minus.gif";
            }
        }

        node.nextSibling.style.display = '';
    }
    // Collapse the branch if it IS visible
    else
    {
        // Change the image (if there is an image)
        if (node.children.length > 0)
        {
            if (node.children.item(0).tagName == "img")
            {
                node.children.item(0).src = IMG_URL + "plus.gif"; 
            }
        }

        node.nextSibling.style.display = 'none';
    }

}


function popup_window(mylink, windowname)
{
    if (! window.focus)
    {
        return true;
    }
    var href;
    if (typeof(mylink) == 'string')
    {
        href=mylink;
    }
    else
    {
        href=mylink.href;
    }
    //var height = 800;
    //var width = 800;
    var height = window.height - 50;
    var width = window.width - 50;
    window.open(href, windowname, 'width=' + width + ',height=' + height + ',scrollbars=yes');
    return false;
}

// [client side code for showing/hiding content]
function ShowHide(divId){
    obj = document.getElementById(divId);
    if (obj.style.display == 'none')
    {
        obj.style.display = 'block';
        //Show print button if divId is printable table
        if (divId == 'printable_table' && $('#print_button').length){
            document.getElementById('print_button').style.display = 'block';
        }
    } 
    else 
    {
        obj.style.display = 'none';
        if (divId == 'printable_table' && $('#print_button').length){
            document.getElementById('print_button').style.display = 'none';
        }
    }
}

//Hide all pop-ups if user clicks anywhere but a trigger/help title
$(document).click(function(e){
    if( e.target.title != 'Help'){
        $('.pop-up').css('display','none');
    }
 });

//Shows documentation in pop up box upon hover
$(function() {

  $('.trigger_hover').hover(function(e) {
    $(this).next('div.pop-up').show();
  }, function() {
    $(this).next('div.pop-up').hide();
  });
  //$(this).next('div.pop-up').css('top', e.pageY).css('left', e.pageX );
  // $(this).next('div.pop-up').show().css('top', e.pageY - moveDown).css('left', e.pageX + moveLeft);
  //});

  $('.trigger').click(function(e) {
    var pop_up = $(this).next('div.pop-up');
    var display = $(this).next('div.pop-up').css('display');
    /*
    if (display != 'none') {
        $(this).next('div.pop-up').css('display','none');
    }
    else {
        $(this).next('div.pop-up').css('display','block');
    }
    */
    //Close all other pop-ups 
    $('.pop-up').each(function(i, pop) {
        if ($(pop).is(pop_up)){
             if (display == 'none') {      
                pop.style.display = 'block';
             }
            else{
                pop.style.display = 'none';
            }
        }
        else{
            pop.style.display = 'none';
        }
    });
    /*
    for (i=0;i<pops.length;i++){
        if (pops[i]!= $(this).next('div.pop-up')){
            pops[i].style.display="none";
        }
    }
    */
  });
    /*
    $(this).next('div.pop-up').css("display","block");
  }, function() {
    $(this).next('div.pop-up').css("display","none");
  });
    */
}); 


function showIt(Id)
{
document.getElementById(Id).style.display="inline";
}


function hideIt(Id)
{
document.getElementById(Id).style.display='none';
}

/*Sodxtrmts Utils*/
function set_date_idx_and_mon_list(initial, initial_graph){
    /*
    Utility to find list of indices of months in
    graph_start_month - graph_end month
    as well as a list of months
    if the analysis starts at start_month
    graph_start/graph_end/start_month are of form '01' - '12'
    Used in hc-sodxtrmts-visualize.js
    */
    results = {
        'month_list':[],
        'data_idx_list':[]
    }
    if (parseInt(initial_graph.graph_start_month)>parseInt(initial_graph.graph_end_month)){
        for (var m = parseInt(initial_graph.graph_start_month);m<=12;m++){
            results.month_list.push(m);
            if (initial.start_month != "01"){
                var idx = 12 - parseInt(initial.start_month) + 1 + m;
                if (idx > 12){idx-=12;}
                results.data_idx_list.push(idx);
            }
            else{
                results.data_idx_list.push(m);
            }
        }
        for (var m = 1;m <= parseInt(initial_graph.graph_end_month);m++){
            results.month_list.push(m);
            if (initial.start_month != "01"){
                var idx = 12 - parseInt(initial.start_month) + 1 + m;
                if (idx > 12){idx-=12;}
                results.data_idx_list.push(idx);
            }
            else{
                results.data_idx_list.push(m);
            }
        }
    }
    else {
        for (var m = parseInt(initial_graph.graph_start_month);m<=parseInt(initial_graph.graph_end_month);m++){
            results.month_list.push(m);
            if (start_month != "01"){
                var idx = 12 - parseInt(initial.start_month)+ 1 + m;
                if (idx > 12){idx-=12;}
                    results.data_idx_list.push(idx);
                }
                else{
                    results.data_idx_list.push(m);
                }
            }

    }
    return results
}

function set_summary_text(summary){
    /*
    Sodxtrmts utility to set graph summary text
    */
    if (summary == 'max'){var SummaryText = 'Maximum of ';}
    if (summary == 'min'){var SummaryText = 'Minimum of ';}
    if (summary == 'sum'){var SummaryText = 'Sum of ';}
    if (summary == 'mean'){var SummaryText = 'Average of ';}
    if (summary == 'individual'){var SummaryText = ' ';}
    return SummaryText;
}

function set_start_end_yr_idx(datadict,initial,initial_graph){
    /*
    sets start/emnd year inidices for visualization of sodxtrmts data analysis
    */
    var results = {
        'yr_start_idx':null,
        'yr_end_idx':null
    };
    results.yr_start_idx = 0;
    results.yr_end_idx = datadict.data.length - 6;
    if (initial_graph.graph_start_year.toLowerCase() !='por'){
        results.yr_start_idx = parseInt(initial_graph.graph_start_year) - parseInt(datadict.start_date);
    }
    if (initial_graph.graph_end_year.toLowerCase() !='por'){
        results.yr_end_idx = results.yr_end_idx - (datadict.end_date - parseInt(initial_graph.graph_end_year));
    }
    return results
}

function set_sodxtrmts_series_data_individual(datadict,initial,initial_graph,series,chart_type){
    /*
    Sets sodxtrmts time series (chart_type = line) or barchart data (chart_type = column) 
    for plotting of individual months in sodxtrmts analysis
    acis_data are year_string, val pairs
    acis_data are needed to set x_plotlines correctly 
    */ 
    var results = {
        'x_cats':[],
        'series_data':[],
        'acis_data':[],
        'data_max':null,
        'data_min':null
    }
    var yr_indices = set_start_end_yr_idx(datadict, initial, initial_graph);
    var md = set_date_idx_and_mon_list(initial,initial_graph);
    var yr_change_idx = 12 - parseInt(initial.start_month) + 2;
    var month_names =  ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    for (var mon_idx=0;mon_idx<md.month_list.length;mon_idx++){
        data = [];
        values=[];
        var s = {};
        for (var key in series){
            s[key] = series[key];
        }
        s['name'] = month_names[md.month_list[mon_idx]-1];
        for (var yr_idx=yr_indices.yr_start_idx;yr_idx<yr_indices.yr_end_idx;yr_idx++) {
            var date;
            if (md.data_idx_list[mon_idx] == yr_change_idx && initial.start_month !="01"){
                date = Date.UTC(parseInt(datadict.data[yr_idx][0]) + 1 , 0, 1)
            }
            else {
                date = Date.UTC(parseInt(datadict.data[yr_idx][0]), 0, 1)
            }
            results.x_cats.push(datadict.data[yr_idx][0]);
            var val = datadict.data[yr_idx][2*md.data_idx_list[mon_idx] - 1]
            if (val != '-----') {
                values.push(precise_round(parseFloat(val),2));
                data.push([date, precise_round(parseFloat(val),2)]);
                if (mon_idx == 0){
                    results.acis_data.push([parseInt(datadict.data[yr_idx][0]), precise_round(parseFloat(val),2)]);
                }
            }
            else {
                values.push(null);
                data.push([date,null]);
                if (mon_idx == 0){
                    results.acis_data.push([parseInt(datadict.data[yr_idx][0]),null]);
                }
            }
        }
        if (chart_type == 'column'){
            s['data'] = values;
        }
        else {
            s['data'] =  data;
        }
        results.series_data.push(s);
        //Find max/min of data (needed to set plot properties)
        if (mon_idx == 0){
            results.data_max = Math.max.apply(Math,values);
            results.data_min = Math.min.apply(Math,values);
        }
        else{
            var max = Math.max.apply(Math,values);
            var min = Math.min.apply(Math,values);
            if (max > results.data_max){
                results.data_max = max;
            }
            if (min < results.data_min){
                results.data_min = min;
            }
        }
    }
    //Override data_max/min if needed
    if (initial_graph.vertical_axis_max != "Use default") {
        try{
            results.data_max = parseFloat(initial_graph.vertical_axis_max);
        }
        catch(e){}
        }
    if (initial_graph.vertical_axis_min != "Use default") {                                                                     try{
            results.data_min = parseFloat(initial_graph.vertical_axis_min);
        }
        catch(e){}
    }
    return results
}

function set_sodxtrmts_series_data_summary(datadict,initial,initial_graph,series, chart_type){
    /*
    Sets sodxtrmts time series (chart_type = line) or barchart data (chart_type = column)
    for summary over months 
    acis_data are year_string, val pairs
    acis_data are needed to set x_plotlines correctly 
    */

    var results = {
        'x_cats':[],
        'series_data':[],
        'acis_data':[],
        'data_max':null,
        'data_min':null
    }
    //Complete series style
    var s = {};
    for (var key in series){
        s[key] = series[key];
    }
    var SummaryText = set_summary_text(initial_graph.graph_summary);
    s['name'] = SummaryText + datadict.monthly_statistic;
    s['color'] = '#00008B'; 
    if (initial_graph.markers == 'F'){
        s['marker'] = {enabled:false};
    }
    //Set up data arrays and find indices
    var data = [];
    var values = [];
    var yr_indices = set_start_end_yr_idx(datadict, initial, initial_graph);
    var md = set_date_idx_and_mon_list(initial,initial_graph);
    var yr_change_idx = 12 - parseInt(initial.start_month) + 2;
    var month_names =  ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var mischr = ["fake","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"];
    //Year Loop
    for (var yr_idx=yr_indices.yr_start_idx;yr_idx<yr_indices.yr_end_idx;yr_idx++) {
        var vals = [];
        var skip_year = 'F';
        //Depending on start month, pick the correct data
        if (md.month_list[0]> md.month_list[md.month_list.length -1] && initial.start_month != "01"){
            var date = Date.UTC(parseInt(datadict.data[yr_idx][0]) + 1, 0, 1);
            var acis_date = parseInt(datadict.data[yr_idx][0]);
        }
        else {
            var date = Date.UTC(parseInt(datadict.data[yr_idx][0]), 0, 1);
            var acis_date = parseInt(datadict.data[yr_idx][0]);
        }
        results.x_cats.push(datadict.data[yr_idx][0]);

        for (var mon_idx=0;mon_idx<md.data_idx_list.length;mon_idx++) {
            var val = datadict.data[yr_idx][2*md.data_idx_list[mon_idx] - 1];
            var flag = datadict.data[yr_idx][2*md.data_idx_list[mon_idx]].toString();
            //Check if we need to skip this year
            if ((mischr.indexOf(flag) > datadict.initial.max_missing_days || val == '-----') && 
            initial_graph.graph_plot_incomplete_years == 'F') {
                skip_year = 'T';
                break;
            }
            if (val != '-----') {
                vals.push(parseFloat(val));
            }
        } //end month loop  

        //Summarize data
        if (skip_year == 'T'){
            if (chart_type == 'column'){
                data.push(null);
            }
            else {
                data.push([date, null]);
            }
            results.acis_data.push([acis_date,null]);
            continue;
        }
        var d = set_data_summary_series(date, vals,initial_graph.graph_summary,chart_type);
        var acis_d = set_data_summary_series(acis_date,vals,initial_graph.graph_summary,'line');
        var val = compute_data_summary(vals,initial_graph.graph_summary);
        data.push(d); results.acis_data.push(acis_d);
        if (!!val){values.push(val);}
    } //End yr loop
    //Push series data
    s['data'] = data;
    results.series_data.push(s); 

    //Find data min/max
    if (values.length > 0){
        results.data_max = find_max(values,datadict.element,datadict.initial.monthly_statistic);
        results.data_min = find_min(values,datadict.element,datadict.initial.monthly_statistic,datadict.initial.departures_from_averages);
    }
    //Override max/min if needed
    if (initial_graph.vertical_axis_max != "Use default") { 
        try{
            results.data_max = parseFloat(initial_graph.vertical_axis_max);
        }
        catch(e){}
    }
    if (initial_graph.vertical_axis_min != "Use default") {
        try{
            results.data_min = parseFloat(initial_graph.vertical_axis_min);
        }
        catch(e){}
    }

    //Compute Running Mean if desired
    if (initial_graph.graph_show_running_mean == 'F'){
        return results;
    }
    var rm_yrs = parseInt(initial_graph.graph_running_mean_years); 
    var running_mean_data = compute_running_mean(data,rm_yrs, chart_type);
    s = {};
    for (var key in series){
        s[key] = series[key];
    }
    s['name']= initial_graph.graph_running_mean_years.toString() + '-Year Running Mean';
    s['type'] = 'spline';
    s['color'] = 'red';
    s['marker'] = {enabled:false};
    s['data'] = running_mean_data;
    results.series_data.push(s);
    return results;
}
