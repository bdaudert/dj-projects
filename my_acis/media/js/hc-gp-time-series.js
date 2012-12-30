$(function () {
    var chart;

    $(document).ready(function() {
        var JSON_URL = document.getElementById("JSON_URL").value;
        var element_long = document.getElementById("element_long").value;
        var element = document.getElementById("element").value;
        var lat = document.getElementById("lat").value;
        var lon = document.getElementById("lon").value;
        var start_date = document.getElementById("start_date").value;
        var end_date = document.getElementById("end_date").value;
        var json_file = document.getElementById("json_file").value;
        var json_file_name = JSON_URL + json_file;
        
        var start = new Array();
        var end = new Array();
        start = start_date.split('-')
        end = end_date.split('-')
        
        $.getJSON(json_file_name, function(datadict) {
            chart = new Highcharts.Chart({
                chart: {
                    renderTo: 'hc-graph',
                    zoomType: 'x',
                    spacingRight: 20
                },
                title: {
                    text:  element_long + ' Lat: ' + lat + ' Lon: ' + lon
                },
                subtitle: {
                    text: document.ontouchstart === undefined ?
                        'Click and drag in the plot area to zoom in' :
                        'Drag your finger over the plot to zoom in'
                },
                xAxis: {
                    type: 'datetime',
                    maxZoom: 1 * 24 * 3600000, // 1 day
                    plotBands: [{
                    from: Date.UTC(parseInt(start[0]), parseInt(start[1]), parseInt(start[2])),
                    to: Date.UTC(parseInt(end[0]), parseInt(end[1]), parseInt(end[2])),
                    }],
                    title: {
                        text: null
                    }
                },
                yAxis: {
                    title: {
                        text: element
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
        
                series: [{
                    type: 'area',
                    name: element,
                    pointInterval:1 * 24 * 3600000, // 1 day
                    pointStart: Date.UTC(parseInt(start[0]), parseInt(start[1]), parseInt(start[2])),
                    data:datadict.data
                }] //end series
            });//end chart
        });
    });//end document ready function
    
});//end top function

