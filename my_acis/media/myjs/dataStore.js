function convertDate(date, sep){
    var yr = String(date.getFullYear());
    var mon = String(date.getMonth()+1);
    var day = String(date.getDate());
    if (String(mon).length == 1){
        mon = '0' + mon;
    }
    if (String(day).length == 1){
        day = '0' + day;
    }
    return yr + sep + mon + sep + day;
}

var all_vd_elements = ['maxt','mint','pcpn','snow','snwd','gdd','hdd','cdd','evap','pet','dtr'];
var popup_no_destroy = 'formDownload,Docu_SpottedOwlKristen,'+
    'Docu_SpottedOwlData35.2,Docu_SpottedOwlData34,Docu_SpottedOwlData30,'+
    'Docu_page_station_finder,Docu_page_projections,' +
    'Docu_spp,Docu_mpp,Docu_sf,Docu_station_finder,' +
    'Docu_nwks,Docu_nwk_links'
    'Docu_single_point_prods,Docu_single_point_prods_station,Docu_single_point_prods_grid,' +
    'Docu_multi_point_prods,Docu_multi_point_prods_station,Docu_multi_point_prods_grid';
    'Docu_page_single_point_prods,Docu_page_single_point_prods_station,Docu_page_single_point_prods_grid,' +
    'Docu_page_multi_point_prods,Docu_page_multi_point_prods_station,Docu_page_multi_point_prods_grid';
var WRCC_URL = 'https://wrcc.dri.edu';
var SINGLE_PRODS_URL = '/csc/scenic/analysis/single/'; 
var tdy = new Date();
var tdy_string = convertDate(tdy,'-');
var grid_vd = {
    '1':[['1950-01-01',tdy_string],[]],
    '3':[['2007-01-01',tdy_string],[]],
    '21':[['1981-01-01',tdy_string],[]],
    '4':[['1970-01-01','1999-12-31'],[]],
    '5':[['1970-01-01','1999-12-31'],['2040-01-01','2069-12-31']],
    '6':[['1970-01-01','1999-12-31'],['2040-01-01','2069-12-31']],
    '7':[['1970-01-01','1999-12-31'],[]],
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
    //grid_vd[String(grid_id)] = [['1950-01-01','2005-12-31'],['2006-01-01','2099-12-31']];
    grid_vd[String(grid_id)] = [['1950-01-01','2099-12-31'],[]];
}
var station_finder_metadata ={
    'name':'Name',
    'state':'State',
    'll': 'Longitude, Latitude',
    'elev':'Elevation',
    'ids':'IDs',
    'sids':'IDs',
    'networks':'Networks',
    'valid_daterange':'Valid Daterange'
}
var area_defaults = {
    'station_id':['Station ID','RENO TAHOE INTL AP, 266779'],
    'station_ids':['Station IDs','266779,050848'],
    'location':['Gridpoint','-119,39'],
    'locations':['Gridpoints','-119,39,-119.1,39.1'],
    'county':['County','Churchill County, 32001'],
    'climate_division':['Climate Division','Northwestern, NV01'],
    'county_warning_area':['Cnty Warn. Area','Las Vegas, NV, VEF'],
    'basin':['Basin','Hot Creek-Railroad Valleys, 16060012'],
    'state':['State','nv'],
    'bounding_box':['Bounding Box','-120.3,38.89,-118.89,40.21'],
    'shape':['Custom Shape','-120.3,38.89,-120.3,40.12,-118.89,40.21,-118.89,38.89'],
    'shape_file':['Custom Shape',''],
}
var state_choices = ['ak', 'al', 'ar', 'as', 'az', 'ca', 'co', 'ct', 'dc', 'de', 'fl', 'fm', 'ga', 'gu', 'hi', 'ia', 'id', 'il', 'in', 'ks', 'ky', 'la', 'ma', 'md', 'me', 'mh', 'mi', 'mn', 'mo', 'mp', 'ms', 'mt', 'nc', 'nd', 'ne', 'nh', 'nj', 'nm', 'nv', 'ny', 'oh', 'ok', 'or', 'pa', 'pr', 'pw', 'ri', 'sc', 'sd', 'tn', 'tx', 'ut', 'va', 'vt', 'wa', 'wi', 'wv', 'wy', 'as']
var state_names = {
 'ak':'Alabama', 
 'al':'Alaska', 
 'as':'American Samoa', 
 'az':'Arizona',
 'ar':'Arkansas',
 'ca':'California',
 'co':'Colorado', 
 'ct':'Connecticut', 
 'de':'Delaware',
 'dc':'District of Columbia', 
 'fl':'Florida', 
 'fm':'Federated States of Micronesia',
 'ga':'Georgia',
 'gu':'Guam',
 'hi':'Hawaii', 
 'id':'Idaho',
 'il':'Illinois',
 'ia':'Indiana',
 'io':'Iowa',
 'ks':'Kansas',
 'ky':'Kentucky', 
 'la':'Louisiana', 
 'ma':'Massachusetts', 
 'md':'Maryland', 
 'me':'Maine', 
 'mh':'Marshall Islands',
 'mi':'Michigan', 
 'mn':'Minnesota',
 'ms':'Mississippi',
 'mo':'Missouri', 
 'mp':'Northern Mariana Islands',
 'mt':'Montana',
 'ne':'Nebraska',
 'nv':'Nevada',
 'nh':'New Hampshire',
 'nj':'New Jersey',
 'nm':'New Mexico',
 'ny':'New York',
 'nc':'North Carolina', 
 'nd':'North Dakota', 
 'oh':'Ohio', 
 'ok':'Oklahoma', 
 'or':'Oregon', 
 'pa':'Pennsylvania', 
 'pr':'Puerto Rico',
 'pw':'Palau',
 'ri':'Rhode Island', 
 'sc':'South Carolina', 
 'sd':'South Dakota', 
 'tn':'Tennessee', 
 'tx':'Texas', 
 'ut':'Utah', 
 'va':'Virgina', 
 'vt':'Vermont', 
 'wa':'Washington',
 'wv':'West Virginia', 
 'wi':'Wisconsin', 
 'wy':'Wyoming'
}
