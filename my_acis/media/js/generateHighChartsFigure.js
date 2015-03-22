//------------------------
// General function for monann
//------------------------
function generate_monTS(data_indices,smry,running_mean_years,show_range) {
    /*
    Generates highcarts figure
    Required Args:
        json_file_path
    Optional Args:
        (if not given, we take defaults from the json file)
        chartType: spline/scatter/line/spline/column/area
        data_indices: indices of months to be plotted
        smry: summary of individual indices: mean/sum/median/max/min or individual
        running_mean_years: number
        show_range: T or F
    */
    
     var datadict = graph_data; //template_variable
     var args = arguments;
     //Set default arguments
     var chartType = $('#chart_type').val();
     /*
     //Override default args with commandline args
     switch (args.length) { // <-- 1 (json_file_path) is number of required arguments
        case 1:
            chartType = args[0];
        case 2:
            chartType = args[0];
            data_indices = args[1];
        case 3:
            chartType = args[0];
            data_indices = args[1];
            smry = args[2];
        case 4:
            chartType = args[0];
            data_indices = args[1];
            smry = args[2];
            running_mean_years = args[3]; 
        case 5:
            chartType = args[0];
            data_indices = args[1];
            smry = args[2];
            running_mean_years = args[3];
            show_range = args[4];
    }
    */
    var axisFontSize = '16px';
    var labelsFontSize = '20px';
    //Define series data
    var series_data = [];
    if (smry == 'individual'){
        r_data = []
        for (var i = 0;i< data_indices.split(',').length;i++){
            var s = {
                type:chartType,
                name: datadict[i].seriesName,
                color: datadict[i].series_color,
                id:'data_' + String(i),
                data: datadict[i].data
            }
            series_data.push(s);
            r_data.push(datadict[i].data);
            //Add running means
            if (running_mean_years != '0'){
                var rm = {
                    type:'trendline',
                    linkedTo:':previous',
                    algorithm: 'EMA',
                    periods:parseInt(running_mean_years),
                    name: 'Running Mean: ' + datadict[i].seriesName,
                    color:datadict[i].running_mean_color,
                    showInLegend: true
                }
            }
            series_data.push(rm);
        }
        /*
        //Add range
        if (show_range == 'T'){
            s_data, r_data =  compute_summary(r_data,smry);
            var r = {
                name: 'Range',
                data:r_data,
                type: 'arearange',
                lineWidth: 0,
                linkedTo: ':previous',
                color: Highcharts.getOptions().colors[0],
                fillOpacity: 0.3,
                zIndex: 0
            }
            series_data.push(r)
        }
        */
    }
    if (smry != 'individual'){
         var months = '';smry_data = []
         for (var i = 0;i< data_indices.split(',').length;i++){
            months+= datadict[i].seriesName + ',';
            smry_data.push(datadict[i].data);   
         }
         //Get smry and range data
         var s_data, r_data = compute_summary(smry_data,smry);
         //Strip last comma
         months = months.splice(0,-1);
         var s = {
            name: smry.toUpperCase() + ' over months: ' + months,
            color: datadict[i].series_color,
            id:'primary',
            data:s_data
        }
        series_data.push(s)
        //Add Range
        if (show_range == 'T'){
            var r = {
                name: 'Range',
                data:r_data,
                type: 'arearange',
                lineWidth: 0,
                linkedTo: 'primary',
                color: Highcharts.getOptions().colors[0],
                fillOpacity: 0.3,
                zIndex: 0
            }
            series_data.push(r)
        }
        //Add running Mean
        if (running_mean_years != '0'){
            var rm = {
                type:'trendline',
                linkedTo:'primary',
                algorithm: 'EMA',
                periods:parseInt(running_mean_years),
                name: 'Running Mean:',
                color:datadict[i].running_mean_color,
                showInLegend: true
            }
            series_data.push(rm);   
        }
    }
    //CHART
    //Clear old plot

    $('#container').contents().remove();
    
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
        credits: {
            href: 'http://wrcc.dri.edu',
            text: 'wrcc.dri.edu'
        },
        //------------------------
        //    TITLE/SUBTITLE
        //------------------------
        title: {
            text: datadict.title,
        },
        subtitle: {
            text: datadict.subTitle,
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
                text: 'Period: ' + datadict.startDate + ' - ' + datadict.endDate,
                style: {
                    fontSize: labelsFontSize,
                },
            },
            labels: {
                format: '{value:%Y}',
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
                text: datadict.yLabel,
                style: {
                    fontSize: labelsFontSize,
                },
            },
            min: datadict.axisMin,
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
                text: datadict.legendTitle
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
                pointFormat: '<b>Year: </b>{point.x:%Y}<br><b>Value:</b> {point.y:.2f}'+datadict.elUnits,
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
function generate_dailyTS(data_index, running_mean_days) {
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
    var args = arguments;
    //Set defaults from datadict
    var data_index = '0';
    var chartID = parseInt(data_index);
    var chartType  = datadict[data_index][0].chartType;
    var running_mean_days = datadict[data_index][0].running_mean_days; 
    //Override defaults with commandline args if given
    switch (args.length) { // <-- 2 is number of required arguments
        case 1:
            data_index = args[0]; 
        case 2:
            data_index = args[0];
            chartType = args[2];
        case 3:
            data_index = args[0];
            chartType = args[2];
            running_mean_days = args[3];    
    }   
    var axisFontSize = '16px';
    var labelsFontSize = '20px';

    //Define series data
    var series_data = []
    for (var j= 0;j<datadict[chartID].length;j++){
        var s = {
            name: datadict[chartID][j].seriesName,
            color: datadict[chartID][j].series_color,
            data: datadict[chartID][j].data
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
                color:datadict[chartID][j].running_mean_color,
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
            pointFormat: '<b>Date: </b>{point.x:%b %e,%Y}<br><b>Value:</b> {point.y:.2f}'+ datadict[chartID].elUnits,
            crosshairs: false,
            shared: false
        },
        //------------------------
        series: series_data
      });//highCharts
};
