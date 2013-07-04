$(function () {
    var style = {
        color:'#000000',
        fontSize:'14px'
    }; 
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
                    style: style
                },
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
                    style: style
                }
            },
            /*
            legend: {
                layout: 'vertical',
                backgroundColor: '#FFFFFF',
                align: 'left',
                verticalAlign: 'top',
                x: 100,
                y: 70,
                floating: true,
                shadow: true
            },
            */
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
                //Define element dependent vars like y-axis max, min, plot-color
                if (datadict[i].element == 'maxt'){
                    //var min = -50;
                    //var max = 130;
                    var p_color = '#FF0000';
                }
                if (datadict[i].element == 'mint'){
                    //var min = -50;
                    //var max = 130;
                    var p_color = '#0000FF';
                }
                if (datadict[i].element == 'pcpn'){
                    var min = 0;
                    var p_color = '#00FF00';
                }
                if (datadict[i].element == 'snow' || datadict[i].element == 'snwd'){
                    var min = 0;
                    var p_color = '#800080';    
                }
                if (datadict[i].element == 'hdd' || datadict[i].element == 'cdd' || datadict[i].element == 'gdd'){
                    var min = 0;
                    var p_color = '#00FFFF';
                }
                var j = i + 1
                var cntr = 'container' + j
                var Chart;            
                Chart = {

                chartContent: cntr,
                options: {

                    title: {
                         style:style,
                         text:datadict[i].stn_name + ', ' + datadict[i].stn_id + ', ' + datadict[i].state
                    },
                    subtitle: {
                        text: 'Date Range ' + datadict[i].record_start  + ' - '+ datadict[i].record_end
                    },
                    yAxis: {
                    min: min,
                    title: {
                        style:style,
                        text: datadict[i].element_long + ' in ' + datadict[i].units
                        }
                    },
                    series: [{
                        name: ' Monthly Averages for ' + datadict[i].element_long,
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
