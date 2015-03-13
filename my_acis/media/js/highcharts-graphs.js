highcharts_graphs = {
    data_comparison: function(divID,el) {
        var graph_data = gdata;
        var axis_min = null;
        var title = 'Grid/Station location: ' + graph_data.grid_location + '/' + graph_data.stn_location
        var y_label = graph_data.elements_long[el];
        var series_data =[]
        var s ={ 
            name:'grid',
            data:graph_data.data[el][0]
        };
        series_data.push(s);
        s = {
            name:'station',
            data:graph_data.data[el][1]
        };
        series_data.push(s);
        $('#' + divID).highcharts({
            chart: {
                zoomType: 'x'
            },
            credits: {
                href: 'http://wrcc.dri.edu',
                text: 'wrcc.dri.edu'
            }, 
            title: {
                text: title
            },
            subtitle: {
                text: graph_data.elements_long[el]
            },
            xAxis: {
                gridlineWidth: 1,
                type:'datetime',  
                title: {
                    text: 'Date'
                },
                labels: {
                    style: {
                        fontSize: '11px'
                    },
                    formatter: function() {
                        return Highcharts.dateFormat('%m/%e/%y',this.value.toFixed(2));
                    }
                }
            },
            yAxis: {
                gridLineWidth: 1,
                title: {
                    text: y_label
                },
                min: axis_min,
                tickLength: 5,
                tickWidth: 1,
                tickPosition: 'outside',
                lineWidth:1,
                labels: {
                    style: {
                    fontSize: '11px'
                    }
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            tooltip: {
                formatter: function() {
                    return  '<b>Long/Lat: ' + this.series.name +'</b><br/>' +
                    Highcharts.dateFormat('%m/%e/%Y',new Date(this.x)) + ': '+ this.y;
                }
            },
            series:series_data
        });
    } //end data_comparison
} //end highcharts_graphs
