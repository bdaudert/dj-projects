$(function () {
    var json_file = document.getElementById("json_file").value;
    var JSON_URL = document.getElementById("JSON_URL").value;
    var json_file_path = '/csc/media/tmp/' + json_file;
    $.getJSON(json_file_path, function(table_dict) {
        var ranges = table_dict.ranges;
        var averages = table_dict.averages;
        var base_temperature = table_dict.base_temperature;
        if (base_temperature) {
            base_temperature = 'Base Temperature: ' + base_temperature
        }
        $('#graph_container').highcharts({
        
            title: {
                text: table_dict.element_name + ' ' + base_temperature
            },
            subtitle: {
                text: 'Mean and Range',
                x: -20
            },
            xAxis: {
                categories: table_dict.month_list
            },
            yAxis: {
                title: {
                    text: null
                }
            },
        
            tooltip: {
                crosshairs: true,
                shared: true,
                valueSuffix: '°C'
            },
            
            legend: {
            },
        
            series: [{
                name: 'Station Name: ' + table_dict.stn_name + ', ID: ' + table_dict.stn_id,
                data: averages,
                zIndex: 1,
                marker: {
                    fillColor: 'white',
                    lineWidth: 2,
                    lineColor: Highcharts.getOptions().colors[0]
                }
            }, {
                name: 'Range',
                data: ranges,
                type: 'arearange',
                lineWidth: 0,
                linkedTo: ':previous',
                color: Highcharts.getOptions().colors[0],
                fillOpacity: 0.3,
                zIndex: 0
            }]
            
        });
    }); //end getJSON
}); // end funct
