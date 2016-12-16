$(function () {
    var downloadMenu = $.extend(true,[],Highcharts.getOptions().exporting.buttons.contextButton.menuItems.splice(2));
    var HOST = document.getElementById('HOST').value;
    var HOST_URL = 'http://' + HOST + '/';
    var json_file = document.getElementById("json_file").value;
    var TMP_URL = document.getElementById("TMP_URL").value;
    var json_file_path = TMP_URL + json_file;
    Highcharts.setOptions({
    colors: ['#058DC7', '#50B432', '#ED561B', '#DDDF00', '#24CBE5']
    });
    var style = {
        color:'#000000',
        fontSize:'14px'
        };
    $.getJSON(json_file_path, function(table_dict) {
        for (var i=0;i<table_dict.length;i++){
            //Define y-axis parameters
            if (table_dict[i].table_name == 'temp'){
                var yAx = {
                    labels: {
                        style:style
                    },
                    tickInterval: 10,
                    title: {
                        text: table_dict[i].table_name_long
                    }
                };
            }
            else if (table_dict[i].table_name == 'pcpn' || table_dict[i].table_name == 'snow' || table_dict[i].table_name == 'snwd'){
                var yAx = {
                    labels: {
                        style:style
                    },
                    tickInterval: 0.1,
                    title: {
                        text: table_dict[i].table_name_long
                    }
                };
            }
            else {
                var yAx = {
                    labels: {
                        style:style
                    },
                    tickInterval: 100,
                    title: {
                        text: table_dict[i].table_name_long,
                        style: style
                    }
                };
            }
            //Define other graph properties
            if (table_dict[i].table_name == 'temp'){
                var plot_type = 'boxplot';
                var enable_legend = false;
                var pl_opts = {}; 
                var tool_tip = {};
                /*
                var tool_tip = {
                    shared: true,
                    formatter: function() {
                    var s = '<b>'+ this.x +'</b>' + '<br/>';
                    var descriptors = ['<br/>Minimum = ', '<br/> Average Minimum = ', '<br/> Mean = ', '<br/> Average Maximum = ', '<br/>Maximum = '];
                    $.each(this.points, function(i, point) {
                        s += descriptors[i] + point.y + ' F ';
                    });
                    return s;
                    }
                };
                */ 
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
            //Vertical plotlines
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
            //Set up Chart
            var defaultChart = {
                chartContent: null,
                highchart: null,
                defaults: {
                    chart: {
                        type: plot_type,
                        plotBorderWidth: 1
                    },
                    credits: {
                        href: HOST_URL,
                        text: HOST 
                    },
                    //------------------------
                    //    EXPORTING (CSV/EXCEL)
                    //------------------------ 
                   navigation: {
                        buttonOptions: {
                            y:15,
                            theme: {
                                // Good old text links
                                style: {
                                    color: '#039',
                                    border:'1px solid #039',
                                    textDecoration: 'underline',
                                    fontWeight: 'bold',
                                    fontSize: '14px'
                                }
                            }
                        }
                    },
                    exporting: {
                        csv: {
                            dateFormat:'%Y-%m-%d'
                        },
                        chartOptions:{
                            legend:{
                                enabled:true
                            }
                        },
                        buttons: {
                            contextButton: {
                                enabled: false
                            },
                            exportButton: {
                                text: 'Download',
                                // Use only the download related menu items from the default context button
                                menuItems: downloadMenu
                            },
                            printButton: {
                                text: 'Print',
                                onclick: function () {
                                    this.print();
                                }
                            }
                        }
                    },
                    legend: {
                        enabled: enable_legend
                    },
                    xAxis: {
                        labels:{
                            style:style
                        },
                        plotLines:x_plotlines,
                        categories:table_dict[i].cats,
                        labels: {
                        step:2
                        },
                        title: {
                            style:style,
                            text: table_dict[i].record_start + ' - ' + table_dict[i].record_end
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
            var cntr = 'hc-container' + i;
            var Chart;
            var series = [];
            var max = -9999.0;
            var min = 9999.0;
            //Find max, min of data
            for (var k=0;k<table_dict[i].graph_data.length;k++){
                var max_test = Math.max.apply(Math, table_dict[i].graph_data[k]);
                var min_test = Math.min.apply(Math,table_dict[i].graph_data[k]);
                if ( max_test > max){
                    max = max_test;
                }
                if ( min_test < min){
                    min = min_test;
                }
            }
            if (table_dict[i].table_name == 'temp'){
                var s = {
                    name:table_dict[i].table_name_long,
                    color:'blue',
                    fillColor: {
                        linearGradient: [0, 0, 0, 300],
                        stops: [[0, 'rgb(69, 114, 167)'],[1, 'rgba(2,0,0,0)']]
                    },
                    data:table_dict[i].graph_data 
                };
                series.push(s);
            }
            else {
                for (var k=0;k<table_dict[i].graph_data.length;k++){
                    var s = {
                        name: table_dict[i].legend[k],
                        color: table_dict[i].colors[k],
                        data: table_dict[i].graph_data[k]
                    };
                    series.push(s);
                }
            }
            var variable = 'pcpn';
            if (table_dict[i].table_name == 'temp'){
                variable = 'maxt';
            }
            else if (table_dict[i].table_name == 'hdd' || table_dict[i].table_name == 'cdd' || table_dict[i].table_name == 'gdd' ){
                variable = 'maxt';
            } 
            var y_axis_props = set_y_axis_properties(max,'Use default', min, 'Use default',variable,'mave','F',10.0);
            var len = series.length
            Chart = {
                chartContent: cntr,
                options: {
                    title: {
                         style:style,
                         text: table_dict[i].title
                    },
                    subtitle: {
                        text: table_dict[i].subtitle
                    },
                    yAxis: {
                        labels: {
                            style:style
                        },
                        title: {
                            text: table_dict[i].table_name_long,
                            style: style
                        },
                        gridLineWidth:0,
                        plotLines:y_axis_props.plotLines,
                        //tickInterval:y_axis_props.tickInterval
                        //tickInterval:precise_round((max - min)/5, 0)
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
