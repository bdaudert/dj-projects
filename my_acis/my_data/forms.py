from django import forms

from django.forms.fields import ChoiceField, MultipleChoiceField
from django.contrib.localflavor.us.forms import USStateField, USStateSelect
from django.contrib.localflavor.us.us_states import STATE_CHOICES
from django.utils.safestring import mark_safe

import datetime
import re
import WRCCUtils

#Utilities
############################################
#find yestarday's data, default end_data
tdy = datetime.datetime.today() - datetime.timedelta(days=1)
#Choose default start_date 4 weeks back
b = datetime.datetime.today() - datetime.timedelta(days=14)
y = datetime.datetime.today() - datetime.timedelta(days=1)
yr = str(tdy.year)
mon = str(tdy.month)
day = str(tdy.day)
if len(mon) == 1:
    mon = '0%s' % mon
if len(day) == 1:
    day = '0%s' % day
yr_b = str(b.year)
mon_b = str(b.month)
day_b = str(b.day)
if len(mon_b) == 1:
    mon_b = '0%s' % mon_b
if len(day_b) == 1:
    day_b = '0%s' % day_b
yr_y = str(y.year)
mon_y = str(y.month)
day_y = str(y.day)
if len(mon_y) == 1:
    mon_y = '0%s' % mon_y
if len(day_y) == 1:
    day_y = '0%s' % day_y
today = '%s%s%s' % (yr, mon, day)
begin = '%s%s%s' % (yr_b, mon_b, day_b)
yesterday = '%s%s%s' % (yr_y, mon_y, day_y)

TIME_PERIOD_CHOICES = (
    ('custom', 'Custom Date Range'),
    ('days', 'Last x days'),
    ('months', 'Last x months'),
    ('years', 'Last x years'),
)

ACIS_ELEMENT_CHOICES = (
        ('pcpn', 'Precipitation (Inches)'),
        ('snow', 'Snowfall (Inches)'),
        ('snwd', 'Snowdepth (Inches)'),
        ('maxt', 'Maximum Temperature (F)'),
        ('mint', 'Minimum Temperature(F)'),
        ('avgt', 'Mean Temperature(F)'),
        ('gdd', 'Growing Degree Days (Base 50F)'),
        ('hdd', 'Heating Degree Days (Base 65F)'),
        ('cdd', 'Cooling Degree Days (Base 65F)'),
        ('gddxx', 'Growing Degree Days (Base xxF)'),
        ('hddxx', 'Heating Degree Days (Base xxF)'),
        ('cddxx', 'Cooling Degree Days (Base xxF)'),
)

ACIS_ELEMENT_CHOICES_SHORT = (
        ('pcpn', 'Precipitation (Inches)'),
        ('maxt', 'Maximum Temperature (F)'),
        ('mint', 'Minimum Temperature(F)'),
        ('avgt', 'Mean Temperature(F)'),
        ('gdd', 'Growing Degree Days (Base 50F)'),
        ('hdd', 'Heating Degree Days (Base 65F)'),
        ('cdd', 'Cooling Degree Days (Base 65F)'),
)

STN_FIND_CHOICES = (
        ('stnid', 'Individual station'),
        ('stnids', 'Comma separated list of stations '),
        ('county', 'County FIPS code'),
        ('climdiv', 'Climate Division'),
        ('cwa', 'County Warning Area (CWA)'),
        ('basin', 'Basin'),
        ('state', 'State'),
        ('bbox', 'Bounding Box'),
        ('stn_id', 'Preselected Station')
)


select_grid_by_CHOICES = (
    ('point', 'Point Location'),
    ('state', 'State'),
    ('bbox', 'Bounding Box'),
)

GRID_CHOICES = (
    ('1', 'NRCC Interpolated (US)'),
    ('2', 'NRCC Hi-Res (East of Rockies)'),
    ('3', 'NARCCAP (US)'),
    ('4', 'CRCM + NCEP (Historical only)'),
    ('5', 'CRCM + CCSM'),
    ('6', 'CRCM + CCSM3'),
    ('7', 'HRM3 + NCEP  (Historical only)'),
    ('8', 'HRM3 HadCM3'),
    ('9', 'MM5I + NCEP (Historical only)'),
    ('10', 'MM5I + CCSM'),
    ('11', 'RCM3 + NCEP (Historical only)'),
    ('12', 'RCM3 + CGCM3'),
    ('13', 'RCM3 + GFDL'),
    ('14', 'WRFG + NCEP (Historical only)'),
    ('15', 'WRFG + CCSM'),
    ('16', 'WRFG + CGCM3'),
)


ELEMENT_CHOICES = (

        ('pcpn', 'Precipitation (Inches)'),
        ('snow', 'Snowfall (Inches)'),
        ('snwd', 'Snowdepth (Inches)'),
        ('maxt', 'Maximum Temperature (F)'),
        ('mint', 'Minimum Temperature(F)'),
        ('avgt', 'Mean Temperature(F)'),
        ('hdd', 'heating Degree Days base 65F(Whole Days)'),
        ('cdd', 'Cooling Degree Days base 65F (Whole Days)'),
        ('cdd', 'Growing Degree Days  50F (Whole Days)'),
        ('hddxx', 'Heating Degree Days base user defined(Whole Days)'),
        ('cddxx', 'Cooling Degree Days base user defined(Whole Days)'),
        ('cddxx', 'Growing Degree Days base user defined (Whole Days)'),
)

