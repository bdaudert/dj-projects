$(function () {
    $(document).ready(function() {
        var JSON_URL = document.getElementById("JSON_URL").value;
        var json_file = document.getElementById("json_file").value;
        var file = JSON_URL + json_file;
        var axes_style = set_AxesStyle();
        var lable_style = set_LableStyle();

        $.getJSON(file, function(datadict) {
            //Define Summary Text
            var SummaryText = datadict.summary
            var graph_title = datadict.graph_title;
            var element = datadict.search_params.element;
            //Depending on summary, define series to be plotted
            var series_data = [];
            var x_plotlines = [];
            var y_plotlines = [];
            //var series = {'pointStart':pointStart,'pointInterval':Interval};
            var series = {'name':SummaryText,'color':'#00008B','marker':{'symbol':datadict.search_params.marker_type}};
            if (datadict.search_params.connector_line == 'F'){
                series['lineWidth'] = 0;
            }
            else{
                series['lineWidth'] = parseFloat(datadict.search_params.connector_line_width);
            }
            //Overwrite marker  if user doesn't want to see marker
            if (datadict.search_params.markers == 'T'){
                series['marker'] = {enabled:false};
            }
            //Define series data
            var data = [];
            var data_max = -9999.0;
            var data_min = 9999.0;
            for (var date_idx=0;date_idx<datadict.data.length;date_idx++) {
                var year = parseInt(datadict.data[date_idx][0].slice(0,4));
                var month = parseInt(datadict.data[date_idx][0].slice(5,7)) - 1;
                var day = parseInt(datadict.data[date_idx][0].slice(8,10));
                var date = Date.UTC(year, month, day);
                //Add vertical plot lines every 10 years or every year
                if (year%10 == 0 && date_idx > 0){
                    var plotline = {
                     color: '#787878',
                     dashStyle:'dash',
                     width: 1,
                     value: date,
                    };
                    x_plotlines.push(plotline);
                }
                //Define plot data 
                var date = date;
                var val =parseFloat(datadict.data[date_idx][1]);
                var pointStart = Date.UTC(2010,0,1)
                if (val != '-----') {
                    data.push([date, parseFloat(val)]);
                    if (val > data_max){
                        data_max = val;
                    }
                    if (val < data_min){
                        data_min = val;
                    }
                }
                else{
                    data.push([date, null]);
                }
            }
            series['data'] = data;
            series_data.push(series);

            //Running mean
            if (datadict.search_params.show_running_mean == 'T'){
                series = {'lineWidth':0.5,'name':datadict.search_params.running_mean_days + '-Day Running Mean','marker':{symbol:datadict.search_params.marker_type},'color':'red'};

                var rm_data = compute_running_mean(data, datadict.search_params.running_mean_days)
                series['data'] = rm_data
                series_data.push(series);
            }


            //Tick marks and y_axis plotlines
            if (datadict.search_params.show_major_grid =='F' && datadict.search_params.show_minor_grid == 'F'){
                var divider = null;
            }
            else if (datadict.search_params.show_minor_grid =='T'){
                var divider = 10.0;
            }
            else if (datadict.search_params.show_major_grid =='T' && datadict.search_params.show_minor_grid == 'F'){
                var divider = 5.0;
            }
            var tickInterval = set_tickInterval(data_max, data_min, divider);
            y_plotlines = set_plotLines(data_max, data_min, tickInterval, null);
            //var lineColor = '#C0D0E0';
            var minorGridLineColor = '#E0E0E0';
            var gridLineWidth = 1;
            var gridLineColor = '#C0C0C0';
            var xAxisText = SummaryText + '  ' +  datadict.element_name; 
            //Define Chart
            var chart = new Highcharts.Chart({
                chart: {
                    type:'line',
                    zoomType: 'x',
                    borderColor:'#006666',
                    borderWidth: 2,
                    renderTo: 'container',
                    //marginLeft: 60,
                    //marginBottom: 100,
                    //marginRigh:0 
                },
                title: {
                    style:lable_style,
                    text: graph_title
                },
                subtitle: {
                    text:xAxisText,
                    style: {
                        color:'#0000FF',
                        fontSize:15
                    }
                },
                credits: {
                        href: 'http://wrcc.dri.edu/',
                        text: 'wrcc.dri.edu'
                },
                xAxis: [
                    {
                        title : {
                            style:lable_style,
                            text: 'Click and drag in the plot area to zoom in!'
                        },
                        labels: {
                            style:axes_style
                        },
                        //lineColor:lineColor,
                        plotLines:x_plotlines,
                        gridLineWidth: gridLineWidth,
                        gridLineColor: gridLineColor,
                        type: 'datetime',
                        maxZoom: 1 * 24 * 3600000, // 1 day
                        dateTimeLabelFormats: { // don't display the dummy year
                            year: '%Y'
                        },
                    }
                    ],
                yAxis: [
                    {
                        title: {
                            style:lable_style,
                            text: datadict.element_name
                        },
                        labels: {
                            style:axes_style
                        },
                        gridLineWidth:0,
                        gridLineColor: gridLineColor,
                        //lineColor:lineColor,
                        plotLines:y_plotlines,
                        minorGridLineColor:minorGridLineColor,
                        tickInterval:tickInterval,
                        startOnTick: false,
                        showFirstLabel: true
                    },
                    {
                        opposite: true,
                        linkedTo: 0,
                        title: {
                            style:lable_style,
                            text: ' ' 
                        },
                        labels: {
                            style:axes_style
                        },
                        gridLineWidth:0,
                        gridLineColor: gridLineColor,
                        //lineColor:lineColor,
                        plotLines:y_plotlines,
                        minorGridLineColor:minorGridLineColor,
                        tickInterval:tickInterval,
                        startOnTick: false,
                        showFirstLabel: true
                    }],
                tooltip: {
                    shared: true
                },
                legend: {
                    enabled: true
                    //verticalAlign:'top'
                },
                series:series_data 
            });//end chart
        });//end getJSON
    });//end document ready function
    
});//end top function

