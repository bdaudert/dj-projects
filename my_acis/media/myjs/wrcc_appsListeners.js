$(document).ready(function ($) {
    //Bootstrap nav menue
    $('[data-submenu]').submenupicker();

    //dataTables
    var dataTables = $('.dataTable');
    dataTables.each(function(index, dT){
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
            'order':[],
            'paging': false,
            'scrollY': 400,
            'scrollCollapse': true,
            'scrollX': 'auto',
            'autoWidth':false,
            'oLanguage': {
                'sSearch': 'Filter:',
            }, 
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
        }); //end dataTabel    
    });//end each    

    //Listeners
    $('#id_station_selection, #id_statistic, #id_variable').on('change', function(){
        if ($('#app_name').val() != 'sodpiii'){
            $('#form2div').css('display','none');
        }
    });
    $('#form2div, #stn_selection').on('change', function(){
        $('.results').css('display','none');
    });
});
