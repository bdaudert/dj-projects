$(function () {
    var HOST = document.getElementById('HOST').value;
    var HOST_URL = 'http://' + HOST + '/';
    var chart;
    $(document).ready(function() {
        var month_names =  ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        var TMP_URL = document.getElementById("TMP_URL").value;
        var json_file = document.getElementById("json_file").value;
        $.getJSON(TMP_URL + json_file, function(datadict) {
            //Read initial parameters
            var initial = datadict.initial;
            var initial_graph = datadict.initial_graph;
            var max_missing_days = parseInt(datadict.initial.max_missing_days);
            var running_mean_years = initial_graph.graph_running_mean_years;
            var plot_incomplete_years = initial_graph.graph_plot_incomplete_years;
            //Plot Options
            var major_grid = initial_graph.major_grid;
            var minor_grid = initial_graph.minor_grid;
            var marker_type = initial_graph.marker_type;
            var vertical_axis_min = initial_graph.vertical_axis_min;
            var vertical_axis_max = initial_graph.vertical_axis_max;
            var image_height = initial_graph.image_height;
            var connector_line_width = parseInt(initial_graph.connector_line_width);
            if (initial_graph.connector_line == 'F'){
                var connector_line_width = 0;
            }
            SummaryText =  set_summary_text(initial_graph.graph_summary) + datadict.monthly_statistic;
            
            //Set axes and text styles
            var top_dist = set_label_position(image_height);
            var axesStyle = set_style('#000000','12px','bold',null);
            var titleStyle = set_style('#000000','14px',null,null);
            var subtitleStyle = set_style('#0000FF','12px','bold',null);

            //Set chart type
            var chart_type = 'line';
            var barchart_els = 'pcpn snwd gdd hdd cdd';
            if (barchart_els.match(datadict.element)){
                chart_type = 'column';
            }
            //if (datadict.element == 'pcpn') {chart_type = 'column';}
            
            //Find indices list for given analysis start_month, 
            //graph_start_month and graph_end_month
            var d_idx_ml = set_date_idx_and_mon_list(initial,initial_graph);
            var month_list = d_idx_ml.month_list;

            //Find start/end_year index
            var yr_indices = set_start_end_yr_idx(datadict,initial,initial_graph);
           
            //Depending on graph summary, define series to be plotted
            //Find start end end index
            var Start = Date.UTC(parseInt(datadict.data[yr_indices.yr_start_idx][0]),0,01);
            var Interval = 365 * 24 * 3600000; // 1 year
            
            p_color = set_plot_color(datadict.element);

            //Set up series template
            var series = {
                'pointStart':Start,
                'pointInterval':Interval,
                'marker':{symbol:marker_type},
                'color':p_color,
                'lineWidth':connector_line_width
            };
            //Set series data
            if (initial_graph.markers == 'F'){series['marker'] = {enabled:false};}
            //Case 1 Plot: summary over Months
            if (initial_graph.graph_summary != 'individual'){
                    var sad = set_sodxtrmts_series_data_summary(datadict,initial,initial_graph,series,chart_type);
            }
            else { //Case2: Plot indiviual months
                var sad = set_sodxtrmts_series_data_individual(datadict,initial,initial_graph,series,chart_type);
            }
            var series_data = sad.series_data;
            var acis_data =sad.acis_data;
            var data_max = sad.data_max;
            var data_min = sad.data_min;
            var x_cats = sad.x_cats;
            //Set Plot Options
            var ChartTitle = datadict.stn_name + ', ' + datadict.stn_state + 
                ' ('  + datadict.stn_network + ' ID: '+datadict.stn_id + ')';
            if (initial_graph.graph_title != 'Use default'){ 
                ChartTitle = initial_graph.graph_title
            }
            var SubTitle = SummaryText + ' of ' +  datadict.element_name + ', Months: ' + 
                month_names[month_list[0] - 1] + ' to '+ month_names[month_list[month_list.length - 1] - 1];
            if (datadict.initial.departures_from_averages == "T"){
                SubTitle+=' (Departures from Average)'
            }
            var xAxisTitle = 'Year ' //+ datadict.data[datadict.data.length -7][0]
            if (month_list[0]> month_list[month_list.length -1]){
                xAxisTitle = 'Ending Year ' //+ datadict.data[datadict.data.length -8][0]
            }
            //Define x_axis properties
            //Sets new data for plotting,minor,major plotlines 
            admm = set_sodxtrmts_x_plotlines(acis_data,major_grid,minor_grid);
            //var dmm = set_yr_plotlines(acis_data);
            //Adjust plotlines in case there are too many data
            //var admm = adjust_x_plotlines(acis_data,dmm,major_grid, minor_grid);
            
            //Define y_axis properties
            var pn = admm.plotLines.length;
            pn = set_plotline_no(pn,major_grid, minor_grid);
            var vmx = initial_graph.vertical_axis_max;
            var vmn = initial_graph.vertical_axis_min;
            var el = datadict.element;
            var ms = datadict.initial.monthly_statistic;
            var da = datadict.initial.departures_from_averages;
            var y_axis_props = set_y_axis_properties(data_max,vmx,data_min,vmn,el,ms,da,pn);
            var y_tickPositions = align_ticks(y_axis_props.plotLines);

        
            //Create Plots, either bar chart or time series
            //Depending on the element 
            if ( chart_type == 'column'){
                //BarChart
                var ChartClass = new BarChart();
            }
            else{
                //TimeSeries
                var ChartClass = new TimeSeries();
            }

            //Set custom chart options
            var Chart;
            Chart = {
                chartContent:'container',
                //spacingBottom:50,
                //marginRigh:0,
                options: {
                    spacingBottom:50,
                    marginRigh:0,
                    title: {
                        text:ChartTitle,
                        style:titleStyle
                    },
                    subtitle: {
                        text:SubTitle,
                        style:subtitleStyle
                    },
                    tooltip: {
                        shared: true, 
                        formatter: function() {
                            var s = Highcharts.dateFormat('%Y', this.x);
                            $.each(this.points, function(i, point) {
                                s+= '<br />' + point.series.name + ': ' + point.y;
                            });
                            return s;
                        }
                    },
                    legend: {
                        enabled: true,
                        //layout: 'vertical',
                        align: 'left',
                        padding:20,
                        floating: true
                    },
                    xAxis:
                        {
                        categories:null,
                        title:{
                            text:xAxisTitle,
                            style:axesStyle
                        },
                        labels: {
                            rotation: -45,
                            formatter:function () {
                                return Highcharts.dateFormat('%Y', this.value);
                            }
                        },
                        //offset:2,
                        min:admm.min,
                        max:admm.max,
                        startOnTick: true,
                        showLastLabel:true,
                        showFirstLabel:true,
                        maxPadding:0,
                        plotLines:admm.plotLines,
                        tickPositions:admm.tickPositions
                    },
                    yAxis: [{
                        title: {
                            text:datadict.element_name
                        },
                        max:y_axis_props.axisMax,
                        min:y_axis_props.axisMin,
                        plotLines:y_axis_props.plotLines,
                        tickPositions:y_tickPositions,
                        tickInterval:y_axis_props.tickInterval,
                        startOnTick: true,
                        showFirstLabel: true,
                        showLastLabel: true
                    }, 
                    {
                        opposite:true,
                        linkedTo: 0,
                        title:'',
                        max:y_axis_props.axisMax,
                        min:y_axis_props.axisMin,
                        plotLines:y_axis_props.plotLines,
                        tickPositions:y_tickPositions,
                        tickInterval:y_axis_props.tickInterval,
                        startOnTick: true,
                        showFirstLabel: true,
                        showLastLabel: true
                    }
                    ],        
                    series:series_data
                }//end options
            };//end Chart
            
            //According to chart type set additional x_axis properties
            if (chart_type == 'line'){
                Chart.options.xAxis.type = 'datetime';
                Chart.options.xAxis.dateTimeLabelFormats = {year: '%Y'};
                Chart.options.xAxis.tickPositions = admm.tickPositions;
                Chart.options.xAxis.plotLines = admm.plotLines;
                Chart.options.yAxis.plotLines = y_axis_props.plotLines;
                Chart.options.yAxis.tickPositions = y_axis_props.tickPositions;
                Chart.options.yAxis.tickInterval = y_axis_props.tickInterval;
            }
            //Extend default chart with custom chart
            Chart= jQuery.extend(true, {}, ChartClass.defaultChart, Chart);
            Chart.init(Chart.options);
            Chart.create();
        });//end getJSON
    });//end document ready function
});//end top function

