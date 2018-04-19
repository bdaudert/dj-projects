//Function to determine if variable is in list
String.prototype.inList=function(list){
   return ( list.indexOf(this.toString()) != -1)
}


function index_sums_years(index_sums,p1, pc1, a01, a11, temp_data, p2, pc2, a02,a12,temp_type, container) {
    $.getJSON(index_sums, function( index_ts ) {
        //Results of correlate_ts.py
        var reg_ind = [];
        for (var i=0; i<index_ts.length; i++){
            reg_ind.push(a01 + i*a11);
        }
        var reg_title_ind = 'Regression Index, pearson_coeff: ' + String(pc1) + ', p_value: ' + String(p1)  + ', slope/intercept: ' + a11 + '/' + a01;
        var temps_ts;
        $.getJSON(temp_data, function(t_data) {
            temp_ts = t_data;
            var reg_temp = [];
            for (var i=0; i<temp_data.length; i++){
                reg_temp.push(a02 + i*a12);
            }        
            var reg_title_temp = 'Regression Temperature, pearson_coeff: ' + String(pc2) + ', p_value: ' + String(p2)  + ', slope/intercept: ' + a12 + '/' + a02;            

            Highcharts.chart(container, {
                title: {
                    text: 'Index Sums and Mean Temperatures over domain'
                },
                subtitle: {
                    text: reg_title_ind + '<br>' + reg_title_temp
                },
                yAxis: [{
                    title: {
                        text: 'Mean sum of Index'
                    }, 
                },{
                    opposite: true,
                    gridLineWidth: 0,
                    title: {
                        text: temp_type + ' mean temperature'
                    }, 
                }],
                tooltip: {
                    shared: true
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle'
                },
                plotOptions: {
                    series: {
                        label: {
                            connectorAllowed: false
                        },
                        pointStart: 1951
                    }
                },
                series: [{
                        type: 'spline',
                        name: 'Mean Sum of Index',
                        data: index_ts, 
                        color: '#000000',
                    },
                    {
                        type: 'spline',
                        name: 'Mean ' + temp_type + ' Temperature',
                        data: temp_ts,
                        color: '#0000ff',
                        yAxis: 1
                    },
                    {
                        type: 'line',
                        name: 'Regression Index',
                        data: reg_ind,
                        color: '#708090'
                    }, 
                    {
                        type: 'line',
                        name: 'Regression Temperature',
                        data: reg_temp,
                        color: '#50a6c2',
                        yAxis: 1
                    }
                ]
            });
        });
    });
}

function index_aves_doys(index_aves, temp_data, temp_type, container){
    $.getJSON( index_aves, function( ts_data ) {
        var index_ts = ts_data;
        var temps_ts;
        $.getJSON(temp_data, function(t_data) {
            temp_ts = t_data;
            Highcharts.chart(container, {
                title: {
                    text: 'Mean over all years (1951 - 2011) for each day in season (Dec 1 = 1, Feb 28 = 90), averaged over all gridpoints'
                },
                subtitle: {
                    text: 'Index = number of Deg C below 5th percentile'
                },
                yAxis: [{
                    title: {
                        text: 'Mean sum of Index'
                    }
                },{
                    opposite: true, 
                    gridLineWidth: 0,
                    title: {
                        text: 'Mean temperature'
                    }
                }],
                tooltip: {
                    shared: true
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle'
                },
                plotOptions: {
                    series: {
                        label: {
                            connectorAllowed: false
                        },
                        pointStart: 1
                    }
                },
                series: [{
                    name: 'Mean Index',
                    data: index_ts
                }, 
                {
                    name: 'Mean ' + temp_type + ' Temperature',
                    data: temp_ts,
                    color: '#0000FF',
                    yAxis: 1
                }],
            });
        });
    });
}

function box_plot_sums_for_locations(data_file, container){
    $.getJSON( data_file, function( data ) {
        var locs = [], raw_data = [], plot_data = [];
        var max, min, median, lq, uq; 
        $.each(data, function(key, val) {
            locs.push(String(key));
            raw_data.push(val.sort(function(a, b){return a-b}));
        });
        $.each(raw_data, function(idx, lst) {
            max = lst.max();
            min = lst.min();
            median = lst.median();
            lq = percentile(lst, 25);
            uq = percentile(lst, 75);
            plot_data.push([min, lq, median, uq, max]);
        }); 
        Highcharts.chart(container, {
            chart: {
                type: 'boxplot'
            },
            title: {
                text: 'Box Plot Sums at 5 locations'
            },
            legend: {
                enabled: false
            },
            xAxis: {
                categories: locs,
                title: {
                    text: 'Locations'
                }
            },
            yAxis: {
                title: {
                    text: 'Index'
                }
            },
            series: [{
                name: 'Index over season',
                data: plot_data,
                tooltip: {
                    headerFormat: '<em>Location {point.key}</em><br/>'
                }
            }]
        });
    });
}

function box_plot_aves_for_locations(data_file, container){
    $.getJSON( data_file, function( data ) {
        var locs = [], raw_data = [], plot_data = [];
        var max, min, median, lq, uq;
        $.each(data, function(key, val) {
            locs.push(String(key));
            raw_data.push(val.sort(function(a, b){return a-b}));
        });
        $.each(raw_data, function(idx, lst) {
            max = lst.max();
            min = lst.min();
            median = lst.median();
            lq = percentile(lst, 25);
            uq = percentile(lst, 75);
            plot_data.push([min, lq, median, uq, max]);
        });
        Highcharts.chart(container, {
            chart: {
                type: 'boxplot'
            },
            title: {
                text: 'Box Plot Means at 5 locations'
            },
            legend: {
                enabled: false
            },
            xAxis: {
                categories: locs,
                title: {
                    text: 'Locations'
                }
            },
            yAxis: {
                title: {
                    text: 'Index'
                }
            },
            series: [{
                name: 'Locations',
                data: plot_data,
                tooltip: {
                    headerFormat: '<em>Location {point.key}</em><br/>'
                }
            }]
        });
    });
}


