$(function () {
    var json_file = document.getElementById("json_file").value;
    var TMP_URL = document.getElementById("TMP_URL").value;
    var json_file_path = TMP_URL + json_file;
    var axesStyle = set_AxesStyle();
    var titleStyle = set_TitleStyle();
    var subtitleStyle = set_SubtitleStyle();
    $.getJSON(json_file_path, function(datadict) {
        //Find max/min of ranges
        var max_vals = [];
        var min_vals = [];
        for (var mon_idx=0;mon_idx<datadict.ranges.length;mon_idx++) {
            max_vals.push(parseFloat(datadict.ranges[mon_idx][2]));
            min_vals.push(parseFloat(datadict.ranges[mon_idx][1]));
        }
        var max = find_max(max_vals, datadict.element,datadict.initial.monthly_statistic);
        var min = find_min(min_vals, datadict.element,datadict.initial.monthly_statistic, datadict.initial.departures_from_averages);
        var x_plotLines = set_plotLines(11, 0, 1);
        //Align x ticks with plotlines
        var x_tickPositions = align_ticks(x_plotLines); 
        var y_axis_props = set_axis_properties(max,'Use default', min, 'Use default',datadict.element,datadict.initial.monthly_statistic,'F',10.0);
        //Align y ticks with plotlines
        var y_tickPositions = align_ticks(y_axis_props.plotLines);
        var averages = datadict.averages;
        var base_temperature = datadict.base_temperature;
        if (datadict.element == 'gdd' || datadict.element == 'hdd' || datadict.element == 'cdd') {
            base_temperature = 'Base Temperature: ' + base_temperature;
        }
        else{
            base_temperature = '';
        }
        //Find name of monthly statistics
        for (idx=0;idx<datadict.header.length;idx++){
            if (datadict.header[idx][0] == 'Monthly Statistic'){
                var monthly_statistic = datadict.header[idx][1];
            }
        }
        $('#graph_container').highcharts({
            credits: {
                href: 'http://wrcc.dri.edu/',
                text: 'wrcc.dri.edu'
            },
            margin:[50,50,50,50],
            title: {
                style:titleStyle,
                text:datadict.stn_name + ', ' + datadict.stn_state 
            },
            subtitle: {
                //text: 'Network: ' + datadict.stn_network + ', ID: ' + datadict.stn_id,
                text: 'Mean and Range of '  + monthly_statistic + ' for ' + datadict.element_name,
                style:subtitleStyle
            },
            labels:{
                items:[{
                    html:'Network: ' + datadict.stn_network + ', ID: ' + datadict.stn_id,
                    //html:'Mean and Range of '  + monthly_statistic + ', ' + datadict.element_name, 
                    //html:'Start Year: ' + datadict.start_date + ' End Year: ' + datadict.end_date,
                    style:{
                        //position:'absolute',
                        //top:'329px',
                        top:'0px',
                        left:'0px',
                        fontSize:'12px',
                        color:'#3E576F'
                    }
                }],
                style: {color: '#000000'}
            },
            legend:{
                enabled:false
            },
            xAxis: {
                labels:{
                    style: axesStyle,
                    step:2
                },
                title:{
                    style:axesStyle,
                    text:'Start Year: ' + datadict.start_date + ' End Year: ' + datadict.end_date,
                },
                categories: datadict.month_list.splice(datadict.month_list.length -1,0),
                plotLines:x_plotLines,
                //tickPositions:x_tickPositions,
                tickInterval:0,
                min:0.5,
                max:10.5
            },
            yAxis: {
                labels:{
                    style: axesStyle
                },
                title: {
                    style:titleStyle,
                    text: datadict.element_name
                },
                gridLineWidth:0,
                max:y_axis_props.axisMax,
                min:y_axis_props.axisMin,
                plotLines:y_axis_props.plotLines,
                tickPositions:y_tickPositions,
                //tickInterval:y_axis_props.tickInterval,
                startOnTick:false
            },
        
            tooltip: {
                crosshairs: true,
                shared: true
                //valueSuffix: 'in'
            },
            
            series: [{
                name: monthly_statistic +  ' of ' + datadict.element_name + ' ' + base_temperature,
                data: averages,
                zIndex: 1,
                marker: {
                    fillColor: 'white',
                    lineWidth: 1,
                    lineColor: Highcharts.getOptions().colors[0]
                }
            }, {
                name: 'Range',
                data: datadict.ranges,
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
