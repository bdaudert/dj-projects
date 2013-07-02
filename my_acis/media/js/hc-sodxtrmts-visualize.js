$(function () {
    var chart;

    $(document).ready(function() {
        var JSON_URL = document.getElementById("JSON_URL").value;
        var json_file = document.getElementById("json_file").value;
        var file = JSON_URL + json_file;
        var month_list_str = document.getElementById("months").value;
        var show_running_mean = document.getElementById("show_running_mean").value;
        var running_mean_years = document.getElementById("running_mean_years").value;
        //convert into javascript array
        var month_list = month_list_str.substring(1,month_list_str.length -1).split(",")
        for (var mon_idx=0;mon_idx<month_list.length;mon_idx++) {
            month_list[mon_idx] = parseInt(month_list[mon_idx]);
        }
        var summary = document.getElementById("summary").value;
        var month_names =  ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        $.getJSON(file, function(datadict) {
            var element = datadict.element;
            var stn_id = datadict.stn_id;
            //Depending on summary, define series to be plotted
            var series_data = [];
            var Start = Date.UTC(parseInt(datadict.start_date),0,01);
            var Interval = 365 * 24 * 3600000; // 1 year
            if (summary != 'individual'){
                var series = {'pointStart':Start,'pointInterval':Interval};
                //Define series name
                if (summary == 'max'){
                    series['name'] = 'Maximum of monthly values';
                }
                if (summary == 'min'){
                    series['name'] = 'Minimum of monthly values';
                }
                if (summary == 'sum'){
                    series['name'] = 'Sum of monthly values';
                }
                if (summary == 'mean'){
                    series['name'] = 'Mean of monthly values';
                }
                //Define series data
                var data = [];
                var values = [];
                for (var yr_idx=0;yr_idx<datadict.data.length - 6;yr_idx++) {
                    var vals = [];
                    for (var mon_idx=0;mon_idx<month_list.length;mon_idx++) {
                        var val = datadict.data[yr_idx][2*month_list[mon_idx] - 1];
                        if (val != '-----') {
                            vals.push(parseFloat(val));
                        }
                    }
                    if (vals.length > 0) {
                        if (summary == 'max'){
                            data.push([Date.UTC(parseInt(datadict.data[yr_idx][0]), 0, 1), Math.max.apply(Math,vals)]);
                            values.push(Math.max.apply(Math,vals));
                        }
                        if (summary == 'min'){
                            data.push([Date.UTC(parseInt(datadict.data[yr_idx][0]), 0, 1), precise_round(Math.min.apply(Math,vals),2)]);
                            values.push(precise_round(Math.min.apply(Math,vals),2));
                        }
                        if (summary == 'sum'){
                            for(var i=0,sum=0;i<vals.length;sum+=vals[i++]);
                            data.push([Date.UTC(parseInt(datadict.data[yr_idx][0]), 0, 1), precise_round(sum,2)]);
                            values.push = precise_round(sum,2);
                        }
                        if (summary == 'mean'){
                            for(var i=0,sum=0;i<vals.length;sum+=vals[i++]);
                            data.push([Date.UTC(parseInt(datadict.data[yr_idx][0]), 0, 1), precise_round(sum/vals.length,2)]);
                            values.push(precise_round(sum/vals.length,2));
                        }
                    }
                    else {
                        data.push([Date.UTC(parseInt(datadict.data[yr_idx][0]), 0, 1), null]);
                        values.push(null);
                    }
                } //end for yr_idx
                // Find max/min (needed to set plot properties)
                var data_max = Math.max.apply(Math,values);
                var data_min = Math.min.apply(Math,values);
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
                                running_mean_data.push([Date.UTC(parseInt(datadict.data[yr_idx][0]), month_idx, 1), precise_round(sum/cnt,2)]);
                            }
                            else{
                                running_mean_data.push([Date.UTC(parseInt(datadict.data[yr_idx][0]), month_idx, 1), null]);
                            }
                        }
                        else{
                            running_mean_data.push([Date.UTC(parseInt(datadict.data[yr_idx][0]), month_idx, 1), null]);
                        }
                    }
                    var series = {'pointStart':Date.UTC(parseInt(datadict.start_date),month_idx,01),'pointInterval':Interval};
                    series['name'] = running_mean_years.toString() + 'Year Running Mean';
                    series['data'] = running_mean_data;
                    series_data.push(series);
                }
            }
            else { //summary = indiviual
                for (var mon_idx=0;mon_idx<month_list.length;mon_idx++) {
                    var series = {'name':month_names[month_list[mon_idx]-1],'pointStart':Start,'pointInterval':Interval};
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
            var xAxisText = 'Months: ';
            if (summary != 'individual'){
                for (var mon in month_list) {
                    xAxisText+= month_names[parseInt(mon)] + '  '
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
                    renderTo: 'container'
                },
                title: {
                    text:  datadict.element_name
                },
                
                subtitle: {
                    //text: data_max + ', ' + data_min
                    text:datadict.stn_name + '(' + stn_id + ')'
                },
                credits: {
                        href: 'http://wrcc.dri.edu/',
                        text: 'wrcc.dri.edu'
                },
                xAxis: {
                    title : {
                        text: xAxisText
                    },
                    type: 'datetime',
                    maxZoom: 365 * 24 * 3600000, // 1 year
                    dateTimeLabelFormats: { // don't display the dummy year
                    year: '%Y'
                    }
                    /*
                    plotBands: [{
                    from: Date.UTC(parseInt(datadict.start_date),0,01),
                    to: Date.UTC(parseInt(datadict.end_date),0,01)
                    }],
                    */
                },
                yAxis: {
                    title: {
                        text: datadict.element_name
                    },
                    tickInterval:tickInterval,
                    startOnTick: false,
                    showFirstLabel: false
                },
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

