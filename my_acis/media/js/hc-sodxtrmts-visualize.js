$(function () {
    var chart;

    $(document).ready(function() {
        var JSON_URL = document.getElementById("JSON_URL").value;
        var json_file = document.getElementById("json_file").value;
        var file = JSON_URL + json_file;
        var start_month = document.getElementById("start_month").value;
        var end_month = document.getElementById("end_month").value;
        var summary = document.getElementById("summary").value;
        var month_names =  ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        $.getJSON(file, function(datadict) {
            var element = datadict.element;
            var stn_id = datadict.stn_id;
            //Given user input, define data to be plotted
            var series_data = [];
            //Find the approprate indices holding monthly data in datadict
            //datadict.data =[[year, month_1_val, flag, month_2_val, flag ...]]
            var start_index = 2 * parseInt(start_month) - 1;
            var end_index = 2 * parseInt(end_month) - 1;
            var index = start_index;
            var month_index =  parseInt(start_month) - 1;
            var indices = [start_index];
            var months = [month_names[parseInt(start_month) - 1]];
            while (index != end_index){
                index = index + 2;
                month_index = month_index + 1;
                if (index == 25){
                    index = 1;
                    month_index = 0;
                }
                indices.push(index);
                months.push(month_names[month_index]);
            }
            //Depending on summary, define series to be plotted
            var Type = 'area';
            var Start = Date.UTC(parseInt(datadict.start_date),0,01);
            var Interval = 365 * 24 * 3600000; // 1 year
            if (summary != 'individual'){
                var series = {'type':Type, 'pointStart':Start,'pointInterval':Interval};
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
                for (var yr_idx=0;yr_idx<datadict.data.length - 6;yr_idx++) {
                    var vals = [];
                    for (var mon_idx=0;mon_idx<indices.length;mon_idx++) {
                        var val = datadict.data[yr_idx][indices[mon_idx]];
                        if (val != '-----') {
                            vals.push(parseFloat(val));
                        }
                    }
                    if (vals) {
                        if (summary == 'max'){
                            data.push(Math.max.apply(Math,vals));
                        }
                        if (summary == 'min'){
                            data.push(precise_round(Math.min.apply(Math,vals),2));
                        }
                        if (summary == 'sum'){
                            for(var i=0,sum=0;i<vals.length;sum+=vals[i++]);
                            data.push(precise_round(sum,2));
                        }
                        if (summary == 'mean'){
                            for(var i=0,sum=0;i<vals.length;sum+=vals[i++]);
                            data.push(precise_round(sum/vals.length,2));
                        }
                    }
                    else {
                        data.push(null);
                    }    
                } //end for yr_idx
                series['data'] = data;
                series_data.push(series);
            }
            else { //summary = indiviual
                for (var mon_idx=0;mon_idx<indices.length;mon_idx++) {
                    var series = {'name':months[mon_idx],'type':Type,'pointStart':Start,'pointInterval':Interval, 'fillOpacity':'0.05'};
                    var data =  [];
                    for (var yr_idx=0;yr_idx<datadict.data.length - 6;yr_idx++) {
                        var val = datadict.data[yr_idx][indices[mon_idx]]
                        if (val != '-----') {
                            data.push(precise_round(parseFloat(val),2));
                        }
                        else {
                            data.push(null);
                        }
                    }
                    series['data'] =  data;
                    series_data.push(series);
                }
            }

            //Define Chart
            chart = new Highcharts.Chart({
                chart: {
                    renderTo: 'container',
                    zoomType: 'x',
                    spacingRight: 20
                },
                title: {
                    text:  datadict.element_name
                },
                subtitle: {
                    text: document.ontouchstart === undefined ?
                        'Click and drag in the plot area to zoom in' :
                        'Drag your finger over the plot to zoom in'
                },
                credits: {
                        href: 'http://wrcc.dri.edu/',
                        text: 'wrcc.dri.edu'
                },
                xAxis: {
                    title : {
                        text: 'Time Period: ' + start_month + ' - ' + end_month
                    },
                    type: 'datetime',
                    maxZoom: 365 * 24 * 3600000, // 1 year
                    plotBands: [{
                    from: Date.UTC(parseInt(datadict.start_date),0,01),
                    to: Date.UTC(parseInt(datadict.end_date),0,01)
                    }],
                },
                yAxis: {
                    title: {
                        text: datadict.element_name
                    },
                    startOnTick: false,
                    showFirstLabel: false
                },
                tooltip: {
                    shared: true
                },
                legend: {
                    enabled: true
                },
                plotOptions: {
                    area: {
                        /*
                        fillColor: {
                            linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
                            stops: [
                                [0, Highcharts.getOptions().colors[0]],
                                [1, 'rgba(2,0,0,0)']
                            ]
                        },
                        */
                        lineWidth: 1,
                        marker: {
                            enabled: false,
                            states: {
                                hover: {
                                    enabled: true,
                                    radius: 5
                                }
                            }
                        },
                        shadow: false,
                        states: {
                            hover: {
                                lineWidth: 1
                            }
                        }
                    }
                },
                series:series_data 
            });//end chart
        });//end getJSON
    });//end document ready function
    
});//end top function

