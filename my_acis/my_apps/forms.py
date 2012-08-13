from django import forms
from django.forms.fields import ChoiceField, MultipleChoiceField
from django.contrib.localflavor.us.forms import USStateField, USStateSelect
from django.contrib.localflavor.us.us_states import STATE_CHOICES

import datetime

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

#Choice fields for WRCC data app forms
##############################################################################
#NOTE: the names given to the form quantities should be the commanline options
#of the correcsponding preogram with underscores instead of dashes!!!
#Important for string handling in my_apps/views.py

#SODRUN CHOICES
SR_ELEMENT_CHOICES = (
        ('maxt', 'Maximum Temprature (Whole Degrees)'),
        ('mint', 'Minimum Temperature(Whole Degrees)'),
        ('snow', 'Snowfall (Tenth of inches)'),
        ('snwd', 'Snowdepth (Whole inches)'),
        ('pcpn', 'Precipitation (Hundredths of inches)'),
        )
AEB_CHOICES = (
        ('A', 'Above'),
        ('B', 'Below'),
        ('E', 'Equal to'),
        )

#SODLIST CHOICES
SL_FRMT_CHOICES = (
        ('json', 'JSON Format'),
        ('kr','ASCII Format'),
        ('kr_csv', 'Comma Separated Values'),
        )

#SODMONLINE(MY) CHOICES
SM_FRMT_CHOICES = (
        ('json', 'JSON'),
        ('kr', 'ASCII'),
        )
SM_ELEMENT_CHOICES = (
        ('pcpn', 'Precipitation (Hundredths of Inches)'),
        ('snow', 'Snowfall (Tenths of Inches)'),
        ('snwd', 'Snowdepth (Whole Inches)'),
        ('maxt', 'Maximum Temprature (Whole or Tenths of Degrees)'),
        ('mint', 'Minimum Temperature(Whole or Tenths of Degrees)'),
        ('avgt', 'Mean Temperature(Whole or Tenths of Degrees)'),
        ('dtr', 'Daily Temperatuer Range (Whole or Tenths of Degrees)'),
        ('mmt', 'Max Min Temperature(Whole or Tenths of Degrees)'),
        ('hdd', 'Heating Degree Days(Whole or Tenths of Degrees)'),
        ('cdd', 'Cooling Degree Days(Whole or Tenths of Degrees)'),
        ('evap', 'Evaporation (Hundredths of Inches)'),
        ('wesf', 'Water Estimate Snow on Ground: (Tenth of Inches)'),
        ('wdmv', 'Wind Movement: (Miles Per Day)'),
        )

SM_TEMP_PRECISION_CHOICES = (
        ('T', 'Tenths of degrees'),
        ('W', 'Whole degrees'),
        (' ', 'Not applicable' ),
)

TMP_UNIT_CHOICE = (
        ('F', 'Fahrenheit'),
        ('C', 'Celsius'),
        (' ', 'Not applicable'),
        )
DIGIT_CHOICES = (
        ('3', 'Values take three spaces'),
        ('4', 'Values take four spaces'),
        ('5', 'Values take five spaces'),
        )
#Sodsum choices
SS_STATION_CHOICE = (
        ('coop_station_id', 'Indidual Coop Station'),
        ('list', 'Comma separated list of stations'),
        ('climdiv', 'By Climate Division'),
        )

SS_ELEMENT_CHOICES = (
        ('pcpn', 'Precipitation'),
        ('snow', 'Snowfall'),
        ('snwd', 'Snowdepth'),
        ('maxt', 'Maximum Temprature'),
        ('mint', 'Minimum Temperature'),
        #('evap', 'Evaporation'),
        #('wdmv', 'Wind Movement'),
        ('wesf', 'Water Estimate Snow Fall'),
        ('multi', '[pcpn, snow, snwd, maxt, mint]'),
        )
