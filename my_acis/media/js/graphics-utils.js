function set_style(color, fontSize, fontWeight, align) {
    var style = {
        color: color,
        fontSize:fontSize,
        fontWeight:fontWeight,
        align:align
    };
    return style;
}

function set_plot_color(element){
    if (element == 'maxt'){
        var p_color = '#660066';
    }
    if (element == 'mint'){
        var p_color = '#0000FF';
    }
    if (element == 'pcpn' || element == 'evap' || element == 'wdmv' || element == 'pet'){
        var p_color = '#008000';
    }
    if (element == 'snow' || element == 'snwd'){
        var p_color = '#800080';
    }
    if (element == 'hdd' || element == 'cdd' || element == 'gdd'){
        var p_color = '#00FFFF';
    }
    return p_color
}

function set_label_position(image_height){
    var top_dist = (parseFloat(image_height)*4/5).toString() +'px';
    if (Math.abs(parseFloat(image_height) -  290) < 0.001){
        //small image
        top_dist = (parseFloat(image_height)*3/4).toString() +'px';
    }
    if (Math.abs(parseFloat(image_height) -  480) < 0.001){
        //large image
        top_dist = (parseFloat(image_height)*5/6).toString() +'px';
    }
    if (Math.abs(parseFloat(image_height) -  610) < 0.001){
        //larger image
        top_dist = (parseFloat(image_height)*6/7).toString() +'px';
    }
    if (Math.abs(parseFloat(image_height) -  820) < 0.001){
        //extra large image
        top_dist = (parseFloat(height)*7/8).toString() +'px';
    }
    return top_dist;
}

function set_yrdata_grids(num_yrs){
    /*
    Sets major and minor grid step size and divisor
    data_type: data type
        Options:1. years, 2. months, 3. days
    num_data: length of data array 
    Output: [minor_grid_step, major_rid_step, divisor]
            divisor: defines the number that 
            the axis start/end points should be divisble by
    */
    //Case 0: no years
    if (num_yrs == 0){
        return {
            'minor_step':1, 
            'major_step':1, 
            'divisor':1
        };
    }
    //Case 1: less than 5 years
    var divisor = 5;
    var minor = 1;
    var major = 5;
    //Case 2: 5 to 10 years
    if (5 < num_yrs && num_yrs <= 10){
        divisor = 2;
        minor = 1;
        major = 2;
    }
    //Case 3: more than 10 years
    if (50 < num_yrs){
        divisor = 5;
        minor = 5;
        major = 10;
    }
    return {
        'minor_step':minor, 
        'major_step':major, 
        'divisor':divisor
        };
}

function set_plotlines(data,step,axis,plotline_opts){
    /*
    data : [[x1,y1],[x2,y2], ...]
    if axis == 'x', set x_plotlines
    if axis == 'y', set y_potlines
    */
    //Sanity Check: step needs to be integer 
    //greater than zero
    var stp = step;
    if (stp === parseInt(stp)){
        if (parseInt(stp < 1)){
        stp = 1;
        }
    }
    else{
        stp = 1;
    }
    if (axis == 'x'){idx = 0;}
    if (axis == 'y'){idx = 1;}
    var plotLines = [];
    if (!plotline_opts){
        var plotLine = {
            color:'#787878',
            dashStyle:'dash',
            width: 0.5
        }
    }
    else{
        var plotLine = plotline_opts;
    }
    for (dat_idx=0;dat_idx<data.length;dat_idx+=step){
        var pl ={};
        for (var key in plotLine){
            pl[key] = plotLine[key];
        }
        pl.value = data[dat_idx][idx];
        plotLines.push(pl);
    }

    //Push last plotline at end of data
    var pl ={};
    for (var key in plotLine){
        pl[key] = plotLine[key];
    }
    pl.value = data[data.length - 1][idx]
    plotLines.push(pl);
    return plotLines;
}

function set_yr_plotlines(data, plotline_opts){
    /*
    Given an array of data of form 
    [[yr1, dat1],[yr2,dat2]] (where yr in acis format yyyy),
    returns new_data, major/minor plotlines (as datetime objects)
    where new_data = [[Date.UCT1, dat1],[Date.UTC2,dat2]]
    */
    //Find new axis_min/axis_max
    var results = {
        'new_data':data,
        'plotlines_minor':[],
        'plotlines_major':[]
    }
    if (data.length){
        var yr_min = parseInt(data[0][0]);
        var yr_max = parseInt(data[data.length - 1][0]);
    }
    else{
        return results; 
    }
    //Set step sizes and divisor(depends on data and data_length)
    var mmd = set_yrdata_grids(data.length);
    //Find closest axis points less/greater
    //than axis_min/axis_max  that are divisble by divisor
    var new_yr_min = find_closest_smaller(yr_min,mmd.divisor);
    var new_yr_max = find_closest_larger(yr_max,mmd.divisor);
    //Insert new data points at start/end
    for (idx=1;idx<=yr_min - new_yr_min;idx++){
        new_data.splice(0,0,[yr_min - idx, null]);
    }
    for (idx=1;idx<=new_yr_max - yr_max ;idx++){
        new_data.splice(new_data.length,0,[yr_max + idx, null]);
    }
    results.new_data = new_data;
    //Define plotlines
    results.plotlines_minor = set_plotlines(new_data,mmd.minor_step,'x',plotline_opts);
    results.plotlines_major = set_plotlines(new_data,mmd.major_step,'x',plotline_opts);
    return results
}

