function compute_running_mean(data, running_mean_points, chart_type){
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
                if (chart_type == 'column'){
                    var val = data[i];
                }
                else {
                    var val = data[i][1];
                }
                if (val != null){
                    sum+=val;
                    cnt+=1;
                }
                else{
                    skip = 'T';
                    break;
                }
            }
            if (cnt > 0 && skip =='F'){
                if (chart_type == 'column'){
                    running_mean_data.push(precise_round(sum/cnt,2));
                }
                else {
                    running_mean_data.push([data[idx][0],precise_round(sum/cnt,2)]);
                }
            }
            else{
                if (chart_type == 'column'){
                    running_mean_data.push(null);
                }
                else {
                    running_mean_data.push([data[idx][0],null]);
                }
            }
        }
        else{
            if (chart_type == 'column'){
                running_mean_data.push(null);
            }
            else {
                running_mean_data.push([data[idx][0],null]);
            }
        }
    }
    return running_mean_data
}


function set_plot_data(data, dates_true, miss_val,chart_type) {
    /*
    Converts data to barchart data
    Data is  a list of entries of form [x_val, y_val]
    if dates_true = true, we convert xcats to Date objects
    */
    results = {
        'xCats':[],
        'data':[],
        'data_max':-9999.0,
        'data_min':9999.0
    };
    for (var date_idx=0;date_idx< data.length;date_idx++) {
        try {
            var y_val = parseFloat(data[date_idx][1]);
        }
        catch (e) {
            var y_val = parseFloat(miss_val);
        }

        if (dates_true){
            var date = data[date_idx][0].replace('-','').replace('-','');
            try {
                var year = parseInt(date.slice(0,4));
                var month = parseInt(date.slice(4,6)) - 1;
                var day = parseInt(date.slice(6,8));
            }
            catch (e) {
                var year = 9999;
                var month = 0;
                var day = 1;
            }
            var x_val = Date.UTC(year, month, day);
        }
        else {
            var x_val = data[date_idx][0];
        }
        results.xCats.push(data[date_idx][0]);
        if (Math.abs(y_val - parseFloat(miss_val)) < 0.0001){
            if (chart_type == 'column') {
                results.data.push(null);
            }
            else {
                results.data.push([x_val,null]);
            }
        }
        else {
            if (chart_type == 'column') {
                results.data.push(y_val);
            }
            else {
                results.data.push([x_val, y_val]);
            }
            if (y_val > results.data_max){
                results.data_max = y_val;
            }
            if (y_val < results.data_min){
                results.data_min = y_val;
            }
        }
    }
    return results;
}


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

