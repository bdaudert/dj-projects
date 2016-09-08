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
from django.db.models.query import QuerySet
from django.conf import settings
#My imports
import AcisWS
import WRCCUtils, WRCCDataApps, WRCCData, WRCCWrappers, WRCCClasses
import wrcc_apps.forms as forms

#Prefix to location of executables
#prefix='/www/apps/csc/AcisWS_WRCC_PythonScripts/'
prefix = settings.BASE_DIR + 'AcisWS_WRCC_PythonScripts/'

def home_view(request):
    context = {
    'title': 'DATA APPLICATIONS',
    }
    return render_to_response('wrcc_apps/home.html', context, context_instance=RequestContext(request))

def cemp(request):
    context = {
    'title': 'Cemp Test Page'
    }
    return render_to_response('wrcc_apps/cemp.html', context, context_instance=RequestContext(request))


def nevcan(request):
    context = {
        'title': 'nevcan Test Page'
    }
    return render_to_response('wrcc_apps/nevcan.html', context, context_instance=RequestContext(request))

def sodlist(request, app_name):
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

    return render_to_response('wrcc_apps/application.html', context, context_instance=RequestContext(request))

def sodlist_new(request):
    context = {
    'title': 'Sodlist'
    }
    form = set_as_form(request, 'Sodlist')
    context['form'] = form
    if form.is_valid():
        kwargs = {}
        for key, val in form.cleaned_data.iteritems():
            if key == 'station_id':
                kwargs['station_id'] = str(val)
            else:
                kwargs[key] = val
        results = WRCCDataApps.Sodlist_new(kwargs)
        context['results'] = results[0]
        context['params'] = form.cleaned_data
        context['station_name'] = results[0]['meta']['name']
    return render_to_response('wrcc_apps/Sodlist.html', context, context_instance=RequestContext(request))

def sodmonline_new(request):
    context = {
    'title': 'Sodmonline'
    }
    form = set_as_form(request, 'Sodmonline')
    context['form'] = form
    if form.is_valid():
        kwargs = {}
        for key, val in form.cleaned_data.iteritems():
            kwargs[str(key)] = str(val)
        results = WRCCDataApps.Sodmonline_new(kwargs)
        context['results'] = results
        context['params'] = kwargs
        #context['station_name'] = results['meta']['name']
    return render_to_response('wrcc_apps/Sodmonline.html', context, context_instance=RequestContext(request))

def sodmonlinemy_new(request):
    context = {
    'title': 'Sodmonlinemy'
    }
    form = set_as_form(request, 'Sodmonline')
    context['form'] = form
    if form.is_valid():
        kwargs = {}
        for key, val in form.cleaned_data.iteritems():
            kwargs[str(key)] = str(val)
        results = WRCCDataApps.Sodmonlinemy_new(kwargs)
        context['results'] = results
        context['params'] = kwargs
        #context['station_name'] = results['meta']['name']
    return render_to_response('wrcc_apps/Sodmonlinemy.html', context, context_instance=RequestContext(request))

def sodsum(request, app_name):
    context = {
    'title': '%s' % app_name,
    }
    if app_name is None:
        raise
    form =  set_as_form(request, app_name)
    context['form'] = form
    out =  'No output yet'
    err = 'No error yet'
    results = {}
    if form.is_valid():
        context['cleaned'] = form.cleaned_data
        data_params = {
                'sids':form.cleaned_data['station_ids'],
                'start_date':form.cleaned_data['start_date'],
                'end_date':form.cleaned_data['end_date'],
                'element':form.cleaned_data['element']
                }
        app_params ={}
        SS_wrapper = WRCCWrappers.Wrapper('Sodsum', data_params, app_specific_params=app_params)
        data = SS_wrapper.get_data()
        results = data
        results = SS_wrapper.run_app(data)
        context['elements'] = data['elements']
    context['results']= dict(results)
    return render_to_response('wrcc_apps/Sodsum.html', context, context_instance=RequestContext(request))

