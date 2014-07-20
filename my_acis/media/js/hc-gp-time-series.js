$(function () {
    var HOST = document.getElementById('HOST').value;
    var HOST_URL = 'http://' + HOST + '/';
    var style_axes = set_style('#000000','12px','bold',null);
    var style_text = set_style('#000000','14px',null,null);
    var defaultChart = {
        chartContent: null,
        highchart: null,
        defaults: {
            chart: {
                //type:'area',
                zoomType: 'x',
                spacingRight: 20
            },
            credits: {
                href: HOST_URL,
                text: HOST
            },
            subtitle: {
                text: document.ontouchstart === undefined ?
                'Click and drag in the plot area to zoom in' :
                'Drag your finger over the plot to zoom in'
            },
            xAxis: {
                labels: {
                    formatter: function () {
                        return Highcharts.dateFormat('%b%d\'%y', this.value);
                    },
                    style: style_axes,
                },
                title : {
                    style: style_text,
                }
            },
            yAxis: {
                labels: {
                    style: style_axes
                },
                startOnTick: false,
                showFirstLabel: false
            },
            tooltip: {
                shared: true
            },
            legend: {
                enabled: false
            },
            plotOptions: {
                area: {
                    fillColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, 'rgba(2,0,0,0)']
                        ]
                    },
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
        var TMP_URL = document.getElementById("TMP_URL").value;
        var json_file = document.getElementById("json_file").value;
        var json_file_name = TMP_URL + json_file;
        $.getJSON(json_file_name, function(datadict) {
            var start_date = datadict.search_params.start_date;
            var end_date = datadict.search_params.end_date;
            for (var el_idx=0;el_idx<datadict.data.length;el_idx++){
                var Chart; 
                Chart = {
                    chartContent:'gp_time_series_' + el_idx,
                    options: {
                        title: {
                            text:  datadict.search_params.elements_long[el_idx] + ' Lat: ' + parseFloat(datadict.search_params.lat).toPrecision(5) + ' Lon: ' + parseFloat(datadict.search_params.lon).toPrecision(5)
                        },
                        xAxis: {
                            title : {
                            text: 'Time Period: ' + start_date + ' - ' + end_date
                            },
                            type: 'datetime',
                            maxZoom: 1 * 24 * 3600000,
                            plotBands: [{
                                from: Date.UTC(parseInt(start_date.slice(0,4)),parseInt(start_date.slice(4,6).replace("^0+(?!$)", "")) - 1, parseInt(start_date.slice(6,8))),
                                to: Date.UTC(parseInt(end_date.slice(0,4)),parseInt(end_date.slice(4,6).replace("^0+(?!$)", "")) - 1, parseInt(end_date.slice(6,8)))
                            }],
                        },
                        yAxis: {
                            title: {
                                text: datadict.search_params.elements_long[el_idx]
                            }
                        },
                        series: [{
                            type: 'area',
                            name: datadict.search_params.element_list[el_idx],
                            color:'#00008B',
                            pointInterval:1 * 24 * 3600000, // 1 day
                            pointStart: Date.UTC(parseInt(start_date.slice(0,4)),parseInt(start_date.slice(4,6).replace("^0+(?!$)", "")) - 1, parseInt(start_date.slice(6,8))),
                            data:datadict.data[el_idx]
                        }] //end series
                    }//end options        
                };//end Chart
                Chart= jQuery.extend(true, {}, defaultChart, Chart);
                Chart.init(Chart.options);
                Chart.create();
            } //end for el_idx
        });//end getJSON
    });//end document ready function
});//end top function