#soddyrec choices
SDR_ELEMENT_CHOICES = (
        ('all', '[maxt, mint, pcpn, snow, snwd, hdd, cdd]'),
        ('tmp', '[maxt, mint, pcpn]'),
        ('wtr', '[pcpn, snow, snwd]'),
        ('pcpn', 'Precipitation'),
        ('snow', 'Snowfall'),
        ('snwd', 'Snowdepth'),
        ('maxt', 'Maximum Temprature'),
        ('mint', 'Minimum Temperature'),
        ('hdd', 'Heating Degree Days'),
        ('cdd', 'Cooling Degree Days'),
        )

#Stnfind choices
STN_FIND_CHOICES = (
        ('stnid', 'Individual station'),
        ('stnids', 'Comma separated list of stations '),
        ('county', 'County FIPS code'),
        ('climdiv', 'Climate Division'),
        ('cwa', 'County Warning Area (CWA)'),
        ('basin', 'Basin'),
        ('state', 'State'),
        ('bbox', 'Bounding Box'),
        )
#sodsumm element choices
SMM_ELEMENT_CHOICES = (
        ('all', '[maxt, mint, avgt, pcpn, snow,hdd, cdd, gdd]'),
        ('tmp', '[maxt, mint]'),
        ('ps', '[pcpn, snow]'),
        ('tps', '[maxt, mint, pcpn, snow]'),
        ('hc', '[hdd, cdd]'),
        ('gdd', '[gdd]'),
    )

#sodxtrmts choices
#Note: element choices are the same as for sodmonline(my)
SX_ANALYSIS_CHOICES = (
        ('mmax', 'Monthly Maximum'),
        ('mmin', 'Monthly Minimum'),
        ('mave', 'Monthly Average'),
        ('sd', 'Standard Deviation'),
        ('ndays', 'Number of Days'),
        ('rmon', 'Range during Month'),
        ('msum', 'Monthly Sum'),
    )

SPCT_ELEMENT_CHOICES = (
        ('pcpn', 'Precipitation'),
        ('snow', 'Snowfall'),
        ('snwd', 'Snowdepth'),
        ('maxt', 'Maximum Temprature '),
        ('mint', 'Minimum Temperature'),
        ('avgt', 'Mean Temperature'),
        ('dtr', 'Daily Temperatuer Range'),
    ('hdd', 'Heating Degree Days'),
    ('cdd', 'Cooling Degree Days'),
    ('gdd', 'Growing degree days'),
    )
PII_ELEMENT_CHOICES = (
        ('pcpn', 'Precipitation'),
        ('snow', 'Snowfall'),
        ('snwd', 'Snowdepth'),
        ('maxt', 'Maximum Temprature '),
        ('mint', 'Minimum Temperature'),
        ('avgt', 'Mean Temperature'),
        )

SRR_ELEMENT_CHOICES = (
        ('pcpn', 'Precipitation'),
        ('snow', 'Snowfall'),
        ('snwd', 'Snowdepth'),
        ('maxt', 'Maximum Temprature '),
        ('mint', 'Minimum Temperature'),
        ('dtr', 'Daily Temperature Range'),
        )

#Custom form fields
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
            if len(str(stn))!=6:
                raise forms.ValidationError("coop_station_ids should be a comma separated list of valid 6 digit coop_station_ids %s!" % str(stn))


class SodrunForm(forms.Form):
    coop_station_id = forms.CharField(max_length=6, min_length=6, initial='266779')
    start_date = forms.CharField(max_length=8, min_length=8, required = False, initial='20120101')
    end_date = forms.CharField(max_length=8, min_length=8, required = False, initial=today)
    element = forms.ChoiceField(choices=SR_ELEMENT_CHOICES, initial='pcpn')
    aeb = forms.ChoiceField(choices=AEB_CHOICES, initial ='A' )
    threshold = forms.IntegerField(initial=0)
    min_run = forms.IntegerField(required=False, initial=1)
    name = forms.CharField(max_length=256, required=False)
    #output_file = forms.CharField(max_length=256, required=False)
    verbose = forms.BooleanField(required=False, initial=False)