DATA_FORMAT_CHOICES = (
    ('json', 'JSON'),
    ('dlm', 'Delimited, .dat'),
    ('clm', 'Columnar, .txt'),
    ('xl', 'Excel, .xls'),
    ('html', 'HTML, .html'),

)

DATA_FORMAT_CHOICES_LTD = (
    ('json', 'JSON'),
    ('dlm', 'Delimited, .dat'),
    ('clm', 'Columnar, .txt'),
    ('xl', 'Excel, .xls'),

)

DELIMITER_CHOICES = (
    ('comma', 'Comma (,)'),
    ('tab', 'Tab (\\t)'),
    ('space', 'Space ()'),
    ('colon', 'Colon (:)'),
    ('pipe', 'Pipe (|)'),
)

acis_elements = acis_elements ={'maxt': 'Maximum Daily Temperature (F)','mint': 'Minimum Daily Temperature (F)', \
'avgt': 'Average Daily Temperature (F)','obst': 'Observation Time Temperature (F)', 'pcpn':'Precipitation (In)', \
'snow':'Snowfall (In)','snwd':'Snow Depth (In)', 'cdd':'Cooling Degree Days (Days, Base 65)', \
'hdd':'Heating Degree Days (Days, Base 65)', 'gdd':'Growing Degree Days (Days, Base 50)', \
'cddXX':'Cooling Degree Days (Days, Base XX)', 'hddXX':'Heating Degree Days (Days, Base XX)', 'gddXX':'Growing Degree Days (Days, Base XX)'}
acis_element_list = ''
for el, el_long in acis_elements.iteritems():
    acis_element_list = acis_element_list + '%s : %s\n' %(el, el_long)

#Help texts
help_comma_elements = 'Comma separated list of ACIS climate elements. Available elements: \n %s' %acis_element_list
help_acis_elements = 'Available climate element in ACIS: \n %s' %acis_element_list
help_grids = 'Gridded/modeled datasets available in Acis. For more info, see "How to use this tool"!'
help_stn_selection = 'Defines the type ofsearch area. For more info, see "How to use this tool"!'
help_date = 'yyyymmdd'
help_date_por = 'yyyymmdd or "por" (period of record) if single station.'
help_lon_lat = 'Grid point coordinate pair: Longitude, Latitude'
'''
help_stn_selection = 'Individual Station:\n' + \
                     'Looks for single station. User will need to enter station ID \n' + \
                     'Comma separated list of stations:\n' + \
                     ' Looks for multiple station. User will need to enter station IDs\n' + \
                     'Use station finder tool to find IDs: http://cyclone1.dri.edu/csc/sw_ckn/station_finder or/\n' + \
                     'Read more on station IDs here: http://cyclone1.dri.edu/csc/media/html/station_id_system_docu.html\n' + \
                     'County FIPS code:\n' + \
                     ' http://cyclone1.dri.edu/csc/media/html/US_FIPS_CountyCodes.htm\n' + \
                     'Climate Division map and list:\n' + \
                     ' http://www.ncdc.noaa.gov/temp-and-precip/us-climate-divisions.php\n' + \
                     'County Warning Area list:\n' + \
                     ' http://www.aprs-is.net/WX/NWSCodes.aspx\n' + \
                     'Basin list:\n' + \
                     ' http://water.usgs.gov/nawqa/sparrow/wrr97/geograp/huc_name.txt\n' + \
                     'Bounding Box:\n' + \
                     ' A bounding box has four coordinates:\n' + \
                     ' West longitude, South latitude, East longitude, North latitude. Please enter them in this order.\n' + \
                     'Preselected Station: If you reached this pages via our station finder or via' + \
                     'one of our applications, your station ID will be entered automatically. Leave this option as is.'
'''
HELP_TEXTS = {'select_stations_by': help_stn_selection, 'grids': help_grids, 'acis_elements':help_acis_elements, \
            'comma_elements':help_comma_elements, 'date':help_date, 'date_por':help_date_por, 'grid_lon_lat':help_lon_lat }

#Custom form fields
class MyDateField(forms.CharField):
    def to_python(self, date):
        # Return an empty string if no input was given.
        if not date:
            return ' '
        formatted_date = ''.join(date.split('-'))
        return formatted_date

    def validate(self, formatted_date):
        if formatted_date == 'por':
            if self.min_length == 8:
                raise forms.ValidationError("Date should be of form yyyymmdd or yyyy-mm-dd.")
        else:
            if len(formatted_date)!=8:
                raise forms.ValidationError("Date should be of form yyyymmdd or yyyy-mm-dd.")
            try:
                int(formatted_date)
            except:
                raise forms.ValidationError("Not a valid date.")

#for background data requests, see GridDataForm3, PointDataForm3
class MyNameField(forms.CharField):
    def to_python(self, name):
        if not name:
            return ' '
        #format name to single string without spaces
        formatted_name = ''.join(name.split(' '))
        return formatted_name

    def validate(self, formatted_name):
        #don't allow special characters in name
        if not re.search(r"^(?:[\w](?<!_))+$", formatted_name):
            raise forms.ValidationError('Not a valid name. Please remove special characters!')