function set_time_series_axis_properties(data,plotline_no,axis){
    results ={
        'tickStep':1,
        'tickPositions':[],
        'plotLines':[]
    }
    if (data.length == 0){
        var step = null;
    }
    else {
        var step = Math.round(data.length/plotline_no);
    }
    results.plotLines = set_plotlines(data,step,axis);
    results.tickPositions = align_ticks(results.plotLines);
    if (results.plotLines.length > 10){
        results.tickStep = Math.round(results.plotLines.length/5.0);
    }
    return results;
}

function set_barchart_axis_properties(data,plotline_no,axis){
    results ={
        'tickPositions':[],
        'plotLines':[],
        'axisMin':null,
        'axisMax':null
    }
    if (data.length == 0){return results;}
    var vals = data, step = 1,larger = 1, i;
    if (axis == 'x'){
        //need to convert categories to plotline values
        vals =[];
        for (i=0;i < data.length;i++){
            vals.push([i,null]);
        }
        results.axisMin = 0;
        larger = find_closest_larger(data.length, plotline_no + 1);
        step = larger / (plotline_no + 1);
        if (step == 0){step = 1;}
    }
    else {
        var d = [];
        for (var j;j<data.length;j++){
            d.push(data[j][1])
        }
        try {
            results.axisMax = Math.max(d);
            results.axisMax = find_closest_larger(results.axisMax , plotline_no);
            results.axisMin = Math.min(d);
            step = results.axisMax / plotline_no;
            if (step == 0){step = 1;} 
        } 
        catch (e) {}

    }
    results.plotLines = set_plotlines(vals,step,axis);
    for (var pl_idx=0;pl_idx<results.plotLines.length;pl_idx++) {
        var val = results.plotLines[pl_idx].value;
        if (axis == 'x'){
            //tickPositions for categories work by index
            //results.tickPositions.push(step*(pl_idx));
            results.tickPositions.push(val);
        }
        else{
            var val = results.plotLines[pl_idx].value;
            results.tickPositions.push(val);
        }
    }
    if (axis == 'x' && larger != data.length){
        results.plotLines.pop()
    }
    return results;
}