class SodlistForm(forms.Form):
    coop_station_id = forms.CharField(max_length=6, min_length=6, initial='266779')
    start_date = forms.CharField(max_length=8, min_length=8, required = False, initial='20120101')
    end_date = forms.CharField(max_length=8, min_length=8, required = False, initial=today)
    output_format = forms.ChoiceField(choices=SL_FRMT_CHOICES, initial='kr')
    #output_file = forms.CharField(max_length=256, required=False)
    start_window = forms.CharField(max_length=4, min_length=4, required = False, initial='0101')
    end_window = forms.CharField(max_length=4, min_length=4, required = False, initial='1231')
    minimize = forms.BooleanField(required=False, initial = False)
    include_tobs_evap = forms.BooleanField(required=False, initial = False)

class SodcnvForm(forms.Form):
    coop_station_id = forms.CharField(max_length=6, min_length=6, initial='266779')
    start_date = forms.CharField(max_length=8, min_length=8, required = False, initial='20120101')
    end_date = forms.CharField(max_length=8, min_length=8, required = False, initial=today)
    #output_file = forms.CharField(max_length=256, required=False)
    start_window = forms.CharField(max_length=4, min_length=4, required = False, initial='0101')
    end_window = forms.CharField(max_length=4, min_length=4, required = False, initial='1231')

class SodmonlineForm(forms.Form):
    coop_station_id = forms.CharField(max_length=6, min_length=6, initial='266779')
    start_date = forms.CharField(max_length=4, initial='2012')
    end_date = forms.CharField(max_length=4, initial='2012')
    element = forms.ChoiceField(choices=SM_ELEMENT_CHOICES, initial='pcpn')
    temperature_precision = forms.ChoiceField(choices=SM_TEMP_PRECISION_CHOICES, initial=' ')
    output_format = forms.ChoiceField(choices=SM_FRMT_CHOICES, initial='kr')
    #output_file = forms.CharField(max_length=256, required=False)
    temp_unit = forms.ChoiceField(choices=TMP_UNIT_CHOICE, initial=' ')
    number_of_characters = forms.ChoiceField(choices=DIGIT_CHOICES, initial='3')

class SodmonlinemyForm(forms.Form):
    coop_station_id = forms.CharField(max_length=6, min_length=6, initial='266779')
    start_date = forms.CharField(max_length=4, min_length=4, initial='2012')
    end_date = forms.CharField(max_length=4, min_length=4, initial='2012')
    element = forms.ChoiceField(choices=SM_ELEMENT_CHOICES, initial='pcpn')
    temperature_precision = forms.ChoiceField(choices=SM_TEMP_PRECISION_CHOICES, initial=' ')
    output_format = forms.ChoiceField(choices=SM_FRMT_CHOICES, initial='kr')
    #output_file = forms.CharField(max_length=256, required=False)
    temp_unit = forms.ChoiceField(choices=TMP_UNIT_CHOICE, initial=' ')
    number_of_characters = forms.ChoiceField(choices=DIGIT_CHOICES, initial='4')

class SodsumForm(forms.Form):
    #coop_station_ids = forms.CharField(initial='266779')
    coop_station_ids = MultiStnField(initial='266779,103732')
    start_date = forms.CharField(max_length=8, required = False, initial='20120101')
    end_date = forms.CharField(max_length=8, required = False, initial=today)
    element = forms.ChoiceField(choices=SS_ELEMENT_CHOICES, initial='multi')

#class to determine method of station selection used insubsequent forms
class Soddyrec0Form(forms.Form):
    station_selection = forms.ChoiceField(choices=STN_FIND_CHOICES, required=False, initial='stnid')

