#!/usr/bin/python

#django imports
from django.template import RequestContext
#from django.contrib.auth.models import User
#from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db.models.query import QuerySet
from django.contrib.localflavor.us.forms import USStateField
from django.conf import settings

#Python imports
import datetime
from collections import defaultdict
import json
from shutil import copy2 as scopy2
import sys, os, stat, re
#for copying mutable objects
import copy
#My modules
import WRCCUtils, DJANGOUtils
import AcisWS, WRCCDataApps, WRCCClasses, WRCCData, WRCCFormCheck
import WRCCToReplace
import scenic.forms as forms

#Set dates
today = WRCCUtils.set_back_date(0)
today_year = today[0:4]
today_month = today[5:7]
today_day = today[8:10]
begin_10yr = WRCCUtils.set_back_date(3660)
yesterday = WRCCUtils.set_back_date(1)
fourtnight = WRCCUtils.set_back_date(14)
week = WRCCUtils.set_back_date(7)
yrs_ago = WRCCUtils.set_back_date(3660)[0:4]
############################################
###PAGES
############################################
def home(request):
    context = {
        'title': settings.APPLICATIONS['home'][0],
    }
    url = settings.APPLICATIONS['home'][2]
    return render_to_response(url, context, context_instance=RequestContext(request))

def swcke_home(request):
    context = {
        'title': 'Page Redirect',
    }
    return render_to_response('scenic/swcke_home.html', context, context_instance=RequestContext(request))

def about(request):
    context = {
        'title': settings.APPLICATIONS['about'][0],
        'icon':'AboutUs.png'
    }
    url = settings.APPLICATIONS['about'][2]
    return render_to_response(url, context, context_instance=RequestContext(request))

def monitoring(request):
    app_name = 'monitoring'
    url = settings.APPLICATIONS[app_name][2]
    app_url = settings.APPLICATIONS[app_name][1]
    context = {
        'title': settings.APPLICATIONS[app_name][0],
        'app_name':app_name,
        'app_url': app_url
    }
    #Find mon, year to locate snotel map
    year = str(datetime.datetime.today().year)
    month = str(datetime.datetime.today().month)
    day = str((datetime.datetime.today() - datetime.timedelta(days=1)).day) #yesterday
    context['full_date_for_ahps'] = '%s/%s/%s' % (year, month.lstrip('0'), day.lstrip('0'))
    if len(month) ==1:
        month = '0%s' %month
    context['month'] = month
    if month == '01':
        context['month_nadm'] = '12'
    else:
        context['month_nadm'] = str(int(month.lstrip('0')) - 1)
    context['year'] = year
    context['year_short'] = '%s%s' % (year[-2], year[-1])
    year_wy = year
    year_short_wy = year
    month_wy = month
    if int(month) > 5:
        month_wy = '05'
    context['month_wy'] = month_wy
    year_short_wy = '%s%s' % (year_wy[-2], year_wy[-1])
    context['year_wy'] = year_wy
    context['year_short_wy'] = '%s%s' % (year_wy[-2], year_wy[-1])
    return render_to_response(url, context, context_instance=RequestContext(request))

def howto(request):
    app_name = 'howto'
    url = settings.APPLICATIONS[app_name][2]
    app_url = settings.APPLICATIONS[app_name][1]
    context = {
        'title': settings.APPLICATIONS[app_name][0],
        'app_name':app_name,
        'app_url': app_url
    }
    app_urls = {};app_names = {};param_urls = {}
    #HOWTO: STATION FINDER
    app_url = settings.APPLICATIONS['station_finder'][1]
    p_url = app_url + '?'
    p_url+='area_type=shape'
    p_url+='&shape=-120.15,39.2,-120.02,39.27,-119.9,39.21,-119.92,38.96,-120.02,38.91,-120.15,38.97,-120.18,39.11'
    p_url+='&variables=mint,pcpn&variables_constraints=all'
    p_url+='&start_date=19300101&end_date=20141231&dates_constraints=all'
    app_urls['station_finder'] = app_url
    param_urls['station_finder'] = p_url
    app_names['station_finder'] = settings.APPLICATIONS['station_finder'][0]
    #HOWTO MULTI LISTER
    app_url = settings.APPLICATIONS['multi_lister'][1]
    p_url = app_url + '?'
    p_url+='area_type=county'
    p_url+='&county=Washoe, 32031'
    p_url+='&data_type=station'
    p_url+='&variables=maxt,mint,avgt,obst'
    p_url+='&start_date=19900101&end_date=' + yesterday
    p_url+='&data_summary=none'
    p_url+='&show_flags=F&show_observation_time=T'
    p_url+='&output_file_name=multi_lister_example'
    p_url+='&user_name=Tester&user_email=scenic@dri.edu'
    app_urls['multi_lister'] = app_url
    param_urls['multi_lister'] = p_url
    app_names['multi_lister'] = settings.APPLICATIONS['multi_lister'][0]
    #Gallery: MONTHLY SUMMARIES
    app_url = settings.APPLICATIONS['monthly_summary'][1]
    p_url = app_url + '?'
    p_url+='area_type=station_id&station_id=269171&variable=maxt'
    p_url+='&start_year=POR&end_year=POR'
    p_url+='&statistic=mmax'
    app_urls['monthly_summary'] = app_url
    param_urls['monthly_summary'] = p_url
    app_names['monthly_summary'] = settings.APPLICATIONS['monthly_summary'][0]
    #Gallery: SUMMARIZING SPATIAL DATA (spatial_summary)
    app_url = settings.APPLICATIONS['spatial_summary'][1]
    p_url = app_url + '?'
    p_url+='area_type=shape&shape=-120.77,36.84,-120.6,36.78,-120.54,36.71,-120.63,36.63,-120.76,36.77'
    p_url+='&spatial_summary=mean&variables=maxt,mint,avgt&grid=1&start_date=20150301&end_date=20150331'
    p_url+='&data_type=grid&grid=1'
    app_urls['spatial_summary'] = app_url
    param_urls['spatial_summary'] = p_url
    app_names['spatial_summary'] = settings.APPLICATIONS['spatial_summary'][0]
    #Set context variables
    context['app_urls'] = app_urls
    context['app_names'] = app_names
    context['param_urls'] = param_urls
    return render_to_response(url, context, context_instance=RequestContext(request))

def projections(request):
    app_name = 'projections'
    url = settings.APPLICATIONS[app_name][2]
    app_url = settings.APPLICATIONS[app_name][1]
    context = {
        'title': settings.APPLICATIONS[app_name][0],
        'app_name':app_name,
        'app_url': app_url
    }
    return render_to_response(url, context, context_instance=RequestContext(request))

def remote_sensing_data(request):
    app_name = 'remote_sensing_data'
    url = settings.APPLICATIONS[app_name][2]
    app_url = settings.APPLICATIONS[app_name][1]
    context = {
        'title': settings.APPLICATIONS[app_name][0],
        'app_name':app_name,
        'app_url': app_url
    }
    return render_to_response(url, context, context_instance=RequestContext(request))

def data(request):
    app_name = 'data'
    url = settings.APPLICATIONS[app_name][2]
    app_url = settings.APPLICATIONS[app_name][1]
    context = {
        'title': settings.APPLICATIONS[app_name][0],
        'app_name':app_name,
        'app_url': app_url
    }
    return render_to_response(url, context, context_instance=RequestContext(request))

def climate_data(request):
    app_name = 'climate_data'
    url = settings.APPLICATIONS[app_name][2]
    app_url = settings.APPLICATIONS[app_name][1]
    context = {
        'title': settings.APPLICATIONS[app_name][0],
        'app_name':app_name,
        'app_url': app_url
    }
    return render_to_response(url, context, context_instance=RequestContext(request))

def single_point_prods(request):
    app_name = 'single_point_prods'
    url = settings.APPLICATIONS[app_name][2]
    app_url = settings.APPLICATIONS[app_name][1]
    context = {
        'title': settings.APPLICATIONS[app_name][0],
        'app_name':app_name,
        'app_url': app_url
    }
    #Link from other apps
    if request.method == 'GET' and ('variables' in request.GET or 'variable' in request.GET):
        #set link params
        init = {}
        get_params = ['station_id','variables', 'start_date','end_date']
        get_initial = {}
        for item in request.GET:
            if str(item) not in get_params and str(item) != 'area_type':
                get_params.append(str(item))
            get_initial[str(item)] = request.GET[item]
        user_params = WRCCUtils.form_to_display_list(get_params,request.GET)
        context['user_params'] = user_params
        for app in ['single_lister', 'monthly_summary', 'climatology','data_comparison', 'seasonal_summary', 'single_year']:
            #initial= DJANGOUtils.set_initial(request, app)
            initial= DJANGOUtils.set_initial(get_initial, app)
            p_str = WRCCUtils.set_url_params(initial)
            context['url_params_' + app] =  p_str
    return render_to_response(url, context, context_instance=RequestContext(request))

def multi_point_prods(request):
    app_name = 'multi_point_prods'
    url = settings.APPLICATIONS[app_name][2]
    app_url = settings.APPLICATIONS[app_name][1]
    context = {
        'title': settings.APPLICATIONS[app_name][0],
        'app_name':app_name,
        'app_url': app_url
    }
    #Link from other apps
    if request.method == 'GET' and ('variables' in request.GET or 'variable' in request.GET):
        #set link params
        for app in ['multi_lister', 'spatial_summary', 'temporal_summary']:
            initial = DJANGOUtils.set_initial(request, app)
            p_str = WRCCUtils.set_url_params(initial)
            context['url_params_' + app] =  p_str
    return render_to_response(url, context, context_instance=RequestContext(request))

