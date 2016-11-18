$(document).ready(function ($) {
    //Bootstrap nav menue
    $('[data-submenu]').submenupicker();

    //dataTables
        var dataTables = $('.dataTable');
    dataTables.each(function(index, dT){
        //Get table info = file name
        var dataTableInfo = 'dataTable';
        if ($('#dataTableInfo_' + String(index)).length){
            dataTableInfo = $.trim(String($('#dataTableInfo_' + String(index)).text()).replace('/^\s*\n/gm', ''));
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
        if ( !$.fn.dataTable.isDataTable( '#station_list' ) ) {
            $(dT).DataTable({
                'dom': 'Bfrtip',
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
                            //Move each row down to make room for header
                            /*
                            var clRows = $('row', sheet);
                            clRows.each(function () {
                                var attr = $(this).attr('r');
                                var ind = parseInt(attr);
                                ind = ind + 1;
                                $(this).attr('r',ind);
                            });
                            //Insert header
                            var h_row = '<row r="1">';
                            h_row += '<c t="inlineStr" r="A1" s="42"><is><t>';
                            h_row += header + '</t></is></c>';
                            //sheet.childNodes[0].childNodes[1].innerHTML = h_row + sheet.childNodes[0].childNodes[1].innerHTML; 
                            $('c[r=A1] t', sheet).text(' C OO aS');
                            */
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
        }//end if not station_list
    });//end each    

    //Listeners
    $('#id_station_selection, #id_statistic, #id_element').on('change', function(){
        if ($('#app_name').val() != 'sodpiii'){
            $('#form2div').css('display','none');
        }
    });

});
