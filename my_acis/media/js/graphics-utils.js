function set_TitleStyle() {
    var style = {
        color:'#000000',
        fontSize:'14px'
    };
    return style;
}

function set_SubtitleStyle() {
    var style = {
        color:'#0000FF',
        fontSize:'14px',
        align:'center'
    };
    return style;
}

function set_AxesStyle() {
    var style = {
        color:'#000000',
        fontSize:'12px',
        fontWeight: 'bold'
    };
    return style;
}

function set_LabelStyle() {
    var style = {
        color:'#3E576F',
        fontSize:'14px'
    };
    return style;
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
            'minor_step':null, 
            'major_step':null, 
            'divisor':null
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



//Algoritmhms
function find_max(vals,element,statistic){
    var max = null;
    try{
        max = Math.max.apply(Math,vals);
    }
    catch(e){}
    if (statistic == 'ndays'){
        max = 35;
    }
    return max;
}

function find_min(vals, element,statistic, dep_from_ave){
    var min = null;
    if ((element == 'snow' || element == 'snwd' || element == 'pcpn' || element == 'evap' || element == 'wdmv') && (statistic !='ndays' && statistic !='sd' && dep_from_ave=='F')) {
        min = 0.0;
    }
    else{
        try{
            min = Math.min.apply(Math,vals);
        }
        catch(e){}
    }
    return min;
}

function find_closest_smaller(num, divisor){
    //Given num, this routine finds the closets smaller integer divisible by divisor
    var fl = Math.floor(num);
    var closest = null;
    while (closest == null ){
        if (fl % divisor == 0){
            closest =  fl;
        }
        else{
            fl = fl - 1;
        }
    }
    return closest;
}

function find_closest_larger(num, divisor){
    //Given num, this routine finds the closets larger integer divisible by divisor
    var cl = Math.ceil(num);
    var closest = null;
    while (closest == null ){
        if (cl % divisor == 0){
            closest =  cl;
        }
        else{
            cl = cl + 1;
        }
    }
    return closest;
}

function set_plotlines(data,step,axis,plotline_opts){
    /*
    data : [[x1,y1],[x2,y2], ...]
    if axis == 'x', set x_plotlines
    if axis == 'y', set y_potlines
    */
    //Sanity Check: step needs to be integer 
    //greater than zero
    var x_step = step;
    if (x_step === parseInt(x_step)){
        if (parseInt(x_step) < 1){
            x_step = 1;
        }
    }
    else{
        if (parseInt(x_step) < 1){
            x_step = 1;
        }
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
    return plotLines;
}

function set_yr_plotlines(data, plotline_opts){
    /*
    Given an array of data of form [[yr1, dat1],[yr2,dat2]] (where yr in acis format yyyy),
    returns new_data, major/minor plotlines (as datetime objects)
    where new_data = [[Date.UCT1, dat1],[Date.UTC2,dat2]]
    */
    //Find new axis_min/axis_max
    var yr_min = parseInt(data[0][0]);
    var yr_max = parseInt(data[data.length - 1][0]);
    var new_data = data;
    //Set step sizes and divisor(depends on data and data_length)
    var mmd = set_yrdata_grids(data.length);
    //Find closest axis points less/greater
    //than axis_min/axis_max  that are divisble by divisor
    var new_yr_min = find_closest_smaller(yr_min,mmd.divisor);
    var new_yr_max = find_closest_larger(yr_max,mmd.divisor);
    //make sure axis starts/end before/after first/last data point
    /*
    if (yr_min % mmd.divisor == 0){
        new_yr_min = find_closest_smaller(yr_min - 1,mmd.divisor);
    }
    if (yr_max % mmd.divisor == 0){
        new_yr_max = find_closest_larger(yr_max + 1,mmd.divisor);
    }
    */
    //Insert new data points at start/end
    for (idx=1;idx<=yr_min - new_yr_min;idx++){
        new_data.splice(0,0,[yr_min - idx, null]);
    }
    for (idx=1;idx<=new_yr_max - yr_max ;idx++){
        new_data.splice(new_data.length,0,[yr_max + idx, null]);
    }
    //Define plotlines
    var plotlines_minor = set_plotlines(new_data,mmd.minor_step,'x',plotline_opts);
    var plotlines_major = set_plotlines(new_data,mmd.major_step,'x',plotline_opts);
    return {
        'new_data':new_data,
        'plotlines_minor':plotlines_minor,
        'plotlines_major':plotlines_major
    };
}


function set_axis_properties(data_max,vertical_axis_max, data_min, vertical_axis_min, element,statistic, dep_from_ave,plotline_no){
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
    if ((element == 'snow' || element == 'snwd' || element == 'pcpn') && (statistic !='ndays' && statistic !='sd' && dep_from_ave=='F')) {
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
    for (val=props.axisMin;val<=props.axisMax + add_top*props.tickInterval;val+=props.tickInterval) {
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

function compute_running_mean(data, running_mean_points){
    var running_mean_data = [];
    if (running_mean_points%2 == 0){
        var num_nulls =running_mean_points/2 - 1;
    }
    else{
        var num_nulls =(running_mean_points - 1)/2;
    }
    for (var idx=0;idx<data.length;idx++) {
        var skip = 'F';
        if (idx >= num_nulls &&  idx <= data.length - 1 - num_nulls) {
            var cnt = 0;
            for(var i=idx - num_nulls,sum=0;i<=idx + num_nulls;i++){
                if (data[i][1] != null){
                    sum+=data[i][1];
                    cnt+=1;
                }
                else{
                    skip = 'T';
                    break;
                }
            }
            if (cnt > 0 && skip =='F'){
                running_mean_data.push([data[idx][0],precise_round(sum/cnt,2)]);
            }
            else{
                running_mean_data.push([data[idx][0],null]);
            }
        }
        else{
            running_mean_data.push([data[idx][0],null]);
        }
    }
    return running_mean_data
}
