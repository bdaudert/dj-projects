$(function () {
    var json_file = document.getElementById("json_file").value;
    var JSON_URL = document.getElementById("JSON_URL").value;
    var json_file_path = '/csc/media/tmp/' + json_file;
    var style = {
        color:'#000000',
        fontSize:'14px'
    };
    $.getJSON(json_file_path, function(table_dict) {
        var ranges = table_dict.ranges;
        //Find max/min of ranges
        var max_vals = [];
        var min_vals = [];
        for (var mon_idx=0;mon_idx<table_dict.ranges.length;mon_idx++) {
            max_vals.push(parseFloat(table_dict.ranges[mon_idx][2]));
            min_vals.push(parseFloat(table_dict.ranges[mon_idx][1]));
        }
        var max = Math.max.apply(Math,max_vals);
        var min = Math.min.apply(Math,min_vals);
        if (max == null || min == null || Math.abs(max - min) < 0.001){
            max = null;
            min = null;
        }
        var averages = table_dict.averages;
        var base_temperature = table_dict.base_temperature;
        if (table_dict.element == 'gdd' || table_dict.element == 'hdd' || table_dict.element == 'cdd') {
            base_temperature = 'Base Temperature: ' + base_temperature;
        }
        else{
            base_temperature = '';
        }
        $('#graph_container').highcharts({
            credits: {
                href: 'http://wrcc.dri.edu/',
                text: 'wrcc.dri.edu'
            },  
            title: {
                style:style,
                text:table_dict.stn_name + ', ID: ' + table_dict.stn_id 
            },
            subtitle: {
                text: 'Mean and Range. Monthly Statistic: '  + table_dict.search_params['Monthly Statistic'],
                x: -20
            },
            xAxis: {
                labels:{
                    style: style
                },   
                categories: table_dict.month_list
            },
            yAxis: {
                labels:{
                    style: style
                },
                title: {
                    style:style,
                    text: table_dict.element_name
                },
                max:max,
                min:min
            },
        
            tooltip: {
                crosshairs: true,
                shared: true,
                valueSuffix: '°C'
            },
            
            legend: {
            },
        
            series: [{
                name: table_dict.element_name + ' ' + base_temperature,
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
                fillOpacity: 0.7,
                zIndex: 0
            }]
            
        });
    }); //end getJSON
}); // end funct
