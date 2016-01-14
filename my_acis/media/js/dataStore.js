function convertDate(date, sep){
        var yr = String(date.getFullYear());
        var mon = String(date.getMonth());
        var day = String(date.getDay());
        if (String(mon).length == 1){
            mon = '0' + mon;
        }
        if (String(day).length == 1){
            day = '0' + day;
        }
        return yr + sep + mon + sep + day;
}
var tdy = new Date();
var tdy_string = convertDate(tdy,'-');

var grid_vd = {
    '1':[['1950-01-01',tdy_string],[]],
    '3':[['2007-01-01',tdy_string],[]],
    '21':[['1981-01-01',tdy_string],[]],
    '4':[['1970-01-01','1999-12-31'],[]],
    '5':[['1970-01-01','1999-12-31'],['2040-01-01','2069-12-31']],
    '6':[['1970-01-01','1999-12-31'],['2040-01-01','2069-12-31']],
    '8':[['1970-01-01','1999-12-31'],['2040-01-01','2069-12-31']],
    '9':[['1970-01-01','1999-12-31'],[]],
    '10':[['1970-01-01','1999-12-31'],['2040-01-01','2069-12-31']],
    '11':[['1970-01-01','1999-12-31'],[]],
    '12':[['1970-01-01','1999-12-31'],['2040-01-01','2069-12-31']],
    '13':[['1970-01-01','1999-12-31'],['2040-01-01','2069-12-31']],
    '14':[['1970-01-01','1999-12-31'],[]],
    '15':[['1970-01-01','1999-12-31'],['2040-01-01','2069-12-31']],
    '16':[['1970-01-01','1999-12-31'],['2040-01-01','2069-12-31']]
};
for (var grid_id=22;grid_id<=41;grid_id++) {
    grid_vd[String(grid_id)] = [['1950-01-01','2005-12-31'],['2006-01-01','2099-12-31']];
}
