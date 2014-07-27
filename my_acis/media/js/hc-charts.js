function BarChart() {
    this.style_axes = set_style('#000000','14px','bold',null);
    this.style_text = set_style('#000000','18px',null,null);
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
                text: 'wrcc.dri.edu'
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
                    step:1,
                    align:'left',
                },
                categories:null,
                minPadding: 0,
                maxPadding: 0,
                startOnTick: true,
                showFirstLabel:true,
                endOnTick:true
            },
            yAxis:[{
                title: {
                    style: this.style_text
                },
                labels: {
                    style: this.style_axes
                },
                startOnTick:false,
                showFirstLabel:true
            },
            {
                opposite: true,
                linkedTo: 0,
                title :{
                    text:'',
                    style:this.style_text
                },
                labels: {
                    style: this.style_axes
                }, 
                startOnTick:false,
                showFirstLabel:true

            }
            ],
            tooltip: {
                shared: true,
                formatter: function() {
                    var s = this.x;
                    $.each(this.points, function(i, point) {
                        s+= '<br />' + point.series.name + ': ' + point.y;
                    });
                    return s;
                }
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
        }, //end defaults
        //Functions
        set_yAxis_props: function(data_max,data_min, element) {
            //uses set_y_axis_properties from graph_utils.js
            return set_y_axis_properties(data_max,'Use default', data_min, 'Use default',element,'mave','F',10.0);
        },
        set_plotColor: function(element){
            //uses set_plot_color from graph_utils.js
            return set_plot_color(element);
        },
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

function TimeSeries(){
    this.style_axes = set_style('#000000','12px','bold',null);;
    this.style_title = set_style('#000000','14px',null,null);
    this.style_subtitle =set_style('#0000FF','15px',null,null);
    this.minorGridLineColor = set_style('#E0E0E0',null,null,null);
    this.gridLineWidth = 0;
    this.gridLineColor = set_style('#C0C0C0',null, null, null);
    this.defaultChart = {
        chartContent: null,
        highchart: null,
        defaults: {
            chart: {
                type:'line',
                zoomType: 'x'
            },
            credits: {
                href: 'http://wrcc.dri.edu',
                text: 'wrcc.dri.edu'
            },
            title: {
                style:this.style_title
            },
            subtitle: {
                style: this.style_subtitle
            },
            xAxis: {
                labels: {
                    /*
                    formatter: function () {
                        return Highcharts.dateFormat('%b%d\'%y', this.value);
                    },
                    */
                    style: this.style_axes
                },
                title : {
                    style: this.style_text,
                    text: 'Click and drag in the plot area to zoom in!'
                },
                gridLineWidth: this.gridLineWidth,
                gridLineColor: this.gridLineColor,
                showFirstLabel:true,
                endOnTick: true
            },
            yAxis: [{
                title: {
                    style:this.style_text
                },
                labels: {
                    style: this.style_axes
                },
                startOnTick: false,
                showFirstLabel: true,
                endOnTick: true,
                gridLineWidth: this.gridLineWidth,
                gridLineColor: this.gridLineColor
            },
            {
                opposite: true,
                linkedTo: 0,
                title:'',
                labels: {
                    style: this.style_axes
                },
                startOnTick: false,
                showFirstLabel: true
                //gridLineWidth: this.gridLineWidth,
                //gridLineColor: this.gridLineColor
            }],
            tooltip: {
                shared: true,
                formatter: function() {
                    var s = Highcharts.dateFormat('%Y-%m-%d', this.x);
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
}
