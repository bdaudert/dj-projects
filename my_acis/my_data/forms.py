#!/usr/bin/python
from django import forms

from django.forms.fields import ChoiceField, MultipleChoiceField
from django.contrib.localflavor.us.forms import USStateField, USStateSelect
from django.contrib.localflavor.us.us_states import STATE_CHOICES
from django.utils.safestring import mark_safe
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple

import datetime
import re
import WRCCUtils, WRCCData
###########################################
#Utilities
############################################
#find yestarday's data, default end_data
tdy = datetime.datetime.today()
#Choose default start_date 4 weeks back
b = datetime.datetime.today() - datetime.timedelta(days=15)
p = datetime.datetime.today() - datetime.timedelta(days=366)
y = datetime.datetime.today() - datetime.timedelta(days=1)
yr = str(tdy.year)
mon = str(tdy.month)
day = str(tdy.day)
if len(mon) == 1:
    mon = '0%s' % mon
if len(day) == 1:
    day = '0%s' % day
yr_b = str(b.year);mon_b = str(b.month);day_b = str(b.day)
yr_p = str(p.year);mon_p = str(p.month);day_p = str(p.day)
if len(mon_b) == 1:
    mon_b = '0%s' % mon_b
if len(day_b) == 1:
    day_b = '0%s' % day_b
if len(mon_p) == 1:
    mon_p = '0%s' % mon_p
if len(day_p) == 1:
    day_p = '0%s' % day_p
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
begin_prism = '%s%s%s' % (yr_p, mon_p, day_p)


readonly_style = 'background-color:#CCCCCC;'

######################################
#Choice Fields
#######################################
#Climate Risk Maps
CLIM_RISK_ELEMENT_CHOICES = (
    ('maxt', 'Maximum Temperature'),
    ('mint', 'Minimum Temperature'),
    ('avgt', 'Average Temperature'),
    ('pcpn', 'Precipitation')
)
#Sodsumm
SDMM_ELEMENT_CHOICES = (
    ('all', 'All of those below'),
    ('temp', 'Temperature'),
    ('prsn', 'Precip/Snowfall'),
    ('both', 'Temp/Precip'),
    ('hc', 'Degree Days'),
    ('g', 'Growing Degree Days'),
)


#Monthly Averages
TIME_PERIOD_CHOICES = (
    ('custom', 'Custom Date Range'),
    ('days', 'Last x days'),
    ('months', 'Last x months'),
    ('years', 'Last x years'),
)

#GridData
GRID_SUMMARY_CHOICES = (
    ('max', 'Temporal Maximum'),
    ('min', 'Temporal Minimium'),
    ('sum', 'Temporal Sum'),
    ('mean', 'Temporal Mean'),
    ('none', 'None, just get raw data')
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

#StnData
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
        ('pcpn', 'Precipitation(In)'),
        ('maxt', 'Maximum Temperature(F)'),
        ('mint', 'Minimum Temperature(F)'),
        ('avgt', 'Mean Temperature(F)'),
        ('gdd', 'Growing Degree Days(Base 50F)'),
        ('hdd', 'Heating Degree Days(Base 65F)'),
        ('cdd', 'Cooling Degree Days(Base 65F)'),
)

GRID_FIND_CHOICES = (
        ('county', 'County FIPS code'),
        ('climdiv', 'Climate Division'),
        ('cwa', 'County Warning Area (CWA)'),
        ('basin', 'Basin'),
        ('state', 'State'),
        ('shape', 'Custom Shape'),
)

#StnFinder
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

STN_FIND_CHOICES_SHORT = (
        ('sw_states', 'Southwest US'),
        ('county', 'County FIPS code'),
        ('climdiv', 'Climate Division'),
        ('cwa', 'County Warning Area (CWA)'),
        ('basin', 'Basin'),
        ('state', 'State'),
        ('states', 'Multiple States'),
        ('bbox', 'Bounding Box')
)

STN_FINDER_LOGIC =(
    ('any_any', 'Any Elements, Any Dates'),
    ('all_all', 'All Elements, All Dates'),
    ('all_any', 'All Elements, Any Date'),
    ('any_all', 'Any Element, All Dates'),
)

#Elements
ELEMENT_CHOICES = (

        ('pcpn', 'Precipitation (Inches)'),
        ('snow', 'Snowfall (Inches)'),
        ('snwd', 'Snowdepth (Inches)'),
        ('maxt', 'Maximum Temperature (F)'),
        ('mint', 'Minimum Temperature(F)'),
        ('avgt', 'Mean Temperature(F)'),
        ('hdd', 'heating Degree Days base 65F(F)'),
        ('cdd', 'Cooling Degree Days base 65F (F)'),
        ('cdd', 'Growing Degree Days  50F (F)'),
        ('hddxx', 'Heating Degree Days base user defined(F)'),
        ('cddxx', 'Cooling Degree Days base user defined(F)'),
        ('cddxx', 'Growing Degree Days base user defined (F)'),
)

#Data Formats
DATA_FORMAT_CHOICES = (
    #('json', 'JSON'),
    ('clm', 'Columnar, .txt'),
    ('dlm', 'Delimited, .dat'),
    ('xl', 'Excel, .xls'),
    ('html', 'HTML, .html'),

)

DATA_FORMAT_CHOICES_LTD = (
    #('json', 'JSON'),
    ('dlm', 'Delimited, .dat'),
    ('clm', 'Columnar, .txt'),
    ('xl', 'Excel, .xls'),

)

#Delimiters
DELIMITER_CHOICES = (
    ('comma', 'Comma (,)'),
    ('tab', 'Tab (\t)'),
    ('space', 'Space ()'),
    ('colon', 'Colon (:)'),
    ('pipe', 'Pipe (|)'),
)

######################################################################
#Help texts
######################################################################
#################
#Element Descriptions
##################
acis_els = ''
for el in WRCCData.acis_elements_dict.keys():
    acis_els+='%s : %s\n' %(el, WRCCData.acis_elements_dict[el]['name_long'])

help_date = 'yyyymmdd, yyyy-mm-dd or yyyy/mm/dd'
help_comma_elements = 'Comma separated list of climate elements. Available elements: \n %s' %acis_els
help_acis_elements = 'Available climate elements.'
help_grids = 'Gridded/modeled datasets available in ACIS.'
help_stn_selection = 'Defines the type of search area.'
help_grid_selection = 'Defines the type of search area.'
help_comma_stns = 'Delimiter separated list of station identifiers. Supported delimiters: comma, space, colon, semi-colon. Please use the station finder to find station ids.'
help_stn_id = 'Station identification number. Please use the Station Finder to find a station id.'
help_date_por = 'yyyymmdd, yyyy-mm-dd, yyyy/mm/dd or "por" (period of record) if single station.'
help_lon_lat = 'Grid point coordinate pair: Longitude, Latitude. Use the map interface by dragging the marker to change location.'
help_data_format = 'Defines format in which data will be returned. Note: html format prints to your screen.'
help_bbox = 'Bounding box latitudes and longitudes: West,South,East,North.'
help_max_missing_days = 'Ignore months with more than this number of days missing.'
help_data_summary = 'Temporal summarization to be performed on data.'

HELP_TEXTS = {
    'select_stations_by': help_stn_selection,
    'select_grid_by':help_grid_selection,
    'stn_id':help_stn_id,
    'grids': help_grids,
    'acis_elements':help_acis_elements,
    'comma_elements':help_comma_elements,
    'date':help_date,
    'date_por':help_date_por,
    'grid_lon_lat':help_lon_lat,
    'data_format':help_data_format,
    'comma_stns':help_comma_stns,
    'bbox':help_bbox,
    'max_missing_days':help_max_missing_days,
    'data_summary': help_data_summary
}
#####################################################################
#Custom form fields
#####################################################################

