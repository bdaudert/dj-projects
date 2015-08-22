$(document).ready(function ($) { 
//$(function(){
    /*
    BACKBUTTON ISSUE
    ***** ADDRESSED IN templates/csc_base.html, 
          only affects the select elements of forms
    /*
    * GREYBOX PUPUPS from GRANT
    */
    $(".popup_map").click(function(ev){ 
        // Let alt-clicks and non-left clicks (which != 1) do their thing
        if ( ev.shiftKey || ev.ctrlKey || ev.altKey || ev.metaKey || ev.which != 1 ) {
            return true;
        }
        var url = this.getAttribute("href");
        var title = $(this).text();
        var width = 792 + 20;
        var height = 700 + 40;
        GB_show(title, url, height, width);
        return false;
    });
    /*
    ELEMENT CHANGE
    */
    $('#element').on('change', function(){
        //Set monthly statistic for monann
        var sum_els = ['pcpn','snwd','snow','gdd','hdd','cdd','evap','pet'];
        if ($(this).val().inList(sum_els)){
            if ($('#statistic').length){
                $('#statistic').val('msum');
            }
        }
        else {
            if ($('#statistic').length){
                $('#statistic').val('mave');    
            }
        }
    });

    /*
    DATES
    */
    $('.year').on('change', function(){
        var which = $(this).attr('id');
        var s_yr_int, e_yr_int;
        s_yr_int = parseInt($('#start_year').val());
        e_yr_int = parseInt($('#end_year').val());
        if (s_yr_int - e_yr_int < 0){
            if (which == 'start_year'){
                try{
                    $('#end_year').val(String(s_yr_int + 10));
                }
                catch(e){
                    $('#end_year').val(String(s_yr_int));
                }
            }
            if (which == 'end_year'){
                try{
                    $('#start_year').val(String(e_yr_int - 10));
                }
                catch(e){
                    $('#start_year').val(String(e_yr_int));
                }
            } 
        }
    });
    $('.month').on('change', function(){
        mon_lens = [31,28,31,30,31,30,31,31,30,31,30,31];
        mon_names = ['January','February','March','April',
            'May','June','July','August','September','October','November','December'];
        var which = $(this).attr('id');
        //Adjust days 
        var mon_int = parseInt($(this).val());
        if (which == 'start_month'){
            $('#start_day > option').remove();
            for (day=1; day<=mon_lens[mon_int -1]; day++) {
                var option = '<option value="' + String(day) + '">' + String(day); 
                /*
                if (day == 1){
                    option+= ' selected';
                }
                */
                option+='</option>';
                $('#start_day').append(option);
            }
            $('#start_day').val(1)
        }
        if (which == 'end_month'){
            $('#end_day > option').remove();                                  
            for (day=1; day<=mon_lens[mon_int -1]; day++) {
                var option = '<option value="' + String(day) + '">' + String(day);   
                /*
                if (day == mon_lens[mon_int -1]){
                    option+= ' selected';
                }
                */
                option+='</option>';
                $('#end_day').append(option);
            }
            $('#end_day').val(mon_lens[mon_int -1])
        }
        //Make sure start/end period are forming consistent time line
        var s_month_int = parseInt($('#start_month').val());
        var e_month_int = parseInt($('#end_month').val());
        var s_day_int = parseInt($('#start_day').val());
        var e_day_int = parseInt($('#end_day').val());
        if ( which == 'start_month' && s_month_int - e_month_int < 0){
            $('#end_month').val(String(s_month_int));
        }
        if (which == 'end_month' && s_month_int - e_month_int < 0){
            $('#start_month').val(String(s_month_int));
        } 
        //Chech the days
        if ( which == 'start_month'){
            mon_len = mon_lens[s_month_int -1];
            if (s_day_int > mon_len){
                $('#start_day').val(String(mon_len));
            }
        }
        if ( which == 'end_month'){
            mon_len = mon_lens[s_month_int -1];
            if (s_day_int > mon_len){
                $('#end_day').val(String(mon_len));
            }
        }

    });

    $('.day').on('change', function(){
        var which = $(this).attr('id');
        var s_day_int = parseInt($('#start_day').val());
        var e_day_int = parseInt($('#end_day').val());
        if (s_day_int - e_day_int < 0){
            try{
                $('#end_day').val(String(s_day_int + 1))
            }
            catch(e){
                $('#start_day').val(String(e_day_int - 1))
            }
        }

    });
    /*
    FORMS
    Hide results and errors on form change
    Also hide plot options if they exits
    */
    /*
    $('#tableDataForm, #tableMapForm').on('change keyup', function(){
    //$('#tableDataForm, #tableMapForm').change(function(){
        hide_errors_results_on_change($(this).attr('id'));
        //If graph options extist, hide them
        if ($('.formGraph')[0]){
            showHideTableRowClass('formGraph', 'hide');
        }
    });
    */
    $('#tableDataForm, #tableMapForm').on('change', 'input, select, textarea', function(){
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
    
    /*
    PLOTS
    */    
    $('#plot_opts_button').on('click', function(){
        if ($('.plOpts:first').css('display') == 'none'){ 
            $('.plOpts').css('display','table-row');
            
        }
        else {   
            $('.plOpts').css('display','none');
        }
    });

    /*
    STATION FINDER DOWNLOAD BUTTON
    on click a second form pops up asking for user email, 
    and additional data download options 
    */
    $('.obtain_sf_data').on('click', function(){
        $("#data_format").children('option[value="html"]').attr('disabled', true)
        ShowPopupDocu('formDownload');
        
    });
    
    /*
    GRID 
    changes start/end data 
    and sets temp resolution for prism data
    */
    $('#grid').on('change keyup', function(){
        if ($(this).val() == '21'){
            if ($('#temp_res').length){
                $('#temp_res').css('display','table-row');
            }
            //Hide special degree day options
            $('#add').css('display','none');
            $('#dd').css('display','none');
        }
        else {
            if ($('#temp_res').length){
                $('#temp_res').css('display','none');
            }
        }
        //Disable elements if prism
        var non_prism_els = ['gdd','hdd','cdd'];
        var station_only_els = ['obst','snow','snwd','evap','wdmv'];
        $("#elements option").each(function(){
            //Check if prism data, disable degree days
            if ($('#grid').val() == '21' && $(this).val().inList(non_prism_els)){
                $(this).attr('disabled',true);
            }
            else{
                if ($(this).val().inList(station_only_els)){
                    $(this).attr('disabled',true);
                }
            }
        });
        var new_dates, ds, de;
        //Change start/end dates/years according to grid
        if ($('#start_year').length && $('#end_year').length){
            ds = $('#start_year').val() + '-01-01';
            de = String(parseInt($('#end_year').val()) - 1) + '-12-31';
            new_dates = set_dates_for_grid($('#grid').val(),ds, de, 'year');
            $('#start_year').val(new_dates.start);
            $('#end_year').val(new_dates.end);
        }
        if ($('#start_date').length && $('#end_date').length){
            ds = $('#start_date').val();
            de = $('#end_date').val()
            new_dates = set_dates_for_grid($('#grid').val(), ds, de, 'dates');
            $('#start_date').val(new_dates.start);
            $('#end_date').val(new_dates.end); 
        }
        //Change start/end years for interannual
        if ($('#app_name').val() == 'single_interannual'){
            set_year_range_for_interannual()
        }
    });
    /*
    GRID 
    temporal resolution 
    (PRISM has monthly/yearly as well as daily)
    */
    $('#temporal_resolution').on('change', function(){
        set_dates_for_grid($('#grid').val(), $('#start_date').val(), $('#end_date').val(), 'dates');
    });

    /*
    DATA TYPE
    Sets form fields according to data_type (station/grid)
    Affected form fields are
    elements
    grid
    */
    $('.data_type').on('change keyup', function(){
        var data_type = $(this).val();
        //Needed for single lister
        $('#data_type').val(data_type);
        //Hide station finder link
        if ($('#stn_finder').length ){
            if (data_type == 'grid' || $(this).val() == "location"){
                $('#stn_finder').css('display','none');
            }
            else{
                $('#stn_finder').css('display','table-row'); 
            }
        }
        /*
        //Set area form field
        if ( $('#area_type').val() == 'location' ||  $('#area_type').val() == 'station_id'){
            set_area('area',$(this)); //form_utils function
        }
        */
        update_value($(this).val()); //form_utils function

        var station_only_els = ['obst','snow','snwd','evap','wdmv'];
        var non_prism_els = ['gdd','hdd','cdd'];
        //Set grid form fields
        var opts = null;
        if (data_type == 'grid' || data_type == 'location' || data_type == 'locations'){
            //Disable station_ids option
            $('#area_type option[value="station_ids"]').attr('disabled',true);
            if ($('#elements').length){
                var opts = $("#elements option");
            }
            if ($('#element').length){
                var opts = $("#element option")
            } 
            if (opts){
                opts.each(function(){
                    //Disable station elements
                    if ($(this).val().inList(station_only_els)){
                        $(this).attr('disabled',true);
                    }
                    //Check if prism data, disable degree days
                    if ($('#grid').val() == '21' && $(this).val().inList(non_prism_els)){
                        $(this).attr('disabled',true);
                    }
                });
            }
            //If prism hide special degree days
            if ($('#grid').val() == '21'){
                $('#add').css('display','none');
                $('#dd').css('display','none');
            }
            else {
                $('#add').css('display','table-row');
            }
            //Hide flags/obs time
            $('#flags').css('display','none');
            $('#obs_time').css('display','none')
            //Show grid
            $('#grid_type').css('display','table-row');
            //Change POR to date or vice versa
            if ($('#start_year').length){
                if ($('#start_year').val().toUpperCase() == 'POR'){
                    $('#start_year').val('1970');
                }
            }
            if ($('#end_year').length){
                if ($('#end_year').val().toUpperCase() == 'POR'){
                    $('#end_year').val('2000');
                }
            }
            //Disable snow from climatology summary type
            if ($('#summary_type').length){
                $('#summary_type option[value="all"]').attr('disabled',true);
                $('#summary_type option[value="prsn"]').attr('disabled',true);
                $('#summary_type option[value="both"]').attr('disabled',true);
                $('#summary_type option[value="temp"]').attr('selected',true);
            }

        }
        //Set station form fields
        if (data_type == 'station' || data_type == 'station_id' || data_type == 'station_ids'){
            //Enable station_ids option
            $('#area_type option[value="station_ids"]').attr('disabled',false); 
            //Show add degree day option    
            $('#add').css('display','table-row');
            $("#elements option").each(function(){
                //Enable all elements
                $(this).attr('disabled',false);
            });
            //Hide flags/obs time
            $('#flags').css('display','table-row');
            //$('#obs_time').css('display','table-row')
            //Show grid
            $('#grid_type').css('display','none');
            //Enable snow from climatology summary type
            if ($('#summary_type').length){
                $('#summary_type option[value="all"]').attr('disabled',false);
                $('#summary_type option[value="prsn"]').attr('disabled',false);
                $('#summary_type option[value="both"]').attr('disabled',false);
                $('#summary_type option[value="all"]').attr('selected',true);
            }            
        } 
    });

    /*
    MONANN LISTENERS
    */
    $('img#show_hide_graph, img#show_hide_summary, img#show_hide_data').on('click', function(){
        var id = $(this).attr('id');
        if (id == 'show_hide_graph'){
            if ($('#user_graph').css('display') == 'none'){
                $('#user_graph').css('display', 'block');
                $('#printable_table').css('display', 'none');
                $('#data_summary').css('display', 'none');
            }
            else{
                $('#user_graph').css('display', 'none');
            }
        }
        if (id == 'show_hide_summary'){
            if ($('#data_summary').css('display') == 'none'){
                $('#user_graph').css('display', 'none');
                $('#printable_table').css('display', 'none');
                $('#data_summary').css('display', 'block');
            }
            else{
                $('#data_summary').css('display', 'none');
            }
        }
        if (id == 'show_hide_data'){
            if ($('#printable_table').css('display') == 'none'){
                $('#user_graph').css('display', 'none');
                $('#printable_table').css('display', 'block');
                $('#data_summary').css('display', 'none');
            }
            else{
                if ($('#user_graph').css('display') == 'none') {
                    $('#printable_table').css('display', 'none');
                }
                else {
                    $('#printable_table').css('display', 'block');
                    $('#user_graph').css('display', 'none');
                }
            }
        }
    });
    /*
    MONANN THRESHOLDS FOR NDAYS
    */
    //lean up needed
    $('#element').on('change', function(){
        set_BaseTemp($(this).val());
        var lgb = '';
        if ( $('#less_greater_or_between').length){
            var threshes = set_threshes($(this).val()).split(',');
            lgb = $('#less_greater_or_between').val();
        }
        if (lgb == 'b'){ 
            $('#threshold_low_for_between').val(threshes[2]);
            $('#threshold_high_for_between').val(threshes[3]);
        }
        if (lgb == 'l'){ $('#threshold_for_less_than').val(threshes[0]);}
        if (lgb == 'g'){$('#threshold_for_less_than').val(threshes[1]);}
    });
    $('#statistic').on('change', function(){
        if ($(this).val() == 'ndays'){ 
            $('#threshold_type').css('display','table-row');
            var lgb = $('#less_greater_or_between').val();
            if (lgb == 'b'){$('#threshold_between').css('display','table-row');}
            if (lgb == 'l'){$('#threshold_below').css('display','table-row');}
            if (lgb == 'g'){$('#threshold_above').css('display','table-row');}
        }
        else{
            $('#threshold_between').css('display','none');
            $('#threshold_below').css('display','none');
            $('#threshold_above').css('display','none');
        }
    });
    $('#less_greater_or_between').on('change', function(){
        var threshes = set_threshes($('#element').val()).split(',');
        var lgb = $(this).val();
        if (lgb == 'b'){ 
            $('#threshold_low_for_between').val(threshes[2]);
            $('#threshold_high_for_between').val(threshes[3]);
            $('#threshold_between').css('display','table-row');
            $('#threshold_below').css('display','none');
            $('#threshold_above').css('display','none');
        }   
        if (lgb == 'l'){ 
            $('#threshold_for_less_than').val(threshes[0]);
            $('#threshold_below').css('display','table-row');
            $('#threshold_between').css('display','none');
            $('#threshold_above').css('display','none');
        }
        if (lgb == 'g'){
            $('#threshold_for_greater_than').val(threshes[1]);
            $('#threshold_above').css('display','table-row');
            $('#threshold_between').css('display','none');
            $('#threshold_below').css('display','none');
        }
        
    });


    /* *******************
       MAPS
    ********************** */
    /*
    AREA TYPE 
    Sets maps and area form field
    depending on area type
    */
    $('.area_type').on('keydown change', function(){
        //Set area form field
        set_area('area',$(this)); //form_utils function
        //set map
        set_map($(this)); //form_utils function
        update_value($(this).val()); //form_utils function
        //Change start/end years for interannual
        if ($('#app_name').val() == 'single_interannual'){
            set_year_range_for_interannual()
        }
     
    });
   

    /*
    DYNAMIC HIGHCHARTS
    */
    $('#chart_type').on('change keyup', function(){
        var chartType = $('#chart_type').val();
        for (var i = 0; i < myChart.series.length; i++) {
            //Check if series is main/average or runmean
            var c_type = myChart.series[i].options.id.split('_')[0];
            if (c_type == 'main'){
                myChart.series[i].update({type:chartType});
            }
        }
    });
    $('#show_range, #show_running_mean, #show_average, #climatology, #percentile_5, #percentile_10, #percentile_25').on('click', function(){
        //Find the correct chart
        var l_type = $(this).val();
        for(var i = myChart.series.length - 1; i > -1; i--){
            if (myChart.series[i].options.id.split('_')[0] == l_type){
                if ($(this).is( ":checked" )){
                    myChart.series[i].setVisible(true, true);
                    myChart.series[i].update({showInLegend: true});
                }
                else{
                    myChart.series[i].setVisible(false, false);
                    myChart.series[i].update({showInLegend: false});
                }
                myChart.redraw();
            }
        }
    });

    $('#running_mean_period').on('change keyup', function(){
        var running_mean_period = $(this).val();
        var rm_data = null, s_id = null, s_name = '';
        for (var i = 0; i < myChart.series.length; i++) {
            //Check if series is main/average or runmean
            var c_type = myChart.series[i].options.id.split('_')[0];
            if (c_type == 'main'){
                //Chart series.data is an object, need to pick the correct x,y values
                var s_data = [];
                for (var j = 0; j < myChart.series[i].data.length; j++) {
                    s_data.push([myChart.series[i].data[j].x,myChart.series[i].data[j].y])
                }
                s_id = myChart.series[i].options.id.split('_')[1];
                s_name = myChart.series[i].options.name;
                rm_data = compute_running_mean(s_data, running_mean_period);
            }
            if (c_type == 'runmean' &&  myChart.series[i].options.id == 'runmean_' + s_id  && rm_data != null){
                var r_name = running_mean_period + '-';
                if ($('#running_mean_days').length){
                    r_name+='day Running Mean ' + s_name;
                }
                if ($('#running_mean_years').length){
                    r_name+='year Running Mean ' + s_name
                }
                myChart.series[i].update({data: rm_data, name:r_name });

                //myChart.series[i].data = rm_data;
                myChart.redraw();
                rm_data = null;
                s_id = null;
            }
        }
    });
    //$('input[name="chart_selector"], select[name="chart_selector"]').on('change', function(event){
     $('#data_indices, #chart_summary').on('change keyup', function(){
        smry = 'individual';
        if ($('#chart_summary').length) {
            smry = $('#chart_summary').val();
        }
        if (smry == 'individual'){
            generateTS_individual()
        }
        else{
            generateTS_smry();
        }   
    });

    //Threshold for interannual
    $('#threshold').on('change keyup', function(){
        var thresh = $(this).val();
        for (var i = 0; i < myChart.series.length; i++) {
            //Only change main series, not aves and runmeans
            var c_type = myChart.series[i].options.id.split('_')[0];
            if(c_type == 'main'){
                myChart.series[i].update({
                    threshold: thresh,
                    color:'blue',
                    negativeColor:'red'
                });
                myChart.redraw(true);
            }
        } 
    });

   $('#target_year_figure').on('change', function(){
        var year = $(this).val();
        //Clear old tab data
        var data_table = $('#textData');
        $('#textData tr').remove();
        var x_min, x_max;
        var p_indices = [], c_indices = [];
        for (var i = 0; i < myChart.series.length; i++) {
            var series_id = myChart.series[i].options.id;
            var series_type = series_id.split('_')[0];
            if (series_type == 'main'){
                var idx = series_id.split('_')[1];
                var s_year = parseInt($('#start_year')) + idx
                if (s_year != year){
                    //Hide series
                    myChart.series[i].setVisible(false,false);
                    myChart.series[i].update({showInLegend: false});
                }
                if (s_year == year){
                    //Show series
                    myChart.series[i].setVisible(true,true);
                    //get x-axis max, min
                    try{
                        x_min = myChart.series[i].options.data[0][0];
                        x_max = myChart.series[i].options.data[myChart.series[i].options.data.length -1][0];
                    }
                    catch(e){}
                    
                    myChart.series[i].update({showInLegend: true});
                    //Show data in data tab
                    for (var j=0; j< myChart.series[i].data.length;j++){
                         date_int = series.data[j].x;
                        //Convert integer time to date string
                        var d = new Date(date_int + 1000*60*60*24);
                        var day = ("0" + d.getDate()).slice(-2);
                        var mon = ("0" + (d.getMonth() + 1)).slice(-2);
                        var year = d.getFullYear();
                        date_str = year + '-' + mon + '-' + day + ' ' + hr;
                        try{
                            val = parseFloat(series.data[j].y).toFixed(4);
                        }
                        catch(e){
                            val = series.data[j].y;
                        }
                        if(typeof val !== "undefined") {
                            var row = $('<tr></tr>').appendTo(data_table);
                            $('<td></td>').text(date_string).appendTo(row);
                            $('<td></td>').text(String(val)).appendTo(row);
                        }
                    }
                }
            }

            //Get climo and percentile indices
            if (series_type == 'climatology'){
                c_indices.push(i)
            }
            if (series_type == 'percentile'){
                p_indices.push(i)
            }
        }
        //Update climo and perentile data to
        //match the new x_axis
        //CLIMO
        for (var i = 0; i < c_indices.length; i++) {
            new_data = [];
            var series_id = myChart.series[c_indices[i]].options.id;
            if (x_min === null){
                myChart.series[c_indices[i]].setVisible(false,false);
                myChart.series[c_indices[i]].update({showInLegend: false});
            }
            else{
                for (var d_idx = 0;d_idx<myChart.series[c_indices[i]].options.data.length;d_idx++){
                    var date = x_min + d_idx * (24 * 60 * 60 * 1000);
                    new_data.push([date, myChart.series[c_indices[i]].options.data[d_idx][1]])
                }
                myChart.series[c_indices[i]].update({data:new_data});
                if ($('#climatology').is(':checked')) {
                    myChart.series[c_indices[i]].setVisible(true,true);
                    myChart.series[c_indices[i]].update({showInLegend: true});
                }
                else{
                    myChart.series[c_indices[i]].setVisible(false,false);
                    myChart.series[c_indices[i]].update({showInLegend: false});
                }
            } 
        }
        //PERCENTILES
        for (var i = 0; i < p_indices.length; i++) {
            new_data = [];
            var series_id = myChart.series[p_indices[i]].options.id;
            var varnum = series_id.split('_')[2];
            if (x_min === null){
                myChart.series[p_indices[i]].setVisible(false,false);
                myChart.series[p_indices[i]].update({showInLegend: false});
            }
            else{
                for (var d_idx = 0;d_idx<myChart.series[p_indices[i]].options.data.length;d_idx++){
                    var date = x_min + d_idx * (24 * 60 * 60 * 1000);
                    new_data.push([date, myChart.series[p_indices[i]].options.data[d_idx][1],  myChart.series[p_indices[i]].options.data[d_idx][2]])
                }
                myChart.series[p_indices[i]].update({data:new_data});
                var series_id = myChart.series[p_indices[i]].options.id;
                var p = series_id.split('_')[1];
                if ($('#percentile_' + p).is(':checked')){
                    myChart.series[p_indices[i]].setVisible(true,true);
                    myChart.series[p_indices[i]].update({showInLegend: true});
                }
                else{
                    myChart.series[p_indices[i]].setVisible(false,false);
                    myChart.series[p_indices[i]].update({showInLegend: false});
                }
            }
        }
        
        myChart.redraw();
    });


    //MAPS
    $('#station_list').on('click', 'tr', function(){
        infowindow.close();
        infowindow.setContent($(this).attr('cString'));
        infowindow.open(window.map, window.markers[$(this).attr('id')]);
        var bounds = window.map.getBounds();
        bounds.extend(new google.maps.LatLng($(this).attr('lat'), $(this).attr('lon')));
    }); 
    $('#station_list').on('mouseover', 'tr', function(){
        $(this).css('backgroundColor', "#8FBC8F");
    });
    $('#station_list').on('mouseout', 'tr', function(){
         $(this).css('backgroundColor',"#FFEFD5");
    });

});
