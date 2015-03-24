//------------------------
// General function for monann
//------------------------
function generateTS(containerID, data_indices) {
    /*
    Generates highcarts figure
    Required Args:
        data_indices: indices of data to be plotted,
            if not given, we pick it up from html element data_indices
        show_range: T or F
    */
    var args = arguments;
    var datadict = graph_data; //template_variable
    switch (arguments.length) { // <-- 0 is number of required arguments
        case 1: var data_indices = $('#data_indices').val();
    }

    var running_mean_period = '0', show_range = 'F', smry = 'individual';
    //Get chart variables from template
    var chartType = $('#chart_type').val();
    
    if ($('#show_running_mean').length && $('#show_running_mean').is(':checked')) {
        running_mean_period = $('#running_mean_period').val();
    }
    if ($('#chart_summary').length) {
        smry = $('#chart_summary').val();
    }
    if ($('#show_range').length && $('#show_range').is(':checked')) {
        show_range = 'T';
    }
    var date_format = '%Y-%m-%d';
    var chartTitle = datadict[0].title;
    var subTitle = datadict[0].subTitle
    if ($('#app_name').length && $('#app_name').val() == 'monann'){
        var date_format = '%Y';
    }
    var elUnits = datadict[0].elUnits;
    
    //Set font size
    var axisFontSize = '16px';
    var labelsFontSize = '20px';
    //Define series data
    var series_data = [],idx;
    if (smry == 'individual'){
        r_data = [];
        for (var i=0;i < data_indices.length;i++){
            idx = data_indices[i];
            var s = {
                type:datadict[idx].chartType,
                name: datadict[idx].seriesName,
                //color: datadict[idx].series_color,
                color:Highcharts.getOptions().colors[2*idx],
                id:'data_' + String(idx),
                data: datadict[idx].data
            }
            series_data.push(s);
            r_data.push(datadict[idx].data);
            //Add running means
            if (running_mean_period != '0'){
                var rm = {
                    type:'trendline',
                    linkedTo:':previous',
                    algorithm: 'EMA',
                    periods:parseInt(running_mean_period),
                    name: 'Running Mean: ' + datadict[idx].seriesName,
                    color:datadict[idx].running_mean_color,
                    showInLegend: true
                }
                series_data.push(rm);
            }
        }
    }
    if (smry != 'individual'){
         var idx,names = '';to_summarize = []
         for (var i=0;i < data_indices.length;i++){
            idx = data_indices[i];
            names+= datadict[idx].seriesName + ',';
            to_summarize.push(datadict[idx].data);   
         }
         //Get smry and range data
         var smry_data = compute_summary(to_summarize,smry);
         //Strip last comma
         name = names.slice(0,-1);
         var s = {
            name: smry.toUpperCase() + ' over: ' + names,
            //color: datadict[0].series_color,
            color:Highcharts.getOptions().colors[2*idx],
            id:'primary',
            data:smry_data.data
        }
        series_data.push(s)
        
        //Add running Mean
        if (running_mean_period != '0'){
            var rm = {
                type:'trendline',
                linkedTo:'primary',
                algorithm: 'EMA',
                periods:parseInt(running_mean_period),
                name: 'Running Mean',
                color:datadict[0].running_mean_color,
                showInLegend: true
            }
            series_data.push(rm);
        }

        //Add Range
        if (show_range == 'T'){
            alert(smry_data.ranges);
            var r = {
                name: 'Range',
                data:smry_data.ranges,
                type: 'arearange',
                lineWidth: 0,
                color: Highcharts.getOptions().colors[2*idx + 1],
                fillOpacity: 0.3,
                zIndex: 0
            }
            series_data.push(r)
        }
    }
    //Clear old plot
    $('#' + containerID).contents().remove();
    //CHART
    $('#' + containerID).highcharts({
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
        credits: {
            href: 'http://wrcc.dri.edu',
            text: 'wrcc.dri.edu'
        },
        //------------------------
        //    EXPORTING (CSV/EXCEL)
        //------------------------ 
        exporting: {
            csv: {
                dateFormat: date_format
            }
        },
        //------------------------
        //    TITLE/SUBTITLE
        //------------------------
        title: {
            text: chartTitle,
        },
        subtitle: {
            text: subTitle,
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
                text: 'Period: ' + datadict[0].startDate + ' - ' + datadict[0].endDate,
                style: {
                    fontSize: labelsFontSize,
                },
            },
            labels: {
                format: '{value:' + date_format  + '}',
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
                text: elUnits,
                style: {
                    fontSize: labelsFontSize,
                },
            },
            min: datadict[0].axisMin,
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
            zIndex: 20
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
                pointFormat: '<b>Year: </b>{point.x:'+  date_format +'}<br><b>Value:</b> {point.y:.2f}' + elUnits,
                crosshairs: false,
                shared: false
            },
            //------------------------
            series: series_data
    });//highCharts
}

//------------------------
// General function for spatial summary
//------------------------
function generate_dailyTS(data_indices, running_mean_days) {
    /*
    Generates highcarts figure
    Required Args:
        datadict
        data_index: index of data in datadict
    Optional Args:
        if none is given, optional args  are obtained from datadict
        chartType, if none is given chartType is obtained from json file
    */
    var chartType = $('#chart_type').val();
    var datadict = graph_data;//template variable
    
    var axisFontSize = '16px';
    var labelsFontSize = '20px';

    //Define series data
    var series_data = []
    for (var i= 0;i<data_indices.split(',').length;i++){
        var s = {
            name: datadict[i].seriesName,
            color: datadict[i].series_color,
            data: datadict[i].data
        }
        series_data.push(s);
        //Add running Mean
        if (running_mean_days != '0'){
            var rm = {
                type:'trendline',
                linkedTo:':previous',
                algorithm: 'EMA',
                periods:parseInt(running_mean_days),
                name:running_mean_days + '-day Running Mean',
                color:datadict[i].running_mean_color,
                showInLegend: true
            }
            series_data.push(rm);
        }   
    }
    $('#container_' + data_index).highcharts({
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
        credits: {
            href: 'http://wrcc.dri.edu',
            text: 'wrcc.dri.edu'
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
                text: elUnits,
                style: {
                    fontSize: labelsFontSize,
                },
            },
            min: datadict[0].axisMin,
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
            pointFormat: '<b>Date: </b>{point.x:%b %e,%Y}<br><b>Value:</b> {point.y:.2f}'+ datadict[chartID].elUnits,
            crosshairs: false,
            shared: false
        },
        //------------------------
        series: series_data
      });//highCharts
};
