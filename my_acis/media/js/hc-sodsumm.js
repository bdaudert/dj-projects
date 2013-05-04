$(function () {
//$(document).ready(function() {
    var json_file = document.getElementById("json_file").value;
    $.getJSON(json_file, function(table_dict) {
        for (var i=0;i<table_dict.length;i++){
            var defaultChart = {
                chartContent: null,
                highchart: null,
                defaults: {
                    chart: {
                        type: 'column'
                    },
                    xAxis: {
                        categories:table_dict[i].x_cats, 
                        labels: {
                            rotation: -41,
                            align: right,
                            style: {
                                fontSize: '13px',
                                fontFamil: 'Verdana, sans-serif'
                            }
                        }
                    },
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

            //Define table_name dependent vars like y-axis max, min, plot-color
            if (table_dict[i].table_name == 'temp'){
                var min = -50;
                var max = 130;
            }
            if (table_dict[i].table_name == 'prsn'){
                var min = 0;
            }
            if (table_dict[i].table_name == 'hdd' || table_dict[i].table_name == 'cdd' || table_dict[i].table_name == 'gdd'){
                var min = 0;
            }
            var cntr = 'container' + i
            var Chart;
            var series = [];
            for (var k=0;k<table_dict[i].table_data.length;k++){
                var s = {
                name: table_dict[i].legend[k],
                color: table_dict[i].colors[k],
                data: table_dict[i].table_data[k]
                };
                series.push(s);
            }
                      
            Chart = {
                chartContent: cntr,
                options: {

                    title: {
                         text: 'Summary:' + table_dict[i].table_name_long
                    },
                    subtitle: {
                        text: 'Year Range: ' + table_dict[i].record_start  + ' - '+ table_dict[i].record_end
                    },
                    yAxis: {
                        min: min,
                        title: {
                        text: table_dict[i].table_name_long + ' in ' + table_dict[i].units
                        }
                    },
                    series:series
                    } 
            };
            Chart= jQuery.extend(true, {}, defaultChart, Chart);
            Chart.init(Chart.options);
            Chart.create();
        }; //endfor
    }); //end getJSON
}); // end doc ready
