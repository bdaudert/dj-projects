$(function () {
//$(document).ready(function() {
    var json_file = document.getElementById("json_file").value;
    var JSON_URL = document.getElementById("JSON_URL").value;
    var json_file_path = '/csc/media/tmp/' + json_file;
    $.getJSON(json_file_path, function(table_dict) {
        for (var i=0;i<table_dict.length;i++){
            if (table_dict[i].table_name == 'hdd' || table_dict[i].table_name == 'cdd' || table_dict[i].table_name == 'gdd'){
                //regular bar chart
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
                            categories:table_dict[i].cats, 
                            labels: {
                                rotation: -41,
                                align: 'right',
                                style: {
                                    fontSize: '13px',
                                    fontFamil: 'Verdana, sans-serif'
                                }
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
            }
            else {
                //stacked bar carts
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
                            categories:table_dict[i].cats 
                        },
                        yAxis: {
                            stackLabels: {
                                enabled: true,
                                style: {
                                    fontWeight: 'bold',
                                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                                }
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
                                borderWidth: 0,
                                stacking: 'normal',
                                dataLabels: {
                                    enabled: true;
                                }
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
            } //end else (stacked bar chart)

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
                         text: table_dict[i].stn_name + ', ' + table_dict[i].stn_id  + ', ' + table_dict[i].table_name_long
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