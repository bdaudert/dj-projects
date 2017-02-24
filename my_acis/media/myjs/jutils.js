String.prototype.rsplit = function(sep, maxsplit) {
    //js equivalent to python rspilt
    var split = this.split(sep);
    return maxsplit ? [ split.slice(0, -maxsplit).join(sep) ].concat(split.slice(-maxsplit)) : split;
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
    geocoder.geocode( { 'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
           window.map.setCenter(results[0].geometry.location);
           window.map.setZoom(7);
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

function poll(url_str) {
    show_loading()
    $.ajax({
        url:url_str, 
        success: function(data){
            window.open(url_str);
        },
        dataType: "json"
    });
    setTimeout(poll(url_str), 5000);
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

function ShowPopupDocu(DivId){
    //Close all dialogs that happen to be open
    $(':ui-dialog').each(function(){
        if ($(this).dialog('isOpen')){
            $(this).dialog('destroy');
        }
    });
    try {
        var bootstrapButton = $.fn.button.noConflict();
        $.fn.bootstrapBtn = bootstrapButton;
    }catch(e){};
    var wWidth = $(window).width();
    var max_height = $(window).height()*0.6, 
        max_width = wWidth * 0.6;
    if (DivId.inList(['formDownload','largeRequestForm'])){
        var max_width = wWidth * 0.3;
    }
    //Open the dialog
    $( '#' + DivId ).dialog({
        position:{
            my:'center',
            at:'center',
            of:window
        },
        title:'You can move and resize me!',
        resizable: true,
        modal: false,
        width:'auto',
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
    if ($(this).css('display') == 'none'){
        $(this).css('display','block');
    }
    else{
        $(this).css('display','none');
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