//axis property function for more complex graphs
function set_y_axis_properties(data_max,vertical_axis_max, data_min, vertical_axis_min, element,statistic, dep_from_ave,plotline_no){
    var props = {
        'axisMin':data_min,
        'axisMax':data_max,
        'tickInterval':null,
        'plotLines':[]
    };
    if (!plotline_no || data_max == null || data_min == null){
        return props;
    }
    if (Math.abs(data_max)<0.00001 && Math.abs(data_min)<0.00001){
        props.axisMin = -1.0;
        props.axisMax = 1.0;
        props.tickInterval = 0.5;
        return props; 
    }
    //Override data_min if necessary
    if ((element == 'snow' || element == 'snwd' || element == 'pcpn') && 
    (statistic !='ndays' && statistic !='sd' && dep_from_ave=='F')) {
        props.axisMin = 0.0;
    }

    if (statistic == 'ndays'){
        props.axisMax = 32;
    }
    var diff = Math.abs(props.axisMax - props.axisMin);
    //Deal with small differences
    steps = [0,plotline_no / 100, plotline_no / 50, plotline_no / 25,plotline_no / 10, plotline_no / 5, plotline_no / 2];
    for (idx=0;idx<=steps.length - 2 ;idx+=1){
        if (steps[idx] <= diff  && diff < steps[idx+1]){
            props.axisMin = Math.floor(props.axisMin);
            var upper = steps[idx+1];
            props.tickInterval = upper / plotline_no;
            //Make sure upper is close to max value
            while (upper - props.axisMax > props.tickInterval){
                if (upper < props.axisMax){
                    break
                }
                upper = precise_round(upper - props.tickInterval,2);
            }
            props.axisMax = props.axisMin + upper;
            break
        }
    }
    //Sanity check
    if (props.axisMax < data_max){
        props.axisMax = data_max;
    }

    //Larger  differences are treated differently
    if (plotline_no / 2 < diff && diff <=plotline_no){
        props.axisMin = Math.floor(props.axisMin);
        var upper = Math.ceil(props.axisMax) + 1;
        props.axisMax = upper;
        props.tickInterval = 1.0;
        
    }
    if (plotline_no < diff){
        props.axisMin = find_closest_smaller(props.axisMin,plotline_no);
        var upper = find_closest_larger(diff,plotline_no);
        props.axisMax = props.axisMin + upper;
        props.tickInterval = (props.axisMax - props.axisMin) / plotline_no;
        //Re-adjust upper is needed
        while (props.axisMin + upper - data_max < 0){
            upper = upper + props.tickInterval;
        }
        while (Math.abs(props.axisMin + upper - data_max) > props.tickInterval){
            upper = upper - props.tickInterval;
        }
        while (data_min - props.axisMin > props.tickInterval){
            props.axisMin = props.axisMin + props.tickInterval;
        }
        props.axisMax = props.axisMin + upper;
    }
    //Sanity check
    while (Math.abs(data_max) > Math.abs(props.axisMax)){
        props.axisMax+=props.tickInterval;
    }
    //Override max/min custom requested by user
    var add_top = 0;
    if (vertical_axis_max != "Use default") {
        try{
            props.axisMax = parseFloat(vertical_axis_max);
            add_top = 1;
        }   
        catch(e){}
    }
    if (vertical_axis_min != "Use default") {            
        try{
            props.axisMin = parseFloat(vertical_axis_min);
        }
        catch(e){}
    }
    if (statistic == 'ndays'){
        props.axisMax = 31;
    }
    //plotlines
    var plotLine = {
        color:'#787878',
        dashStyle:'dash',
        width: 0.5
    }
    //if (add_top == 0 && props.axisMax < 1){add_top = 1;}
    for (val=props.axisMin;parseInt(100*val)<=parseInt(100*(props.axisMax + add_top*props.tickInterval));val+=props.tickInterval) {
        var pL = {};
        for (var key in plotLine){
            pL[key] = plotLine[key];
        }
        //rounding
        var intRegex = /^\d+$/;
        if (0 <= props.tickInterval && props.tickInterval < 0.1 ){
            var v = precise_round(val,2);
        }
        else if (0.1 <= props.tickInterval && !intRegex.test(val)){
            var v = precise_round(val,1);
        }
        else{
            var v = val;
        }
        /*
        if (0 <= val && val < 0.1 ){
            var v = precise_round(val,2);
        }
        else if (0.1 <= val && !intRegex.test(val)){
            var v = precise_round(val,1);
        }
        else{
            var v = val;
        }
        */
        if (v > props.axisMax && vertical_axis_max != "Use default"){
            try{
                v = parseFloat(vertical_axis_max);
            }
            catch(e){}
            //continue;
        }
        pL.value = v;
        props.plotLines.push(pL);
    }
    return props;
}

function align_ticks(plotlines){
    //Aligns axis ticks with plotlines
    tickPositions = [];
    for (idx=0;idx<plotlines.length;idx++){
        var tp = plotlines[idx].value;
        tickPositions.push(tp);
    }
    return tickPositions;
}

function set_tickInterval(data_max, data_min, divider){
    //scale/re-scale in case data_max, data_min are too small
    if (!divider || data_max == null || data_min == null || (Math.abs(data_max)<0.00001 && Math.abs(data_min)<0.00001)){
        return null;
    }
    //var tickInterval = (Math.abs(parseFloat(100*data_max) - parseFloat(100*data_min)))/ parseFloat(divider);
    //tickInterval = Math.round(tickInterval) / parseFloat(100);
    var tickInterval = (Math.abs(data_max - data_min))/divider;
    if (0.0 <= tickInterval && tickInterval < 0.1){
        tickInterval = precise_round(tickInterval, 2);
    }    
    else if (tickInterval > 1){
        //tickInterval = precise_round(tickInterval, 0);
        tickInterval = Math.ceil(tickInterval);
    }
    else {
        tickInterval = 1;
    }
    return tickInterval;
}

function set_plotline_no(pn_init,major_grid, minor_grid){
    var pn = pn_init;
    if (pn > 20){
        if (major_grid =='F' && minor_grid == 'F'){
            var pn  = 1.0;
        }
        else if (minor_grid =='T'){
            var pn = 10.0;
        }
        else if (major_grid =='T' && minor_grid == 'F'){
            var pn = 5.0;
        }
    }
    return pn;
}

