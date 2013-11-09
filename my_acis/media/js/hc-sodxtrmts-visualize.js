$(function () {
    var chart;
    $(document).ready(function() {
        var mischr = ["fake","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"];
        var month_names =  ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        var JSON_URL = document.getElementById("JSON_URL").value;
        var json_file = document.getElementById("json_file").value;
        $.getJSON('/csc/media/tmp/' + json_file, function(datadict) {
            var initial = datadict.initial;
            var initial_graph = datadict.initial_graph;
            //Graph Options
            var summary = initial_graph.graph_summary;
            var show_running_mean = initial_graph.graph_show_running_mean;
            var running_mean_years = initial_graph.graph_running_mean_years;
            var plot_incomplete_years = initial_graph.graph_plot_incomplete_years;
            //Plot Options
            var graph_title = initial_graph.graph_title;
            var major_grid = initial_graph.major_grid;
            var minor_grid = initial_graph.minor_grid
            var connector_line = initial_graph.connector_line;
            var connector_line_width = parseInt(initial_graph.connector_line_width);
            var markers = initial_graph.markers;
            var marker_type = initial_graph.marker_type;
            var vertical_axis_min = initial_graph.vertical_axis_min;
            var vertical_axis_max = initial_graph.vertical_axis_max;
            var image_height = initial_graph.image_height;
            var month_list = [];
            for (mon = parseInt(initial_graph.graph_start_month);mon<=parseInt(initial_graph.graph_end_month);mon++)
                month_list.push(mon);

            if (connector_line == 'F'){
                connector_line_width = 0;
            }

            //set postion of network info label
            var top_dist = set_label_position(image_height);
            var axesStyle = set_AxesStyle();
            var titleStyle = set_TitleStyle();
            var subtitleStyle = set_SubtitleStyle();
            //Define Summary Text
            if (summary == 'max'){
                var SummaryText = 'Maximum';
            }
            if (summary == 'min'){
                var SummaryText = 'Minimum';
            }
            if (summary == 'sum'){
                var SummaryText = 'Sum';
            }
            if (summary == 'mean'){
                var SummaryText = 'Average';
            }
            if (summary == 'individual'){
                var SummaryText = ' ';
            }

            var max_missing_days = parseInt(datadict.search_params.max_missing_days);
            //Depending on summary, define series to be plotted
            //Find start end end index
            var yr_start_idx = 0;
            var yr_end_idx = datadict.data.length;
            if (initial_graph.graph_start_year.toLowerCase() !='por'){
                yr_start_idx = parseInt(initial_graph.graph_start_year) - parseInt(datadict.start_date);
            }
            if (initial_graph.graph_end_year.toLowerCase() !='por'){
                yr_end_idx = yr_end_idx - (datadict.end_date - parseInt(initial_graph.graph_end_year));
            }

            var series_data = [];
            var Start = Date.UTC(parseInt(datadict.data[yr_start_idx][0]),0,01);
            var Interval = 365 * 24 * 3600000; // 1 year
            //Case 1 Plot: summary over Months
            if (summary != 'individual'){
                var series = {'pointStart':Start,'pointInterval':Interval, marker:{symbol:marker_type}, lineWidth:connector_line_width};
                if (markers == 'F'){
                    series['marker'] = {enabled:false}
                }
                //Define series name
                series['name'] = SummaryText;
                series['color'] = '#00008B';
                //Define series data
                var data = [];
                var acis_data = [];
                var values = [];
                //Find end year index --> omit table (mean, skew...) summaries at end of array 
                if (month_list[0]> month_list[month_list.length -1]){
                    //first month > last
                    var end_idx = 7;
                }
                else {
                    var end_idx = 6;
                }
                //Define plot data
                for (var yr_idx=yr_start_idx;yr_idx<yr_end_idx - end_idx;yr_idx++) {
                    var vals = [];
                    var skip_year = 'F';                    
                    if (month_list[0]> month_list[month_list.length -1]){
                        var date = Date.UTC(parseInt(datadict.data[yr_idx][0]) + 1, 0, 1)
                        var acis_date = parseInt(datadict.data[yr_idx][0]);
                    }
                    else {
                        var date = Date.UTC(parseInt(datadict.data[yr_idx][0]), 0, 1)
                        var acis_date = parseInt(datadict.data[yr_idx][0]);
                    }
                    //Month Loop
                    for (var mon_idx=0;mon_idx<month_list.length;mon_idx++) {
                        var val = datadict.data[yr_idx][2*month_list[mon_idx] - 1];
                        var flag = datadict.data[yr_idx][2*month_list[mon_idx]].toString();
                        //Check if we need to skip this year
                        if ((mischr.indexOf(flag) > max_missing_days || val == '-----') && plot_incomplete_years == 'F') {
                            skip_year = 'T';
                            break;
                        }
            
                        if (val != '-----') {
                            vals.push(parseFloat(val));
                        }
                    } //end month loop
                    if (skip_year == 'T'){
                        data.push([date, null]);
                        acis_data.push([acis_date,null]);
                        //values.push(null);
                        continue;
                    }
                    if (vals.length > 0) {
                        if (summary == 'max'){
                            data.push([date, Math.max.apply(Math,vals)]);
                            acis_data.push([acis_date, Math.max.apply(Math,vals)]);
                            values.push(Math.max.apply(Math,vals));
                        }
                        if (summary == 'min'){
                            data.push([date, precise_round(Math.min.apply(Math,vals),2)]);
                            acis_data.push([acis_date, precise_round(Math.min.apply(Math,vals),2)]);
                            values.push(precise_round(Math.min.apply(Math,vals),2));
                        }
                        if (summary == 'sum'){
                            for(var i=0,sum=0;i<vals.length;sum+=vals[i++]);
                            data.push([date, precise_round(sum,2)]);
                            acis_data.push([acis_date, precise_round(sum,2)]);
                            values.push(precise_round(sum,2));
                        }
                        if (summary == 'mean'){
                            for(var i=0,sum=0;i<vals.length;sum+=vals[i++]);
                            data.push([date, precise_round(sum/vals.length,2)]);
                            acis_data.push([acis_date, precise_round(sum/vals.length,2)]);
                            values.push(precise_round(sum/vals.length,2));
                        }
                    }
                    else {
                        data.push([date, null]);
                        acis_data.push([acis_date, null]);
                        //values.push(null);
                    }
                } //end for yr_idx
                series['data'] = data;
                series_data.push(series);
                // Find max/min (needed to set plot properties)
                data_max = 0;
                data_min = 0;
                if (values.length > 0){
                    var data_max = find_max(values,datadict.element,datadict.search_params.monthly_statistic);
                    var data_min = find_min(values,datadict.element,datadict.search_params.monthly_statistic);
                    if (vertical_axis_max != "Use default") { 
                        try{
                            var data_max = parseFloat(vertical_axis_max);
                        }
                        catch(e){}
                    }
                    if (vertical_axis_min != "Use default") {                                                                                                   
                        try{
                            var data_min = parseFloat(vertical_axis_min);
                        }
                        catch(e){}
                    }
                }
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
                        skip_year = 'F';
                        if (month_list[0]> month_list[month_list.length -1]){
                            var date = Date.UTC(parseInt(datadict.data[yr_idx + yr_start_idx][0]) + 1, mon_idx, 1)
                        }
                        else {
                            var date = Date.UTC(parseInt(datadict.data[yr_idx + yr_start_idx][0]), mon_idx, 1)
                        }
                        if (yr_idx >= num_nulls &&  yr_idx <= values.length - 1 - num_nulls) {
                            //for(var i=yr_idx - num_nulls,sum=0;i<=yr_idx + num_nulls;sum+=values[i++]);
                            var cnt = 0;
                            for(var i=yr_idx - num_nulls,sum=0;i<=yr_idx + num_nulls;i++){
                                if (values[i] != null){
                                    sum+=values[i];
                                    cnt+=1;
                                }
                                else {
                                    skip_year = 'T';
                                    break;
                                }
                            }
                            if (cnt > 0 && skip_year =='F'){
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
                    series['name'] = running_mean_years.toString() + '-Year Running Mean';
                    series['data'] = running_mean_data;
                    series['color'] = 'red';
                    series['marker'] = {enabled:false}
                    series_data.push(series);
                }
            }
            else { //Case2: Plot indiviual months
                for (var mon_idx=0;mon_idx<month_list.length;mon_idx++) {
                    var series = {'name':month_names[month_list[mon_idx]-1],'pointStart':Start,'pointInterval':Interval,marker:{symbol:marker_type}};
                    if (markers == 'F'){
                        series['marker'] = {enabled:false}
                    }
                    var data =  [];
                    var acis_data = [];
                    var values = [];
                    for (var yr_idx=yr_start_idx;yr_idx<yr_end_idx - 6;yr_idx++) {
                        var val = datadict.data[yr_idx][2*month_list[mon_idx] - 1]
                        if (val != '-----') {
                            values.push(precise_round(parseFloat(val),2));
                            data.push([Date.UTC(parseInt(datadict.data[yr_idx][0]), 0, 1), precise_round(parseFloat(val),2)]);
                            if (mon_idx ==0){
                                acis_data.push([parseInt(datadict.data[yr_idx][0]), precise_round(parseFloat(val),2)]);
                            }
                        }
                        else {
                            values.push(null);
                            data.push([Date.UTC(parseInt(datadict.data[yr_idx][0]), 0, 1),null]);
                            if (mon_idx == 0){ 
                                acis_data.push([parseInt(datadict.data[yr_idx][0]),null]);
                            }
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
                        var max = Math.max.apply(Math,values);
                        var min = Math.min.apply(Math,values);
                        if (max > data_max){
                            data_max = max;
                        }
                        if (min < data_min){
                            data_min = min;
                        }
                    }
                }
                // Override max/min if needed
                if (vertical_axis_max != "Use default") {
                    try{
                        var data_max = parseFloat(vertical_axis_max);
                    }
                    catch(e){}
                }
                if (vertical_axis_min != "Use default"){
                    try {
                        var data_min = parseFloat(vertical_axis_min);
                    }
                    catch(e){}
                }
            }

            //Define plot characteristics
            //Define x_plotlines
            //Sets new data for plotting,minor,major plotlines
            var pls = [];
            var x_plotlines = [];
            var x_tickPositions = [];
            var dmm = set_yr_plotlines(acis_data);
            var yr_step = 1;
            if (minor_grid =='T'){
                pls = dmm.plotlines_minor;
                var yr_step = 2;
            }
            else if (major_grid =='T' && minor_grid == 'F'){
                pls = dmm.plotlines_major;
            }
            else {
                pls = dmm.plotlines_major;
            }
            //convert to Date
            for (var pl_idx=0;pl_idx<pls.length;pl_idx++) {
                var pl ={};
                for (var key in pls[pl_idx]){
                    pl[key] = pls[pl_idx][key];
                }
                pl.value = Date.UTC(pls[pl_idx].value,0,1);
                if (major_grid =='F' && minor_grid == 'F'){
                    if (pl_idx ==0 || pl_idx == pls.length -1){
                        x_plotlines.push(pl);
                    }
                }
                else {
                    x_plotlines.push(pl);
                }
                x_tickPositions.push(pl.value);
            }
            var x_min = Date.UTC(dmm.new_data[0][0],0,1);
            var x_max = Date.UTC(dmm.new_data[dmm.new_data.length -1][0],0,1);
            //Define y_plotlines and tickInterval
            var y_plotlines = [];
            var plotline_no = x_plotlines.length;
            /*
            if (major_grid =='F' && minor_grid == 'F'){
                var plotline_no  = 1.0;
            }
            else if (minor_grid =='T'){
                //var plotline_no = 10.0;
                var plotline_no = x_plotlines.length;
            }
            else if (major_grid =='T' && minor_grid == 'F'){
                //var plotline_no = 5.0;
                var plotline_no = x_plotlines.length;
            }
            */
            var y_axis_props = set_axis_properties(data_max, data_min, datadict.element,datadict.search_params.monthly_statistic,plotline_no);
            var y_tickPositions = align_ticks(y_axis_props.plotLines);
            if (graph_title == "Use default"){
                graph_title = datadict.stn_name + ', ' + datadict.stn_state + '<br />';
            }
            if (major_grid == 'F' && minor_grid == 'F') {
                var lineColor = 'transparent';
                var minorGridLineColor ='transparent';
                var gridLineWidth = 0;
                var gridLineColor = 'transparent';
            }
            else {
                var lineColor = '#C0D0E0';
                var minorGridLineColor = '#E0E0E0';
                var gridLineWidth = 0;
                var gridLineColor = '#C0C0C0';
            }
            var xAxisText = SummaryText + '  ' +  datadict.element_name + ', Months: ' + 
                month_names[month_list[0] - 1] + ' - '+ month_names[month_list[month_list.length - 1] - 1]; 
            if (month_list[0]> month_list[month_list.length -1]){
                var apdx = 'Ending Year ' //+ datadict.data[datadict.data.length -8][0]
            }
            else {
                var apdx = 'Year ' //+ datadict.data[datadict.data.length -7][0]
            }
            //Define Chart
            chart = new Highcharts.Chart({
                chart: {
                    type:'line',
                    borderColor:'#006666',
                    borderWidth: 2,
                    //plotBorderColor: '#787878',
                    //plotBorderWidth: 0.5,
                    renderTo: 'container',
                    //marginLeft: 60,
                    marginBottom: 100,
                    marginRigh:0 
                },
                title: {
                    style:titleStyle,
                    text: graph_title
                },
                subtitle: {
                    text:xAxisText,
                    //text:'Network: ' + datadict.stn_network + ', ID: ' + datadict.stn_id,
                    style: subtitleStyle        
                },
                labels: {
                    items:[{
                        html:'Network: ' + datadict.stn_network + ', ID: ' + datadict.stn_id,
                        style:{
                            position:'absolute',
                            margin:'0px',
                            top:top_dist,
                            left:'0px',
                            fontSize:'12px',
                            color:'#3E576F'
                        }   
                    }],
                    style: {color: '#000000'}
                },
                credits: {
                        href: 'http://wrcc.dri.edu/',
                        text: 'wrcc.dri.edu'
                },
                xAxis: [
                    {
                        title : {
                            style:titleStyle,
                            text: apdx
                        },
                        
                        labels: {
                            formatter: function () {
                                return Highcharts.dateFormat('%Y', this.value);
                            },
                            //rotation:-90,
                            style:axesStyle,
                            step:yr_step
                        },
                        offset:2,
                        min:x_min,
                        max:x_max,
                        showLastLabel:true,
                        showFirstLabel:true,
                        lineColor:lineColor,
                        plotLines:x_plotlines,
                        tickPositions:x_tickPositions,
                        //endOnTick:true,
                        gridLineWidth: gridLineWidth,
                        gridLineColor: gridLineColor,
                        type: 'datetime',
                        dateTimeLabelFormats: { // don't display the dummy year
                            year: '%Y'
                        },
                    }
                    ],
                yAxis: [
                    {
                        title: {
                            style:titleStyle,
                            text: datadict.element_name
                        },
                        labels: {
                            style:axesStyle
                        },
                        min:y_axis_props.axisMin,
                        max:y_axis_props.axisMax,
                        gridLineWidth:0,
                        gridLineColor: gridLineColor,
                        lineColor:lineColor,
                        plotLines:y_axis_props.plotLines,
                        tickPositions:y_tickPositions,
                        minorGridLineColor:minorGridLineColor,
                        //tickInterval:y_axis_props.tickInterval,
                        startOnTick: false,
                        showFirstLabel: true
                    },
                    {
                        opposite: true,
                        linkedTo: 0,
                        title: {
                            style:titleStyle,
                            text: ' ' 
                        },
                        labels: {
                            style:axesStyle
                        },
                        min:y_axis_props.axisMin,
                        max:y_axis_props.axisMax,
                        gridLineWidth:0,
                        gridLineColor: gridLineColor,
                        lineColor:lineColor,
                        plotLines:y_axis_props.plotLines,
                        tickPositions:y_tickPositions,
                        minorGridLineColor:minorGridLineColor,
                        //tickInterval:y_axis_props.tickInterval,
                        startOnTick: false,
                        showFirstLabel: true
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

