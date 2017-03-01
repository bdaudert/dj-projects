//------------------------
// General function for monthly_summary
//------------------------
//Function to determine if variable is in list
String.prototype.inList=function(list){
   return ( list.indexOf(this.toString()) != -1)
}

var myChart;
var downloadMenu = $.extend(true,[],Highcharts.getOptions().exporting.buttons.contextButton.menuItems.splice(2));


function generateTS_individual(chart_indices) {
    /*
    Generates highcarts figure
    Required Args:
        chart_indices: indices of data to be plotted,
        if not given, we pick it up from html variable chart_indices
    */
    var args = arguments,
        datadict = graph_data; //template_variable
    try{
        var climoData = cp_data.climoData;
        var percentileData = cp_data.percentileData;
    }
    catch(e){}
    switch (arguments.length) { // <-- 0 is number of required arguments
        case 0: {
            var chart_indices = [];
            $('#chart_indices input:checked').each(function() {
                chart_indices.push($(this).val());
            });
        }
    }
    //Convert daat indices to list
    if (typeof chart_indices == 'string'){

        chart_indices = chart_indices.replace(', ',',').split(',');
    }
    var app_name = '';
    if ($('#app_name').length){app_name=$('#app_name').val();}
    var smry = 'individual';
    //Get chart variables from template
    var chartType = $('#chart_type').val();
    if ($('#running_mean_period').length){
        var running_mean_period = $('#running_mean_period').val();
    }
    else {
        var running_mean_period = '0';
    }
    if (app_name == 'data_comparison'){
        var chartTitle = datadict[chart_indices[0]].title + ';' + datadict[chart_indices[1]].title; 
    }
    else{
        if (chart_indices.length){
            var chartTitle = datadict[chart_indices[0]].title;
        }
        else{
            var chartTitle = '';
        }
    }
    var subTitle = datadict[chart_indices[0]].subTitle;
    //Set font size
    var axisFontSize = '16px';
    var labelsFontSize = '16px';
    //Set params according to application 
    if (app_name == 'monthly_summary' || app_name =='seasonal_summary'){
        var date_format = '%Y';
        if ( $('#statistic').length && $('#statistic').val() == 'ndays'){
            var yLabelmain = 'days';
        }
        else {
            var yLabelmain = datadict[0].elUnits;
        }
    }
    if (app_name  == 'spatial_summary' || app_name == 'data_comparison' || app_name =='single_year'){
        var date_format = '%Y-%m-%d';
        if (app_name == 'data_comparison'){
            var yLabelmain = datadict[0].yLabel;
        }
        else{
            var yLabelmain = datadict[0].seriesName + ' (' + datadict[0].elUnits + ')';
        }
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
        min: datadict[chart_indices[0]].axisMin,
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
   
    //When plotting multiple variables, change title/subtitle
    //And add yAxis for each variable
    if (app_name == 'spatial_summary'){
        if (chart_indices.length > 1){
            //Change chart title/subtitle
            var chartTitle = subTitle;
            var subTitle = 'Spatial Summary: ' + $('#spatial_summary').val().toUpperCase();
            for (var i=1;i<chart_indices.length;i++){
                var idx = chart_indices[i];
                var yAxis = {
                    title: {
                        text: datadict[idx].seriesName + ' (' + datadict[idx].elUnits + ')',
                        style: {
                            color: Highcharts.getOptions().colors[2*idx]
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
    //Single-Year climo and precentile data
    if (app_name == 'single_year'){
        //Find target_year
        if ($('#target_year_figure').length){
            var target_year = $('#target_year_figure').val();
        }
        else{
            var target_year = $('#target_year_form').val();
        }
        //Sanity check on Target year:

        //Climo data
        var v = false;
        if ($('#show_climatology').val() == 'T' || $('#climatology').is(':checked')){
            v = true;
        }
        var climo = {
            visible:v,
            showInLegend:v,
            id: 'climatology',
            name: '50% Percentile',
            data: climoData,
            color: '#000'
        }
        //Percentile Data
        var percentiles = ['5% -95%', '10% - 90%','25% - 75%'];
        var percentile_names = ['5','10','25'];
        var percentile_colors = ['#B7E2F0','#8FBAC8','#5D8896'];
        var perc = []
        for (var i=0; i< percentileData.length;i++){
            v = false;
            if ($('#show_percentile_' + percentile_names[i]).val() == 'T' || $('#percentile_' + percentile_names[i]).is(':checked')){
                v = true;
            }
            var p_name = percentiles[i];
            var p_id = percentile_names[i];
            var p_color = percentile_colors[i];
            var r = {
                visible:v,
                id: 'percentile_' + p_id,
                name: p_name + ' Percentile',
                showInLegend:v,
                type:'arearange',
                lineWidth:1,
                lineColor:'white',
                color:p_color,
                data: percentileData[i],
                fillOpacity: 0.6,
                zIndex:-1,
            };
            perc.push(r)
        }
    }
    var series_data = [],idx;
    for (var i=0;i < chart_indices.length;i++){
        idx = chart_indices[i];
        var s_id = String(idx);
        var s = {
            type:chartType,
            name: datadict[idx].seriesName,
            //color: datadict[idx].series_color,
            color:Highcharts.getOptions().colors[2*idx],
            id:'main_' + s_id,
            data: datadict[idx].data
        }
        //link to approprate axis if we are
        //plotting multiple variables
        if (app_name == 'spatial_summary' && idx > 0) {
            s['yAxis'] = i;
        }
        //Set threshold for seasonal_summary
        if (app_name != 'single_year'){
            var ave_data = compute_average(datadict[idx].data);
        }
        if (app_name == 'seasonal_summary'){
            //Precip/Snow/Evap colors
            s['threshold'] = ave_data[0][1].toFixed(2);
            s['color'] = 'blue';
            s['negativeColor'] = 'red';
            if ($('#variable').length && $('#variable').val().inList(['maxt','mint','avgt','obst'])){
                s['color'] = 'red';
                s['negativeColor'] = 'blue';
            }
            if ($('#variable').length && $('#variable').val().inList(['gdd','hdd','cdd'])){
                s['color'] = 'green';
                s['negativeColor'] = 'goldenrod';
            }
        }
        if (app_name == 'single_year'){
            if (String($('#start_year').val()).toLowerCase() == 'por'){
                var sy = $('#min_year').val();
            }
            else{
                var sy = $('#start_year').val()
            }
            if (parseInt(sy) + idx === parseInt(target_year)){
                s['visible'] = true;
                s['showInLegend'] = true;
            }
            else{
                s['visible'] = false;
                s['showInLegend'] = false;
            }
        }
        //Deal with skinny bar bug
        if (chartType == 'column'){
            s['stacking'] = null;
            if (app_name == 'monthly_summary' || app_name =='seasonal_summary'){
                s['pointRange'] = 1 * 24 * 3600*1000*365;
            }
            else{
                s['pointRange'] = 1 * 24 * 3600*1000;
            }
        }
        series_data.push(s);
        if (app_name == 'single_year'){
            if (parseInt(sy) + idx === parseInt(target_year)){
                series_data.push(climo);
                for (j=0;j < perc.length;j++){
                    series_data.push(perc[j]);
                }
            }
        }
           
        //Add running mean
        if (running_mean_period != '0'){
            var rm_data =compute_running_mean(datadict[idx].data, parseInt(running_mean_period));
            var r_name = running_mean_period + '-';
            if (app_name == 'monthly_summary' || app_name == 'seasonal_summary'){
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
                showInLegend:v,
                type:'line',
                lineWidth:1,
                color:Highcharts.getOptions().colors[2*i+1],
                name: r_name + s['name'],
                data:rm_data
            }
            series_data.push(rm);            
        }
        //Average over period
        var v = false;
        if ($('#show_average').length && $('#show_average').is(':checked')){v = true;};
        if (app_name != 'single_year'){
            var a = {
                visible:v,
                id: 'average_' + s_id,
                name: 'Average:' + s['name'],
                showInLegend:v,
                type:'line',
                lineWidth:1,
                color:'#ff0000',
                data: ave_data,
                linkedTo: s_id
            };
            series_data.push(a);
        }
        //Set average as initial threshold for seasonal_summary
        if (app_name == 'seasonal_summary'){
            $('#chart_threshold').val(ave_data[0][1].toFixed(2));
        }
        //Range
        if (app_name != 'single_year'){
            var range_data = compute_range(datadict[idx].data);
            var v = false;
            if ($('#show_range').is(':checked')){v = true;};
            var r = {
                visible:v,
                id: 'range_' + s_id,
                name: 'Range:' + s['name'],
                showInLegend:v,
                type:'arearange',
                lineWidth:0,
                color:'#ff0000',
                data: range_data,
                fillOpacity: 0.1,
                zIndex:0.1,
                linkedTo: s_id
            };
            series_data.push(r);
        }
    }
    
    //Clear old plot
    //$('#hc-container').contents().remove();
    //CHART
    var h = $(window).height();
    var basicOptions = {
        //------------------------
        //  CHART PROPERTIES
        //------------------------
        chart: {
            renderTo: 'hc-container',
            type:  chartType,
            height:h*0.7,
            marginTop:100,
            zoomType: 'x',
            spacingBottom: 30,
            spacingTop: 10,
            spacingLeft: 10,
            spacingRight: 10,
            //borderWidth:1,
            //borderColor: '#000000',
            plotBorderColor: '#000000',
            plotBorderWidth:1
        },
        credits: {
            href: 'http://wrcc.dri.edu',
            text: 'wrcc.dri.edu'
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
                dateFormat: date_format
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
        //------------------------
        //    TITLE/SUBTITLE
        //------------------------
        title: {
            text: chartTitle
        },
        subtitle: {
            text: subTitle
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
                    fontSize: labelsFontSize
                }
            },
            labels: {
                format: '{value:' + date_format  + '}',
                rotation: -45,
                //align: 'left',
                style: {
                    fontSize: axisFontSize,
                    zIndex: 6
                }
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
            draggable: true,
            layout: 'vertical',
            backgroundColor: 'white',
            align: 'left',
            verticalAlign: 'top',
            y:20,// >0 moves down
            //x:0, // >0 moves right
            borderWidth: 1,
            borderRadius: 5,
            padding:10,
            floating: true,
            title:{
                text: ':: Legend'
            },
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
                }
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
    myChart = new Highcharts.Chart(basicOptions);
}

function generateTS_smry(chart_indices) {
    /*
    Generates highcarts figure
    Required Args:
        chart_indices: indices of data to be plotted,
            if not given, we pick it up from html variable chart_indices 
    */
    var args = arguments,
        datadict = graph_data; //template_variable
    switch (arguments.length) { // <-- 0 is number of required arguments
        //case 0: var chart_indices = $('#chart_indices').val();
        case 0: {
            var chart_indices = [];
            $('#chart_indices input:checked').each(function() {
                chart_indices.push($(this).val());
            });
        }
    }
    //Convert daat indices to list
    if (typeof chart_indices == 'string'){
        chart_indices = chart_indices.replace(', ',',').split(',');
    } 
    var running_mean_period = '0';
    //Get chart variables from template
    var chartType = $('#chart_type').val();
    running_mean_period = $('#running_mean_period').val();
    smry = $('#chart_summary').val();
    var date_format = '%Y-%m-%d';
    var chartTitle = datadict[chart_indices[0]].title;
    var subTitle = datadict[chart_indices[0]].subTitle
    if ($('#app_name').length && $('#app_name').val() == 'monthly_summary'){
        var date_format = '%Y';
    }
    var elUnits = datadict[0].elUnits;
    
    //Set font size
    var axisFontSize = '16px';
    var labelsFontSize = '16px';
    //Define series data
    var series_data = [],idx, s_id;
    var idx,names = '', to_summarize = []
    for (var i=0;i < chart_indices.length;i++){
        idx = chart_indices[i];
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
        if (app_name =='monthly_summary'){
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
            showInLegend:v,
            type:'line',
            lineWidth:1,
            color:Highcharts.getOptions().colors[1],
            name: r_name + s['name'],
            data:rm_data
        }
        series_data.push(rm);
    }
    //Average over period
    var ave_data = compute_average(datadict[idx].data);
    var v = false;
    if ($('#show_average').is(':checked')){v = true;};
    var a = {
        visible:v,
        id: 'average_' + s_id,
        name: 'Average:' + s['name'],
        showInLegend:v,
        type:'line',
        lineWidth:1,
        color:'#ff0000',
        data: ave_data
    };
    series_data.push(a);
    //Range
    var v = false
    if ($('#show_range').is(':checked')){v = true;}
    if (app_name != 'single_year'){
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
            linkedTo: s_id
        };
        series_data.push(r);
    }
    //Clear old plot
    $('#hc-container').contents().remove();
    //CHART
    var h = $(window).height(); 
    var basicOptions = {
        //------------------------
        //  CHART PROPERTIES
        //------------------------
        chart: {
            renderTo: 'hc-container',
            type:  chartType,
            height:h*0.7,
            marginTop:100,
            zoomType: 'x',
            spacingBottom: 30,
            spacingTop: 10,
            spacingLeft: 10,
            spacingRight: 10,
            //borderWidth:1,
            //borderColor: '#000000',
            plotBorderColor: '#000000',
            plotBorderWidth:1
        },
        credits: {
            href: 'http://wrcc.dri.edu',
            text: 'wrcc.dri.edu'
        },
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
        //------------------------
        //    EXPORTING (CSV/EXCEL)
        //------------------------ 
        exporting: {
            csv: {
                dateFormat: date_format
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
        //------------------------
        //    TITLE/SUBTITLE
        //------------------------
        title: {
            text: chartTitle
        },
        subtitle: {
            text: subTitle
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
                    fontSize: labelsFontSize
                }
            },
            labels: {
                format: '{value:' + date_format  + '}',
                rotation: -45,
                //align: 'left',
                style: {
                    fontSize: axisFontSize,
                    zIndex: 6
                }
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
                    fontSize: labelsFontSize
                }
            },
            min: datadict[0].axisMin,
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
        },
        //------------------------
        //LEGEND
        //------------------------
        legend: {
            draggable:true,
            layout: 'vertical',
            backgroundColor: 'white',
            align: 'left',
            verticalAlign: 'top',
            y: 20, // >0 moves down
            //x: -400, // >0 moves right
            borderWidth: 1,
            borderRadius: 5,
            floating: true,
            title:{
                text: ':: Legend'
            },
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
                }
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