class MultiStnField(forms.CharField):
    def to_python(self, stn_list):
        "Normalize data to a list of strings."
        # Return an empty list if no input was given.
        if not stn_list:
            return []
        return stn_list.split(',')

    def validate(self, stn_list):
        "Check if value consists only of valid coop_station_ids."
        for stn in stn_list:
            if not str(stn).isalnum:
                raise forms.ValidationError("Not a valid station_id! Station ID are alphanumeric %s!" % str(stn))

class BBoxField(forms.CharField):
    def to_python(self, bbox_str):
        "Normalize data to a list of strings."
        # Return an empty string if no input was given.
        if not bbox_str:
            return ' '
        return str(bbox_str)
    def validate(self, bbox_str):
        "Check if bbox_str is a valid bounding box."
        bbox_list = bbox_str.split(',')
        if len(bbox_list)!= 4:
            raise forms.ValidationError("Not a valid bounding box. Missing lat or lon! %s" %str(bbox_str))
        for ll in bbox_list:
            try:
                float(ll)
            except:
                raise forms.ValidationError("Not a valid lat/lon. %s" %str(ll))

class MultiElementField(forms.CharField):
    def to_python(self, el_tuple):
        "Normalize data to a list of strings."
        # Return an empty list if no input was given.
        if not el_tuple:
            raise forms.ValidationError("Need at least one element.")
            #return []
        else:
            if isinstance(el_tuple, list):
                el_list = [str(el).strip(' ') for el in el_list]
            else:
                el_list =  el_tuple.split(',')
                el_list = [str(el).strip(' ') for el in el_list]
            return el_list

    def validate(self, el_tuple):
        "Check if value consists only of valid coop_station_ids."
        for el in el_tuple:
            el_strip = re.sub(r'(\d+)(\d+)', '', el) #strip digits from gddxx, hddxx, cddxx
            if str(el_strip) not in ['pcpn', 'snow', 'snwd', 'maxt', 'mint', 'avgt', 'obst', 'cdd', 'hdd', 'gdd']:
                raise forms.ValidationError(\
                mark_safe("elements should be a comma separated list of valid element choices:<br/>") + \
                mark_safe("pcpn, snow, snwd, <br/>") + \
                mark_safe("maxt, mint, avgt, <br/>") + \
                mark_safe("obst, cdd, hdd, gdd <br/>") + \
                mark_safe(" or cddxx, hddxx, gddxx where xx is the base temperature in Fahrenheit, e.g. 68<br/>") + \
                mark_safe("You entered: %s" %str(el)))

#Data Retrieval Forms
class PointDataForm0(forms.Form):
    def __init__(self, *args, **kwargs):
        stn_id = kwargs.get('initial', {}).get('stn_id', None)
        super(PointDataForm0, self).__init__(*args, **kwargs)

        if stn_id is None:
            stn_id = self.data.get('stn_id')

        if stn_id is None:
            self.fields['select_stations_by'] = forms.ChoiceField(choices=STN_FIND_CHOICES, required=False, initial='stnid', help_text=HELP_TEXTS['select_stations_by'])
        else:
            self.fields['select_stations_by'] = forms.ChoiceField(choices=STN_FIND_CHOICES,required=False, initial='stn_id', widget=forms.HiddenInput(), help_text=HELP_TEXTS['select_stations_by'])
            self.fields['stn_id'] = forms.CharField(required=False, initial=stn_id, help_text='Station id recognized by Acis. See "About this tool" for more information.')
        '''
        #self.fields['element'] = forms.ChoiceField(choices=ELEMENT_CHOICES, initial='pcpn', required=False)
        self.fields['elements'] = forms.CharField(initial ='maxt,mint,avgt', required=False, help_text=HELP_TEXTS['comma_elements'])
        self.fields['data_format'] = forms.ChoiceField(choices=DATA_FORMAT_CHOICES, initial='html', required=False, help_text='Defines format in which data will be returned.')
        '''
