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

function set_Labelstyle() {
    var style = {
        color:'#3E576F',
        fontSize:'14px'
    };
    return style;
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
        return [null, null, null];
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
    else if (10 < num_yrs){
        divisor = 10;
        minor = 5;
        major = 10;
    }
    return [minor, major, divisor];
}



//Algoritmhms
function find_max(vals,element){
    var max = null;
    try{
        max = Math.max.apply(Math,vals);
    }
    catch(e){}
    return max;
}

function find_min(vals, element){
    var min = null;
    if (element == 'snow' || element == 'snwd' || element == 'pcpn' || element == 'evap' || element == 'wdmv') {
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
        var pl = plotLine;
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
    var num_years = data.length;
    var yr_min = parseInt(data[0][0]);
    var yr_max = parseInt(data[num_years -1 ][0]);
    var new_data = data;
    /*
    //Replace Acis dates with Date.UTC
    for (yr_idx=0;yr_idx< new_data.length;yr_idx++){
        new_data[yr_idx][0] = Date.UTC(parseInt(data[yr_idx][0]), 0, 1);
    }
    */
    //Set step sizes and divisor(depends on data and data_length)
    var min_maj_div = set_yrdata_grids(num_years);
    //Find closest axis points less/greater
    //than axis_min/axis_max  that are divisble by divisor
    var new_yr_min = find_closest_smaller(yr_min,min_maj_div[2]);
    var new_yr_max = find_closest_larger(yr_max,min_maj_div[2]);
    //make sure axis starts/end before/after first/last data point
    if (yr_min % min_maj_div[2] == 0){
        new_yr_min = find_closest_smaller(yr_min - 1,min_maj_div[2]);
    }
    if (yr_max % min_maj_div[2] == 0){
        new_yr_max = find_closest_larger(yr_max + 1,min_maj_div[2]);
    }
    //Insert new data points at start/end
    for (idx=1;idx<=yr_min - new_yr_min;idx++){
        //new_data.splice(0,0,[Date.UTC(yr_min - idx,0,1), null]);
        new_data.splice(0,0,[yr_min - idx, null]);
    }
    for (idx=1;idx<=new_yr_max - yr_max;idx++){
        //new_data.concat([Date.UTC(yr_max + idx,0,1), null]);
        //new_data.concat([yr_max + idx, null]);
        new_data.splice(new_data.length,0,[yr_max + idx, null]);
    }
    //Define plotlines
    var plotlines_minor = set_plotlines(new_data,min_maj_div[0],'x',plotline_opts);
    var plotlines_major = set_plotlines(new_data,min_maj_div[1],'x',plotline_opts);
    return [new_data,plotlines_minor, plotlines_major]; 
}


function set_axis_properties(data_max, data_min, element,plotline_no){
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
    if (element == 'snow' || element == 'snwd' || element == 'pcpn') {
        props.axisMin = 0.0;
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
                upper = upper - props.tickInterval;
            }
            props.axisMax = props.axisMin + upper;
            break
        }
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
    //plotlines
    var plotLine = {
        color:'#787878',
        dashStyle:'dash',
        width: 0.5
    }
    for (val=props.axisMin;val<=props.axisMax + props.tickInterval;val+=props.tickInterval) {
        var pL = {};
        for (var key in plotLine){
            pL[key] = plotLine[key];
        }
        pL.value = val;
        props.plotLines.push(pL);
    }
    return props;
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
