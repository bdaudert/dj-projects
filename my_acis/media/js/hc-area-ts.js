$(function () {
    var style_axes = set_AxesStyle();
    var style_text = set_TitleStyle();
    var minorGridLineColor = '#E0E0E0';
    var gridLineWidth = 0;
    var gridLineColor = '#C0C0C0';
    var defaultChart = {
        chartContent: null,
        highchart: null,
        defaults: {
            chart: {
                type:'line',
                zoomType: 'x',
                borderColor:'#006666',
            },
            credits: {
                href: 'http://wrcc.dri.edu/',
                text: 'wrcc.dri.edu'
            },
            title: {
                style:style_text
            },
            subtitle: {
                style: {
                    color:'#0000FF',
                    fontSize:'15px'
                }
            },
            xAxis: {
                labels: {
                    /*
                    formatter: function () {
                        return Highcharts.dateFormat('%b%d\'%y', this.value);
                    },
                    */
                    style: style_axes
                },
                title : {
                    style: style_text,
                    text: 'Click and drag in the plot area to zoom in!'
                },
                gridLineWidth: gridLineWidth,
                gridLineColor: gridLineColor
            },
            yAxis: [{
                title: {
                    style:style_text
                },
                labels: {
                    style: style_axes
                },
                startOnTick: false,
                showFirstLabel: true,
                gridLineWidth: gridLineWidth,
                gridLineColor: gridLineColor
            },
            {
                opposite: true,
                linkedTo: 0,
                labels: {
                    style: style_axes
                },
                startOnTick: false,
                showFirstLabel: true
                //gridLineWidth: gridLineWidth,
                //gridLineColor: gridLineColor
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
            },   
        },//end defaults
        // here you'll merge the defauls with the object options
        init: function(options) {
            this.highchart= jQuery.extend({}, this.defaults, options);
            this.highchart.chart.renderTo = this.chartContent;
        },
        create: function() {
            new Highcharts.Chart(this.highchart);
        }
    }; // end var defaultChart
 
    $(document).ready(function() {
        var JSON_URL = document.getElementById("JSON_URL").value;
        var json_file_name = document.getElementById("json_file").value;
        var json_file = JSON_URL + json_file_name;
        $.getJSON(json_file, function(datadict) {
            var graph_title = datadict.search_params.graph_title;
            var element_list = datadict.search_params.element_list;
            var series_data;
            var series;
            var data;
            var data_min;
            var data_max;
            var year;
            var month;
            var day;
            var date;
            var val;
            for (var el_idx=0;el_idx<element_list.length;el_idx++) {
                //Define plot data 
                series_data = [];
                series = {'name':datadict.search_params.element_list_long[el_idx],'color':'#00008B','marker':{'symbol':datadict.search_params.marker_type}};
                if (datadict.search_params.connector_line == 'F'){
                    series['lineWidth'] = 0;
                }
                else{
                    series['lineWidth'] = parseFloat(datadict.search_params.connector_line_width);
                }
                data = []; 
                data_max = -9999.0;
                data_min = 9999.0;
                for (var date_idx=0;date_idx<datadict.data[el_idx].length;date_idx++) {
                    year = parseInt(datadict.data[el_idx][date_idx][0].slice(0,4));
                    month = parseInt(datadict.data[el_idx][date_idx][0].slice(5,7)) - 1;
                    day = parseInt(datadict.data[el_idx][date_idx][0].slice(8,10));
                    date = Date.UTC(year, month, day);
                    val = datadict.data[el_idx][date_idx][1];
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

                    var rm_data = compute_running_mean(data, datadict.search_params.running_mean_days);
                    series['data'] = rm_data;
                    series_data.push(series);
                }
                //Tick marks and plotlines
                //Set up divider for plotlines
                var plotline_no = null;
                var x_step = null;
                var x_tickStep = 1;
                var y_props = {
                'axisMax':data_max,
                'axixMin':data_min,
                'plotLines':[]
                }
                var y_tickPositions = [];
                var x_tickPositions = [];
                var x_plotlines = [];
                if (datadict.search_params.minor_grid =='T'){
                    plotline_no = 10.0;
                    var x_step = Math.round(datadict.data[el_idx].length/plotline_no);
                }
                else if (datadict.search_params.major_grid =='T' && datadict.search_params.minor_grid == 'F'){
                    plotline_no = 5.0;
                    var x_step  = Math.round(datadict.data[el_idx].length/plotline_no);
                }
                x_plotlines = set_plotlines(data,x_step,'x');
                x_tickPositions = align_ticks(x_plotlines);
                if (x_plotlines.length > 10){
                    x_tickStep = Math.round(x_plotlines.length/5.0);
                }
                y_props = set_axis_properties(data_max,datadict.search_params.vertical_axis_max, data_min, datadict.search_params.vertical_axis_min, element_list[el_idx],'none',plotline_no)
                y_tickPositions = align_ticks(y_props.plotLines);
                //Define Chart
                var Chart;
                Chart = {
                    chartContent:'area_time_series_' + el_idx,
                    options: {
                        title: {
                            text: datadict.search_params.spatial_summary_long + '  ' +  datadict.search_params.element_list_long[el_idx]
                        },
                        subtitle: {
                            text:datadict.search_params.area_description
                        },
                        xAxis: {
                            title:'Start Date: ' + datadict.search_params.start_date+  ' End Date: ' + datadict.search_params.end_date,
                            type: 'datetime',
                            maxZoom: 1 * 24 * 3600000, 
                            labels: {
                                formatter: function () {
                                    return Highcharts.dateFormat('%b%d\'%y', this.value);
                                },
                                step:x_tickStep
                            },
                            //lineColor:lineColor,
                            plotLines:x_plotlines,
                            tickPositions:x_tickPositions
                        },
                        yAxis: [{
                            title: {
                                text: datadict.search_params.element_list_long[el_idx]
                            },
                            max:y_props.axisMax,
                            min:y_props.axisMin,
                            plotLines:y_props.plotLines,
                            tickPositions:y_tickPositions
                            //minorGridLineColor:minorGridLineColor
                        },
                        {
                            opposite: true,
                            linkedTo: 0,
                            max:y_props.axisMax,
                            min:y_props.axisMin,
                            plotLines:y_props.plotLines,
                            tickPositions:y_tickPositions
                            //minorGridLineColor:minorGridLineColor
                        }],
                        series:series_data 
                    }//end options
                };//end Chart
                Chart= jQuery.extend(true, {}, defaultChart, Chart);
                Chart.init(Chart.options);
                Chart.create();
            }//end for el_idx
        });//end getJSON
    });//end document ready function
});//end top function

