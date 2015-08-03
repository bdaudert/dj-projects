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
from django.core.mail import send_mail
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
import WRCCUtils, AcisWS, WRCCDataApps, WRCCClasses, WRCCData, WRCCFormCheck
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
def test(request):
    context = {
        'title': 'Southwest Climate and ENvironmental Information Collaborative',
    }
    return render_to_response('scenic/index.html', context, context_instance=RequestContext(request))

def home(request):
    context = {
        'title': 'Start by choosing one of the following:',
    }
    return render_to_response('scenic/home.html', context, context_instance=RequestContext(request))

def swcke_home(request):
    context = {
        'title': 'Page Redirect',
    }
    return render_to_response('scenic/swcke_home.html', context, context_instance=RequestContext(request))

def about_us(request):
    context = {
        'title': 'Overview',
        'icon':'AboutUs.png'
    }
    return render_to_response('scenic/about_us.html', context, context_instance=RequestContext(request))

def who_we_are(request):
    context = {
        'title': 'Who we are',
        'icon':'AboutUs.png'
    }
    return render_to_response('scenic/who_we_are.html', context, context_instance=RequestContext(request))

def what_we_do(request):
    context = {
        'title': 'What we do',
        'icon':'AboutUs.png'
    }
    return render_to_response('scenic/what_we_do.html', context, context_instance=RequestContext(request))

def contact_us(request):
    context = {
        'title': 'Contact Us',
        'icon':'AboutUs.png'
    }
    return render_to_response('scenic/contact_us.html', context, context_instance=RequestContext(request))

