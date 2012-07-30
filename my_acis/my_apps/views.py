#!/usr/bin/python
#Python imports
import subprocess
import sys
import csv
#django Imports
from django.template import RequestContext
#from django.contrib.auth.models import User
#from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic.list_detail import object_detail, object_list
from django.db.models.query import QuerySet
#My imports
import AcisWS
import WRCCUtils
import WRCCDataApps
import my_apps.forms as forms

#Prefix to location of executables
prefix='/Users/bdaudert/DRI/AcisWS_WRCC_PythonScripts/'

def home_view(request):
	context = {
	'title': 'DATA APPLICATIONS',
	}
	return render_to_response('my_apps/home.html', context, context_instance=RequestContext(request))

def app(request, app_name):
	#app_name = request.GET.get('app_name')
	context = {
	'title': '%s' % app_name,
	}
	if app_name is None:
		raise
	form = set_as_form(request, app_name)
	out =  'No output yet'
	err = 'No error yet'
	ex_list = ['python', 'print \'HALLO\'']
	if form.is_valid():
		context['cleaned'] = form.cleaned_data
		if app_name == 'Sodrun':
			app = 'ws_sodrun.py'
		elif app_name in ['Sodlist', 'Sodmonline', 'Sodmonlinemy', 'Sodcnv']:
			app = 'ws_sodlist.py'
			if app_name == 'Sodlist':
				prog = 'sodlist'
			elif app_name == 'Sodmonline':
				prog = 'sodmonline'
			elif app_name == 'Sodmonlinemy':
				prog = 'sodmonlinemy'
			elif app_name == 'Sodcnv':
				prog = 'sodcnv'
		ex_list = ['python', prefix + app]
		if app_name !='Sodrun':
			ex_list.append('--program')
			ex_list.append(prog)

		for key, val in form.cleaned_data.iteritems():
			#define commandline options(clo).
			#NOTE: this demand the names in the form to be of certain format
			if val is None or val=='':
				pass
			else:
				if key not in ['verbose','minimize','include_tobs_evap']:
					clo_list = key.split('_')
					clo = '--' + '-'.join(l for l in clo_list)
					ex_list.append(clo)
					ex_list.append(str(val))
				else:
					if val:
						clo_list = key.split('_')
						clo = '--' + '-'.join(l for l in clo_list)
						ex_list.append(clo)
	context['list'] = ex_list
	proc = subprocess.Popen(ex_list, stdout=subprocess.PIPE)
	status = proc.returncode
	(stdout, stderr) = proc.communicate()
	context['executable'] = ex_list
	context['status'] = status
	context['app_name'] = app_name
	context['form'] = form
	context['out'] = stdout
	context['err'] = stderr

	return render_to_response('my_apps/application.html', context, context_instance=RequestContext(request))

def app_new(request, app_name):
	context = {
	'title': '%s' % app_name,
	}
	if app_name is None:
		raise
	form = set_as_form(request, app_name)
	out =  'No output yet'
	err = 'No error yet'
	results = {}
	if form.is_valid():
		context['cleaned'] = form.cleaned_data
		(data, dates, elements, coop_station_id, station_name) = AcisWS.get_sodsum_data(form.cleaned_data)
		results = WRCCDataApps.SodSum(data, dates, elements, coop_station_id, station_name)
		context['elements'] = elements
	context['form'] = form
	context['results']= dict(results)
	return render_to_response('my_apps/sodsum.html', context, context_instance=RequestContext(request))


#Utlities
def set_as_form(request, app_name, init = None):
	form_name = '%sForm' % app_name
	form_class = getattr(forms, form_name)
	if request.POST:
		form = form_class(request.POST)
	else:
		if init is not None:
			form = form_class(initial=init)
		else:
			form = form_class(initial={'app_name': app_name})
	return form