class PointDataForm1(forms.Form):
    def __init__(self, *args, **kwargs):
        select_stations_by = kwargs.get('initial', {}).get('select_stations_by', None)
        elements = kwargs.get('initial', {}).get('elements', None)
        data_format =  kwargs.get('initial', {}).get('data_format', None)
        stn_id = kwargs.get('initial', {}).get('stn_id', None)
        super(PointDataForm1, self).__init__(*args, **kwargs)

        if select_stations_by is None:
            select_stations_by = self.data.get('select_stations_by')
        if stn_id is None:
            stn_id = self.data.get('stn_id')
        if elements is None:
            elements = self.data.get('elements')
        if data_format is None:
            data_format = self.data.get('data_format')


        self.fields['select_stations_by'] = forms.CharField(required=False, initial=select_stations_by, widget=forms.HiddenInput(), help_text=HELP_TEXTS['select_stations_by'])

        if select_stations_by == 'stn_id':
            self.fields['station_id'] = forms.CharField(required=False, initial=stn_id, help_text='Station id recognized by Acis. See "How to use this tool" for more info.')
            self.fields['station_id'].widget.attrs['readonly'] = 'readonly'
        elif select_stations_by == 'stnid':
            self.fields['station_id'] = forms.CharField(required=False,initial='266779', help_text='Station id recognized by Acis. See "About this tool" for more info.')
        elif select_stations_by == 'stnids':
            #self.fields['grid'] = forms.ChoiceField(choices=GRID_CHOICES)
            self.fields['station_ids'] = MultiStnField(required=False,initial='266779,103732', help_text='Comma separated list of valid station ids.' )
        elif select_stations_by == 'county':
            self.fields['county'] = forms.CharField(required=False,max_length=5, min_length=5, initial='09001', help_text='Valid US county identifier.')
        elif select_stations_by == 'climdiv':
            self.fields['climate_division'] = forms.CharField(required=False,max_length=4, min_length=4, initial='NV01', help_text='Valid US climate division identifier.')
        elif select_stations_by == 'cwa':
            self.fields['county_warning_area'] = forms.CharField(required=False,max_length=3, initial='BOI', help_text='Valid US county warning area identifier.')
        elif select_stations_by == 'basin':
            self.fields['basin'] = forms.CharField(required=False,max_length=8, min_length=8, initial='01080205', help_text='Valid US darinage basin identifier.')
        elif select_stations_by == 'state':
            self.fields['state'] = forms.ChoiceField(choices=STATE_CHOICES, help_text='Valid US state abreviation.')
        elif select_stations_by == 'bbox':
            self.fields['bounding_box'] = BBoxField(required=False,initial='-90,40,-88,41', help_text='Bounding box latitudes and longitudes: West,South,East,North.')

        self.fields['elements'] = MultiElementField(initial='maxt,mint,pcpn', help_text=HELP_TEXTS['comma_elements'])
        '''
        for element in elements:
            if element == 'cddxx':
                self.fields['base_temperature_cddxx'] = forms.IntegerField(initial=65, help_text='Base temperature used to calculate cooling degree days.')
            if element == 'hddxx':
                self.fields['base_temperature_hddxx'] = forms.IntegerField(initial=65, help_text='Base temperature used to calculate heating degree days.')
            if element == 'gddxx':
                self.fields['base_temperature_gddxx'] = forms.IntegerField(initial=50, help_text='Base temperature used to calculate growing degree days.')
        '''
        self.fields['start_date'] = MyDateField(max_length=10, min_length=3, initial=begin, help_text=HELP_TEXTS['date_por'])
        self.fields['end_date'] = MyDateField(max_length=10, min_length=3, initial=today, help_text=HELP_TEXTS['date_por'])
        self.fields['data_format'] = forms.ChoiceField(choices=DATA_FORMAT_CHOICES, initial='html', help_text='Defines format in which data will be returned.')
        self.fields['delimiter'] = forms.ChoiceField(choices=DELIMITER_CHOICES, help_text='Delimiter used to seperate data values.')

class PointDataForm3(forms.Form):
   def __init__(self, *args, **kwargs):
        select_stations_by = kwargs.get('initial', {}).get('select_stations_by', None)
        data_format =  kwargs.get('initial', {}).get('data_format', None)
        super(PointDataForm3, self).__init__(*args, **kwargs)

        if select_stations_by is None:
            select_stations_by = self.data.get('select_stations_by')
        if data_format is None:
            data_format = self.data.get('data_format')

        self.fields['user_name'] = MyNameField(initial='Your Name', help_text = 'Enter a user name without special characters. Example: first name initial + last name.')
        self.fields['email'] = forms.EmailField(initial='Your e-mail', help_text='Enter a valid e-mail address at wich we can reach you.')

        if select_stations_by == 'stn_id':
            self.fields['station_id'] = forms.CharField(initial=kwargs.get('initial', {}).get('stn_id', None), help_text='Station id recognized by Acis. See "How to use this tool" for more info.')
        elif select_stations_by == 'stnid':
            self.fields['station_id'] = forms.CharField(initial=kwargs.get('initial', {}).get('station_id', None), help_text='Station id recognized by Acis. See "About this tool" for more info.')
        elif select_stations_by == 'stnids':
            self.fields['station_ids'] = MultiStnField(initial=kwargs.get('initial', {}).get('station_ids', None),help_text='Comma separated list of valid station ids.' )
        elif select_stations_by == 'county':
            self.fields['county'] = forms.CharField(max_length=5, min_length=5, initial=kwargs.get('initial', {}).get('county', None),help_text='Valid US county identifier.')
        elif select_stations_by == 'climdiv':
            self.fields['climate_division'] = forms.CharField(max_length=4, min_length=4, initial=kwargs.get('initial', {}).get('climate_division', None),help_text='Valid US climate division identifier.')
        elif select_stations_by == 'cwa':
            self.fields['county_warning_area'] = forms.CharField(max_length=3, initial=kwargs.get('initial', {}).get('county_warning_area', None),help_text='Valid US county warning area identifier.')
        elif select_stations_by == 'basin':
            self.fields['basin'] = forms.CharField(max_length=8, min_length=8, initial=kwargs.get('initial', {}).get('basin', None),help_text='Valid US darinage basin identifier.')
        elif select_stations_by == 'state':
            self.fields['state'] = forms.ChoiceField(choices=STATE_CHOICES, initial=kwargs.get('initial', {}).get('state', None),help_text='Valid US state abreviation.')
        elif select_stations_by == 'bbox':
            self.fields['bounding_box'] = BBoxField(initial=kwargs.get('initial', {}).get('bounding_box', None),help_text='Bounding box latitudes and longitudes: West,South,East,North.')
        self.fields['elements'] = MultiElementField(initial=kwargs.get('initial', {}).get('elements', None), help_text=HELP_TEXTS['comma_elements'])
        self.fields['start_date'] = MyDateField(max_length=10, min_length=3, initial=kwargs.get('initial', {}).get('start_date', None),help_text=HELP_TEXTS['date_por'])
        self.fields['end_date'] = MyDateField(max_length=10, min_length=3, initial=kwargs.get('initial', {}).get('end_date', None), help_text=HELP_TEXTS['date_por'])
        #self.fields['data_format'] = forms.CharField(required=False, initial=kwargs.get('initial', {}).get('data_format', None), help_text='Defines format in which data will be returned.')
        self.fields['data_format'] = forms.ChoiceField(choices=DATA_FORMAT_CHOICES_LTD, initial='txt', help_text='Defines format in which data will be returned.')
        if data_format in ['dlm', 'html']:
            self.fields['delimiter'] = forms.ChoiceField(required=False,choices=DELIMITER_CHOICES, initial=kwargs.get('initial', {}).get('delimiter', None),help_text='Delimiter used to seperate data values.')
        self.fields['select_stations_by'] = forms.CharField(widget=forms.HiddenInput(), initial=select_stations_by, help_text=HELP_TEXTS['select_stations_by'])

