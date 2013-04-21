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

    $(document).ready(function() {
        var json_file = document.getElementById("json_file").value;
        var JSON_URL = document.getElementById("JSON_URL").value;
        var json_file_path = JSON_URL + json_file;
        $.getJSON(json_file_path, function(datadict) {
            for (var i=0;i<datadict.length;i++){
                if (datadict[i].element == 'mint' || datadict[i].element == 'maxt'){
                    var min = -50;
                    var max = 130;
                }
                if (datadict[i].element == 'pcpn' || datadict[i].element == 'snow' || datadict[i].element == 'snwd'){
                    var min = 0;
                }
                if (datadict[i].element == 'hdd' || datadict[i].element == 'cdd' || datadict[i].element == 'gdd'){
                    var min = 0;
                }
                var j = i + 1
                var cntr = 'container' + j
                var Chart;            
                Chart = {

                chartContent: cntr,
                options: {

                    title: {
                         text: 'Monthly Averages for ' + datadict[i].element_long
                    },
                    subtitle: {
                        text: 'Date Range ' + datadict[i].record_start  + ' - '+ datadict[i].record_end
                    },
                    yAxis: {
                    min: min,
                    title: {
                        text: datadict[i].element + ' in ' + datadict[i].units
                        }
                    },
                    series: [{
                        name: datadict[i].stn_name + ', ' + datadict[i].stn_id + ', ' + datadict[i].state,
                        data: datadict[i].data

                    }]
                },
            };
            Chart= jQuery.extend(true, {}, defaultChart, Chart);
            Chart.init(Chart.options);
            Chart.create();
            }; //endfor
        }); //end getJSON
    }); // end doc ready
});//end top function
