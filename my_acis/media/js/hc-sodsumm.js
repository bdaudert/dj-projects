$(function () {
//$(document).ready(function() {
    var json_file = document.getElementById("json_file").value;
    var JSON_URL = document.getElementById("JSON_URL").value;
    var tab_list =  document.getElementById("tab_list").value;
    var json_file_path = '/csc/media/tmp/' + json_file;
    Highcharts.setOptions({
    colors: ['#058DC7', '#50B432', '#ED561B', '#DDDF00', '#24CBE5']
    });
    $.getJSON(json_file_path, function(table_dict) {
        for (var i=0;i<table_dict.length;i++){
            var yAx = {
                title: {
                    text: table_dict[i].table_name_long
                    }
                };
            if (table_dict[i].table_name == 'temp'){
                /*
                var yAx = {
                    stackLabels: {
                        enabled: true,
                        style: {
                            fontWeight: 'bold',
                            color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                        }
                    }
                };
                var stckn = 'normal';
                */
                var plot_type = 'boxplot';
                var enable_legend = false;
                var pl_opts = {}; 
                var tool_tip = {}; 
            }
            else {
                var plot_type = 'column';
                var enable_legend = true;
                var pl_opts = {
                        column: {
                            pointPadding: 0.2,
                            borderWidth: 0
                        }
                };
                var tool_tip = {
                    formatter: function() {
                        return ''+
                        this.x +': '+ this.y;
                    }
                };
            }
            //Set up Chart
            var defaultChart = {
                chartContent: null,
                highchart: null,
                defaults: {
                    chart: {
                        type: plot_type
                    },
                    credits: {
                        href: 'http://wrcc.dri.edu/',
                        text: 'wrcc.dri.edu' 
                    },
                    legend: {
                        enabled: enable_legend
                    },
                    xAxis: {
                        categories:table_dict[i].cats, 
                        title: {
                            text: 'Month'
                        }                    
                    },
                    yAxis: yAx,
                    tooltip: tool_tip, 
                    plotOptions: pl_opts,
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
            var cntr = 'container' + i;
            var Chart;
            var series = [];
            if (table_dict[i].table_name == 'temp'){
                var s = {
                    name:table_dict[i].table_name_long,
                    color:'blue',
                    fillColor: {
                        linearGradient: [0, 0, 0, 300],
                        stops: [[0, 'rgb(69, 114, 167)'],[1, 'rgba(2,0,0,0)']]
                    },
                    data:table_dict[i].table_data 
                };
                series.push(s);
            }
            else {
                for (var k=0;k<table_dict[i].table_data.length;k++){
                    var s = {
                        name: table_dict[i].legend[k],
                        color: table_dict[i].colors[k],
                        data: table_dict[i].table_data[k]
                    };
                    series.push(s);
                }
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
                        title: {
                        text: table_dict[i].table_name_long + ' in ' + table_dict[i].units
                        }
                    },
                    series: series
                } 
            };//end Chart
            Chart= jQuery.extend(true, {}, defaultChart, Chart);
            Chart.init(Chart.options);
            Chart.create();
        }; //endfor
    }); //end getJSON
}); // end doc ready
