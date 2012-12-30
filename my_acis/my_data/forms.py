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
#find todays date
tdy = datetime.datetime.today()
yr = str(tdy.year)
mon = str(tdy.month)
day = str(tdy.day)
if len(mon) == 1:
    mon = '0%s' % mon
if len(day) == 1:
    day = '0%s' % day
today = '%s%s%s' % (yr, mon, day)

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
        ('stn_id', 'Pick a finder method')
)

GRID_SELECTION_CHOICES = (
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

DELIMITER_CHOICES = (
    ('comma', 'Comma (,)'),
    ('tab', 'Tab (\\t)'),
    ('space', 'Space ()'),
    ('colon', 'Colon (:)'),
    ('pipe', 'Pipe (|)'),
)

#Custom form fields
class MyDateField(forms.CharField):
    def to_python(self, date):
        # Return an empty string if no input was given.
        if not date:
            return ' '
        return date

    def validate(self, date):
        if date == 'por':
            pass
        else:
            if len(date)!=8:
                raise forms.ValidationError("Date should be 8 digits long (yyyymmdd). You entered: %s!" %str(date))
            try:
                int(date)
            except:
                raise forms.ValidationError("Not a valid date. You entered: %s!" %str(date))

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
            return []
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
class PointData0Form(forms.Form):
    def __init__(self, *args, **kwargs):
        stn_id = kwargs.get('initial', {}).get('stn_id', None)
        super(PointData0Form, self).__init__(*args, **kwargs)

        if stn_id is None:
            stn_id = self.data.get('stn_id')

        if stn_id is None:
            self.fields['station_selection'] = forms.ChoiceField(choices=STN_FIND_CHOICES, required=False, initial='stnid')
        else:
            self.fields['station_selection'] = forms.CharField(max_length=6, min_length=6,required=False, initial='stn_id', widget=forms.HiddenInput())
            self.fields['stn_id'] = forms.CharField(required=False, initial=stn_id)
        #self.fields['element'] = forms.ChoiceField(choices=ELEMENT_CHOICES, initial='pcpn', required=False)
        self.fields['elements'] = forms.CharField(initial ='maxt,mint,avgt', required=False)
        self.fields['data_format'] = forms.ChoiceField(choices=DATA_FORMAT_CHOICES, initial='html', required=False)

class PointDataForm1(forms.Form):
    def __init__(self, *args, **kwargs):
        station_selection = kwargs.get('initial', {}).get('station_selection', None)
        elements = kwargs.get('initial', {}).get('elements', None)
        data_format =  kwargs.get('initial', {}).get('data_format', None)
        stn_id = kwargs.get('initial', {}).get('stn_id', None)
        super(PointDataForm1, self).__init__(*args, **kwargs)

        if station_selection is None:
            station_selection = self.data.get('station_selection')
        if stn_id is None:
            stn_id = self.data.get('stn_id')
        if elements is None:
            elements = self.data.get('elements')
        if data_format is None:
            data_format = self.data.get('data_format')


        self.fields['station_selection'] = forms.CharField(required=False, initial=station_selection, widget=forms.HiddenInput())

        if station_selection == 'stn_id':
            self.fields['station_id'] = forms.CharField(initial=stn_id)
            self.fields['station_id'].widget.attrs['readonly'] = 'readonly'
        elif station_selection == 'stnid':
            self.fields['station_id'] = forms.CharField(max_length=6, min_length=6, initial='266779')
            #self.fields['station_id'].help_text='for more information see "Station Id systems explained"'
        elif station_selection == 'stnids':
            self.fields['station_ids'] = MultiStnField(required=False,initial='266779,103732')
        elif station_selection == 'county':
            self.fields['county'] = forms.CharField(required=False,max_length=5, min_length=5, initial='09001')
        elif station_selection == 'climdiv':
            self.fields['climate_division'] = forms.CharField(required=False,max_length=4, min_length=4, initial='NV01')
        elif station_selection == 'cwa':
            self.fields['county_warning_area'] = forms.CharField(required=False,max_length=3, initial='BOI')
        elif station_selection == 'basin':
            self.fields['basin'] = forms.CharField(required=False,max_length=8, min_length=8, initial='01080205')
        elif station_selection == 'state':
            self.fields['state'] = forms.ChoiceField(choices=STATE_CHOICES)
        elif station_selection == 'bbox':
            self.fields['bounding_box'] = BBoxField(required=False,initial='-90,40,-88,41')

        self.fields['elements'] = MultiElementField(initial=elements)
        #self.fields['elements'] = forms.CharField(required=False, initial=elements, widget=forms.HiddenInput())
        for element in elements:
            if element == 'cddxx':
                self.fields['base_temperature_cddxx'] = forms.IntegerField(initial=65)
            if element == 'hddxx':
                self.fields['base_temperature_hddxx'] = forms.IntegerField(initial=65)
            if element == 'gddxx':
                self.fields['base_temperature_gddxx'] = forms.IntegerField(initial=50)
        self.fields['start_date'] = MyDateField(max_length=8, min_length=8, required = False, initial='20120101', help_text="yyyymmdd")
        self.fields['end_date'] = MyDateField(max_length=8, min_length=8, required = False, initial=today, help_text="yyyymmdd")
        self.fields['data_format'] = forms.CharField(required=False, initial=data_format, widget=forms.HiddenInput())
        if data_format in ['dlm', 'html']:
            self.fields['delimiter'] = forms.ChoiceField(choices=DELIMITER_CHOICES)

class GridData0Form(forms.Form):
        grid_selection = forms.ChoiceField(choices=GRID_SELECTION_CHOICES, required=False, initial='point')
        elements =forms.CharField(initial ='maxt,mint,avgt', required=False)
        data_format = forms.ChoiceField(choices=DATA_FORMAT_CHOICES, initial='html', required=False)

class GridDataForm1(forms.Form):
    def __init__(self, *args, **kwargs):
        grid_selection = kwargs.get('initial', {}).get('grid_selection', None)
        elements = kwargs.get('initial', {}).get('elements', [])
        data_format =  kwargs.get('initial', {}).get('data_format', None)
        super(GridDataForm1, self).__init__(*args, **kwargs)

        if grid_selection is None:
            grid_selection = self.data.get('grid_selection')
        if elements is []:
            elements = self.data.get('elements')
        if data_format is None:
            data_format = self.data.get('data_format')

        self.fields['grid_selection'] = forms.CharField(required=False, initial=grid_selection, widget=forms.HiddenInput())
        self.fields['grid'] = forms.ChoiceField(choices=GRID_CHOICES)
        if grid_selection == 'point':
            self.fields['location'] = forms.CharField(initial="-77.7,41.8")
        elif grid_selection == 'state':
            self.fields['state'] = forms.ChoiceField(choices=STATE_CHOICES)
        elif grid_selection == 'bbox':
            self.fields['bounding_box'] = BBoxField(required=False,initial='-90,40,-88,41')

        self.fields['elements'] = MultiElementField(initial=elements)
        for element in elements:
            if element == 'cddxx':
                self.fields['base_temperature_cddxx'] = forms.IntegerField(initial=65)
            if element == 'hddxx':
                self.fields['base_temperature_hddxx'] = forms.IntegerField(initial=65)
            if element == 'gddxx':
                self.fields['base_temperature_gddxx'] = forms.IntegerField(initial=50)
        self.fields['start_date'] = MyDateField(max_length=8, min_length=8, required = False, initial='20120101', help_text="yyyymmdd")
        self.fields['end_date'] = MyDateField(max_length=8, min_length=8, required = False, initial=today, help_text="yyyymmdd")
        self.fields['data_format'] = forms.CharField(required=False, initial=data_format, widget=forms.HiddenInput())
        if data_format in ['dlm', 'html']:
            self.fields['delimiter'] = forms.ChoiceField(choices=DELIMITER_CHOICES)

#Data Application Forms
class MetaGraphForm(forms.Form):
    def __init__(self, *args, **kwargs):
        stn_id = kwargs.get('initial', {}).get('stn_id', None)
        super(MetaGraphForm, self).__init__(*args, **kwargs)

        if stn_id is None:
            stn_id = self.data.get('stn_id')

        if stn_id is None:
            self.fields['station_id'] = forms.CharField(required=False, initial='266779')
        else:
            self.fields['station_id'] = forms.CharField(required=False, initial=stn_id)

class MonthlyAveragesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        stn_id = kwargs.get('initial', {}).get('stn_id', None)
        super(MonthlyAveragesForm, self).__init__(*args, **kwargs)

        if stn_id is None:
            stn_id = self.data.get('stn_id')

        if stn_id is None:
            self.fields['station_id'] = forms.CharField(required=False, initial='266779')
        else:
            self.fields['station_id'] = forms.CharField(required=False, initial=stn_id)
        self.fields['elements'] = MultiElementField(initial='pcpn')
        self.fields['start_date'] = MyDateField(max_length=8, required = False, initial='20000101', help_text="yyyymmdd or 'por' for period of record")
        self.fields['end_date'] = MyDateField(max_length=8, required = False, initial='por', help_text="yyyymmdd or 'por' for period of record")

class ClimateMapForm0(forms.Form):
        grid_selection = forms.ChoiceField(choices=([('state', 'State'),('bbox', 'Bounding Box')]), required=False, initial='state')
        element = forms.ChoiceField(choices=ACIS_ELEMENT_CHOICES, required=False, initial='maxt')
        time_period = forms.ChoiceField(choices=TIME_PERIOD_CHOICES, required=False, initial='months')
        x = forms.IntegerField(required=False, initial=1)

class ClimateMapForm1(forms.Form):
    def __init__(self, *args, **kwargs):
        grid_selection = kwargs.get('initial', {}).get('grid_selection', None)
        element = kwargs.get('initial', {}).get('element', None)
        time_period =  kwargs.get('initial', {}).get('time_period', None)
        x = kwargs.get('initial', {}).get('x', None)

        super(ClimateMapForm1, self).__init__(*args, **kwargs)

        if grid_selection is None:
            grid_selection = self.data.get('grid_selection')
        if element is None:
            element = self.data.get('element')
        if time_period is None:
            time_period = self.data.get('time_period')
        if x is None:
            x = self.data.get('x')

        self.fields['grid_selection'] = forms.CharField(required=False, initial=grid_selection, widget=forms.HiddenInput())
        self.fields['grid'] = forms.ChoiceField(choices=GRID_CHOICES)
        if grid_selection == 'point':
            self.fields['location'] = forms.CharField(initial='-77.7,41.8')
        elif grid_selection == 'state':
            self.fields['state'] = forms.ChoiceField(choices=STATE_CHOICES)
        elif grid_selection == 'bbox':
            self.fields['bounding_box'] = BBoxField(required=False,initial='-90,40,-88,41')

        self.fields['element'] = forms.CharField(initial=element)
        self.fields['element'].widget.attrs['readonly'] = 'readonly'
        if element == 'cddxx':
            self.fields['base_temperature_cddxx'] = forms.IntegerField(initial=65)
        if element == 'hddxx':
            self.fields['base_temperature_hddxx'] = forms.IntegerField(initial=65)
        if element == 'gddxx':
            self.fields['base_temperature_gddxx'] = forms.IntegerField(initial=50)

        if time_period == 'custom':
            self.fields['start_date'] = MyDateField(max_length=8, min_length=8, required = False, initial='20120101', help_text="yyyymmdd")
            self.fields['end_date'] =MyDateField(max_length=8, min_length=8, required = False, initial=today, help_text="yyyymmdd")
        else:
            if x is None:
                self.fields['start_date'] = MyDateField(max_length=8, min_length=8, required = False, initial='20120101', help_text="yyyymmdd")
                self.fields['end_date'] = MyDateField(max_length=8, min_length=8, required = False, initial=today, help_text="yyyymmdd")
            else:
                start_date = WRCCUtils.get_start_date(time_period,today, x)
                self.fields['start_date'] = MyDateField(required = False, initial=start_date)
                self.fields['start_date'].widget.attrs['readonly'] = 'readonly'
            self.fields['end_date'] = MyDateField(required=False, initial=today)
            self.fields['end_date'].widget.attrs['readonly'] = 'readonly'

class GPTimeSeriesForm(forms.Form):
        def __init__(self, *args, **kwargs):
            lat = kwargs.get('initial', {}).get('lat', None)
            lon = kwargs.get('initial', {}).get('lon', None)

            super(GPTimeSeriesForm, self).__init__(*args, **kwargs)

            if lat is None:
                lat = self.data.get('lat')
            if lon is None:
                lon = self.data.get('lon')

            if lat is None:
                 self.fields['lat'] = forms.FloatField(initial='41.8', required=False)
            else:
                self.fields['lat'] = forms.FloatField(initial=lat, required=False)
            if lon is None:
                 self.fields['lon'] = forms.FloatField(initial='-77.7', required=False)
            else:
                self.fields['lon'] = forms.FloatField(initial=lon, required=False)
            self.fields['element'] = forms.ChoiceField(choices=ACIS_ELEMENT_CHOICES_SHORT, required=False, initial='maxt')
            self.fields['start_date'] = MyDateField(max_length=8, min_length=8, required = False, initial='20120101', help_text="yyyymmdd")
            self.fields['end_date'] = MyDateField(max_length=8, min_length=8, required = False, initial=today, help_text="yyyymmdd")
            self.fields['grid'] = forms.ChoiceField(choices=GRID_CHOICES)