function box_plot_num_days(data_file, container){
    $.getJSON( data_file, function( data ) {
        var years = [], raw_data = [], plot_data = [];
        var max, min, median, lq, uq;
        $.each(data, function(key, val) {
            years.push(String(key));
            raw_data.push(val.sort(function(a, b){return a-b}));
        });
        $.each(raw_data, function(idx, lst) {
            max = lst.max();
            min = lst.min();
            median = lst.median();
            lq = percentile(lst, 25);
            uq = percentile(lst, 75);
            plot_data.push([min, lq, median, uq, max]);
        });
        Highcharts.chart(container, {
            chart: {
                type: 'boxplot'
            },
            title: {
                text: 'Number of days below 5th percentile'
            },
            legend: {
                enabled: false
            },
            xAxis: {
                categories: years,
                title: {
                    text: 'Years'
                }
            },
            yAxis: {
                title: {
                    text: 'Number of days'
                }
            },
            series: [{
                name: 'Years',
                data: plot_data,
                tooltip: {
                    headerFormat: '<em>Year {point.key}</em><br/>'
                }
            }]
        });
    });
}

function pca_ts(data_file, container, comp_idx){
    $.getJSON( data_file, function( ts_data ) {
        var data = [], i, d_utc, ymd_str, y, m, d;
        var t_step = 0;
        var tickpositions = [];
        var categories = [];
        var year_start_vals = [];
        for (i = 0; i < ts_data.length; i++){
            t_step+=1;
            ymd_str = ts_data[i][0].split('-');
            y = parseInt(ymd_str[0]);
            m = parseInt(ymd_str[1]) - 1;
            d = parseInt(ymd_str[2]);
            //console.log(String(y) + '-' + String(m) + '-' + String(d))
            d_utc = Date.UTC(y,m,d);
            val = ts_data[i][1]/ 100;
            //data.push([d_utc, val]);
            //data.push([t_step, val])
            data.push(val);
            categories.push(ts_data[i][0]);
            if (i % 90 == 0){
                tickpositions.push(ts_data[i][0]);
                year_start_vals.push([d_utc, val]);   
            }
        }
        Highcharts.chart(container, {
            chart: {
                zoomType: 'x'
            },
            title: {
                //text: 'PCA time series ' + String(comp_idx) + ' component'
                text:''
            },
            subtitle: {
                text: 'Click and drag in the plot area to zoom in'
            },
            xAxis: {
                /*
                type: 'datetime',
                dateTimeLabelFormats: { // don't display the dummy year
                    year: '%Y'
                },
                labels: {
                    enabled: false
                },
                */
                categories: categories,
                title: {
                    text: 'Date'
                }
            }, 
            yAxis: {
                title: {
                    text: 'Standard deviations'
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle'
            },
            series: [{
                name: 'PCA_' + String(comp_idx),
                data: data
                /*
                dataLabels: {
                    enabled:true,
                    formatter: function(){
                        for (i = 90; i < 5490; i+=90 ) {
                            if(this.point == this.series.data[i]){
                                return this.x
                            }
                        }
                        if(this.point === this.series.data[0]){
                            return this.x
                        }
                        if(this.point === this.series.data[this.series.data.length - 1]){
                            return this.x;
                        }
                    } 
                },
                */
            }]
        });
    });
}

function hist_aves(data_file, container){
    $.getJSON( data_file, function( data ) {
        var plot_data = data;
        Highcharts.chart(container, {
            title: {
                text: 'Histogram over index averages (all winter days, all location, 1951 - 2005)'
            },
            xAxis: [{
                title: { text: 'Data' },
                alignTicks: false
            }, {
                title: { text: 'Histogram' },
                alignTicks: false,
                opposite: true
            }],

            yAxis: [{
                title: { text: 'Data' }
            }, {
                title: { text: 'Histogram' },
                opposite: true
            }],

            series: [{
                name: 'Histogram',
                type: 'histogram',
                binsNumber: 20,
                xAxis: 1,
                yAxis: 1,
                baseSeries: 's1',
                zIndex: 1,
            }, {
                name: 'Data',
                visible: false,
                type: 'scatter',
                data: plot_data,
                id: 's1',
                zIndex: -1,
                marker: {
                    radius: 1.5
                }
            }]
        });
    });
}

function hist_sums(data_file, container){
    $.getJSON(data_file, function( data ) {
        var plot_data = data;
        Highcharts.chart(container, {
            title: {
                text: 'Histogram over index sums over winter (all location, 1951 -2005)'
            },
            xAxis: [{
                title: { text: 'Data' },
                alignTicks: false
            }, {
                title: { text: 'Histogram' },
                alignTicks: false,
                opposite: true
            }],

            yAxis: [{
                title: { text: 'Data' }
            }, {
                title: { text: 'Histogram' },
                opposite: true
            }],

            series: [{
                name: 'Histogram',
                type: 'histogram',
                binsNumber: 20,
                xAxis: 1,
                yAxis: 1,
                baseSeries: 's1',
                zIndex: 1
            }, {
                name: 'Data',
                visible: false,
                type: 'scatter',
                data: plot_data,
                id: 's1',
                zIndex: -1,
                marker: {
                    radius: 1.5
                }
            }]
        });
    });
}
