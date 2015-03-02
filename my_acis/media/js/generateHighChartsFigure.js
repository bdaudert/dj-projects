//------------------------
// General function for 
//------------------------
function generateHighChartTS(figureID) {
    $(document).ready(function() {
        var json_file = document.getElementById('json_file').value;
        var chartID = parseInt(figureID)
        $.getJSON('/tmp/' + json_file, function(datadict) {
            var series_data = datadict[chartID].data;
            var chartType = datadict[chartID].chartType;
            var title = datadict[chartID].title;
            var subtitle = datadict[chartID].subtitle;
            var dateStart = datadict[chartID].start_date;
            var dateEnd = datadict[chartID].end_date;
            var yLable = datadict[chartID].yLabel;
            var xLable = datadict[chartID].xLabel;
            var legendTitle = datadict[chartID].legendTitle;
            var axis_min = datadict[chartID].axis_min;
            var varUnits = datadict[chartID].varUnits;
        
            axisFontSize = '16px';
            labelsFontSize = '20px';

            $('#' + figureID).highcharts({
                //------------------------
                //  CHART PROPERTIES
                //------------------------
                chart: {
                    //renderTo: figureID,
                    type:  chartType,
                    zoomType: 'x',
                    spacingBottom: 30,
                    spacingTop: 10,
                    spacingLeft: 10,
                    spacingRight: 10,
                },
                //------------------------
                //    TITLE/SUBTITLE
                //------------------------
                title: {
                    text: title,
                },
                subtitle: {
                    text: subtitle,
                },
                //------------------------
                //XAXIS
                //------------------------
                xAxis: {
                    gridlineWidth: 1,
                    type:'datetime',  
                    showLastTickLabel: true,
                    maxZoom: 1 * 24 * 3600*1000, // one day
                    title: {
                        text: '', //no need to label this as Date
                        style: {
                            fontSize: labelsFontSize,
                        },
                    },
                    labels: {
                        format: '{value:%Y-%m-%d}',
                        rotation: 90,
                        align: 'left',
                        style: {
                            fontSize: axisFontSize,
                            zIndex: 6,
                        },
                    }
                },
                //------------------------
                //YAXIS
                //------------------------
                yAxis: {
                    gridLineWidth: 1,
                    title: {
                        text: yLabel,
                        style: {
                            fontSize: labelsFontSize,
                        },
                    },
                    min: axis_min,
                    tickLength: 5,
                    tickWidth: 1,
                    tickPosition: 'outside',
                    lineWidth:1,
                    labels: {
                        style: {
                            fontSize: axisFontSize,
                            zIndex: 6,
                        }
                    }
                },
                //------------------------
                //LEGEND
                //------------------------
                legend: {
                    layout: 'vertical',
                    backgroundColor: 'white',
                    align: 'right',
                    verticalAlign: 'top',
                    y: 50, // >0 moves down
                    x: -500, // >0 moves right
                    borderWidth: 1,
                    borderRadius: 5,
                    floating: true,
                    draggable: true,
                    zIndex: 20,
                    title: {
                        text: legendTitle,
                    }
                },
                //------------------------
                // PLOT OPTIONS
                //------------------------
                plotOptions: {
                    spline: {
                        marker: {
                            radius: 4,
                            lineWidth: 1,
                            enable: true,
                            symbol: 'circle',
                        }
                    },
                    series: {
                        states: {
                            hover: {
                                enabled: true,
                                brightness: 0.2
                            },
                        },
                        marker: {
                            radius: 4,
                            lineWidth: 1,
                            enable: true,
                            symbol: 'circle',
                        }
                    },
                    areaspline: {
                        fillOpacity: 0.1, //not working to be transparent... someone set need hex colors not 'red'
                    },
                    line: {
                        connectNulls: false
                    },
                    area: {
                        stacking: 'normal',
                        lineColor: '#666666',
                        lineWidth: 1,
                        marker: {
                            lineWidth: 1,
                            lineColor: '#666666'
                        }
                    },
                },
                //------------------------
                //TOOLTIP -What happens when hover over the item
                //------------------------
                tooltip: {
                headerFormat: '',
                pointFormat: '<b>Date: </b>{point.x:%b %e,%Y}<br><b>Value:</b> {point.y:.2f}'+varUnits,
                crosshairs: false,
                    shared: false,
                },
                //------------------------
                series: series_data,
              });//highCharts
        });//getJSON
    });//document.ready function
};
