$(document).ready(function ($) {
    //DataTables
    var dataTableInfo = $.trim(String($('.dataTableInfo').text()).replace('/^\s*\n/gm', ''));
    var L = dataTableInfo.split('\n'), newL = [];
    var header = '';
    for (var k =0;k<L.length;k++){
        //remove spaces
        var l_short = $.trim(L[k]).replace(/;/g, ' ');
        newL.push(l_short);
        header += l_short;
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
                    'customize': function(xlsx){
                        var sheet = xlsx.xl.worksheets['sheet1.xml'];
                        var first_row = $('c[r=A1] t', sheet).text();
                        $('c[r=A1] t', sheet).text(header);
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