def sods(request, app_name):
    units = {'pcpn':'Hundredths of Inches', 'snow':'Tenths of Inches', 'snwd': 'Inches', 'maxt':'Whole Degrees', 'mint':'Whole Degrees',\
             'avgt':'Whole Degrees', 'dtr':'Whole Degrees', 'hdd':'Days', 'cdd':'Days','gdd':'Days'}
    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    context = {
    'title': '%s' % app_name,
    }
    #Form 1 dealing with station selection and for some apps, preliminary information
    form1 = set_as_form(request, 'Sod0', init={'app_name': app_name})
    context['form1'] = form1
    if 'stn_selection' in request.POST:
        #if app_name == 'Soddd':
        #    form1 = set_as_form(request, 'Sod0', init={'app_name': app_name, 'skip_days':False})
        #elif app_name  == 'Sodthr':
        #    form1 = set_as_form(request, 'Sod0', init={'app_name': app_name, 'custom_tables':False, 'number_of_threholds':1})
        #else:
        form1 = set_as_form(request, 'Sod0', init={'app_name': app_name})
        context['form1'] = form1
        if form1.is_valid():
            context['form_2_ready'] = '2ready'
            station_selection = form1.cleaned_data['station_selection']
            if app_name == 'Soddd':
                initial = {'app_name':app_name, 'station_selection':station_selection, \
                'skip_days':form1.cleaned_data['skip_days'], 'truncate':form1.cleaned_data['truncate'] }
            elif app_name == 'Sodpct':
                initial = {'app_name':app_name, 'station_selection':station_selection,\
                'threshold':form1.cleaned_data['threshold'], 'element':form1.cleaned_data['element'], \
                'individual_averages': form1.cleaned_data['individual_averages'] }
            elif app_name == 'Sodthr':
                initial = {'app_name':app_name, 'station_selection':station_selection,\
                'custom_tables':form1.cleaned_data['custom_tables'],'number_of_thresholds': form1.cleaned_data['number_of_thresholds']}
            elif app_name == 'Sodxtrmts':
                initial = {'app_name':app_name, 'station_selection':station_selection,\
                'statistic':form1.cleaned_data['statistic'], 'element':form1.cleaned_data['element'], \
                'frequency_analysis':form1.cleaned_data['frequency_analysis'],'statistic_period':'monthly'}
            elif app_name == 'Sodpiii':
                initial = {'app_name':app_name, 'station_selection':station_selection,\
                'skew':form1.cleaned_data['skew'], 'cv':form1.cleaned_data['cv'], 'mean':form1.cleaned_data['mean'], \
                'pct_average':form1.cleaned_data['pct_average'], 'days':form1.cleaned_data['days']}
            else:
                initial = {'app_name':app_name, 'station_selection':station_selection}
            form2 = set_as_form2(init=initial)
            context['form2'] = form2
        else:
            station_selection=None

    #Form2 Application parameters
    if 'app_form' in request.POST:
        form2 = set_as_form(request, 'Sod')
        context['form2'] = form2
        #import pdb; pdb.set_trace()
        if  form2.is_valid():
            context['cleaned'] = form2.cleaned_data
            #Check for POR
            vd = None
            if 'station_id' in form2.cleaned_data.keys() or 'stnid' in form2.cleaned_data.keys():
                if 'station_id' in form2.cleaned_data.keys():
                    stn_id = form2.cleaned_data['station_id']
                if 'stnid' in form2.cleaned_data.keys():
                    stn_id = form2.cleaned_data['stn_id']
                if 'start_date' in form2.cleaned_data.keys() and form2.cleaned_data['start_date'].upper() == 'POR':
                        vd = WRCCUtils.find_valid_daterange(stn_id, max_or_min='max')
                if 'end_date' in form2.cleaned_data.keys() and form2.cleaned_data['end_date'].upper() == 'POR' and vd is None:
                        vd = WRCCUtils.find_valid_daterange(stn_id, max_or_min='max')
            if vd is not None and len(vd) == 2:
                form2.cleaned_data['start_date'] = vd[0]
                form2.cleaned_data['end_date'] = vd[1]
            (data, dates, elements, station_ids, station_names) = AcisWS.get_sod_data(form2.cleaned_data, app_name)
            #get contexts for the different apps and run data application
            if app_name in ['Sodrun', 'Sodrunr']:
                if elements == ['maxt', 'mint']:
                    context['el'] = 'range'
                else:
                    context['el'] = str(elements[0])
                if form2.cleaned_data['aeb'] == 'A':
                    context['op'] = '>'
                elif form2.cleaned_data['aeb'] == 'B':
                    context['op'] = '<'
                else:
                    context['op'] = '='
                context['thresh'] = form2.cleaned_data['threshold']
                context['dur'] = form2.cleaned_data['minimum_run']
                app_args = {'app_name': app_name, 'data':data,'dates':dates,'elements':elements,\
                'station_ids':station_ids,'station_names':station_names,'op':context['op'],\
                'thresh':context['thresh'], 'verbose': form2.cleaned_data['verbose'], 'minimum_run': form2.cleaned_data['minimum_run']}
                results = WRCCDataApps.Sodrun(**app_args)
            elif app_name == 'Soddynorm':
                app_args = {'app_name': app_name, 'data':data,'dates':dates,'elements':elements,\
                'station_ids':station_ids,'station_names':station_names,\
                'filter_type':form2.cleaned_data['filter_type'],\
                'filter_days':form2.cleaned_data['number_of_days']}
                results = WRCCDataApps.Soddynorm(**app_args)
                '''
                results = run_data_app(app_name, data, dates, elements, station_ids, station_names, \
                form2.cleaned_data['filter_type'], form2.cleaned_data['number_of_days'])
                '''
            elif app_name == 'Soddyrec':
                app_args = {'app_name': app_name, 'data':data,'dates':dates,'elements':elements,\
                    'station_ids':station_ids,'station_names':station_names}
                results = WRCCDataApps.Soddyrec(**app_args)
                #context['data'] =results
            elif app_name == 'Soddd':
                base_temp = form2.cleaned_data['base_temperature']
                output_type = form2.cleaned_data['output_type']
                max_miss = form2.cleaned_data['max_missing_days']
                a_b = form2.cleaned_data['above_or_below']
                if a_b == 'a':
                    context['a_b'] = 'ABOVE'
                else:
                    context['a_b'] = 'BELOW'
                max_miss = form2.cleaned_data['max_missing_days']
                ncdc_round = form2.cleaned_data['ncdc_roundoff']
                context['ncdc_round'] = ncdc_round
                app_args = {'app_name':app_name,'data':data,'dates':dates,'elements':elements,\
                'station_ids':station_ids,'station_names':station_names,\
                'base_temp':base_temp, 'a_b':a_b,'output_type':output_type, \
                'max_miss':max_miss, 'ncdc_round':ncdc_round}
                context['skip_max_above'] = 'NO DAYS SKIPPED'
                context['skip_min_below'] = 'NO DAYS SKIPPED'
                context['trunc_high'] = 'NONE'
                context['trunc_low'] = 'NONE'
                if form2.cleaned_data['skip_days']:
                     skip_max_above = form2.cleaned_data['skip_days_with_max_above']
                     skip_min_below = form2.cleaned_data['skip_days_with_min_below']
                     app_args['skip_max_above'] = skip_max_above
                     app_args['skip_min_below'] = skip_min_below
                     context['skip_max_above'] = skip_max_above
                     context['skip_min_below'] = skip_min_below
                if form2.cleaned_data['truncate']:
                    trunc_high = form2.cleaned_data['truncation_upper_limit']
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
                'station_ids':station_ids,'station_names':station_names}
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
                'ids':station_ids,'station_names':station_names,'el_type':el_type, 'max_missing_days':form2.cleaned_data['max_missing_days']}
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
            elif app_name == 'Sodpct':
                el_type = form2.cleaned_data['element']
                if abs(form2.cleaned_data['threshold'] + 9999) < 0.05:
                    threshold = None
                else:
                    threshold = form2.cleaned_data['threshold']
                ia = form2.cleaned_data['individual_averages']
                number_days_ahead = form2.cleaned_data['number_days_ahead']
                if 'threshold_ab' in form2.cleaned_data.keys():
                    threshold_ab = form2.cleaned_data['threshold_ab']
                else:
                    threshold_ab = None
                if el_type in ['hdd', 'cdd', 'gdd']:
                    base_temperature = form2.cleaned_data['base_temperature']
                    if el_type == 'gdd':
                        min_temperature = form2.cleaned_data['min_temperature']
                        max_temperature = form2.cleaned_data['max_temperature']
                    else:
                        min_temperature = None
                        max_temperature = None
                else:
                    base_temperature = None
                    min_temperature = None
                    max_temperature = None
                if 'begin_month' in form2.cleaned_data.keys():
                    begin_month = form2.cleaned_data['begin_month']
                else:
                    begin_month = None
                if 'accumulate_over_season' in form2.cleaned_data.keys():
                    accumulate_over_season = form2.cleaned_data['accumulate_over_season']
                else:
                    accumulate_over_season = None
                app_args = {'app_name':app_name,'data':data,'dates':dates,'elements':elements,\
                'station_ids':station_ids,'station_names':station_names,'el_type':el_type,\
                'ia':ia, 'number_days_ahead':number_days_ahead,'threshold':threshold, 'threshold_ab':threshold_ab, \
                'base_temperature':base_temperature, 'min_temperature':min_temperature, \
                'max_temperature':max_temperature, 'begin_month':begin_month, 'accumulate_over_season':accumulate_over_season }
                if threshold_ab == 'A':
                    context['op'] = 'Above'
                elif threshold_ab == 'B':
                    context['op'] = 'Below'
                context['base_temperature'] = base_temperature
                context['min_temperature'] = min_temperature
                context['min_temperature'] = max_temperature
                context['begin_month'] = begin_month
                context['threshold'] = threshold
                if threshold_ab == 'a':context['op'] = 'ABOVE'
                if threshold_ab == 'b':context['op'] = 'BELOW'
                context['element'] =  el_type
                context['units'] = units[el_type]
                context['individual_averages'] = ia
                results = run_data_app(**app_args)
            elif app_name == 'Sodthr':
                header = {}
                el_type = form2.cleaned_data['element']
                start_year = dates[0][0:4]
                end_year = dates[-1][0:4]
                number_of_thresholds = form2.cleaned_data['number_of_thresholds']
                custom_tables = form2.cleaned_data['custom_tables']
                if custom_tables == 'T':
                    time_series = []
                    thresholds = []
                    #set headers
                    for k in range(3):
                        header[k] = set_sodthr_headers(k, el_type, str(form2.cleaned_data['interval_start']), \
                        str(form2.cleaned_data['midpoint']),str(form2.cleaned_data['interval_end']), start_year, end_year, \
                        int(form2.cleaned_data['max_missing_days_first_and_last']), int(form2.cleaned_data['max_missing_days_differences']), \
                        str(form2.cleaned_data['above_or_below']), str(form2.cleaned_data['latest_or_earliest_for_period_1']), \
                        str(form2.cleaned_data['latest_or_earliest_for_period_2']))
                    #Find list of thresholds, and time_series_booleans
                    for k in range(int(number_of_thresholds)):
                        thresholds.append(float(form2.cleaned_data['threshold_%s' % str(k)]))
                        time_series.append(form2.cleaned_data['time_series_%s' % str(k)])
                    #set application arguments
                    app_args = {'app_name':app_name,'data':data,'dates':dates,'elements':elements,\
                    'station_ids':station_ids,'station_names':station_names,'el_type':el_type, 'custom_tables':True, \
                    'interval_start':form2.cleaned_data['interval_start'], 'midpoint':form2.cleaned_data['midpoint'], \
                    'interval_end':form2.cleaned_data['interval_end'], 'thresholds': thresholds, 'time_series': time_series, \
                    'le_1': form2.cleaned_data['latest_or_earliest_for_period_1'], \
                    'le_2':form2.cleaned_data['latest_or_earliest_for_period_2'], 'ab':form2.cleaned_data['above_or_below'], \
                    'miss_days_1':form2.cleaned_data['max_missing_days_first_and_last'], 'miss_days_2':form2.cleaned_data['max_missing_days_differences']}
                else:
                    #set headers
                    for k in range(3):
                        header[k] = set_sodthr_headers(k, el_type, '0101', '0731',  '1231', start_year, \
                        end_year, 10, 10, 'BELOW', 'latest','earliest')
                    app_args = {'app_name':app_name,'data':data,'dates':dates,'elements':elements,\
                    'station_ids':station_ids,'station_names':station_names,'el_type':el_type, 'custom_tables':False}
                context['header'] = header
                results = run_data_app(**app_args)
            elif app_name == 'Sodxtrmts':
                context['element'] = form2.cleaned_data['element']
                context['max_missing_days'] = form2.cleaned_data['max_missing_days']
                context['start_month'] = WRCCData.NUMBER_TO_MONTH_NAME[form2.cleaned_data['start_month']]
                mon_start = int(form2.cleaned_data['start_month'].lstrip('0'))
                month_list = []
                for mon_idx in range(mon_start -1,12):
                    month_list.append(months[mon_idx])
                for mon_idx in range(mon_start-1):
                    month_list.append(months[mon_idx])
                month_list.append('ANN')
                context['month_list'] = month_list
                context['frequency_analysis'] = WRCCData.DISPLAY_PARAMS[form2.cleaned_data['frequency_analysis']]
                context['statistic'] = WRCCData.DISPLAY_PARAMS[form2.cleaned_data['statistic']]
                context['departure_from_averages'] = WRCCData.DISPLAY_PARAMS[form2.cleaned_data['departures_from_averages']]
                app_args = {
                    'app_name':app_name,
                    'data':data,
                    'dates':dates,
                    'elements':elements,
                    'station_ids':station_ids,
                    'station_names':station_names,
                    'element':form2.cleaned_data['element'],
                    'max_missing_days':form2.cleaned_data['max_missing_days'],
                    'start_month': form2.cleaned_data['start_month'],
                    'statistic_period':'monthly',
                    'statistic': form2.cleaned_data['statistic'],
                    'frequency_analysis': form2.cleaned_data['frequency_analysis'],
                    'departures_from_averages':form2.cleaned_data['departures_from_averages']
                }
                if form2.cleaned_data['frequency_analysis'] == 'T':
                    context['frequency_analysis_type'] = form2.cleaned_data['frequency_analysis_type']
                    app_args['frequency_analysis_type'] = form2.cleaned_data['frequency_analysis_type']
                if form2.cleaned_data['statistic'] == 'ndays':
                    app_args['less_greater_or_between'] = form2.cleaned_data['less_greater_or_between']
                    if form2.cleaned_data['less_greater_or_between'] == 'b':
                        app_args['threshold_low_for_between'] = form2.cleaned_data['threshold_low_for_between']
                        app_args['threshold_high_for_between'] = form2.cleaned_data['threshold_high_for_between']
                    else:
                        app_args['threshold_for_less_or_greater'] = form2.cleaned_data['threshold_for_less_or_greater']
                if form2.cleaned_data['element'] in ['hdd', 'gdd', 'cdd']:
                    app_args['base_temperature'] = form2.cleaned_data['base_temperature']
                context['app_arg'] = app_args
                results = WRCCDataApps.Sodxtrmts(**app_args)
                #context['fa_results'] = dict(fa_results)
            elif app_name == 'Sodpiii':
                lisdur = [ '6 Hrs', '12 Hrs', '1 Day', '2 Days', '3 Days', \
                        '4 Days', '5 Days', '6 Days', '7 Days', '8 Days', '9 Days', \
                        '10 Days', '15 Days', '20 Days', '25 Days', '30 Days']
                context['el_type'] = form2.cleaned_data['element']
                context['units'] = units[form2.cleaned_data['element']]
                context['start_year'] = form2.cleaned_data['start_date'][0:4]
                context['end_year'] = str(int(form2.cleaned_data['end_date'][0:4]) - 1)
                context['start_month'] = form2.cleaned_data['start_date'][4:6]
                context['end_month'] = form2.cleaned_data['end_date'][4:6]
                app_args = {'app_name':app_name,'data':data,'dates':dates,'elements':elements,\
                'station_ids':station_ids,'station_names':station_names, \
                'el_type':form2.cleaned_data['element'], 'skew':form2.cleaned_data['skew'], \
                'cv':form2.cleaned_data['cv'], 'mean': form2.cleaned_data['mean'], \
                'pct_average':form2.cleaned_data['pct_average'], \
                'value_subsequent':form2.cleaned_data['value_subsequent'], \
                'value_missing':form2.cleaned_data['value_missing'],'days':form2.cleaned_data['days']}
                if form2.cleaned_data['element'] == 'avgt':
                    app_args['ab'] = form2.cleaned_data['mean_temperatures']
                duration = {}
                if form2.cleaned_data['days'] == 'i':
                    app_args['number_of_days'] = int(form2.cleaned_data['number_of_days'])
                    duration[0] = '%i Days' % int(form2.cleaned_data['number_of_days'])
                elif form2.cleaned_data['days'] == '5':
                    for k in range(5):
                        duration[k] = lisdur[k + 2]
                elif form2.cleaned_data['days'] == 'a':
                    for k in range(len(lisdur)):
                        duration[k] = lisdur[k]
                context['duration'] = duration
                results_0, results, averages, stdevs, skews = WRCCDataApps.Sodpiii(**app_args)
                context['averages'] = averages
                context['stdevs'] = stdevs
                context['skews'] = skews
                context['results_0'] = dict(results_0)
            else:
                results = {}

            #general context
            try:
                context['results'] = dict(results)
            except:
                context['results'] = results
            context['dates'] = dates
            if app_name in ['Sodrun', 'Sodrunr', 'Soddyrec', 'Sodcnv', 'Sodlist']:
                context['start_year'] = dates[0]
                context['end_year'] = dates[-1]
            elif app_name in ['Soddd', 'Sodpiii', 'Sodsumm']:
                context['start_year'] = dates[0][0:4]
                context['end_year'] = str(int(dates[-1][0:4]))
            else:
                context['start_year'] = dates[0][0:4]
                if app_name == 'Sodxtrmts':
                    context['end_year'] = dates[-1][0:4]
                else:
                    context['end_year'] = str(int(dates[-1][0:4])+1)
            context['num_yrs'] = int(dates[-1][0:4]) - int(dates[0][0:4])+1
            context['elements'] = dict([(k,v) for k,v in enumerate(elements)])
            context['data'] = dict(data)
            context['station_ids'] = dict([(k,v) for k,v in enumerate(station_ids)])
            context['station_names'] = dict([(k,v) for k,v in enumerate(station_names)])
        #form_2 not valid or we are done with analysis
        form2 = set_as_form(request, 'Sod')
        context['form2'] = form2
        context['form_2_ready'] = True
        station_selection = None
        #else: #form_2 is not valid
        #    print "The following errors occurred:"
        #    print form2.errors
        #    station_selection = None
    return render_to_response('wrcc_apps/%s.html' % app_name, context, context_instance=RequestContext(request))

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


