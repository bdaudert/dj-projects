$(document).ready(function ($) {
    //DataTables
    var dataTableInfo = $.trim(String($('.dataTableInfo').text()).replace('/^\s*\n/gm', ''));
    var L = dataTableInfo.split('\n'), newL = [];
    for (var k =0;k<L.length;k++){
        newL.push($.trim(L[k]));
    }
    dataTableInfo = newL.join(' ');

    //Note, this interferes when station finder 
    if ( !$.fn.dataTable.isDataTable( '#station_list' ) ) {
        //Initialize Data Tables
        $('.dataTable').DataTable({
            'dom': 'Bfrtip',
            'paging': false,
            'scrollY': 400,
            'scrollCollapse': true,
            'scrollX': 'auto',
            'autoWidth':false,
            'buttons': [
                {
                    'extend':'csvHtml5',
                    'title':dataTableInfo,
                    'exportOptions': {
                        'columns': ':visible'
                    }
                },
                {
                    'extend':'excelHtml5',
                    'title':dataTableInfo,
                    'exportOptions': {
                        'columns': ':visible'
                    }
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
                    'exportOptions': {
                        'columns': ':visible'
                    }
                },
                'colvis'
            ]
        });
    }


    $('#id_station_selection, #id_statistic, #id_element').on('change', function(){
        if ($('#app_name').val() != 'sodpiii'){
            $('#form2div').css('display','none');
        }
    });

});
