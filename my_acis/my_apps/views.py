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
                initial = {'app_name':app_name, 'station_selection':station_selection, \
                'skip_days':skip_days, 'truncate':truncate }
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
                base_temp = form2.cleaned_data['base_temperature']
                output_type = form2.cleaned_data['output_type']
                max_miss = form2.cleaned_data['max_missing_days']
                a_b = form2.cleaned_data['above_or_below']
                max_miss = form2.cleaned_data['max_missing_days']
                ncdc_round = form2.cleaned_data['ncdc_roundoff']
                app_args = {'app_name':app_name,'data':data,'dates':dates,'elements':elements,\
                'coop_station_ids':coop_station_ids,'station_names':station_names,\
                'base_temp':base_temp, 'a_b':a_b,'output_type':output_type, \
                'max_miss':max_miss, 'ncdc_round':ncdc_round}
                if skip_days:
                     skip_max_above = form2.cleaned_data['skip_days_with_max_above']
                     skip_min_below = form2.cleaned_data['skip_days_with_min_below']
                     app_args['skip_max_above'] = skip_max_above
                     app_args['skip_min_below'] = skip_min_below
                     context['skip_max_above'] = skip_max_above
                     context['skip_min_below'] = skip_min_below
                if truncate:
                    trunc_high = form2.cleaned_data['truncation_higher_limit']
                    trunc_low = form2.cleaned_data['truncation_lower_limit']
                    app_args['trunc_high'] = trunc_high
                    app_args['trunc_low'] = trunc_low
                    context['trunc_high'] = trunc_high
                    context['trunc_low'] = trunc_low
                context['base_temp'] = base_temp
                context['output_type'] = output_type
                context['max_miss'] = max_miss
                if form2.cleaned_data['output_type'] == 'm':
                    context['monthly'] = 'yes'
                else:
                    context['daily'] = 'yes'
                results = run_data_app(**app_args)
            elif app_name == 'Sodpad':
                app_args = {'app_name':app_name,'data':data,'dates':dates,'elements':elements,\
                'coop_station_ids':coop_station_ids,'station_names':station_names}
                results = run_data_app(**app_args)
                mon_dict = {}
                day_dict = {}
                for doy in range(366):
                    mon, day = WRCCUtils.compute_mon_day(doy+1)
                    mon_dict[doy] = mon
                    day_dict[doy] = day
                context['mon'] = mon_dict
                context['day'] = day_dict
                context['durations'] ={ 1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:12,12:14,13:15,14:16,15:18,16:20,17:22,18:24,19:25,20:26,21:28,22:30}
            elif app_name == 'Sodsumm':
                el_type  = form2.cleaned_data['element']
                app_args = {'app_name':app_name,'data':data,'dates':dates,'elements':elements,\
                'coop_station_ids':coop_station_ids,'station_names':station_names, 'el_type':el_type}
                results = run_data_app(**app_args)
                context['max_missing_days'] = form2.cleaned_data['max_missing_days']
                if el_type  == 'temp':
                    table_list = ['temp']
                elif el_type  == 'prsn':
                    table_list = ['prsn']
                elif el_type  == 'both':
                    table_list = ['temp', 'prsn']
                elif el_type == 'hc':
                    table_list = ['hdd', 'cdd']
                elif el_type ==  'g':
                    table_list = ['gdd', 'corn']
                elif el_type == 'all':
                    table_list = ['temp', 'prsn', 'hdd', 'cdd', 'gdd', 'corn']
                context['headers'] = set_sodsumm_headers(table_list)
            else:
                results = {}

            context['results'] =  dict(results)
            context['dates'] = dates
            context['start_year'] = dates[0][0:4]
            context['end_year'] = str(int(dates[-1][0:4])+1)
            context['num_yrs'] = int(dates[-1][0:4]) - int(dates[0][0:4])+1
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