def single_lister(request):
    app_name = 'single_lister'
    url = settings.APPLICATIONS[app_name][2]
    app_url = settings.APPLICATIONS[app_name][1]
    context = {
        'title': settings.APPLICATIONS[app_name][0],
        'app_name':app_name,
        'app_url': app_url
    }
    initial = DJANGOUtils.set_initial(request,app_name)
    context['initial'] = initial

    if 'station_id_change' in request.POST:
        response_data = find_station_vd(request)
        response = set_ajax_response(response_data)
        return response

    if 'formDownload' in request.POST:
        form = DJANGOUtils.set_form(request,clean=False)
        json_file = request.POST.get('json_file', None)
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        file_name = form['output_file_name'] + '_' + time_stamp
        with open(settings.TEMP_DIR + json_file, 'r') as f:
            req =  json.load(f)
        #Override data_format, delimiter, output_file
        req['form']['data_format'] = form['data_format']
        req['form']['delimiter'] = form['delimiter']
        req['form']['output_file_name'] = form['output_file_name']
        if form['data_format'] in ['clm','dlm']:
            if form['data_format'] == 'clm':
                file_extension = '.txt'
            else:
                file_extension = '.dat'
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment;filename=%s%s' % (file_name,file_extension)
            if form['output_format'] == 'verbose':
                CsvWriter = WRCCClasses.CsvWriter(req, f=None, response=response)
            else:
                CsvWriter = WRCCClasses.CsvWriterNew(req, f=None, response=response)
            CsvWriter.write_to_file()
            return response
        if form['data_format'] in ['xl']:
            file_extension = '.xls'
            response = HttpResponse(content_type='application/vnd.ms-excel;charset=UTF-8')
            if form['output_format'] == 'verbose':
                ExcelWriter = WRCCClasses.ExcelWriter(req,response=response)
            else:
                ExcelWriter = WRCCClasses.ExcelWriterNew(req,response=response)
            ExcelWriter.write_to_file()
            response['Content-Disposition'] = 'attachment;filename=%s%s' % (file_name, file_extension)
            return response

    if request.method == 'GET' and 'projection' in request.GET:
        '''
        Link from projection page
            override some options
        '''
        new_init = {
            'area_type':'location',
            'location':'-119,39',
            'grid':'22'
        }
        initial = DJANGOUtils.set_initial(new_init, app_name)
        context['initial'] = initial
        return render_to_response(url, context, context_instance=RequestContext(request))

    #MAIN APP
    #Data request submitted
    if 'formData' in request.POST or (request.method == 'GET' and 'variables' in request.GET):
        form_cleaned = DJANGOUtils.set_form(initial,clean = True)
        form = DJANGOUtils.set_form(initial, clean = False)
        #Check form fields
        fields_to_check = [form_cleaned['area_type'],'start_date','end_date','start_window','end_window','degree_days']
        form_error = check_form(form_cleaned, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            if form_cleaned['area_type'] == 'location':
                #Only show gridpoint map if area caused form_error
                if 'Gridpoint' in form_error.keys():
                    context['need_gridpoint_map'] = True
            return render_to_response(url, context, context_instance=RequestContext(request))
        #Data requests
        try:
            req = WRCCUtils.request_and_format_data(form_cleaned)
            if 'smry' not in req.keys() and 'data' not in  req.keys():
                results = {'error':'No data found for these parameters!'}
                context['results'] = results
                return render_to_response(url, context, context_instance=RequestContext(request))
        except Exception, e:
            results = {'error':'Data request error: %s' %str(e)}
            context['results'] = results
            return render_to_response(url, context, context_instance=RequestContext(request))
        #req = WRCCUtils.request_and_format_data(form_cleaned)
        #Format Data for display and/or download
        #Overide data with windowed data if desired
        if 'data_summary' in form.keys() and form['data_summary'] == 'windowed_data':
            d = req['data'][0]
            header = d[0]
            sd = form_cleaned['start_date']
            ed = form_cleaned['end_date']
            sw = form_cleaned['start_window']
            ew = form_cleaned['end_window']
            req['data'] = WRCCUtils.get_windowed_data(d, sd, ed, sw, ew)
            req['data'].insert(0,header)
            req['data'] = [req['data']]
        if not req['data'] and not req['smry']:
            req['error'] = 'No data found for these parameters.'
            context['results'] = req
            return render_to_response(url, context, context_instance=RequestContext(request))
        context['run_done'] = True
        context['results'] = req
        #Set display headers
        header_keys = WRCCUtils.set_display_keys(app_name, form_cleaned)
        context['params_display_list'] = WRCCUtils.form_to_display_list(header_keys,form)
        if 'meta' in req.keys() and req['meta']:
            meta_keys = WRCCUtils.get_meta_keys(form_cleaned)
            meta_display_list = WRCCUtils.metadict_to_display_list(req['meta'][0], meta_keys,form)
            context['meta_display_list'] = meta_display_list
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        file_name = form_cleaned['output_file_name'] + '_' + time_stamp
        #Deal with different data formats
        if form_cleaned['data_format'] in ['clm','dlm'] and (req['data'] or req['smry']):
            if form_cleaned['data_format'] == 'clm':
                file_extension = '.txt'
            else:
                file_extension = '.dat'
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment;filename=%s%s' % (file_name,file_extension)
            if form['output_format'] == 'verbose':
                CsvWriter = WRCCClasses.CsvWriter(req, f=None, response=response)
            else:
                CsvWriter = WRCCClasses.CsvWriterNew(req, f=None, response=response)
            CsvWriter.write_to_file()
            return response
        if form_cleaned['data_format'] in ['xl'] and (req['data'] or req['smry']):
            file_extension = '.xls'
            response = HttpResponse(content_type='application/vnd.ms-excel;charset=UTF-8')
            if form['output_format'] == 'verbose':
                ExcelWriter = WRCCClasses.ExcelWriter(req,response=response)
            else:
                ExcelWriter = WRCCClasses.ExcelWriterNew(req,response=response)
            ExcelWriter.write_to_file()
            response['Content-Disposition'] = 'attachment;filename=%s%s' % (file_name, file_extension)
            return response
        #Save data for download button
        if form_cleaned['data_format'] in ['html'] and (req['data'] or req['smry']):
            results_json = json.dumps(req)
            json_file  = form['output_file_name'] + '.json'
            with open(settings.TEMP_DIR + json_file,'w+') as f:
                f.write(results_json)
            context['json_file'] = json_file
    return render_to_response(url, context, context_instance=RequestContext(request))

def single_year(request):
    app_name = 'single_year'
    url = settings.APPLICATIONS[app_name][2]
    app_url = settings.APPLICATIONS[app_name][1]
    context = {
        'title': settings.APPLICATIONS[app_name][0],
        'app_name':app_name,
        'app_url': app_url
    }

    if 'station_id_change' in request.POST:
        response_data = find_station_vd(request)
        response = set_ajax_response(response_data)
        return response

    #Download button pressed
    if 'formDownload' in request.POST:
        form = DJANGOUtils.set_form(request,clean=False)
        json_file = request.POST.get('json_file', None)
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        file_name = form['output_file_name'] + '_' + time_stamp
        with open(settings.TEMP_DIR + json_file, 'r') as f:
            req =  json.load(f)
        #Override data_format, delimiter, output_file
        req['form']['data_format'] = form['data_format']
        req['form']['delimiter'] = form['delimiter']
        req['form']['output_file_name'] = form['output_file_name']
        if form['data_format'] in ['clm','dlm']:
            if form['data_format'] == 'clm':
                file_extension = '.txt'
            else:
                file_extension = '.dat'
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment;filename=%s%s' % (file_name,file_extension)
            CsvWriter = WRCCClasses.CsvWriter(req, f=None, response=response)
            CsvWriter.write_to_file()
            return response
        if form['data_format'] in ['xl']:
            file_extension = '.xls'
            response = HttpResponse(content_type='application/vnd.ms-excel;charset=UTF-8')
            ExcelWriter = WRCCClasses.ExcelWriter(req,response=response)
            ExcelWriter.write_to_file()
            response['Content-Disposition'] = 'attachment;filename=%s%s' % (file_name, file_extension)
            return response

    if request.method == 'GET' and 'projection' in request.GET:
        '''
        Link from projection page
            override some options
        '''
        new_init = {
            'area_type':'location',
            'location':'-119,39',
            'grid':'22'
        }
        initial = DJANGOUtils.set_initial(new_init, app_name)
        context['initial'] = initial
        return render_to_response(url, context, context_instance=RequestContext(request))

    #MAIN APP
    initial = DJANGOUtils.set_initial(request,app_name)
    context['initial'] = initial
    if 'formData' in request.POST or (request.method == 'GET' and 'variable' in request.GET):
        form = DJANGOUtils.set_form(initial,clean = False)
        form_cleaned = DJANGOUtils.set_form(initial,clean = True)
        year_txt_data, year_graph_data, climoData, percentileData = WRCCUtils.get_single_single_year_data(form_cleaned)
        if not year_txt_data:
            results = {
                'error':'No data found for these parameters!'
            }
            return render_to_response(url, context, context_instance=RequestContext(request))
        context['run_done'] = True
        header_keys = WRCCUtils.set_display_keys(app_name, form)
        context['params_display_list'] = WRCCUtils.form_to_display_list(header_keys,form)
        results = {
            'variable_short': form['variable'],
            'data_indices':range(len(year_txt_data)),
            'data':year_txt_data,
            'target_year':int(form_cleaned['target_year']),
            'error':''
        }
        cp_data = {
            'climoData':climoData,
            'percentileData':percentileData
        }
        results['cp_data'] = cp_data
        #Set graph data
        graph_data = []
        for yr_idx, year in enumerate(year_graph_data.keys()):
            year = int(form_cleaned['start_year']) + yr_idx
            yr_data = year_graph_data[year]
            GDWriter = WRCCClasses.GraphDictWriter(form_cleaned, yr_data)
            graph_dict = GDWriter.write_dict()
            graph_data.append(graph_dict)
        results['graph_data'] = graph_data
        context['results'] = results
        #Save results for downloading
        yr_range = range(int(form_cleaned['start_year']),int(form_cleaned['end_year']) + 1)
        json_dict = {
            'smry':[],
            #'params_display_list':context['params_display_list']
            'form':form_cleaned,
            'data':[results['data'][year] for year in yr_range]
        }
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        json_file = '%s_%s.json' %(time_stamp,app_name)
        WRCCUtils.load_data_to_json_file(settings.TEMP_DIR +json_file, json_dict)
        context['json_file'] = json_file

    return render_to_response(url, context, context_instance=RequestContext(request))

def seasonal_summary(request):
    app_name = 'seasonal_summary'
    url = settings.APPLICATIONS[app_name][2]
    app_url = settings.APPLICATIONS[app_name][1]
    context = {
        'title': settings.APPLICATIONS[app_name][0],
        'app_name':app_name,
        'app_url': app_url
    }

    if 'station_id_change' in request.POST:
        response_data = find_station_vd(request)
        response = set_ajax_response(response_data)
        return response

    #Download button pressed
    if 'formDownload' in request.POST:
        form = DJANGOUtils.set_form(request,clean=False)
        json_file = request.POST.get('json_file', None)
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        file_name = form['output_file_name'] + '_' + time_stamp
        with open(settings.TEMP_DIR + json_file, 'r') as f:
            req =  json.load(f)
        #Override data_format, delimiter, output_file
        req['form']['data_format'] = form['data_format']
        req['form']['delimiter'] = form['delimiter']
        req['form']['output_file_name'] = form['output_file_name']
        if form['data_format'] in ['clm','dlm']:
            if form['data_format'] == 'clm':
                file_extension = '.txt'
            else:
                file_extension = '.dat'
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment;filename=%s%s' % (file_name,file_extension)
            CsvWriter = WRCCClasses.CsvWriter(req, f=None, response=response)
            CsvWriter.write_to_file()
            return response
        if form['data_format'] in ['xl']:
            file_extension = '.xls'
            response = HttpResponse(content_type='application/vnd.ms-excel;charset=UTF-8')
            ExcelWriter = WRCCClasses.ExcelWriter(req,response=response)
            ExcelWriter.write_to_file()
            response['Content-Disposition'] = 'attachment;filename=%s%s' % (file_name, file_extension)
            return response

    if request.method == 'GET' and 'projection' in request.GET:
        '''
        Link from projection page
            override some options
        '''
        new_init = {
            'area_type':'location',
            'location':'-119,39',
            'grid':'22'
        }
        initial = DJANGOUtils.set_initial(new_init, app_name)
        context['initial'] = initial
        return render_to_response(url, context, context_instance=RequestContext(request))

    #MAIN APP
    initial = DJANGOUtils.set_initial(request,app_name)
    context['initial'] = initial
    if 'formData' in request.POST or (request.method == 'GET' and 'variable' in request.GET):
        form = DJANGOUtils.set_form(initial,clean = False)
        form_cleaned = DJANGOUtils.set_form(initial,clean = True)
        variable_short = WRCCUtils.variables_to_table_headers(form['variable'],form['units'])[0]
        results = {
            'data_indices':[0],
            'variable_short':variable_short,
            'data':[],
            'error':''
        }
        #Data request
        year_data, hc_data = WRCCUtils.get_single_seasonal_summary_data(form_cleaned)
        context['run_done'] = True
        header_keys = WRCCUtils.set_display_keys(app_name, form)
        context['params_display_list'] = WRCCUtils.form_to_display_list(header_keys,form)
        if not year_data:
            context['results'] = results
            return render_to_response(url, context, context_instance=RequestContext(request))
        results['data'] = year_data
        #Set up graph data
        GDWriter = WRCCClasses.GraphDictWriter(form_cleaned, hc_data)
        graph_dict = GDWriter.write_dict()
        results['graph_data'] = [graph_dict]
        #results['chartType'] = graph_dict['chartType']
        context['results'] = results

        #Save results for downloading
        json_dict = {
            'smry':[],
            #'params_display_list':context['params_display_list']
            'form':form_cleaned,
            'data':[results['data']]
        }
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        json_file = '%s_yearly_summaries.json' %(time_stamp)
        WRCCUtils.load_data_to_json_file(settings.TEMP_DIR +json_file, json_dict)
        context['json_file'] = json_file

    return render_to_response(url, context, context_instance=RequestContext(request))

def multi_lister(request):
    app_name = 'multi_lister'
    url = settings.APPLICATIONS[app_name][2]
    app_url = settings.APPLICATIONS[app_name][1]
    context = {
        'title': settings.APPLICATIONS[app_name][0],
        'app_name':app_name,
        'app_url': app_url
    }
    #Overlay maps
    if 'formOverlay' in request.POST:
        initial = DJANGOUtils.set_initial(request,'map_overlay')
        #AJAX
        kml_file_path = DJANGOUtils.create_kml_file(initial['area_type'], initial['overlay_state'])
        if kml_file_path[0:5] == 'ERROR':
            response_data = json.dumps({'overlay_error':kml_file_path})
        else:
            response_data = json.dumps({'kml_file_path':kml_file_path})
        response = set_ajax_response(response_data)
        return response

    if 'formLargeRequest' in request.POST:
        form_cleaned = DJANGOUtils.set_form(request,clean=True)
        form_error = check_form(form_cleaned, ['user_email'])
        response_data = json.dumps({'no_form_error':'True'})
        if form_error:
            response_data = json.dumps({'form_error':'Please enter a valid email address and resubmit!'})
        else:
            #Process request offline
            json_file = form_cleaned['output_file_name'] + settings.PARAMS_FILE_EXTENSION
            WRCCUtils.load_data_to_json_file(settings.DATA_REQUEST_BASE_DIR +json_file, form_cleaned)
        response = set_ajax_response(response_data)
        return response

    if 'formDownload' in request.POST:
        form = DJANGOUtils.set_form(request,clean=False)
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        file_name = form['output_file_name'] + '_' + time_stamp
        json_file = request.POST.get('json_file', None)
        with open(settings.TEMP_DIR + json_file, 'r') as f:
            req =  json.load(f)
        #Override data_format, delimiter, output_file
        req['form']['data_format'] = form['data_format']
        req['form']['delimiter'] = form['delimiter']
        req['form']['output_file_name'] = form['output_file_name']

        if form['data_format'] in ['clm','dlm']:
            if form['data_format'] == 'clm':file_extension = '.txt'
            else:file_extension = '.dat'
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment;filename=%s%s' % (file_name,file_extension)
            if form['output_format'] == 'verbose':
                CsvWriter = WRCCClasses.CsvWriter(req, f=None, response=response)
            else:
                CsvWriter = WRCCClasses.CsvWriterNew(req, f=None, response=response)
            CsvWriter.write_to_file()
            return response
        if form['data_format'] in ['xl']:
            file_extension = '.xls'
            response = HttpResponse(content_type='application/vnd.ms-excel;charset=UTF-8')
            #WRCCUtils.write_to_excel(response,req)
            if form['output_format'] == 'verbose':
                ExcelWriter = WRCCClasses.ExcelWriter(req,response=response)
            else:
                ExcelWriter = WRCCClasses.ExcelWriterNew(req,response=response)
            ExcelWriter.write_to_file()
            response['Content-Disposition'] = 'attachment;filename=%s%s' % (file_name, file_extension)
            return response

    if request.method == 'GET' and 'projection' in request.GET:
        '''
        Link from projection page
            override some options
        '''
        new_init = {
            'data_type':'grid',
            'grid':'22'
        }
        initial = DJANGOUtils.set_initial(new_init, app_name)
        context['initial'] = initial
        return render_to_response(url, context, context_instance=RequestContext(request))

    #MAIN APP
    initial = DJANGOUtils.set_initial(request,app_name)
    context['initial'] = initial
    context['need_overlay_map'] = False
    if 'formData' in request.POST or (request.method == 'GET' and 'variables' in request.GET):
        initial = DJANGOUtils.set_initial(request,app_name)
        context['initial'] = initial
        form = DJANGOUtils.set_form(initial,clean=False)
        form_cleaned = DJANGOUtils.set_form(initial)
        #Check for form errors
        fields_to_check = [form_cleaned['area_type'],'start_date', 'end_date','degree_days']
        form_error = check_form(form_cleaned, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            return render_to_response(url, context, context_instance=RequestContext(request))

        #Deal with large requests
        num_points, num_days = WRCCUtils.check_request_size(form_cleaned)
        large_request =  WRCCUtils.check_if_large_request(num_points, num_days)
        #large_request = True
        if large_request:
            #check if we need extra download form field
            if form_cleaned['data_format'] == 'html':
                context['show_extra_download_fields'] = True
            context['large_request'] = True
            return render_to_response(url, context, context_instance=RequestContext(request))

        #Small Data request
        req = {}
        if 'locations' in form_cleaned.keys():
            req =  WRCCUtils.request_and_format_multiple_gridpoints(form_cleaned)
        else:
            req = WRCCUtils.request_and_format_data(form_cleaned)
        context['results'] = req
        context['run_done'] = True
        #Format Data for display and/or download
        header_keys = WRCCUtils.set_display_keys(app_name, form_cleaned)
        context['params_display_list'] = WRCCUtils.form_to_display_list(header_keys,form)
        #Write data to file if requested
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        file_name = form_cleaned['output_file_name'] + '_' + time_stamp
        #Deal with different data formats
        if form_cleaned['data_format'] in ['clm','dlm'] and (req['data'] or req['smry']):
            if form_cleaned['data_format'] == 'clm':
                file_extension = '.txt'
            else:
                file_extension = '.dat'
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment;filename=%s%s' % (file_name,file_extension)
            if form['output_format'] == 'verbose':
                CsvWriter = WRCCClasses.CsvWriter(req, f=None, response=response)
            else:
                CsvWriter = WRCCClasses.CsvWriterNew(req, f=None, response=response)
            CsvWriter.write_to_file()
            return response
        if form_cleaned['data_format'] in ['xl'] and (req['data'] or req['smry']):
            file_extension = '.xls'
            response = HttpResponse(content_type='application/vnd.ms-excel;charset=UTF-8')
            if form['output_format'] == 'verbose':
                ExcelWriter = WRCCClasses.ExcelWriter(req,response=response)
            else:
                ExcelWriter = WRCCClasses.ExcelWriterNew(req,response=response)
            ExcelWriter.write_to_file()
            response['Content-Disposition'] = 'attachment;filename=%s%s' % (file_name, file_extension)
            return response
        #Save data for download button
        if form_cleaned['data_format'] in ['html'] and (req['data'] or req['smry']):
            results_json = json.dumps(req)
            json_file  = form['output_file_name'] + '.json'
            with open(settings.TEMP_DIR + json_file,'w+') as f:
                f.write(results_json)
            context['json_file'] = json_file
    #Shape file upload
    if 'formShapeFile' in request.POST:
        results = {}
        #initial = DJANGOUtils.set_initial(request, app_name)
        #shape_file = request.FILES.get('file')
        files = request.FILES.getlist('files')
        feature_id = request.POST['feature_id']
        '''
        #Check that file format is correct
        if str(shape_file).split('.')[-1] != 'shp':
            results['error'] = 'File should have extension .shp'
            context['results'] = results
            return render_to_response(url, context, context_instance=RequestContext(request))
        '''

        #Save shapefiles in tmp dir
        #shp_file = '/tmp/' + str(shape_file)
        shp_file = None
        for shape_file in files:
            if str(shape_file).split('.')[-1] == 'shp':
                shp_file = '/tmp/' + str(shape_file)
            with open('/tmp/' + str(shape_file),'wb+') as dest:
                for chunk in shape_file.chunks():
                    dest.write(chunk)
        if shp_file is None:
            results['error'] = 'One file must have extension .shp'
            context['results'] = results
            return render_to_response(url, context, context_instance=RequestContext(request))
        #Convert polygon coordinates to lon, lat coordinate string
        poly_ll = WRCCUtils.shapefile_to_ll(app_name, shp_file, feature_id)
        if poly_ll is '':
            results['error'] = 'Uploaded file is not a valid shape file or feature ID does not exists.'
            #form_error = [WRCCData.DISPLAY_PARAMS['shape'],'Only polygons without holes are supported']
            context['results'] = results
            return render_to_response(url, context, context_instance=RequestContext(request))
        #Override shape parameters in initial
        initial['area_type'] = 'shape'
        initial['shape'] = poly_ll
        initial['area_type_value'] = poly_ll
        initial['area_type_lable'] = 'Custom Shape'
        context['initial'] = initial
        context['need_polygon_map'] = True
        return render_to_response(url, context, context_instance=RequestContext(request))

    return render_to_response(url, context, context_instance=RequestContext(request))

def temporal_summary(request):
    app_name = 'temporal_summary'
    url = settings.APPLICATIONS[app_name][2]
    app_url = settings.APPLICATIONS[app_name][1]
    context = {
        'title': settings.APPLICATIONS[app_name][0],
        'app_name':app_name,
        'app_url': app_url,
        'need_bbox_map':False
    }
    json_file = request.GET.get('json_file', None)
    #Check if we are coming in from other page, e.g. Gridded Data
    #Set initial accordingly
    if json_file is not None:
        json_data = WRCCUtils.load_json_data_from_file(settings.TEMP_DIR + json_file)
        if not json_data or not 'search_params' in json_data.keys():
            initial = DJANGOUtils.set_initial(request,app_name)
        else:
            initial = DJANGOUtils.set_initial(json_data['search_params'],app_name)
    else:
        initial = DJANGOUtils.set_initial(request,app_name)
    #Plot Options
    initial_plot = DJANGOUtils.set_map_plot_options(request)
    join_initials(initial, initial_plot)
    context['initial'] = initial
    if initial['area_type'] == 'bounding_box':
        context['need_bbox_map'] = True
    #Link from other page
    if request.method == 'GET' and 'variables' in request.GET:
        form_cleaned = DJANGOUtils.set_form(request,clean=True)
        form = DJANGOUtils.set_form(request,clean=False)
        header_keys = WRCCUtils.set_display_keys(app_name, form_cleaned)
        context['params_display_list'] = WRCCUtils.form_to_display_list(header_keys,form)

    if 'formMap' in request.POST:
        context['need_bbox_map'] = False
        form = DJANGOUtils.set_initial(request, app_name)
        #form = DJANGOUtils.set_form(request, clean=False)
        form_cleaned = DJANGOUtils.set_form(request)
        #Set initials
        initial = DJANGOUtils.set_initial(form, app_name)
        initial_plot = DJANGOUtils.set_map_plot_options(form)
        join_initials(initial, initial_plot)
        context['initial'] = initial
        header_keys = WRCCUtils.set_display_keys(app_name, form_cleaned)
        context['params_display_list'] = WRCCUtils.form_to_display_list(header_keys,form)

        #Back Button/download files issue fix:
        if not 'area_type' in form.keys():
            for key in WRCCData.SEARCH_AREA_FORM_TO_ACIS.keys():
                if key in form.keys():
                    form['area_type'] = key
                    break

        #Form Check
        fields_to_check = ['start_date', 'end_date','degree_days', 'cmap', form['area_type'], 'variables']
        #fields_to_check = ['start_date', 'end_date','degree_days',form['area_type'], 'variables']
        form_error = check_form(form_cleaned, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            return render_to_response(url, context, context_instance=RequestContext(request))

        #Generate Maps
        figure_files = []
        image = {
            'type':'png',
            'proj':form['projection'],
            'interp':form['interpolation'],
            'overlays':[form['map_ol'], 'county:0.5:black'],
            'cmap':form['cmap'],
            'width':WRCCData.IMAGE_SIZES_MAP[form['image_size']]
        }
        params = {
            'image':image,
            'output':'json',
            'area_type':WRCCData.SEARCH_AREA_FORM_TO_ACIS[form['area_type']],
            WRCCData.SEARCH_AREA_FORM_TO_ACIS[form['area_type']]:form[form['area_type']],
            'grid': form['grid'],
            'sdate':form['start_date'],
            'edate':form['end_date'],
            'units':form['units'],
            'level_number':form['level_number'],
            'temporal_summary':form['temporal_summary'],
            'elems':[]
            }
        for el_idx,variable in enumerate(form_cleaned['variables']):
            pms = copy.deepcopy(params)
            a_el_dict = {
                'name':variable,
                'smry':form_cleaned['temporal_summary'],
                'smry_only':1
            }
            if pms['units'] == 'metric':
                if variable in ['pcpn','snow','snwd']:
                    a_el_dict['units'] = 'mm'
                else:
                    a_el_dict['units'] = 'degreeC'
            pms['elems'] = [a_el_dict]
            fig = WRCCClasses.GridFigure(pms)
            result = fig.get_grid()
            time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
            figure_file = 'clim_sum_map_' + time_stamp + '.png'
            file_path_big =settings.TEMP_DIR + figure_file
            fig.build_figure(result, file_path_big)
            figure_files.append(figure_file)
        context['JSON_URL'] = settings.TMP_URL
        context['figure_files'] = figure_files
        context['run_done'] = True
        context['results'] = True
    return render_to_response(url, context, context_instance=RequestContext(request))

def monthly_spatial_summary(request):
    app_name = 'monthly_spatial_summary'
    url = settings.APPLICATIONS[app_name][2]
    app_url = settings.APPLICATIONS[app_name][1]
    context = {
        'title': settings.APPLICATIONS[app_name][0],
        'app_name':app_name,
        'app_url': app_url
    }
    initial  = DJANGOUtils.set_initial(request,app_name)
    context['initial'] = initial

    if 'formData' in request.POST or (request.method == 'GET' and 'variable' in request.GET):
        #Set form and initial
        form = DJANGOUtils.set_form(initial, clean=False)
        form_cleaned = DJANGOUtils.set_form(initial)
        #Form Check
        fields_to_check = []
        form_error = check_form(form_cleaned, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            return render_to_response(url, context, context_instance=RequestContext(request))

        #Display parameters
        header_keys = WRCCUtils.set_display_keys(app_name, form_cleaned)
        context['params_display_list'] = WRCCUtils.form_to_display_list(header_keys,form)
        results = WRCCUtils.monthly_spatial_summary(form_cleaned)
        context['results'] = results
        '''
        #AJAX
        if form_error:
            response_data = json.dumps({'form_error':form_error})
            response = set_ajax_response(response_data)
            return response
        header_keys = WRCCUtils.set_display_keys(app_name, form_cleaned)
        params_display_list = WRCCUtils.form_to_display_list(header_keys,form)
        results = WRCCUtils.monthly_spatial_summary(form_cleaned)
        response_data = json.dumps({
            'params_display_list':params_display_list,
            'results':results
        })
        response = set_ajax_response(response_data)
        return response
        '''
    return render_to_response(url, context, context_instance=RequestContext(request))


def spatial_summary(request):
    app_name = 'spatial_summary'
    url = settings.APPLICATIONS[app_name][2]
    app_url = settings.APPLICATIONS[app_name][1]
    context = {
        'title': settings.APPLICATIONS[app_name][0],
        'app_name':app_name,
        'app_url': app_url
    }
    #Overlay maps
    if 'formOverlay' in request.POST:
        initial = DJANGOUtils.set_initial(request,'map_overlay')
        #AJAX
        kml_file_path = DJANGOUtils.create_kml_file(initial['area_type'], initial['overlay_state'])
        if kml_file_path[0:5] == 'ERROR':
            response_data = json.dumps({'overlay_error':kml_file_path})
        else:
            response_data = json.dumps({'kml_file_path':kml_file_path})
        response = set_ajax_response(response_data)
        return response

    #Download button pressed
    if 'formDownload' in request.POST:
        form = DJANGOUtils.set_form(request,clean=False)
        json_file = request.POST.get('json_file', None)
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        file_name = form['output_file_name'] + '_' + time_stamp
        with open(settings.TEMP_DIR + json_file, 'r') as f:
            req =  json.load(f)
        #Override data_format, delimiter, output_file
        req['form']['data_format'] = form['data_format']
        req['form']['delimiter'] = form['delimiter']
        req['form']['output_file_name'] = form['output_file_name']
        if form['data_format'] in ['clm','dlm']:
            if form['data_format'] == 'clm':
                file_extension = '.txt'
            else:
                file_extension = '.dat'
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment;filename=%s%s' % (file_name,file_extension)
            CsvWriter = WRCCClasses.CsvWriter(req, f=None, response=response)
            CsvWriter.write_to_file()
            return response
        if form['data_format'] in ['xl']:
            file_extension = '.xls'
            response = HttpResponse(content_type='application/vnd.ms-excel;charset=UTF-8')
            #WRCCUtils.write_to_excel(response,req)
            ExcelWriter = WRCCClasses.ExcelWriter(req,response=response)
            ExcelWriter.write_to_file()
            response['Content-Disposition'] = 'attachment;filename=%s%s' % (file_name, file_extension)
            return response
    if 'formLargeRequest' in request.POST:
        form_cleaned = DJANGOUtils.set_form(request,clean=True)
        form_error = check_form(form_cleaned, ['user_email'])
        response_data = json.dumps({'no_form_error':'True'})
        if form_error:
            response_data = json.dumps({'form_error':'Please enter a valid email address and resubmit!'})
        else:
            #Process request offline
            json_file = form_cleaned['output_file_name'] + settings.PARAMS_FILE_EXTENSION
            WRCCUtils.load_data_to_json_file(settings.DATA_REQUEST_BASE_DIR +json_file, form_cleaned)
        response = set_ajax_response(response_data)
        return response

    if request.method == 'GET' and 'projection' in request.GET:
        '''
        Link from projection page
            override some options
        '''
        new_init = {
            'data_type':'grid',
            'grid':'22'
        }
        initial = DJANGOUtils.set_initial(new_init, app_name)
        context['initial'] = initial
        return render_to_response(url, context, context_instance=RequestContext(request))

    #MAIN APP
    initial  = DJANGOUtils.set_initial(request,app_name)
    context['initial'] = initial
    if 'formData' in request.POST or (request.method == 'GET' and 'variables' in request.GET):
        #Set form and initial
        form = DJANGOUtils.set_form(initial, clean=False)
        form_cleaned = DJANGOUtils.set_form(initial)
        #context['xx'] = form_cleaned
        #Form Check
        fields_to_check = [form['area_type'],'start_date', 'end_date','degree_days', 'variables']
        #,'connector_line_width', 'vertical_axis_min', 'vertical_axis_max']
        form_error = check_form(form_cleaned, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            return render_to_response(url, context, context_instance=RequestContext(request))

        #Display parameters
        header_keys = WRCCUtils.set_display_keys(app_name, form_cleaned)
        context['params_display_list'] = WRCCUtils.form_to_display_list(header_keys,form)

        #Data Request
        #Skip data generation of it has already been performed
        results = {}
        json_file = request.GET.get('json_file', None)
        if json_file is not None:
            context['json_file'] =json_file
            context['JSON_URL'] = settings.TEMP_DIR
            with open(settings.TEMP_DIR + json_file, 'r') as f:
                try:
                    req = WRCCUtils.u_convert(json.loads(f.read()))
                    if not 'smry' in req.keys() or not req['smry']:
                        results['error'] = 'No data found in file %s' %json_file
                        context['results'] = results
                        return render_to_response(url, context, context_instance=RequestContext(request))
                except Exception, e:
                    results['error'] = 'Error when reading %s: %s' (json_file, str(e))
                    context['results'] = results
                    return render_to_response(url, context, context_instance=RequestContext(request))
        #Get Data
        #Check for large requests
        #Greater than 2 years not allowed
        if int(form['end_date'][0:4]) - int(form['start_date'][0:4]) > 2:
            context['show_extra_download_fields']  = True
            context['large_request'] = True
            '''
            results['error'] = 'This request is too large. Please limit your analysis to 5 years or less!'
            context['results'] = results
            '''
            return render_to_response(url, context, context_instance=RequestContext(request))
        '''
        try:
            req = WRCCUtils.request_and_format_data(form_cleaned)
            if 'smry' not in req.keys() or not req['smry']:
                results['error'] = 'No data found for these parameters!'
                context['results'] = results
                return render_to_response(url, context, context_instance=RequestContext(request))
        except Exception, e:
            results['error'] = 'Data request error: %s' %str(e)
            context['results'] = results
            return render_to_response(url, context, context_instance=RequestContext(request))
        '''
        if 'locations' in form_cleaned.keys():
            req = WRCCUtils.request_and_format_multiple_gridpoints(form_cleaned)
        else:
            req = WRCCUtils.request_and_format_data(form_cleaned)
        if not req['smry'] and req['data']:
            results['smry'] = req['data']
        else:
            results['smry'] = req['smry']
        #Save to json file for downloading

        #format data for highcarts
        graph_data = []
        for el_idx, variable in enumerate(form_cleaned['variables']):
            el_data = WRCCUtils.extract_highcarts_data_spatial_summary(req['smry'],el_idx, variable,form_cleaned)
            GraphDictWriter = WRCCClasses.GraphDictWriter(form_cleaned, el_data, variable = variable)
            datadict = GraphDictWriter.write_dict()
            graph_data.append(datadict)

        results['graph_data'] = graph_data

        variables = []
        for el in form_cleaned['variables']:
            el_strip, base_temp = WRCCUtils.get_el_and_base_temp(el)
            el_name = WRCCData.ACIS_ELEMENTS_DICT[el_strip]['name_long']
            if base_temp is not None:
                el_name+= str(base_temp)
            variables.append(el_name)
        results['variables'] = variables
        #Pick up chart indices from previous run
        chart_indices_list = str(initial['chart_indices_string']).split(',')
        #Check that these indices exist in new run
        chart_indices = []
        for idx in chart_indices_list:
            if idx < len(graph_data) and initial['chart_variables'][int(idx)] in form_cleaned['variables']:
                new_idx = form_cleaned['variables'].index(initial['chart_variables'][int(idx)])
                chart_indices.append(new_idx)
        if not chart_indices:
            chart_indices = [idx for idx in range(len(form_cleaned['variables']))]
        results['chart_indices'] = chart_indices
        context['results'] = results
        context['run_done'] = True
        #Save results for downloading
        json_dict = {
            'smry':results['smry'],
            #'params_display_list':context['params_display_list']
            'form':form_cleaned,
            'data':[]
        }
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        json_file = '%s_%s.json' %(time_stamp, app_name)
        WRCCUtils.load_data_to_json_file(settings.TEMP_DIR +json_file, json_dict)
        context['json_file'] = json_file

    #Shape file upload
    if 'formShapeFile' in request.POST:
        results = {}
        #initial = DJANGOUtils.set_initial(request, app_name)
        #shape_file = request.FILES.get('file')
        files = request.FILES.getlist('files')
        feature_id = request.POST['feature_id']
        '''
        #Check that file format is correct
        if str(shape_file).split('.')[-1] != 'shp':
            results['error'] = 'File should have extension .shp'
            context['results'] = results
            return render_to_response(url, context, context_instance=RequestContext(request))
        '''

        #Save shapefiles in tmp dir
        #shp_file = '/tmp/' + str(shape_file)
        shp_file = None
        for shape_file in files:
            if str(shape_file).split('.')[-1] == 'shp':
                shp_file = '/tmp/' + str(shape_file)
            with open('/tmp/' + str(shape_file),'wb+') as dest:
                for chunk in shape_file.chunks():
                    dest.write(chunk)
        if shp_file is None:
            results['error'] = 'One file must have extension .shp'
            context['results'] = results
            return render_to_response(url, context, context_instance=RequestContext(request))
        #Convert polygon coordinates to lon, lat coordinate string
        poly_ll = WRCCUtils.shapefile_to_ll(app_name, shp_file, feature_id)
        if poly_ll is '':
            results['error'] = 'Uploaded file is not a valid shape file or feature ID does not exists.'
            #form_error = [WRCCData.DISPLAY_PARAMS['shape'],'Only polygons without holes are supported']
            context['results'] = results
            return render_to_response(url, context, context_instance=RequestContext(request))
        #Override shape parameters in initial
        initial['area_type'] = 'shape'
        initial['shape'] = poly_ll
        initial['area_type_value'] = poly_ll
        initial['area_type_lable'] = 'Custom Shape'
        context['initial'] = initial
        context['need_polygon_map'] = True
        return render_to_response(url, context, context_instance=RequestContext(request))

    return render_to_response(url, context, context_instance=RequestContext(request))


def climate_engine(request):
    app_name = 'climate_engine'
    context = {
        'title': '',
        'app_name':app_name
    }
    context['initial'] = {'app_name':app_name}
    return render_to_response('scenic/data/climate_engine.html', context, context_instance=RequestContext(request))


def station_finder(request):
    app_name = 'station_finder'
    url = settings.APPLICATIONS[app_name][2]
    app_url = settings.APPLICATIONS[app_name][1]
    context = {
        'title': settings.APPLICATIONS[app_name][0],
        'app_name':app_name,
        'app_url': app_url
    }
    context['run_done'] = False
    context['need_overlay_map'] = False
    context['need_polygon_map'] = False

    if 'station_id_change' in request.POST:
        response_data = find_station_vd(request)
        response = set_ajax_response(response_data)
        return response

    #Overlay maps
    if 'formOverlay' in request.POST:
        initial = DJANGOUtils.set_initial(request,'map_overlay')
        #AJAX
        kml_file_path = DJANGOUtils.create_kml_file(initial['area_type'], initial['overlay_state'])
        if kml_file_path[0:5] == 'ERROR':
            response_data = json.dumps({'overlay_error':kml_file_path})
        else:
            response_data = json.dumps({'kml_file_path':kml_file_path})
        response = set_ajax_response(response_data)
        return response

    #Download data for all sations displayed
    #Request will be processed offline
    if 'formDownload' in request.POST:
        initial = DJANGOUtils.set_initial(request,'sf_download')
        form_cleaned = DJANGOUtils.set_form(initial, clean=True)
        fields_to_check = ['user_email']
        form_error = check_form(form_cleaned, fields_to_check)
        if form_error:
            response_data = json.dumps({'form_error_download':'Not a valid email address!'})
        else:
            response_data = json.dumps({'large_request':'True'})
        #Submit large request
        json_dict = copy.deepcopy(form_cleaned)
        json_file = form_cleaned['output_file_name'] + settings.PARAMS_FILE_EXTENSION
        WRCCUtils.load_data_to_json_file(settings.DATA_REQUEST_BASE_DIR +json_file, json_dict)
        response = set_ajax_response(response_data)
        return response

    #Set initial
    from subprocess import call
    call(["touch", settings.TEMP_DIR + "Empty.json"])
    #Set up initial map (NV stations)
    initial = DJANGOUtils.set_initial(request, app_name)
    context['initial'] = initial

    #Set up maps if needed
    if request.method == "GET" and not 'variables' in request.GET and not 'station_id' in request.GET:
        #Generate initial map
        by_type = 'state'; val = 'nv'
        date_range = [initial['start_date'],initial['end_date']]
        el_date_constraints = initial['variables_constraints'] + '_' + initial['dates_constraints']
        station_json, f_name = AcisWS.station_meta_to_json(by_type, val, el_list=['1','2','4'],time_range=date_range, constraints=el_date_constraints)
        #Write json file for link to data lister
        json_dict = copy.deepcopy(initial)
        #Need to get stations IDS for data download
        json_dict['station_ids'] = WRCCUtils.get_station_ids('/tmp/' + f_name)
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        json_file_name = '%s_%s_params.json' %(time_stamp,app_name)
        WRCCUtils.load_data_to_json_file(settings.TEMP_DIR + json_file_name, json_dict)
        context['params_json'] = json_file_name
        if 'error' in station_json.keys():
            results = {'error':station_json['error']}
            context['results'] = results
        if 'stations' not in station_json.keys() or  station_json['stations'] == []:
            context['results'] = {'error':'No stations found for these search parameters.'}
        if 'stations' in station_json.keys() and station_json['stations']:
            context['results'] = {'station_json':f_name}
        header_keys = WRCCUtils.set_display_keys(app_name, initial)
        context['params_display_list'] = WRCCUtils.form_to_display_list(header_keys,initial)

    if 'formData' in request.POST or (request.method == 'GET' and 'variables' in request.GET):
        #Turn request object into python dict
        form = DJANGOUtils.set_form(request,clean=False)
        form_cleaned = DJANGOUtils.set_form(request,clean=True)
        fields_to_check = [form_cleaned['area_type'],'start_date', 'end_date']
        context['xx'] = form_cleaned
        #form_error = check_form(form_cleaned, fields_to_check)
        form_error = None
        if form_error:
            context['form_error'] = form_error
            return render_to_response(url, context, context_instance=RequestContext(request))
        #Convert variable list to var majors
        el_vX_list = []
        for el_idx, variable in enumerate(form_cleaned['variables']):
            el,base_temp = WRCCUtils.get_el_and_base_temp(variable)
            if variable in ['pet','dtr']:
                el_vX_list.append('1')
                el_vX_list.append('2')
            else:
                el_vX_list.append(str(WRCCData.ACIS_ELEMENTS_DICT[el]['vX']))
        #Make unique
        el_vX_list = list(set(el_vX_list))
        #Set up params for station_json generation
        by_type = WRCCData.ACIS_TO_SEARCH_AREA[form_cleaned['area_type']]
        val = form_cleaned[by_type]
        date_range = [form_cleaned['start_date'],form_cleaned['end_date']]
        el_date_constraints = form_cleaned['variables_constraints'] + '_' + form_cleaned['dates_constraints']
        station_json, f_name = AcisWS.station_meta_to_json(by_type, val, el_list=el_vX_list,time_range=date_range, constraints=el_date_constraints)
        #Write to file for map generation
        station_ids = WRCCUtils.get_station_ids('/tmp/' + f_name)
        context['number_of_stations'] = len(station_ids.split(','))
        #Update hidden var that keeps track of stations
        initial['station_ids_string'] = station_ids
        context['initial'] = initial
        #Write json file for link to data lister
        json_dict = copy.deepcopy(form_cleaned)
        json_dict['station_ids'] = station_ids
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        json_file_name = '%s_%s_params.json' %(time_stamp,app_name)
        WRCCUtils.load_data_to_json_file(settings.TEMP_DIR + json_file_name, json_dict)

        if 'error' in station_json.keys():
            results = {'error':station_json['error']}
            context['results'] = results
        if 'stations' not in station_json.keys() or  station_json['stations'] == []:
            context['results'] = {'error':'No stations found for these search parameters.'}
        if 'stations' in station_json.keys() and station_json['stations']:
            context['results'] = {'station_json':f_name}
        context['run_done'] = True
        header_keys = WRCCUtils.set_display_keys(app_name, initial)
        context['params_display_list'] = WRCCUtils.form_to_display_list(header_keys,initial)
        context['form_cleaned']= form_cleaned
    #Shape file upload
    if 'formShapeFile' in request.POST:
        results = {}
        #initial = DJANGOUtils.set_initial(request, app_name)
        #shape_file = request.FILES.get('file')
        files = request.FILES.getlist('files')
        feature_id = request.POST['feature_id']

        #Save shapefiles in tmp dir
        #shp_file = '/tmp/' + str(shape_file)
        shp_file = None
        for shape_file in files:
            if str(shape_file).split('.')[-1] == 'shp':
                shp_file = '/tmp/' + str(shape_file)
            with open('/tmp/' + str(shape_file),'wb+') as dest:
                for chunk in shape_file.chunks():
                    dest.write(chunk)
        if shp_file is None:
            results['error'] = 'One file must have extension .shp'
            context['results'] = results
            return render_to_response(url, context, context_instance=RequestContext(request))
        #Convert polygon coordinates to lon, lat coordinate string
        poly_ll = WRCCUtils.shapefile_to_ll(app_name, shp_file, feature_id)
        if poly_ll is '':
            results['error'] = 'Uploaded file is not a valid shape file or feature ID does not exists.'
            #form_error = [WRCCData.DISPLAY_PARAMS['shape'],'Only polygons without holes are supported']
            context['results'] = results
            return render_to_response(url, context, context_instance=RequestContext(request))
        #Override shape parameters in initial
        initial['area_type'] = 'shape'
        initial['shape'] = poly_ll
        initial['area_type_value'] = poly_ll
        initial['area_type_lable'] = 'Custom Shape'
        context['initial'] = initial
        context['need_polygon_map'] = True
        return render_to_response(url, context, context_instance=RequestContext(request))

    return render_to_response(url, context, context_instance=RequestContext(request))


def data_comparison(request):
    app_name = 'data_comparison'
    url = settings.APPLICATIONS[app_name][2]
    app_url = settings.APPLICATIONS[app_name][1]
    context = {
        'title': settings.APPLICATIONS[app_name][0],
        'app_name':app_name,
        'app_url': app_url
    }
    initial = DJANGOUtils.set_initial(request,'data_comparison')
    context['initial'] = initial
    context['need_gridpoint_map'] = True

    if request.method == 'GET' and 'projection' in request.GET:
        '''
        Link from projection page
            override some options
        '''
        new_init = {
            'area_type':'location',
            'location':'-119,39',
            'grid':'22'
        }
        initial = DJANGOUtils.set_initial(new_init, app_name)
        context['initial'] = initial
        return render_to_response(url, context, context_instance=RequestContext(request))

    if 'formData' in request.POST or (request.method == 'GET' and ('station_id' in request.GET or 'location' in request.GET)):
        context['form_message'] = True
        form = DJANGOUtils.set_form(initial, clean=False)
        form['app_name'] = 'data_comparison'
        form_cleaned = DJANGOUtils.set_form(initial, clean=True)
        form_cleaned['app_name'] = 'data_comparison'
        DC = WRCCClasses.DataComparer(form)
        gdata,sdata,dist = DC.get_data()
        context['run_done'] = True
        results = {
            'grid_data':gdata,
            'station_data':sdata,
            'distance':dist
        }
        results['graph_data'] = DC.get_graph_data(gdata,sdata)
        context['need_gridpoint_map'] = False
        results['stats'] = DC.get_statistics(results['graph_data'][0],results['graph_data'][1])
        context['results'] = results
        header_keys = WRCCUtils.set_display_keys(app_name, form_cleaned)
        context['params_display_list'] = WRCCUtils.form_to_display_list(header_keys,form)
    return render_to_response(url, context, context_instance=RequestContext(request))

#######################
#SOD programs
######################

def monthly_summary(request):
    app_name = 'monthly_summary'
    url = settings.APPLICATIONS[app_name][2]
    app_url = settings.APPLICATIONS[app_name][1]
    context = {
        'title': settings.APPLICATIONS[app_name][0],
        'app_name':app_name,
        'app_url': app_url
    }
    initial = DJANGOUtils.set_initial(request, app_name)
    context['initial'] = initial

    if 'station_id_change' in request.POST:
        response_data = find_station_vd(request)
        response = set_ajax_response(response_data)
        return response

    if request.method == 'GET' and 'projection' in request.GET:
        '''
        Link from projection page
            override some options
        '''
        new_init = {
            'area_type':'location',
            'location':'-119,39',
            'grid':'22'
        }
        initial = DJANGOUtils.set_initial(new_init, app_name)
        context['initial'] = initial
        return render_to_response(url, context, context_instance=RequestContext(request))

    if 'formData' in request.POST or (request.method == 'GET' and 'variable' in request.GET):
        form = DJANGOUtils.set_form(initial,clean=False)
        form_cleaned = DJANGOUtils.set_form(initial,clean=True)
        #Form sanity check
        fields_to_check = ['start_year', 'end_year','max_missing_days']
        form_error = check_form(form_cleaned, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            return render_to_response(url, context, context_instance=RequestContext(request))
        #Set data job params
        data_params = {
            'start_date':form_cleaned['start_year'],
            'end_date':form_cleaned['end_year'],
            'variable':form_cleaned['variable']
        }
        if 'location' in form_cleaned.keys():
            data_params['location'] = form_cleaned['location']
            data_params['grid'] = form_cleaned['grid']
        if 'station_id' in form_cleaned.keys():
            data_params['sid'] = form_cleaned['station_id']
        #Set and format app params
        app_params = copy.deepcopy(form_cleaned)
        if app_params['less_greater_or_between'] == 'l':
            app_params['threshold_for_less_or_greater'] = app_params['threshold_for_less_than']
        if app_params['less_greater_or_between'] == 'g':
            app_params['threshold_for_less_or_greater'] = app_params['threshold_for_greater_than']
        for key in ['location','station_id', 'start_year', 'end_year','threshold_for_less_than','threshold_for_greater_than']:
            try:del app_params[key]
            except:pass
        #Run data retrieval job
        DJ = WRCCClasses.SODDataJob('Sodxtrmts', data_params)
        #Obtain metadata and data
        if 'station_id' in form_cleaned.keys():
            meta_dict = DJ.get_station_meta()
            data = DJ.get_data_station()
        if 'location' in form_cleaned.keys():
            meta_dict = DJ.get_grid_meta()
            data = DJ.get_data_grid()
        #Set dates list
        dates_list = DJ.get_dates_list()
        #Run application
        App = WRCCClasses.SODApplication('SodxtrmtsSCENIC', data, app_specific_params=app_params)
        data = App.run_app()
        #Set header
        dataTableInfo = ''
        header = set_sodxtrmts_head(form_cleaned)
        for head in header:
            dataTableInfo+=head[0] + ': '+ head[1] + '\n'
        if not data or len(data[0]) <=1:
            results = {
                'header':[],
                'dataTableInfo':'',
                'data':[],
                'data_summary':[],
                'errors': 'No Data found for these parameters'
            }
            context['results'] = results
            return render_to_response(url, context, context_instance=RequestContext(request))
        else:
            header_list = []
            dataTableInfo = ''
            if app_params['statistic_period'] == 'monthly':
                p =  copy.deepcopy(WRCCData.MONTH_NAMES_LETTER)
            if app_params['statistic_period'] == 'weekly':
                p = range(1,53)
                context['weeks'] = copy.deepcopy(p)
            for m in p:
                header_list.append(str(m))
                #space for data flag slots
                header_list.append('F')

            results = {
                'header':header,
                'dataTableInfo':dataTableInfo,
                'chart_indices':'0',
                'smry':'individual',
                'variable':data_params['variable'],
                'running_mean_years':'5',
                'show_range': False,
                'data': [['Yr'] + header_list + ['An', 'F']] + data[0][0:-6],
                'data_summary':[[' '] + header_list + ['An', ' ']] + data[0][-6:]
            }
        #Write data to file for highcharts
        hc_data = WRCCUtils.extract_highcarts_data_monthly_summary(results['data'],form_cleaned)
        graph_data = []
        for p_idx,d in enumerate(hc_data):
            if app_params['statistic_period'] == 'monthly':
                sname = WRCCData.MONTH_NAMES_SHORT_CAP[p_idx]
            if app_params['statistic_period'] == 'weekly':
                sname = 'Week ' + str(p[p_idx])
            GDWriter = WRCCClasses.GraphDictWriter(form_cleaned, d, name=sname)
            graph_dict = GDWriter.write_dict()
            #Add additional initial plot options
            #1. chart layers
            graph_data.append(graph_dict)
        results['graph_data'] = graph_data
        #results['chartType'] = graph_dict['chartType']
        context['run_done'] = True
        context['results'] = results
        #Save data table to file for later download
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        json_file = '%s_%s.json' %(time_stamp, app_name)
        with open(settings.TEMP_DIR + '%s' %(json_file),'w+') as f:
            f.write(json.dumps(results))
        context['json_file'] = json_file

    #Downlaod Table Data
    if 'formDownload' in request.POST:
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        data_format = request.POST.get('data_format', 'clm')
        delimiter = request.POST.get('delimiter', 'comma')
        output_file_name = request.POST.get('output_file_name', 'output')
        output_file_name = output_file_name + '_' + time_stamp
        json_file = request.POST.get('json_file', None)
        with open(settings.TEMP_DIR + json_file, 'r') as f:
            results =  json.load(f)
        context['results'] = results
        DDJ = WRCCToReplace.DownloadDataJob('Sodxtrmts',data_format,delimiter, output_file_name, request=request, json_in_file=settings.TEMP_DIR + json_file)
        return DDJ.write_to_file()

    return render_to_response(url, context, context_instance=RequestContext(request))


def climatology(request):
    app_name = 'climatology'
    url = settings.APPLICATIONS[app_name][2]
    app_url = settings.APPLICATIONS[app_name][1]
    context = {
        'title': settings.APPLICATIONS[app_name][0],
        'app_name':app_name,
        'app_url': app_url
    }
    initial= DJANGOUtils.set_initial(request, app_name)
    context['initial'] = initial

    if 'station_id_change' in request.POST:
        response_data = find_station_vd(request)
        response = set_ajax_response(response_data)
        return response

    if request.method == 'GET' and 'projection' in request.GET:
        '''
        Link from projection page
            override some options
        '''
        new_init = {
            'area_type':'location',
            'location':'-119,39',
            'grid':'22',
            'summary_type':'temp'
        }
        initial = DJANGOUtils.set_initial(new_init, app_name)
        context['initial'] = initial
        return render_to_response(url, context, context_instance=RequestContext(request))

    if 'formData' in request.POST or (request.method == 'GET' and ('station_id' in request.GET or 'location' in request.GET)):
        form = DJANGOUtils.set_form(initial,clean=False)
        form_cleaned = DJANGOUtils.set_form(initial,clean=True)
        #form = DJANGOUtils.set_form(request,clean=False)
        #form_cleaned = DJANGOUtils.set_form(request,clean=True)
        #Set up page header params
        if 'station_id' in form.keys():
            context['station_name'] = form['station_id']
        if 'location' in form.keys():
            context['grid_name'] =  WRCCData.GRID_CHOICES[initial['grid']][0]

        fields_to_check = ['start_year', 'end_year','max_missing_days']

        #Check for form errors
        form_error = check_form(form_cleaned, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            return render_to_response(url, context, context_instance=RequestContext(request))

        #Set data and app params
        data_params = {
                'start_date':form['start_year'],
                'end_date':form['end_year'],
                'variable':form['summary_type']
                }
        app_params = {
                'el_type':form['summary_type'],
                'max_missing_days':form['max_missing_days'],
                'units':form['units']
                }
        if 'location' in form_cleaned.keys():
            data_params['loc'] = form_cleaned['location']
            data_params['grid'] = form_cleaned['grid']
            app_params['loc'] = form_cleaned['location']
            app_params['grid'] = form_cleaned['grid']
        if 'station_id' in form_cleaned.keys():
            data_params['sid'], name = WRCCUtils.find_id_and_name(form['station_id'], settings.MEDIA_DIR + '/json/US_station_id.json')
        #Initialize Data Job class
        DJ = WRCCClasses.SODDataJob('Sodsumm', data_params)
        if 'location' in form_cleaned.keys():
            meta_dict = DJ.get_grid_meta()
            data = DJ.get_data_grid()
        if 'station_id' in form_cleaned.keys():
            meta_dict = DJ.get_station_meta()
            data = DJ.get_data_station()
        dates_list = DJ.get_dates_list()
        #Sanity checks
        if not meta_dict['names'] or not meta_dict['ids']:
            results = {}
            context['run_done']= True
            return render_to_response(url, context, context_instance=RequestContext(request))
        if not data or not dates_list:
            results = {}
            context['run_done']= True
            header_keys = WRCCUtils.set_display_keys(app_name, form_cleaned)
            context['params_display_list'] = WRCCUtils.form_to_display_list(header_keys,form)
            return render_to_response(url, context, context_instance=RequestContext(request))
        #Run application
        App = WRCCClasses.SODApplication('Sodsumm', data, app_specific_params=app_params)
        results = App.run_app()
        #Format results to single station output
        if not results:
            results = {}
            context['run_done']= True
            return render_to_response(url, context, context_instance=RequestContext(request))
        else:
            results = results[0]
        context['results'] = results
        #Sodsumm table headers for html
        context['tab_names'] = WRCCData.TAB_NAMES_WITH_GRAPHICS[form['summary_type']]
        tab_list = WRCCData.TAB_LIST_WITH_GRAPHICS[form['summary_type']]
        table_list =WRCCData.TABLE_LIST_WITH_GRAPHICS[form['summary_type']]
        context['table_list'] = table_list
        context['tab_list'] = tab_list
        #Define html content
        context['run_done'] = True
        #Check if dates_list exits and has correct format
        if dates_list and len(dates_list) >=2 and len(dates_list[0])>=4 and len(dates_list[1])>=4:
            context['start_year'] = dates_list[0][0:4]
            context['end_year'] = dates_list[-1][0:4]
        else:
            context['start_year'] = '0000'
            context['end_year'] = '0000'
            dates_list = ['0000','0000']
        context['station_name'] = meta_dict['names']
        headers = set_sodsumm_headers(table_list)
        context['headers'] = headers
        json_list = []
        for tab_idx, tab in enumerate(tab_list):
            table = table_list[tab_idx]
            table_dict = {}
            table_dict = generate_sodsumm_graphics(results,tab,table,form['units'])
            if not table_dict:
                results = {}
                context['run_done']= True
                return render_to_response(url, context, context_instance=RequestContext(request))
            #Add other params to table_dict
            table_dict['record_start'] = dates_list[0][0:4]
            table_dict['record_end'] = dates_list[-1][0:4]
            if 'sid' in data_params.keys():
                table_dict['title'] = meta_dict['names'][0] + ', ' +\
                    meta_dict['states'][0] + ', ' + table_dict['table_name_long']
                table_dict['subtitle'] = 'Network: ' + meta_dict['networks'][0] + ', ID: ' + str(data_params['sid'])
            if 'loc' in data_params.keys():
                table_dict['title'] = 'Location ' + str(data_params['loc']) + ', ' + table_dict['table_name_long']
                table_dict['subtitle'] = 'Grid ' + WRCCData.GRID_CHOICES[str(data_params['grid'])][0]
            json_list.append(table_dict)
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        json_file = '%s_%s_%s_%s.json' \
        %(time_stamp,app_name,dates_list[0][0:4], dates_list[-1][0:4])
        WRCCUtils.load_data_to_json_file(settings.TEMP_DIR + json_file, json_list)
        context['JSON_DIR'] = settings.TEMP_DIR
        context['json_file'] = json_file
    #Downlaod Table Data
    for table_idx in range(7):
        if 'formDownload' + str(table_idx) in request.POST:
            data_format = request.POST.get('data_format', 'clm')
            delimiter = request.POST.get('delimiter', 'comma')
            output_file_name = request.POST.get('output_file_name', 'output')
            json_file = request.POST.get('json_file', None)
            tab = request.POST.get('tab', None)
            json_data = WRCCUtils.load_json_data_from_file(settings.TEMP_DIR + json_file)
            #find the correct data set corresponding to the tab name
            for idx, data_dict in enumerate(json_data):
                if data_dict['table_name'] == tab:
                    #Overwrite json_in_file
                    json_in_file_name = json_file + '_in'
                    WRCCUtils.load_data_to_json_file(settings.TEMP_DIR + json_in_file_name, data_dict)
                    break
            DDJ = WRCCToReplace.DownloadDataJob('Sodsumm',data_format,delimiter, output_file_name, request=request, json_in_file=settings.TEMP_DIR + json_in_file_name)
            return DDJ.write_to_file()

    return render_to_response(url, context, context_instance=RequestContext(request))
##############################
#Utlities
##############################
def find_station_vd(request):
    '''
    Find valid daterange or this station
    '''
    station_id = request.POST.get('station_id')
    sid, stn_name = WRCCUtils.find_id_and_name(station_id,settings.MEDIA_DIR +'json/US_station_id.json')
    element_list = request.POST.get('el_tuple','maxt,mint,pcpn').replace(', ',',').split(',')
    mx_or_mn = request.POST.get('max_or_min','max')
    vd = WRCCUtils.find_valid_daterange(sid,el_list=element_list, max_or_min=mx_or_mn)
    r =  {
        'vd':vd,
        'station_id':station_id
    }
    response_data = json.dumps(r)
    return response_data
###########
#AJAX
###########
def set_ajax_response(response_data):
    response = HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )
    return response
###########
#General
###########
#FORM SANITY CHECKS
def check_form(form, fields_to_check):
    '''
    Sanity check for Sodxtrmst form
    form is given as dict
    Note that WRCCformCcheck function names are
    corresponding to field names
    '''
    form_error = {}
    for field in fields_to_check:
        checker = getattr(WRCCFormCheck, 'check_' + field)
        err = checker(form)
        if err:
            if field in ['start_year','end_year']:
                form_error[field] = err
            else:
                form_error[field] = err
            #Stop at first error
            break
    return form_error

def set_as_form(request, f_name, init = None):
    form_name = f_name
    form_class = getattr(forms, form_name)
    if request.POST:
        form = form_class(request.POST)
    else:
        if init is not None:
            form = form_class(initial=init)
        else:
            form = form_class(initial={'stn_id': None})
    return form

def run_external_script(cmd):
    """ Capture a command's standard output."""
    import subprocess
    out, err = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    return out, err
###################
#Headers
####################
def set_sodxtrmts_head(form):
    #Define Header Order:
    header_order =['start_year', 'end_year', '','variable']
    #Additional headere items
    if form['variable'] in ['gdd', 'hdd', 'cdd']:header_order+=['base_temperature']
    header_order+=['statistic']
    if form['departures_from_averages'] == 'T':
         header_order+=['departures_from_averages', '']
    else:
        header_order+=['']
    if form['statistic'] == 'ndays':
        if form['less_greater_or_between'] == 'l':
            header_order+=['less_greater_or_between','threshold_for_less_than','']
        elif form['less_greater_or_between'] == 'g':
            header_order+=['less_greater_or_between','threshold_for_greater_than','']
        else: #between
            header_order+=['less_greater_or_between','threshold_low_for_between','threshold_high_for_between','']
    header_order+=['max_missing_days']
    if form['frequency_analysis'] == 'T':
        if form['frequency_analysis_type'] == 'g':
            header_order+=['gev']
        elif form['frequency_analysis_type'] == 'p':
            header_order+=['pearson']
    header_order+=['']
    #Define SCHTUPID header
    header = []
    for key in header_order:
        if key in ['less_greater_or_between','frequency_analysis_type','frequency_analysis', 'departures_from_averages', 'statistic', 'variables','variable']:
            header.append([WRCCData.DISPLAY_PARAMS[key], WRCCData.DISPLAY_PARAMS[str(form[key])]])
            if key == 'variable':
                if form['units'] == 'metric':
                     units = WRCCData.UNITS_METRIC[str(form[key])]
                else:
                     units = WRCCData.UNITS_ENGLISH[str(form[key])]
                header.append(['Units', units])
        elif key == '':
            #header.append([])
            pass
        else:
            if key in form.keys():
                header.append([WRCCData.DISPLAY_PARAMS[key], str(form[key])])
    #Prepend station name or location
    if 'station_id' in form.keys():
        if 'user_area_id' in form.keys():
            header.insert(0,['Station', form['user_area_id']])
        else:
            header.insert(0,['Station', form['station_id']])
    if 'location' in form.keys():
        header.insert(0,['Location (lon, lat)', form['location']])
        header.insert(1,['Grid', WRCCData.GRID_CHOICES[form['grid']][0]])
    return header

def set_sodsumm_headers(table_list):
    headers = {}
    def set_header(table):
        rows = []
        if table == 'temp':
            rows.append('<b>Temperature Statistics</b>')
            rows.append('Averages -- Daily Extremes -- Mean Extremes -- Number of Days')
        if table == 'prsn':
            rows.append('<b>Precipitation/Snow Statistics</b>')
            rows.append('Total Precipitation -- Number of Days -- Total Snowfall')
        if table == 'hdd':
            rows.append('<b>Heating Degree Days</b>')
            rows.append('Degree Days to selected Base Temperatures')
        if table == 'cdd':
            rows.append('<b>Cooling Degree Days</b>')
            rows.append('Degree Days to selected Base Temperatures')
        if table == 'corn':
            rows.append('<b>Corn Growing Degree Days</b>')
        return "\n".join(rows)

    for table in table_list:
         headers[table] = set_header(table)
    return headers
######################
#Data
#####################
def set_params_for_shape_queries(search_params):
    shape_type = None
    shape_coords = None
    PointIn = None
    poly = None #set of  of lat,lon coords, needed to check if point in poly
    #Set up data request params
    bbox=''
    params = {
        'sdate':search_params['start_date'],
        'edate':search_params['end_date'],
        'grid':search_params['grid'],
        'meta':'ll,elev',
    }
    #find variable parameter
    if 'variable' in search_params.keys():
        params['elems'] = search_params['variable']
    elif 'variables' in search_params.keys():
         params['elems'] = search_params['variables']
    #Find search area parameters, shape and bounding box if needed

    #key, val, acis_param, name_long, search_type = WRCCUtils.get_search_area_values(search_params, 'gridded')
    if 'location' in search_params.keys():
        params['loc'] = search_params['location']
        shape_type = 'location'
        shape_coords = [float(s) for s in search_params['location'].replace(' ','').split(',')]
    elif 'state' in search_params.keys():
        params['state'] = search_params['state']
        shape_type = 'state'
    elif 'shape' in search_params.keys():
        shape_coords = [float(s) for s in search_params['shape'].replace(' ','').split(',')]
        #Find out what shape it is (circle, bbox, location, polygon)
        #and find enclosing bbox
        shape_type, bbox = WRCCUtils.get_bbox(search_params['shape'])
        #check if we have circle or polygon
        if shape_type == 'location':
            params['loc'] = search_params['shape']
        else:
            params['bbox'] = bbox
            if shape_type == 'polygon':
                PointIn = getattr(WRCCUtils,'point_in_poly')
                poly = [(shape_coords[2*idx],shape_coords[2*idx+1]) for idx in range(len(shape_coords)/2)]
            if shape_type == 'circle':
                PointIn = getattr(WRCCUtils,'point_in_circle')
                poly = shape_coords
    else:
        #county_warning_area,county, basin,climate_division
        #Need to make ACIS general call to dinf shape_coords and enclosing bbox
        shape_type = search_params['select_grid_by']
        at_acis = WRCCData.SEARCH_AREA_FORM_TO_ACIS[shape_type]
        val = search_params[search_params['select_grid_by']]
        gen_params={'id':val,'meta':'geojson,bbox,name,id'}
        #Make General Call
        try:
            gen_req = AcisWS.General(at_acis, gen_params)
            bbox = gen_req['meta'][0]['bbox']
            shape_coords = gen_req['meta'][0]['geojson']['coordinates'][0][0]
            PointIn = getattr(WRCCUtils,'point_in_poly')
            poly = [(shape_coords[2*idx][0],shape_coords[2*idx+1][1]) for idx in range(len(shape_coords)/2)]
            params['bbox'] = bbox
        except:
            pass
    return params, shape_type,shape_coords,PointIn,poly
######################
#Graphics generation
######################
def generate_sodsumm_graphics(results, tab, table, units):
    if not results:
        return {}
    cats = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    if tab =='temp':
        if units == 'metric':
            Units =  'Celsius'
            U = 'C'
        else:
            Units = 'Fahrenheit'
            U = 'F'
        legend = ['Extr Low','Ave Low','Mean', 'Ave High', 'Extr High']
        colors  = ['#FF0000', '#690000', '#00FF00', '#ADD8E6', '#0000FF']
        table_name_long = 'Temperatures (' + U + ')'
        Units = 'Fahrenheit'
        graph_data = [[] for i in range(12)]
        #graph_data = [[] for i in range(5)] # low, ave min, ave mean,ave max, high
        for idx, row in enumerate(results[table][1:13]):
            for i in range(5):
                if i == 0:k = 6 #low
                if i == 1:k = 2 #mean low
                if i == 2:k = 3 #mean ave
                if i == 3:k = 1 #mean high
                if i == 4:k = 4 #high
                try:
                    val = float(row[k])
                    if abs(val + 99.0)<0.000001 or abs(val + 9999.0)<0.00001 or abs(val - 9999.0)<0.00001:
                        graph_data[idx].append(None)
                    else:
                        graph_data[idx].append(val)
                except:
                    graph_data[idx].append(None)
    elif tab in ['hdd', 'cdd']:
        if units == 'metric':
            Units =  'Celsius'
            U = 'C'
        else:
            Units = 'Fahrenheit'
            U = 'F'
        colors = ['#87CEFA', '#00FFFF', '#14D8FF', '#143BFF', '#8A14FF']
        if table == 'hdd':
            if units == 'metric':
                legend = ['Base 18', 'Base 16', 'Base 14', 'Base 13', 'Base 10']
            else:
                legend = ['Base 65', 'Base 60', 'Base 57', 'Base 55', 'Base 50']
        else:
            if units == 'metric':
                legend = ['Base 13', 'Base 14', 'Base 16', 'Base 18', 'Base 21']
            else:
                legend = ['Base 55', 'Base 57', 'Base 60', 'Base 65', 'Base 70']
        table_name_long = WRCCData.ACIS_ELEMENTS_DICT[table]['name_long']  + '(' + U + ')'
        graph_data = [[] for i in range(5)]
        for i in range(5):
            for k in range(len(cats)):
                try:
                    val = float(results[table][i+1][k+1])
                    if abs(val + 99.0)<0.000001 or abs(val + 9999.0)<0.00001 or abs(val - 9999.0)<0.00001:
                        graph_data[i].append(None)
                    else:
                        graph_data[i].append(val)
                except:
                    graph_data[i].append(None)
    elif tab == 'gdd':
        if units == 'metric':
            Units =  'Celsius'
            U = 'C'
        else:
            Units = 'Fahrenheit'
            U = 'F'
        colors = ['#87CEFA', '#00FFFF', '#14D8FF', '#143BFF', '#8A14FF']
        table_name_long = WRCCData.ACIS_ELEMENTS_DICT[table]['name_long'] + '(' + U + ')'
        if units == 'metric':
            legend = ['Base 4', 'Base 7', 'Base 10', 'Base 13', 'Base 16']
        else:
            legend = ['Base 40', 'Base 45', 'Base 50', 'Base 55', 'Base 60']
        graph_data = [[] for i in range(5)]
        for i in range(5):
            for k in range(len(cats)):
                try:
                    val = float(results[table][2*i+1][k+2])
                    if abs(val + 99.0)<0.000001 or abs(val + 9999.0)<0.00001 or abs(val - 9999.0)<0.00001:
                        graph_data[i].append(None)
                    else:
                        graph_data[i].append(val)
                except:
                    graph_data[i].append(None)
    elif tab == 'corn':
        if units == 'metric':
            Units =  'Celsius'
            U = 'C'
        else:
            Units = 'Fahrenheit'
            U = 'F'
        colors = ['#14FFFF', '#00FFFF', '#14D8FF', '#143BFF', '#8A14FF']
        table_name_long = 'Corn Degree Days (' + U + ')'
        if units == 'metric':
            legend = ['Base 10']
        else:
            legend = ['Base 50']
        table_name_long = 'Corn Degree Days (' + U + ')'
        graph_data =[[]]
        for k in range(len(cats)):
            try:
                val = float(results[table][1][k+2])
                if abs(val + 99.0)<0.000001 or abs(val + 9999.0)<0.00001 or abs(val - 9999.0)<0.00001:
                    graph_data[0].append(None)
                else:
                    graph_data[0].append(val)
            except:
                graph_data[0].append(None)
    elif  tab == 'pcpn':
        if units == 'metric':
            Units =  'Millimeter'
            U = 'mm'
        else:
            Units = 'Inches'
            U = 'In'
        colors = ['#00FFFF','#00009B', ' #0000FF']
        legend = ['Ave Precip Low', 'Precip Mean', 'Ave Precip High']
        table_name_long = 'Precipitation (' + U + ')'
        graph_data = [[] for k in range(3)]
        for idx, row in enumerate(results[table][1:13]):
            for i in range(3):
                if i == 0:k=4
                if i == 1:k=1
                if i == 2:k=2
                try:
                    val = float(row[k])
                    if abs(val + 99.0)<0.000001 or abs(val + 9999.0)<0.00001 or abs(val - 9999.0)<0.00001:
                        graph_data[i].append(None)
                    else:
                        graph_data[i].append(val)
                except:
                    graph_data[i].append(None)
    elif tab == 'snow':
        if units == 'metric':
            Units =  'Millimeter'
            U = 'mm'
        else:
            Units = 'Inches'
            U = 'In'
        colors = ['#00FFFF','#00009B']
        legend = ['Snow Mean', 'Ave Snow High']
        table_name_long = 'Snow Fall (' + U + ')'
        graph_data = [[] for k in range(2)]
        for idx, row in enumerate(results[table][1:13]):
            for i in range(2):
                if i == 0:k=12
                if i == 1:k=13
                try:
                    val = float(row[k])
                    if abs(val + 99.0)<0.000001 or abs(val + 9999.0)<0.00001 or abs(val - 9999.0)<0.00001:
                        graph_data[i].append(None)
                    else:
                        graph_data[i].append(val)
                except:
                    graph_data[i].append(None)
    table_dict = {
        'cats':cats,
        'units':Units,
        'table_name':tab,
        'table_name_long':table_name_long,
        'legend':legend,
        'colors': colors,
        'graph_data': graph_data,
        'table_data':results[table]
        }
    return table_dict
#############################
#Display and search params
##############################
def set_el_string_and_list(form):
    if not 'variables' in form.keys() and not 'variable' in form.keys() and not 'variables_string' in form.keys():
        return '', []
    if 'variable' in form.keys():
        form_els = form['variable']
    if 'variables' in form.keys():
        form_els = form['variables']
    if isinstance(form_els,list):
        el_list = [str(el) for el in form_els]
        el_string = ''
        for el_idx, el in enumerate(el_list):
            el_string+=str(el)
            if el_idx < len(el_list) - 1:
                el_string+=','
        return el_string, el_list
    elif isinstance(form_els,basestring):
        el_string = form_els.replace(', ',',')
        el_list = el_string.split(',')
        return el_string, el_list
    else:
        try:
            el_string = form['variables_string'].replace('  ','')
            el_list = el_string.split(',')
        except:
            return '', []
##################
#Initialization
###################
def join_dicts(d, d_1):
    for key, val in d_1.iteritems():
        d[key]=val

def join_initials(initial,initial_2):
    #combine the graph options with the plot options
    for key, val in initial_2.iteritems():
        initial[key] = val