class GridDataForm0(forms.Form):
        select_grid_by = forms.ChoiceField(choices=select_grid_by_CHOICES, required=False, initial='point', help_text='Area defining gridpoints of interest.')
        #elements =forms.CharField(initial ='maxt,mint,avgt', required=True, help_text=HELP_TEXTS['comma_elements'])
        #data_format = forms.ChoiceField(choices=DATA_FORMAT_CHOICES, initial='html', required=False, help_text='Delimiter used to seperate data values.')

class GridDataForm1(forms.Form):
    def __init__(self, *args, **kwargs):
        select_grid_by = kwargs.get('initial', {}).get('select_grid_by', None)
        super(GridDataForm1, self).__init__(*args, **kwargs)

        if select_grid_by is None:select_grid_by = self.data.get('select_grid_by')
        if select_grid_by == 'point':
            self.fields['location'] = forms.CharField(initial="-77.7,41.8", help_text=HELP_TEXTS['grid_lon_lat'])
        elif select_grid_by == 'state':
            self.fields['state'] = forms.ChoiceField(choices=STATE_CHOICES, help_text='US state abbreviation.')
        elif select_grid_by == 'bbox':
            self.fields['bounding_box'] = BBoxField(initial='-90,40,-88,41', help_text='Bounding boxcoordinates: West, South, East, North.')
        else:
            self.fields['bounding_box'] = BBoxField(initial='-90,40,-88,41', help_text='Bounding boxcoordinates: West, South, East, North.')

        self.fields['select_grid_by'] = forms.CharField(initial=select_grid_by, widget=forms.HiddenInput(), help_text='Area defining gridpoints of interest.')
        #self.fields['elements'] = MultiElementField(initial=elements,widget=forms.HiddenInput(), help_text=HELP_TEXTS['comma_elements'])
        self.fields['elements'] = MultiElementField(initial='maxt,mint,pcpn', help_text=HELP_TEXTS['comma_elements'])
        '''
        for element in elements:
            if element == 'cddxx':
                self.fields['base_temperature_cddxx'] = forms.IntegerField(initial=65, help_text='Base temperature used to calculate cooling degree days.')
            if element == 'hddxx':
                self.fields['base_temperature_hddxx'] = forms.IntegerField(initial=65, help_text='Base temperature used to calculate heating degree days.')
            if element == 'gddxx':
                self.fields['base_temperature_gddxx'] = forms.IntegerField(initial=50, help_text='Base temperature used to calculate growing degree days.')
        '''
        if select_grid_by == 'point':
            self.fields['start_date'] = MyDateField(max_length=10, min_length=8,initial=begin, help_text=HELP_TEXTS['date'])
        else:
            self.fields['start_date'] = MyDateField(max_length=10, min_length=8,initial=yesterday, help_text=HELP_TEXTS['date'])
        self.fields['end_date'] = MyDateField(max_length=10, min_length=8, initial=today, help_text=HELP_TEXTS['date'])
        self.fields['grid'] = forms.ChoiceField(choices=GRID_CHOICES, help_text=HELP_TEXTS['grids'])
        self.fields['data_format'] = forms.ChoiceField(choices=DATA_FORMAT_CHOICES, initial='html', help_text='Defines format in which data will be returned.')
        self.fields['delimiter'] = forms.ChoiceField(choices=DELIMITER_CHOICES, help_text='Delimiter used to seperate data values.')

