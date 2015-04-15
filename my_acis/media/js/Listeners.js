$(function(){
    /*
    ELEMENT CHANGE
    */
    $('#element').on('change', function(){
        //Set monthly statistic for monann
        var sum_els = ['pcpn','snwd','snow','gdd','hdd','cdd','evap','pet'];
        if ($(this).val().inList(sum_els)){
            if ($('#monthly_statistic').length){
                $('#monthly_statistic').val('msum');
            }
        }
        else {
            if ($('#monthly_statistic').length){
                $('#monthly_statistic').val('mave');    
            }
        }
    });

    /*
    FORMS
    Hide results and errors on form change
    Also hide plot options if they exits
    */
    $('#tableDataForm, #tableMapForm').on('change keyup', function(){
        hide_errors_results_on_change($(this).attr('id'));
        //If graph options extist, hide them
        if ($('.formGraph')[0]){
            showHideTableRowClass('formGraph', 'hide');
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
        //Set area form field
        if ( $('#area_type').val() == 'location' ||  $('#area_type').val() == 'station_id'){
            set_area('area',this); //form_utils function
        }
        //set map
        set_map(this); //form_utils function
        update_value($(this).val()); //form_utils function

        var station_only_els = ['obst','snow','snwd','evap','wdmv'];
        var non_prism_els = ['gdd','hdd','cdd'];
        //Set grid form fields
        if (data_type == 'grid' || data_type == 'location' || data_type == 'locations'){
            if ($('#elements').length){
                var opts = $("#elements option");
            }
            if ($('#element').length){
                var opts = $("#element option")
            } 
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
            if ($('#start_year').length && $('#end_year').length){
                if ($('#start_year').val() == 'POR'){
                    $('#start_year').val('1970');
                }
                if ($('#end_year').val() == 'POR'){
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
    $('#monthly_statistic').on('change', function(){
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
    $('.area_type').on('change', function(){
       //Set area form field
      set_area('area',this); //form_utils function
      //set map
      set_map(this); //form_utils function
      update_value($(this).val()); //form_utils function
    });
   

    /*
    Update maps on area form field change
    i.e. move marker or pan in on new location
    */
    $('.area_type').on('change', function(){
        update_maps($(this));
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
    $('#show_range, #show_running_mean').on('click', function(){
        //Find the correct chart
        var l_type = $(this).val();
        for(var i = myChart.series.length - 1; i > -1; i--){
            if (myChart.series[i].options.id.split('_')[0] == l_type){
                if ($(this).is( ":checked" )){
                    myChart.series[i].setVisible(true, true);
                    //myChart.series[i].show();
                }
                else{
                    myChart.series[i].setVisible(false, false);
                    //myChart.series[i].hide();
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

});


