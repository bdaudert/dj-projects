$(document).ready(function () {
    //Bootstrap nav menue
    $('[data-submenu]').submenupicker();
    var dataTables = $('.dataTable'), id;
    dataTables.each(function(index, dT){
        if ( !$.fn.dataTable.isDataTable( '#station_list' ) ) {
            //Get table info = file name
            var dataTableInfo = 'dataTable';
            id = $(this).attr('id').split('-')[1];
            if ($('#dataTableInfo-' + id).length){
                dataTableInfo = $.trim(String($('#dataTableInfo-' + id).text()).replace('/^\s*\n/gm', ''));
                var L = dataTableInfo.split('\n'), newL = [];
                var header = '';
                for (var k =0;k<L.length;k++){
                    //remove spaces
                    var l_short = $.trim(L[k]).replace(/;/g, ' ');
                    newL.push(l_short);
                    header += l_short;
                }
                dataTableInfo = newL.join(' ');
            }
            //Create dataTable
            $(dT).DataTable({
                'dom': 'Bfrtip',
                'paging': false,
                'scrollX': 'auto',
                'autoWidth':false,
                'scrollY': 600,
                'scrollCollapse': true,
                'aaSorting':[],
                'oLanguage': {
                    'sSearch': 'Filter:',
                }, 
                'columnDefs': [{
                    'targets': "_all",
                    'render': function (data, type, full, meta) {
                        if (type === 'copy') {
                            var api = new $.fn.dataTable.Api(meta.settings);
                            data = $(api.column(meta.col).header()).text() + ": " + data;
                        }
                        return data;
                    }
                }],
                'buttons': [
                    {
                        'extend':'csvHtml5',
                        'title':dataTableInfo,
                        'exportOptions': {
                            'columns': ':visible'
                        },
                        'customize': function(doc){
                            return dataTableInfo + '\n' + doc;
                        } 
                    },
                    {
                        'extend':'excelHtml5',
                        'title':dataTableInfo,
                        'exportOptions': {
                            'columns': ':visible'
                        },
                        customize: function (xlsx) {
                            var sheet = xlsx.xl.worksheets['sheet1.xml'];
                            var numrows = 1;
                            var clR = $('row', sheet);

                            //update Row
                            clR.each(function () {
                                var attr = $(this).attr('r');
                                var ind = parseInt(attr);
                                ind = ind + numrows;
                                $(this).attr("r",ind);
                            });

                            // Create row before data
                            $('row c', sheet).each(function () {
                                var attr = $(this).attr('r');
                                var pre = attr.substring(0, 1);
                                var ind = parseInt(attr.substring(1, attr.length));
                                ind = ind + numrows;
                                $(this).attr("r", pre + ind);
                            });

                            function Addrow(index,data) {
                                msg='<row r="'+index+'">'
                                for(i=0;i<data.length;i++){
                                    var key=data[i].key;
                                    var value=data[i].value;
                                    msg += '<c t="inlineStr" r="' + key + index + '">';
                                    msg += '<is>';
                                    msg +=  '<t>'+value+'</t>';
                                    msg+=  '</is>';
                                    msg+='</c>';
                                }
                                msg += '</row>';
                                return msg;
                            }
                            //insert
                            //var r1 = Addrow(1, [{ key: 'A', value: '' }, { key: 'B', value: '' }]);
                            var r1 = Addrow(1, [{ key: 'A', value: header }]);
                            sheet.childNodes[0].childNodes[1].innerHTML = r1 + sheet.childNodes[0].childNodes[1].innerHTML;
                        }
                        /*
                        #This works!!
                        'customize': function(xlsx){
                            var sheet = xlsx.xl.worksheets['sheet1.xml'];
                            var first_row = $('c[r=A1] t', sheet).text();
                            $('c[r=A1] t', sheet).text(header);
                            //Move each row down to make room for header
                        }
                        */
                    },
                    {
                        'extend':'pdfHtml5',
                        'title': dataTableInfo,
                        'orientation': 'landscape',
                        'pageSize':'A4',
                        'exportOptions': {
                            'columns': ':visible'
                        }
                    },
                    {
                        'extend':'print',
                        'title': dataTableInfo,
                        'exportOptions': {
                            'columns': ':visible'
                        }
                    },
                    {
                        'extend':'copy',
                        'title': dataTableInfo,
                        'text':'Copy Table',
                        'exportOptions': {
                            'columns': ':visible'
                        },
                        'customize': function(doc){
                            return dataTableInfo + '\n' + doc;
                        }
                    },
                    /*
                    {
                        'extend': 'copyHtml5',
                        'text': 'Copy Selected Rows',
                        'title': dataTableInfo,
                        'header': false,
                        'exportOptions': {
                            'modifier': {
                                'selected': true
                            },
                            'orthogonal': 'copy'
                        }
                    },*/
                    'colvis'
                ]
            }); //end dataTable 
        }//end if not station_list
    });//end each
    //Prevent misalignment of header/footer on  show/hide
    //$('.dataTable').wrap('<div class="dataTables_scroll" />');
    /*
    FORM HELP TEXTS
    */
    $('.qmark').on('click', function(){
        //Close all dialogs that happen to be open
        $(':ui-dialog').each(function(){
            if ($(this).dialog('isOpen')){
                $(this).dialog('destroy');
            }   
        });
        var id = $(this).attr('id');
        var pop_up = $('#' + id).next('div.pop-up');
        var max_height = $(window).height()*0.3, 
            max_width = $(window).width()*0.2;
        $(pop_up).dialog({
            position:{
                my:'bottom left',
                at:'top right',
                of:'#' + id
            },
            title:'You can move me!',
            resizable: true,
            modal: false,
            width:'auto',
            height:'auto',
            maxHeight:max_height,
            open: function() {
                $(this).scrollTop(0);
                $(this).closest(".ui-dialog")
                .find(".ui-dialog-titlebar-close")
                .removeClass("ui-dialog-titlebar-close")
                .html("<span class='ui-button-icon-primary ui-icon ui-icon-closethick'></span>");
            },
            create: function(){
                $(this).css("maxWidth", max_width);
                //$(this).css("maxHeight", max_height);
            },
            close: function () {
               $(pop_up).dialog('destroy');
            }
        }).height('auto').width('auto');
        $(pop_up).scrollTop(0);
        $(".ui-dialog").css("z-index", 10);
        $(".ui-widget-content").css("background-color", "#dedede");
        $(".ui-widget-header").css("color", "#000000");
        $(".ui-widget-header").css("background-color", "#ffffff");
        $(".ui-icon").css("background-color", "#000000");
        $(".ui-icon").css("background-color", "#ffffff");
    });
    /*
    LINKED VARIABLE UPDATES
    */ 
    $('.data_format').on('change', function(){
        $('.data_format').val($(this).val());
    });
    $('.delimiter').on('change', function(){
        $('.delimiter').val($(this).val());
    });
    $('.output_file_name').on('change', function(){
        $('.output_file_name').val($(this).val());
    });
    $('.user_name').on('change', function(){
        $('.user_name').val($(this).val());
    });
    $('.user_email').on('change', function(){
        $('.user_email').val($(this).val());
    });

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
    Zoom To Location on map
    */
    $('zoombutton').on('click', function(){
        zoomToLocation();
    });

    $("#address").focus(function(){
        if ($(this).val() == 'Place/Location'){
            $(this).val('');
        }
    });

    $('#address').bind("enterKey",function(e){
        zoomToLocation();
    });
    $('#address').keyup(function(e){
        if(e.keyCode == 13)
        {
            $(this).trigger("enterKey");
         }
    });
 

    /*
    DATE CHANGES
    */
    $('#start_date, #end_date').on('change', function(){
        //Set start/end window according to dates
        if ($('#start_window').length || $('#end_window').length){
            var date_eight = $(this).val().replace(/\-/g,'').replace(/\//g,'').replace(/\:/g,'');
            date_eight = date_eight.toLowerCase();
            var ds = $('#start_date').val().replace(/\-/g,'').replace(/\//g,'').replace(/\:/g,'');
            ds = ds.slice(0,4) + '-' + ds.slice(4,6) + '-' +  ds.slice(6,8);
            var de = $('#end_date').val().replace(/\-/g,'').replace(/\//g,'').replace(/\:/g,'');
            de = de.slice(0,4) + '-' + de.slice(4,6) + '-' +  de.slice(6,8)
            if (date_eight.length == 8 || date_eight.toLowerCase() == 'por'){
                if ($(this).attr('id') == 'start_date'){
                    if ($(this).val().toLowerCase() == 'por' && $('#end_date').val().toLowerCase() == 'por'){
                        $('#start_window').val('01-01');
                        $('#end_window').val('01-31');
                    }
                    if ($(this).val().toLowerCase() == 'por' && $('#end_date').val().toLowerCase() != 'por'){
                        var d = new Date(de);
                        //Weird lag of one day in js Date
                        d.setDate(d.getDate() + 1);
                        d.setDate(d.getDate() - 2);
                        var mm = ('0' + (d.getMonth()+1).toString()).slice(-2); 
                        var dd = ('0' + d.getDate().toString()).slice(-2);
                        $('#start_window').val(mm + '-' + dd);
                    } 
                    if ($(this).val().toLowerCase() != 'por'){
                        var d = new Date(ds);
                        //Weird lag of one day in js Date
                        d.setDate(d.getDate() + 1);
                        var mm = ('0' + (d.getMonth()+1).toString()).slice(-2); 
                        var dd = ('0' + d.getDate().toString()).slice(-2);
                        $('#start_window').val(mm + '-' + dd);
                    }
                }
                else{
                    if ($(this).val().toLowerCase() == 'por' && $('#start_date').val().toLowerCase() == 'por'){
                        $('#start_window').val('01-01');
                        $('#end_window').val('01-31');
                    }
                    if ($(this).val().toLowerCase() == 'por' && $('#start_date').val().toLowerCase() != 'por'){
                        var d = new Date(ds);
                        //Weird lag of one day in js Date
                        d.setDate(d.getDate() + 1); 
                        d.setDate(d.getDate() + 2);
                        var mm = ('0' + (d.getMonth()+1).toString()).slice(-2); 
                        var dd = ('0' + d.getDate().toString()).slice(-2);
                        $('#end_window').val(mm + '-' + dd);
                    }
                    if ($(this).val().toLowerCase() != 'por'){
                        var d = new Date(de);
                        //Weird lag of one day in js Date
                        d.setDate(d.getDate() + 1); 
                        var mm = ('0' + (d.getMonth()+1).toString()).slice(-2); 
                        var dd = ('0' + d.getDate().toString()).slice(-2);
                        $('#end_window').val(mm + '-' + dd);
                    } 
                }
            }
        }
    });
    $('#season').on('change', function(){
        today_year == String((new Date()).getFullYear());
        if ($('#season').val().inList(['winter','water_year'])){
            //Disable this year
            if ($('#year').val() == today_year){
                $('#year').val(String(parseInt(today_year) - 1));
            }
            $('#year option[value="'+ today_year + '"]').attr('disabled', true);
        }
    });

    /*
    STATION FINDER DISPLAY 
    */
    $('#display').on('change', function(){
        if ($(this).val() == 'map'){
            $('#dat_format').css('display','none');
            $('.delim').css('display','none');
            $('.out_file').css('display','none');
            if ($('#station_json').val() !=''){
                $('.sf_map').css('display','block');
            }
            else{
                $('.sf_map').css('display','none');
            }
        }
        if ($(this).val() == 'table'){
            $('#meta_keys').css('display','block');
            $('#data_format').val('html');//Default is excel
            $('#dat_format').css('display','block');
            if ($('.data_format').val().inList(['dlm','clm'])){
                $('.delim').css('display','block');
            }
            else{
                $('.delim').css('display','none');
            }
            if ($('#data_format').val() != 'html'){
                $('.out_file').css('display','block');
            }
            else{
                $('.out_file').css('display','none');
            }
            $('.sf_map').css('display','none');
        }
    });
    /*
    DATA FORMAT
    */
    $('.data_format').on('change', function(){
        if ($(this).val().inList(['clm','dlm'])){
            $('.delim').css('display','block');
         }
         else{
            $('.delim').css('display','none');

         }
         if ($(this).val().inList(['clm','dlm','xl'])){
            $('.out_file').css('display','block'); 
            if ($('#data_summary').val() == 'none' || $('#data_summary').val() == 'windowed_data'){
                $('.out_format').css('display','block');
            }
            else{
                $('.out_format').css('display','none');
            }
         }
         else{
            $('.out_file').css('display','none'); 
            $('.out_format').css('display','none');
         }   
    });
    /*
    DATA SUMMARY CHANGE
    */
    $('#data_summary').on('change', function(){
        /*
        Sets data summary fields.
        data summary can be temporal, spatial, windowed data or none
        */
        var app_name = $('#app_name').val();
        
        //Set output_format if data_format not html and no data summary
        if ($(this).val() == 'none' || $(this).val() == 'windowed_data'){
            if ($('.data_format').val() != 'html'){
                $('.out_format').css('display','block');
            }
            else{
                $('.out_format').css('display','none');
            }
        }
        else{
            $('.out_format').css('display','none');
        }
        
        if ($(this).val() == 'windowed_data'){
            $('#spat_summary').css('display','none');
            $('#temp_summary').css('display','none');
            $('#start_wind').css('display','block');
            $('#end_wind').css('display','block');
            //If data_type is station show flags/obs_time
            if ($('#data_type').length && $('#data_type').val() == 'station'){
                $('#flags').css('display','block');
                $('#obs_time').css('display','block');
            }
            else{
                $('#flags').css('display','none');
                $('#obs_time').css('display','none');
            }
        }
        else if ($(this).val() == 'spatial_summary' || $(this).val() == 'temporal_summary'){
            if ($(this).val() == 'spatial_summary'){
                $('#spat_summary').css('display','block');
                $('#temp_summary').css('display','none');
            }
            else{
                $('#spat_summary').css('display','none');
                $('#temp_summary').css('display','block');
            }
            
            //Hide windowed data options
            $('#start_wind').css('display','none');
            $('#end_wind').css('display','none');
            //Hide flags obs time
            $('#flags').css('display','none');
            $('#obs_time').css('display','none');
        }
        else if ($(this).val() =='none'){
            $('#spat_summary').css('display','none');
            $('#temp_summary').css('display','none');
            $('#start_wind').css('display','none');
            $('#end_wind').css('display','none');
            //If data_type is station show flags/obs_time
            if ($('#data_type').length && $('#data_type').val() == 'station'){
                $('#flags').css('display','block');
                $('#obs_time').css('display','block');
            }
            else{
                $('#flags').css('display','none');
                $('#obs_time').css('display','none');
            
            }
        }
    });

    /*
    ELEMENT(S) CHANGE
    */
    $('#variables').on('change', function(){
        //Update chart indices string
        if ($('#chart_indices_string').length){
            var count = $("#variables :selected").length;
            var indices = ''
            for (var i=0;i<count;i++){
                indices+=String(i) + ',';
            }
            indices = indices.substring(0, indices.length -1);
            $('#chart_indices_string').val(indices);
        }
    });

    $('#variable').on('change', function(){
        //Set monthly statistic for monthly_summary
        var sum_els = ['pcpn','snow','evap','pet'];
        if ($(this).val().inList(sum_els)){
            if ($('#statistic').length){
                $('#statistic option[value="msum"]').attr('disabled', false);                
                $('#statistic').val('msum');
            }
        }
        else {
            if ($('#statistic').length){
                $('#statistic').val('mave');
                if ($(this).val() == 'snwd'){
                    $('#statistic option[value="msum"]').attr('disabled', true);
                }
            }
        }
        if ($('#calculation').length){
            if ($(this).val().inList(sum_els)){
                $('#calculation option[value="cumulative"]').attr('disabled', false);
                $('#calculation').val('cumulative');
            }
            else{
                $('#calculation').val('values');
                $('#calculation option[value="cumulative"]').attr('disabled', true);

            }
        }
        if ($('#temporal_summary').length){
            if ($(this).val().inList(sum_els)){
                $('#temporal_summary option[value="sum"]').attr('disabled', false);
                $('#temporal_summary').val('sum');
            }
            else{
                $('#temporal_summary').val('mean');
                if ($(this).val() == 'snwd'){
                    $('#temporal_summary option[value="sum"]').attr('disabled', true);
                }
            }
        }
        if ($('#spatial_summary').length){
            if ($(this).val().inList(sum_els)){
                $('#spatial_summary option[value="sum"]').attr('disabled', false);
                $('#spatial_summary').val('sum');
            }
            else{
                $('#spatial_summary').val('mean');
                if ($(this).val() == 'snwd'){
                    $('#spatial_summary option[value="sum"]').attr('disabled', true);
                }
            }
        }
    });

    /*
    DATES
    */ 
    $('.year').on('change', function(){
        /*
        Checks that start year < end year
        and lies within grid range
        */
        var which = $(this).attr('id');
        var s_yr_int, e_yr_int, diff;
        var min_year, max_year, min_year_fut=null, max_year_fut=null;
        s_yr_int = parseInt($('#start_year').val());
        e_yr_int = parseInt($('#end_year').val());
        min_year = parseInt($('#min_year').val());
        max_year = parseInt($('#max_year').val());
        if ($('#min_year_fut').val() != ""){
            min_year_fut = parseInt($('#min_year_fut').val());
        }
        else{min_year_fut = min_year;}
        if ($('#max_year_fut').val() != ""){
            max_year_fut = parseInt($('#max_year_fut').val());
        }
        else{max_year_fut = max_year;}
        diff = Math.abs(e_yr_int - s_yr_int);
        if (which == 'start_year'){
            //Switch to fut
            if (s_yr_int > max_year  && e_yr_int < max_year){
                $('#end_year').val(String(max_year_fut));
            }
            else{   
                if (s_yr_int + diff > max_year){
                    $('#end_year').val(String(max_year));
                }
                else{
                    if (e_yr_int - s_yr_int < 0){
                        $('#end_year').val(String(s_yr_int + diff));
                    }
                }
            }
        }
        if (which == 'end_year'){
            //Switch to fut
            if (e_yr_int > max_year  && s_yr_int < max_year){
                $('#start_year').val(String(min_year_fut));
            }
            else{
                if (e_yr_int - diff < min_year){
                    $('#start_year').val(String(min_year));
                }
                else{
                    if (e_yr_int - s_yr_int < 0){
                        $('#start_year').val(String(e_yr_int - diff));
                    }
                }
            }

        }
        //Update mn/max_year and target year
        if ($('#app_name').val() == 'intraannual'){
            if ($('#start_year').val().toLowerCase()!='por'){
                $('.target_year').val($('#start_year').val());
            }
            else{
                $('.target_year').val($('#min_year').val());
            }
        }
        if ($('#season').length){
            var d = new Date();
            var today_year = String(d.getFullYear());
            var today_month = String(parseInt(d.getMonth() + 1));
            if (String($(this).val()) == today_year){
                $('#season option[value="year_to_date"]').attr('disabled', false);
                $('#season option[value="water_year"]').attr('disabled', true); 
                $('#season option[value="winter"]').attr('disabled', true);
                if (parseInt(today_month) < 5){
                    $('#season option[value="spring"]').attr('disabled', true);
                }
                if (parseInt(today_month) < 8){
                    $('#season option[value="summer"]').attr('disabled', true);
                }  
                if (parseInt(today_month) < 11){
                    $('#season option[value="fall"]').attr('disabled', true);
                }  
                for (var mon_idx = parseInt(today_month);mon_idx <= 12; mon_idx++){
                    $('#season option[value="' + String(mon_idx) + '"]').attr('disabled', true);
                }
                $('#season option[value="ann"]').attr('disabled', true);
            }
            else if (String($(this).val()) == String(parseInt(today_year) - 1)){
                if (parseInt(today_month) < 11){
                    $('#season option[value="water_year"]').attr('disabled', true);
                }
                else{
                    $('#season option[value="water_year"]').attr('disabled', false);
                }
                for (var mon_idx = 1;mon_idx <= 12; mon_idx++){
                    $('#season option[value="' + String(mon_idx) + '"]').attr('disabled', false);
                }
                $('#season option[value="ann"]').attr('disabled', false);
                if (parseInt(today_month) < 2){
                    $('#season option[value="winter"]').attr('disabled', true);
                }
                else{
                    $('#season option[value="winter"]').attr('disabled', false);
                }
                $('#season option[value="spring"]').attr('disabled', false);
                $('#season option[value="summer"]').attr('disabled', false);
                $('#season option[value="fall"]').attr('disabled', false);
                $('#season option[value="year_to_date"]').attr('disabled', true);
            }
            else {
                for (var mon_idx = 1;mon_idx <= 12; mon_idx++){
                    $('#season option[value="' + String(mon_idx) + '"]').attr('disabled', false);
                }
                $('#season option[value="water_year"]').attr('disabled', false);
                $('#season option[value="ann"]').attr('disabled', false);
                $('#season option[value="winter"]').attr('disabled', false);
                $('#season option[value="spring"]').attr('disabled', false);
                $('#season option[value="summer"]').attr('disabled', false);
                $('#season option[value="fall"]').attr('disabled', false);
                $('#season option[value="year_to_date"]').attr('disabled', true);
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
    
    $('#DataForm, #MapForm').on('change', 'input, select, textarea', function(){
        if ($(this).attr('id')){
            var form_field_id = $(this).attr('id');
        }
        else{
            var form_field_id = $(this).attr('class');
        }
        //Hide results
        if ($('#app_name').val() == 'station_finder'){
            if ($('#display').val() == 'table'){
                if (!form_field_id.inList(['display','data_format', 'delimiter','output_file_name'])){
                    $('.results').css('display','none');
                }
            } 
            else{
                 if ($(this).attr('id') != 'display'){
                    $('.results').css('display','none');
                }
            }
        }
        else{
            $('.results').css('display','none');
        }
        //Hide appropriate form errors
        //Start and end date may have correlated errors
        $('.form_error').css('display','none');
        if ($('#back_button_error').length){
            $('#back_button_error').css('display','none');
        }
    });
    
    /*
    PLOTS
    */    
    $('#plot_opts_button').on('click', function(){
        if ($('.plOpts:first').css('display') == 'none'){ 
            if ($(this).val().inList(['image_size','cmap'])){
                $('.plOpts').css('display','inline-block');
            }
            else{
                $('.plOpts').css('display','block');
            }
            
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
        ShowPopupDocu('formDownload');
        $('.data_format option[value="html"]').attr('disabled', true);
    });
    
    /*
    GRID 
    changes start/end data 
    and sets temp resolution for prism data
    */
    $('#grid').on('change keyup', function(){
        if ($(this).val() == '21'){
            if ($('#temp_res').length){
                $('#temp_res').css('display','block');
            }
            //Hide special degree day options
            $('#add').css('display','none');
            $('#dd').css('display','none');
        }
        else {
            if ($('#temp_res').length){
                $('#temp_res').css('display','none');
            }
             $('#add').css('display','block');
            if ($('#add_degree_days').val() == 'T'){
                $('#dd').css('display','block');
            }
        }
        //Disable variables if prism
        var non_prism_els = ['gdd','hdd','cdd'];
        var station_only_els = ['obst','snow','snwd','evap','wdmv'];
        $("#variables option").each(function(){
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
        var new_dates, ds, de, start_div, end_div;
        //Change start/end dates/years according to grid
        var start=null, end=null,new_dates,p='year';
        if ($('#start_year').length && $('#end_year').length){
            start = $('#start_year').val();
            end = $('#end_year').val();
            p = 'year';
            set_year_range()
            //Update target year for intra
            if ($('#app_name').val() == 'intraannual'){
                if ($('#start_year').val().toLowerCase()!='por'){
                    $('.target_year').val($('#start_year').val());
                }
                else{
                    $('.target_year').val($('#min_year').val());
                }
            }
        }
        if ($('#start_date').length && $('#end_date').length){
            start = $('#start_date').val();
            end = $('#end_date').val();
            p = 'date';
            new_dates = set_dates_for_grid($(this).val(),start,end,p);
        }
        if ($('#year').length){
            start = $('#year').val();
            end = $('#year').val();
            p = 'year';
        }
        //Set date values
        var date_vals = set_dates_for_grid($(this).val(),start,end,p);
        $('#start_' + p).val(date_vals.start);
        $('#end_' + p).val(date_vals.end);
        if ($('#year').length){
            $('#year').val(date_vals.start);
        } 
    });
    /*
    GRID 
    temporal resolution 
    (PRISM has monthly/yearly as well as daily)
    */
    $('#temporal_resolution').on('change', function(){
        var date_vals = set_dates_for_grid($('#grid').val(), $('#start_date').val(), $('#end_date').val(), 'dates');
        $('#start_date').val(date_vals.start);
        $('#end_date').val(date_vals.end); 
    });

    /*
    DATA TYPE
    Sets form fields according to data_type (station/grid)
    Affected form fields are
    variables
    grid
    */
    $('.data_type').on('change keyup', function(){
        var data_type = $(this).val();
        //Needed for single lister
        $('#data_type').val(data_type);
        //Hide station finder link
        if ($('#stn_finder').length ){
            if (data_type == 'grid' || $(this).val().inList(['location','locations'])){
                $('#stn_finder').css('display','none');
            }
            else{
                $('#stn_finder').css('display','block'); 
            }
        }
        update_value($(this).val()); //form_utils function
        //Set the variables
        set_variables();
        
        //var station_only_els = ['obst','snow','snwd','evap','wdmv'];
        //var non_prism_els = ['gdd','hdd','cdd'];
        
        //Set grid form fields
        //var opts = null;
        if (data_type == 'grid' || data_type.inList(['location','locations'])){
            //Disable station_ids option
            $('#area_type option[value="station_ids"]').attr('disabled',true);
            $('#area_type option[value="location"]').attr('disabled',false);
            $('#area_type option[value="locations"]').attr('disabled',false);
            //If prism hide special degree days
            if ($('#grid').val() == '21'){
                $('#add').css('display','none');
                $('#dd').css('display','none');
            }
            else {
                $('#add').css('display','block');
                if ($('#add_degree_days').val() == 'T'){
                    $('#dd').css('display','block');
                }
            }
            //Hide flags/obs time
            $('#flags').css('display','none');
            $('#obs_time').css('display','none')
            //Show grid
            $('#grid_type').css('display','block');
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
                $('#summary_type option[value="pcpn"]').attr('disabled',true);
                $('#summary_type option[value="both"]').attr('disabled',true);
                $('#summary_type option[value="temp"]').attr('selected',true);
            }

        }
        //Set station form fields
        if (data_type == 'station' || data_type.inList(['station_id','station_ids'])){
            //Enable station_ids option
            $('#area_type option[value="station_ids"]').attr('disabled',false); 
            $('#area_type option[value="locations"]').attr('disabled',true);
            $('#area_type option[value="location"]').attr('disabled',true);
            //Show add degree day option    
            $('#add').css('display','block');
            $("#variables option").each(function(){
                //Enable all variables
                $(this).attr('disabled',false);
            });
            //Hide flags/obs time
            $('#flags').css('display','block');
            //$('#obs_time').css('display','block')
            //Show grid
            $('#grid_type').css('display','none');
            //Enable snow from climatology summary type
            if ($('#summary_type').length){
                $('#summary_type option[value="all"]').attr('disabled',false);
                $('#summary_type option[value="prsn"]').attr('disabled',false);
                $('#summary_type option[value="pcpn"]').attr('disabled',true);
                $('#summary_type option[value="both"]').attr('disabled',false);
                $('#summary_type option[value="all"]').attr('selected',true);
            }            
        } 
    });

    /*
    MONTHLY SUMMARIES LISTENERS
    */
    $('#show_hide_graph').on('click', function(){
        if ($(this).val() == 'Show Graph'){
            $('#main-graph').css('display','block');
            setTimeout(function(){},1000);
            $(window).resize();
            $(this).val('Hide Graph');
        }
        else{
            $('#main-graph').css('display','none');
            $(this).val('Show Graph');
        }
    });
    $('#show_hide_summary').on('click', function(){
        if ($(this).val() == 'Show Summary'){
            $('#summary-table').css('display', 'block');
            $(this).val('Hide Summary');
        }
        else{
            $('#summary-table').css('display', 'none');
            $(this).val('Show Summary');
        }
    });
    $('#show_hide_data').on('click', function(){
        if ($(this).val() == 'Show Data'){
            $('#main-table').css('display', 'block');
            $(this).val('Hide Data');
        }
        else{
            $('#main-table').css('display', 'none');
            $(this).val('Show Data');
        }
    });

    /*
    MONTHLY SUMMARIES THRESHOLDS FOR NDAYS
    */
    //lean up needed
    $('#variable').on('change', function(){
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
            $('#threshold_type').css('display','block');
            var lgb = $('#less_greater_or_between').val();
            if (lgb == 'b'){$('#threshold_between').css('display','block');}
            if (lgb == 'l'){$('#threshold_below').css('display','block');}
            if (lgb == 'g'){$('#threshold_above').css('display','block');}
        }
        else{
            $('#threshold_type').css('display','none');
            $('#threshold_between').css('display','none');
            $('#threshold_below').css('display','none');
            $('#threshold_above').css('display','none');
        }
    });
    $('#less_greater_or_between').on('change', function(){
        var threshes = set_threshes($('#variable').val()).split(',');
        var lgb = $(this).val();
        if (lgb == 'b'){ 
            $('#threshold_low_for_between').val(threshes[2]);
            $('#threshold_high_for_between').val(threshes[3]);
            $('#threshold_between').css('display','block');
            $('#threshold_below').css('display','none');
            $('#threshold_above').css('display','none');
        }   
        if (lgb == 'l'){ 
            $('#threshold_for_less_than').val(threshes[0]);
            $('#threshold_below').css('display','block');
            $('#threshold_between').css('display','none');
            $('#threshold_above').css('display','none');
        }
        if (lgb == 'g'){
            $('#threshold_for_greater_than').val(threshes[1]);
            $('#threshold_above').css('display','block');
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
    //resets overlay map if same region is chosen
    $('.area_type').on('mouseup', function() {
        if ($(this).val().inList(['basin','county_warning_area', 'county','climate_division'])){
            $('.area_type').trigger("change");
        } 
    });
    $('.area_type').on('keydown change', function(){
        //Set area form field
        set_area($(this)); //form_utils function
        /*need to change data type for single apps*/
        if ($(this).val().inList(['location','locations'])){
            $('#data_type').val('grid');
            if ($('#stn_finder').length){
                $('#stn_finder').css('display','none');
            }
        }
        else if ($(this).val()== 'station_id'){
            $('#data_type').val('station');
            if ($('#stn_finder').length){
                $('#stn_finder').css('display','block');
            }
        }
        set_variables();
        set_map($(this)); //form_utils function
        update_value($(this).val()); //form_utils function
        if ($(this).val() == 'shape_file'){
            ShowPopupDocu('uploadShapeFile');
        }
        if (app_name == 'climatology'){
            if ($(this).val() == 'location'){
                if ($('#summary_type').val().inList(['all','both'])){
                    $('#summary_type').val('temp');
                }
                $('#summary_type option[value="all"]').attr('disabled',true);
                $('#summary_type option[value="both"]').attr('disabled',true);
            }
            else{
                $('#summary_type option[value="all"]').attr('disabled',false);      
                $('#summary_type option[value="both"]').attr('disabled',false);
            }
        }
        //Hide or show obs time and flags options
        if ($('#data_type').val() == 'grid' || $('#area_type').val().inList(['location','locations'])){
            $('#obs_time').css('display','none');
            $('#flags').css('display','none');
        }
        else{
            $('#obs_time').css('display','block');
            $('#flags').css('display','block'); 
        }
        //Single app specific
        //Deal with dates AND
        //Show/Hide grid form field and station finder form_field
        var start='9999-99-99', end= '9999-99-99';
        if ($('#start_date').length && $('#end_date').length){
            start = $('#start_date').val();
            end = $('#end_date').val();
            p = 'date';
        }
        if ($('#start_year').length && $('#end_year').length){
            start = $('#start_year').val();
            end = $('#end_year').val();
            p = 'year';
        }
        var date_vals = null;
        if ($(this).val() == 'station_id'){
            $('#grid_type').css('display','none');
            $('#stn_finder').css('station_finder','block');
            //Trigger ajax call to find valid daterange of station
            //This call also sets the year range or start/end dates appropriately
            $('#station_id').trigger('change');    
        }
        if ($(this).val().inList(['location','locations'])){
            $('#grid_type').css('display','block');
            date_vals = set_dates_for_grid($('#grid').val(),start, end,p);
        }
        if ($('#app_name').val() == 'station_finder' && $(this).val() != 'station_id'){
            date_vals = set_dates_for_station($(this).val(), start, end,p);
        }
        if (date_vals){
            $('#start_' + p).val(date_vals.start);
            $('#end_' + p).val(date_vals.end);
        }
        //Change start/end yearsi and set year ranges
        var app_name = $('#app_name').val();
        if (app_name.inList(['seasonal_summary','intraannual','monthly_summary','climatology'])){
            //Set range dropdown values
            set_year_range(start=$('#start_year').val(),end=$('#end_year').val());
            //Update target year for intra
            console.log($('#start_year').val());
            if (app_name == 'intraannual'){
                if ($('#start_year').val().toLowerCase()!='por'){
                    $('.target_year').val($('#start_year').val());
                }
                else{
                    $('.target_year').val($('#min_year').val());
                }
            }
        }

    });

    $('#location').on('change', function(){
        MAP_APP.Utils.update_marker_on_map($(this).val());
    });

    /*
    DYNAMIC HIGHCHARTS
    */
    $('#legend_button').click(function() {
        if ($(this).val() == 'Hide Legend'){
            $(this).val('Show Legend');
            //Hide the Legend
            myChart.legend.enabled = false;
            myChart.legend.group.hide();
            myChart.legend.box.hide();
            myChart.legend.display = false;
            //Disable legend in exporting
            myChart.options.exporting.chartOptions.legend.enabled = false;
        }
        else{
            //Show Legend
            $(this).val('Hide Legend');
            myChart.legend.enabled = true;
            myChart.legend.group.show();
            myChart.legend.box.show();
            myChart.legend.display = true;
            //Enable legend in exporting
            myChart.options.exporting.chartOptions.legend.enabled = true;
        }
    });
    
    $('#chart_type').on('change keyup', function(){
        var chartType = $('#chart_type').val();
        for (var i = 0; i < myChart.series.length; i++) {
            //Check if series is main/average or runmean
            var c_type = myChart.series[i].options.id.split('_')[0];
            if (c_type == 'main'){
                myChart.series[i].update({type:chartType});
            }
        }
        //Update hidden chart variables in  main form
        $('.chart_type').val($(this).val());
    });

    //chart checkboxes
    $('#show_range, #show_running_mean, #show_average, #climatology, #percentile_5, #percentile_10, #percentile_25').on('click', function(){
        //Find the correct chart
        var l_type = $(this).val();
        for(var i = myChart.series.length - 1; i > -1; i--){
            if (myChart.series[i].options.id.split('_')[0] == l_type || myChart.series[i].options.id == l_type){
                if ($(this).is( ":checked" )){
                    myChart.series[i].setVisible(true, true);
                    myChart.series[i].update({showInLegend: true});
                    if ($('#legend_button').val() == 'Show Legend'){
                       myChart.legend.enabled = false;
                       myChart.legend.group.hide();
                       myChart.legend.box.hide();
                       myChart.legend.display = false; 
                    }
                }
                else{
                    myChart.series[i].setVisible(false, false);
                    myChart.series[i].update({showInLegend: false});
                }
                myChart.redraw();
            }
        }
        //Update hidden chart variables in  main form
        if ($(this).is(':checked')) { 
            $('.' + $(this).attr('id')).val('T');
        }
        else{
             $('.' + $(this).attr('id')).val('F');
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
                    //Update hidden chart vars
                    $('.running_mean_days').val(running_mean_period);
                }
                if ($('#running_mean_years').length){
                    r_name+='year Running Mean ' + s_name;
                    //Update hidden chart vars
                    $('.running_mean_years').val(running_mean_period);
                }
                myChart.series[i].update({data: rm_data, name:r_name });

                //myChart.series[i].data = rm_data;
                myChart.redraw();
                rm_data = null;
                s_id = null;
            }
        }
    });
    //Monthly summary dynamic chart updates
    $('.chart_indices, #chart_summary').on('change keyup', function(){
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
        //Update hidden chart variables in  main form
        if ($(this).attr('id') == 'chart_summary'){
            $('.chart_summary').val($(this).val());
        }
        if ($(this).attr('class') == 'chart_indices'){
            var index_string = '';
            //$("#chart_indices :selected").each(function(){
            $(".chart_indices :checked").each(function(){
                index_string+=$(this).val() + ','; 
            });
            index_string = index_string.substring(0,index_string.length - 1);
            $('.chart_indices_string').val(index_string);
        }

    });

    //Threshold for seasonal_summary
    $('#chart_threshold').on('change keyup', function(){
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
        //Update hidden chart variables in  main form
         $('.chart_threshold').val($(this).val());
    });

   $('#target_year_figure').on('change', function(){
        var year = parseInt($(this).val());
        //Set plot vars
        $('.target_year').val(String(year));
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
                var s_year = parseInt($('#min_year').val()) + parseInt(idx);
                if (s_year != year){
                    //Hide series
                    myChart.series[i].setVisible(false,false);
                    myChart.series[i].update({showInLegend: false});
                }
                else{
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
                        date_int = myChart.series[i].data[j].x;
                        //Convert integer time to date string
                        var d = new Date(date_int + 1000*60*60*24);
                        var day = ("0" + d.getDate()).slice(-2);
                        var mon = ("0" + (d.getMonth() + 1)).slice(-2);
                        var yr = d.getFullYear();
                        date_str = yr + '-' + mon + '-' + day;
                        try{
                            val = parseFloat(myChart.series[i].data[j].y).toFixed(4);
                        }
                        catch(e){
                            val = myChart.series[i].data[j].y;
                        }
                        if(typeof val !== "undefined") {
                            var row = $('<tr></tr>').appendTo(data_table);
                            $('<td></td>').text(date_str).appendTo(row);
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
    $('#station_list tbody').on('click', 'tr', function(){
        infowindow.close();
        infowindow.setContent($(this).attr('cString'));
        infowindow.open(window.sf_map, window.markers[parseInt($(this).attr('id'))]);
        var bounds = window.sf_map.getBounds();
        bounds.extend(new google.maps.LatLng(parseFloat($(this).attr('lat')), parseFloat($(this).attr('lon'))));
    });
    /***************
    AJAX CALLS
    ****************/
    //STATION_ID Change --> Find POR of station
    $('#station_id').on('change', function(){
        $('.ajax_error').html();
        waitingDialog.show('Finding date range for station', {dialogSize: 'sm', progressType: 'warning'});
        var el_list = [], el_tupe = null; 
        if ($('#variables').length){
            el_list = $('#variables').val();
            el_tuple = el_list + "";
        }   
        if ($('#variable').length){
            el_list = [$('#variable').val()];
            el_tuple = $('#variable').val();
        }
        var form_data = 'station_id_change=True';
        form_data+='&csrfmiddlewaretoken=' + $("[name=csrfmiddlewaretoken]").val();
        form_data+='&station_id=' + $(this).val();
        form_data+='&el_tuple=' + el_tuple;
        form_data+='&max_or_min=min';
        var new_url = window.location.href.split('?')[0] + form_data;
        var jqxhr = $.ajax({
            url:'',
            method: "POST",
            data: form_data
        })
        .done(function(response) {
            response = JSON.parse(response);
            //console.log(response);
            var station_start_date = response['start_date'],
                station_end_date = response['end_date'];
            $('#min_date').val(station_start_date);
            $('#max_date').val(station_end_date);
            $('#min_year').val(station_start_date.slice(0,4));
            $('#max_year').val(station_end_date.slice(0,4));
            if (station_start_date.inList(['9999-99-99','']) || station_end_date.inList(['9999-99-99',''])){
                var stn_finder_link = '<a target="blank" href="http://www.wrcc.dri.edu/csc/scenic/data/climate_data/station_finder/">Station Finder</a>';
                var err = 'Could not find valid date range for this station and chosen variables.<br />'
                err+='Please check the ';
                err+= stn_finder_link;
                err+=' to find stations for your region and date ranges.';
                $('.ajax_error').html(err);
            }
            else {
                if ($('#app_name').val().inList(['intraannual','seasonal_summary','monthly_summary','climatology'])){
                 set_year_range(start=String(station_start_date).slice(0,4),end=String(station_end_date).slice(0,4));
                }
                if ($('#app_name').val().inList(['single_lister'])){
                    var form_start_date = $('#start_date').val();
                    var form_end_date = $('#end_date').val();
                    if (new Date(station_start_date) > new Date(form_start_date)){
                        $('#start_date').val(station_start_date);
                    }
                    if (new Date(station_end_date) < new Date(form_end_date)){
                        $('#end_date').val(station_end_date);
                    }
                    if (new Date(station_end_date) < new Date(form_start_date)){
                        $('#start_date').val(station_start_date);
                        $('#end_date').val(station_end_date);
                        //alert('Start/End dates changed to valid date range for this station: ' + station_start_date + ' - ' + station_end_date);
                    }
                    if (new Date(station_start_date) > new Date(form_end_date))
{
                        $('#start_date').val(station_start_date);
                        $('#end_date').val(station_end_date);
                        //alert('Start/End dates changed to valid date range for this station: ' + station_start_date + ' - ' + station_end_date);
                    }

                }
            }
            waitingDialog.hide();
        })
        .fail(function(jqXHR) {
            $('.ajax_error').html(get_ajax_error(jqXHR.status));
            waitingDialog.hide();
       }) 
    });

    //OVERLAY_STATES
    $('#overlay_state').on('change', function(){
        waitingDialog.show('Processing', {dialogSize: 'sm', progressType: 'warning'});
        $('.overlay_state').val($(this).val());
        //$('#overlayForm').on('submit', function(event){
        //event.preventDefault();
        var form_data = $("#overlayForm").serialize();
        form_data+='&area_type=' + $('#area_type').val();
        var jqxhr = $.ajax({
            url:'',
            method: "POST",
            data: form_data,
        })
        .done(function(response) {
            response = JSON.parse(response);
            if ('overlay_error' in response){
                $('.ajax_error').html(response['overlay_error'])
            }
            else{
                $('#kml_file_path').val(response['kml_file_path']);
                initialize_map_overlays();
            }
            waitingDialog.hide();
        })
        .fail(function(jqXHR) {
            $('.ajax_error').html(get_ajax_error(jqXHR.status));
            waitingDialog.hide();
       }) 
    });

    //Station Finder data download
    $('#StationFinderDownloadForm').on('submit', function(event){
        waitingDialog.show('Processing', {dialogSize: 'sm', progressType: 'warning'});
        event.preventDefault();
        $('#formDownload').dialog('close');
        //var form_data = $('#DataForm :input, #StationFinderDownloadForm :input').serialize();
        var form_data = $('#DataForm, #StationFinderDownloadForm').serialize();
        var jqxhr = $.ajax({
            url:'',
            method: "POST",
            data: form_data,
        })
        .done(function(response) {       
            response = JSON.parse(response);
            if ('form_error_download' in response){
                 $('#formDownload').dialog('open');
                $('.formErrorDownload').html(response['form_error_download']);
                $('.formErrorDownload').css('display','block');
            }
            else{
                $('.formErrorDownload').css('display','none');
                ShowPopupDocu('offlineMessage');
            }
            waitingDialog.hide();
        })
        .fail(function(jqXHR) {
            $('.ajax_error').html(get_ajax_error(jqXHR.status));
            waitingDialog.hide();
       })
    });
    //Large requests
    $('#LargeRequestForm').on('submit', function(event){
        waitingDialog.show('Processing', {dialogSize: 'sm', progressType: 'warning'});
        event.preventDefault();
        $('#formLargeRequest').dialog('close');
        //All extra input variables are linked and updated in the DataForm
        //Note need hidded vars user_name, email, delimiter, etx in main form
        var form_data = $('#DataForm, #LargeRequestForm').serialize(); 
        var jqxhr = $.ajax({
            url:'',
            method: "POST",
            data: form_data,
        })
        .done(function(response) {
            response = JSON.parse(response);
            if ('form_error' in response){
                $('#formLargeRequest').dialog('open');
                $('.formErrorLargeRequest').html(response['form_error']);
                $('.formErrorLargeRequest').css('display','block');
            }
            else{
                $("#largeRequestForm").dialog('close');
                $('.formErrorLargeRequest').css('display','none');
                //$('#offlineMessage').css('display','block');
                ShowPopupDocu('offlineMessage');

            }
            waitingDialog.hide();
        })
        .fail(function(jqXHR) {
            $('.ajax_error').html(get_ajax_error(jqXHR.status));
            waitingDialog.hide();
       })
    });
});