class GridDataForm3(forms.Form):
    def __init__(self, *args, **kwargs):
        select_grid_by = kwargs.get('initial', {}).get('select_grid_by', None)
        data_format =  kwargs.get('initial', {}).get('data_format', None)
        super(GridDataForm3, self).__init__(*args, **kwargs)

        if select_grid_by is None:
            select_grid_by = self.data.get('select_grid_by')
        if data_format is None:
            data_format = self.data.get('data_format')

        self.fields['user_name'] = MyNameField(initial='Your Name', help_text = 'Enter a user name without special characters.Example: first name initial + last name.')
        self.fields['email'] = forms.EmailField(initial='Your e-mail', help_text='Enter a valid e-mail address at wich we can reach you.')

        if select_grid_by == 'point':
            self.fields['location'] = forms.CharField(initial=kwargs.get('initial', {}).get('location', None), help_text='Gridpoint coordinates: latitude, longitude.')
        elif select_grid_by == 'state':
            self.fields['state'] = forms.ChoiceField(initial=kwargs.get('initial', {}).get('state', None), choices=STATE_CHOICES, help_text='US state abbreviation.')
        elif select_grid_by == 'bbox':
            self.fields['bounding_box'] = BBoxField(initial=kwargs.get('initial', {}).get('bounding_box', None), help_text='Bounding boxcoordinates: West, South, East, North.')

        self.fields['elements'] = MultiElementField(initial=kwargs.get('initial', {}).get('elements', None), help_text='Comma separated list of Acis element abbreviations. See "How to use this tool" for complete list.')
        self.fields['start_date'] = MyDateField(max_length=10, min_length=8, initial=kwargs.get('initial', {}).get('start_date', None), help_text=HELP_TEXTS['date'])
        self.fields['end_date'] = MyDateField(max_length=10, min_length=8, initial=kwargs.get('initial', {}).get('end_date', None), help_text=HELP_TEXTS['date'])
        self.fields['grid'] = forms.ChoiceField(choices=GRID_CHOICES, initial=kwargs.get('initial', {}).get('grid', None), help_text=HELP_TEXTS['grids'])
        #self.fields['data_format'] = forms.CharField(required=False, initial=data_format, widget=forms.HiddenInput(), help_text='Defines format in which data will be returned.')
        self.fields['data_format'] = forms.ChoiceField(choices=DATA_FORMAT_CHOICES_LTD, initial='txt', help_text='Defines format in which data will be returned.')
        if data_format in ['dlm', 'html']:
            self.fields['delimiter'] = forms.ChoiceField(required=False,choices=DELIMITER_CHOICES, initial=kwargs.get('initial', {}).get('delimiter', None), help_text='Delimiter used to seperate data values.')
        self.fields['select_grid_by'] = forms.CharField(initial=select_grid_by, widget=forms.HiddenInput(), help_text='Area defining gridpoints of interest.')

#Data Application Forms
class MetaGraphForm(forms.Form):
    def __init__(self, *args, **kwargs):
        stn_id = kwargs.get('initial', {}).get('stn_id', None)
        super(MetaGraphForm, self).__init__(*args, **kwargs)

        if stn_id is None:
            stn_id = self.data.get('stn_id')

        if stn_id is None:
            self.fields['station_id'] = forms.CharField(required=True, initial='266779', help_text='Coop station id. See "How to use this tool" for more info.')
        else:
            self.fields['station_id'] = forms.CharField(required=True, initial=stn_id, help_text='Coop station id. See "How to use this tool" for more info.')

class MonthlyAveragesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        stn_id = kwargs.get('initial', {}).get('stn_id', None)
        super(MonthlyAveragesForm, self).__init__(*args, **kwargs)

        if stn_id is None:
            stn_id = self.data.get('stn_id')

        if stn_id is None:
            self.fields['station_id'] = forms.CharField(required=False, initial='266779', help_text='Station id recognized by Acis. See "How to use this tool" for more information.')
        else:
            self.fields['station_id'] = forms.CharField(required=False, initial=stn_id, help_text='Station id recognized by Acis. See "How to use this tool" for more information.')
        self.fields['elements'] = MultiElementField(initial='pcpn, snow', help_text=HELP_TEXTS['comma_elements'])
        self.fields['start_date'] = MyDateField(max_length=10, required = False, initial='20000101', help_text=HELP_TEXTS['date_por'])
        self.fields['end_date'] = MyDateField(max_length=10, required = False, initial='por', help_text=HELP_TEXTS['date_por'])

class ClimateMapForm0(forms.Form):
        select_grid_by = forms.ChoiceField(choices=([('state', 'State'),('bbox', 'Bounding Box')]), required=False, initial='state', help_text='Area defining gridpoints of interest.')
        element = forms.ChoiceField(choices=ACIS_ELEMENT_CHOICES, required=False, initial='maxt', help_text=HELP_TEXTS['acis_elements'])
        time_period = forms.ChoiceField(choices=TIME_PERIOD_CHOICES, required=False, initial='months', help_text='Time period over which to compute map gridpoint values.')
        x = forms.IntegerField(required=False, initial=1, help_text='Integer defining the number of days/months or years.')

