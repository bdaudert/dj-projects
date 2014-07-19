$(function () {
    $(document).ready(function() {
        var json_file = document.getElementById("json_file").value;
        var TMP_URL = document.getElementById("TMP_URL").value;
        var json_file_path = TMP_URL + json_file;
        var xCats = ['Jan',
                    'Feb',
                    'Mar',
                    'Apr',
                    'May',
                    'Jun',
                    'Jul',
                    'Aug',
                    'Sep',
                    'Oct',
                    'Nov',
                    'Dec'];
        $.getJSON(json_file_path, function(datadict) {
            for (var i=0;i<datadict.length;i++){
                //Find max/min values of data
                var max = null;
                var min = null;
                if (datadict[i].data){
                    max = Math.max.apply(Math,datadict[i].data);
                    min = Math.min.apply(Math,datadict[i].data);
                }
                //Horizontal Plotlines
                var y_axis_props = set_axis_properties(max,'Use default', min, 'Use default',datadict[i].element,'mave','F',10.0);
                //Define element dependent vars like y-axis max, min, plot-color
                var p_color = set_plot_color(datadict[i].element);
                var j = i + 1
                var cntr = 'container' + j
                //Default BarChart
                var ChartClass = new BarChart(xCats); 
                //Extension to default BarChart
                var Chart;            
                Chart = {
                    chartContent: cntr,
                    options: {
                        title: {
                            text:datadict[i].stn_name + ', ' + datadict[i].stn_id + ', ' + datadict[i].state
                        },
                        subtitle: {
                            text: 'Date Range ' + datadict[i].record_start  + ' - '+ datadict[i].record_end
                        },
                        yAxis: {
                            min: min,
                            max: max,
                            gridLineWidth:0,
                            max:y_axis_props.axisMax,
                            min:y_axis_props.axisMin,
                            plotLines:y_axis_props.plotLines,
                            //tickInterval:precise_round((max - min)/5, 0),
                            title: {
                                text: datadict[i].unit
                            }
                        },
                        series: [{
                            name: ' Monthly Averages: ' + datadict[i].element_long,
                            color: p_color,
                            data: datadict[i].data
                        }]
                    },
                };
                //Merge Default BarChart class withn Chart
                Chart= jQuery.extend(true, {}, ChartClass.defaultChart, Chart);
                Chart.init(Chart.options);
                Chart.create();
            }; //endfor
        }); //end getJSON
    }); // end doc ready
});//end top function
