//------------------------
// General function for monann
//------------------------
var myChart;
function generateTS_individual(data_indices) {
    /*
    Generates highcarts figure
    Required Args:
        data_indices: indices of data to be plotted,
        if not given, we pick it up from html element data_indices
    */
    var args = arguments;
    var datadict = graph_data; //template_variable
    switch (arguments.length) { // <-- 0 is number of required arguments
        case 0: var data_indices = $('#data_indices').val();
    }
    var app_name = '';
    if ($('#app_name').length){app_name=$('#app_name').val();}
    var running_mean_period = '0', smry = 'individual';
    //Get chart variables from template
    var chartType = $('#chart_type').val();
    var running_mean_period = $('#running_mean_period').val();
    var chartTitle = datadict[data_indices[0]].title;         
    var subTitle = datadict[data_indices[0]].subTitle;
    //Set font size
    var axisFontSize = '16px';
    var labelsFontSize = '20px';
    //Set params according to application 
    if (app_name == 'monann'){
        var date_format = '%Y';
        if ($('#monthly_statistic').val() == 'ndays'){
            var yLabelmain = 'days';
        }
        else {
            var yLabelmain = datadict[0].elUnits;
        }
    }
    if (app_name  == 'spatial_summary' || app_name == 'data_comparison'){
        var date_format = '%Y-%m-%d';
        var yLabelmain = datadict[0].seriesName + ' (' + datadict[0].elUnits + ')';
    }
    //predefine main yAxis
    var yAxes =[{
        gridLineWidth: 1,
        title: {
            text: yLabelmain, 
            style: {
                fontSize: labelsFontSize,
                color: Highcharts.getOptions().colors[0]
            }
        },
        min: datadict[data_indices[0]].axisMin,
        tickLength: 5,
        tickWidth: 1,
        tickPosition: 'outside',
        lineWidth:1,
        labels: {
            style: {
                fontSize: axisFontSize,
                zIndex: 6
            }
        }
    }];
   
    //When plotting multiple elements, change title/subtitle
    //And add yAxis for each element
    if (app_name == 'spatial_summary'){
        if (data_indices.length > 1){
            //Change chart title/subtitle
            var chartTitle = subTitle;
            var subTitle = $('#spatial_summary').val().toUpperCase();
            for (var i=1;i<data_indices.length;i++){
                var idx = data_indices[i];
                var yAxis = {
                    title: {
                        text: datadict[idx].seriesName + ' (' + datadict[idx].elUnits + ')',
                        style: {
                            color: Highcharts.getOptions().colors[idx]
                        }
                    },
                    labels: {
                        format: '{value}',
                        style: {
                            color: Highcharts.getOptions().colors[2*idx]
                        }
                    },
                    opposite: true
                }
                yAxes.push(yAxis);
            }
        }
    }
    //Define series data
    var series_data = [],idx;
    for (var i=0;i < data_indices.length;i++){
        idx = data_indices[i];
        var s_id = String(idx);
        var s = {
            type:datadict[idx].chartType,
            name: datadict[idx].seriesName,
            //color: datadict[idx].series_color,
            color:Highcharts.getOptions().colors[2*idx],
            id:'main_' + s_id,
            data: datadict[idx].data
        }
        //link to approprate axis if we are
        //plotting multiple elements
        if (app_name == 'spatial_summary' && idx > 0) {
            s['yAxis'] =  i;
        }
        series_data.push(s);
        //Add running mean
        if (running_mean_period != '0'){
            var rm_data =compute_running_mean(datadict[idx].data, parseInt(running_mean_period));
            var r_name = running_mean_period + '-';
            if (app_name == 'monann'){
                    r_name+='year Running Mean ';
            }
            else{
                    r_name+='day Running Mean ';
            }
            //Running mean
            var v = false
            if ($('#show_running_mean').is(':checked')){v = true;}
            var rm = {
                visible:v,
                id:'runmean_' + s_id,
                showInLegend:true,
                type:'line',
                lineWidth:1,
                color:Highcharts.getOptions().colors[2*i+1],
                name: r_name + s['name'],
                data:rm_data
            }
            series_data.push(rm);            
        }
        //Range
        var range_data = compute_range(datadict[idx].data);
        var v = false;
        if ($('#show_range').is(':checked')){v = true;};
        var r = {
            visible:v,
            id: 'range_' + s_id,
            name: 'Range:' + s['name'],
            showInLegend:false,
            type:'arearange',
            lineWidth:0,
            color:'#ff0000',
            data: range_data,
            fillOpacity: 0.1,
            zIndex:0.1,
            linkedTo: s_id,
        };
        series_data.push(r);
    }
    
    //Clear old plot
    $('#container').contents().remove();
    //CHART
    var basicOptions = {
        //------------------------
        //  CHART PROPERTIES
        //------------------------
        chart: {
            renderTo: 'container',
            type:  chartType,
            marginTop: 100,
            zoomType: 'x',
            spacingBottom: 30,
            spacingTop: 10,
            spacingLeft: 10,
            spacingRight: 10,
            borderWidth:1,
            borderColor: '#006666',
            plotBorderColor: '#346691',
            plotBorderWidth:1
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
        yAxis: yAxes,
        //------------------------
        //LEGEND
        //------------------------
        legend: {
            layout: 'vertical',
            backgroundColor: 'white',
            align: 'right',
            verticalAlign: 'top',
            y:10, // >0 moves down
            //x:0, // >0 moves right
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
                pointFormat: '<span style="color:{point.series.color}">{point.x:' +  date_format + '}: {point.y:.2f}</span><br />',
                crosshairs: false,
                shared: true
            },
            //------------------------
            series: series_data
    } //end basicOptions
    myChart=new Highcharts.Chart(basicOptions); 
}

function generateTS_smry(data_indices) {
    /*
    Generates highcarts figure
    Required Args:
        data_indices: indices of data to be plotted,
            if not given, we pick it up from html element data_indices 
    */
    var args = arguments;
    var datadict = graph_data; //template_variable
    switch (arguments.length) { // <-- 0 is number of required arguments
        case 0: var data_indices = $('#data_indices').val();
    }
    var running_mean_period = '0';
    //Get chart variables from template
    var chartType = $('#chart_type').val();
    running_mean_period = $('#running_mean_period').val();
    smry = $('#chart_summary').val();
    var date_format = '%Y-%m-%d';
    var chartTitle = datadict[data_indices[0]].title;
    var subTitle = datadict[data_indices[0]].subTitle
    if ($('#app_name').length && $('#app_name').val() == 'monann'){
        var date_format = '%Y';
    }
    var elUnits = datadict[0].elUnits;
    
    //Set font size
    var axisFontSize = '16px';
    var labelsFontSize = '20px';
    //Define series data
    var series_data = [],idx, s_id;
    var idx,names = '', to_summarize = []
    for (var i=0;i < data_indices.length;i++){
        idx = data_indices[i];
        names+= datadict[idx].seriesName + ',';
        to_summarize.push(datadict[idx].data);   
     }
    //Get smry and range data
    var smry_data = compute_summary(to_summarize,smry);
    //Strip last comma
    name = names.slice(0,-1);
    s_id = 'smry';
    var s = {
        name: smry.toUpperCase() + ' over: ' + names,
        //color: datadict[0].series_color,
        color:Highcharts.getOptions().colors[0],
        id:'main_' + s_id,
        data:smry_data.data
    }
    series_data.push(s)
    //Add running mean
    if (running_mean_period != '0'){
        var rm_data =compute_running_mean(smry_data.data, parseInt(running_mean_period));
        var r_name = running_mean_period + '-';
        if (app_name =='monann'){
                r_name+='year Running Mean ';
        }
        else{
                r_name+='day Running Mean ';
        }
        var v = false;
        if ($('#show_running_mean').is(':checked')){v = true;}
        //Running mean
        var rm = {
            visible:v,
            id:'runmean_' + s_id,
            showInLegend:true,
            type:'line',
            lineWidth:1,
            color:Highcharts.getOptions().colors[1],
            name: r_name + s['name'],
            data:rm_data
        }
        series_data.push(rm);
    }
    //Range
    var v = false
    if ($('#show_range').is(':checked')){v = true;}
    var range_data = compute_range(smry_data.data);
    var r = {
        visible:v,
        id: 'range_' + s_id,
        name: 'Range:' + s['name'],
        showInLegend:false,
        type:'arearange',
        lineWidth:0,
        color:'#ff0000',
        data: range_data,
        fillOpacity: 0.1,
        zIndex:0.1,
        linkedTo: s_id,
    };
    series_data.push(r);
    
    //Clear old plot
    $('#container').contents().remove();
    //CHART
    
    var basicOptions = {
        //------------------------
        //  CHART PROPERTIES
        //------------------------
        chart: {
            renderTo: 'container',
            type:  chartType,
            zoomType: 'x',
            spacingBottom: 30,
            spacingTop: 10,
            spacingLeft: 10,
            spacingRight: 10,
            borderWidth:1,
            borderColor: '#006666',
            plotBorderColor: '#346691',
            plotBorderWidth:1
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
            y: 10, // >0 moves down
            //x: -400, // >0 moves right
            borderWidth: 1,
            borderRadius: 5,
            floating: true,
            draggable: true,
            /*
            title:{
                text: ':: Drag me'
            },
            */
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
                pointFormat: '<span style="color:{point.series.color}">{point.x:'+  date_format +'}<b>: {point.y:.2f}' + elUnits + '</span><br />',
                crosshairs: false,
                shared: true
            },
            //------------------------
            series: series_data
    }//end basicOptions
    myChart=new Highcharts.Chart(basicOptions);
}