function set_plotLines(data_max, data_min, tickInterval, options_dict){
    var plotLines = []
    if (!options_dict){
        var plotLine = { 
            color:'#787878',
            dashStyle:'dash',
            width: 0.5
        }
    }
    else{
        var plotLine = options_dict;
    }
    if (Math.abs(tickInterval)<0.00001 || (Math.abs(data_max)<0.00001 && Math.abs(data_min)<0.00001)){
        return null
    }
    for (val=data_min;val<=data_max;val+=tickInterval) {
        var pL = {};
        for (var key in plotLine){
            pL[key] = plotLine[key];
        }
        if (0.0 <= tickInterval && tickInterval < 0.1){
            var v = precise_round(val,2);
        }
        else if (tickInterval >1){
            var v = precise_round(val,0);
        }
        else{
            var v = precise_round(val,1);
        }
        pL.value = v;
        plotLines.push(pL);
    }
    if (plotLines.length == 0){
        return null
    }
    else{
        return plotLines;
    }
}

//Sodxtrmts Utils
function set_sodxtrmts_x_plotlines(data,major_grid, minor_grid){
    /*
    Data is of form
    [[yr1, dat1],[yr2,dat2], ...] 
    where yr in acis format yyyy
    */
    var results = {
        'plotLines':[],
        'tickPositions':[],
        'axisMin':null,
        'axisMax':null,
    };
    if (!data.length){return results;}
    results.axisMin = parseInt(data[0][0]);
    results.axisMax = parseInt(data[data.length - 1][0]);
    //Start with step for minor grid
    var step = 1, 
    div = find_largest_divisor(data.length);
    if (minor_grid == 'F' && major_grid == "T"){
        if (data.length % 2 == 0){
            //Even number of data points
            step = 2;
        }
        else {
            //Odd number of data points
            if (div == data.length){
                step = 1;
            }
            else {
                step = data.length / div;
            }
        }
    }
    else if (major_grid == "F" && minor_grid == "F"){
        step = data.length - 1;
    }
    //Adjust step if dataset is large
    if (data.length > 50 && data.length <= 100){
        if (minor_grid == 'T'){
            step = 5;
        }
        if (major_grid == 'T' && minor_grid == 'F'){
            step = 10;
        }
    }
    else if (data.length > 100){
        if (minor_grid == 'T'){
            step = 10;
        }
        if (major_grid == 'T' && minor_grid == 'F'){
            step = 20;
        }
    }
    if (parseInt(data[data.length - 1][0]) % step != 0){
        results.axisMax = find_closest_larger(parseInt(data[data.length - 1][0]),step);
    }
    var pls = set_plotlines(data,step,'x');
    //convert to Date
    for (var pl_idx=0;pl_idx<pls.length;pl_idx++) {
        var pl ={};
        for (var key in pls[pl_idx]){
            pl[key] = pls[pl_idx][key];
        }
        pl.value = Date.UTC(pls[pl_idx].value,0,1);
        if (major_grid =='F' && minor_grid == 'F'){
            if (pl_idx ==0 || pl_idx == pls.length -1){
                    results.plotLines.push(pl);
            }
        }
        else {
            results.plotLines.push(pl);
        }
        results.tickPositions.push(pl.value);
    }
    return results; 
}

function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

function set_color_bar(min,max,palette) {
    var hex_color_list = palette.split(','),
    cb  = document.getElementById('colorbar'),
    ctx = cb.getContext('2d'),
    cb_width = parseInt(cb.width),
    cb_height = parseInt(cb.height),
    x_step = Math.floor(cb_width / hex_color_list.length);
    for(var i = 0; i < hex_color_list.length; i++) {
        rgb = hexToRgb('#' + hex_color_list[i]);
        ctx.beginPath();
        var color = 'rgb(' + rgb.r + ', ' + rgb.g + ', ' + rgb.b + ')',
        grd = ctx.createLinearGradient(i*x_step,0,(i+1)*x_step,0); //Gradient
        grd.addColorStop(0,'#' + hex_color_list[i]);
        try {
            grd.addColorStop(1,'#' + hex_color_list[i+1]);
        }
        catch(e){
            grd.addColorStop(1,'#' + hex_color_list[i]);
        }
        //ctx.fillStyle = color;
        ctx.fillStyle = grd;
        ctx.fillRect(i * x_step, 0, x_step, cb_height);
        //Text adding does not work for me, interediate solution: click function
        /* 
        ctx.font="14px Verdana black";
        var data_diff = Math.abs(parseFloat(max) - parseFloat(min)),
        data_step = Math.floor(data_diff /  (hex_color_list + 1)),
        tick = String(Math.floor(min + i*data_step));
        ctx.fillText(tick,i*x_step,cb_height);
        */
    }

    cb.onclick = function(e) {
        var x = e.offsetX;
        var data_val = Math.abs(parseFloat(max) - parseFloat(min)) * x /(cb_width);
        alert(data_val);
    };
}