def run_data_app(app_name,*args, **kwargs):
    data_app = getattr(WRCCDataApps, app_name)
    '''
    try:
        results = data_app(*args, **kwargs)
    except:
        results = 'Error: Could not run data app %s. Check arguments:'  % app_name
    '''
    results = data_app(*args, **kwargs)
    return results

def set_sodthr_headers(tbl_idx, el, int_start, midpoint,  int_end, start_year, end_year, days_miss_1, days_miss_2, ab, le_1, le_2):
    lines = []
    if tbl_idx == 0:
        lines.append('PROBABILITY OF <b>%s</b> DATE OF <b>%s %s</b></br>' % (le_1, el, ab))
        lines.append('THE INDICATED THRESHOLD VALUE (DEGREES F).</br>')
        lines.append('DURING THE FOLLOWING INTERVAL:</br>')
        lines.append('START MONTH-DAY: <b>%s</b>  END MONTH-DAY:  <b>%s</b>' % (int_start, midpoint))
        lines.append('YEARS USED:  <b>%s -  %s</b> </br>' % (start_year, end_year))
        lines.append('WITH NO MORE THAN  <b>%i</b> MISSING DAYS DURING THE INTERVAL.</br>' % days_miss_1)
        lines.append('[ -01-01 ] INDICATES NON-OCCURRENCE OF THE THRESHOLD</br>')
    elif tbl_idx == 1:
        lines.append('PROBABILITY OF <b>%s</b> DATE OF <b>%s %s</b></br>' % (le_2, el, ab))
        lines.append('THE INDICATED THRESHOLD VALUE (DEGREES F).</br>')
        lines.append('DURING THE FOLLOWING INTERVAL:</br>')
        lines.append('START MONTH-DAY: <b>%s</b>  END MONTH-DAY:  <b>%s</b>' % (midpoint, int_end))
        lines.append('YEARS USED:  <b>%s -  %s</b> </br>' % (start_year, end_year))
        lines.append('WITH NO MORE THAN  <b>%i</b> MISSING DAYS DURING THE INTERVAL.</br>' % days_miss_1)
        lines.append('[ -01-01 ] INDICATES NON-OCCURRENCE OF THE THRESHOLD</br>')
    else:
        lines.append('PROBABILITY OF NO MORE THAN THE INDICATED NUMBER OF DAYS (I.E., PERCENTILE)</br>')
        lines.append('---  BETWEEN  ---</br>')
        lines.append('(1) THE <b>%s</b> DATE OF <b>%s %s</b></br>' % (le_1, el, ab))
        lines.append('THE INDICATED THRESHOLD VALUE (DEGREES F) DURING</br>')
        lines.append('THE  FIRST INTERVAL ---      START MONTH-DAY: <b>%s</b> END MONTH-DAY:  <b>%s</b> </br>'  % (int_start, midpoint))
        lines.append('---  AND  ---</br>')
        lines.append('(2) THE <b>%s</b> DATE OF <b>%s %s</b></br>' % (le_2, el, ab))
        lines.append('THE SAME THRESHOLD VALUE (DEGREES F) DURING</br>')
        lines.append('THE  SECOND INTERVAL ---      START MONTH-DAY: <b>%s</b> END MONTH-DAY:  <b>%s</b> </br>'  % (midpoint, int_end))
        lines.append('YEARS USED:  <b>%s -  %s</b> </br>' % (start_year, end_year))
        lines.append('WITH NO MORE THAN  <b>%i</b> MISSING DAYS DURING THE TWO INTERVALS COMBINED.</br>' % days_miss_2)
        lines.append('[ 367.0 ] INDICATES NON-OCCURRENCE OF THE THRESHOLD</br>')

    return "\n".join(lines)