class ClimateMapForm1(forms.Form):
    def __init__(self, *args, **kwargs):
        select_grid_by = kwargs.get('initial', {}).get('select_grid_by', None)
        element = kwargs.get('initial', {}).get('element', None)
        time_period =  kwargs.get('initial', {}).get('time_period', None)
        x = kwargs.get('initial', {}).get('x', None)
        start_date = kwargs.get('initial', {}).get('start_date', None)
        end_date = kwargs.get('initial', {}).get('end_date', None)
        grid = kwargs.get('initial', {}).get('end_date', None)
        state = kwargs.get('initial', {}).get('state', None)
        bounding_box = kwargs.get('initial', {}).get('bounding_box', None)
        super(ClimateMapForm1, self).__init__(*args, **kwargs)

        if select_grid_by is None:select_grid_by = self.data.get('select_grid_by')
        if element is None:element = self.data.get('element')
        if time_period is None:time_period = self.data.get('time_period')
        if x is None:x = self.data.get('x')
        if start_date is None:start_date = self.data.get('start_date')
        if end_date is None:end_date = self.data.get('end_date')
        if grid is None:grid=self.data.get('grid')
        if state is None:state=self.data.get('grid')
        if bounding_box is None:bounding_box=self.data.get('bounding_box')

        self.fields['select_grid_by'] = forms.CharField(required=False, initial=select_grid_by, widget=forms.HiddenInput(), help_text='Area defining gridpoints of interest.')
        if select_grid_by == 'state':
            self.fields['state'] = forms.ChoiceField(choices=STATE_CHOICES, help_text='US state.')
        elif select_grid_by == 'bbox':
            self.fields['bounding_box'] = BBoxField(required=False,initial='-90,40,-88,41', help_text='Bounding box latitudes and longitudes: West,South,East,North.')
        elif state is not None:
            self.fields['state'] = forms.ChoiceField(required=False, choices=STATE_CHOICES, initial=state, help_text='US state.')
        elif bounding_box is not None:
            self.fields['bounding_box'] = BBoxField(required=False,initial=bounding_box, help_text='Bounding box latitudes and longitudes: West,South,East,North.')
        self.fields['element'] = forms.CharField(initial=element, help_text='Valid element recognized by Acis.')
        if element == 'cddxx':
            self.fields['base_temperature_cddxx'] = forms.IntegerField(initial=65, help_text='Base temperature used to calculate cooling degree days.')
        if element == 'hddxx':
            self.fields['base_temperature_hddxx'] = forms.IntegerField(initial=65, help_text='Base temperature used to calculate heating degree days.')
        if element == 'gddxx':
            self.fields['base_temperature_gddxx'] = forms.IntegerField(initial=50, help_text='Base temperature used to calculate growing degree days.')

        if time_period == 'custom':
            self.fields['start_date'] = MyDateField(max_length=10, min_length=8, required = False, initial=begin, help_text=HELP_TEXTS['date'])
            self.fields['end_date'] =MyDateField(max_length=10, min_length=8, required = False, initial=today, help_text=HELP_TEXTS['date'])
        elif start_date is not None and end_date is not None:
            self.fields['start_date'] = MyDateField(max_length=10, min_length=8, required = False, initial=start_date, help_text=HELP_TEXTS['date'])
            self.fields['end_date'] =MyDateField(max_length=10, min_length=8, required = False, initial=end_date, help_text=HELP_TEXTS['date'])
        else:
            if x is None:
                self.fields['start_date'] = MyDateField(max_length=10, min_length=8, required = False, initial='20130101', help_text=HELP_TEXTS['date'])
            else:
                start_date = WRCCUtils.get_start_date(time_period,today, x)
                self.fields['start_date'] = MyDateField(required = False, initial=start_date, help_text=HELP_TEXTS['date'])
                self.fields['start_date'].widget.attrs['readonly'] = 'readonly'
            self.fields['end_date'] = MyDateField(required=False, initial=today, help_text=HELP_TEXTS['date'])
            self.fields['end_date'].widget.attrs['readonly'] = 'readonly'
        if grid is None:
            self.fields['grid'] = forms.ChoiceField(choices=GRID_CHOICES, help_text=HELP_TEXTS['grids'])
        else:
            self.fields['grid'] = forms.ChoiceField(choices=GRID_CHOICES, initial=grid, help_text=HELP_TEXTS['grids'])