class SoddyrecForm(forms.Form):
    def __init__(self, *args, **kwargs):
        station_selection = kwargs.get('initial', {}).get('station_selection', None)
        super(SoddyrecForm, self).__init__(*args, **kwargs)
        self.fields['station_selection'] = forms.ChoiceField(choices=STN_FIND_CHOICES, required=False, initial='stnid')
        if station_selection is None:
            station_selection = self.data.get('station_selection')
        if station_selection == 'stnid':
            self.fields['coop_station_id'] = forms.CharField(max_length=6, min_length=6, initial='266779')
        elif station_selection == 'stnids':
            self.fields['coop_station_ids'] = MultiStnField(required=False,initial='266779,103732')
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
            self.fields['bounding_box'] = forms.CharField(required=False,initial='-90,40,-88,41')
        self.fields['start_date'] = forms.CharField(max_length=8, initial='20100101')
        self.fields['end_date'] = forms.CharField(max_length=8, initial=today)
        self.fields['eighty_column_screen'] = forms.BooleanField(required=False)
        self.fields['element'] = forms.ChoiceField(choices=SDR_ELEMENT_CHOICES, initial='all')

class Soddynorm0Form(forms.Form):
    station_selection = forms.ChoiceField(choices=STN_FIND_CHOICES, required=False, initial='stnid')
    filter_required = forms.BooleanField(initial=False)

class SoddynormForm(forms.Form):
    #station_selection comes from StnfindForm, filter_required from FilterForm
    def __init__(self, *args, **kwargs):
        station_selection = kwargs.get('initial', {}).get('station_selection', None)
        filter_required = kwargs.get('initial', {}).get('filter_required', None)
        super(SoddyrecForm, self).__init__(*args, **kwargs)
        self.fields['station_selection'] = forms.ChoiceField(choices=STN_FIND_CHOICES, required=False, initial='stnid')
        if station_selection is None:
            station_selection = self.data.get('station_selection')
        if station_selection == 'stnid':
            self.fields['coop_station_id'] = forms.CharField(max_length=6, min_length=6, initial='266779')
        elif station_selection == 'stnids':
            self.fields['coop_station_ids'] = MultiStnField(required=False,initial='266779,103732')
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
            self.fields['bounding_box'] = forms.CharField(required=False,initial='-90,40,-88,41')
        self.fields['start_date'] = forms.CharField(max_length=4, min_length=4, initial='2000')
        self.fields['end_date'] = forms.CharField(max_length=4, min_length=4, initial='2012')
        if not filter_required:
            filter_required = self.data.get('filter_required')
        if filter_required:
            self.fields['filter_type'] = forms.ChoiceField(choices=([('gauss','Gaussian'), ('rm','Running Mean'), ]), initial='gauss')

        self.fields['number_of_days'] = forms.CharField(max_length=2, required = False)

class SodsummForm(forms.Form):
    def __init__(self, station_selection, *args, **kwargs):
        '''
        copy from SoddyrecForm once fixed
        '''
        self.fields['start_date'] = forms.CharField(max_length=4, min_length=4, initial='2000')
        self.fields['end_date'] = forms.CharField(max_length=4, min_length=4, initial='2012')
        self.fields['max_number_days_missing'] = forms.CharField(max_length=8, initial = 5)
        self.fields['element'] = forms.ChoiceField(choices=SMM_ELEMENT_CHOICES, initial='all')

class SodxtrmtsForm(forms.Form):
    def __init__(self, station_selection, *args, **kwargs):
        '''
        copy from SoddyrecForm once fixed, possibly more to deal with other input options
        '''
        self.fields['start_date'] = forms.CharField(max_length=4, min_length=4, initial='2000')
        self.fields['end_date'] = forms.CharField(max_length=4, min_length=4, initial='2012')
        self.fields['element'] = forms.ChoiceField(choices=SPCT_ELEMENT_CHOICES, initial='pcpn')
        self.fields['analysis_type'] = forms.ChoiceField(choices=SX_ANALYSIS_CHOICES, initial='mave')

class SodpctForm(forms.Form):
    def __init__(self, station_selection, *args, **kwargs):
        '''
        copy from SoddyrecForm once fixed, possibly more to deal with other input options
        '''
        self.fields['start_date'] = forms.CharField(max_length=4, min_length=4, initial='2000')
        self.fields['end_date'] = forms.CharField(max_length=4, min_length=4, initial='2012')
        #Note number_of_days has max of 31, implement!!
        self.fields['number_of_days'] = forms.CharField(max_length=2, required = False)
        self.fields['element'] = forms.ChoiceField(choices=SPCT_ELEMENT_CHOICES, initial='pcpn')

