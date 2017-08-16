String.prototype.rsplit = function(sep, maxsplit) {
    //js equivalent to python rspilt
    var split = this.split(sep);
    return maxsplit ? [ split.slice(0, -maxsplit).join(sep) ].concat(split.slice(-maxsplit)) : split;
}

//Function to determine if variable is in list
String.prototype.inList=function(list){
   return ( list.indexOf(this.toString()) != -1)
}


function int_time_to_date_string(int_time_epoch){
    //int_time_epoch is seconds since 19700101
    var d = new Date(0); // The 0 there is the key, which sets the date to the epoch
    d.setUTCSeconds(int_time_epoch / 1000);
    month = '' + (d.getMonth() + 1),
    day = '' + d.getDate(),
    year = d.getFullYear();
    return year + '-' + month + '-' + day;
}

function set_back_date(num_days){
    var d = new Date();
    d.setDate(d.getDate() - parseInt(num_days));
    var mm = String(d.getMonth() + 1); // getMonth() is zero-based
    var dd = String(d.getDate());
    if (mm.length == 1){mm = '0' + mm};
    if (dd.length == 1){dd = '0' + dd};
    return [String(d.getFullYear()), mm, dd].join('-');
}

function advance_date(date, num_days, back_or_forward){
    /*
    date needs to be of format yyyy-mm-dd
    */
    var d = new Date(date);
    if (back_or_forward = 'back'){
        d.setDate(d.getDate() - (parseInt(num_days) + 1) );
    }
    if (back_or_forward = 'forward'){
        d.setDate(d.getDate() + (parseInt(num_days) + 1));
    }
    var mm = String(d.getMonth() + 1); // getMonth() is zero-based
    var dd = String(d.getDate());
    var yyyy = String(d.getFullYear())
    if (mm.length == 1){mm = '0' + mm};
    if (dd.length == 1){dd = '0' + dd};
    return [yyyy, mm, dd].join('-');
}


function zoomToLocation() {
    var address = document.getElementById('address').value;
    var geocoder = new google.maps.Geocoder();
    var map = window.map;
    if ($('#app_name').val() == 'station_finder'){
        map = window.sf_map;
    }
    geocoder.geocode( { 'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
           map.setCenter(results[0].geometry.location);
           map.setZoom(7);
           if (window.marker){
                window.marker.setPosition(results[0].geometry.location);
                var lat = results[0].geometry.location.lat();
                var lon = results[0].geometry.location.lng();
                var infowindow = infowindow = new google.maps.InfoWindow({
                    content: '<div id="MarkerWindow" ' +
                    'style="line-height:1.35;overflow:hidden;white-space:nowrap;">'+
                    '<p><b>Lat: </b>' + lat + '<br/>'+
                    '<b>Lon: </b>' + lon + '<br/>' +
                    '</div>',
                    maxWidth: 100
                });
                infowindow.open(window.map, window.marker);
                if ($('#location').length) {
                    $('#location').val(String(lon) + ',' + String(lat));
                }
            }
            if (window.polygon){
                window.polygon.setMap(null);
                $('#shape').val('');
            }
        }
        else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
  });
}

function inrange(min,number,max){
    if ( !isNaN(number) && (number >= min) && (number <= max) ){
        return true;
    } else {
        return false;
    };
}


function get_ajax_error(ajax_status){
    if (ajax_status == 500) {
        return 'Internal Server Error [500].';
    }
    if(ajax_status == 429){
        return 'Too many requests.';
    }
    else{
        return 'An unknown error occured.';
    }

}

function convertDateToString(date, sep){
        yr = String(date.getFullYear());
        mon = String(date.getMonth() + 1);
        day = String(date.getDate());
        if (String(mon).length == 1){
            mon = '0' + mon;
        }
        if (String(day).length == 1){
            day = '0' + day;
        }
        return yr + sep + mon + sep + day;
}

function DateStringToJSDateString(date){
    /*
    Return date in format yyy-mm-dd
    */
    if (date.length == 8){
        return date.slice(0,4) + '-' + date.slice(4,6) + '-' + date.slice(6,8);
    }
    else if (date.length == 10){
        return date.slice(0,4) + '-' + date.slice(5,7) + '-' + date.slice(8,10);
    }
    else{
        return date
    }

}


