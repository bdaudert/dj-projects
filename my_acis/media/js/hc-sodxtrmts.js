$(function () {
    var json_file = document.getElementById("json_file").value;
    var JSON_URL = document.getElementById("JSON_URL").value;
    var json_file_path = '/csc/media/tmp/' + json_file;
    var style_axes = set_AxesStyle();
    var style_text = set_LableStyle();
    $.getJSON(json_file_path, function(table_dict) {
        //Find max/min of ranges
        var max_vals = [];
        var min_vals = [];
        for (var mon_idx=0;mon_idx<table_dict.ranges.length;mon_idx++) {
            max_vals.push(parseFloat(table_dict.ranges[mon_idx][2]));
            min_vals.push(parseFloat(table_dict.ranges[mon_idx][1]));
        }
        var max = find_max(max_vals, table_dict.element);
        var min = find_min(min_vals, table_dict.element);
        var x_plotLines = set_plotLines(11, 0, 1);
        var y_axis_props = set_axis_properties(max, min, table_dict.element,10.0);
        /*
        var tickInterval = y_axis_props.tickInterval;
        var axisMin = y_axis_props.axisMin;
        var axisMax = y_axis_props.axisMax;
        var y_plotLines = y_axis_props.plotLines;
        */

        /*
        var tickInterval = set_tickInterval(max, min,10.0)
        var axisMin = set_axisMin(min, table_dict.element, tickInterval);
        var axisMax = set_axisMax(max, table_dict.element, tickInterval);
        var y_plotLines = set_plotLines(axisMax, axisMin, tickInterval);
        */
        var averages = table_dict.averages;
        var base_temperature = table_dict.base_temperature;
        if (table_dict.element == 'gdd' || table_dict.element == 'hdd' || table_dict.element == 'cdd') {
            base_temperature = 'Base Temperature: ' + base_temperature;
        }
        else{
            base_temperature = '';
        }
        //Find name of monthly statistics
        for (idx=0;idx<table_dict.header.length;idx++){
            if (table_dict.header[idx][0] == 'Monthly Statistic'){
                var monthly_statistic = table_dict.header[idx][1];
            }
        }
        $('#graph_container').highcharts({
            credits: {
                href: 'http://wrcc.dri.edu/',
                text: 'wrcc.dri.edu'
            },
            margin:[50,50,50,50],
            title: {
                style:style_text,
                text:table_dict.stn_name + ', ' + table_dict.stn_state 
            },
            subtitle: {
                text: 'Network: ' + table_dict.stn_network + ', ID: ' + table_dict.stn_id,
                //text: 'Mean and Range of '  + monthly_statistic + ' for ' + table_dict.element_name,
                x: -20
            },
            labels:{
                items:[{
                    html:'Mean and Range of '  + monthly_statistic + ', ' + table_dict.element_name, 
                    //html:'Start Year: ' + table_dict.start_date + ' End Year: ' + table_dict.end_date,
                    style:{
                        top:'-10px',
                        left:'50px',
                        fontSize:'14px',
                        color:'#0000FF'
                    }
                },
                {
                    html:'Start Year: ' + table_dict.start_date + ' End Year: ' + table_dict.end_date,
                    style:{
                        top:'330px',
                        left:'150px',
                        fontSize:'12px',
                        color:'#000000'
                    }
                }],
                style: {color: '#000000'}
            },
            legend:{
                enabled:false
            },
            xAxis: {
                labels:{
                    style: style_axes,
                    step:2
                },   
                categories: table_dict.month_list,
                plotLines:x_plotLines
            },
            yAxis: {
                labels:{
                    style: style_axes
                },
                title: {
                    style:style_text,
                    text: table_dict.element_name
                },
                max:y_axis_props.axisMax,
                min:y_axis_props.axisMin,
                gridLineWidth:0,
                tickInterval:y_axis_props.tickInterval,
                startOnTick:false,
                plotLines:y_axis_props.plotLines
            },
        
            tooltip: {
                crosshairs: true,
                shared: true
                //valueSuffix: 'in'
            },
            
            series: [{
                name: monthly_statistic +  ' of ' + table_dict.element_name + ' ' + base_temperature,
                data: averages,
                zIndex: 1,
                marker: {
                    fillColor: 'white',
                    lineWidth: 1,
                    lineColor: Highcharts.getOptions().colors[0]
                }
            }, {
                name: 'Range',
                data: table_dict.ranges,
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