class MyDateField(forms.CharField):
    def to_python(self, date):
        # Return an empty string if no input was given.
        if not date:
            return ' '
        formatted_date = ''.join(date.split('-'))
        formatted_date = ''.join(formatted_date.split('/'))
        return formatted_date.lower()

    def validate(self, formatted_date):
        if formatted_date.lower() == 'por':
            if self.min_length == 8:
                raise forms.ValidationError("Date should be of form yyyymmdd or yyyy-mm-dd or yyyy/mm/dd.")
        else:
            if len(formatted_date)!=8:
                raise forms.ValidationError("Date should be of form yyyymmdd or yyyy-mm-dd or yyyy/mm/dd.")
            try:
                int(formatted_date)
            except:
                raise forms.ValidationError("Not a valid date.")
        #Check for leapyear
        if formatted_date.lower() != 'por':
            if not WRCCUtils.is_leap_year(formatted_date[0:4]) and formatted_date[4:6] == '02' and formatted_date[6:8] == '29':
                raise forms.ValidationError("%s is a leap year and February only has 28 days. Please change your date." %formatted_date[0:4])

class MyYearField(forms.CharField):
    def to_python(self, date):
        # Return an empty string if no input was given.
        if not date:
            return ' '
        return date.lower()

    def validate(self, date):
        if len(date) != 4 and date.lower() != 'por':
            raise forms.ValidationError("Not a vailid year.")
        try:
            int(date)
            if date[0] not in ['1', '2']:
                raise forms.ValidationError("Valid year range is: 1000 - 2999. You entered: %s" %date)
        except:
            if date.lower() != 'por':
                raise forms.ValidationError("Year should consist of four integers. You entered: %s" %date)

class MyWindowField(forms.CharField):
    def to_python(self, date):
        # Return an empty string if no input was given.
        if not date:
            return ' '
        return date

    def validate(self, date):
        if len(date) != 4:
            raise forms.ValidationError("Not a vailid time window.")
        try:
            mon = int(date[0:2])
            if mon < 1 or mon >12:
                raise forms.ValidationError("Valid month range is: 01 - 12. You entered: %s" %date[0:2])
            try:
                day = int(date[2:4])
                if mon == 2 and day >28:
                    raise forms.ValidationError("Valid date range for February is: 01 - 28. You entered: %s" %date[2:4])
            except:
                raise forms.ValidationError("Not a valid day. You entered: %s" %date[2:4])
        except:
            raise forms.ValidationError("Not a valid month. You entered: %s" %date[0:2])
        try:
            day = int(date[2:4])
            if day < 1 or day >13:
                raise forms.ValidationError("Valid day range is: 01 - 31. You entered: %s" %date[2:4])
        except:
            raise forms.ValidationError("Not a valid day. You entered: %s" %date[2:4])


class MyStateField(forms.CharField):
    def to_python(self, states):
        if not states:
            return ' '
        return states

    def validate(self, states):
        states_list = states.split(',')
        for state in states_list:
            if state not in WRCCData.fips_state_keys.keys() and state not in WRCCData.state_choices:
                raise forms.ValidationError('Need comma separated list of valid US states. Not a valid US State: %s' % state)
#for background data requests, see GridDataForm3, StationDataForm3
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
        return re.sub('\,+', ',',re.sub('[\,+\;\:\s+]', ',',stn_list).strip()).strip(',').split(',')

    def validate(self, stn_list):
        "Check if value consists only of valid station_ids."
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

class PolyField(forms.CharField):
    def to_python(self, poly_str):
        "Normalize data to a list of strings."
        # Return an empty string if no input was given.
        if not poly_str:
            return ' '
        return str(poly_str)
    def validate(self, poly_str):
        "Check if bbox_str is a valid bounding box."
        poly_list = poly_str.split(',')
        for ll in poly_list:
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
            el_strip= re.sub(r'(\d+)(\d+)', '', el) #strip digits from gddxx, hddxx, cddxx
            if str(el_strip) not in ['pcpn', 'snow', 'snwd', 'maxt', 'mint', 'avgt', 'obst', 'cdd', 'hdd', 'gdd', 'evap', 'wdmv']:
                raise forms.ValidationError(\
                mark_safe("elements should be a comma separated list of valid element choices:<br/>") + \
                mark_safe("pcpn, snow, snwd, <br/>") + \
                mark_safe("maxt, mint, avgt, <br/>") + \
                mark_safe("evap, wdmv, obst, cdd, hdd, gdd <br/>") + \
                mark_safe(" or cddxx, hddxx, gddxx where xx is the base temperature in Fahrenheit, e.g. 68<br/>") + \
                mark_safe("You entered: %s" %str(el)))

class MultiPRISMElementField(forms.CharField):
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
            if el not in ['maxt', 'mint', 'pcpn', 'dept']:
                raise forms.ValidationError(\
                    mark_safe('Not a valid PRISM data element') + \
                    mark_safe('Valid PRISM element choices:<br/>') + \
                    mark_safe('pcpn, maxt, mint, dewpt, <br/>') + \
                    mark_safe('You entered: %s' %str(el)))
######################################################################
#Form Classes
######################################################################
#Data download form
class DownloadForm(forms.Form):
    data_format = forms.ChoiceField(choices=DATA_FORMAT_CHOICES_LTD, initial='clm', help_text=HELP_TEXTS['data_format'])
    delimiter = forms.ChoiceField(choices=DELIMITER_CHOICES, initial='tab',help_text='Delimiter used to seperate data values. Not applicable for excel output.')
    output_file_name = MyNameField(required=False, initial='Output', help_text = 'Enter a name for your output file. Please do not use special characters (e.g. underscores are not allowed).')
    #output_file_name = forms.CharField(required=False,initial='Output', help_text ='Enter a name for your output file. Please do not use special characters (e.g. underscores are not allowed).')
#Generic form for Kelly's SOD programs
class SodForm(forms.Form):
    def __init__(self, *args, **kwargs):
        stn_id = kwargs.get('initial', {}).get('stn_id', None)
        start_date = kwargs.get('initial', {}).get('start_date', None)
        end_date = kwargs.get('initial', {}).get('end_date', None)
        start_year = kwargs.get('initial', {}).get('start_year', None)
        end_year = kwargs.get('initial', {}).get('end_year', None)
        date_type = kwargs.get('initial', {}).get('date_type', None) #y= year, d=full 8 digit date
        super(SodForm, self).__init__(*args, **kwargs)
        if stn_id is None:stn_id = self.data.get('station_ID')
        if start_date is None:start_date = self.data.get('start_date')
        if end_date is None:end_date = self.data.get('end_date')
        if start_year is None:start_year = self.data.get('start_year')
        if end_year is None:end_year = self.data.get('end_year')
        if date_type is None:date_type ='y'

        self.fields['date_type'] = forms.CharField(required=False, initial=date_type, widget=forms.HiddenInput())

        if stn_id is None:
            self.fields['station_ID'] = forms.CharField(required=False, initial='266779', help_text=HELP_TEXTS['stn_id'])
        else:
            self.fields['station_ID'] = forms.CharField(required=False, initial=stn_id, help_text=HELP_TEXTS['stn_id'])

        if date_type == 'd':
            if start_date is not None:
                self.fields['start_date'] = MyDateField(required=False, max_length=10, min_length=3, initial=start_date, help_text=HELP_TEXTS['date_por'])
            else:
                self.fields['start_date'] = MyDateField(required=False, max_length=10, min_length=3, initial='POR', help_text=HELP_TEXTS['date_por'])
            if end_date is not None:
                self.fields['end_date'] = MyDateField(required=False, max_length=10, min_length=3, initial=end_date, help_text=HELP_TEXTS['date_por'])
            else:
                self.fields['end_date'] = MyDateField(max_length=10, min_length=3, initial=yesterday, help_text=HELP_TEXTS['date_por'])
        elif date_type == 'y':
            if start_year is not None:
                self.fields['start_year'] = MyYearField(required=False,initial=start_year, help_text='yyyy or "POR" for period of record')
            else:
                self.fields['start_year'] = MyYearField(required=False, initial='POR', help_text='yyyy or "POR" for period of record')
            if end_year is not None:
                self.fields['end_year'] = MyYearField(required=False,initial=end_year, help_text='yyyy or "POR" for period of record')
            else:
                self.fields['end_year'] = MyYearField(required=False, initial=begin[0:4], help_text='yyyy or "POR" for period of record')

