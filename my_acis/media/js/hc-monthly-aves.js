$(function () {
    $(document).ready(function() {
        var json_file = document.getElementById("json_file").value;
        var TMP_URL = document.getElementById("TMP_URL").value;
        var json_file_path = TMP_URL + json_file;
        var xCats = [
            'Jan',
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
            'Dec'
        ];
        /*
        d=[];
        var x_plotLines = [];
        for (i=0;i<xCats.length;i++){
            d.push([i,null])
        }
        var x_plotLines = set_plotlines(d,1,'x',xCats.length);
        */
        x_props = set_barchart_axis_properties(xCats,12,'x');
        $.getJSON(json_file_path, function(datadict) {
            for (var i=0;i<datadict.length;i++){
                //Set up BarChart Template Class
                var ChartClass = new BarChart();
                //Find max/min values of data
                var data_max = null;
                var data_min = null;
                if (datadict[i].data){
                    data_max = Math.max.apply(Math,datadict[i].data);
                    data_min = Math.min.apply(Math,datadict[i].data);
                }

                //Y-axis properties
                var y_axis_props = set_y_axis_properties(data_max,'Use default', data_min, 'Use default',datadict[i].element,'mave','F',10.0);;
                //Define element dependent vars like y-axis max, min, plot-color
                var p_color = set_plot_color(datadict[i].element);
                var j = i + 1
                var cntr = 'container' + j
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
                        xAxis: {
                            categories:xCats,
                            plotLines:x_props.plotLines,
                            tickInterval:x_props.tickInterval
                        },
                        yAxis: {
                            min: data_min,
                            max: data_max,
                            gridLineWidth:0,
                            plotLines:y_axis_props.plotLines,
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