def dashboard(request):
    context = {
        'title': 'Climate Dashboard',
        'icon':'Dashboard.png'
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

    return render_to_response('scenic/dashboard.html', context, context_instance=RequestContext(request))

def gallery(request):
    context = {
        'title': 'How To'
    }
    app_urls = {};app_names = {};param_urls = {}

    #Gallery: FINDING A POINT/AREA OF INETREST
    app_url = settings.APPLICATIONS['station_finder'][1]
    p_url = app_url + '?'
    p_url+='area_type=county&county=Sierra,%2006091'
    p_url+='&elements=mint,pcpn&elements_constraints=all'
    p_url+='&start_date=19300101&end_date=20141231&dates_constraints=all'
    app_urls['station_finder'] = app_url
    param_urls['station_finder'] = p_url
    app_names['station_finder'] = settings.APPLICATIONS['station_finder'][0]
    #Gallery: EXTREMES (monann ndays)
    app_url = settings.APPLICATIONS['monann'][1]
    p_url = app_url + '?'
    #p_url+='area_type=location&location=-120.44,39.32&element=mint&grid=1&start_year=1970&end_year=2000'
    p_url+='area_type=station_id&station_id=048218&element=mint&start_year=POR&end_year=POR'
    p_url+='&statistic=ndays&less_greater_or_between=l&threshold_for_less_than=32&plot_months=3,4,5'
    app_urls['extremes'] = app_url
    param_urls['extremes'] = p_url
    app_names['extremes'] = settings.APPLICATIONS['monann'][0]
    #Gallery: SUMMARIZING SPATIAL DATA (spatial_summary)
    app_url = settings.APPLICATIONS['spatial_summary'][1]
    p_url = app_url + '?'
    p_url+='area_type=shape&shape=-120.77,36.84,-120.6,36.78,-120.54,36.71,-120.63,36.63,-120.76,36.77'
    p_url+='&spatial_summary=mean&elements=maxt,mint,avgt&grid=1&start_date=20150301&end_date=20150331'
    p_url+='&data_type=grid&grid=1'
    app_urls['spatial_summary'] = app_url
    param_urls['spatial_summary'] = p_url
    app_names['spatial_summary'] = settings.APPLICATIONS['spatial_summary'][0]
    #Set context variables
    context['app_urls'] = app_urls
    context['app_names'] = app_names
    context['param_urls'] = param_urls
    return render_to_response('scenic/gallery.html', context, context_instance=RequestContext(request))

def resources(request):
    context = {
        'title': 'External Resources'
    }
    return render_to_response('scenic/resources.html', context, context_instance=RequestContext(request))

def upload_test(request):
    context = {
        'title': 'Shapefile upload test'
    }
    form = forms.UploadFileForm()
    poly_ll = ''
    if request.method == 'POST':
        form = forms.UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #shape_file = request.FILES['shape_file']
            shape_files = request.FILES.getlist('files')
            feature_id = form.cleaned_data['feature_id']
            context['shape_files'] = shape_files
            #Write shape files to /tmp
            shp_file = None
            for shape_file in shape_files:
                if str(shape_file).split('.')[-1] == 'shp':
                    shp_file = str(shape_file)
                with open('/tmp/' + str(shape_file),'wb+') as dest:
                    for chunk in shape_file.chunks():
                        dest.write(chunk)
            #Read shape file and retrieve lat, lon coordinates
            context['shp_file'] = shp_file
            if shp_file is not None:
                from osgeo import gdal, ogr, osr
                ## Project all coordinates to WGS84
                output_osr = osr.SpatialReference()
                output_osr.ImportFromEPSG(4326)  ## WGS84
                ##output_osr.ImportFromEPSG(4269)  ## NAD83
                ## Get the spatial reference
                input_ds = ogr.Open('/tmp/' + shp_file)
                input_layer = input_ds.GetLayer()
                input_osr = input_layer.GetSpatialRef()
                ## Build the tranform object for projecting the coordinates
                tx = osr.CoordinateTransformation(input_osr, output_osr)
                #Get the feature by ID
                input_ftr = input_layer.GetFeature(long(feature_id))
                context['FID'] = feature_id
                input_geom = input_ftr.GetGeometryRef()
                input_geom_type = input_geom.GetGeometryName()
                context['geometry'] = input_geom_type
                ## Project a copy of the geometry
                proj_geom = input_geom.Clone()
                proj_geom.Transform(tx)

                #Extract lon, lat coordinates from
                #different geometry types
                #1.POINT and MULTIPOINT
                if input_geom_type in  ['POINT','MULTIPOINT']:
                    for i in range(0, proj_geom.GetPointCount()):
                        pt = proj_geom.GetPoint(i)
                        poly_ll+=str(pt[0]) + ',' + str(pt[1])
                        if i < proj_geom.GetPointCount() - 1:
                            poly_ll+=','
                #4.POLYGONS, LINES, MULTILINESTRINGS
                if input_geom_type in ['POLYGON','LINE','MULTILINESTRING']:
                    ## POLYGONS are made up of LINEAR RINGS
                    for i in range(0, proj_geom.GetGeometryCount()):
                        sub_geom = proj_geom.GetGeometryRef(i)

                        ## LINEAR RINGS are made up of POINTS
                        for j in range(0, sub_geom.GetPointCount()):
                            pt = sub_geom.GetPoint(j)
                            poly_ll+=str(pt[0]) + ',' + str(pt[1])
                            if j < sub_geom.GetPointCount() - 1:
                                poly_ll+=','

                    ## Get the next feature
                    #input_ftr = input_layer.GetNextFeature()
                    ## Or break after the first one
                    #break
    context['poly_ll'] = poly_ll
    context['form'] = form
    return render_to_response('scenic/upload_test.html', context, context_instance=RequestContext(request))

def data_home(request):
    context = {
        'title': 'Data Access'
    }
    return render_to_response('scenic/data/home.html', context, context_instance=RequestContext(request))

def single_point_prods(request):
    context = {
        'title': 'Single Point Products'
    }
    #Link from other apps
    if request.method == 'GET' and ('elements' in request.GET or 'element' in request.GET):
        #set link params
        init = {}
        for item in request.GET:
            try:
                key = WRCCData.DISPLAY_PARAMS[item]
                val = str(request.GET[item])
                init[key] = val
            except:
                continue
        context['initial'] = init
        for app in ['single_lister', 'monann', 'climatology','data_comparison']:
            initial, checkbox_vals = set_initial(request, app)
            p_str = '?'
            for key, val in initial.iteritems():
                k = str(key);
                #convert lists to strings (elements)
                if isinstance(val, list):
                    v = (',').join(val)
                else:
                    v = str(val)
                p_str+= k +'=' + v + '&'
            #strip last &
            p_str=p_str[0:-1]
            context['url_params_' + app] =  p_str

    return render_to_response('scenic/data/single/home.html', context, context_instance=RequestContext(request))

def multi_point_prods(request):
    context = {
        'title': 'Multi Point Products'
    }
    #Link from other apps
    if request.method == 'GET' and ('elements' in request.GET or 'element' in request.GET):
        #set link params
        for app in ['multi_lister', 'spatial_summary', 'temporal_summary']:
            initial, checkbox_vals = set_initial(request, app)
            p_str = '?'
            for key, val in initial.iteritems():
                k = str(key);
                #convert lists to strings (elements)
                if isinstance(val, list):
                    v = (',').join(val)
                else:
                    v = str(val)
                p_str+= k +'=' + v + '&'
            #strip last &
            p_str=p_str[0:-1]
            context['url_params_' + app] =  p_str
    return render_to_response('scenic/data/multi/home.html', context, context_instance=RequestContext(request))


def sw_networks(request):
    context = {
        'title': 'Southwest Networks',
        'icon':'DataPortal.png'
    }
    return render_to_response('scenic/data/sw_networks.html', context, context_instance=RequestContext(request))

def feedback(request):
    context = {
        'title': 'Feedback',
        'icon':'AboutUs.png'
    }
    errors = []
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
            errors.append('Enter a subject.')
        if not request.POST.get('message', ''):
            errors.append('Enter a message.')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid e-mail address.')
        if not errors:
            send_mail(
                request.POST['subject'],
                request.POST['message'],
                request.POST.get('email', 'noreply@example.com'),
                ['csc-wrcc@dri.edu'],
            )
            context['message'] = 'Thank you for your input!'
        else:
            context['message'] = errors
            context['error'] = errors
    return render_to_response('scenic/feedback.html', context, context_instance=RequestContext(request))

def download(request):
    context = {
        'title': 'Download',
        'icon':'ToolProduct.png'
    }
    app_name = request.GET.get('app_name', None)
    json_file_name = request.GET.get('json_file', None)
    json_file = settings.TEMP_DIR + json_file_name
    json_in_file_name = json_file_name
    tab = request.GET.get('tab', None)
    form0 = forms.DownloadForm()
    context['form0'] = form0
    if 'form0' in request.POST:
        form0 = set_as_form(request,'DownloadForm')
        context['form0'] = form0
        if form0.is_valid():
            #context['data_dict'] = form0.cleaned_data
            data_format = form0.cleaned_data['data_format']
            delimiter = form0.cleaned_data['delimiter']
            output_file_name = form0.cleaned_data['output_file_name']
            #If Sodsumm, we need to fine the right data set
            if app_name == 'Sodsumm':
                json_data = WRCCUtils.load_json_data_from_file(json_file)
                #find the correct data set corresponding to the tab name
                for idx, data_dict in enumerate(json_data):
                    if data_dict['table_name'] == tab:
                        #context['data_dict'] = data_dict
                        #Overwrite json_in_file
                        json_in_file_name = json_file_name + '_in'
                        WRCCUtils.load_data_to_json_file(settings.TEMP_DIR + json_in_file_name, data_dict)
                        break
            DDJ = WRCCToReplace.DownloadDataJob(app_name,data_format,delimiter, output_file_name, request=request, json_in_file=settings.TEMP_DIR + json_in_file_name)
            if data_format in ['clm', 'dlm','xl']:
                return DDJ.write_to_file()
            else:
                response = DDJ.write_to_file()
                context['response'] = response
    return render_to_response('scenic/download.html', context, context_instance=RequestContext(request))

def single_lister(request):
    context = {
        'title': settings.APPLICATIONS['single_lister'][0]
    }
    url = settings.APPLICATIONS['single_lister'][2]
    initial, checkbox_vals = set_initial(request,'single_lister')
    context['initial'] = initial; context['checkbox_vals'] =  checkbox_vals
    #Data request submitted
    if 'formData' in request.POST or (request.method == 'GET' and 'elements' in request.GET):
        #form = set_form(initial, clean = False)
        form_cleaned = set_form(initial,clean = True)
        form = set_form(initial, clean = False)
        #Check form fields
        fields_to_check = [form_cleaned['area_type'],'start_date','end_date','start_window','end_window','degree_days']
        form_error = check_form(form_cleaned, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            if form_cleaned['area_type'] == 'location':
                #Only show gridpoint map if area caused form_error
                if 'Location (lon,lat)' in form_error.keys():
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
            req['data'] = WRCCUtils.get_window_data(d, sd, ed, sw, ew)
            req['data'].insert(0,header)
            req['data'] = [req['data']]
        if not req['data'] and not req['smry']:
            req['errors'] = {'errors':'No data found for these parameters.'}
            context['results'] = req
            return render_to_response(url, context, context_instance=RequestContext(request))
        context['run_done'] = True
        context['results'] = req

        if form_cleaned['data_summary'] == 'none':
            if 'station_id' in form_cleaned.keys():
                header_keys = ['station_id','start_date', 'end_date']
            else:
                header_keys = ['user_area_id','start_date', 'end_date']
        else:
            if 'station_id' in form_cleaned.keys():
                header_keys = ['station_id','data_summary','start_date', 'end_date']
            else:
                header_keys = ['user_area_id','data_summary','start_date', 'end_date']
        context['params_display_list'] = WRCCUtils.form_to_display_list(header_keys,form_cleaned)
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
            CsvWriter = WRCCClasses.CsvWriter(req, f=None, response=response)
            CsvWriter.write_to_file()
            return response
        if form_cleaned['data_format'] in ['xl'] and (req['data'] or req['smry']):
            file_extension = '.xls'
            response = HttpResponse(content_type='application/vnd.ms-excel;charset=UTF-8')
            #WRCCUtils.write_to_excel(response,req)
            ExcelWriter = WRCCClasses.ExcelWriter(req,response=response)
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
    #Download button pressed
    if 'formDownload' in request.POST:
        form = set_form(request,clean=False)
        json_file = request.POST.get('json_file', None)
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        file_name = form['output_file_name'] + '_' + time_stamp
        with open(settings.TEMP_DIR + json_file, 'r') as f:
            data =  json.load(f)

        if form['data_format'] in ['clm','dlm']:
            if form['data_format'] == 'clm':
                file_extension = '.txt'
            else:
                file_extension = '.dat'
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment;filename=%s%s' % (file_name,file_extension)
            CsvWriter = WRCCClasses.CsvWriter(data, f=None, response=response)
            CsvWriter.write_to_file()
            return response
        if form['data_format'] in ['xl']:
            file_extension = '.xls'
            response = HttpResponse(content_type='application/vnd.ms-excel;charset=UTF-8')
            ExcelWriter = WRCCClasses.ExcelWriter(data,response=response)
            ExcelWriter.write_to_file()
            response['Content-Disposition'] = 'attachment;filename=%s%s' % (file_name, file_extension)
            return response
    return render_to_response(url, context, context_instance=RequestContext(request))


def single_interannual(request):
    context = {
        'title': settings.APPLICATIONS['single_interannual'][0]
    }
    url = settings.APPLICATIONS['single_interannual'][2]
    initial, checkbox_vals = set_initial(request,'interannual')
    context['initial'] = initial; context['checkbox_vals'] =  checkbox_vals
    if 'formData' in request.POST:
        form = set_form(request,clean = False)
        form_cleaned = set_form(request,clean = True)
        element_short = WRCCUtils.elements_to_table_headers(form['element'],form['units'])[0]
        results = {
            'data_indices':[0],
            'element_short':element_short,
            'data':[],
            'errors':''
        }
        #Data request
        year_data, hc_data = WRCCUtils.get_single_interannaul_data(form_cleaned)
        context['run_done'] = True
        header_keys = ['user_area_id','temporal_summary', 'element',\
        'start_year', 'end_year','window']
        context['params_display_list'] = WRCCUtils.form_to_display_list(header_keys,form_cleaned)
        if not year_data:
            context['results'] = results
            return render_to_response(url, context, context_instance=RequestContext(request))
        results['data'] = year_data
        #Set up graph data
        GDWriter = WRCCClasses.GraphDictWriter(form_cleaned, hc_data)
        graph_dict = GDWriter.write_dict()
        results['graph_data'] = [graph_dict]
        results['chartType'] = graph_dict['chartType']
        context['results'] = results
    #Download button pressed
    if 'formDownload' in request.POST:
        form = set_form(request,clean=False)
        json_file = request.POST.get('json_file', None)
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        file_name = form['output_file_name'] + '_' + time_stamp
        with open(settings.TEMP_DIR + json_file, 'r') as f:
            data =  json.load(f)

        if form['data_format'] in ['clm','dlm']:
            if form['data_format'] == 'clm':
                file_extension = '.txt'
            else:
                file_extension = '.dat'
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment;filename=%s%s' % (file_name,file_extension)
            CsvWriter = WRCCClasses.CsvWriter(data, f=None, response=response)
            CsvWriter.write_to_file()
            return response
        if form['data_format'] in ['xl']:
            file_extension = '.xls'
            response = HttpResponse(content_type='application/vnd.ms-excel;charset=UTF-8')
            ExcelWriter = WRCCClasses.ExcelWriter(data,response=response)
            ExcelWriter.write_to_file()
            response['Content-Disposition'] = 'attachment;filename=%s%s' % (file_name, file_extension)
            return response
    return render_to_response(url, context, context_instance=RequestContext(request))

def multi_lister(request):
    context = {
        'title': settings.APPLICATIONS['multi_lister'][0]
    }
    url = settings.APPLICATIONS['multi_lister'][2]
    initial, checkbox_vals = set_initial(request,'multi_lister')
    context['initial'] = initial; context['checkbox_vals'] =  checkbox_vals
    #Set initial overlay state for overlay map
    #context[initial['overlay_state'].lower() + '_selected'] = 'selected'
    if 'formData' in request.POST:
        form = set_form(request,clean=False)
        form_cleaned = set_form(request)
        #Check for form errors
        fields_to_check = [form_cleaned['area_type'],'start_date', 'end_date','degree_days']
        if form_cleaned['data_summary'] in['none','windowed_data']:
            fields_to_check.append('user_email')
        form_error = check_form(form_cleaned, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            #Only show maps if area field is in form_error
            if 'County'in form_error.keys() or 'County Warning Area' in form_error.keys():
                context['need_overlay_map'] = True
            if 'Basin'in form_error.keys() or 'Climate Division' in form_error.keys():
                context['need_overlay_map'] = True
            if 'Custom Shape' in form_error.keys():
                context['need_polygon_map'] = True
            return render_to_response(url, context, context_instance=RequestContext(request))
        #Deal with large requests
        if form_cleaned['data_summary'] in['none','windowed_data']:
            context['large_request'] = True
            #Process request offline
            json_file = form_cleaned['output_file_name'] + settings.PARAMS_FILE_EXTENSION
            WRCCUtils.load_data_to_json_file(settings.DATA_REQUEST_BASE_DIR +json_file, form_cleaned)
            return render_to_response(url, context, context_instance=RequestContext(request))

        #Data request
        req = {}
        '''
        try:
            req = WRCCUtils.request_and_format_data(form_cleaned)
            if 'smry' not in req.keys() and 'data' not in  req.keys():
                req['error'] = 'No data found for these parameters!'
                context['results'] = req
                return render_to_response(url, context, context_instance=RequestContext(request))
        except Exception, e:
            req['error'] = 'Data request error: %s' %str(e)
            context['results'] = req
            return render_to_response(url, context, context_instance=RequestContext(request))
        '''
        req = WRCCUtils.request_and_format_data(form_cleaned)
        context['results'] = req
        context['run_done'] = True
        #Format Data for display and/or download
        header_keys = ['data_type',form_cleaned['area_type'],\
            'data_summary','start_date', 'end_date']
        context['params_display_list'] = WRCCUtils.form_to_display_list(header_keys,form_cleaned)
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
            CsvWriter = WRCCClasses.CsvWriter(req, f=None, response=response)
            CsvWriter.write_to_file()
            return response
        if form_cleaned['data_format'] in ['xl'] and (req['data'] or req['smry']):
            file_extension = '.xls'
            response = HttpResponse(content_type='application/vnd.ms-excel;charset=UTF-8')
            ExcelWriter = WRCCClasses.ExcelWriter(req,response=response)
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

    #Overlay maps
    if 'formOverlay' in request.POST:
        context['need_overlay_map'] = True
        initial, checkbox_vals = set_initial(request,'map_overlay')
        context[initial['overlay_state'] + '_selected'] = 'selected'
        #overide kml_file_path
        initial['kml_file_path'] = create_kml_file(initial['area_type'], initial['overlay_state'])
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals

    #Download button pressed
    if 'formDownload' in request.POST:
        form = set_form(request,clean=False)
        json_file = request.POST.get('json_file', None)
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        file_name = form['output_file_name'] + '_' + time_stamp
        with open(settings.TEMP_DIR + json_file, 'r') as f:
            req =  json.load(f)
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
    return render_to_response(url, context, context_instance=RequestContext(request))

def temporal_summary(request):
    context = {
        'title': settings.APPLICATIONS['temporal_summary'][0]
    }
    url = settings.APPLICATIONS['temporal_summary'][2]
    json_file = request.GET.get('json_file', None)
    #Check if we are coming in from other page, e.g. Gridded Data
    #Set initial accordingly
    if json_file is not None:
        json_data = WRCCUtils.load_json_data_from_file(settings.TEMP_DIR + json_file)
        if not json_data or not 'search_params' in json_data.keys():
            initial,checkbox_vals = set_temporal_summary_initial(request)
            #initial,checkbox_vals = set_initial(request,'temporal_summary')
        else:
            #initial,checkbox_vals = set_initial(json_data['search_params'],'temporal_summary')
            initial,checkbox_vals = set_temporal_summary_initial(json_data['search_params'])
    else:
        #initial,checkbox_vals = set_initial(request,'temporal_summary')
        initial,checkbox_vals = set_temporal_summary_initial(request)
    #Plot Options
    initial_plot, checkbox_vals_plot = set_map_plot_options(request)
    join_initials(initial, initial_plot, checkbox_vals, checkbox_vals_plot)
    context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
    if initial['area_type'] != 'bounding_box':
        context['hide_bbox_map'] = True
    #Set up maps if needed
    #context[initial['area_select']] = WRCCData.AREA_DEFAULTS[initial['area_select']]
    #context[initial['overlay_state'] + '_selected'] = 'selected'

    #Link from other page
    if request.method == 'GET' and 'elements' in request.GET:
        form_cleaned = set_form(request,clean=True)
        form = set_form(request,clean=False)
        header_keys = [form_cleaned['area_type'],'temporal_summary',\
            'elements','units','start_date', 'end_date','grid']
        context['params_display_list'] = WRCCUtils.form_to_display_list(header_keys,form_cleaned)

    if 'formMap' in request.POST:
        context['hide_bbox_map'] = True
        form = set_form(request, clean=False)
        form_cleaned = set_form(request)
        #Set initials
        initial,checkbox_vals = set_temporal_summary_initial(form)
        #initial,checkbox_vals = set_initial(form,'temporal_summary')
        initial_plot, checkbox_vals_plot = set_map_plot_options(form)
        join_initials(initial, initial_plot, checkbox_vals, checkbox_vals_plot)
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
        header_keys = [form['area_type'],'temporal_summary',\
            'elements','units','start_date', 'end_date','grid']
        context['params_display_list'] = WRCCUtils.form_to_display_list(header_keys,form_cleaned)

        #Back Button/download files issue fix:
        if not 'area_type' in form.keys():
            for key in WRCCData.SEARCH_AREA_FORM_TO_ACIS.keys():
                if key in form.keys():
                    form['area_type'] = key
                    break

        #Form Check
        fields_to_check = ['start_date', 'end_date','degree_days','level_number', 'cmap', form['area_type'], 'elements']
        #fields_to_check = ['start_date', 'end_date','degree_days',form['area_type'], 'elements']
        form_error = check_form(form_cleaned, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            if form_cleaned['area_type'] in ['basin','county','county_warning_area', 'climate_division']:
                context['need_overlay_map'] = True
            kml_file_path = create_kml_file(form['area_type'], form['overlay_state'])
            context['kml_file_path'] = kml_file_path
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
        for el_idx,element in enumerate(form_cleaned['elements']):
            pms = copy.deepcopy(params)
            a_el_dict = {
                'name':element,
                'smry':form_cleaned['temporal_summary'],
                'smry_only':1
            }
            if pms['units'] == 'metric':
                if element in ['pcpn','snow','snwd']:
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
    return render_to_response(url, context, context_instance=RequestContext(request))

def spatial_summary(request):
    context = {
        'title': settings.APPLICATIONS['spatial_summary'][0]
    }
    url = settings.APPLICATIONS['spatial_summary'][2]
    initial,checkbox_vals = set_initial(request,'spatial_summary')
    context['initial'] = initial;context['checkbox_vals'] = checkbox_vals

    if 'formData' in request.POST or (request.method == 'GET' and 'elements' in request.GET):
        #Set form and initial
        form = set_form(initial, clean=False)
        form_cleaned = set_form(initial)
        '''
        #Back Button/download files issue fix:
        #if area_type none, find it
        if not 'area_type' in form_cleaned.keys() or form_cleaned['area_type'] not in form_cleaned.keys():
            for key in WRCCData.SEARCH_AREA_FORM_TO_ACIS.keys():
                if key in form.keys():
                    form['area_type'] = key
                    form_cleaned['area_type'] = key
                    break
        '''
        #Form Check
        fields_to_check = [form['area_type'],'start_date', 'end_date','degree_days', 'elements']
        #,'connector_line_width', 'vertical_axis_min', 'vertical_axis_max']
        form_error = check_form(form_cleaned, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            if form_cleaned['area_type'] in ['basin','county','county_warning_area', 'climate_division']:
                context['need_overlay_map'] = True
            try:
                kml_file_path = create_kml_file(form['area_type'], form['overlay_state'])
                context['kml_file_path'] = kml_file_path
            except:
                pass
            return render_to_response(url, context, context_instance=RequestContext(request))

        #Display parameters
        header_keys = ['data_type',form_cleaned['area_type'],\
            'spatial_summary','elements','units','start_date', 'end_date']
        context['params_display_list'] = WRCCUtils.form_to_display_list(header_keys,form_cleaned)

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
                        results['errors'] = 'No data found in file %s' %json_file
                        context['results'] = results
                        return render_to_response(url, context, context_instance=RequestContext(request))
                except Exception, e:
                    results['error'] = 'Error when reading %s: %s' (json_file, str(e))
                    context['results'] = results
                    return render_to_response(url, context, context_instance=RequestContext(request))
        #Get Data
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
        req = WRCCUtils.request_and_format_data(form_cleaned)
        results['smry'] = req['smry']
        #Save to json file for downloading

        #format data for highcarts
        graph_data = []
        for el_idx, element in enumerate(form_cleaned['elements']):
            el_data = WRCCUtils.extract_highcarts_data_spatial_summary(req['smry'],el_idx, element,form_cleaned)
            GraphDictWriter = WRCCClasses.GraphDictWriter(form_cleaned, el_data, element = element)
            datadict = GraphDictWriter.write_dict()
            graph_data.append(datadict)

        results['graph_data'] = graph_data

        elements = []
        for el in form_cleaned['elements']:
            el_strip, base_temp = WRCCUtils.get_el_and_base_temp(el)
            el_name = WRCCData.ACIS_ELEMENTS_DICT[el_strip]['name_long']
            if base_temp is not None:
                el_name+= str(base_temp)
            elements.append(el_name)
        results['elements'] = elements
        results['data_indices'] = [0]; results['chartType'] = graph_data[0]['chartType']
        #results['json_file_path'] = settings.TMP_URL + json_file
        context['results'] = results
        context['run_done'] = True
        #Save resulst for downloading
        json_dict = {
            'smry':results['smry'],
            #'params_display_list':context['params_display_list']
            'form':form_cleaned,
            'data':[]
        }
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        json_file = '%s_spatial_summary.json' %(time_stamp)
        WRCCUtils.load_data_to_json_file(settings.TEMP_DIR +json_file, json_dict)
        context['json_file'] = json_file
    #Overlay maps
    if 'formOverlay' in request.POST:
        context['need_overlay_map'] = True
        initial, checkbox_vals = set_initial(request,'map_overlay')
        context[initial['overlay_state'] + '_selected'] = 'selected'
        #overide kml_file_path
        initial['kml_file_path'] = create_kml_file(initial['area_type'], initial['overlay_state'])
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals

    #Download button pressed
    if 'formDownload' in request.POST:
        form = set_form(request,clean=False)
        json_file = request.POST.get('json_file', None)
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        file_name = form['output_file_name'] + '_' + time_stamp
        with open(settings.TEMP_DIR + json_file, 'r') as f:
            req =  json.load(f)
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

    return render_to_response(url, context, context_instance=RequestContext(request))


def climateengine(request):
    context = {
        'title': ''
        }
    return render_to_response('scenic/data/multi/climateengine.html', context, context_instance=RequestContext(request))


def station_finder(request):
    context = {
        'title': settings.APPLICATIONS['station_finder'][0]
    }
    url = settings.APPLICATIONS['station_finder'][2]

    from subprocess import call
    call(["touch", settings.TEMP_DIR + "Empty.json"])
    #Set up initial map (NV stations)
    #context['station_json'] = 'NV_stn.json'
    initial,checkbox_vals = set_initial(request,'station_finder')
    context['initial'] = initial;context['checkbox_vals']=checkbox_vals
    #Set up maps if needed
    if request.method == "GET" and not 'elements' in request.GET:
        #Generate initial map
        by_type = WRCCData.ACIS_TO_SEARCH_AREA['state']
        val = 'nv'
        date_range = [initial['start_date'],initial['end_date']]
        el_date_constraints = initial['elements_constraints'] + '_' + initial['dates_constraints']
        station_json, f_name = AcisWS.station_meta_to_json(by_type, val, el_list=['1','2','4'],time_range=date_range, constraints=el_date_constraints)
        context['station_ids'] = WRCCUtils.get_station_ids('/tmp/' + f_name)

        #Write json file for link to data lister
        json_dict = copy.deepcopy(initial)
        json_dict['station_ids'] = WRCCUtils.get_station_ids('/tmp/' + f_name)
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        json_file_name = '%s_params.json' %(time_stamp)
        WRCCUtils.load_data_to_json_file(settings.TEMP_DIR + json_file_name, json_dict)
        context['params_json'] = json_file_name
        if 'error' in station_json.keys():
            context['error'] = station_json['error']
        if 'stations' not in station_json.keys() or  station_json['stations'] == []:
            context['error'] = "No stations found for these search parameters."
        context['station_json'] = f_name

    if 'formData' in request.POST or (request.method == 'GET' and 'elements' in request.GET):
        #Turn request object into python dict
        form = set_form(request,clean=False)
        form_cleaned = set_form(request,clean=True)
        fields_to_check = [form_cleaned['area_type'],'start_date', 'end_date', 'elements']
        form_error = check_form(form_cleaned, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            if form_cleaned['area_type'] in ['basin','county','county_warning_area', 'climate_division']:
                context['need_overlay_map'] = True
            return render_to_response(url, context, context_instance=RequestContext(request))
        #Convert element list to var majors
        el_vX_list = []
        for el_idx, element in enumerate(form_cleaned['elements']):
            el,base_temp = WRCCUtils.get_el_and_base_temp(element)
            el_vX_list.append(str(WRCCData.ACIS_ELEMENTS_DICT[el]['vX']))
        #context['req']= el_vX_list
        #Set up params for station_json generation
        by_type = WRCCData.ACIS_TO_SEARCH_AREA[form_cleaned['area_type']]
        val = form_cleaned[WRCCData.ACIS_TO_SEARCH_AREA[form_cleaned['area_type']]]
        date_range = [form_cleaned['start_date'],form_cleaned['end_date']]
        el_date_constraints = form_cleaned['elements_constraints'] + '_' + form_cleaned['dates_constraints']
        station_json, f_name = AcisWS.station_meta_to_json(by_type, val, el_list=el_vX_list,time_range=date_range, constraints=el_date_constraints)
        #Write to file for map generation
        context['station_ids'] = WRCCUtils.get_station_ids('/tmp/' + f_name)
        json_dict = copy.deepcopy(form_cleaned)
        json_dict['station_ids'] = WRCCUtils.get_station_ids('/tmp/' + f_name)
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        json_file_name = '%s_params.json' %(time_stamp)
        WRCCUtils.load_data_to_json_file(settings.TEMP_DIR + json_file_name, json_dict)

        if 'error' in station_json.keys():
            context['error'] = station_json['error']
        if 'stations' not in station_json.keys() or  station_json['stations'] == []:
            context['error'] = "No stations found for these search parameters."
        context['station_json'] = f_name
        context['run_done'] = True
    #Download data for all sations displayed
    #Request will be processed offline
    if 'formDownload' in request.POST:
        initial, checkbox_vals = set_initial(request,'sf_download')
        context[initial['overlay_state'] + '_selected'] = 'selected'
        context['large_request'] = True
        form_cleaned = set_form(initial, clean=True)
        fields_to_check = ['user_email']
        form_error = check_form(form_cleaned, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            m = ['basin','county','county_warning_area', 'climate_division']
            if 'area_type' in initial.keys() and initial['area_type'] in m:
                context['need_overlay_map'] = True
            return render_to_response(url, context, context_instance=RequestContext(request))
        context['x'] = initial
        #context['xx'] = form_cleaned
        #os.remove(settings.DATA_REQUEST_BASE_DIR + 'SFDownloadTest_params.json')
        json_file = form_cleaned['output_file_name'] + settings.PARAMS_FILE_EXTENSION
        WRCCUtils.load_data_to_json_file(settings.DATA_REQUEST_BASE_DIR +json_file, form_cleaned)
        return render_to_response(url, context, context_instance=RequestContext(request))

    #Overlay maps
    if 'formOverlay' in request.POST:
        context['need_overlay_map'] = True
        initial, checkbox_vals = set_initial(request,'map_overlay')
        context[initial['overlay_state'] + '_selected'] = 'selected'
        #overide kml_file_path
        initial['kml_file_path'] = create_kml_file(initial['area_type'], initial['overlay_state'])
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals

    return render_to_response(url, context, context_instance=RequestContext(request))

#######################
#Mixed Data Applications
######################
def likelihood(request):
    context = {
        'title': settings.APPLICATIONS['likelihood'][0]
    }
    url = settings.APPLICATIONS['likelihood'][2]

    initial,checkbox_vals = set_combined_analysis_initial(request,'likelihood')
    context['initial'] = initial; context['checkbox_vals'] = checkbox_vals
    return render_to_response(url, context, context_instance=RequestContext(request))

def data_comparison(request):
    context = {
        'title': settings.APPLICATIONS['data_comparison'][0]
    }
    url = settings.APPLICATIONS['data_comparison'][2]

    initial, checkbox_vals = set_initial(request,'data_comparison')
    context['initial'] = initial; context['checkbox_vals'] = checkbox_vals
    if 'formData' in request.POST or (request.method == 'GET' and 'station_location' in request.GET):
        context['form_message'] = True
        form = set_form(request, clean=False)
        form_cleaned = set_form(request, clean=True)
        #Link from station finder
        if 'station_location' in request.GET:
            form['location'] = request.GET['station_location']
            form_cleaned['location'] = request.GET['station_location']
        DC = WRCCClasses.DataComparer(form)
        gdata,sdata,dist = DC.get_data()
        context['run_done'] = True
        results = {
            'grid_data':gdata,
            'station_data':sdata,
            'distance':dist
        }
        results['graph_data'] = DC.get_graph_data(gdata,sdata)
        results['stats'] = DC.get_statistics(results['graph_data'][0],results['graph_data'][1])
        context['results'] = results
    return render_to_response(url, context, context_instance=RequestContext(request))

#######################
#SOD programs
######################

def monann(request):
    context = {
        'title': settings.APPLICATIONS['monann'][0]
    }
    url = settings.APPLICATIONS['monann'][2]

    initial,checkbox_vals = set_initial(request, 'monann')
    context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
    #Set graph and plot options
    #Time Serie Table Generation and graph if desired
    if 'formData' in request.POST or (request.method == 'GET' and 'element' in request.GET):
        form = set_form(initial,clean=False)
        form_cleaned = set_form(initial,clean=True)
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
            'element':form_cleaned['element']
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
        App = WRCCClasses.SODApplication('Sodxtrmts', data, app_specific_params=app_params)
        data = App.run_app()
        #Set header
        header = set_sodxtrmts_head(form_cleaned)
        if not data:
            results = {
                'header':'',
                'data':[],
                'data_summary':[],
                'errors': 'No Data found for these parameters'
            }
            context['results'] = results
            return render_to_response(url, context, context_instance=RequestContext(request))
        else:
            header_list = []
            if app_params['statistic_period'] == 'monthly':
                p =  copy.deepcopy(WRCCData.MONTH_NAMES_SHORT_CAP)
            if app_params['statistic_period'] == 'weekly':
                p = range(1,53)
                context['weeks'] = copy.deepcopy(p)
            for m in p:
                header_list.append(str(m))
                #space for data flag slots
                header_list.append(' ')
            results = {
                'header':header,
                'data_indices':'0,1',
                'smry':'individual',
                'running_mean_years':'5',
                'show_range': False,
                'data': [['YEAR'] + header_list + ['ANN', ' ']] + data[0],
                'data_summary':[[' '] + header_list + ['ANN', ' ']] + data[0][-6:]
            }
        #Write data to file for highcharts
        hc_data = WRCCUtils.extract_highcarts_data_monann(results['data'],form_cleaned)
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
        results['chartType'] = graph_dict['chartType']
        context['run_done'] = True
        context['results'] = results
        #Save data table to file for later download
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        json_file = '%s_sodxtrmts.json' %(time_stamp)
        with open(settings.TEMP_DIR + '%s' %(json_file),'w+') as f:
            f.write(json.dumps(results))
        context['json_file'] = json_file
    #Downlaod Table Data
    if 'formDownload' in request.POST:
        data_format = request.POST.get('data_format', 'clm')
        delimiter = request.POST.get('delimiter', 'comma')
        output_file_name = request.POST.get('output_file_name', 'output')
        json_file = request.POST.get('json_file', None)
        with open(settings.TEMP_DIR + json_file, 'r') as f:
            results =  json.load(f)
        context['results'] = results
        DDJ = WRCCToReplace.DownloadDataJob('Sodxtrmts',data_format,delimiter, output_file_name, request=request, json_in_file=settings.TEMP_DIR + json_file)
        return DDJ.write_to_file()

    return render_to_response(url, context, context_instance=RequestContext(request))


def climatology(request):
    context = {
        'title': settings.APPLICATIONS['climatology'][0]
    }
    url = settings.APPLICATIONS['climatology'][2]

    initial, checkbox_vals = set_initial(request,'climatology')
    context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
    if 'formData' in request.POST or (request.method == 'GET' and ('station_id' in request.GET or 'location' in request.GET)):
        form = set_form(request,clean=False)
        form_cleaned = set_form(request,clean=True)
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
                #'sid':WRCCUtils.find_id(form['station_id'], settings.MEDIA_DIR + '/json/US_station_id.json'),
                'start_date':form['start_year'],
                'end_date':form['end_year'],
                'element':form['summary_type']
                }
        app_params = {
                'el_type':form['summary_type'],
                'max_missing_days':form['max_missing_days'],
                'units':form['units']
                }
        if 'location' in form_cleaned.keys():
            data_params['loc'] = form_cleaned['location']
            data_params['grid'] = form_cleaned['grid']
        if 'station_id' in form_cleaned.keys():
            data_params['sid'] = WRCCUtils.find_id(form['station_id'], settings.MEDIA_DIR + '/json/US_station_id.json')
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
            results = dict(results[0])
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
            #Add other params to table_dict
            table_dict['record_start'] = dates_list[0][0:4]
            table_dict['record_end'] = dates_list[-1][0:4]
            if 'sid' in data_params.keys():
                table_dict['title'] = meta_dict['names'][0] + ', ' +\
                    meta_dict['states'][0] + ', ' + table_dict['table_name_long']
                table_dict['subtitle'] = 'Network: ' + meta_dict['networks'][0] + ', ID: ' + str(data_params['sid'])
            if 'loc' in data_params.keys():
                table_dict['title'] = 'Location ' + str(data_params['loc']) + ', ' + table_dict['table_name_long']
                table_dict['subtitle'] = ''
            json_list.append(table_dict)
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        json_file = '%s_sodsumm_%s_%s.json' \
        %(time_stamp,dates_list[0][0:4], dates_list[-1][0:4])
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

###########
#General
###########
def create_kml_file(area_type, overlay_state):
    kml_file_name = overlay_state + '_' + area_type + '.kml'
    kml_file_path = settings.TMP_URL +  kml_file_name
    status = WRCCUtils.generate_kml_file(area_type, overlay_state, kml_file_name, settings.TEMP_DIR)
    return kml_file_path


def set_GET(request):
    try:
        rm = request.method
    except:
        def Get(key, default):
            if key in request.keys():
                return request[key]
            else:
                return default
        return Get

    if rm == 'GET':
        Get = getattr(request.GET, 'get')
    elif rm == 'POST':
        Get = getattr(request.POST, 'get')
    return Get

def set_GET_list(request):
    try:
        rm = request.method
    except:
        def Get(key, default):
            if key in request.keys():
                val = request[key]
                if isinstance(request[key],basestring):
                    val = request[key].replace(' ','').split(',')
                return val
            else:
                return default
        return Get

    if rm == 'GET':
        Getlist = getattr(request.GET, 'getlist')
    elif rm == 'POST':
        Getlist = getattr(request.POST, 'getlist')
    return Getlist

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
            form_error[WRCCData.DISPLAY_PARAMS[field]] = err
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
    header_order =['start_year', 'end_year', '','element']
    #Additional headere items
    if form['element'] in ['gdd', 'hdd', 'cdd']:header_order+=['base_temperature']
    header_order+=['statistic']
    if form['departures_from_averages'] == 'T':
         header_order+=['departures_from_averages', '']
    else:
        header_order+=['']
    if form['statistic'] == 'ndays':
        if form['less_greater_or_between'] == 'l':
            header_order+=['less_greater_or_between','threshold_for_less_or_greater','']
        elif form['less_greater_or_between'] == 'g':
            header_order+=['less_greater_or_between','threshold_for_less_or_greater','']
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
        if key in ['less_greater_or_between','frequency_analysis_type','frequency_analysis', 'departures_from_averages', 'statistic', 'elements','element']:
            header.append([WRCCData.DISPLAY_PARAMS[key], WRCCData.DISPLAY_PARAMS[str(form[key])]])
            if key == 'element':
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
    return header


def set_sodsumm_headers(table_list):
    headers = {}
    def set_header(table):
        rows = []
        if table == 'temp':
            rows.append('<th colspan="16"> <b>Tempearture Statistics</b></th>')
            rows.append('<tr><td colspan="5">-------</td><td colspan="5">Averages</td><td colspan="4">-----------Daily Extremes </td><td colspan="4">----------------Mean Extremes </td><td colspan="4">-----------Number of Days</td></tr>')
        elif table == 'prsn':
            rows.append('<th colspan="15"><b>Precipitation/Snow Statistics</b></th>')
            rows.append('<tr><td colspan="6">----------------------Total Precipitation </td><td colspan="2">---------------------------</td><td colspan="2">Number of Days</td><td colspan="3">----------------Total Snowfall</td></tr>')

        elif table == 'hdd':
            rows.append('<th colspan="14"><b>Heating degree days</b></th>')
            rows.append('<tr><td colspan="14">Output is rounded, unlike NCDC values, which round input.</td></tr>')
            rows.append('<tr><td colspan="14">Degree Days to selected Base Temperatures</td></tr>')
        elif table == 'cdd':
            rows.append('<th colspan="14"><b>Cooling degree days</b></th>')
            rows.append('<tr><td colspan="14">Output is rounded, unlike NCDC values, which round input.</td></tr>')
            rows.append('<tr><td colspan="14">Degree Days to selected Base Temperatures(F)</td></tr>')
        elif table == 'gdd':
            rows.append('<th colspan="15"><b>Growing degree days</b></th>')
            rows.append('<tr><td colspan="15">Output is rounded, unlike NCDC values, which round input.</td>')
            rows.append('<tr><td colspan="15">Growing Degree Days to selected Base Temperatures</td></tr>')
        elif table == 'corn':
            rows.append('<th colspan="15"><b>Corn Growing Degree Days</b></th>')
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
    #find element parameter
    if 'element' in search_params.keys():
        params['elems'] = search_params['element']
    elif 'elements' in search_params.keys():
         params['elems'] = search_params['elements']
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
                    graph_data[idx].append(float(row[k]))
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
                    graph_data[i].append(float(results[table][i+1][k+1]))
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
                    graph_data[i].append(float(results[table][2*i+1][k+2]))
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
        graph_data =[[]]
        for k in range(len(cats)):
            try:
                graph_data[0].append(float(results[table][1][k+2]))
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
                    graph_data[i].append(float(row[k]))
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
                    graph_data[i].append(float(row[k]))
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
    if not 'elements' in form.keys() and not 'element' in form.keys() and not 'elements_string' in form.keys():
        return '', []
    if 'element' in form.keys():
        form_els = form['element']
    if 'elements' in form.keys():
        form_els = form['elements']
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
            el_string = form['elements_string'].replace('  ','')
            el_list = el_string.split(',')
        except:
            return '', []

##################
#Initialization
###################

def join_dicts(d, d_1):
    for key, val in d_1.iteritems():
        d[key]=val


def join_initials(initial,initial_2, checkbox_vals,checkbox_vals_2):
    #combine the graph options with the plot options
    for key, val in initial_2.iteritems():
        initial[key] = val
    for key, val in checkbox_vals_2.iteritems():
        checkbox_vals[key] = val

def set_map_plot_options(request):
    initial = {}
    checkbox_vals = {}
    Get = set_GET(request)
    initial['image_size'] = Get('image_size', 'medium')
    initial['level_number'] = Get('level_number', '5')
    initial['cmap'] = Get('cmap', 'rainbow')
    initial['map_ol'] = Get('map_ol', 'state')
    initial['interpolation'] = Get('interpolation', 'cspline')
    initial['projection'] = Get('projection', 'lcc')
    #set the check box values
    for image_size in ['small', 'medium', 'large', 'larger', 'extra_large', 'wide', 'wider', 'widest']:
        checkbox_vals['image_size' + '_' + image_size + '_selected'] = ''
        if initial['image_size'] == image_size:
            checkbox_vals['image_size' + '_' + image_size + '_selected'] = 'selected'
    for mo in ['county', 'state']:
        checkbox_vals['map_ol' + mo + '_selected'] = ''
        if initial['map_ol'] == mo:
            checkbox_vals['map_ol' + mo + '_selected'] = 'selected'
    for ip in ['cspline', 'none']:
        checkbox_vals['interpolation' + ip + '_selected'] = ''
        if initial['interpolation'] == ip:
            checkbox_vals['interpolation' + ip + '_selected'] = 'selected'
    for p in ['lcc']:
        checkbox_vals['projection' + p + '_selected'] = ''
        if initial['projection'] == p:
            checkbox_vals['projection' + p + '_selected'] = 'selected'
    return initial, checkbox_vals


def set_temporal_summary_initial(request):
    initial = {'req_type':'temporal_summary'}
    checkbox_vals = {}
    Get = set_GET(request)
    Getlist = set_GET_list(request)
    initial['area_type'] = Get('area_type','state')
    initial['area_type_label'] = WRCCData.DISPLAY_PARAMS[initial['area_type']]
    initial['area_type_value'] = Get(str(initial['area_type']), WRCCData.AREA_DEFAULTS[initial['area_type']])
    initial['overlay_state'] = Get('overlay_state', 'nv')
    el_str = Get('elements',None)
    if isinstance(el_str,basestring) and el_str:
        initial['elements']= el_str.replace(' ','').split(',')
    else:
        initial['elements'] = Getlist('elements', ['maxt','mint','pcpn'])
    initial['elements_string'] = ','.join(initial['elements'])
    initial['add_degree_days'] = Get('add_degree_days', 'F')
    initial['degree_days'] = Get('degree_days', 'gdd55,hdd70')
    initial['units'] = Get('units', 'english')
    initial['start_date']  = Get('start_date', week)
    initial['end_date']  = Get('end_date', yesterday)
    initial['grid'] = Get('grid', '1')
    initial['data_summary'] = 'temporal'
    initial['temporal_summary'] = Get('temporal_summary', 'mean')
    initial['show_plot_opts'] = Get('show_plot_opts','T')
    #set the check box values
    for area_type in WRCCData.SEARCH_AREA_FORM_TO_ACIS.keys():
        checkbox_vals[area_type + '_selected'] =''
        if area_type == initial['area_type']:
            checkbox_vals[area_type + '_selected'] ='selected'
    for e in ['maxt','mint','avgt', 'pcpn','gdd','hdd','cdd']:
        checkbox_vals['elements_' + e + '_selected'] =''
        for el in initial['elements']:
            if el == e:
                checkbox_vals['elements_' + e + '_selected'] ='selected'
    for bl in ['T','F']:
        for cbv in ['add_degree_days']:
            checkbox_vals[cbv + '_' + bl + '_selected'] = ''
            if initial[cbv] == bl:
                checkbox_vals[cbv + '_' + bl + '_selected'] = 'selected'
    for u in ['english', 'metric']:
        checkbox_vals['units_' + u + '_selected'] =''
        if u == initial['units']:
            checkbox_vals['units_' +u + '_selected'] ='selected'
    for g in ['1','21','3','4','5','6','7','8','9','10','11','12','13','14','15','16']:
        checkbox_vals['grid_' + g + '_selected'] =''
        if initial['grid'] == g:
            checkbox_vals['grid_' + g + '_selected'] ='selected'
    for st in ['max','min','mean','sum']:
        checkbox_vals['temporal_summary_' + st + '_selected'] =''
        if st == initial['temporal_summary']:
            checkbox_vals['temporal_summary_' + st + '_selected'] ='selected'
    return initial, checkbox_vals

#NEW UTILS
def set_elements(form):
    '''
    Note: all requests and apps work with element lists
    Form key elements should exist
    Given form input we check if elements is key
    if not, check if element is key and add elements to keys
    '''
    if 'elements' not in form.keys():
        if 'element' in form.keys():
            return form['element']
        else:
            return []
    else:
        return form['elements']


def set_form(request, clean=True):
    '''
    Coverts request input to usable form input:
    Deals with unicode issues
    and autofill options for identifiers
    NOTE: elements should always be a list (also when clean = False)
    If Clean == True,
    We also clean up some form fields for submission:
        date fields, convert to yyyymmdd
        window fields, convert to mmdd
        name strings are converted to ids
        Combine elemenst weith degree days
    '''
    try:
        req_method = request.method
    except:
        if isinstance(request,dict):
            req_method = 'dict'
        else:req_method = None
    form= {}
    form['req_method'] = req_method
    #Convert request object to python dictionary
    if req_method == 'dict':
        for key, val in request.iteritems():
            form[str(key)]= val
        #Special case elements, always needs to be list
        if 'element' in request.keys() and not 'elements' in request.keys():
            form['elements'] = [form['element']]
        if 'elements' in request.keys():
            form['elements'] = WRCCUtils.convert_elements_to_list(request['elements'])
    elif req_method == 'POST':
        for key, val in request.POST.items():
            form[str(key)]= val
        #form = dict((str(x),str(y)) for x,y in request.POST.items())
        #Special case elements, always needs to be list
        if 'element' in request.POST.keys() and not 'elements' in request.POST.keys():
            form['elements'] = [str(request.POST['element'])]
        if 'elements' in request.POST.keys():
            #form['elements'] = WRCCUtils.convert_elements_to_list(request.POST['elements'])
            els = request.POST.getlist('elements',request.POST.get('elements','').split(','))
            form['elements'] = [str(el) for el in els]
    elif req_method == 'GET':
        #form = dict((str(x),str(y)) for x,y in request.GET.items())
        for key, val in request.GET.items():
            form[str(key)]= val
        #Special case elements, always needs to be list
        if 'element' in request.GET.keys() and not 'elements' in request.GET.keys():
            form['elements'] = [str(request.GET['element'])]
        if 'elements' in request.GET.keys():
            #form['elements'] = WRCCUtils.convert_elements_to_list(request.GET['elements'])
            form['elements'] = request.GET.get('elements','').split(',')

            '''
            els = request.GET.getlist('elements',request.GET.get('elements','').split(','))
            form['elements'] = [str(el) for el in els]
            '''
    else:
        form = {}
    #Convert unicode to string
    if 'elements' in form.keys():
        form['elements'] = [str(el) for el in form['elements']]
    if 'csrfmiddlewaretoken' in form.keys():
        del form['csrfmiddlewaretoken']
    if 'formData' in form.keys():
        del form['formData']

    if not clean:
        return form
    #Clean up form for submission
    #Clean Dates and windows
    for key in ['start_date', 'end_date', 'start_year', 'end_year','start_window','end_window']:
        if key not in form.keys():
            continue
        if form[key].lower() == 'por':
            if str(key) in ['start_date']:
                k=key; idx = 0;sd = 'por'; ed = form['end_date']
            if str(key) in ['end_date']:
                k=key; idx = 1;ed = 'por'; sd = form['start_date']
            if str(key) in ['start_year']:
                k='start_date'; idx = 0;sd = 'por'
                if form['end_year'].lower() == 'por':ed = 'por'
                else:ed = str(int(form['end_year']) -1) + '-12-31'
            if str(key) in ['end_year']:
                k='end_date'; idx = 1;ed = 'por'
                if form['start_year'].lower() == 'por':sd = 'por'
                else:sd = form['start_year'] + '-01-01'
            if 'element' in form.keys() and not 'elements' in form.keys():
                if form['element'] in ['dtr']:
                    el_list = ['maxt','mint']
                if form['element'] in ['pet']:
                    el_list = ['maxt','mint','pcpn']
            if 'elements' in form.keys() and not 'element' in form.keys():
                if isinstance(form['elements'],basestring):
                    el_list = form['elements'].replace(' ','').split(',')
                else:
                    el_list = form['elements']
            else:
                el_list = None
            if 'station_id' in form.keys():
                stn_id = WRCCUtils.find_id(str(form['station_id']),settings.MEDIA_DIR +'json/US_station_id.json')
                form[k] = WRCCUtils.find_valid_daterange(stn_id, start_date=sd, end_date=ed, el_list=el_list, max_or_min='max')[idx]
            else:
                form[str(key)] = str(form[key]).replace('-','').replace(':','').replace('/','').replace(' ','')
        else:
            form[str(key)] = str(form[key]).replace('-','').replace(':','').replace('/','').replace(' ','')

    #Convert user input of area names to ids
    for key in ['station_id','county', 'basin', 'county_warning_area', 'climate_division']:
        if not key in form.keys():
            continue
        form['user_area_id'] =  form[key]
        form[key] = WRCCUtils.find_id(form[key],settings.MEDIA_DIR +'json/US_' + key + '.json')
    if not 'user_area_id' in form.keys():
        try:
            form['user_area_id'] = form[form['area_type']]
        except:
            try:
                form['user_area_id'] =  form[form['data_type']]
            except:
                pass
    #station_ids is special case
    if 'station_ids' in form.keys():
        stn_ids = ''
        stn_list = form['station_ids'].rstrip(',').split(',')
        #Remove leading spaces from list items
        stn_list = [v.lstrip(' ').rstrip(' ') for v in stn_list]
        stn_ids = WRCCUtils.find_ids(stn_list,settings.MEDIA_DIR +'json/US_' + 'station_id' + '.json')
        form['station_ids'] = stn_ids
    #set data summary if needed
    if 'data_summary' not in form.keys():
        if 'temporal_summary' in form.keys():
            form['data_summary'] = 'temporal'
        if 'spatial_summary' in form.keys():
            form['data_summary'] = 'spatial'
    if 'date_format' not in form.keys():
        form['date_format'] = 'dash'
    #Combine elements
    if 'add_degree_days' in form.keys() and form['add_degree_days'] == 'T':
        for dd in form['degree_days'].replace(' ','').split(','):
            '''
            if form['units'] == 'metric':
                el_strip, base_temp = WRCCUtils.get_el_and_base_temp(dd)
                form['elements'].append(el_strip + str(WRCCUtils.convert_to_english('base_temp',base_temp)))
            else:
                form['elements'].append(dd)
            '''
            form['elements'].append(dd)
    return form


#Initializers
def set_initial(request,req_type):
    '''
    Set html form
    Args:
        request: django request object
        req_type: application, one of
            single_lister, multi_lister, station_finder
            map_overlay,
            sf_download
            spatial_summary, temporal_summary
            monann, climatology
            data_comparison, liklihood
    Returns:
        two dictionaries
        initial: form input
        checkbox_vals: values for checkboxes (selected or '')
    '''
    initial = {}
    initial['req_type'] = req_type
    checkbox_vals = {}
    Get = set_GET(request)
    Getlist = set_GET_list(request)
    #Set area type: station_id(s), location, basin,...
    area_type = None
    if req_type in ['single_lister','climatology','monann', 'interannual']:
        initial['area_type'] = Get('area_type','station_id')
    elif req_type in ['data_comparison']:
        initial['area_type'] = 'location'
    else:
        initial['area_type'] = Get('area_type','state')
    #Set todays date parameters
    initial['today_year'] = today_year
    initial['today_month'] = today_month
    initial['today_day'] = today_day
    #Set area depending on area_type
    if req_type == 'data_comparison':
        location = Get('location',None)
        station_id = Get('station_id',None)
        if location is None and station_id is not None:
            #Link from station finder,
            #set location to station lon, lat if we are
            stn_id = WRCCUtils.find_id(station_id,settings.MEDIA_DIR + '/json/US_station_id.json')
            meta = AcisWS.StnMeta({'sids':stn_id,'meta':'ll'})
            ll = None
            ll = str(meta['meta'][0]['ll'][0]) + ',' + str(meta['meta'][0]['ll'][1])
            initial['location'] = ll
            '''
            if meta and 'meta' in meta.keys():
                if 'll' in meta['meta'][0].keys() and len(meta['meta'][0]['ll']) == 2:
                    ll = str(meta['meta'][0]['ll'][0]) + ',' + str(meta['meta'][0]['ll'][1])
            if ll:
                initial['location'] = ll
            '''
        else:
            initial[str(initial['area_type'])] = Get(str(initial['area_type']), WRCCData.AREA_DEFAULTS[initial['area_type']])
    else:
        initial[str(initial['area_type'])] = Get(str(initial['area_type']), WRCCData.AREA_DEFAULTS[initial['area_type']])
    initial['area_type_label'] = WRCCData.DISPLAY_PARAMS[initial['area_type']]
    initial['area_type_value'] = initial[str(initial['area_type'])]

    #If station_finder download, we need to set the station_ids
    if req_type == 'sf_download':
        initial['station_ids'] = Get('station_ids','')

    #Set data type and map parameters
    if initial['area_type'] in ['station_id']:
        initial['autofill_list'] = 'US_' + initial['area_type']
        initial['data_type'] = 'station'
    elif initial['area_type'] in ['location']:
        initial['data_type'] = 'grid'
    elif initial['area_type'] in ['basin','county_warning_area','county','climate_division','state','shape']:
        initial['autofill_list'] = 'US_' + initial['area_type']
        initial['data_type'] = Get('data_type','station')
    #Set up map parameters
    initial['overlay_state'] = Get('overlay_state','nv').lower()
    initial['host'] = settings.HOST
    #Create kml files for oerlay state
    for at in ['basin', 'county', 'county_warning_area', 'climate_division']:
        kml_file_path = create_kml_file(at, initial['overlay_state'])
    if initial['area_type'] in ['basin', 'county', 'county_warning_area', 'climate_division']:
        initial['kml_file_path'] = create_kml_file(initial['area_type'], initial['overlay_state'])

    #Set element(s)--> always as list if multiple
    if req_type == 'map_overlay':
        initial['elements'] = Get('elements','maxt,mint,pcpn').split(',')
    elif req_type in ['monann','data_comparison', 'interannual']:
        initial['element'] = Get('element','pcpn')
    else:
        els = Getlist('elements',None)
        if not els:
            els = Get('elements',None)
            if not els:
                els = ['maxt','mint','pcpn']
            elif isinstance(els, basestring):
                els = els.replace(' ','').split(',')
        elif isinstance(els, list) and  len(els) == 1 and len(els[0].split(',')) > 1:
            els = els[0].replace(' ','').split(',')
        elif isinstance(els, basestring):
            els = els.replace(' ','').split(',')
        initial['elements'] = els

    #Set units
    initial['units'] = Get('units','english')

    #Set degree days
    if req_type not in ['station_finder', 'monann', 'climatology', 'data_comparison', 'interannual']:
        initial['add_degree_days'] = Get('add_degree_days', 'F')
        if initial['units'] == 'metric':
            initial['degree_days'] = Get('degree_days', 'gdd13,hdd21')
        else:
            initial['degree_days'] = Get('degree_days', 'gdd55,hdd70')

    #Set dates
    if req_type in ['monann','climatology']:
        initial['start_year']  = Get('start_year', 'POR')
        initial['end_year']  = Get('end_year', 'POR')
    elif req_type in ['interannual']:
        initial['start_year']  = Get('start_year', '1970')
        initial['end_year']  = Get('end_year', '1999')
        if initial['area_type'] == 'station_id':
            initial['min_year'] = Get('min_year','1850')
            initial['max_year'] = Get('max_year', str(int(today_year) + 1))
        if initial['area_type'] == 'location':
            initial['min_year'] = Get('min_year','1970')
            initial['max_year'] = Get('max_year', '2000')
        initial['start_month']  = Get('start_month', '1')
        initial['end_month']  = Get('end_month', '1')
        initial['start_day']  = Get('start_day', '1')
        initial['end_day']  = Get('end_day', '31')
    else:
        initial['start_date']  = Get('start_date', WRCCUtils.format_date_string(fourtnight,'-'))
        initial['end_date']  = Get('end_date', WRCCUtils.format_date_string(yesterday,'-'))
    #data windows and flags
    if req_type in ['single_lister', 'multi_lister']:
        initial['start_window'] = Get('start_window', '01-01')
        initial['end_window'] = Get('end_window','01-31')
        initial['temporal_resolution'] = Get('temporal_resolution','dly')
        initial['show_flags'] = Get('show_flags', 'F')
        initial['show_observation_time'] = Get('show_observation_time', 'F')
    #data summaries
    if req_type in  ['temporal_summary', 'interannual']:
        initial['data_summary'] = Get('data_summary', 'temporal')
    elif req_type in ['spatial_summary','multi_lister']:
        initial['data_summary'] = Get('data_summary', 'spatial')
    else:
        initial['data_summary'] = Get('data_summary', 'none')
    if req_type in ['single_lister', 'multi_lister','temporal_summary', 'interannual']:
        if req_type == 'interannual':
            initial['temporal_summary'] = Get('temporal_summary', 'sum')
        else:
            initial['temporal_summary'] = Get('temporal_summary', 'mean')
    if req_type in ['single_lister', 'multi_lister','spatial_summary']:
        initial['spatial_summary'] = Get('spatial_summary', 'mean')
    if req_type not in ['station_finder', 'sf_download']:
        initial['grid'] = Get('grid','1')

    #download options
    initial['data_format'] = Get('data_format', 'html')
    initial['date_format'] = Get('date_format', 'dash')
    initial['delimiter'] = Get('delimiter', 'space')
    initial['output_file_name'] = Get('output_file_name', 'Output')
    initial['user_name'] = Get('user_name', 'Your Name')
    initial['user_email'] = Get('user_email', 'Your Email')

    #Set app specific params
    if req_type in ['spatial_summary', 'monann','interannual','data_comparison']:
        initial['show_running_mean'] = Get('show_running_mean','T')
        if req_type in ['spatial_summary','data_comparison']:
            initial['running_mean_days'] = Get('running_mean_days', '9')
        if req_type in ['monann','interannual']:
            initial['running_mean_years'] = Get('running_mean_years', '5')
    if req_type in ['monann','climatology','sf_link']:
        initial['max_missing_days']  = Get('max_missing_days', '5')
    if req_type == 'station_finder':
        initial['elements_constraints'] = Get('elements_constraints', 'all')
        initial['dates_constraints']  = Get('dates_constraints', 'all')
    if req_type in  ['monann','sf_link']:
        initial['start_month'] = Get('start_month','01')
        initial['statistic'] = Get('statistic','msum')
        initial['less_greater_or_between'] = Get('less_greater_or_between','b')
        initial['threshold_low_for_between'] = Get('threshold_low_for_between',0.01)
        initial['threshold_high_for_between'] = Get('threshold_high_for_between',0.1)
        initial['threshold_for_less_than'] = Get('threshold_for_less_than',1)
        initial['threshold_for_greater_than'] = Get('threshold_for_greater_than',1)
        initial['departures_from_averages'] = Get('departures_from_averages','F')
        initial['frequency_analysis'] = Get('frequency_analysis','F')
        #Set initial plot options
        initial['plot_type'] = Get('plot_type','individual')
        initial['plot_months'] = Get('plot_months','0,1')
    if req_type == 'monann':
        initial['base_temperature'] = Get('base_temperature','65')
        initial['statistic_period'] = Get('statistic_period','monthly')
    if req_type in ['climatology','sf_link']:
        initial['summary_type'] = Get('summary_type', 'all')


    #Checkbox vals
    checkbox_vals['state_' + initial['overlay_state'] + '_selected'] = 'selected'
    if 'elements_constraints' in initial.keys() and 'dates_constraints' in initial.keys():
        for b in ['any', 'all']:
            checkbox_vals['elements_' + b  + '_selected'] =''
            checkbox_vals['dates_' + b  + '_selected'] =''
            if initial['elements_constraints'] == b:
                checkbox_vals['elements_' + b  + '_selected'] ='selected'
            if initial['dates_constraints'] == b:
                checkbox_vals['dates_' + b  + '_selected'] ='selected'
    if 'area_type' in initial.keys():
        for area_type in WRCCData.SEARCH_AREA_FORM_TO_ACIS.keys() + ['none']:
            checkbox_vals[area_type + '_selected'] =''
            if area_type == initial['area_type']:
                checkbox_vals[area_type + '_selected'] ='selected'
    if 'data_type' in initial.keys():
        for data_type in ['station','grid']:
            checkbox_vals['data_type_' + data_type + '_selected'] =''
            if data_type == initial['data_type']:
                checkbox_vals['data_type_' + data_type + '_selected'] ='selected'
    if 'elements' in initial.keys():
        for element in initial['elements']:
            checkbox_vals['elements_' + element + '_selected'] ='selected'
            '''
            for el in initial['elements']:
                if str(el) == element:
                    checkbox_vals['elements_' + element + '_selected'] ='selected'
            '''
    if 'element' in initial.keys():
        checkbox_vals['element_' + initial['element'] + '_selected'] ='selected'
    if 'data_format' in initial.keys():
        for df in ['clm', 'dlm','xl', 'html']:
            checkbox_vals['data_format_' + df + '_selected'] =''
            if df == initial['data_format']:
                checkbox_vals['data_format_' + df + '_selected'] ='selected'
    if 'units' in initial.keys():
        for u in ['english', 'metric']:
            checkbox_vals['units_' + u + '_selected'] =''
            if u == initial['units']:
                checkbox_vals['units_' +u + '_selected'] ='selected'
    if 'data_summary' in initial.keys():
        for ds in ['none','windowed_data','temporal', 'spatial']:
            checkbox_vals['data_summary_' + ds + '_selected'] =''
            if ds == initial['data_summary']:
                checkbox_vals['data_summary_' + ds + '_selected'] ='selected'
    if 'temporal_summary' in initial.keys():
        for st in ['max','min','mean','sum','median']:
            checkbox_vals['temporal_summary_' + st + '_selected'] =''
            if st == initial['temporal_summary']:
                checkbox_vals['temporal_summary_' + st + '_selected'] ='selected'
    if 'spatial_summary' in initial.keys():
        for st in ['max','min','mean','sum','median']:
            checkbox_vals['spatial_summary_' + st + '_selected'] =''
            if st == initial['spatial_summary']:
                checkbox_vals['spatial_summary_' + st + '_selected'] ='selected'
    if 'statistic' in initial.keys():
        checkbox_vals[initial['statistic'] + '_selected'] ='selected'
        for lgb in ['l', 'g', 'b']:
            if initial['less_greater_or_between'] == lgb:
                checkbox_vals[lgb + '_selected'] ='selected'
        #set plot type and plot months
        plot_months = initial['plot_months'].split(',')
        for m_idx in range(0,12):
            if str(m_idx) in plot_months:
                checkbox_vals['chart_data_indices_' +  str(m_idx) + '_selected'] ='selected'
        checkbox_vals['chart_smry_' +  initial['plot_type'] + '_selected'] = 'selected'
    if 'statistic_period' in initial.keys():
        checkbox_vals[initial['statistic_period'] + '_selected'] =''
        for sp in ['monthly', 'weekly']:
            checkbox_vals[sp  + '_selected'] =''
            if initial['statistic_period'] == sp:
                checkbox_vals[initial['statistic_period'] + '_selected'] ='selected'

    if 'date_format' in initial.keys():
        for df in ['none', 'dash','colon', 'slash']:
            checkbox_vals['date_format_' + df + '_selected'] =''
            if df == initial['date_format']:
                checkbox_vals['date_format_' + df + '_selected'] ='selected'
    if 'temporal_resolution' in initial.keys():
        for tr in ['dly','mly','yly']:
            checkbox_vals['temporal_resolution_' + tr + '_selected'] = ''
            if tr == initial['temporal_resolution']:
                checkbox_vals['temporal_resolution_' + tr + '_selected'] = 'selected'
    if 'delimiter' in initial.keys():
        for dl in ['comma', 'tab', 'space', 'colon', 'pipe']:
            checkbox_vals[dl + '_selected'] =''
            if dl == initial['delimiter']:
                checkbox_vals[dl + '_selected'] ='selected'
    if 'show_flags' in initial.keys():
        for bl in ['T','F']:
            checkbox_vals['show_flags_' + bl + '_selected'] = ''
            if initial['show_flags'] == bl:
                checkbox_vals['show_flags_' + bl + '_selected'] = 'selected'
    if 'show_observation_time' in initial.keys():
        for bl in ['T','F']:
            checkbox_vals['show_observation_time_' + bl + '_selected'] = ''
            if initial['show_observation_time'] == bl:
                checkbox_vals['show_observation_time' + '_' + bl + '_selected'] = 'selected'
    if 'add_degree_days' in initial.keys():
        for bl in ['T','F']:
            checkbox_vals['add_degree_days_' + bl + '_selected'] = ''
            if initial['add_degree_days'] == bl:
                checkbox_vals['add_degree_days_' + bl + '_selected'] = 'selected'
    if 'show_running_mean' in initial.keys():
        for bl in ['T','F']:
            checkbox_vals['show_running_mean_' + bl + '_selected'] = ''
            if initial['show_running_mean'] == bl:
                checkbox_vals['show_running_mean_' + bl + '_selected'] = 'selected'
    if 'grid' in initial.keys():
        for g in ['1','21','3','4','5','6','7','8','9','10','11','12','13','14','15','16']:
            checkbox_vals['grid_' + g + '_selected'] =''
            if initial['grid'] == g:
                checkbox_vals['grid_' + g + '_selected'] ='selected'
    if req_type == 'climatology':
        for st in ['all','temp','prsn','both','hc','g']:
            checkbox_vals[st + '_selected'] =''
            if st == initial['summary_type']:
                checkbox_vals[st + '_selected'] ='selected'
    return initial,checkbox_vals
