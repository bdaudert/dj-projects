function getAverage(chart) {
    //loop through data and build total/count to calculate average from
    //only use visible series
    var total = 0;
    var count = 0;
    $.each(chart.series, function(i,series) {
        if(series.visible === true && series.name != 'average') {
             $.each(series.data, function(i,point) {
                total += point.y;
                count++;
            });
        }
    });
    var average = (total / count);
    
    //if the average series already exists, remove it
    var avgSer = chart.get('average');
    if(avgSer != null) {
        avgSer.remove();
    }
    
    //get the axis extremes to use as the x values for the average series
    var ext = chart.xAxis[0].getExtremes();
    
    //add the average series
    chart.addSeries({
        id: 'average',
        name: 'average',
        showInLegend:true, 
        type:'line',
        lineWidth:1,
        color:'#c00',
        data:[[ext.min, average],[ext.max, average]]
    });
}

function getRange(chart) {
    //loop through data and build total/count to calculate min/max from
    //only use visible series
    //var minvalue = 0;
    //var count = 0;
    //$.each(chart.series, function(i,series) {
     //   if(series.visible === true && series.name != 'average') {
      //       $.each(series.data, function(i,point) {
     //           total += point.y;
     //           count++;
     //       });
     //   }
    //});

    //if the average series already exists, remove it
    var avgSer = chart.get('range');
    if(avgSer != null) {
        avgSer.remove();
    }

    //get the axis extremes to use as the x values for the average series
    var extx = chart.xAxis[0].getExtremes();
    var exty = chart.yAxis[0].getExtremes();
    chart.addSeries({
        id: 'range',
        name: 'range',
        showInLegend:false,
        type:'arearange',
        lineWidth:0,
        color:'#ff0000',
        data: [[extx.min, exty.dataMin, exty.dataMax],[extx.max, exty.dataMin,exty.dataMax]],
    fillOpacity: 0.1,
    zIndex:0.1,
    linkedTo: 'previous'
    });
}


function getRunningMean(chart,num) {
    var total = 0;
    var count = 0;
    var rm_data = [];
    $.each(chart.series, function(i,series) {
        if(series.visible === true && series.name != 'average') {
             $.each(series.data, function(i,point) {
                total += point.y;
                count++;
            });
        }
    });
    var average = (total / count);

    //if the average series already exists, remove it
    var avgSer = chart.get('runningMean');
    if(avgSer != null) {
        avgSer.remove();
    }

    //get the axis extremes to use as the x values for the average series
    var ext = chart.xAxis[0].getExtremes();

    //add the average series
    chart.addSeries({
        id: 'runningMean',
        name: 'runningMean',
        showInLegend:true,
        type:'line',
        lineWidth:1,
        color:'#c00',
        data:[[ext.min, average],[ext.max, average]]
    });
}

