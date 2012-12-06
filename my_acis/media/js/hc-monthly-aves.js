$(function () {
    var defaultChart = {
        chartContent: null,
        highchart: null,
        defaults: {
            chart: {
                type: 'column'
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
                        this.x +': '+ this.y;
                }
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
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

    var Charts;
    $(document).ready(function() {
        var json_file = document.getElementById("json_file").value;
        var MEDIA_URL = document.getElementById("MEDIA_URL").value;
        var json_file_path = MEDIA_URL +'json/' + json_file;
        $.getJSON(json_file_path, function(datadict) {
            Charts = {

                chartContent: 'container',
                options: {

                    title: {
                         text: 'Monthly Averages for ' + datadict[0].element_long
                    },
                    subtitle: {
                        text: datadict[0].stn_name + ', ' + datadict[0].stn_id + ', ' + datadict[0].state + '<br/>' + 
                        'Date Range' + datadict[0].record_start  + ' - '+ datadict[0].record_end
                    },
                    yAxis: {
                    min: 0,
                    title: {
                        text: datadict[0].element + ' ' + datadict[0].units
                        }
                    },
                    series: [{
                        name: datadict[0].stn_name + ', ' + datadict[0].stn_id,
                        data: datadict[0].data

                    }]
                },
            };
            Charts = jQuery.extend(true, {}, defaultChart, Charts);
            Charts.init(Charts.options);
            Charts.create();
        }); //end getJSON
    }); // end doc ready
});//end top function