class SodsummForm(SodForm):
    def __init__(self, *args, **kwargs):
        super(SodsummForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['station_ID', 'start_year', 'end_year','summary_type','max_missing_days', 'generate_graphics']
    max_missing_days = forms.IntegerField(initial=5, required=False, help_text=HELP_TEXTS['max_missing_days'])
    summary_type = forms.ChoiceField(choices=SDMM_ELEMENT_CHOICES, initial='all', help_text= 'Only generate tables/graphs for these climate elements')
    generate_graphics = forms.ChoiceField(choices=([('T', 'Yes'),('F', 'No')]), initial='T', help_text= 'Generate plots from data')

class SodxtrmtsForm(SodForm):
    def __init__(self, *args, **kwargs):
        super(SodxtrmtsForm, self).__init__(*args, **kwargs)

        #self.fields.keyOrder = ['station_ID', 'element', 'monthly_statistic', 'start_year', 'end_year', 'max_missing_days', 'start_month', 'departures_from_averages', 'frequency_analysis','base_temperature', 'less_greater_or_between', 'threshold_low_for_between', 'threshold_low_for_between', 'threshold_for_less_or_greater', 'frequency_analysis_type']

        self.fields['element'] = forms.ChoiceField(choices=WRCCData.SXTR_ELEMENT_CHOICES, initial=kwargs.get('initial', {}).get('element', 'pcpn'), help_text = 'Climate Element')
        self.fields['start_year'] = MyYearField(max_length=4, min_length=3, initial=kwargs.get('initial', {}).get('start_year', 'POR'), help_text='Earliest start date. Format: yyyy or "POR" for period of record.')
        self.fields['end_year'] = MyYearField(max_length=4, min_length=3, initial=kwargs.get('initial', {}).get('end_year', '2013'), help_text='Latest end date. Format: yyyy or "POR" for period of record.')
        self.fields['monthly_statistic'] = forms.ChoiceField(choices=WRCCData.SXTR_ANALYSIS_CHOICES, initial=kwargs.get('initial', {}).get('monthly_statistic', 'msum'), help_text = 'Desired monthly characteristic of the selected climate element')
        self.fields['max_missing_days'] = forms.IntegerField(initial=kwargs.get('initial', {}).get('max_missing_days', 5), help_text=HELP_TEXTS['max_missing_days'])
        self.fields['start_month'] = forms.ChoiceField(choices=WRCCData.MONTH_CHOICES, initial=kwargs.get('initial', {}).get('start_month', '01'),help_text = 'Define a year as starting with this month.')
        self.fields['departures_from_averages']= forms.ChoiceField(choices = ([('T', 'Yes'),('F', 'No'),]), initial = kwargs.get('initial', {}).get('departures_from_averages', 'F'), help_text = 'Express results as departures from column averages.')
        self.fields['frequency_analysis'] = forms.ChoiceField(choices = ([('F', 'No'),]), initial = kwargs.get('initial', {}).get('frequency_analysis', 'F'), help_text='Perform Frequency Analysis. Coming Soon!')

        #Optional Params
        self.fields['base_temperature'] = forms.IntegerField(initial=kwargs.get('initial', {}).get('base_temperature', 65), help_text = 'Base Temperature for degree day element.')
        #self.fields['less_greater_or_between'] = forms.ChoiceField(widget=forms.Select(attrs = {'onclick' :"SetSodxtrmtsThresh(this)"}),choices = ([('l', 'Less Than'),('g', 'Greater Than'),('b', 'Between'),]), initial = kwargs.get('initial', {}).get('less_greater_or_between', 'g'), help_text='Number of Days less than/greater thana threshold or between two threshold.')
        self.fields['less_greater_or_between'] = forms.ChoiceField(widget=forms.RadioSelect,choices = ([('l', 'Less Than'),('g', 'Greater Than'),('b', 'Between'),]), initial = kwargs.get('initial', {}).get('less_greater_or_between', 'g'), help_text='Choose if you want to count the number of days that are less than/greater than a threshold or the number of days between an upper and lower thershold! Then choose the desired threshold(s) below!')
        self.fields['threshold_for_less_or_greater'] = forms.FloatField(initial = kwargs.get('initial', {}).get('threshold_for_less_or_greater', 0.005), help_text = 'Set this threshold if you chose "Less Than" or "Greater Than" above.')
        self.fields['threshold_low_for_between'] = forms.FloatField(initial = kwargs.get('initial', {}).get('threshold_low_for_between', 0.001),required=False, help_text = 'Set this lower threshold if you chose "Between" above.')
        self.fields['threshold_high_for_between'] = forms.FloatField(initial = kwargs.get('initial', {}).get('threshold_high_for_between', 0.11),required=False, help_text = 'Set this upper threshold if you chose "Between" above.')
        #self.fields['frequency_analysis_type']= forms.ChoiceField(choices = ([('p', 'Pearson III'),('g', 'GEV'),]), initial = kwargs.get('initial', {}).get('frequency_analysis_type', 'g'), help_text = 'Pearson III or Generalized Extreme Value frequency analysis otpions are available.')


class SodxtrmtsVisualizeForm(forms.Form):
    #months = forms.MultipleChoiceField(widget=CheckboxSelectMultiple, choices=WRCCData.MONTH_CHOICES, initial=WRCCData.MONTH_CHOICES[0], help_text = 'Choose one or more months to analyze.')
    start_month = forms.ChoiceField(choices=WRCCData.MONTH_CHOICES, initial='01', required=False, help_text = 'Start the visualization on this month.')
    end_month = forms.ChoiceField(choices=WRCCData.MONTH_CHOICES, initial='02', required=False, help_text = 'End the visualization on this month.')
    summary = forms.ChoiceField(choices=WRCCData.SXTR_SUMMARY_CHOICES, initial='mean', help_text='How to summarize the months.')
    show_running_mean = forms.ChoiceField(choices=([('F', 'No'), ('T', 'Yes')]), required=False, initial='T', help_text='Show running mean.')
    running_mean_years = forms.IntegerField(initial=9,required=False, help_text='Years over which to compute the running mean.')
    plot_incomplete_years = forms.ChoiceField(choices=([('F', 'No'), ('T', 'Yes')]), required=False, initial='F', help_text='Calculate and plot values even if the "maximum number of days missing" threhsold is not met.')
    #Plot Options
    graph_title = forms.CharField(required=False, initial='Use default', help_text='Enter a title to appear at the top of your graph.')
    image_size = forms.ChoiceField(choices=WRCCData.IMAGE_SIZES, initial='medium', help_text='Select an image size.')
    major_grid = forms.ChoiceField(choices=([('F', 'No'), ('T', 'Yes')]), required=False, initial='T', help_text='Show major grid.')
    minor_grid = forms.ChoiceField(choices=([('F', 'No'), ('T', 'Yes')]), required=False, initial='T', help_text='Show minor grid.')
    connector_line = forms.ChoiceField(choices=([('F', 'No'), ('T', 'Yes')]), required=False, initial='T', help_text='Connect data points.')
    connector_line_width = forms.FloatField(initial=1, max_value=10, min_value=0, required=False,help_text='Choose the width of the connector line. Choose 0 if you only want to see markers. 10 is the maximum line widh allowed.')
    markers = forms.ChoiceField(choices=([('F', 'No'), ('T', 'Yes')]), required=False, initial='T', help_text='Show markers at each data point.')
    marker_type = forms.ChoiceField(choices=WRCCData.MARKER_CHOICES, required=False, initial='diamond', help_text='.')

###############
#End SODS
##############

class StationDataForm0(forms.Form):
    def __init__(self, *args, **kwargs):
        stn_id = kwargs.get('initial', {}).get('stn_id', None)
        super(StationDataForm0, self).__init__(*args, **kwargs)

        if stn_id is None:
            stn_id = self.data.get('stn_id')

        if stn_id is None:
            self.fields['select_stations_by'] = forms.ChoiceField(choices=STN_FIND_CHOICES, required=False, initial='stnid', help_text=HELP_TEXTS['select_stations_by'])
        else:
            self.fields['select_stations_by'] = forms.ChoiceField(choices=STN_FIND_CHOICES,required=False, initial='stn_id', widget=forms.HiddenInput(), help_text=HELP_TEXTS['select_stations_by'])
            self.fields['stn_id'] = forms.CharField(required=False, initial=stn_id, help_text=HELP_TEXTS['stn_id'])
        self.fields['data_format'] = forms.ChoiceField(choices=DATA_FORMAT_CHOICES, initial='html', help_text=HELP_TEXTS['data_format'])

class StationDataForm1(forms.Form):
    def __init__(self, *args, **kwargs):
        select_stations_by = kwargs.get('initial', {}).get('select_stations_by', None)
        elements = kwargs.get('initial', {}).get('elements', None)
        data_format =  kwargs.get('initial', {}).get('data_format', None)
        stn_id = kwargs.get('initial', {}).get('stn_id', None)
        super(StationDataForm1, self).__init__(*args, **kwargs)

        if select_stations_by is None:
            select_stations_by = self.data.get('select_stations_by')
        if stn_id is None:
            stn_id = self.data.get('stn_id')
        if elements is None:
            elements = self.data.get('elements')
        if data_format is None:
            data_format = self.data.get('data_format')


        self.fields['select_stations_by'] = forms.CharField(initial=select_stations_by, widget=forms.HiddenInput(),help_text=HELP_TEXTS['select_stations_by'])
        #self.fields['select_stations_by'].widget.attrs = {'readonly':True, 'style':readonly_style}
        if select_stations_by == 'stn_id':
            self.fields['station_id'] = forms.CharField(required=False, initial=stn_id, help_text=HELP_TEXTS['stn_id'])
            self.fields['station_id'].widget.attrs = {'readonly':True, 'style':readonly_style}
        elif select_stations_by == 'stnid':
            self.fields['station_id'] = forms.CharField(required=False,initial='266779', help_text=HELP_TEXTS['stn_id'])
        elif select_stations_by == 'stnids':
            self.fields['station_ids'] = MultiStnField(required=False,initial='266779,050848', help_text=HELP_TEXTS['comma_stns'])
        elif select_stations_by == 'county':
            self.fields['county'] = forms.CharField(required=False,max_length=5, min_length=5, initial='08051', help_text='Valid US county identifier.')
        elif select_stations_by == 'climdiv':
            self.fields['climate_division'] = forms.CharField(required=False,max_length=4, min_length=4, initial='NV01', help_text='Valid US climate division identifier.')
        elif select_stations_by == 'cwa':
            self.fields['county_warning_area'] = forms.CharField(required=False,max_length=3, initial='PUB', help_text='US county warning area identifier. Both upper and lower case are valid input formats.')
        elif select_stations_by == 'basin':
            self.fields['basin'] = forms.CharField(required=False,max_length=8, min_length=8, initial='10180002', help_text='Valid US drainage basin identifier.')
        elif select_stations_by == 'state':
            self.fields['state'] = forms.ChoiceField(choices=STATE_CHOICES, initial='NV', help_text='Valid US state abreviation.')
        elif select_stations_by == 'bbox':
            self.fields['bounding_box'] = BBoxField(required=False,initial='-115,34,-114,35', help_text=HELP_TEXTS['bbox'])

        self.fields['elements'] = MultiElementField(initial='maxt,mint,pcpn', help_text=HELP_TEXTS['comma_elements'])
        if select_stations_by in ['stn_id', 'stnid']:
            self.fields['start_date'] = MyDateField(max_length=10, min_length=3, initial='POR', help_text=HELP_TEXTS['date_por'])
            self.fields['end_date'] = MyDateField(max_length=10, min_length=3, initial='POR', help_text=HELP_TEXTS['date_por'])
        else:
            self.fields['start_date'] = MyDateField(max_length=8, min_length=8, initial=begin, help_text=HELP_TEXTS['date'])
            self.fields['end_date'] = MyDateField(max_length=8, min_length=8, initial=yesterday, help_text=HELP_TEXTS['date'])
        self.fields['show_flags'] = forms.ChoiceField(choices=([('T', 'Yes'),('F', 'No')]), required=False, initial='F', help_text='Show the data flag with each data point.')
        self.fields['show_observation_time'] = forms.ChoiceField(choices=([('T', 'Yes'),('F', 'No')]), required=False, initial='F', help_text='Show the hour at which the observation was taken for each data point.(1 - 24 =  midnight, -1 means no observation time was recorded)')
        if data_format:
            self.fields['data_format'] = forms.ChoiceField(choices=DATA_FORMAT_CHOICES, initial=data_format, help_text=HELP_TEXTS['data_format'])
            if data_format in ['clm', 'dlm', 'xl']:
                self.fields['output_file_name'] = MyNameField(required=False,initial='DataRequest', help_text='Name of output file. Special characters are not allowed. Spaces will be ignored')
        else:
            self.fields['data_format'] = forms.ChoiceField(choices=DATA_FORMAT_CHOICES, initial='dlm', help_text=HELP_TEXTS['data_format'])
            self.fields['output_file_name'] = MyNameField(required=False,initial='DataRequest', help_text='Name of output file. Special characters are not allowed. Spaces will be ignored')
        if data_format in ['dlm', 'clm', 'html']:
            self.fields['delimiter'] = forms.ChoiceField(choices=DELIMITER_CHOICES, help_text='Delimiter used to seperate data values.')

class StationDataForm3(forms.Form):
   def __init__(self, *args, **kwargs):
        select_stations_by = kwargs.get('initial', {}).get('select_stations_by', None)
        data_format =  kwargs.get('initial', {}).get('data_format', None)
        super(StationDataForm3, self).__init__(*args, **kwargs)

        if select_stations_by is None:
            select_stations_by = self.data.get('select_stations_by')
        if data_format is None:
            data_format = self.data.get('data_format')


        self.fields['user_name'] = MyNameField(initial='Your Name', help_text = 'Enter a user name without special characters (e.g. underscores are not allowed). Example: first name initial + last name.')
        self.fields['email'] = forms.EmailField(initial='Your e-mail', help_text='Enter a valid e-mail address at wich we can reach you.')

        self.fields['select_stations_by'] = forms.CharField(initial=select_stations_by, widget=forms.HiddenInput(), help_text=HELP_TEXTS['select_stations_by'])
        if select_stations_by == 'stn_id':
            self.fields['station_id'] = forms.CharField(initial=kwargs.get('initial', {}).get('stn_id', None), help_text=HELP_TEXTS['stn_id'])
        elif select_stations_by == 'stnid':
            self.fields['station_id'] = forms.CharField(initial=kwargs.get('initial', {}).get('station_id', None), help_text=HELP_TEXTS['stn_id'])
        elif select_stations_by == 'stnids':
            self.fields['station_ids'] = MultiStnField(initial=kwargs.get('initial', {}).get('station_ids', None),help_text=HELP_TEXTS['comma_stns'])
        elif select_stations_by == 'county':
            self.fields['county'] = forms.CharField(max_length=5, min_length=5, initial=kwargs.get('initial', {}).get('county', None),help_text='Valid US county identifier.')
        elif select_stations_by == 'climdiv':
            self.fields['climate_division'] = forms.CharField(max_length=4, min_length=4, initial=kwargs.get('initial', {}).get('climate_division', None),help_text='Valid US climate division identifier.')
        elif select_stations_by == 'cwa':
            self.fields['county_warning_area'] = forms.CharField(max_length=3, initial=kwargs.get('initial', {}).get('county_warning_area', None),help_text='US county warning area identifier. Both upper and lower case are valid input formats.')
        elif select_stations_by == 'basin':
            self.fields['basin'] = forms.CharField(max_length=8, min_length=8, initial=kwargs.get('initial', {}).get('basin', None),help_text='Valid US drainage basin identifier.')
        elif select_stations_by == 'state':
            self.fields['state'] = forms.ChoiceField(choices=STATE_CHOICES, initial=kwargs.get('initial', {}).get('state', None),help_text='Valid US state abreviation.')
        elif select_stations_by == 'bbox':
            self.fields['bounding_box'] = BBoxField(initial=kwargs.get('initial', {}).get('bounding_box', None),help_text=HELP_TEXTS['bbox'])
        self.fields['elements'] = MultiElementField(initial=kwargs.get('initial', {}).get('elements', None), help_text=HELP_TEXTS['comma_elements'])
        self.fields['start_date'] = MyDateField(max_length=10, min_length=3, initial=kwargs.get('initial', {}).get('start_date', None),help_text=HELP_TEXTS['date_por'])
        self.fields['end_date'] = MyDateField(max_length=10, min_length=3, initial=kwargs.get('initial', {}).get('end_date', None), help_text=HELP_TEXTS['date_por'])
        self.fields['show_flags'] = forms.ChoiceField(choices=([('T', 'Yes'),('F', 'No')]), required=False, initial=kwargs.get('initial', {}).get('show_flags', 'F'), help_text='Show the data flag with each data point. Data Flags: M = Missing, T = Trace, S = Subsequent, A = Accumulated')
        self.fields['show_observation_time'] = forms.ChoiceField(choices=([('T', 'Yes'),('F', 'No')]), required=False, initial=kwargs.get('initial', {}).get('show_observation_time', 'F'), help_text='Show the time at which the observation was taken for each data point.')
        if data_format:
            self.fields['data_format'] = forms.ChoiceField(choices=DATA_FORMAT_CHOICES, initial=data_format, help_text=HELP_TEXTS['data_format'])
            if data_format in ['clm', 'dlm', 'xl']:
                self.fields['output_file_name'] = forms.ChoiceField(required=False, initial='DataRequest', help_text='Name of output file. Special characters are not allowed. Spaces will be ignored.')
        else:
            self.fields['data_format'] = forms.ChoiceField(choices=DATA_FORMAT_CHOICES, initial='dlm', help_text=HELP_TEXTS['data_format'])
            self.fields['output_file_name'] = MyNameField(required=False,initial='DataRequest', help_text='Name of output file. Special characters are not allowed. Spaces will be ignored')
        if data_format in ['dlm', 'clm', 'html']:
            self.fields['delimiter'] = forms.ChoiceField(choices=DELIMITER_CHOICES, help_text='Delimiter used to seperate data values.')

class GridDataForm0(forms.Form):
        select_grid_by = forms.ChoiceField(choices=select_grid_by_CHOICES, required=False, initial='point', help_text=HELP_TEXTS['select_stations_by'])
        temporal_resolution = forms.ChoiceField(choices=([('dly', 'Daily'),('mly', 'Monthly'),('yly', 'Yearly')]), required=False, initial='dly', help_text='Time resolution of data.')
        data_summary = forms.ChoiceField(choices=GRID_SUMMARY_CHOICES, required=False, initial='mean', help_text=HELP_TEXTS['data_summary'])
        data_format = forms.ChoiceField(choices=DATA_FORMAT_CHOICES, initial='html', help_text=HELP_TEXTS['data_format'])

class GridDataForm1(forms.Form):
    def __init__(self, *args, **kwargs):
        select_grid_by = kwargs.get('initial', {}).get('select_grid_by', None)
        location = kwargs.get('initial', {}).get('location', None)
        temporal_resolution = kwargs.get('initial', {}).get('temporal_resolution', None)
        data_summary = kwargs.get('initial', {}).get('data_summary', None)
        data_format =  kwargs.get('initial', {}).get('data_format', None)
        super(GridDataForm1, self).__init__(*args, **kwargs)

        if select_grid_by is None:select_grid_by = self.data.get('select_grid_by')
        if temporal_resolution is None:temporal_resolution = self.data.get('temporal_resolution')
        if data_summary is None:data_summary = self.data.get('data_summary')
        if data_format is None:data_format = self.data.get('data_format')

        if select_grid_by == 'point':
            self.fields['location'] = forms.CharField(initial="-119,39", help_text=HELP_TEXTS['grid_lon_lat'])
        elif select_grid_by == 'state':
            self.fields['state'] = forms.ChoiceField(choices=STATE_CHOICES, initial='NV', help_text='US state abbreviation.')
        elif select_grid_by == 'bbox':
            self.fields['bounding_box'] = BBoxField(initial='-115,34,-114,35', help_text=HELP_TEXTS['bbox'])
        else:
            self.fields['bounding_box'] = BBoxField(initial='-115,34,-114,35', help_text=HELP_TEXTS['bbox'])

        self.fields['select_grid_by'] = forms.CharField(initial=select_grid_by, widget=forms.HiddenInput(), help_text=HELP_TEXTS['select_stations_by'])
        if location is not None:
            self.fields['location'] = forms.CharField(initial=location, help_text=HELP_TEXTS['grid_lon_lat'])
        if temporal_resolution in ['mly', 'yly']:
            self.fields['elements'] = MultiPRISMElementField(initial='maxt,mint,pcpn', help_text=HELP_TEXTS['comma_elements'])
            self.fields['grid'] = forms.ChoiceField(choices=([('21', 'PRISM')]), help_text=HELP_TEXTS['grids'])
        elif temporal_resolution == 'dly':
            self.fields['elements'] = MultiElementField(initial='maxt,mint,pcpn', help_text=HELP_TEXTS['comma_elements'])
            self.fields['grid'] = forms.ChoiceField(choices=GRID_CHOICES, help_text=HELP_TEXTS['grids'])
        if select_grid_by == 'point':
            if temporal_resolution in ['mly', 'yly']:
                if select_grid_by == 'point':
                    self.fields['start_date'] = MyDateField(max_length=10, min_length=8,initial='18950101', help_text=HELP_TEXTS['date'])
                else:
                    self.fields['start_date'] = MyDateField(max_length=10, min_length=8,initial='20120101', help_text=HELP_TEXTS['date'])
                    #Not working for some reason
                    #self.fields['start_date'] = MyDateField(max_length=10, min_length=8,initial=begin_prism, help_text=HELP_TEXTS['date'])
            else:
                self.fields['start_date'] = MyDateField(max_length=10, min_length=8,initial=begin, help_text=HELP_TEXTS['date'])
        else:
            if temporal_resolution in ['mly', 'yly']:
                self.fields['start_date'] = MyDateField(max_length=10, min_length=8,initial='20120101', help_text=HELP_TEXTS['date'])
                #Not working for some reason
                #self.fields['start_date'] = MyDateField(max_length=10, min_length=8,initial=begin_prism, help_text=HELP_TEXTS['date'])
            else:
                self.fields['start_date'] = MyDateField(max_length=10, min_length=8,initial=yesterday, help_text=HELP_TEXTS['date'])
        if temporal_resolution in ['mly', 'yly']:
            #Not working for some reasons
            #self.fields['end_date'] = MyDateField(max_length=10, min_length=8, initial=yesterday, help_text=HELP_TEXTS['date']
            self.fields['end_date'] = MyDateField(max_length=10, min_length=8, initial='20130101', help_text=HELP_TEXTS['date'])
        else:
            self.fields['end_date'] = MyDateField(max_length=10, min_length=8, initial=yesterday, help_text=HELP_TEXTS['date'])
        if data_format:
            self.fields['data_format'] = forms.ChoiceField(choices=DATA_FORMAT_CHOICES, initial=data_format, help_text=HELP_TEXTS['data_format'])
            if data_format in ['clm', 'dlm', 'xl']:
                self.fields['output_file_name'] = MyNameField(required=False,initial='DataRequest', help_text='Name of output file. Special characters are not allowed. Spaces will be ignored')
        else:
            self.fields['data_format'] = forms.ChoiceField(choices=DATA_FORMAT_CHOICES, initial='dlm', help_text=HELP_TEXTS['data_format'])
            self.fields['output_file_name'] = MyNameField(required=False,initial='DataRequest', help_text='Name of output file. Special characters are not allowed. Spaces will be ignored')
        if data_format in ['dlm', 'clm', 'html']:
            self.fields['delimiter'] = forms.ChoiceField(choices=DELIMITER_CHOICES, help_text='Delimiter used to seperate data values.')
        if data_summary is None or data_summary == 'none' or select_grid_by == 'point':
            self.fields['visualize'] = forms.ChoiceField(choices=([('F', 'No'), ('T', 'Yes')]), widget=forms.HiddenInput(),required=False, initial='F', help_text='Generate a map to visualize data')
            #self.fields['data_summary'] = forms.CharField(widget=forms.HiddenInput(), required=False, initial='none', help_text=HELP_TEXTS['data_summary'])
            self.fields['data_summary'] = forms.CharField(initial='none', help_text=HELP_TEXTS['data_summary'])
            self.fields['data_summary'].widget.attrs = {'readonly':True, 'style':readonly_style}
        else:
            self.fields['visualize'] = forms.ChoiceField(choices=([('F', 'No'), ('T', 'Yes')]), required=False, initial='F', help_text='Generate a map to visualize data')
            #self.fields['data_summary'] = forms.ChoiceField(choices=GRID_SUMMARY_CHOICES, initial=data_summary, help_text=HELP_TEXTS['data_summary'])
            self.fields['data_summary'] = forms.CharField(initial=data_summary, help_text=HELP_TEXTS['data_summary'])
            self.fields['data_summary'].widget.attrs = {'readonly':True, 'style':readonly_style}
        #self.fields['temporal_resolution'] = forms.CharField(initial=temporal_resolution, widget=forms.HiddenInput())
        self.fields['temporal_resolution']  = forms.CharField(initial=temporal_resolution, help_text='Time resolution of data.')
        self.fields['temporal_resolution'].widget.attrs = {'readonly':True, 'style':readonly_style}

class GridDataForm3(forms.Form):
    def __init__(self, *args, **kwargs):
        select_grid_by = kwargs.get('initial', {}).get('select_grid_by', None)
        data_format =  kwargs.get('initial', {}).get('data_format', None)
        temporal_resolution = kwargs.get('initial', {}).get('temporal_resolution', None)
        data_summary = kwargs.get('initial', {}).get('summary', None)
        super(GridDataForm3, self).__init__(*args, **kwargs)

        if select_grid_by is None:select_grid_by = self.data.get('select_grid_by')
        if data_format is None:data_format = self.data.get('data_format')
        if temporal_resolution is None:temporal_resolution = self.data.get('temporal_resolution')
        if data_summary is None:data_summary = self.data.get('data_summary')

        self.fields['user_name'] = MyNameField(initial='Your Name', help_text = 'Enter a user name without special characters.Example: first name initial + last name.')
        self.fields['email'] = forms.EmailField(initial='Your e-mail', help_text='Enter a valid e-mail address at wich we can reach you.')

        if select_grid_by == 'point':
            self.fields['location'] = forms.CharField(initial=kwargs.get('initial', {}).get('location', None), help_text='Gridpoint coordinates: latitude, longitude.')
        elif select_grid_by == 'state':
            self.fields['state'] = forms.ChoiceField(initial=kwargs.get('initial', {}).get('state', None), choices=STATE_CHOICES, help_text='US state abbreviation.')
        elif select_grid_by == 'bbox':
            self.fields['bounding_box'] = BBoxField(initial=kwargs.get('initial', {}).get('bounding_box', None), help_text=HELP_TEXTS['bbox'])
        if temporal_resolution in ['mly', 'yly']:
            self.fields['elements'] = MultiPRISMElementField(initial='maxt,pcpn', help_text=HELP_TEXTS['comma_elements'])
            self.fields['grid'] = forms.ChoiceField(choices=([('21', 'PRISM')]), help_text=HELP_TEXTS['grids'])
        else:
            self.fields['elements'] = MultiElementField(initial='maxt,mint,pcpn', help_text=HELP_TEXTS['comma_elements'])
            self.fields['grid'] = forms.ChoiceField(choices=GRID_CHOICES, help_text=HELP_TEXTS['grids'])
        self.fields['start_date'] = MyDateField(max_length=10, min_length=8, initial=kwargs.get('initial', {}).get('start_date', None), help_text=HELP_TEXTS['date'])
        self.fields['end_date'] = MyDateField(max_length=10, min_length=8, initial=kwargs.get('initial', {}).get('end_date', None), help_text=HELP_TEXTS['date'])
        if data_format:
            self.fields['data_format'] = forms.ChoiceField(choices=DATA_FORMAT_CHOICES, initial=data_format, help_text=HELP_TEXTS['data_format'])
            if data_format in ['clm', 'dlm', 'xl']:
                self.fields['output_file_name'] = MyNameField(required=False,initial='DataRequest', help_text='Name of output file. Special characters are not allowed. Spaces will be ignored')
        else:
            self.fields['data_format'] = forms.ChoiceField(choices=DATA_FORMAT_CHOICES, initial='dlm', help_text=HELP_TEXTS['data_format'])
            self.fields['output_file_name'] = MyNameField(required=False,initial='DataRequest', help_text='Name of output file. Special characters are not allowed. Spaces will be ignored')
        if data_format in ['dlm', 'clm', 'html']:
            self.fields['delimiter'] = forms.ChoiceField(choices=DELIMITER_CHOICES, help_text='Delimiter used to seperate data values.')
        self.fields['select_grid_by'] = forms.CharField(initial=select_grid_by, widget=forms.HiddenInput(), help_text=HELP_TEXTS['select_stations_by'])
        if data_summary is None or data_summary == 'none' or select_grid_by == 'point' or temporal_resolution in ['mly', 'yly']:
            self.fields['visualize'] = forms.ChoiceField(choices=([('F', 'No'), ('T', 'Yes')]), widget=forms.HiddenInput(),required=False, initial='F', help_text='Generate a map to visualize data')
            #self.fields['data_summary'] = forms.ChoiceField(choices=GRID_SUMMARY_CHOICES, widget=forms.HiddenInput(), initial=kwargs.get('initial', {}).get('data_summary', 'none'), help_text='Temporal summarization to be performed on data.')
            self.fields['data_summary'] = forms.CharField(initial='none', help_text=HELP_TEXTS['data_summary'])
            self.fields['data_summary'].widget.attrs = {'readonly':True, 'style':readonly_style}
        else:
            self.fields['visualize'] = forms.ChoiceField(choices=([('F', 'No'), ('T', 'Yes')]), required=False, initial='F', help_text='Generate a map to visualize data')
            #self.fields['data_summary'] = forms.ChoiceField(choices=GRID_SUMMARY_CHOICES, initial=data_summary, help_text='Temporal summarization to be performed on data.')
            self.fields['data_summary'] = forms.CharField(initial=data_summary, help_text=HELP_TEXTS['data_summary'])
            self.fields['data_summary'].widget.attrs = {'readonly':True, 'style':readonly_style}
            #self.fields['temporal_resolution'] = forms.CharField(initial=temporal_resolution, widget=forms.HiddenInput())
            self.fields['temporal_resolution']  = forms.CharField(initial=temporal_resolution, help_text='Time resolution of data.')
            self.fields['temporal_resolution'].widget.attrs = {'readonly':True, 'style':readonly_style}

#Data Application Forms
class MetaGraphForm(forms.Form):
    def __init__(self, *args, **kwargs):
        stn_id = kwargs.get('initial', {}).get('stn_id', None)
        super(MetaGraphForm, self).__init__(*args, **kwargs)

        if stn_id is None:
            stn_id = self.data.get('stn_id')

        if stn_id is None:
            self.fields['station_id'] = forms.CharField(required=True, initial='266779', help_text='COOP station identification number. Please use the Station Finder to find your station id.')
        else:
            self.fields['station_id'] = forms.CharField(required=True, initial=stn_id, help_text='COOP station identification number. Please use the Station Finder to find your station id.')

class MonthlyAveragesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        stn_id = kwargs.get('initial', {}).get('stn_id', None)
        super(MonthlyAveragesForm, self).__init__(*args, **kwargs)

        if stn_id is None:
            stn_id = self.data.get('stn_id')

        if stn_id is None:
            self.fields['station_id'] = forms.CharField(required=False, initial='266779', help_text=HELP_TEXTS['stn_id'])
        else:
            self.fields['station_id'] = forms.CharField(required=False, initial=stn_id, help_text=HELP_TEXTS['stn_id'])
        self.fields['elements'] = MultiElementField(initial='maxt,mint,pcpn,snow,snwd', help_text=HELP_TEXTS['comma_elements'])
        self.fields['start_date'] = MyDateField(max_length=10, required = False, initial='POR', help_text=HELP_TEXTS['date_por'])
        self.fields['end_date'] = MyDateField(max_length=10, required = False, initial='POR', help_text=HELP_TEXTS['date_por'])

class ClimateRiskForm0(forms.Form):
        select_grid_by = forms.ChoiceField(choices=GRID_FIND_CHOICES, required=False, initial='shape', help_text=HELP_TEXTS['select_stations_by'])
        element = forms.ChoiceField(choices=CLIM_RISK_ELEMENT_CHOICES, required=False, initial='maxt', help_text='Climate Element')


class ClimateRiskForm1(forms.Form):
    def __init__(self, *args, **kwargs):
        select_grid_by = kwargs.get('initial', {}).get('select_grid_by', None)
        element = kwargs.get('initial', {}).get('element', None)
        state = kwargs.get('initial', {}).get('state', None)
        bounding_box = kwargs.get('initial', {}).get('bounding_box', None)
        start_date = kwargs.get('initial', {}).get('start_date', None)
        end_date = kwargs.get('initial', {}).get('end_date', None)
        super(ClimateRiskForm1, self).__init__(*args, **kwargs)

        if select_grid_by is None:select_grid_by = self.data.get('select_grid_by')
        if element is None:element = self.data.get('element')
        if state is None:state=self.data.get('state')
        if bounding_box is None:bounding_box=self.data.get('bounding_box')
        if start_date is None:start_date=self.data.get('start_date')
        if end_date is None:end_date=self.data.get('end_date')


        self.fields['select_grid_by'] = forms.CharField(required=False, initial=select_grid_by, widget=forms.HiddenInput(), help_text=HELP_TEXTS['select_grid_by'])

        if select_grid_by == 'shape' or bounding_box is not None:
            self.fields['shape'] = PolyField(required=False,initial='-115,34, -115, 35,-114,35, -114, 34', help_text='Use the map interface to select your polygon.')
        elif select_grid_by == 'state':
            self.fields['state'] = forms.ChoiceField(choices=STATE_CHOICES, initial='NV',help_text='US state.')
        elif select_grid_by == 'county':
            self.fields['county'] = forms.CharField(required=False,max_length=5, min_length=5, initial='08051', help_text='Valid US county identifier.')
        elif select_grid_by == 'climdiv':
            self.fields['climate_division'] = forms.CharField(required=False,max_length=4, min_length=4, initial='NV01', help_text='Valid US climate division identifier.')
        elif select_grid_by == 'cwa':
            self.fields['county_warning_area'] = forms.CharField(required=False,max_length=3, initial='PUB', help_text='US county warning area identifier. Both upper and lower case are valid input formats.')
        elif select_grid_by == 'basin':
            self.fields['basin'] = forms.CharField(required=False,max_length=8, min_length=8, initial='10180002', help_text='Valid US darinage basin identifier.')
        elif state is not None:
            self.fields['state'] = forms.ChoiceField(required=False, choices=STATE_CHOICES, initial=state, help_text='US state.')
        self.fields['element'] = forms.ChoiceField(choices=CLIM_RISK_ELEMENT_CHOICES,initial=element, help_text='Climate Element')
        self.fields['element'].widget.attrs = {'readonly':True, 'style':readonly_style}
        if start_date is None:
            self.fields['start_date'] = MyDateField(required = False, initial=begin, help_text=HELP_TEXTS['date'])
        else:
            self.fields['start_date'] = MyDateField(required = False, initial=start_date, help_text=HELP_TEXTS['date'])
        if end_date is None:
            self.fields['end_date'] = MyDateField(required = False, initial=today, help_text=HELP_TEXTS['date'])
        else:
            self.fields['end_date'] = MyDateField(required = False, initial=end_date, help_text=HELP_TEXTS['date'])
        self.fields['summary'] = forms.ChoiceField(choices=WRCCData.CLIM_RISK_SUMMARY_CHOICES, initial='mean',help_text='How to spatially summarize gridpoints lying in polygon.')
        self.fields['grid'] = forms.ChoiceField(choices=GRID_CHOICES, help_text=HELP_TEXTS['grids'])

        '''
        if element == 'maxt':lower='50';upper='90';max_dec = 1
        if element == 'mint':lower='30';upper='70';max_dec = 1
        if element == 'avgt':lower='40';upper='60';max_dec = 1
        if element == 'pcpn':lower='0.0';upper='1.0';max_dec = 2
        self.fields['lower_threshold'] = forms.DecimalField(max_digits=5, decimal_places=max_dec,required=False, initial=lower, help_text='Lower threshold')
        self.fields['upper_threshold'] = forms.DecimalField(max_digits=5, decimal_places=max_dec,required=False, initial=upper, help_text='Upper threshold')
        self.fields['number_of_days']  = forms.CharField(required=False, initial='all', help_text='Number of days the threshold conditions should be met.')
        self.fields['window_start'] = MyWindowField(max_length=4, min_length=4, required = False, initial='0101', help_text='mmdd')
        self.fields['window_end'] = MyWindowField(max_length=4, min_length=4, required = False, initial='1231', help_text='mmdd')
        '''
class ClimateMapForm0(forms.Form):
        select_grid_by = forms.ChoiceField(choices=([('state', 'State'),('bbox', 'Bounding Box')]), required=False, initial='state', help_text=HELP_TEXTS['select_stations_by'])
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
        grid = kwargs.get('initial', {}).get('grid', None)
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
        if state is None:state=self.data.get('state')
        if bounding_box is None:bounding_box=self.data.get('bounding_box')

        self.fields['select_grid_by'] = forms.CharField(required=False, initial=select_grid_by, widget=forms.HiddenInput(), help_text=HELP_TEXTS['select_grid_by'])
        if select_grid_by == 'state':
            self.fields['state'] = forms.ChoiceField(choices=STATE_CHOICES, initial='NV',help_text='US state.')
        elif select_grid_by == 'bbox':
            self.fields['bounding_box'] = BBoxField(required=False,initial='-115,34,-114,35', help_text=HELP_TEXTS['bbox'])
        elif state is not None:
            self.fields['state'] = forms.ChoiceField(required=False, choices=STATE_CHOICES, initial=state, help_text='US state.')
        elif bounding_box is not None:
            self.fields['bounding_box'] = BBoxField(required=False,initial=bounding_box, help_text=HELP_TEXTS['bbox'])
        if element is not None:
            self.fields['element'] = forms.ChoiceField(choices=ACIS_ELEMENT_CHOICES,initial=element, help_text='Valid element recognized by Acis.')
        else:
            self.fields['element'] = forms.ChoiceField(choices=ACIS_ELEMENT_CHOICES,initial=element, help_text='Valid element recognized by Acis.')
        if element == 'cddxx':
            self.fields['base_temperature_cddxx'] = forms.IntegerField(initial=65, help_text='Base temperature used to calculate cooling degree days.')
        if element == 'hddxx':
            self.fields['base_temperature_hddxx'] = forms.IntegerField(initial=65, help_text='Base temperature used to calculate heating degree days.')
        if element == 'gddxx':
            self.fields['base_temperature_gddxx'] = forms.IntegerField(initial=50, help_text='Base temperature used to calculate growing degree days.')

        if time_period == 'custom':
            self.fields['start_date'] = MyDateField(max_length=10, min_length=8, required = False, initial=begin, help_text=HELP_TEXTS['date'])
            self.fields['end_date'] =MyDateField(max_length=10, min_length=8, required = False, initial=yesterday, help_text=HELP_TEXTS['date'])
        elif start_date is not None and end_date is not None:
            self.fields['start_date'] = MyDateField(max_length=10, min_length=8, required = False, initial=start_date, help_text=HELP_TEXTS['date'])
            self.fields['end_date'] =MyDateField(max_length=10, min_length=8, required = False, initial=end_date, help_text=HELP_TEXTS['date'])
        else:
            if x is None:
                self.fields['start_date'] = MyDateField(max_length=10, min_length=8, required = False, initial='20130101', help_text=HELP_TEXTS['date'])
            else:
                start_date = WRCCUtils.get_start_date(time_period,yesterday, x)
                self.fields['start_date'] = MyDateField(required = False, initial=start_date, help_text=HELP_TEXTS['date'])
                self.fields['start_date'].widget.attrs = {'readonly':True, 'style':readonly_style}
            self.fields['end_date'] = MyDateField(required=False, initial=yesterday, help_text=HELP_TEXTS['date'])
            self.fields['end_date'].widget.attrs = {'readonly':True, 'style':readonly_style}
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
                 self.fields['lat'] = forms.FloatField(initial='38.86', required=True, help_text='Valid latitude.')
            else:
                self.fields['lat'] = forms.FloatField(initial=lat, required=True, help_text='Valid latitude.')
            if lon is None:
                 self.fields['lon'] = forms.FloatField(initial='-119.76', required=True, help_text='Valid longitude.')
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
                self.fields['end_date'] = MyDateField(max_length=10, min_length=8, required = False, initial=yesterday, help_text=HELP_TEXTS['date'])
            else:
                self.fields['end_date'] = MyDateField(max_length=10, min_length=8, required = False, initial=end_date, help_text=HELP_TEXTS['date'])
            if grid is None:
                self.fields['grid'] = forms.ChoiceField(choices=GRID_CHOICES, help_text=HELP_TEXTS['grids'])
            else:
                self.fields['grid'] = forms.ChoiceField(choices=GRID_CHOICES, initial=grid, help_text=HELP_TEXTS['grids'])
class StationLocatorForm0(forms.Form):
    select_stations_by = forms.ChoiceField(choices=STN_FIND_CHOICES_SHORT, required=False, initial='state', help_text=HELP_TEXTS['select_stations_by'])
    element_selection = forms.ChoiceField(choices=([('T', 'Choose climate elements'),('F', 'Any climate element')]), required=False, initial='F', help_text='Only look for stations that have data for all of these elements.')
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
        self.fields['element_selection'] = forms.CharField(required=False, initial=element_selection, widget=forms.HiddenInput(), help_text='Only look for stations that have data for all of these elements.')

        if select_stations_by == 'stn_id':
            self.fields['station_id'] = forms.CharField(initial=stn_id, help_text=HELP_TEXTS['stn_id'])
            self.fields['station_id'].widget.attrs = {'readonly':True, 'style':readonly_style}
        elif select_stations_by == 'stnid':
            self.fields['station_id'] = forms.CharField(initial='266779',help_text=HELP_TEXTS['stn_id'])
        elif select_stations_by == 'stnids':
            self.fields['station_ids'] = MultiStnField(required=False,initial='266779,050848', help_text=HELP_TEXTS['comma_stns'])
        elif select_stations_by == 'county':
            self.fields['county'] = forms.CharField(required=False,max_length=5, min_length=5, initial='08051', help_text='Valid US county identifier.')
        elif select_stations_by == 'climdiv':
            self.fields['climate_division'] = forms.CharField(required=False,max_length=4, min_length=4, initial='NV01', help_text='Valid US climate division identifier.')
        elif select_stations_by == 'cwa':
            self.fields['county_warning_area'] = forms.CharField(required=False,max_length=3, initial='PUB', help_text='US county warning area identifier. Both upper and lower case are valid input formats.')
        elif select_stations_by == 'basin':
            self.fields['basin'] = forms.CharField(required=False,max_length=8, min_length=8, initial='10180002', help_text='Valid US darinage basin identifier.')
        elif select_stations_by == 'state':
            self.fields['state'] = forms.ChoiceField(choices=STATE_CHOICES, initial='NV', help_text='US state.')
        elif select_stations_by == 'states':
            self.fields['states'] = MyStateField(initial='nv,id', help_text='Comma separated list of US state appreviations. Both upper and lower case are valid input formats.')
        elif select_stations_by == 'sw_states':
            self.fields['states'] = MyStateField(initial='ca,nv,co,nm,az,ut', help_text='Comma separated list of US states. Both upper and lower case are valid input formats.')
        elif select_stations_by == 'bbox':
            self.fields['bounding_box'] = BBoxField(required=False,initial='-115,34,-114,35', help_text=HELP_TEXTS['bbox'])
        if element_selection == 'T':
            self.fields['elements'] = MultiElementField(initial='maxt,mint,pcpn', help_text=HELP_TEXTS['comma_elements'])

            self.fields['start_date'] = MyDateField(max_length=10, required = False, initial='18900101',min_length=8, help_text=HELP_TEXTS['date'])
            self.fields['end_date'] = MyDateField(max_length=10, required = False, initial=yesterday,min_length=8, help_text=HELP_TEXTS['date'])
            self.fields['constraints'] = forms.ChoiceField(choices=STN_FINDER_LOGIC, required=False, initial='any_any')

