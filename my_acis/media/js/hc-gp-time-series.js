$(function () {
    var chart;

    $(document).ready(function() {
        var JSON_URL = document.getElementById("JSON_URL").value;
        var element_long = document.getElementById("element_long").value;
        var element = document.getElementById("element").value;
        var lon_lat = document.getElementById("location").value;
        var lon = lon_lat.split(",")[0];
        var lat = lon_lat.split(",")[1];
        var start_date = document.getElementById("start_date").value;
        var end_date = document.getElementById("end_date").value;
        var json_file = document.getElementById("json_file").value;
        var json_file_name = JSON_URL + json_file;
        var style = {
                color:'#000000',
                fontSize:'14px'
            };         
        $.getJSON(json_file_name, function(datadict) {
            chart = new Highcharts.Chart({
                chart: {
                    renderTo: 'hc-graph',
                    zoomType: 'x',
                    spacingRight: 20
                },
                title: {
                    text:  element_long + ' Lat: ' + parseFloat(lat).toPrecision(5) + ' Lon: ' + parseFloat(lon).toPrecision(5)
                },
                subtitle: {
                    text: document.ontouchstart === undefined ?
                        'Click and drag in the plot area to zoom in' :
                        'Drag your finger over the plot to zoom in'
                },
                credits: {
                        href: 'http://wrcc.dri.edu/',
                        text: 'wrcc.dri.edu'
                },
                xAxis: {
                    labels: {
                        style: style
                    },
                    title : {
                        style: style,
                        text: 'Time Period: ' + start_date + ' - ' + end_date
                    },
                    type: 'datetime',
                    maxZoom: 1 * 24 * 3600000, // 1 day
                    plotBands: [{
                    from: Date.UTC(parseInt(start_date.slice(0,4)),parseInt(start_date.slice(4,6).replace("^0+(?!$)", "")) - 1, parseInt(start_date.slice(6,8))),
                    to: Date.UTC(parseInt(end_date.slice(0,4)),parseInt(end_date.slice(4,6).replace("^0+(?!$)", "")) - 1, parseInt(end_date.slice(6,8)))
                    }],
                    title: {
                        text: null
                    }
                },
                yAxis: {
                    labels: {
                        style: style
                    },
                    title: {
                        style: style,
                        text: element_long
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
                    color:'#00008B',
                    pointInterval:1 * 24 * 3600000, // 1 day
                    pointStart: Date.UTC(parseInt(start_date.slice(0,4)),parseInt(start_date.slice(4,6).replace("^0+(?!$)", "")) - 1, parseInt(start_date.slice(6,8))),
                    data:datadict.data
                }] //end series
            });//end chart
        });
    });//end document ready function
    
});//end top function

