from django import forms
from django.forms.fields import ChoiceField, MultipleChoiceField
from django.contrib.localflavor.us.models import USStateField

import datetime

#find todays date
tdy = datetime.datetime.today()
yr = str(tdy.year)
mon = str(tdy.month)
day = str(tdy.day)
if len(mon) == 1:
	mon = '0%s' % mon
if len(day) == 1:
	day = '0%' % day
today = '%s%s%s' % (yr, mon, day)

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
SODSUM_STATION_CHOICE = (
	('coop_station_id', 'Indidual Coop Station'),
	('list', 'Comma separated list of stations'),
	('state', 'By US state'),
	)

SS_ELEMENT_CHOICES = (
	('pcpn', 'Precipitation'),
	('snow', 'Snowfall'),
	('snwd', 'Snowdepth'),
	('maxt', 'Maximum Temprature'),
	('mint', 'Minimum Temperature'),
        ('evap', 'Evaporation'),
        ('wdmv', 'Wind Movement'),
	('wesf', 'Water Estimate Snow Fall'),
	('multi', '[pcpn, snow, snwd, maxt, mint, evap, wdmv, wesf]'),
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
        coop_station_id = forms.CharField(max_length=6, min_length=8, initial='266779')
        start_date = forms.CharField(max_length=8, min_length=8, required = False, initial='20120101')
        end_date = forms.CharField(max_length=8, min_length=8, required = False, initial=today)
	#output_file = forms.CharField(max_length=256, required=False)
	start_window = forms.CharField(max_length=4, min_length=4, required = False, initial='0101')
	end_window = forms.CharField(max_length=4, min_length=4, required = False, initial='1231')

class SodmonlineForm(forms.Form):
	coop_station_id = forms.CharField(max_length=6, min_length=6, initial='266779')
	start_date = forms.CharField(max_length=4, required = False, initial='2012')
	end_date = forms.CharField(max_length=4, required = False, initial='2012')
	element = forms.ChoiceField(choices=SM_ELEMENT_CHOICES, initial='pcpn')
	temperature_precision = forms.ChoiceField(choices=SM_TEMP_PRECISION_CHOICES, initial=' ')
	output_format = forms.ChoiceField(choices=SM_FRMT_CHOICES, initial='kr')
	#output_file = forms.CharField(max_length=256, required=False)
	temp_unit = forms.ChoiceField(choices=TMP_UNIT_CHOICE, initial=' ')
	number_of_characters = forms.ChoiceField(choices=DIGIT_CHOICES, initial='3')

class SodmonlinemyForm(forms.Form):
	coop_station_id = forms.CharField(max_length=6, min_length=6, initial='266779')
	start_date = forms.CharField(max_length=4, min_length=4, required = False, initial='2012')
	end_date = forms.CharField(max_length=4, min_length=4, required = False, initial='2012')
	element = forms.ChoiceField(choices=SM_ELEMENT_CHOICES, initial='pcpn')
	temperature_precision = forms.ChoiceField(choices=SM_TEMP_PRECISION_CHOICES, initial=' ')
	output_format = forms.ChoiceField(choices=SM_FRMT_CHOICES, initial='kr')
	#output_file = forms.CharField(max_length=256, required=False)
	temp_unit = forms.ChoiceField(choices=TMP_UNIT_CHOICE, initial=' ')
	number_of_characters = forms.ChoiceField(choices=DIGIT_CHOICES, initial='4')

class SodsumForm(forms.Form):
	#coop_station_ids = forms.CharField(initial='266779')
	coop_station_ids = MultiStnField(initial='266779,103732')
	start_date = forms.CharField(max_length=8, min_length=8, required = False, initial='20120101')
	end_date = forms.CharField(max_length=8, min_length=8, required = False, initial=today)
	element = forms.ChoiceField(choices=SS_ELEMENT_CHOICES, initial='multi')
	'''
	stations = forms.ChoiceField(choices=SODSUM_STATION_CHOICES, initial='Coop_station_id')
	start_date = forms.CharField(max_length=4, required = False, initial='por')
	end_date = forms.CharField(max_length=4, required = False, initial=today)

	def __init__(self, stations, *args, **kwargs):
		super(SodsumForm, self).__init__(*args, **kwargs)
		is stations == 'coop_statio_id':
			coop_station_id = forms.CharField(max_length=8, initial='266779')
		elif stations == 'list':
			stns = forms.CharField(initial = '266779, 303184')
		elif stations = 'state':
			state = USStateField()
	'''

class Survey(forms.Form):
    name = forms.CharField(max_length=20)
    age = forms.IntegerField()

    def __init__(self, questions, *args, **kwargs):
        super(Survey, self).__init__(*args, **kwargs)
        # now we add each question individually
        for i, question in enumerate(questions):
             self.fields['question_%d' % i] = forms.ChoiceField(label=question)