class SodpadForm(forms.Form):
    def __init__(self, station_selection, *args, **kwargs):
        '''
        copy from SoddyrecForm once fixed, possibly more to deal with other input options
        '''
        self.fields['start_date'] = forms.CharField(max_length=4, min_length=4, initial='2000')
        self.fields['end_date'] = forms.CharField(max_length=4, min_length=4, initial='2012')

class SodthrForm(forms.Form):
    def __init__(self, station_selection, *args, **kwargs):
        '''
        copy from SoddyrecForm once fixed, possibly more to deal with other input options
        '''
        self.fields['start_date'] = forms.CharField(max_length=4, min_length=4, initial='2000')
        self.fields['end_date'] = forms.CharField(max_length=4, min_length=4, initial='2012')
        #self.fields['table_type'] = forms.ChoiceField(choices=([('std','Standard'), ('ctm','Custom'), ]), initial='std')
class SodddForm(forms.Form):
    def __init__(self, station_selection, *args, **kwargs):
        '''
        copy from SoddyrecForm once fixed, possibly more to deal with other input options
        '''
        self.fields['start_date'] = forms.CharField(max_length=4, min_length=4, initial='2000')
        self.fields['end_date'] = forms.CharField(max_length=4, min_length=4, initial='2012')
        self.fields['base_temperature'] = forms.CharField(max_length=4, initial='60')
        self.fields['above_or_below'] = forms.CharField(max_length=1, min_length=1, initial='a')
        self.fields['skip_days'] = forms.BooleanField(required=False, initial=False)
        self.fields['table_type'] = forms.ChoiceField(choices=([('dly','Daily Averages'), ('mly','Monthly Time Series'), ]), initial='dly')

class SodpiipreForm(forms.Form):
    skew = forms.ChoiceField(choices=([('as','Areal Skew'), ('ss','Station Skew'), ]), initial='ss')
    cv = forms.ChoiceField(choices=([('acv','Areal CV'), ('scv','Station CV'), ]), initial='scv')
    mean = forms.ChoiceField(choices=([('am','Areal Mean'), ('scv','Station Mean'), ]), initial='sm')
    pct_average = forms.ChoiceField(choices=([('apct','Areal PCT Average'), ('spct','Station PCT Average'), ]), initial='spct')


class SodpiiForm(forms.Form):
    def __init__(self, station_selection, skew, cv, mean, pct_average, *args, **kwargs):
        '''
        copy from SoddyrecForm once fixed, possibly more to deal with other input options
        NOTE: MESSY INPUT OPTTIONS NEED FIXING UP
        '''
        self.fields['start_date'] = forms.CharField(max_length=6, min_length=6, initial='2000')
        self.fields['end_date'] = forms.CharField(max_length=6, min_length=6, initial='2012')
        self.fields['element'] = forms.ChoiceField(choices=PII_ELEMENT_CHOICES, initial='pcpn')

class SodrunrForm(forms.Form):
    def __init__(self, station_selection, *args, **kwargs):
        '''
        copy from SoddyrecForm once fixed, possibly more to deal with other input options
        '''
        self.fields['start_date'] = forms.CharField(max_length=8, min_length=8, required = False, initial='20120101')
        self.fields['end_date'] = forms.CharField(max_length=8, min_length=8, required = False, initial=today)
        self.fields['element'] = forms.ChoiceField(choices=SRR_ELEMENT_CHOICES, initial='pcpn')
        self.fields['aeb'] = forms.ChoiceField(choices=AEB_CHOICES, initial ='A' )
        self.fields['threshold'] = forms.IntegerField(initial=0)
        self.fields['min_run'] = forms.IntegerField(required=False, initial=1)
