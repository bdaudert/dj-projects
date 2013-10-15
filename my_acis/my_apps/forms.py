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

#APPLICATION_CHOICES
APP_NAME_CHOICES = (
        ('Soddyrec', 'Soddyrec'),
        ('Soddynorm', 'Soddynorm'),
        ('Sodsumm', 'Sodsumm'),
        ('Sodxtrmts', 'Sodxtrmts'),
        ('Sodpct', 'Sodpct'),
        ('Sodpad', 'Sodpad'),
        ('Sodthr', 'Sodthr'),
        ('Soddd', 'Soddd'),
        ('Sodpiii', 'Sodpiii'),
        ('Sodrunr', 'Sodrunr'),
        ('Sodrun', 'Sodrun'),
        )

#SODRUN CHOICES
SR_ELEMENT_CHOICES = (
        ('maxt', 'Maximum Temperature (Whole Degrees)'),
        ('mint', 'Minimum Temperature(Whole Degrees)'),
        ('range', 'Temperature Range(Whole Degrees)'),
        ('snow', 'Snowfall (Tenth of inches)'),
        ('snwd', 'Snowdepth (Whole inches)'),
        ('pcpn', 'Precipitation (Hundredths of inches)'),
        )
SRR_ELEMENT_CHOICES = (
        ('maxt', 'Maximum Temperature (Whole Degrees)'),
        ('mint', 'Minimum Temperature(Whole Degrees)'),
        ('range', 'Temperature Range(Whole Degrees)'),
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
        #('json', 'JSON Format'),
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
        ('maxt', 'Maximum Temperature (Whole or Tenths of Degrees)'),
        ('mint', 'Minimum Temperature(Whole or Tenths of Degrees)'),
        ('avgt', 'Mean Temperature(Whole or Tenths of Degrees)'),
        ('dtr', 'Daily Temperatuer Range (Whole or Tenths of Degrees)'),
        ('mmt', 'Max Min Temperature(Whole or Tenths of Degrees)'),
        ('hdd', 'Heating Degree Days(Whole or Tenths of Degrees)'),
        ('cdd', 'Cooling Degree Days(Whole or Tenths of Degrees)'),
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
        ('maxt', 'Maximum Temperature'),
        ('mint', 'Minimum Temperature'),
        #('evap', 'Evaporation'),
        #('wdmv', 'Wind Movement'),
        #('wesf', 'Water Estimate Snow Fall'),
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
        ('maxt', 'Maximum Temperature'),
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

SXTR_ELEMENT_CHOICES = (
        ('pcpn', 'Daily Precipitation'),
        ('snow', 'Daily Snowfall'),
        ('snwd', 'Daily Snowdepth'),
        ('maxt', 'Daily Maximum Temperature '),
        ('mint', 'Daily Minimum Temperature'),
        ('avgt', 'Daily Mean Temperature'),
        ('dtr', 'Daily Temperature Range'),
        ('hdd', 'Heating Degree Days'),
        ('cdd', 'Cooling Degree Days'),
        ('gdd', 'Growing degree days'),
    )

PIII_ELEMENT_CHOICES = (
        ('pcpn', 'Precipitation'),
        ('snow', 'Snowfall'),
        ('snwd', 'Snowdepth'),
        ('maxt', 'Maximum Temperature '),
        ('mint', 'Minimum Temperature'),
        ('avgt', 'Mean Temperature'),
        )

PIII_DAY_CHOICES = (
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (4, 'Four'),
        (5, 'Five'),
        (6, 'Six'),
        (7, 'Seven'),
        (8, 'Eight'),
        (9, 'Nine'),
        (10, 'Ten'),
        (15, 'Fifteen'),
        (20, 'Twenty'),
        (25, 'Twenty five'),
        (30, 'Thirty'),
)

SDMM_ELEMENT_CHOICES = (
        ('temp', 'Temperature Statistics'),
        ('prsn', 'Precipitation and Snowfall Statistics'),
        ('both', 'Both Temperature and Precipitation Statistics'),
        ('hc', ' Heating and Cooling Degree Day Summaries '),
        ('g', 'Growing Degree Day Summaries'),
        ('all', 'All Statistics'),
        )
SDTHR_ELEMENT_CHOICES = (
        ('maxt', 'Maximum Temperature '),
        ('mint', 'Minimum Temperature'),
        ('avgt', 'Mean Temperature'),
        ('dtr', 'Daily Temperature Range'),
        )

F_ANALYSIS_CHOICES = (
        ('p', 'Pearson Type III'),
        ('g', 'Generalized Extreme Value'),
        #('b', 'Beta-P'),
        #('c', 'Censored Gamma'),
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
            if len(str(stn))!=6:
                raise forms.ValidationError("coop_station_ids should be a comma separated list of valid 6 digit coop_station_ids %s!" % str(stn))


class SodrunForm(forms.Form):
    coop_station_id = forms.CharField(max_length=6, min_length=6, initial='266779')
    start_date = MyDateField(max_length=8, min_length=8, required = False, initial='20120101', help_text="yyyymmdd")
    end_date = MyDateField(max_length=8, min_length=8, required = False, initial=today, help_text="yyyymmdd")
    element = forms.ChoiceField(choices=SR_ELEMENT_CHOICES, initial='pcpn')
    aeb = forms.ChoiceField(choices=AEB_CHOICES, initial ='A' )
    threshold = forms.IntegerField(initial=0)
    min_run = forms.IntegerField(required=False, initial=1)
    name = forms.CharField(max_length=256, required=False)
    #output_file = forms.CharField(max_length=256, required=False)
    verbose = forms.BooleanField(required=False, initial=False)

class SodlistForm(forms.Form):
    coop_station_id = forms.CharField(max_length=6, min_length=6, initial='266779')
    start_date = MyDateField(max_length=8, min_length=8, required = False, initial='20120101', help_text="yyyymmdd")
    end_date = MyDateField(max_length=8, min_length=8, required = False, initial=today, help_text="yyyymmdd")
    output_format = forms.ChoiceField(choices=SL_FRMT_CHOICES, initial='kr')
    #output_file = forms.CharField(max_length=256, required=False)
    start_window = forms.CharField(max_length=4, min_length=4, required = False, initial='0101')
    end_window = forms.CharField(max_length=4, min_length=4, required = False, initial='1231')
    minimize = forms.BooleanField(required=False, initial = False)
    include_tobs_evap = forms.BooleanField(required=False, initial = False)

class SodcnvForm(forms.Form):
    coop_station_id = forms.CharField(max_length=6, min_length=6, initial='266779')
    start_date = MyDateField(max_length=8, min_length=8, required = False, initial='20120101', help_text="yyyymmdd")
    end_date = MyDateField(max_length=8, min_length=8, required = False, initial=today, help_text="yyyymmdd")
    #output_file = forms.CharField(max_length=256, required=False)
    start_window = forms.CharField(max_length=4, min_length=4, required = False, initial='0101')
    end_window = forms.CharField(max_length=4, min_length=4, required = False, initial='1231')

class SodmonlineForm(forms.Form):
    coop_station_id = forms.CharField(max_length=6, min_length=6, initial='266779')
    start_date = MyDateField(max_length=4, initial='2012', help_text="yyyy")
    end_date = forms.CharField(max_length=4, initial='2012', help_text="yyyy")
    element = forms.ChoiceField(choices=SM_ELEMENT_CHOICES, initial='pcpn')
    temperature_precision = forms.ChoiceField(choices=SM_TEMP_PRECISION_CHOICES, initial=' ')
    output_format = forms.ChoiceField(choices=SM_FRMT_CHOICES, initial='kr')
    #output_file = forms.CharField(max_length=256, required=False)
    temp_unit = forms.ChoiceField(choices=TMP_UNIT_CHOICE, initial=' ')
    number_of_characters = forms.ChoiceField(choices=DIGIT_CHOICES, initial='3')

class SodmonlinemyForm(forms.Form):
    coop_station_id = forms.CharField(max_length=6, min_length=6, initial='266779')
    start_date = MyDateField(max_length=4, min_length=4, initial='2012', help_text="yyyymmdd")
    end_date = MyDateField(max_length=4, min_length=4, initial='2012', help_text="yyyymmdd")
    element = forms.ChoiceField(choices=SM_ELEMENT_CHOICES, initial='pcpn')
    temperature_precision = forms.ChoiceField(choices=SM_TEMP_PRECISION_CHOICES, initial=' ')
    output_format = forms.ChoiceField(choices=SM_FRMT_CHOICES, initial='kr')
    #output_file = forms.CharField(max_length=256, required=False)
    temp_unit = forms.ChoiceField(choices=TMP_UNIT_CHOICE, initial=' ')
    number_of_characters = forms.ChoiceField(choices=DIGIT_CHOICES, initial='4')

class SodsumForm(forms.Form):
    #coop_station_ids = forms.CharField(initial='266779')
    coop_station_ids = MultiStnField(initial='266779,103732')
    start_date = MyDateField(max_length=8, required = False, initial='20120101', help_text="yyyymmdd")
    end_date = MyDateField(max_length=8, required = False, initial=today, help_text="yyyymmdd")
    element = forms.ChoiceField(choices=SS_ELEMENT_CHOICES, initial='multi')

#class to determine method of station selection used insubsequent forms
class Sod0Form(forms.Form):
    def __init__(self, *args, **kwargs):
        app_name = kwargs.get('initial', {}).get('app_name', None)
        super(Sod0Form, self).__init__(*args, **kwargs)

        self.fields['station_selection'] = forms.ChoiceField(choices=STN_FIND_CHOICES, required=False, initial='stnid')
        self.fields['app_name'] = forms.ChoiceField(choices=APP_NAME_CHOICES, required=False, initial='Soddd', widget=forms.HiddenInput())
        if app_name is None:
            app_name = self.data.get('app_name')
        if app_name == 'Soddd':
            self.fields['skip_days'] = forms.BooleanField(initial=False, required=False)
            self.fields['truncate'] = forms.BooleanField(initial=False, required=False)
        if app_name == 'Sodpct':
            self.fields['element'] = forms.ChoiceField(choices=SXTR_ELEMENT_CHOICES, initial='pcpn')
            self.fields['individual_averages'] = forms.ChoiceField(choices=([('I','Individual'), ('A','Day Sums or Averages'),]), required=False, initial='I')
            self.fields['threshold'] = forms.DecimalField(required=False, initial=-9999.0)
        if app_name == 'Sodthr':
            #self.fields['custom_tables'] = forms.BooleanField(initial=False, required=False)
            self.fields['custom_tables'] = forms.ChoiceField(choices = ([('T', 'True'),('F', 'False'),]), initial = 'F')
            self.fields['number_of_thresholds']= forms.IntegerField(min_value=1,max_value=10, initial=1)
        if app_name == 'Sodxtrmts':
            self.fields['monthly_statistic'] = forms.ChoiceField(choices=SX_ANALYSIS_CHOICES, initial='mave')
            self.fields['element'] = forms.ChoiceField(choices=SXTR_ELEMENT_CHOICES, initial='maxt')
            self.fields['frequency_analysis'] = forms.ChoiceField(choices = ([('T', 'True'),('F', 'False'),]), initial = 'F')
        if app_name == 'Sodpiii':
            self.fields['skew'] = forms.ChoiceField(choices=([('as','Areal Skew'), ('ss','Station Skew'), ]), initial='ss')
            self.fields['cv'] = forms.ChoiceField(choices=([('acv','Areal CV'), ('scv','Station CV'), ]), initial='scv')
            self.fields['mean'] = forms.ChoiceField(choices=([('am','Areal Mean'), ('sm','Station Mean'), ]), initial='sm')
            self.fields['pct_average'] = forms.ChoiceField(choices=([('apct','Areal PCT Average'), ('spct','Station PCT Average'), ]), initial='spct')
            self.fields['days'] = forms.ChoiceField(choices=([('i','Individual Day'), ('5','Day 1-5'), ('a','All Days'), ]), initial='i')
class SodForm(forms.Form):
    def __init__(self, *args, **kwargs):
        station_selection = kwargs.get('initial', {}).get('station_selection', None)
        app_name = kwargs.get('initial', {}).get('app_name', None)
        super(SodForm, self).__init__(*args, **kwargs)

        self.fields['station_selection'] = forms.ChoiceField(choices=STN_FIND_CHOICES, required=False, initial='stnid', widget=forms.HiddenInput())
        self.fields['app_name'] = forms.ChoiceField(choices=APP_NAME_CHOICES, required=False, initial='Soddyrec', widget=forms.HiddenInput())

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

        if app_name is None:
            app_name = self.data.get('app_name')

        if app_name in ['Soddyrec', 'Sodcnv', 'Sodlist', 'Sodrun', 'Sodrunr']:
            self.fields['start_date'] = MyDateField(max_length=8, initial='20000101', help_text="yyyymmdd")
            self.fields['end_date'] = MyDateField(max_length=8, initial=20091231, help_text="yyyymmdd")
            #self.fields['end_date'] = forms.CharField(max_length=8, initial='20091231')
        elif app_name in ['Soddynorm', 'Soddd', 'Sodmonline', 'Sodmonlinemy', 'Sodpad', 'Sodsumm', 'Sodpct', 'Sodthr', 'Sodxtrmts']:
            self.fields['start_date'] = MyDateField(max_length=4, min_length=4, initial='2000', help_text="yyyy")
            self.fields['end_date'] = MyDateField(max_length=4, min_length=4, initial='2010', help_text="yyyy")
        elif app_name == 'Sodpiii':
            self.fields['start_date'] = MyDateField(max_length=6, min_length=6, initial='200001', help_text="yyyymm")
            self.fields['end_date'] = MyDateField(max_length=6, min_length=6, initial='200912', help_text="yyyymm")

        if app_name in ['Sodrun', 'Sodrunr']:
            if app_name == 'Sodrunr':
                self.fields['element'] = forms.ChoiceField(choices=SRR_ELEMENT_CHOICES, initial='range')
                self.fields['aeb'] = forms.ChoiceField(choices=AEB_CHOICES, initial ='A' )
                self.fields['threshold'] = forms.IntegerField(initial=40)
            else:
                self.fields['element'] = forms.ChoiceField(choices=SR_ELEMENT_CHOICES, initial='pcpn')
                self.fields['aeb'] = forms.ChoiceField(choices=AEB_CHOICES, initial ='A' )
                self.fields['threshold'] = forms.IntegerField(initial=0)
            self.fields['minimum_run'] = forms.IntegerField(required=False, initial=1)
            self.fields['verbose'] = forms.BooleanField(required=False, initial=False)
        elif app_name == 'Soddyrec':
            self.fields['element'] = forms.ChoiceField(choices=SDR_ELEMENT_CHOICES, initial='all')
        elif app_name == 'Soddynorm':
            self.fields['filter_type'] = forms.ChoiceField(choices=([('gauss','Gaussian'), ('rm','Running Mean'), ]), initial='rm', required = False)
            self.fields['number_of_days'] = forms.ChoiceField(choices=((str(n), n) for n in range(1,32)), initial = '1')
        elif app_name == 'Soddd':
            self.fields['base_temperature'] = forms.IntegerField(initial=65)
            self.fields['above_or_below'] = forms.ChoiceField(choices=([('a','Above'), ('b','Below'), ]), initial='a')
            self.fields['output_type'] = forms.ChoiceField(choices=([('m','Monthly Time Series'), ('d','Daily Long-term Averages'), ]), initial='m')
            self.fields['max_missing_days'] = forms.IntegerField(initial=0, required=False)
            self.fields['ncdc_roundoff'] = forms.BooleanField(initial=False, required=False)

            skip_days = kwargs.get('initial', {}).get('skip_days', False)
            truncate = kwargs.get('initial', {}).get('truncate', False)
            if skip_days:
                self.fields['skip_days_with_max_above'] = forms.IntegerField(initial=110)
                self.fields['skip_days_with_min_below'] = forms.IntegerField(initial=20)
            if truncate:
                self.fields['truncation_upper_limit'] = forms.IntegerField(initial=110)
                self.fields['truncation_lower_limit'] = forms.IntegerField(initial=20)
        elif app_name == 'Sodsumm':
            self.fields['max_missing_days'] = forms.IntegerField(initial=5, required=False)
            self.fields['element'] = forms.ChoiceField(choices=SDMM_ELEMENT_CHOICES, initial='all')
        elif app_name == 'Sodlist':
            self.fields['output_format'] = forms.ChoiceField(choices=SL_FRMT_CHOICES, initial='kr')
            self.fields['start_window'] = forms.CharField(max_length=4, min_length=4, required = False, initial='0101')
            self.fields['end_window'] = forms.CharField(max_length=4, min_length=4, required = False, initial='1231')
            self.fields['minimize'] = forms.BooleanField(required=False, initial = False)
            self.fields['include_tobs_evap'] = forms.BooleanField(required=False, initial = False)
        elif app_name == 'Sodcnv':
            self.fields['start_window'] = forms.CharField(max_length=4, min_length=4, required = False, initial='0101')
            self.fields['end_window'] = forms.CharField(max_length=4, min_length=4, required = False, initial='1231')
        elif app_name in ['Sodmonline', 'Sodmonlinemy']:
            self.fields['element'] = forms.ChoiceField(choices=SM_ELEMENT_CHOICES, initial='pcpn')
            self.fields['temperature_precision'] = forms.ChoiceField(choices=SM_TEMP_PRECISION_CHOICES, initial=' ')
            self.fields['output_format'] = forms.ChoiceField(choices=SM_FRMT_CHOICES, initial='kr')
            self.fields['temp_unit'] = forms.ChoiceField(choices=TMP_UNIT_CHOICE, initial=' ')
            self.fields['number_of_characters'] = forms.ChoiceField(choices=DIGIT_CHOICES, initial='3')
        elif app_name in ['Sodrun', 'Sodrunr']:
            self.fields['element'] = forms.ChoiceField(choices=SR_ELEMENT_CHOICES, initial='pcpn')
            self.fields['aeb'] = forms.ChoiceField(choices=AEB_CHOICES, initial ='A' )
            self.fields['threshold'] = forms.IntegerField(initial=0)
            self.fields['min_run'] = forms.IntegerField(required=False, initial=1)
            self.fields['name'] = forms.CharField(max_length=256, required=False)
            self.fields['verbose'] = forms.BooleanField(required=False, initial=False)
        elif app_name == 'Sodpct':
            threshold = kwargs.get('initial', {}).get('threshold', None)
            element = kwargs.get('initial', {}).get('element', None)
            individual_averages = kwargs.get('initial', {}).get('individual_averages', None)
            if threshold is None:threshold = self.data.get('threshold')
            if element is None:element = self.data.get('element')
            if individual_averages is None:individual_averages = self.data.get('individual_averages')
            self.fields['element'] = forms.CharField(initial=element)
            self.fields['element'].widget.attrs['readonly'] = 'readonly'
            self.fields['individual_averages'] = forms.CharField(initial=individual_averages)
            self.fields['individual_averages'].widget.attrs['readonly'] = 'readonly'
            self.fields['threshold'] = forms.DecimalField(initial=threshold)
            self.fields['threshold'].widget.attrs['readonly'] = 'readonly'
            #self.fields['threshold'] = forms.DecimalField(label=threshold)
            if threshold is not None:
                self.fields['threshold_ab'] = forms.ChoiceField(choices=([('a','Above'), ('b','Below'),]))
            if element in ['hdd', 'cdd', 'gdd']:
                self.fields['base_temperature'] = forms.IntegerField(initial=65)
                if element == 'gdd':
                    self.fields['min_temperature'] = forms.IntegerField(initial=50)
                    self.fields['max_temperature'] = forms.IntegerField(initial=80)
            if individual_averages == 'I':
                self.fields['accumulate_over_season'] = forms.BooleanField(required=False, initial = False)
                self.fields['begin_month'] = forms.IntegerField(min_value=1,max_value=12, initial=1)
            self.fields['number_days_ahead'] = forms.IntegerField(min_value=1,max_value=31, initial=5)
        elif app_name == 'Sodthr':
            number_of_thresholds = kwargs.get('initial', {}).get('number_of_thresholds', None)
            custom_tables = kwargs.get('initial', {}).get('custom_tables',None)

            if number_of_thresholds is None: number_of_thresholds = self.data.get('number_of_thresholds')
            if custom_tables is None:custom_tables = self.data.get('custom_tables')

            self.fields['element'] = forms.ChoiceField(choices=SDTHR_ELEMENT_CHOICES, required=False, initial='mint')
            if custom_tables == 'T':
                self.fields['interval_start'] = forms.CharField(max_length=4, min_length=4, required = False, initial='0101')
                self.fields['interval_end'] = forms.CharField(max_length=4, min_length=4, required = False, initial='1231')
                self.fields['midpoint'] = forms.CharField(max_length=4, min_length=4, initial='0731')
                self.fields['number_of_thresholds'] = forms.IntegerField(initial=number_of_thresholds)
                self.fields['number_of_thresholds'].widget.attrs['readonly'] = 'readonly'
                if number_of_thresholds is not None:
                    for thresh in range(int(number_of_thresholds)):
                        self.fields['threshold_%s' % thresh] = forms.DecimalField(initial = 0.0)
                        self.fields['time_series_%s' % thresh] = forms.BooleanField(required=False, initial = False)
                self.fields['latest_or_earliest_for_period_1'] = forms.ChoiceField(choices=([('e','Earliest'), ('l','Latest'), ]), initial='e')
                self.fields['latest_or_earliest_for_period_2'] = forms.ChoiceField(choices=([('e','Latest'), ('l','Earliest'), ]), initial='l')
                self.fields['above_or_below'] = forms.ChoiceField(choices=([('a','Above'), ('b','Below'), ]), initial='b')
            else:
                self.fields['number_of_thresholds'] = forms.IntegerField(initial=None, widget=forms.HiddenInput())
            self.fields['max_missing_days_first_and_last'] = forms.IntegerField(initial=10, required=False)
            self.fields['max_missing_days_differences'] = forms.IntegerField(initial=10, required=False)
            self.fields['custom_tables'] = forms.ChoiceField(choices = ([('T', 'True'),('F', 'False'),]), initial = custom_tables)
            self.fields['custom_tables'].widget.attrs['readonly'] = 'readonly'
        elif app_name == 'Sodxtrmts':
            monthly_statistic = kwargs.get('initial', {}).get('monthly_statistic', None)
            element = kwargs.get('initial', {}).get('element', None)
            frequency_analysis = kwargs.get('initial', {}).get('frequency_analysis', None)
            if element is None:element = self.data.get('element')
            if monthly_statistic is None:monthly_statistic = self.data.get('monthly_statistic')
            if frequency_analysis is None:frequency_analysis = self.data.get('frequency_analysis')
            self.fields['frequency_analysis'] = forms.CharField(initial=frequency_analysis)
            self.fields['frequency_analysis'].widget.attrs['readonly'] = 'readonly'
            if frequency_analysis == 'T':
                self.fields['frequency_analysis_type'] = forms.ChoiceField(choices=F_ANALYSIS_CHOICES, required=False, initial='p')
            self.fields['element'] = forms.CharField(initial=element)
            self.fields['element'].widget.attrs['readonly'] = 'readonly'
            if element in ['hdd', 'cdd', 'gdd']:
                self.fields['base_temperature'] = forms.IntegerField(initial=65)
            if monthly_statistic == 'ndays':
                self.fields['less_greater_or_between'] = forms.ChoiceField(choices=([('l','Less Than'), ('g','Greater Than'),('b','Between'), ]), initial='b')
                self.fields['threshold_for_less_or_greater'] = forms.DecimalField(initial = 0.0)
                self.fields['threshold_low_for_between'] = forms.DecimalField(initial = 0.0)
                self.fields['threshold_high_for_between'] = forms.DecimalField(initial = 1.0)
            self.fields['element'] = forms.CharField(initial=element)
            self.fields['element'].widget.attrs['readonly'] = 'readonly'
            self.fields['monthly_statistic'] = forms.CharField(initial=monthly_statistic)
            self.fields['monthly_statistic'].widget.attrs['readonly'] = 'readonly'
            self.fields['max_missing_days'] = forms.IntegerField(initial=5, required=False)
            self.fields['start_month'] = forms.CharField(initial='01', required=False)
            self.fields['departures_from_averages'] = forms.ChoiceField(choices = ([('T', 'True'),('F', 'False'),]), initial = 'F')
        elif app_name == 'Sodpiii':
            skew = kwargs.get('initial', {}).get('skew', None)
            cv = kwargs.get('initial', {}).get('cv', None)
            mean = kwargs.get('initial', {}).get('mean', None)
            pct_average = kwargs.get('initial', {}).get('pct_average', None)
            days = kwargs.get('initial', {}).get('days', None)
            if skew is None:skew = self.data.get('skew')
            if cv is None:cv = self.data.get('cv')
            if mean is None:mean = self.data.get('mean')
            if pct_average is None:pct_average = self.data.get('pct_average')
            if days is None:days = self.data.get('days')
            self.fields['skew'] = forms.CharField(initial=skew)
            self.fields['skew'].widget.attrs['readonly'] = 'readonly'
            self.fields['cv'] = forms.CharField(initial=cv)
            self.fields['cv'].widget.attrs['readonly'] = 'readonly'
            self.fields['mean'] = forms.CharField(initial=mean)
            self.fields['mean'].widget.attrs['readonly'] = 'readonly'
            self.fields['pct_average'] = forms.CharField(initial=pct_average)
            self.fields['pct_average'].widget.attrs['readonly'] = 'readonly'
            if skew == 'as' or cv == 'acv' or mean == 'am' or pct_average == 'apct':
                self.fields['element'] = forms.CharField(initial='pcpn')
                self.fields['element'].widget.attrs['readonly'] = 'readonly'
            else:
                self.fields['element'] = forms.ChoiceField(choices=PIII_ELEMENT_CHOICES, initial='maxt')
            if skew == 'ss' or cv == 'scv' or mean == 'sm' or pct_average == 'spct':
                self.fields['mean_temperatures']= forms.ChoiceField(choices = ([('b', 'Below Average'),('a', 'Above Average'), ('n', 'None'),]), initial = 'None')
                self.fields['days'] = forms.CharField(initial=days)
                self.fields['days'].widget.attrs['readonly'] = 'readonly'
                if days == 'i':
                    self.fields['number_of_days'] = forms.ChoiceField(choices=PIII_DAY_CHOICES, initial='20')
            self.fields['value_subsequent'] = forms.IntegerField(required=False, initial=9991)
            self.fields['value_missing'] = forms.IntegerField(required=False, initial=9999)
        else:
            pass

