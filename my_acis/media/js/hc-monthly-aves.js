$(function () {
    var style_axes = {
        color:'#000000',
        fontSize:'14px',
        fontWeight: 'bold'
    };
    var style_text = {
        color:'#000000',
        fontSize:'18px'
    };
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
    var defaultChart = {
        chartContent: null,
        highchart: null,
        defaults: {
            chart: {
                type: 'column'
            },
            credits: {
                href: 'http://wrcc.dri.edu/',
                text: 'wrcc.dri.edu'
            },
            xAxis: {
                labels: {
                    style: style_axes, 
                    step:2
                },
                plotLines: x_plotlines,
                categories: [
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
                ]
            },
            yAxis: {
                labels: {
                    style: style_axes
                }
            },
            tooltip: {
                formatter: function() {
                    return ''+
                        this.x +': '+ this.y;
                }
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
        },//end defaults

        // here you'll merge the defauls with the object options

        init: function(options) {

            this.highchart= jQuery.extend({}, this.defaults, options);
            this.highchart.chart.renderTo = this.chartContent;
        },

        create: function() {

            new Highcharts.Chart(this.highchart);
        }

    }; // end var defaultChart

    $(document).ready(function() {
        var json_file = document.getElementById("json_file").value;
        var JSON_URL = document.getElementById("JSON_URL").value;
        var json_file_path = JSON_URL + json_file;
        var p_color = '#0000FF';
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
                if (datadict[i].element == 'maxt'){
                    var p_color = '#FF0000';
                }
                if (datadict[i].element == 'mint'){
                    var p_color = '#0000FF';
                }
                if (datadict[i].element == 'pcpn' || datadict[i].element == 'evap' || datadict[i].element == 'wdmv'){
                    var p_color = '#00FF00';
                }
                if (datadict[i].element == 'snow' || datadict[i].element == 'snwd'){
                    var p_color = '#800080';    
                }
                if (datadict[i].element == 'hdd' || datadict[i].element == 'cdd' || datadict[i].element == 'gdd'){
                    var p_color = '#00FFFF';
                }
                var j = i + 1
                var cntr = 'container' + j
                var Chart;            
                Chart = {

                chartContent: cntr,
                options: {

                    title: {
                         style:style_text,
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
                            style:style_text,
                            text: datadict[i].element_long
                            }
                    },
                    series: [{
                        name: ' Monthly Averages: ' + datadict[i].element_long,
                        color: p_color,
                        data: datadict[i].data
                    }]
                },
                };
            Chart= jQuery.extend(true, {}, defaultChart, Chart);
            Chart.init(Chart.options);
            Chart.create();
            }; //endfor
        }); //end getJSON
    }); // end doc ready
});//end top function
