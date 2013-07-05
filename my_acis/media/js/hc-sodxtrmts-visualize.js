$(function () {
    var chart;

    $(document).ready(function() {
        var JSON_URL = document.getElementById("JSON_URL").value;
        var json_file = document.getElementById("json_file").value;
        var file = JSON_URL + json_file;
        var month_list_str = document.getElementById("months").value;
        var show_running_mean = document.getElementById("show_running_mean").value;
        var running_mean_years = document.getElementById("running_mean_years").value;
        var graph_title = document.getElementById("graph_title").value;
        var major_grid = document.getElementById("major_grid").value;
        var minor_grid = document.getElementById("minor_grid").value;
        var connector_line = document.getElementById("connector_line").value;
        var connector_line_width = document.getElementById("connector_line_width").value;
        if (connector_line == 'F'){
            connector_line_width = 0;        
        }
        var markers = document.getElementById("markers").value;
        var marker_type = document.getElementById("marker_type").value;
        //convert into javascript array
        var month_list = month_list_str.substring(1,month_list_str.length -1).split(",")
        for (var mon_idx=0;mon_idx<month_list.length;mon_idx++) {
            month_list[mon_idx] = parseInt(month_list[mon_idx]);
        }
        var summary = document.getElementById("summary").value;
        var month_names =  ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        var style_axes = {
                color:'#000000',
                fontSize:'14px',
                fontWeight: 'bold'
            };
        var style_text = {
                color:'#000000',
                fontSize:'18px'
            };
        $.getJSON(file, function(datadict) {
            var element = datadict.element;
            var stn_id = datadict.stn_id;
            //Depending on summary, define series to be plotted
            var series_data = [];
            var Start = Date.UTC(parseInt(datadict.start_date),0,01);
            var Interval = 365 * 24 * 3600000; // 1 year
            var x_plotlines = [];
            var y_plotlines = [];
            if (summary != 'individual'){
                var series = {'pointStart':Start,'pointInterval':Interval, marker:{symbol:marker_type}, lineWidth:connector_line_width};
                if (markers == 'F'){
                    series['marker'] = {enabled:false}
                }
                //Define series name
                if (summary == 'max'){
                    series['name'] = 'Maximum over the months';
                }
                if (summary == 'min'){
                    series['name'] = 'Minimum over the months';
                }
                if (summary == 'sum'){
                    series['name'] = 'Sum over the months';
                }
                if (summary == 'mean'){
                    series['name'] = 'Average over the months';
                }
                series['color'] = '#00008B';
                //Define series data
                var data = [];
                var values = [];
                //Find end year index 
                if (month_list[0]> month_list[month_list.length -1]){
                    var end_idx = 7
                }
                else {
                    var end_idx = 6
                } 
                for (var yr_idx=0;yr_idx<datadict.data.length - end_idx;yr_idx++) {
                    //Add vertical plot lines every 10 years or every year
                    if (major_grid =='T'){
                        if (parseInt(datadict.data[yr_idx][0])%10 == 0 && yr_idx > 0){
                            var plotline = {
                                color: '#787878',
                                dashStyle:'dash',
                                width: 1,
                                value: Date.UTC(parseInt(datadict.data[yr_idx][0]), 0, 1),
                            };
                            x_plotlines.push(plotline);
                        }
                    }
                    if (minor_grid =='T'){
                        //leave cluncy code in case we want differnent minor grid
                        if (parseInt(datadict.data[yr_idx][0])%5 == 0 && yr_idx > 0){
                            var plotline = {
                                color: '#787878',
                                dashStyle:'dash',
                                width: 0.5,
                                value: Date.UTC(parseInt(datadict.data[yr_idx][0]), 0, 1),
                            };
                            x_plotlines.push(plotline);
                        }
                    } 
                    if (major_grid =='F' && minor_grid =='F'){
                        x_plotlines = null;
                    }
                    var vals = [];
                    //Define plot data 
                    if (month_list[0]> month_list[month_list.length -1]){
                        var date = Date.UTC(parseInt(datadict.data[yr_idx][0]) + 1, 0, 1)
                    }
                    else {
                        var date = Date.UTC(parseInt(datadict.data[yr_idx][0]), 0, 1)
                    } 
                    for (var mon_idx=0;mon_idx<month_list.length;mon_idx++) {
                        var val = datadict.data[yr_idx][2*month_list[mon_idx] - 1];
                        if (val != '-----') {
                            vals.push(parseFloat(val));
                        }
                    }
                    if (vals.length > 0) {
                        if (summary == 'max'){
                            data.push([date, Math.max.apply(Math,vals)]);
                            values.push(Math.max.apply(Math,vals));
                        }
                        if (summary == 'min'){
                            data.push([date, precise_round(Math.min.apply(Math,vals),2)]);
                            values.push(precise_round(Math.min.apply(Math,vals),2));
                        }
                        if (summary == 'sum'){
                            for(var i=0,sum=0;i<vals.length;sum+=vals[i++]);
                            data.push([date, precise_round(sum,2)]);
                            values.push = precise_round(sum,2);
                        }
                        if (summary == 'mean'){
                            for(var i=0,sum=0;i<vals.length;sum+=vals[i++]);
                            data.push([date, precise_round(sum/vals.length,2)]);
                            values.push(precise_round(sum/vals.length,2));
                        }
                    }
                    else {
                        data.push([date, null]);
                        values.push(null);
                    }
                } //end for yr_idx
                // Find max/min (needed to set plot properties)
                var data_max = Math.max.apply(Math,values);
                if (datadict.element == 'pcpn' || datadict.element == 'snow' || datadict.element == 'snwd' || datadict.element == 'wdmv' || datadict.element == 'evap'){
                    var data_min = 0;
                }
                else{
                    var data_min = Math.min.apply(Math,values);
                }
                //Define y_plotlines
                if (major_grid =='T'){
                    for (var val=data_min + (data_max - data_min)/5;val<=data_max + 4*(data_max - data_min)/5;val+=(data_max - data_min)/5) {
                        var plotline = {
                            color: '#787878',
                            dashStyle:'dash',
                            width: 1,
                            value: val,
                            };
                            y_plotlines.push(plotline);
                    }
                }
                if (minor_grid =='T'){
                    for (var val=data_min + (data_max - data_min)/10;val<=data_max + 4*(data_max - data_min)/10;val+=(data_max - data_min)/10) {
                        var plotline = {
                            color: '#787878',
                            dashStyle:'dash',
                            width: 0.5,
                            value: val,
                            };
                            y_plotlines.push(plotline);
                    }
                }
                if (major_grid =='F' && minor_grid =='F'){
                    y_plotlines = null;
                }
                series['data'] = data;
                series_data.push(series);
                //Running Mean
                if (show_running_mean == 'T'){
                    var running_mean_data = [];
                    if (running_mean_years%2 == 0){
                        var num_nulls =running_mean_years/2 - 1;
                        var month_idx = 5;
                    }
                    else{
                        var num_nulls =(running_mean_years - 1)/2;
                        var month_idx = 0;
                    }
                    for (var yr_idx=0;yr_idx<values.length;yr_idx++) {
                        if (month_list[0]> month_list[month_list.length -1]){
                            var date = Date.UTC(parseInt(datadict.data[yr_idx][0]) + 1, mon_idx, 1)
                        }
                        else {
                            var date = Date.UTC(parseInt(datadict.data[yr_idx][0]), mon_idx, 1)
                        }
                        if (yr_idx >= num_nulls &&  yr_idx <= values.length - 1 - num_nulls) {
                            //for(var i=yr_idx - num_nulls,sum=0;i<=yr_idx + num_nulls;sum+=values[i++]);
                            var cnt = 0;
                            for(var i=yr_idx - num_nulls,sum=0;i<=yr_idx + num_nulls;i++){
                                if (values[i] != null){
                                    sum+=values[i];
                                    cnt+=1;
                                }
                            }
                            if (cnt > 0){
                                running_mean_data.push([date, precise_round(sum/cnt,2)]);
                            }
                            else{
                                running_mean_data.push([date, null]);
                            }
                        }
                        else{
                            running_mean_data.push([date, null]);
                        }
                    }
                    var series = {'pointStart':Date.UTC(parseInt(datadict.start_date),month_idx,01),'pointInterval':Interval,marker:{symbol:marker_type}};
                    series['name'] = running_mean_years.toString() + 'Year Running Mean';
                    series['data'] = running_mean_data;
                    series['color'] = 'red';
                    series['marker'] = {enabled:false}
                    series_data.push(series);
                }
            }
            else { //summary = indiviual
                for (var mon_idx=0;mon_idx<month_list.length;mon_idx++) {
                    var series = {'name':month_names[month_list[mon_idx]-1],'pointStart':Start,'pointInterval':Interval,marker:{symbol:marker_type}};
                    if (markers == 'F'){
                        series['marker'] = {enabled:false}
                    }
                    var data =  [];
                    var values = [];
                    for (var yr_idx=0;yr_idx<datadict.data.length - 6;yr_idx++) {
                        var val = datadict.data[yr_idx][2*month_list[mon_idx] - 1]
                        if (val != '-----') {
                            values.push(precise_round(parseFloat(val),2));
                            data.push([Date.UTC(parseInt(datadict.data[yr_idx][0]), 0, 1), precise_round(parseFloat(val),2)]);
                        }
                        else {
                            values.push(null);
                            data.push([Date.UTC(parseInt(datadict.data[yr_idx][0]), 0, 1),null]); 
                        }
                    }
                    series['data'] =  data;
                    series_data.push(series);
                    //Find max/min of data (needed to set plot properties)
                    if (mon_idx == 0){
                        var data_max = Math.max.apply(Math,values);
                        var data_min = Math.min.apply(Math,values);
                    }
                    else{
                        max = Math.max.apply(Math,values);
                        min = Math.min.apply(Math,values);
                        if (max > data_max){
                            data_max = max;
                        }
                    if (min < data_min){
                            data_min = min;
                        }
                    }
                }
            }

            //Define plot characteristics
            if (graph_title == "Use default"){
                graph_title = datadict.stn_name + '(' + stn_id + ')';
            }
            if (major_grid == 'F') {
                var lineColor = 'transparent';
                var minorGridLineColor ='transparent';
                var gridLineWidth = 0;
                var gridLineColor = 'transparent';
            }
            else {
                var lineColor = '#C0D0E0';
                var minorGridLineColor = '#E0E0E0';
                var gridLineWidth = 1;
                var gridLineColor = '#C0C0C0';
            }
            var xAxisText = 'Months: ';
            if (month_list[0]> month_list[month_list.length -1]){
                var apdx = 'Ending Year ' //+ datadict.data[datadict.data.length -8][0]
            }
            else {
                var apdx = 'Year ' //+ datadict.data[datadict.data.length -7][0]
            }
            if (summary != 'individual'){
                for (var mon_idx=0;mon_idx<month_list.length;mon_idx++)  {
                    xAxisText+= month_names[month_list[mon_idx] - 1] + ' ' 
                }
            }
            if (data_max == null || data_min == null){
                var tickInterval = null;
            }
            else if (Math.abs(data_max - data_min) < 0.001){
                var tickInterval = null;
            } 
            else {
                //var tickInterval = precise_round((data_max - data_min)/10, 1);
                var tickInterval = null;
            }
            //Define Chart
            chart = new Highcharts.Chart({
                chart: {
                    type:'line',
                    borderColor:'#006666',
                    borderWidth: 2,
                    renderTo: 'container',
                    //marginLeft: 60,
                    marginBottom: 100,
                    marginRigh:0 
                },
                title: {
                    style:style_text,
                    text: graph_title
                },
                subtitle: {
                    text:xAxisText,
                    style: {
                        color:'#0000FF',
                        fontSize:15
                    }
                },
                credits: {
                        href: 'http://wrcc.dri.edu/',
                        text: 'wrcc.dri.edu'
                },
                xAxis: [
                    {
                        title : {
                            style:style_text,
                            text: apdx
                        },
                        labels: {
                            style:style_axes
                        },
                        lineColor:lineColor,
                        plotLines:x_plotlines,
                        gridLineWidth: gridLineWidth,
                        gridLineColor: gridLineColor,
                        type: 'datetime',
                        maxZoom: 365 * 24 * 3600000, // 1 year
                        dateTimeLabelFormats: { // don't display the dummy year
                            year: '%Y'
                        },
                    }
                    /*
                    {
                        opposite: true,
                        linkedTo: 0,
                        labels: {
                            style:style_axes
                        },
                        plotLines:x_plotlines,
                        gridLineWidth: gridLineWidth,
                        gridLineColor: gridLineColor,
                        type: 'datetime',
                        maxZoom: 365 * 24 * 3600000, // 1 year
                        dateTimeLabelFormats: { // don't display the dummy year
                            year: '%Y'
                        }
                    }*/
                    ],
                yAxis: [
                    {
                        title: {
                            style:style_text,
                            text: datadict.element_name
                        },
                        labels: {
                            style:style_axes
                        },
                        gridLineWidth:0,
                        gridLineColor: gridLineColor,
                        lineColor:lineColor,
                        plotLines:y_plotlines,
                        minorGridLineColor:minorGridLineColor,
                        tickInterval:tickInterval,
                        startOnTick: false,
                        showFirstLabel: false
                    },
                    {
                        opposite: true,
                        linkedTo: 0,
                        title: {
                            style:style_text,
                            text: ' ' 
                        },
                        labels: {
                            style:style_axes
                        },
                        gridLineWidth:0,
                        gridLineColor: gridLineColor,
                        lineColor:lineColor,
                        plotLines:y_plotlines,
                        minorGridLineColor:minorGridLineColor,
                        tickInterval:tickInterval,
                        startOnTick: false,
                        showFirstLabel: false
                    }],
                tooltip: {
                    shared: true
                },
                legend: {
                    enabled: true
                    //verticalAlign:'top'
                },
                series:series_data 
            });//end chart
        });//end getJSON
    });//end document ready function
    
});//end top function

