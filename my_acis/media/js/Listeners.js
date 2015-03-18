$(function(){
    /*
    Hide results and errors on form change
    Also hide plot options if they exits
    */
    $('#tableDataForm').on('change keyup', function(){
        hide_errors_results_on_change('tableDataForm');
        //If graph options extist, hide them
        if ($('.formGraph')[0]){
            showHideTableRowClass('formGraph', 'hide');
        }
    });
    /*
    plot options
    */    
    $('#plot_opts_button').on('click', function(){
        if ($('#tableplOpts').css('display') == 'none'){ 
            $('#tableplOpts').css('display','block');
            
        }
        else {   
            $('#tableplOpts').css('display','none');
        }
    });

    /*
    Station finder download data button
    on click a second form pops up asking for user email, 
    and additional data download options 
    */
    $('.obtain_sf_data').on('click', function(){
        $("#data_format").children('option[value="html"]').attr('disabled', true)
        ShowPopupDocu('formDownload');
        
    });
    /*
    Generates new highcarts
    graph when chartType is changed
    Currently used in spatial_summary
    */
    $('.chart_type').on('change', function(){
        var chartType = $(this).val();
        var figureID = $(this).parents('div').attr('id');
        var json_file_path = $('#json_file_path').val();
        generateHighChartTS(json_file_path,figureID,chartType); 
    });

    /*
    Set temporal resoliuton field for PRISM grid
    */
    $('#grid').on('change keyup', function(){
        if ($(this).val() == '21'){
            $('#temp_res').css('display','table-row');
            //Hide special degree day options
            $('#add').css('display','none');
            $('#dd').css('display','none');
        }
        else {
            $('#temp_res').css('display','none');
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
        
    });

    /*
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
            $("#elements option").each(function(){
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
        }
        
    });

    //monann functions --> clean up needed
    $('#element').on('change', function(){
        set_BaseTemp_and_Threshes('tableData',this);
    });
    $('#monthly_statistic').on('change', function(){
        set_NDays_thresholds('tableData',this);
    });
    $('#less_greater_or_between').on('change', function(){
        change_lgb();
    });
    /* CHECK THIS: units had set_degree_days(this.value) attached 
    $('.monann_units').on('change', function(){
        set_degree_days($(this).val());
    });
    */
});
