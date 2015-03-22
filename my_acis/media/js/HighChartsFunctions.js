function compute_summary(data, smry){
    var s, smry_data = [], ranges = [];
    for (i = 0;i<data[0].length;i++){
        var year_int = data[0][i][0];
        var vals_to_summarize = [];
        for (j=0;j<data.length;j++){
            vals_to_summarize.push(data[j][i][1]);
        }
        //Summarize
        var max = s = Math.max.apply(null,vals_to_summarize);
        var min = Math.min.apply(null,vals_to_summarize);
        if (vals_to_summarize.length >0){
            if (smry == 'mean'){
                s = Math.mean.apply(null,vals_to_summarize);
            }
            if (smry == 'sum'){
                s = Math.sum.apply(null,vals_to_summarize);       
            }
            if (smry == 'max'){
                s = max;
            }
            if (smry == 'min'){
                s = min;
            }
            if (smry == 'median'){
                s = Math.median.apply(null,vals_to_summarize);
            }
        }
        ranges.push[year_int, min, max];
        smry_data.push([year_int,s]);
    }
    return smry_data, ranges
}

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
    console.log(total);
    console.log(count);
    var average = (total / count);
    console.log(average);
    
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
    console.log(extx)
    console.log(exty)
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
    linkedTo: 'previous',
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