function form_change(formID){ 
    $('#' + formID).find('input,select').change(function(){
        //Hide results
        $('.results').css('display','none');
        //Hide form errors
        $('.form_error').css('display','none');
    });
}


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
  newWin= window.open("Print_Table_Data");
  newWin.document.write(NodeToPrint.outerHTML);
  newWin.print();
  //newWin.close();
}


//Highlights node by setting border, hides  all variables of class DivClass
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
        node.style.border ="4px solid #989898";
        //Unborder all other nodes of same class name
        for (i=0;i<nodes_to_blur.length;i++){     
            if (nodes_to_blur[i] != node){
                //qmarks_to_turn_off[i].blur();
                nodes_to_blur[i].style.border="none";
            }
            else{
                nodes_to_blur[i].style.border="4px solid #989898";
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

function create_ajax_no_vd_response(station_id){
    var today = new Date(),
        today_string = convertDateToString(today,'-')
    var station_finder_link = '/csc/scenic/analysis/station_finder/?area_type=station_id';
    station_finder_link+='&station_id=' + station_id;
    station_finder_link+='&variables=maxt&variables=mint&variables=pcpn';
    station_finder_link+='&variables=snow&variables=snwd&variables=gdd&variables=hdd&variables=cdd';
    station_finder_link+='&start_date=1850-01-01&end_date=' + today_string;
    station_finder_link+='&variables_constraints=any&dates_constraints=any';
    var html ='<p class="error large">'; 
    html+=station_id + ' has no data for the chosen variable(s)!</p>';
    html+= '<p class="bg-info large" style="border:1px solid black;padding:5px;">';
    html+='Please uss the <a class="link" target="_blank" href="' + station_finder_link + '">Station Finder</a>';
    html+=' to find valid variables and date ranges.<p>'
    $(document.body).append('<div id="no_vd"></div>');
    $('#no_vd').html(html);
    $('#no_vd').css('display','none') 
    return 'no_vd';
}

function DestroyPopupDocu(DivId){
    $('#' + DivId).dialog('destroy');
}

function ShowPopupDocu(DivId){
    var title = 'You can move and resize me!',
        wWidth = $(window).width(),
        width = 'auto';
        max_height = $(window).height()*0.6,
        max_width = wWidth * 0.6;
    if ($('#' + DivId).attr('title')){
        title = $('#' + DivId).attr('title');
    }    
    //Close all dialogs that happen to be open
    $(':ui-dialog').each(function(){
        var pop_id = $(this).attr('id');
        if ($(this).dialog('isOpen')){
            //console.log(pop_id);
            if (!pop_id.inList(popup_no_destroy)){
                //see dataStore.js
                //console.log($(this).attr('id'));
                $(this).dialog('destroy');
            }
        }
    });
    try {
        var bootstrapButton = $.fn.button.noConflict();
        $.fn.bootstrapBtn = bootstrapButton;
    }catch(e){};
    
    if (DivId == 'formDownload' || DivId == 'largeRequestForm'){
        max_width = wWidth * 0.3;
    }
    if (DivId.inList('Docu_howto_scenic_data,Docu_CCTAG_report,Docu_howto_scenic_manual,Docu_howto_climate_primer')){
        max_width = wWidth * 0.9;
        width = wWidth * 0.6;
    }
    if (DivId.inList('Docu_COOP,Docu_GHCN,Docu_ICAO,Docu_NWSLI,Docu_FAA,Docu_WMO,Docu_WBAN,Docu_CoCoRaHS,Docu_Threadex')){
        max_width = wWidth * 0.3;
    }
    //Open the dialog
    $( '#' + DivId ).dialog({
        position:{
            my:'center',
            at:'center',
            of:window
        },
        title:title,
        resizable: true,
        id: DivId,
        modal: false,
        width:width,
        height:'auto',
        create: function(){
            $(this).css("maxWidth", max_width);
            $(this).css("maxHeight", max_height);
        },
        open: function() {
            $(this).scrollTop(0);
            $(this).closest(".ui-dialog")
            .find(".ui-dialog-titlebar-close")
            .removeClass("ui-dialog-titlebar-close")
            .html("<span class='ui-button-icon-primary ui-icon ui-icon-closethick'></span>");
        },
        close: function () {
            $(this).dialog('destroy');
        }
    });
    $( '#' + DivId ).scrollTop(0);
    $(".ui-dialog").css("z-index", 10);
    $(".ui-widget-content").css("background-color", "#dedede");
    $(".ui-widget-header").css("color", "#000000");
    $(".ui-widget-header").css("background-color", "#ffffff");
    $(".ui-icon").css("background-color", "#000000");
    $(".ui-icon").css("background-color", "#ffffff");
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
    var height = String(window.innerHeight);
    var width = String(window.innerWidth - 400);
    var attrs = "width=" + width + ",height=" + height + ",scrollbars=yes,toolbar=yes,top=500,left=500";
    window.open(href, windowname, "width=" + width + ",height=" + height,"scrollbars=yes");
    return false;
}

// [client side code for showing/hiding content]
function ShowHide(divId){
    var div = $('#' + divId);
    if (div.css('display') == 'none'){
        div.css('display','block');
    }
    else{
        div.css('display','none');
    }
}

function ShowSodsummTab(divId){
    var id;
    $('.sodsumm-tab').each(function(){
        id = $(this).attr('id');
        var hc_container = $('#' + id + ' div:first-child').attr('id');
        if (id == divId){
            $(this).css('display','block');
            $('#nav-' + id).addClass('active');
            var h = $(window).height();
            var w = $(window).width();
            $('#' + hc_container).css('width', w*0.66);
            $('#' + hc_container).css('height', h*0.6);
            var chart = $('#' + hc_container).highcharts();
            setTimeout(function () {
                chart.reflow();
            });
        }
        else {
            $(this).css('display','none');
            $('#nav-' + id).removeClass('active');
        }
    });
}

//Shows documentation in pop up box upon hover
$(function() {
    $('.trigger_hover').hover(function(e) {
        $(this).next('div.pop-up').show();
    }, function() {
        $(this).next('div.pop-up').hide();
    });

    $('.trigger').click(function(e) {
        var pop_up = $(this).next('div.pop-up');
        var display = $(this).next('div.pop-up').css('display');
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
  });
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


//DATA UTILS
function findMedian(data) {

    // extract the .values field and sort the resulting array
    var m = data.map(function(v) {
        return v;
    }).sort(function(a, b) {
        return a - b;
    });

    var middle = Math.floor((m.length - 1) / 2); // NB: operator precedence
    if (m.length % 2) {
        return m[middle];
    } else {
        return (m[middle] + m[middle + 1]) / 2.0;
    }
}

function findSum(data){
    var sum = null;
    if (data.length > 0) {
        sum = data.reduce(function(a,b) {
            return a + b;
        });
    }
    return sum
}

function compute_summary(data, smry){
    smry_data = {
        'data':[],
        'ranges':[]
    };
    //time period loop
    for (i = 0;i<data[0].length;i++){
        var date_int = data[0][i][0];
        var vals_to_summarize = [];
        //data loop
        for (j=0;j<data.length;j++){
                try{ var val = data[j][i][1]; }
                catch(e){ var val = null; }

                if (val != null){
                    vals_to_summarize.push(data[j][i][1]);
                }
        }
        //Summarize
        var max = Math.max.apply(null,vals_to_summarize);
        var min = Math.min.apply(null,vals_to_summarize);
        if (min == Number.POSITIVE_INFINITY || min == Number.NEGATIVE_INFINITY){
            min = null;
        }
        if (max == Number.POSITIVE_INFINITY || max == Number.NEGATIVE_INFINITY){
            max = null;
        }
        var sum = findSum(vals_to_summarize);
        var s = null;
        if (vals_to_summarize.length >0){
            if (smry == 'mean'){
                if (vals_to_summarize.length > 0  && sum != null) {
                    s =  sum / vals_to_summarize.length;
                }
            }
            if (smry == 'sum'){
                s = sum;
            }
            if (smry == 'max'){
                s = max;
            }
            if (smry == 'min'){
                s = min;
            }
            if (smry == 'median'){
                s = findMedian(vals_to_summarize);
            }
        }
        smry_data.ranges.push([date_int, min, max]);
        smry_data.data.push([date_int,s]);
    }
    return smry_data
}

function compute_running_mean(data,running_mean_period){
    var running_mean_data = [];
    if (running_mean_period%2 == 0){
        var num_nulls =running_mean_period/2 - 1;
    }
    else{
        var num_nulls =(running_mean_period - 1)/2;
    }
    for (var idx=0;idx<data.length;idx++) {
        var skip = 'F';
        var rm_data = [];
        if (idx >= num_nulls &&  idx <= data.length - 1 - num_nulls) {
            var cnt = 0;
            for(var i=idx - num_nulls,sum=0;i<=idx + num_nulls;i++){
                var val = data[i][1];
                if (val != null){
                    sum+=val;
                    cnt+=1;
                }
                else{
                    skip = 'T';
                    break;
                }
            }
            if (cnt > 0 && skip =='F'){
                rm_data = [data[idx][0],parseFloat(sum)/parseFloat(cnt)];
            }
        }
        if (rm_data.length > 0){
            running_mean_data.push(rm_data);
        }
    }
    return running_mean_data
}

function compute_average(data){
    var sum=0, ave= null; var count = 0;
    for (var idx = 0;idx<data.length;idx++){
        d = data[idx][1];
        if (String(d) != '-9999' && d != null){
            try {
                sum+= parseFloat(d);
                count+=1;
            }
            catch(e){}
        }
    }
    if (count > 0){
        ave = sum / parseFloat(count);
    }
    return [[data[0][0], ave], [data[data.length -1][0], ave]]
}

function compute_range(data){
    var d,dt = [],mx = null, mn = null;
    for (var idx = 0;idx<data.length;idx++){
        d = data[idx][1];
        if (String(d) != '-9999' && d != null){
            dt.push(d);
        }
    }
    if (dt.length > 0){
        var mn = Math.min.apply(Math,dt);
        var mx = Math.max.apply(Math,dt);
    }
    return [[data[0][0], mn, mx], [data[data.length -1][0], mn, mx]]
}


function compute_running_mean_old(data, running_mean_points, chart_type){
    var running_mean_data = [];
    if (running_mean_points%2 == 0){
        var num_nulls =running_mean_points/2 - 1;
    }
    else{
        var num_nulls =(running_mean_points - 1)/2;
    }
    for (var idx=0;idx<data.length;idx++) {
        var skip = 'F';
        if (idx >= num_nulls &&  idx <= data.length - 1 - num_nulls) {
            var cnt = 0;
            for(var i=idx - num_nulls,sum=0;i<=idx + num_nulls;i++){
                if (chart_type == 'column'){
                    var val = data[i];
                }
                else {
                    var val = data[i][1];
                }
                if (val != null){
                    sum+=val;
                    cnt+=1;
                }
                else{
                    skip = 'T';
                    break;
                }
            }
            if (cnt > 0 && skip =='F'){
                if (chart_type == 'column'){
                    running_mean_data.push(precise_round(sum/cnt,2));
                }
                else {
                    running_mean_data.push([data[idx][0],precise_round(sum/cnt,2)]);
                }
            }
            /*
            else{
                if (chart_type == 'column'){
                    running_mean_data.push(null);
                }
                else {
                    running_mean_data.push([data[idx][0],null]);
                }
            }
            */
        }
        /*
        else{
            if (chart_type == 'column'){
                running_mean_data.push(null);
            }
            else {
                running_mean_data.push([data[idx][0],null]);
            }
        }
        */
    }
    return running_mean_data
}


function set_plot_data(data, dates_true, miss_val,chart_type) {
    /*
    Converts data to barchart data
    Data is  a list of entries of form [x_val, y_val]
    if dates_true = true, we convert xcats to Date objects
    */
    results = {
        'x_cats':[],
        'data':[],
        'data_max':-9999.0,
        'data_min':9999.0
    };
    for (var date_idx=0;date_idx< data.length;date_idx++) {
        try {
            var y_val = parseFloat(data[date_idx][1]);
        }
        catch (e) {
            try {
                var y_val = parseFloat(miss_val);
            }
            catch(e) {
                var y_val = null
            }
        }
        //Convert dates if needed
        if (dates_true){
            var date = data[date_idx][0].replace('-','').replace('-','');
            try {
                var year = parseInt(date.slice(0,4));
                var month = parseInt(date.slice(4,6)) - 1;
                var day = parseInt(date.slice(6,8));
            }
            catch (e) {
                var year = 9999;
                var month = 0;
                var day = 1;
            }
            var x_val = Date.UTC(year, month, day);
        }
        else {
            var x_val = data[date_idx][0];
        }
        results.x_cats.push(data[date_idx][0]);
        if (y_val == null){
            if (chart_type == 'column') {
                results.data.push(null);
            }
            else {
                results.data.push([x_val,null]);
            }
            continue;
        }
        
        if (Math.abs(y_val - parseFloat(miss_val)) < 0.0001){
            if (chart_type == 'column') {
                results.data.push(null);
            }
            else {
                results.data.push([x_val,null]);
            }
        }
        else {
            if (chart_type == 'column') {
                results.data.push(y_val);
            }
            else {
                results.data.push([x_val, y_val]);
            }
            if (y_val > results.data_max){
                results.data_max = y_val;
            }
            if (y_val < results.data_min){
                results.data_min = y_val;
            }
        }
    }
    return results;
}

function isPrime (n){
    if (n < 2) return false;
    /**
     * An integer is prime if it is not divisible 
     by any prime less than or equal to its square root
    **/
    var q = parseInt(Math.sqrt (n));

    for (var i = 2; i <= q; i++){
        if (n % i == 0){
            return false;
        }
    }
    return true;
}


function find_max(vals,variable,statistic){
    var max = null;
    try{
        max = Math.max.apply(Math,vals);
    }
    catch(e){}
    if (statistic == 'ndays'){
        max = 35;
    }
    return max;
}

function find_min(vals, variable,statistic, dep_from_ave){
    var min = null;
    if ((variable == 'snow' || variable == 'snwd' || variable == 'pcpn' || variable == 'evap' || variable == 'wdmv') && (statistic !='ndays' && statistic !='sd' && dep_from_ave=='F')) {
        min = 0.0;
    }
    else{
        try{
            min = Math.min.apply(Math,vals);
        }
        catch(e){}
    }
    return min;
}
function find_smallest_divisor(n){
    //smallest divisor of n
    var div;
    if (isPrime(n)){
         div = n;
    }
    else{
        var flag = true,
        div = 3;
        while (flag){
            if (n % div == 0){
                flag = false;
            }
            div=div+1;
        }
    }
    return div
}

function find_largest_divisor(n){
    //Largest divisor of n
    var div;
    if (isPrime(n)){
         div = n;
    }
    else{
        var flag = true,
        div = n - 1;
        while (flag){
            if (n % div == 0){
                flag = false;
            }
            div=div - 1;
        }
    }
    return div
}

function find_closest_smaller(num, divisor){
    //Given num, this routine finds the closets smaller integer divisible by divisor
    var fl = Math.floor(num);
    var closest = null;
    while (closest == null ){
        if (fl % divisor == 0){
            closest =  fl;
        }
        else{
            fl = fl - 1;
        }
    }
    return closest;
}

function find_closest_larger(num, divisor){
    //Given num, this routine finds the closets larger integer divisible by divisor
    var cl = Math.ceil(num);
    var closest = null;
    while (closest == null ){
        if (cl % divisor == 0){
            closest =  cl;
        }
        else{
            cl = cl + 1;
        }
    }
    return closest;
}

function compute_statistic(vals, summary){
    /*
    Computes summary over vals
    vals must be non-empty array
    */
    if (!vals.length){
        return null;
    }

    if (summary == 'max'){
        return Math.max.apply(Math,vals);
    }
    else if (summary == 'min'){
        return precise_round(Math.min.apply(Math,vals),2);
    }
    else if (summary == 'sum'){
        for(var i=0,sum=0;i<vals.length;sum+=vals[i++]);
        return precise_round(sum,2);
    }
    else if (summary == 'mean'){
        for(var i=0,sum=0;i<vals.length;sum+=vals[i++]);
        return precise_round(sum/vals.length,2);
    }
    else {
        return null;
    }
}

function set_data_summary_series(date, vals, summary, chart_type){
    results =[]; 
    if (vals.length > 0) {
        var value = compute_statistic(vals, summary);
        if (chart_type == 'column'){
            results = value;
        }
        else {
            results = [date, value];
        } 
    }
    else {
        if (chart_type == 'column'){
            results = null;
        }
        else {
            results = [date, null];
        } 
    } 
    return results
}

//GRAPHIC UTILS
function set_style(color, fontSize, fontWeight, align) {
    var style = {
        color: color,
        fontSize:fontSize,
        fontWeight:fontWeight,
        align:align
    };
    return style;
}

function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}
function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}
function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}
//SODSUMM FUNCTIONS
function set_y_axis_properties(data_max,vertical_axis_max, data_min, vertical_axis_min, variable,statistic, dep_from_ave,plotline_no){
    var props = {
        'axisMin':data_min,
        'axisMax':data_max,
        'tickInterval':null,
        'plotLines':[]
    };
    if (!plotline_no || data_max == null || data_min == null){
        return props;
    }
    if (Math.abs(data_max)<0.00001 && Math.abs(data_min)<0.00001){
        props.axisMin = -1.0;
        props.axisMax = 1.0;
        props.tickInterval = 0.5;
        return props; 
    }
    //Override data_min if necessary
    if ((variable == 'snow' || variable == 'snwd' || variable == 'pcpn') && 
    (statistic !='ndays' && statistic !='sd' && dep_from_ave=='F')) {
        props.axisMin = 0.0;
    }

    if (statistic == 'ndays'){
        props.axisMax = 32;
    }
    var diff = Math.abs(props.axisMax - props.axisMin);
    //Deal with small differences
    steps = [0,plotline_no / 100, plotline_no / 50, plotline_no / 25,plotline_no / 10, plotline_no / 5, plotline_no / 2];
    for (idx=0;idx<=steps.length - 2 ;idx+=1){
        if (steps[idx] <= diff  && diff < steps[idx+1]){
            props.axisMin = Math.floor(props.axisMin);
            var upper = steps[idx+1];
            props.tickInterval = upper / plotline_no;
            //Make sure upper is close to max value
            while (upper - props.axisMax > props.tickInterval){
                if (upper < props.axisMax){
                    break
                }
                upper = precise_round(upper - props.tickInterval,2);
            }
            props.axisMax = props.axisMin + upper;
            break
        }
    }
    //Sanity check
    if (props.axisMax < data_max){
        props.axisMax = data_max;
    }

    //Larger  differences are treated differently
    if (plotline_no / 2 < diff && diff <=plotline_no){
        props.axisMin = Math.floor(props.axisMin);
        var upper = Math.ceil(props.axisMax) + 1;
        props.axisMax = upper;
        props.tickInterval = 1.0;
        
    }
    if (plotline_no < diff){
        props.axisMin = find_closest_smaller(props.axisMin,plotline_no);
        var upper = find_closest_larger(diff,plotline_no);
        props.axisMax = props.axisMin + upper;
        props.tickInterval = (props.axisMax - props.axisMin) / plotline_no;
        //Re-adjust upper is needed
        while (props.axisMin + upper - data_max < 0){
            upper = upper + props.tickInterval;
        }
        while (Math.abs(props.axisMin + upper - data_max) > props.tickInterval){
            upper = upper - props.tickInterval;
        }
        while (data_min - props.axisMin > props.tickInterval){
            props.axisMin = props.axisMin + props.tickInterval;
        }
        props.axisMax = props.axisMin + upper;
    }
    //Sanity check
    while (Math.abs(data_max) > Math.abs(props.axisMax)){
        props.axisMax+=props.tickInterval;
    }
    //Override max/min custom requested by user
    var add_top = 0;
    if (vertical_axis_max != "Use default") {
        try{
            props.axisMax = parseFloat(vertical_axis_max);
            add_top = 1;
        }   
        catch(e){}
    }
    if (vertical_axis_min != "Use default") {            
        try{
            props.axisMin = parseFloat(vertical_axis_min);
        }
        catch(e){}
    }
    if (statistic == 'ndays'){
        props.axisMax = 31;
    }
    //plotlines
    var plotLine = {
        color:'#787878',
        dashStyle:'dash',
        width: 0.5
    }
    //if (add_top == 0 && props.axisMax < 1){add_top = 1;}
    for (val=props.axisMin;parseInt(100*val)<=parseInt(100*(props.axisMax + add_top*props.tickInterval));val+=props.tickInterval) {
        var pL = {};
        for (var key in plotLine){
            pL[key] = plotLine[key];
        }
        //rounding
        var intRegex = /^\d+$/;
        if (0 <= props.tickInterval && props.tickInterval < 0.1 ){
            var v = precise_round(val,2);
        }
        else if (0.1 <= props.tickInterval && !intRegex.test(val)){
            var v = precise_round(val,1);
        }
        else{
            var v = val;
        }
        /*
        if (0 <= val && val < 0.1 ){
            var v = precise_round(val,2);
        }
        else if (0.1 <= val && !intRegex.test(val)){
            var v = precise_round(val,1);
        }
        else{
            var v = val;
        }
        */
        if (v > props.axisMax && vertical_axis_max != "Use default"){
            try{
                v = parseFloat(vertical_axis_max);
            }
            catch(e){}
            //continue;
        }
        pL.value = v;
        props.plotLines.push(pL);
    }
    return props;
}
