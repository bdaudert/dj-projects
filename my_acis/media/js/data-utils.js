function findMedian(data) {

    // extract the .values field and sort the resulting array
    var m = data.map(function(v) {
        return v;
    }).sort(function(a, b) {
        return a - b;
    });

    var middle = Math.floor((m.length - 1) / 2); // NB: operator precedence
    if (m.length % 2) {
        return m[middle];
    } else {
        return (m[middle] + m[middle + 1]) / 2.0;
    }
}

function findSum(data){
    var sum = null;
    if (data.length > 0) {
        sum = data.reduce(function(a,b) {
            return a + b;
        });
    }
    return sum
}

function compute_summary(data, smry){
    smry_data = {
        'data':[],
        'ranges':[]
    };
    //time period loop
    for (i = 0;i<data[0].length;i++){
        var date_int = data[0][i][0];
        var vals_to_summarize = [];
        //data loop
        for (j=0;j<data.length;j++){
                try{ var val = data[j][i][1]; }
                catch(e){ var val = null; }

                if (val != null){
                    vals_to_summarize.push(data[j][i][1]);
                }
        }
        //Summarize
        var max = Math.max.apply(null,vals_to_summarize);
        var min = Math.min.apply(null,vals_to_summarize);
        if (min == Number.POSITIVE_INFINITY || min == Number.NEGATIVE_INFINITY){
            min = null;
        }
        if (max == Number.POSITIVE_INFINITY || max == Number.NEGATIVE_INFINITY){
            max = null;
        }
        var sum = findSum(vals_to_summarize);
        var s = null;
        if (vals_to_summarize.length >0){
            if (smry == 'mean'){
                if (vals_to_summarize.length > 0  && sum != null) {
                    s =  sum / vals_to_summarize.length;
                }
            }
            if (smry == 'sum'){
                s = sum;
            }
            if (smry == 'max'){
                s = max;
            }
            if (smry == 'min'){
                s = min;
            }
            if (smry == 'median'){
                s = findMedian(vals_to_summarize);
            }
        }
        smry_data.ranges.push([date_int, min, max]);
        smry_data.data.push([date_int,s]);
    }
    return smry_data
}

function compute_running_mean(data,running_mean_period){
    var running_mean_data = [];
    if (running_mean_period%2 == 0){
        var num_nulls =running_mean_period/2 - 1;
    }
    else{
        var num_nulls =(running_mean_period - 1)/2;
    }
    for (var idx=0;idx<data.length;idx++) {
        var skip = 'F';
        var rm_data = [];
        if (idx >= num_nulls &&  idx <= data.length - 1 - num_nulls) {
            var cnt = 0;
            for(var i=idx - num_nulls,sum=0;i<=idx + num_nulls;i++){
                var val = data[i][1];
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
                rm_data = [data[idx][0],parseFloat(sum)/parseFloat(cnt)];
            }
        }
        if (rm_data.length > 0){
            running_mean_data.push(rm_data);
        }
    }
    return running_mean_data
}

function compute_average(data){
    var sum=0, ave= null; var count = 0;
    for (var idx = 0;idx<data.length;idx++){
        d = data[idx][1];
        if (String(d) != '-9999' && d != null){
            try {
                sum+= parseFloat(d);
                count+=1;
            }
            catch(e){}
        }
    }
    if (count > 0){
        ave = sum / parseFloat(count);
    }
    return [[data[0][0], ave], [data[data.length -1][0], ave]]
}

function compute_range(data){
    var d,dt = [],mx = null, mn = null;
    for (var idx = 0;idx<data.length;idx++){
        d = data[idx][1];
        if (String(d) != '-9999' && d != null){
            dt.push(d);
        }
    }
    if (dt.length > 0){
        var mn = Math.min.apply(Math,dt);
        var mx = Math.max.apply(Math,dt);
    }
    return [[data[0][0], mn, mx], [data[data.length -1][0], mn, mx]]
}


function compute_running_mean_old(data, running_mean_points, chart_type){
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
            /*
            else{
                if (chart_type == 'column'){
                    running_mean_data.push(null);
                }
                else {
                    running_mean_data.push([data[idx][0],null]);
                }
            }
            */
        }
        /*
        else{
            if (chart_type == 'column'){
                running_mean_data.push(null);
            }
            else {
                running_mean_data.push([data[idx][0],null]);
            }
        }
        */
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
        'x_cats':[],
        'data':[],
        'data_max':-9999.0,
        'data_min':9999.0
    };
    for (var date_idx=0;date_idx< data.length;date_idx++) {
        try {
            var y_val = parseFloat(data[date_idx][1]);
        }
        catch (e) {
            try {
                var y_val = parseFloat(miss_val);
            }
            catch(e) {
                var y_val = null
            }
        }
        //Convert dates if needed
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
        results.x_cats.push(data[date_idx][0]);
        if (y_val == null){
            if (chart_type == 'column') {
                results.data.push(null);
            }
            else {
                results.data.push([x_val,null]);
            }
            continue;
        }
        
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

function isPrime (n){
    if (n < 2) return false;
    /**
     * An integer is prime if it is not divisible 
     by any prime less than or equal to its square root
    **/
    var q = parseInt(Math.sqrt (n));

    for (var i = 2; i <= q; i++){
        if (n % i == 0){
            return false;
        }
    }
    return true;
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
function find_smallest_divisor(n){
    //smallest divisor of n
    var div;
    if (isPrime(n)){
         div = n;
    }
    else{
        var flag = true,
        div = 3;
        while (flag){
            if (n % div == 0){
                flag = false;
            }
            div=div+1;
        }
    }
    return div
}

function find_largest_divisor(n){
    //Largest divisor of n
    var div;
    if (isPrime(n)){
         div = n;
    }
    else{
        var flag = true,
        div = n - 1;
        while (flag){
            if (n % div == 0){
                flag = false;
            }
            div=div - 1;
        }
    }
    return div
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

function compute_data_summary(vals, summary){
    /*
    Computes summary over vals
    vals must be non-empty array
    */
    if (!vals.length){
        return null;
    }

    if (summary == 'max'){
        return Math.max.apply(Math,vals);
    }
    else if (summary == 'min'){
        return precise_round(Math.min.apply(Math,vals),2);
    }
    else if (summary == 'sum'){
        for(var i=0,sum=0;i<vals.length;sum+=vals[i++]);
        return precise_round(sum,2);
    }
    else if (summary == 'mean'){
        for(var i=0,sum=0;i<vals.length;sum+=vals[i++]);
        return precise_round(sum/vals.length,2);
    }
    else {
        return null;
    }
}

function set_data_summary_series(date, vals, summary, chart_type){
    results =[]; 
    if (vals.length > 0) {
        var value = compute_data_summary(vals, summary);
        if (chart_type == 'column'){
            results = value;
        }
        else {
            results = [date, value];
        } 
    }
    else {
        if (chart_type == 'column'){
            results = null;
        }
        else {
            results = [date, null];
        } 
    } 
    return results
}
