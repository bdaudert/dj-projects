//------------------------
// General function for monann
//------------------------
function generate_monannTS(json_file_path,chartType,data_indices,smry,rm,range) {
        /*
        Generates highcarts figure
        Required Args:
            json_file_path
        Optional Args:
            chartType, if none is given chartType is obtained from json file
            data_indices:
            smry: summary of individual indices: mean/sum/median/max/min or individual
            rm: running mean years
            range: yes or no
        */
        $.getJSON(json_file_path, function(datadict) {
            //Set figureID and chartType
             switch (arguments.length - 1) { // <-- 1 is number of required arguments
                case 0:  
                    figureID = '0';
                    chartType = datadict.chartType;
                    data_indices = 1;
                    smry = datadict.smry;
                    rm = datadict.show_running_mean;
                    range = datadict.show_range;
                case 1:
                    data_indices = 1;
                    smry = datadict.smry;
                    rm = datadict.show_running_mean;
                    range = datadict.show_range;
                case 2:
                    smry = datadict.smry;
                    rm = datadict.show_running_mean;
                    range = datadict.show_range;
                case 3:
                    rm = datadict.show_running_mean;
                    range = datadict.show_range;
                case 4:
                    range = datadict.show_range;

            }   
            var axisFontSize = '16px';
            var labelsFontSize = '20px';

            //Define series data
            var series_data = [{
                    name: datadict.seriesName,
                    color: datadict.plotColor,
                    data: datadict.data
                }]
            //Add running mean
            /*
            if (rm){
                rm_series = {
                    type:'spline',
                    name:datadict[chartID].running_mean_title,
                    color:'#FF0000',
                    data:datadict[chartID].running_mean_data
                }
                series_data.push(rm_series);
            }
            */
            $('#container').highcharts({
                //------------------------
                //  CHART PROPERTIES
                //------------------------
                chart: {
                    type:chartType,
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
                    text: datadict[chartID].title,
                },
                subtitle: {
                    text: datadict[chartID].subTitle,
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
                        text: 'Period: ' + datadict[chartID].startDate + ' - ' + datadict[chartID].endDate,
                        style: {
                            fontSize: labelsFontSize,
                        },
                    },
                    labels: {
                        format: '{value:%Y-%m-%d}',
                        rotation: -45,
                        //align: 'left',
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
                        text: datadict[chartID].yLabel,
                        style: {
                            fontSize: labelsFontSize,
                        },
                    },
                    min: datadict[chartID].axisMin,
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
                    x: -400, // >0 moves right
                    borderWidth: 1,
                    borderRadius: 5,
                    floating: true,
                    draggable: true,
                    zIndex: 20,
                    title: {
                        text: datadict[chartID].legendTitle
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
                            symbol: 'circle'
                        }
                    },
                    series: {
                        states: {
                            hover: {
                                enabled: true,
                                brightness: 0.2
                            }
                        },
                        marker: {
                            radius: 4,
                            lineWidth: 1,
                            enable: true,
                            symbol: 'circle'
                        }
                    },
                    areaspline: {
                        fillOpacity: 0.1 //not working to be transparent... someone set need hex colors not 'red'
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
                    pointFormat: '<b>Date: </b>{point.x:%b %e,%Y}<br><b>Value:</b> {point.y:.2f}'+datadict[chartID].elUnits,
                    crosshairs: false,
                    shared: false
                },
                //------------------------
                series: series_data
              });//highCharts
        });//getJSON
};

//------------------------
// General function for spatial summary
//------------------------
function generate_spatial_summaryTS(json_file_path,figureID,chartType) {
        /*
        Generates highcarts figure
        Required Args:
            json_file_path
        Optional Args:
            figureId, if none is given, figureID is set to zero
            chartType, if none is given chartType is obtained from json file
        */
        var chartID = parseInt(figureID);
        $.getJSON(json_file_path, function(datadict) {
            //Set figureID and chartType
             switch (arguments.length - 1) { // <-- 1 is number of required arguments
                case 0:  
                    figureID = '0';
                    chartType = datadict[chartID].chartType;
                case 1:
                    chartType = datadict[chartID].chartType;
            }   
            var chartID = parseInt(figureID);
            var axisFontSize = '16px';
            var labelsFontSize = '20px';

            //Define series data
            var series_data = [{
                    name: datadict[chartID].seriesName,
                    color: datadict[chartID].plotColor,
                    data: datadict[chartID].data
                }]
            //Add running mean
            if ('running_mean_data' in datadict[chartID]){
                rm_series = {
                    type:'spline',
                    name:datadict[chartID].running_mean_title,
                    color:'#FF0000',
                    data:datadict[chartID].running_mean_data
                }
                series_data.push(rm_series);
            }

            $('#container_' + figureID).highcharts({
                //------------------------
                //  CHART PROPERTIES
                //------------------------
                chart: {
                    type:chartType,
                    zoomType: 'x',
                    spacingBottom: 30,
                    spacingTop: 10,
                    spacingLeft: 10,
                    spacingRight: 10,
                    plotBorderWidth: 1,
                    borderColor: '#006666',
                    borderWidth: 1,
                },
                //------------------------
                //    TITLE/SUBTITLE
                //------------------------
                title: {
                    text: datadict[chartID].title,
                },
                subtitle: {
                    text: datadict[chartID].subTitle,
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
                        text: 'Period: ' + datadict[chartID].startDate + ' - ' + datadict[chartID].endDate,
                        style: {
                            fontSize: labelsFontSize,
                        },
                    },
                    labels: {
                        format: '{value:%Y-%m-%d}',
                        rotation: -45,
                        //align: 'left',
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
                        text: datadict[chartID].yLabel,
                        style: {
                            fontSize: labelsFontSize,
                        },
                    },
                    min: datadict[chartID].axisMin,
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
                    x: -400, // >0 moves right
                    borderWidth: 1,
                    borderRadius: 5,
                    floating: true,
                    draggable: true,
                    zIndex: 20,
                    title: {
                        text: datadict[chartID].legendTitle
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
                            symbol: 'circle'
                        }
                    },
                    series: {
                        states: {
                            hover: {
                                enabled: true,
                                brightness: 0.2
                            }
                        },
                        marker: {
                            radius: 4,
                            lineWidth: 1,
                            enable: true,
                            symbol: 'circle'
                        }
                    },
                    areaspline: {
                        fillOpacity: 0.1 //not working to be transparent... someone set need hex colors not 'red'
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
                    pointFormat: '<b>Date: </b>{point.x:%b %e,%Y}<br><b>Value:</b> {point.y:.2f}'+datadict[chartID].elUnits,
                    crosshairs: false,
                    shared: false
                },
                //------------------------
                series: series_data
              });//highCharts
        });//getJSON
};