class GPTimeSeriesForm(forms.Form):
        def __init__(self, *args, **kwargs):
            lat = kwargs.get('initial', {}).get('lat', None)
            lon = kwargs.get('initial', {}).get('lon', None)
            start_date = kwargs.get('initial', {}).get('start_date', None)
            end_date = kwargs.get('initial', {}).get('end_date', None)
            element = kwargs.get('initial', {}).get('element', None)
            grid = kwargs.get('initial', {}).get('end_date', None)
            super(GPTimeSeriesForm, self).__init__(*args, **kwargs)

            if lat is None:lat = self.data.get('lat')
            if lon is None:lon = self.data.get('lon')
            if start_date is None:start_date = self.data.get('start_date')
            if end_date is None:end_date = self.data.get('end_date')
            if element is None:element = self.data.get('element')
            if grid is None:grid=self.data.get('grid')

            if lat is None:
                 self.fields['lat'] = forms.FloatField(initial='41.8', required=True, help_text='Valid latitude.')
            else:
                self.fields['lat'] = forms.FloatField(initial=lat, required=True, help_text='Valid latitude.')
            if lon is None:
                 self.fields['lon'] = forms.FloatField(initial='-77.7', required=True, help_text='Valid longitude.')
            else:
                self.fields['lon'] = forms.FloatField(initial=lon, required=True, help_text='Valid longitude.')
            if element is None:
                self.fields['element'] = forms.ChoiceField(choices=ACIS_ELEMENT_CHOICES_SHORT, required=False, initial='maxt', help_text=HELP_TEXTS['acis_elements'])
            else:
                self.fields['element'] = forms.ChoiceField(choices=ACIS_ELEMENT_CHOICES_SHORT, required=False, initial=element, help_text=HELP_TEXTS['acis_elements'])
            if start_date is None:
                self.fields['start_date'] = MyDateField(max_length=10, min_length=8, required = False, initial='20130101', help_text=HELP_TEXTS['date'])
            else:
                self.fields['start_date'] = MyDateField(max_length=10, min_length=8, required = False, initial=start_date, help_text=HELP_TEXTS['date'])
            if end_date is None:
                self.fields['end_date'] = MyDateField(max_length=10, min_length=8, required = False, initial=today, help_text=HELP_TEXTS['date'])
            else:
                self.fields['end_date'] = MyDateField(max_length=10, min_length=8, required = False, initial=end_date, help_text=HELP_TEXTS['date'])
            if grid is None:
                self.fields['grid'] = forms.ChoiceField(choices=GRID_CHOICES, help_text=HELP_TEXTS['grids'])
            else:
                self.fields['grid'] = forms.ChoiceField(choices=GRID_CHOICES, initial=grid, help_text=HELP_TEXTS['grids'])
class StationLocatorForm0(forms.Form):
    select_stations_by = forms.ChoiceField(choices=STN_FIND_CHOICES, required=False, initial='state', help_text=HELP_TEXTS['select_stations_by'])
    element_selection = forms.ChoiceField(choices=([('T', 'Cherry pick elements'),('F', 'All Acis elements')]), required=False, initial='F', help_text='Only look for stations that have data for certain elements.')
class StationLocatorForm1(forms.Form):
    def __init__(self, *args, **kwargs):
        select_stations_by = kwargs.get('initial', {}).get('select_stations_by', None)
        element_selection = kwargs.get('initial', {}).get('element_selection', None)
        stn_id = kwargs.get('initial', {}).get('stn_id', None)
        super(StationLocatorForm1, self).__init__(*args, **kwargs)

        if select_stations_by is None:select_stations_by = self.data.get('select_stations_by')
        if element_selection is None:element_selection = self.data.get('element_selection')
        if stn_id is None:stn_id = self.data.get('stn_id')


        self.fields['select_stations_by'] = forms.CharField(required=False, initial=select_stations_by, widget=forms.HiddenInput(), help_text=HELP_TEXTS['select_stations_by'])
        self.fields['element_selection'] = forms.CharField(required=False, initial=element_selection, widget=forms.HiddenInput(), help_text='Only look for stations that have data for certain elements.')

        if select_stations_by == 'stn_id':
            self.fields['station_id'] = forms.CharField(initial=stn_id, help_text='Station id recognized by Acis. See "How to use this tool" for more info.')
            self.fields['station_id'].widget.attrs['readonly'] = 'readonly'
        elif select_stations_by == 'stnid':
            self.fields['station_id'] = forms.CharField(initial='266779', help_text='Station id recognized by Acis. See "About this tool" for more info.')
        elif select_stations_by == 'stnids':
            self.fields['station_ids'] = MultiStnField(required=False,initial='266779,103732', help_text='Comma separated list of valid station ids.' )
        elif select_stations_by == 'county':
            self.fields['county'] = forms.CharField(required=False,max_length=5, min_length=5, initial='09001', help_text='Valid US county identifier.')
        elif select_stations_by == 'climdiv':
            self.fields['climate_division'] = forms.CharField(required=False,max_length=4, min_length=4, initial='NV01', help_text='Valid US climate division identifier.')
        elif select_stations_by == 'cwa':
            self.fields['county_warning_area'] = forms.CharField(required=False,max_length=3, initial='BOI', help_text='Valid US county warning area identifier.')
        elif select_stations_by == 'basin':
            self.fields['basin'] = forms.CharField(required=False,max_length=8, min_length=8, initial='01080205', help_text='Valid US darinage basin identifier.')
        elif select_stations_by == 'state':
            self.fields['state'] = forms.ChoiceField(choices=STATE_CHOICES, help_text='US state.')
        elif select_stations_by == 'bbox':
            self.fields['bounding_box'] = BBoxField(required=False,initial='-90,40,-88,41', help_text='Bounding box latitudes and longitudes: West,South,East,North.')
        if element_selection == 'T':
            self.fields['elements'] = MultiElementField(initial='mint,maxt,avgt', help_text=HELP_TEXTS['comma_elements'])

            self.fields['start_date'] = MyDateField(max_length=10, required = False, initial='20130101',min_length=8, help_text=HELP_TEXTS['date'])
            self.fields['end_date'] = MyDateField(max_length=10, required = False, initial=today,min_length=8, help_text= 'yyyymmdd.')

