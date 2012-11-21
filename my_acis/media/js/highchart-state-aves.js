$(function () {
    var masterChart,
        detailChart;
    
    $(document).ready(function() {
    
        var state = document.getElementById("state").value;
        var element = document.getElementById("element").value;
        var month = document.getElementById("month").value;
        var month_name = document.getElementById("month_name").value;
        var MEDIA_URL = document.getElementById("MEDIA_URL").value;
        var json_file_name = MEDIA_URL +'json/' + state + '_' + month + '.json';
        $.getJSON(json_file_name, function(datadict) { 
        
            if (element == 'avgt'){
                var data = datadict.avgt;
                var Element = 'Mean Average Temperature';
                }
            else if (element == 'pcpn'){
                var data = datadict.pcpn;
                var Element = 'Mean Precipitaion';            
                }
            else if (element == 'maxt'){
                var data = datadict.maxt;
                var Element = 'Mean Maximum Temperature';
                }
            else if (element == 'mint'){
                var data = datadict.mint;
                var Element = 'Mean Minumum Temperature';
                }
            else if (element == 'snow'){
                var data = datadict.pcpn;
                var Element = 'Snow Fall';
                } 
            else if (element == 'snwd'){
                var data = datadict.pcpn;
                var Element = 'Snow Depth';
                }
            var dates = datadict.year_list;
            // create the master chart
            function createMaster() {
                masterChart = new Highcharts.Chart({
                    chart: {
                        renderTo: 'master-container',
                        reflow: false,
                        borderWidth: 0,
                        backgroundColor: null,
                        marginLeft: 50,
                        marginRight: 20,
                        zoomType: 'x',
                        events: {
        
                            // listen to the selection event on the master chart to update the
                            // extremes of the detail chart
                            selection: function(event) {
                                var extremesObject = event.xAxis[0],
                                    min = extremesObject.min,
                                    max = extremesObject.max,
                                    detailData = [],
                                    detail_date_valData = [],
                                    xAxis = this.xAxis[0];
        
                                // reverse engineer the last part of the data
                                jQuery.each(this.series[0].data, function(i, point) {
                                    if (point.x > min && point.x < max) {
                                        detailData.push({
                                            x: point.x,
                                            y: point.y
                                        });
                                        detail_date_valData.push([point.x, point.y]);
                                    }
                                });
        
                                // move the plot bands to reflect the new detail span
                                xAxis.removePlotBand('mask-before');
                                xAxis.addPlotBand({
                                    id: 'mask-before',
                                    from: Date.UTC(1900, 0, 1),
                                    to: min,
                                    color: 'rgba(0, 0, 0, 0.2)'
                                });
        
                                xAxis.removePlotBand('mask-after');
                                xAxis.addPlotBand({
                                    id: 'mask-after',
                                    from: max,
                                    to: Date.UTC(2012, 12, 31),
                                    color: 'rgba(0, 0, 0, 0.2)'
                                });
        
        
                                detailChart.series[0].setData(detailData);
                                detailChart.series[1].setData(fitData(detail_date_valData).data); 
                                return false;
                            }
                        } //end evens
                    },//end chart
                    title: {
                        text: null
                    },
                    xAxis: {
                        type: 'datetime',
                        showLastTickLabel: true,
                        maxZoom: 48 * 24 * 3600000, // 1 day (days, hrs, secs)
                        plotBands: [{
                            id: 'mask-before',
                            from: Date.UTC(1900, 0, 1),
                            to: Date.UTC(2012, 12, 31), //initial band will show last 2 years in detail
                            color: 'rgba(0, 0, 0, 0.2)'
                        }],
                        title: {
                            text: null
                        }
                    },
                    yAxis: {
                        gridLineWidth: 0,
                        labels: {
                            enabled: false
                        },
                        title: {
                            text: null
                        },
                        showFirstLabel: false
                    },
                    tooltip: {
                        formatter: function() {
                            return false;
                        }
                    },
                    legend: {
                        enabled: false
                    },
                    credits: {
                        enabled: false
                    },
                    plotOptions: {
                        series: {
                            fillColor: {
                                linearGradient: [0, 0, 0, 70],
                                stops: [
                                    [0, '#4572A7'],
                                    [1, 'rgba(0,0,0,0)']
                                ]
                            },
                            lineWidth: 1,
                            marker: {
                                enabled: false
                            },
                            shadow: false,
                            states: {
                                hover: {
                                    lineWidth: 1
                                }
                            },
                            enableMouseTracking: false
                        }
                    },
        
                    series: [{
                        type: 'area',
                        name: Element,
                        pointInterval: 365*25 * 3600 * 1000, //somehow, this makes it go from 1900 to present
                        pointStart: Date.UTC(1900, 0, 01),
                        data: data
                    }],
        
                    exporting: {
                        enabled: false
                    }
        
                }, function(masterChart) {
                    createDetail(masterChart)
                });
            } //end createMaster
        
            // create the detail chart
            function createDetail(masterChart) {
        
                // prepare the detail chart
                var detailData = [],
                    detail_date_valData = [], //for regression line
                    detailStart = Date.UTC(1900, 1, 1);
        
                jQuery.each(masterChart.series[0].data, function(i, point) {
                    if (point.x >= detailStart) {
                        detailData.push(point.y);
                        detail_date_valData.push([point.x, point.y]); 
                    }
                });
        
                // create a detail chart referenced by a global variable
                detailChart = new Highcharts.Chart({
                    chart: {
                        marginBottom: 120,
                        renderTo: 'detail-container',
                        reflow: false,
                        marginLeft: 50,
                        marginRight: 20,
                        style: {
                            position: 'absolute'
                        }
                    },
                    credits: {
                        enabled: false
                    },
                    title: {
                        text: Element + ' for ' + state + ' in ' + month_name 
                    },
                    subtitle: {
                        text: 'Select an area by dragging across the lower chart'
                    },
                    xAxis: {
                        type: 'datetime'
                    },
                    yAxis: {
                        title: {
                            text: null
                        },
                        maxZoom: 0.1
                    },
                    tooltip: {
                        formatter: function() {
                            var point = this.points[0];
                            return '<b>'+ point.series.name +'</b><br/>'+
                                //Highcharts.dateFormat('%A %B %e %Y', this.x) + ':<br/>'+
                                //'Temp = '+ Highcharts.numberFormat(point.y, 2) +' F';
                                Highcharts.dateFormat('%Y', this.x) + ':<br/>'+
                                Element + ' = '+ Highcharts.numberFormat(point.y, 2) +' F';
                        },
                        shared: true
                    },
                    legend: {
                        enabled: false
                    },
                    plotOptions: {
                        series: {
                            marker: {
                                enabled: false,
                                states: {
                                    hover: {
                                        enabled: true,
                                        radius: 3
                                    }
                                }
                            }
                        }
                    },
                    series: [{
                        name: Element,
                        pointStart: detailStart,
                        pointInterval: 365*25 * 3600 * 1000, //somehow, this makes it go from 1900 to present
                        data: detailData
                    }, 
                    {
                        name: 'Regression Line',
                        pointStart: detailStart,
                        pointInterval: 365*25 * 3600 * 1000, //somehow, this makes it go from 1900 to present
                        type: 'line',
                        /* function returns data for trend-line */
                        data: (function() {
                        return fitData(detail_date_valData).data; //calls functions from {{MEDIA_URL}}js/regression.js
                        })()
                    }],
        
                    exporting: {
                        enabled: false
                    }
        
                });//end createDetail(masterChart) 
            }//
        
            // make the container smaller and add a second container for the master chart
            var $container = $('#hc-graph-state-aves')
                .css('position', 'relative');
        
            var $detailContainer = $('<div id="detail-container">')
                .appendTo($container);
        
            var $masterContainer = $('<div id="master-container">')
                .css({ position: 'absolute', top: 300, height: 80, width: '100%' })
                .appendTo($container);
        
            // create master and in its callback, create the detail chart
            createMaster();
        }); //end get json function
    }); // end document(ready) function
    
});// end top function
