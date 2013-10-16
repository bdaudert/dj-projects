$(function () {
    var json_file = document.getElementById("json_file").value;
    var JSON_URL = document.getElementById("JSON_URL").value;
    var json_file_path = '/csc/media/tmp/' + json_file;
    var style_axes = {
            color:'#000000',
            fontSize:'14px',
            fontWeight: 'bold'
        };
    var style_text = {
            color:'#000000',
            fontSize:'18px'
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
        var x_plotlines = [];
        for (var val=0;val<12;val++){
            var plotline = {
                color: '#787878',
                dashStyle:'dash',
                width: 1,
                value: val,
            };
            x_plotlines.push(plotline);
        }
        var y_plotlines = [];
        for (var val=min + (max - min)/10;val<=max + 4*(max - min)/10;val+=(max - min)/10) {
            var plotline = {
                color: '#787878',
                dashStyle:'dash',
                width: 1,
                value: val,
            };
            y_plotlines.push(plotline);
        }
        if (y_plotlines.length == 0 ){
            y_plotlines = null;
        }
        if (max == null || min == null || Math.abs(max - min) < 0.0001){
            var tickInterval = null;
        }
        else {
            if (table_dict.element != 'pcpn' && table_dict.element != 'snow' && table_dict.element != 'snwd'){
                var tickInterval = precise_round((max - min)/10,0);
                //var tickInterval = null;
            }
            else {
                var tickInterval = precise_round((max - min)/10,1);
            }
        }

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
                    html:'Mean and Range of '  + monthly_statistic + ' for ' + table_dict.element_name, 
                    //html:'Start Year: ' + table_dict.start_date + ' End Year: ' + table_dict.end_date,
                    style:{
                        top:'-10px',
                        left:'100px',
                        fontSize:'14px'
                    }
                },
                {
                    html:'Start Year: ' + table_dict.start_date + ' End Year: ' + table_dict.end_date,
                    style:{
                        top:'292px',
                        left:'150px',
                        fontSize:'12px'
                    }
                }],
                style: {color: '#000000'}
            },
            xAxis: {
                labels:{
                    style: style_axes
                },   
                categories: table_dict.month_list,
                plotLines:x_plotlines
            },
            yAxis: {
                labels:{
                    style: style_axes
                },
                title: {
                    style:style_text,
                    text: table_dict.element_name
                },
                max:max,
                min:min,
                gridLineWidth:0,
                //tickPixelInterval:tickInterval,
                plotLines:y_plotlines
            },
        
            tooltip: {
                crosshairs: true,
                shared: true,
                valueSuffix: '°C'
            },
            
            //egend: {
            //},
        
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
