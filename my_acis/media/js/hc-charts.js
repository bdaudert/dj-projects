function BarChart(xAxisCats) {
    this.xAxisCats = xAxisCats;
    this.style_axes = {
        color:'#000000',
        fontSize:'14px',
        fontWeight: 'bold'
    };
    this.style_text = {
        color:'#000000',
        fontSize:'18px'
    };
    this.Plotlines = []
    for (var val=0;val<xAxisCats.length;val++){
        var Plotline = {
            color: '#787878',
            dashStyle:'dash',
            width: 1,
            value: val,
        };
        this.Plotlines.push(Plotline);
    }
    this.defaultChart = {
        chartContent: null,
        highchart: null,
        defaults: {
            chart: {
                type: 'column',
                plotBorderWidth: 1
            },
            credits: {
                href: 'http://wrcc.dri.edu',
                text: 'http://wrcc.dri.edu'
            },
            title:{
                style:this.style_text
            },
            xAxis: {
                title: {
                    style: this.style_text
                },
                labels: {
                    style: this.style_axes, 
                    step:2
                },
                plotLines: this.Plotlines,
                tickInterval:1,
                categories: this.xAxisCats
            },
            yAxis: {
                title: {
                    style: this.style_text
                },
                labels: {
                    style: this.style_axes
                }
            },
            tooltip: {
                formatter: function() {
                    return ''+
                        this.x +': '+ this.y;
                }
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
        }, //end defaults
        // here you'll merge the defauls with the object options
        init: function(options) {
            this.highchart= jQuery.extend({}, this.defaults, options);
            this.highchart.chart.renderTo = this.chartContent;
        },
        create: function() {
            new Highcharts.Chart(this.highchart);
        }
    }//end defaultChart
}