def set_sodsumm_headers(table_list):
    headers = {}
    def set_header(table):
        rows = []
        if table == 'temp':
            rows.append('<th colspan="12"> Temperature Statistics</th><th>#Day</th><th>-Max</th><th>#Day</th><th>-Min</th>')
            rows.append('<tr><td colspan="4">Averages</td><td colspan="4">Daily Extremes</td><td colspan="4">Mean Extremes</td><td> >= </td><td>=< </td><td>=< </td><td>=< </td></tr>')
            rows.append('<tr><td></td><td>Max</td><td>Min</td><td>Mean</td><td>High--</td><td>-Date</td><td>Low--</td><td>Date</td><td>High-</td><td>Yr</td><td>Low-</td><td>Yr</td><td>90</td><td>32</td><td>32</td><td>0</td></tr>')
        elif table == 'prsn':
            rows.append('<th colspan="15">Precipitation/Snow Statistics</th>')
            rows.append('<tr><td colspan="15">Missing data not yet determined</td></tr>')
            rows.append('<tr><td colspan="6">Total Precipitation</td><td colspan="2">Precipitation</td><td colspan="3">Total Snowfall</td><td colspan="4">#Days Precip >=</td></tr>')
            rows.append('<tr><td colspan="2">Mean</td><td colspan="2">High--Yr</td><td colspan="2">Low-Yr</td><td>1-Day</td><td>Max</td><td>Mean</td><td colspan="2">High-Yr</td><td>0.01</td><td>0.10</td><td>0.50</td><td>1.00</td></tr>')

        elif table == 'hdd':
            rows.append('<th colspan="14">For Heating degree day calculations:</th>')
            rows.append('<tr><td colspan="14">Output is rounded, unlike NCDC values, which round input.</td></tr>')
            rows.append('<tr><td colspan="14">Missing data not yet determined</td></tr>')
            rows.append('<tr><td colspan="14">Degree Days to selected Base Temperatures(F)</td></tr>')
            rows.append('<tr><td>Base</td><td colspan="13">Heating Degree Days</td></tr>')
            rows.append('<tr><td>Below</td><td>Jan</td><td>Feb</td><td>Mar</td><td>Apr</td><td>May</td><td>Jun</td><td>Jul</td><td>Aug</td><td>Sep</td><td>Oct</td><td>Nov</td><td>Dec</td><td>Ann</td></tr>')
        elif table == 'cdd':
            rows.append('<th colspan="14">For Cooling degree day calculations:</th>')
            rows.append('<tr><td colspan="14">Output is rounded, unlike NCDC values, which round input.</td></tr>')
            rows.append('<tr><td colspan="14">Missing data not yet determined</td></tr>')
            rows.append('<tr><td colspan="14">Degree Days to selected Base Temperatures(F)</td></tr>')
            rows.append('<tr><td>Base</td><td colspan="13">Cooling Degree Days</td></tr>')
            rows.append('<tr><td>Above</td><td>Jan</td><td>Feb</td><td>Mar</td><td>Apr</td><td>May</td><td>Jun</td><td>Jul</td><td>Aug</td><td>Sep</td><td>Oct</td><td>Nov</td><td>Dec</td><td>Ann</td></tr>')
        elif table == 'gdd':
            rows.append('<th colspan="15">For Growing degree day calculations:</th>')
            rows.append('<tr><td colspan="15">Output is rounded, unlike NCDC values, which round input.</td>')
            rows.append('<tr><td colspan="15">Missing data not yet determined</td></tr>')
            rows.append('<tr><td colspan="15">Growing Degree Days to selected Base Temperatures(F)</td></tr>')
            rows.append('<tr><td colspan="2">Base</td><td>Jan</td><td>Feb</td><td>Mar</td><td>Apr</td><td>May</td><td>Jun</td><td>Jul</td><td>Aug</td><td>Sep</td><td>Oct</td><td>Nov</td><td>Dec</td><td>Ann</td></tr>')
        elif table == 'corn':
            rows.append('<th colspan="15">Corn Growing Degree Days</th>')
            rows.append('<td colspan="2">Base</td><td>Jan</td><td>Feb</td><td>Mar</td><td>Apr</td><td>May</td><td>Jun</td><td>Jul</td><td>Aug</td><td>Sep</td><td>Oct</td><td>Nov</td><td>Dec</td><td>Ann</td></tr>')
        return "\n".join(rows)

    for table in table_list:
         headers[table] = set_header(table)
    return headers
