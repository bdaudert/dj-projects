$(function () {
    var stn_id = document.getElementById("stn_id").value;
    var stn_name = document.getElementById("stn_name").value
    var date_range = document.getElementById("date_range").value
    var state = document.getElementById("state").value;
    var element = document.getElementById("element").value;
    var MEDIA_URL = document.getElementById("MEDIA_URL").value;
    var defaultChart = {
        defaults: {
            chart: {
                renderTo: 'container',
                type: 'column'
            },
            title: {
                text: 'Monthly Averages'
            },
            subtitle: {
                text: stn_name + ', ' + stn_id + ', ' + state + '<br/>' + 'Date Range' + date_range 
            },
            xAxis: {
                categories: [
                    'Jan',
                    'Feb',
                    'Mar',
                    'Apr',
                    'May',
                    'Jun',
                    'Jul',
                    'Aug',
                    'Sep',
                    'Oct',
                    'Nov',
                    'Dec'
                ]
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Rainfall (in)'
                }
            },
            legend: {
                layout: 'vertical',
                backgroundColor: '#FFFFFF',
                align: 'left',
                verticalAlign: 'top',
                x: 100,
                y: 70,
                floating: true,
                shadow: true
            },
            tooltip: {
                formatter: function() {
                    return ''+
                        this.x +': '+ this.y +' in';
                }
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
                series: []
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
        for (var i=0;i<elements.length;i++)
        { 
            var Chart = {
                options: {
                    series: [{
                        name: stn_name + ', ' + stn_id,
                        data: results.i.data

                    }]
                },
            };
            Chart = jQuery.extend(true, {}, defaultChart, Chart);
            Chart.init(Chart.options);
            Chart.create();
        };
    });
    
});