def set_sodsumm_headers(table_list):
    headers = {}
    def set_header(table):
        rows = []
        if table == 'temp':
            rows.append('<th colspan="16"> Temperature Statistics:</th>')
            rows.append('<th colspan="2"></th><th colspan="4">Averages, </th><th colspan="4">Daily Extremes, </th><th colspan="4">Mean Extremes, </th><th colspan="2"> >= =<  =<  =< </th>')
        elif table == 'prsn':
            rows.append('<th colspan="15">Precipitation/Snow Statistics:</th>')
            rows.append('<th colspan="6">Total Precipitation, </th><th colspan="2">Precipitation, </th><th colspan="3">Total Snowfall, </th><th colspan="4">#Days Precip</th>')

        elif table == 'hdd':
            rows.append('<th colspan="14">Heating degree days:</th>')
            rows.append('<tr><td colspan="14">Output is rounded, unlike NCDC values, which round input.</td></tr>')
            rows.append('<tr><td colspan="14">Degree Days to selected Base Temperatures(F)</td></tr>')
        elif table == 'cdd':
            rows.append('<th colspan="14">Cooling degree days:</th>')
            rows.append('<tr><td colspan="14">Output is rounded, unlike NCDC values, which round input.</td></tr>')
            rows.append('<tr><td colspan="14">Degree Days to selected Base Temperatures(F)</td></tr>')
        elif table == 'gdd':
            rows.append('<th colspan="15">Growing degree days:</th>')
            rows.append('<tr><td colspan="15">Output is rounded, unlike NCDC values, which round input.</td>')
            rows.append('<tr><td colspan="15">Growing Degree Days to selected Base Temperatures(F)</td></tr>')
        elif table == 'corn':
            rows.append('<th colspan="15">Corn Growing Degree Days</th>')
        return "\n".join(rows)

    for table in table_list:
         headers[table] = set_header(table)
    return headers
