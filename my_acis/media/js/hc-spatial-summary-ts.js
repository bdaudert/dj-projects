$(function () {
    $(document).ready(function() {
        var TMP_URL = document.getElementById("TMP_URL").value;
        var json_file_name = document.getElementById("json_file").value;
        var json_file = TMP_URL + json_file_name;
        $.getJSON(json_file, function(datadict) {
            var graph_title = datadict.search_params.graph_title,
            element_list = datadict.search_params.element_list,
            series_data,series,data,
            data_min,data_max,year,
            month,day,date,val, el_name, p_color;
            for (var el_idx=0;el_idx<element_list.length;el_idx++) {
                el_name = element_list[el_idx].split(' ')[0];
                p_color = set_plot_color(el_name);
                //Define plot data 
                series_data = [];
                series = {
                    'name':datadict.search_params.element_list_long[el_idx],
                    'color':p_color,
                    'marker':{'symbol':datadict.search_params.marker_type}
                };
                if (datadict.search_params.connector_line == 'F'){
                    series['lineWidth'] = 0;
                }
                else{
                    series['lineWidth'] = parseFloat(datadict.search_params.connector_line_width);
                }
                var barchart_els = 'pcpn snwd gdd hdd cdd';
                if (barchart_els.match(el_name)){
                    var dmm = set_plot_data(datadict.graph_data[el_idx],true, 999.0,'column');
                }
                else {
                    var dmm = set_plot_data(datadict.graph_data[el_idx],true, 999.0,'line');
                }
                var data = dmm.data;
                var x_cats = dmm.x_cats;
                var data_max = dmm.data_max;
                var data_min = dmm.data_min;
                series['data'] = data;
                series_data.push(series);
                //Running mean
                if (datadict.search_params.show_running_mean == 'T'){
                    series = {
                        'lineWidth':0.5,
                        'type':'spline',
                        'name':datadict.search_params.running_mean_days + '-Day Running Mean',
                        'color':'red', 'marker':{enabled:false}
                    };
                    if (barchart_els.match(el_name)){
                        var rm_data = compute_running_mean(data, datadict.search_params.running_mean_days,'column');
                    }
                    else {
                        var rm_data = compute_running_mean(data, datadict.search_params.running_mean_days,'line');
                    }  
                    series['data'] = rm_data;
                    series_data.push(series);
                }
                var plotline_no = null;
                if (datadict.search_params.minor_grid =='T'){
                    plotline_no = 10.0;
                }
                else if (datadict.search_params.major_grid =='T' && datadict.search_params.minor_grid == 'F'){
                    plotline_no = 5.0;
                }
                if (barchart_els.match(el_name)){
                    //overwrite plotlines and tick pos
                    x_props = set_barchart_axis_properties(data,plotline_no,'x');
                    //x_props = set_sodxtrmts_x_plotlines(data,'T', 'F');
                }
                else {
                    x_props = set_time_series_axis_properties(data, plotline_no,'x');
                }
                y_axis_props = set_y_axis_properties(data_max,datadict.search_params.vertical_axis_max, data_min, datadict.search_params.vertical_axis_min, element_list[el_idx],'none','F',plotline_no)
                //x_tickPositions = align_ticks(x_props.plotLines);
                y_tickPositions = align_ticks(y_axis_props.plotLines);
                var title = datadict.search_params.spatial_summary_long + '  ' +  datadict.search_params.element_list_long[el_idx];
                var subtitle = datadict.search_params.area_description;
                var x_axis_title = 'Start Date: ' + datadict.search_params.start_date+  ' End Date: ' + datadict.search_params.end_date; 
                var y_axis_title = datadict.search_params.element_list_long[el_idx]
                //Define Charts
                //Note: barchart for certain elements
                if (barchart_els.match(el_name)){
                    var ChartClass = new BarChart();
                    var Chart;
                    Chart = {
                        chartContent: 'spatial_summary_' + el_idx,
                        options: {
                            title: {
                                text: title
                            },
                            subtitle: {
                                text:subtitle
                            },
                            xAxis: {
                                categories:x_cats,
                                max:x_props.axisMax,
                                //min:x_props.axisMin,
                                plotLines:x_props.plotLines,
                                tickPositions:x_props.tickPositions,
                                labels: {
                                    rotation: -45,
                                    formatter:function () {
                                        return this.value;
                                    }
                                },
                                showLastLabel:true,
                                showFirstLabel:true,
                                tickWidth:0 
                            },
                            yAxis: [
                                {
                                    min: data_min,
                                    max: data_max,
                                    gridLineWidth:0,
                                    plotLines:y_axis_props.plotLines,
                                    title: {
                                        text:y_axis_title 
                                    }
                                },
                                {
                                    opposite:true,
                                    linkedTo:0,
                                    min: data_min,
                                    max: data_max,
                                    gridLineWidth:0,
                                    plotLines:y_axis_props.plotLines,
                                    title: {
                                        text:''
                                    }
                                }
                            ],
                            series:series_data
                        }
                    };                    
                }
                else {
                    var ChartClass = new TimeSeries();
                    var Chart;
                    Chart = {
                        chartContent:'spatial_summary_' + el_idx,
                        options: {
                            title: {
                                text: title
                            },
                            subtitle: {
                                text:subtitle
                            },  
                            xAxis: {
                                title:{
                                    text:x_axis_title
                                },
                                type: 'datetime',
                                maxZoom: 1 * 24 * 3600000, 
                                labels: {
                                    formatter: function () {
                                        return Highcharts.dateFormat('%Y-%m-%d', this.value);
                                    },
                                    //step:x_props.tickStep, 
                                    rotation: -45
                                },
                                plotLines:x_props.plotLines,
                                tickPositions:x_props.tickPositions,
                                min:x_props.axisMin,
                                max:x_props.axisMax,
                            },
                            yAxis: [{
                                title: {
                                    text:y_axis_title
                                },
                                max:y_axis_props.axisMax,
                                min:y_axis_props.axisMin,
                                plotLines:y_axis_props.plotLines,
                                tickPositions:y_tickPositions
                                //minorGridLineColor:minorGridLineColor
                            },
                            {
                                opposite: true,
                                linkedTo: 0,
                                title:'',
                                max:y_axis_props.axisMax,
                                min:y_axis_props.axisMin,
                                plotLines:y_axis_props.plotLines,
                                tickPositions:y_tickPositions
                                //minorGridLineColor:minorGridLineColor
                            }],
                            series:series_data 
                        }//end options
                    };//end Chart
                }
                Chart= jQuery.extend(true, {}, ChartClass.defaultChart, Chart);
                Chart.init(Chart.options);
                Chart.create();
            }//end for el_idx
        });//end getJSON
    });//end document ready function
});//end top function

