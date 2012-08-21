#!/usr/bin/python
#Python imports
import subprocess
import sys
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

def sodlist(request, app_name):
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

def sodsum(request, app_name):
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
        #(data, dates, elements, coop_station_id, station_name) = AcisWS.get_sodsum_data_multi(form.cleaned_data)
        (data, elements, coop_station_id, station_name) = AcisWS.get_sodsum_data(form.cleaned_data)
        #results = WRCCDataApps.SodsumMulti(data, dates, elements, coop_station_id, station_name)
        results = WRCCDataApps.Sodsum(data, elements, coop_station_id, station_name)
        context['elements'] = elements
    context['form'] = form
    context['results']= dict(results)
    return render_to_response('my_apps/Sodsum.html', context, context_instance=RequestContext(request))

def sods(request, app_name):
    context = {
    'title': '%s' % app_name,
    }
    form1 = set_as_form(request, 'Sod0', init={'app_name': app_name})
    context['form1'] = form1
    if 'stn_selection' in request.POST:
        if app_name == 'Soddd':
            form1 = set_as_form(request, 'Sod0', init={'app_name': app_name, 'skip_days':False})
        else:
            form1 = set_as_form(request, 'Sod0', init={'app_name': app_name})
        context['form1'] = form1
        if form1.is_valid():
            station_selection = form1.cleaned_data['station_selection']
            if app_name == 'Soddd':
                skip_days = form1.cleaned_data['skip_days']
                truncate = form1.cleaned_data['truncate']
                initial = {'app_name':app_name, 'station_selection':station_selection, 'skip_days':skip_days, 'truncate':truncate }
            else:
                initial = {'app_name':app_name, 'station_selection':station_selection}
            form2 = set_as_form2(init=initial)
            context['form2'] = form2
        else:
            station_selection=None
    if 'app_form' in request.POST:
        form2 = set_as_form(request, 'Sod')
        context['form2'] = form2
        #import pdb; pdb.set_trace()
        if  form2.is_valid():
            skip_days = None
            truncate = None
            context['cleaned'] = form2.cleaned_data
            (data, dates, elements, coop_station_ids, station_names) = AcisWS.get_sod_data(form2.cleaned_data, app_name)
            if app_name == 'Soddynorm':
                results = run_data_app(app_name, data, dates, elements, coop_station_ids, station_names, \
                form2.cleaned_data['filter_type'], form2.cleaned_data['number_of_days'])
            elif app_name == 'Soddyrec':
                results = run_data_app(app_name, data, dates, elements, coop_station_ids, station_names)
            elif app_name == 'Soddd':
                app_arg_list = [app_name, data, dates,elements, coop_station_ids,station_names, form2.cleaned_data['base_temperature'], \
                form2.cleaned_data['above_or_below'],form2.cleaned_data['output_type'], form2.cleaned_data['max_days_to_skip'], \
                form2.cleaned_data['max_missing_days']]
                if skip_days:
                     app_arg_list.append(form2.cleaned_data['skip_days_with_max_above'], \
                     form2.cleaned_data['skip_days_with_min_below'])
                if truncate:
                    app_arg_list.append(form2.cleaned_data['truncation_higher_limit'], \
                    form2.cleaned_data['truncation_lower_limit'])
                #results = run_data_app(','.join(app_arg_list))
                results = []
            else:
                results = {}
            context['results'] =  dict(results)
            context['dates'] = dates
            context['elements'] = dict([(k,v) for k,v in enumerate(elements)])
            context['data'] = dict(data)
            context['coop_station_ids'] = dict([(k,v) for k,v in enumerate(coop_station_ids)])
            context['station_names'] = dict([(k,v) for k,v in enumerate(station_names)])
        else:
            station_selection = None
    return render_to_response('my_apps/%s.html' % app_name, context, context_instance=RequestContext(request))

#Utlities
def set_as_form(request, f_name, init = None):
    form_name = '%sForm' % f_name
    form_class = getattr(forms, form_name)
    if request.POST:
        form = form_class(request.POST)
    else:
        if init is not None:
            form = form_class(initial=init)
        else:
            form = form_class(initial={'app_name': f_name})
    return form

def set_as_form2(init=None):
    form_class = getattr(forms, 'SodForm')
    form = form_class(initial=init)
    return form

def run_data_app(app_name, *args, **kwargs):
    try:
        data_app = getattr(WRCCDataApps, app_name)
        results = data_app(*args, **kwargs)
    except:
        results = {}
    return results
