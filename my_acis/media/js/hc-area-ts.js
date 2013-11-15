$(function () {
    $(document).ready(function() {
        var JSON_URL = document.getElementById("JSON_URL").value;
        var json_file = document.getElementById("json_file").value;
        var file = JSON_URL + json_file;
        var axes_style = set_AxesStyle();
        var lable_style = set_LabelStyle();

        $.getJSON(file, function(datadict) {
            //Define Summary Text
            var SummaryText = datadict.summary
            var graph_title = datadict.graph_title;
            var element = datadict.search_params.element;
            //Define plot data 
            var series_data = [];
            var series = {'name':SummaryText,'color':'#00008B','marker':{'symbol':datadict.search_params.marker_type}};
            if (datadict.search_params.connector_line == 'F'){
                series['lineWidth'] = 0;
            }
            else{
                series['lineWidth'] = parseFloat(datadict.search_params.connector_line_width);
            }
            var data = []; 
            var data_max = -9999.0;
            var data_min = 9999.0;
            for (var date_idx=0;date_idx<datadict.data.length;date_idx++) {
                var year = parseInt(datadict.data[date_idx][0].slice(0,4));
                var month = parseInt(datadict.data[date_idx][0].slice(5,7)) - 1;
                var day = parseInt(datadict.data[date_idx][0].slice(8,10));
                var date = Date.UTC(year, month, day);
                var val = datadict.data[date_idx][1];
                if (val != '-----') {
                    try {
                        data.push([date, parseFloat(val)]);
                    }
                    catch (e) {
                        data.push([date, null]);
                    }
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
            }//end for
            series['data'] = data;
            series_data.push(series);
            //Running mean
            if (datadict.search_params.show_running_mean == 'T'){
                series = {'lineWidth':0.5,'name':datadict.search_params.running_mean_days + '-Day Running Mean','color':'red', 'marker':{enabled:false}};

                var rm_data = compute_running_mean(data, datadict.search_params.running_mean_days)
                series['data'] = rm_data
                series_data.push(series);
            }


            //Tick marks and plotlines
            //Set up divider for plotlines
            var plotline_no = null;
            var x_step = null;
            if (datadict.search_params.show_minor_grid =='T'){
                plotline_no = 10.0;
                var x_step = Math.round(datadict.data.length/plotline_no);
            }
            else if (datadict.search_params.show_major_grid =='T' && datadict.search_params.show_minor_grid == 'F'){
                plotline_no = 5.0;
                var x_step  = Math.round(datadict.data.length/plotline_no);
            }
            x_plotlines = set_plotlines(data,x_step,'x');
            x_tickPositions = align_ticks(x_plotlines);
            var x_tickStep = 1;
            if (x_plotlines.length > 10){
                x_tickStep = Math.round(x_plotlines.length/5.0);
            }
            y_props = set_axis_properties(data_max,datadict.search_params.vertical_axis_max, data_min, datadict.search_params.vertical_axis_min, element,'none',plotline_no)
            y_tickPositions = align_ticks(y_props.plotLines);
            var minorGridLineColor = '#E0E0E0';
            var gridLineWidth = 0;
            var gridLineColor = '#C0C0C0';
            var xAxisText = SummaryText + '  ' +  datadict.element_name + '<br >Start Date: ' + datadict.search_params.start_date+  ' End Date: ' + datadict.search_params.end_date;
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
                        fontSize:'15px'
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
                            style:axes_style,
                            step:x_tickStep,
                            formatter: function () {
                                return Highcharts.dateFormat('%b%d\'%y', this.value);
                            }
                        },
                        //lineColor:lineColor,
                        plotLines:x_plotlines,
                        tickPositions:x_tickPositions,
                        gridLineWidth: gridLineWidth,
                        gridLineColor: gridLineColor,
                        //type: 'datetime',
                        //maxZoom: 1 * 24 * 3600000, // 1 day
                        dateTimeLabelFormats: { // don't display the dummy year
                            year: '%Y',
                        },
                    }
                    ],
                yAxis: [
                    {
                        title: {
                            style:lable_style,
                            text: datadict.yAxisText
                        },
                        labels: {
                            style:axes_style
                        },
                        gridLineWidth:0,
                        gridLineColor: gridLineColor,
                        max:y_props.axisMax,
                        min:y_props.axisMin,
                        //lineColor:lineColor,
                        plotLines:y_props.plotLines,
                        tickPositions:y_tickPositions,
                        minorGridLineColor:minorGridLineColor,
                        //tickInterval:y_props.tickInterval,
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
                        max:y_props.axisMax,
                        min:y_props.axisMin,
                        //lineColor:lineColor,
                        plotLines:y_props.plotLines,
                        tickPositions:y_tickPositions,
                        minorGridLineColor:minorGridLineColor,
                        //tickInterval:y_props.tickInterval,
                        startOnTick: false,
                        showFirstLabel: true
                    }],
                tooltip: {
                    shared: true,
                    formatter: function() {
                        var s = Highcharts.dateFormat('%b%d\'%y', this.x);
                        $.each(this.points, function(i, point) {
                            s+= '<br />' + point.series.name + ': ' + point.y;
                        });
                        return s;
                    }   
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

