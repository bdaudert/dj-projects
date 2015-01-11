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

#My modules
import WRCCUtils, AcisWS, WRCCDataApps, WRCCClasses, WRCCData, WRCCFormCheck
import scenic.forms as forms

#Set dates
today = WRCCUtils.set_back_date(0)
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

def help(request):
    context = {
        'title': 'Help Tool',
        'icon':'Magnify.png'
    }
    return render_to_response('scenic/help/home.html', context, context_instance=RequestContext(request))

def main_map(request):
    context = {
        'title': 'Resources',
        'state_choices': ['AZ', 'CA', 'CO', 'NM', 'NV', 'UT'],
        'icon':'Network.png'
    }
    context['json_file'] = 'Network.json'
    return render_to_response('scenic/main_map.html', context, context_instance=RequestContext(request))

def resources(request):
    context = {
        'title': 'Resources'
    }
    return render_to_response('scenic/resources.html', context, context_instance=RequestContext(request))

def resources_station(request):
    context = {
        'title': 'Station Data Resources'
    }
    return render_to_response('scenic/resources_station.html', context, context_instance=RequestContext(request))

def gallery(request):
    context = {
        'title': 'Gallery'
    }
    return render_to_response('scenic/gallery.html', context, context_instance=RequestContext(request))

def resources_grid(request):
    context = {
        'title': 'Gridded Data Resources'
    }
    return render_to_response('scenic/resources_grid.html', context, context_instance=RequestContext(request))

#Temp home page fpr Kelly to look at
def main(request):
    context = {
        'title': 'Resources',
        'state_choices': ['AZ', 'CA', 'CO', 'NM', 'NV', 'UT'],
        'icon':'Network.png'
    }
    state = request.GET.get('state_key', None)
    element = request.GET.get('element', None)
    if state is None:state = 'NV'
    if element is None: element='mint'
    month = int(datetime.date.today().month)
    if len(str(month)) == 1:
        mon = '0%s' %str(month)
    else:
        mon = str(month)
    day  = str(WRCCData.MONTH_LENGTHS[month -1])
    if len(day) == 1:
        day = '0%s' %day
    context['day'] = day
    context['month'] = month
    context['mon'] = mon
    context['month_name'] = WRCCData.MONTH_NAMES_LONG[month - 1]
    context['state'] = state
    context['element'] = element
    return render_to_response('scenic/main_maves.html', context, context_instance=RequestContext(request))

def about_us(request):
    context = {
        'title': 'About Us',
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

def data_home(request):
    context = {
        'title': 'Data Access'
    }
    return render_to_response('scenic/data/home.html', context, context_instance=RequestContext(request))

def single_point_prods(request):
    context = {
        'title': 'Single Point Products'
    }
    return render_to_response('scenic/data/single/home.html', context, context_instance=RequestContext(request))

def multi_point_prods(request):
    context = {
        'title': 'Multi Point Products'
    }
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
            DDJ = WRCCClasses.DownloadDataJob(app_name,data_format,delimiter, output_file_name, request=request, json_in_file=settings.TEMP_DIR + json_in_file_name)
            if data_format in ['clm', 'dlm','xl']:
                return DDJ.write_to_file()
            else:
                response = DDJ.write_to_file()
                context['response'] = response
    return render_to_response('scenic/download.html', context, context_instance=RequestContext(request))

def single_lister(request):
    context = {
        'title': 'Data Lister',
    }
    initial, checkbox_vals = set_initial_lister(request, 'single')
    context['initial'] = initial; context['checkbox_vals'] =  checkbox_vals
    return render_to_response('scenic/data/single/lister.html', context, context_instance=RequestContext(request))

def multi_lister(request):
    context = {
        'title': 'Data Lister',
    }
    initial, checkbox_vals = set_initial_lister(request, 'multi')
    context['initial'] = initial; context['checkbox_vals'] =  checkbox_vals
    #Set initial overlay state for overlay map
    context[initial['overlay_state'].lower() + '_selected'] = 'selected'

    #Overlay maps
    if 'formOverlay' in request.POST:
        context['need_overlay_map'] = True
        form = set_form(request,clean=False)
        context['xx'] = form
        initial, checkbox_vals = set_initial_lister(form,'multi')
        #checkbox_vals[form['area_type'] + '_selected'] = 'selected'
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
        context[initial['overlay_state'] + '_selected'] = 'selected'
    return render_to_response('scenic/data/multi/lister.html', context, context_instance=RequestContext(request))

def data_station_temp(request):
    context = {
        'title': 'Data download in progess...',
    }
    if request.method == 'GET':
        context['params_json'] = request.GET.get('params_json',None)
        context['station_ids'] = request.GET.get('station_ids',None)
    return render_to_response('scenic/data/station/data_temp.html', context, context_instance=RequestContext(request))

def data_station(request):
    context = {
        'title': 'Historic Station Data Lister (Daily)',
    }
    if request.method == 'GET' and  'params_json' in  request.GET and 'station_ids' in request.GET:
        #We are linking from station_finder
        params_json = request.GET.get('params_json')
        station_ids = request.GET.get('station_ids')
        initial = WRCCUtils.load_json_data_from_file(settings.TEMP_DIR + params_json)
        context['form_message'] = True
        context['form_message_sf'] = True
        initial['station_ids'] = station_ids
        initial, checkbox_vals = set_data_station_initial(initial)
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
        user_params_list, user_params_dict = set_user_params(initial, 'data_station')
        context['user_params_list'] = user_params_list;context['user_params_dict'] = user_params_dict
    else:
        #Set up maps if needed
        initial, checkbox_vals = set_data_station_initial(request)
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
        context['host'] = settings.HOST
        context['area_type'] = initial['select_stations_by']
        kml_file_path = create_kml_file('basin', 'NV')
        kml_file_path = create_kml_file('county', 'NV')
        kml_file_path = create_kml_file('county_warning_area', 'NV')
        kml_file_path = create_kml_file('climate_division', 'NV')
        kml_file_name = initial['overlay_state'] + '_' + initial['select_stations_by'] + '.kml'
        context[initial['select_stations_by']] = WRCCData.AREA_DEFAULTS[initial['select_stations_by']]
        context[initial['overlay_state'] + '_selected'] = 'selected'
        context[initial['select_stations_by']] = WRCCData.AREA_DEFAULTS[initial['select_stations_by']]
        initial, checkbox_vals = set_data_station_initial(request)
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals

    #if 'formData' in request.POST or (request.method == 'GET' and ('elements' in request.GET or 'params_json' in  request.GET)):
    if 'formData' in request.POST or (request.method == 'GET' and 'elements' in request.GET):
        '''
        params_json = request.GET.get('params_json',None)
        station_ids = request.GET.get('station_ids',None)
        if request.method == 'GET':
            if params_json:
                #We are linking from station_finder
                form_initial = WRCCUtils.load_json_data_from_file(settings.TEMP_DIR + params_json)
            else:
                form_initial = set_form_old(request,clean=False)
            context['form_message'] = True
        if params_json:
            if station_ids:
                form_initial['station_ids'] = station_ids
            form = set_form_old(form_initial,clean=False)
            form_cleaned = set_form_old(form_initial)
        else:
            form = set_form_old(request,clean=False)
            form_cleaned = set_form_old(request)
        '''
        form = set_form_old(request,clean=False)
        form_cleaned = set_form_old(request)
        #user_params_list, user_params_dict = set_user_params(form_initial, 'data_station')
        user_params_list, user_params_dict = set_user_params(form, 'data_station')
        context['user_params_list'] = user_params_list;context['user_params_dict'] = user_params_dict
        #Back Button/download files issue fix:
        #if select_stations_by none, find it
        if not 'select_stations_by' in form_cleaned.keys() or form_cleaned['select_stations_by'] not in form_cleaned.keys():
            for key in WRCCData.SEARCH_AREA_FORM_TO_ACIS.keys():
                if key in form.keys():
                    form['select_stations_by'] = key
                    form_cleaned['select_stations_by'] = key
                    break
        context['form_cleaned'] = form_cleaned
        #Set wich apps to link to:
        if len(form_cleaned['elements'].replace(' ','').split(',')) == 1:
            if 'station_id' in form.keys():
                context['link_to_all'] = True
        elif len(form_cleaned['elements'].replace(' ','').split(',')) >= 1 and 'station_id' in form.keys():
            context['link_to_mon_aves'] = True
        #Set params for external links
        if 'station_id' in form.keys():
            monthly_aves_params_list, monthly_aves_params_dict = set_user_params(form, 'monthly_aves')
            sodsumm_params_list, sodsumm_params_dict = set_user_params(form, 'sodsumm')
            sodxtrmts_params_list, sodxtrmts_params_dict = set_user_params(form, 'sodxtrmts')
            context['sodsumm_params_list'] = sodsumm_params_list
            context['sodsumm_params_dict']=sodsumm_params_dict
            context['monthly_aves_params_list'] = monthly_aves_params_list
            context['monthly_aves_params_dict']= monthly_aves_params_dict
            context['sodxtrmts_params_dict'] = sodxtrmts_params_dict
            context['sodxtrmts_params_list']= sodxtrmts_params_list
        if 'location' in form_cleaned.keys():
            sodxtrmts_params_list, sodxtrmts_params_dict = set_user_params(form, 'sodxtrmts')
            context['sodxtrmts_params_dict'] = sodxtrmts_params_dict
            context['sodxtrmts_params_list']= sodxtrmts_params_list
        #Set element_list and unit_dict context for htl loops
        if not 'elements' in form.keys():
            context['element_list'] = []
            context['unit_dict'] = {}
        else:
            unit_dict = {}
            el_name_dict = {}
            context['element_list'] = form['elements']
            for el in form['elements']:
                if 'units' in form.keys() and form['units'] == 'metric':
                    el_strip, base_temp = WRCCUtils.get_el_and_base_temp(el,units='metric')
                else:
                    el_strip, base_temp = WRCCUtils.get_el_and_base_temp(el)
                if 'units' in form.keys() and  form['units'] == 'metric' and base_temp:
                    base_temp = WRCCUtils.convert_to_metric('maxt',base_temp)
                if not base_temp:base_temp=''
                el_name_dict[el] = WRCCData.MICHELES_ELEMENT_NAMES[str(el_strip)] + str(base_temp)
                if 'units' in form.keys() and  form['units'] == 'metric':
                    unit_dict[el] = WRCCData.UNITS_METRIC[el_strip]
                    unit_dict['elev']= WRCCData.UNITS_METRIC['elev']
                else:
                    unit_dict[el] = WRCCData.UNITS_ENGLISH[el_strip]
                    unit_dict['elev']= WRCCData.UNITS_ENGLISH['elev']
            context['el_name_dict'] = el_name_dict
            context['unit_dict'] = unit_dict
        #Set form initials
        initial,checkbox_vals = set_data_station_initial(form)
        context['initial'] = initial;context['checkbox_vals']  = checkbox_vals
        display_params_list, params_dict = set_data_station_params(form)
        context['display_params_list'] = display_params_list;context['params_dict'] = params_dict
        fields_to_check = [form_cleaned['select_stations_by'],'start_date', \
        'end_date','degree_days', 'elements']

        #Check for form errors
        if 'user_email' in form_cleaned.keys():
            fields_to_check.append('user_email')
            context['large_request'] = True
        form_error = check_form(form_cleaned, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            if form_cleaned['select_stations_by'] in ['basin','county','county_warning_area', 'climate_division']:
                context['need_overlay_map'] = True
            kml_file_path = create_kml_file(form['select_stations_by'], form['overlay_state'])
            context['kml_file_path'] = kml_file_path
            return render_to_response('scenic/data/station/home.html', context, context_instance=RequestContext(request))
        #Check if data request is large,
        '''
        We find enclosing bbox of the request and assume
        that stations are placed evenly on a 50km grid
        to crudely estimate the size of the data request
        Large data requests are between 0.00098GB and 1GB
        We gather params and ask user for name and e-mail and
        notify user that request will be processed offline.
        Data requests larger than 1GB will not be processed.
        Data requests smaller than 0.00098GB will be processed on the fly.
        '''
        sdate = form_cleaned['start_date']
        edate = form_cleaned['end_date']
        if sdate.lower() == 'por' or edate.lower() == 'por':
            s_date = WRCCUtils.date_to_datetime('19500101')
            e_date = WRCCUtils.date_to_datetime('19991231')
        else:
            s_date = WRCCUtils.date_to_datetime(sdate)
            e_date = WRCCUtils.date_to_datetime(edate)
        #days = (e_date - s_date).days
        try:
            days = (e_date - s_date).days
        except:
            days = 50*356
        #Find potential data size: we find enclosing bbox and assume
        #stations are placed evenly on a 50km grid
        bbox = []
        if 'shape' in form.keys():
            t,bbox = WRCCUtils.get_bbox(form['shape'])
        elif form['select_stations_by'] in ['basin', 'state', 'climate_division', 'county', 'county_warning_area']:
            sa = WRCCData.SEARCH_AREA_FORM_TO_ACIS[form['select_stations_by']]
            bbox = AcisWS.get_acis_bbox_of_area(sa, form_cleaned[form_cleaned['select_stations_by']])
        if 'station_ids' in form.keys():
            num_lats, num_lons = 1, len(form['station_ids'].split(','))
        else:
            num_lats, num_lons = WRCCUtils.find_num_lls(bbox,'4')
        num_data_points = days * num_lats *num_lons * len(form_cleaned['elements'])
        num_giga_bytes = 1 * num_data_points /float(1024**3)
        num_mega_bytes = round(1 * num_data_points /float(1024**2),2)
        '''
        if 2 * 0.00098 < num_giga_bytes:
            ldr = 'At the moment we do not accept data requests producing \
                more than 2MB of data. Your request size is approximately %s MB. \
                We will support larger requests in the near future. \
                Thank you for your patience!' %str(num_mega_bytes)
            context['too_large'] = ldr
            return render_to_response('scenic/data/station/home.html', context, context_instance=RequestContext(request))
        '''
        if 'user_name' and 'user_email' in form_cleaned.keys():
            ldr = \
                'Data request submitted successfully. \n \
                Notification will be sent to %s when the request has been processed!' %form_cleaned['user_email']
            #Process request offline
            json_file = form_cleaned['output_file_name'] + settings.PARAMS_FILE_EXTENSION
            WRCCUtils.load_data_to_json_file(settings.DATA_REQUEST_BASE_DIR +json_file, form_cleaned)
            #WRCCUtils.load_data_to_json_file(settings.DATA_REQUEST_BASE_DIR +json_file, json_dict)
            context['large_request'] = ldr
            return render_to_response('scenic/data/station/home.html', context, context_instance=RequestContext(request))
        elif num_giga_bytes > 2:
            ldr = 'At the moment we do not accept data requests producing \
                more than 2GB of data. Your request size is approximately %s GB' %str(num_giga_bytes)
            context['too_large'] = ldr
            return render_to_response('scenic/data/station/home.html', context, context_instance=RequestContext(request))
        elif 0.00098 < num_giga_bytes and  num_giga_bytes < 2:
            ldr = \
                'You requested a large amount of data. \
                We estimated %s MB. \
                Please provide your name and email and resubmit the form.\
                we will process your request off-line and \
                notify you when your request has been processed. \
                Thank you for your patience!' %str(num_mega_bytes)

            context['large_request'] = ldr
            return render_to_response('scenic/data/station/home.html', context, context_instance=RequestContext(request))
        context['large_request'] = False
        #Data request
        resultsdict = AcisWS.get_station_data(form_cleaned, 'sodlist_web')
        #Format data
        resultsdict = WRCCUtils.format_station_data(resultsdict, form_cleaned)
        context['results'] = resultsdict
        # If request successful, get params for link to apps page
        context['stn_idx'] = [i for i in range(len(resultsdict['stn_ids']))] #for html looping
        if 'station_ids' in form_cleaned.keys():
            if len(form_cleaned['station_ids'].split(',')) != len(resultsdict['stn_ids']):
                stn_error = 'Data could not be found for these stations: '
                missing_stations =''
                results_ids = []
                results_names = []
                for idx in range(len(resultsdict['stn_ids'])):
                    for id_net in resultsdict['stn_ids'][idx]:
                        results_ids.append(id_net.split(' ')[0])
                    results_names.append(resultsdict['stn_names'][idx])
                stn_list = form_cleaned['station_ids'].split(',')
                stn_names = form['station_ids'].replace(' ', '').split(',')
                for stn_idx, stn_id in enumerate(stn_list):
                    if stn_id not in results_ids:
                        missing_stations+=  stn_names[stn_idx] + ', '
                missing_stations = missing_stations.rstrip(', ')
                stn_error+= missing_stations
                context['station_ids_error'] = stn_error
                resultsdict['station_ids_error'] = stn_error
        if 'data_format' not in form_cleaned.keys():
            form_cleaned['data_format'] == 'html'
        if form_cleaned['data_format'] != 'html':
            return WRCCUtils.write_station_data_to_file(resultsdict,params_dict,request=request)
        else:
            #Write results to json file for later download
            json_dict = {
                'params_dict':params_dict,
                'display_params_list':display_params_list,
                'resultsdict':resultsdict
            }
            time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
            json_file = '%s_data_station.json' %(time_stamp)
            json_dict['json_file'] = json_file
            json_dict['JSON_URL'] = settings.TEMP_DIR
            results_json = json.dumps(json_dict)
            with open(settings.TEMP_DIR + '%s' %(json_file),'w+') as f:
                f.write(results_json)
            context['json_file'] = json_file

    #Overlay maps
    if 'formOverlay' in request.POST:
        context['need_overlay_map'] = True
        form = set_form_old(request,clean=False)
        initial, checkbox_vals = set_data_station_initial(request)
        #Override initial where needed
        initial['select_stations_by'] = form['select_overlay_by']
        checkbox_vals[form['select_overlay_by'] + '_selected'] = 'selected'
        #context['checked'] = form['select_overlay_by'] + '_selected'
        initial['area_type_value'] = WRCCData.AREA_DEFAULTS[form['select_overlay_by']]
        initial[form['select_overlay_by']] = WRCCData.AREA_DEFAULTS[form['select_overlay_by']]
        initial['area_type_label'] = WRCCData.DISPLAY_PARAMS[form['select_overlay_by']]
        initial['autofill_list'] = 'US_' + form['select_overlay_by']
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
        context[form['overlay_state'] + '_selected'] = 'selected'
        kml_file_path = create_kml_file(form['select_overlay_by'], form['overlay_state'])
        context['kml_file_path'] = kml_file_path
        context['area_type'] = form['select_overlay_by']
        context['host'] = settings.HOST

    #Downlaod Table Data
    if 'formDownload' in request.POST:
        form = set_form_old(request,clean=False)
        json_file = request.POST.get('json_file', None)
        if not json_file:
            results = {'error':'No json file found for data download.'}
            return render_to_response('scenic/data/station/home.html', context, context_instance=RequestContext(request))
        with open(settings.TEMP_DIR + json_file, 'r') as f:
            json_dict =  json.load(f)
            #Overwrite download options
            json_dict['params_dict']['data_format'] = form['data_format_download']
            json_dict['params_dict']['delimiter'] = form['delimiter_download']
            json_dict['params_dict']['output_file_name'] = form['output_file_name_download']
        return WRCCUtils.write_station_data_to_file(json_dict['resultsdict'],json_dict['params_dict'],request=request)

    return render_to_response('scenic/data/station/home.html', context, context_instance=RequestContext(request))


def data_gridded(request):
    context = {
        'title': 'Gridded Data Lister',
    }
    initial, checkbox_vals = set_data_gridded_initial(request)
    context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
    #Set up maps if needed
    context['host'] = settings.HOST
    context['area_type'] = initial['select_grid_by']
    context[initial['select_grid_by']] = WRCCData.AREA_DEFAULTS[initial['select_grid_by']]
    kml_file = initial['overlay_state'] + '_' + initial['select_grid_by'] + '.kml'
    context[initial['overlay_state'] + '_selected'] = 'selected'
    context[initial['select_grid_by']] = WRCCData.AREA_DEFAULTS[initial['select_grid_by']]

    if 'formData' in request.POST or (request.method == 'GET' and 'elements' in request.GET):
        if request.method == 'GET':
            context['form_message'] = True
            form_initial = set_form_old(request, clean=False)
            user_params_list, user_params_dict = set_user_params(form_initial, 'data_gridded')
            context['user_params_list'] = user_params_list;context['user_params_dict'] = user_params_dict
        #Turn request object into python dict
        form = set_form_old(request,clean=False)
        form_cleaned = set_form_old(request)
        #Set form defaults for link from other pages
        if 'units' not in form.keys():
            form['units']='english'
            form_cleaned['units'] = 'english'
        #Back Button/download files issue fix:
        #if select_grid_by none, find it
        if not 'select_grid_by' in form_cleaned.keys() or form_cleaned['select_grid_by'] not in form_cleaned.keys():
            for key in WRCCData.SEARCH_AREA_FORM_TO_ACIS.keys():
                if key in form.keys():
                    form['select_grid_by'] = key
                    form_cleaned['select_grid_by'] = key
                    break

        context['form_cleaned'] = form_cleaned
        #Link to other apps
        spatial_summary_params_list, spatial_summary_params_dict = set_user_params(form, 'spatial_summary')
        temporal_summary_params_list, temporal_summary_params_dict = set_user_params(form, 'temporal_summary')
        context['temporal_summary_params_list'] = temporal_summary_params_list
        context['temporal_summary_params_dict']=temporal_summary_params_dict
        context['spatial_summary_params_list'] = spatial_summary_params_list
        context['spatial_summary_params_dict']=spatial_summary_params_dict
        #Set form initial
        initial,checkbox_vals = set_data_gridded_initial(form)
        context['initial'] = initial;context['checkbox_vals']  = checkbox_vals
        display_params_list, params_dict = set_data_gridded_params(form)
        context['display_params_list'] = display_params_list;context['params_dict'] = params_dict
        fields_to_check = [form_cleaned['select_grid_by'],'start_date', 'end_date','degree_days','elements']
        #Check for form errors
        if 'user_email' in form_cleaned.keys():
            fields_to_check.append('user_email')
            context['large_request'] = True
        form_error = check_form(form_cleaned, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            if form_cleaned['select_grid_by'] in ['basin','county','county_warning_area', 'climate_division']:
                context['need_overlay_map'] = True
            kml_file_path = create_kml_file(form['select_grid_by'], form['overlay_state'])
            context['kml_file_path'] = kml_file_path
            return render_to_response('scenic/data/gridded/home.html', context, context_instance=RequestContext(request))
        context['elev_unit'] = 'ft'
        if 'units' in form.keys() and form['units'] == 'metric':context['elev_unit'] = 'm'
        #Add id in display params and change params_dict to id if needed
        if form[form['select_grid_by']].upper()!= form_cleaned[form_cleaned['select_grid_by']].upper():
            display_params_list[0][1]+= ', ' + str(form_cleaned[form_cleaned['select_grid_by']])
            params_dict[form['select_grid_by']] = str(form_cleaned[form_cleaned['select_grid_by']])
        #Check if data request is large,
        '''
        We estimate number or lats, lons and days in request
        and calculate the approximate size of the data request.
        Large data requests are between 0.00098GB and 1GB
        We gather params and ask user for name and e-mail and
        notify user that request will be processed offline.
        Data requests larger than 1GB will not be processed.
        Data requests smaller than 0.00098GB will be processed on the fly.
        '''
        s_date = WRCCUtils.date_to_datetime(form_cleaned['start_date'])
        e_date = WRCCUtils.date_to_datetime(form_cleaned['end_date'])
        days = (e_date - s_date).days
        if days ==0:days= 1
        bbox = []
        if 'shape' in form.keys():
            t,bbox = WRCCUtils.get_bbox(form['shape'])
        elif form['select_grid_by'] in ['basin', 'state', 'climate_division', 'county', 'county_warning_area']:
            sa = WRCCData.SEARCH_AREA_FORM_TO_ACIS[form['select_grid_by']]
            bbox = AcisWS.get_acis_bbox_of_area(sa, form_cleaned[form_cleaned['select_grid_by']])
        num_lats, num_lons = WRCCUtils.find_num_lls(bbox,form['grid'])
        time_interval = 1.0
        if form['temporal_resolution'] == 'mly':time_interval =30.0
        if form['temporal_resolution'] == 'yly':time_interval =365.0
        if form['data_summary'] == 'temporal':time_interval=time_interval * float(days)
        num_data_points = days * num_lats *num_lons * len(form_cleaned['elements']) / time_interval
        num_giga_bytes = 2 * num_data_points /float(1024**3)
        num_mega_bytes = round(2 * num_data_points /float(1024**2),2)
        '''
        if 2 * 0.00098 < num_giga_bytes:
            ldr = 'At the moment we do not accept data requests producing \
                more than 2MB of data. Your request size is approximately %s MB. \
                We will support larger requests in the near future. \
                Thank you for your patience!' %str(num_mega_bytes)
            context['too_large'] = ldr
            return render_to_response('scenic/data/gridded/home.html', context, context_instance=RequestContext(request))
        '''

        if 'user_name' in form_cleaned.keys():
            ldr = \
                'Data request submitted successfully. \n \
                Notification will be sent to %s when the request has been processed!' %form_cleaned['user_email']
            context['large_request'] = ldr
            json_file = form_cleaned['output_file_name'] + settings.PARAMS_FILE_EXTENSION
            WRCCUtils.load_data_to_json_file(settings.DATA_REQUEST_BASE_DIR +json_file, form_cleaned)
            return render_to_response('scenic/data/gridded/home.html', context, context_instance=RequestContext
(request))
        elif num_giga_bytes > 2:
            ldr = 'At the moment we do not accept data requests producing \
                more than 2GB of data. Your request size is approximately %s GB' %str(num_giga_bytes)
            context['too_large'] = ldr
            return render_to_response('scenic/data/gridded/home.html', context, context_instance=RequestContext(request))
        elif 2 * 0.00098 < num_giga_bytes and  num_giga_bytes < 2:
            ldr = \
                'You requested a large amount of data. \
                We estimated %s MB. \
                Please provide your user name and email and resubmit the form.\
                we will process your request off-line and \
                notify you when your request has been processed. \
                Thank you for your patience!' %str(num_mega_bytes)
            context['large_request'] = ldr
            return render_to_response('scenic/data/gridded/home.html', context, context_instance=RequestContext(request))
        context['large_request'] = False
        #Data request
        req = AcisWS.get_grid_data(form_cleaned, 'griddata_web')
        context['hide_gp_map'] = True
        if 'error' in req.keys():
            context['results'] = {'errors':req['error']}
            return render_to_response('scenic/data/gridded/home.html', context, context_instance=RequestContext(request))
        #format data
        results = WRCCUtils.format_grid_data(req, form_cleaned)
        if not results:
            context['results']  = {'errors': 'No data found for these parameters!'}
        else:
            context['results'] = results
        #If Spatial Summary, write json file for spatial_summary graph
        if form_cleaned['data_summary'] == 'spatial' or 'location' in form_cleaned.keys():
            if 'location' in form_cleaned.keys() and form_cleaned['data_summary']!='spatial':
                start_idx = 4
            else:
                start_idx = 1
            if form_cleaned['data_summary'] == 'spatial':
                graph_data =[[[dat] for dat in results] for el in form_cleaned['elements'].replace(' ','').split(',')]
            else:
                graph_data = [[[dat[0]] for dat in results]for el in form_cleaned['elements'].replace(' ','').split(',')]
            for date_idx,date_data in enumerate(results):
                for el_idx,el_data in enumerate(date_data[start_idx:]):
                    graph_data[el_idx][date_idx].append(el_data)
            json_dict = {
            'search_params':params_dict,
            'display_params_list':display_params_list,
            'download_data':results,
            'graph_data':graph_data
            }
            time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
            json_file = '%s_spatial_summary.json' %(time_stamp)
            WRCCUtils.load_data_to_json_file(settings.TEMP_DIR +json_file, json_dict)
            context['JSON_URL'] = settings.TMP_URL
            context['json_file'] = json_file
        #Render to page if html format was chosen, else save to file
        if form_cleaned['data_format'] == 'html':
            #Write results to json file for later download
            json_dict = {
                'results':results,
                'form':form
            }
            time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
            json_file = '%s_data_station.json' %(time_stamp)
            json_dict['json_file'] = json_file
            json_dict['JSON_URL'] = settings.TEMP_DIR
            results_json = json.dumps(json_dict)
            with open(settings.TEMP_DIR + '%s' %(json_file),'w+') as f:
                f.write(results_json)
            context['json_file'] = json_file
            return render_to_response('scenic/data/gridded/home.html', context, context_instance=RequestContext(request))
        else:
            return WRCCUtils.write_griddata_to_file(results,form,request=request)

    #Overlay Maps
    if 'formOverlay' in request.POST:
        context['need_overlay_map'] = True
        form = set_form_old(request)
        initial, checkbox_vals = set_data_gridded_initial(request)
        #Override initial where needed
        initial['select_grid_by'] = form['select_overlay_by']
        checkbox_vals[form['select_overlay_by'] + '_selected'] = 'selected'
        initial['area_type_value'] = WRCCData.AREA_DEFAULTS[form['select_overlay_by']]
        initial[form['select_overlay_by']] = WRCCData.AREA_DEFAULTS[form['select_overlay_by']]
        initial['area_type_label'] = WRCCData.DISPLAY_PARAMS[form['select_overlay_by']]
        initial['autofill_list'] = 'US_' + form['select_overlay_by']
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
        context[form['overlay_state'] + '_selected'] = 'selected'
        kml_file_path = create_kml_file(form['select_overlay_by'], form['overlay_state'])
        context['kml_file_path'] = kml_file_path
        context['area_type'] = form['select_overlay_by']
        context['host'] = settings.HOST

   #Downlaod Table Data
    if 'formDownload' in request.POST:
        form = set_form_old(request,clean=False)
        json_file = request.POST.get('json_file', None)
        if not json_file:
            results = {'error':'No json file found for data download.'}
            return render_to_response('scenic/data/station/home.html', context, context_instance=RequestContext(request))
        with open(settings.TEMP_DIR + json_file, 'r') as f:
            json_dict =  json.load(f)
            #Overwrite download options
            json_dict['form']['data_format'] = form['data_format_download']
            json_dict['form']['delimiter'] = form['delimiter_download']
            json_dict['form']['output_file_name'] = form['output_file_name_download']
        return WRCCUtils.write_griddata_to_file(json_dict['results'],json_dict['form'],request=request)

    return render_to_response('scenic/data/gridded/home.html', context, context_instance=RequestContext(request))



def apps_home(request):
    context = {
        'title': 'Data Analysis',
        'state_choices': ['AZ', 'CA', 'CO', 'NM', 'NV', 'UT'],
        'icon':'ToolProduct.png'
    }
    stn_id = request.GET.get('stn_id', None)
    if stn_id is None:
        pass
    else:
        context['stn_id'] = stn_id
    #Main display temps/precip for month since 1900
    state = request.GET.get('state_key', None)
    element = request.GET.get('element', None)
    if state is None:state = 'NV'
    if element is None: element='mint'
    month = int(datetime.date.today().month)
    context['month'] = month
    context['month_name'] = WRCCData.MONTH_NAMES_LONG[month - 1]
    context['state'] = state
    context['element'] = element
    return render_to_response('scenic/apps/home.html', context, context_instance=RequestContext(request))

def apps_station(request):
    context = {
        'title': 'Station Data Analysis'
        }
    #Link from other page
    if request.method == 'GET' and 'station_id' in request.GET:
        context['hide_sodsumm'] = True
        context['hide_metagrapgh'] = True
        form_cleaned = set_form_old(request,clean=True)
        form = set_form_old(request,clean=False)
        user_params_list, user_params_dict =set_user_params(form, 'apps_station')
        if 'elements' in user_params_dict.keys():
            context['hide_sodxtrmts'] = True
        context['user_params_list'] = user_params_list;context['user_params_dict']=user_params_dict
    return render_to_response('scenic/apps/station/home.html', context, context_instance=RequestContext(request))


def apps_gridded(request):
    context = {
        'title': 'Gridded Data Analysis'
        }
    #Link from other page
    if request.method == 'GET' and 'elements' in request.GET:
        form_cleaned = set_form_old(request,clean=True)
        form = set_form_old(request,clean=False)
        user_params_list, user_params_dict =set_user_params(form, 'apps_gridded')
        context['user_params_list'] = user_params_list;context['user_params_dict']=user_params_dict
    return render_to_response('scenic/apps/gridded/home.html', context, context_instance=RequestContext(request))

def apps_mixed(request):
    context = {
        'title': 'Combined Data Analysis'
        }
    #Link from other page
    if request.method == 'GET' and 'elements' in request.GET:
        form_cleaned = set_form_old(request,clean=True)
        form = set_form_old(request,clean=False)
        user_params_list, user_params_dict =set_user_params(form, 'apps_mixed')
        context['user_params_list'] = user_params_list;context['user_params_dict']=user_params_dict
    return render_to_response('scenic/apps/combined/home.html', context, context_instance=RequestContext(request))

def apps_gis(request):
    context = {
        'title': 'Geospatial Data Tools',
        'icon':'ToolProduct.png'
        }
    return render_to_response('scenic/apps/gis/home.html', context, context_instance=RequestContext(request))

def google_ee(request):
    context = {
        'title': 'Google Earth Engine'
        }
    return render_to_response('scenic/apps/gridded/google_ee.html', context, context_instance=RequestContext(request))


def metagraph(request):
    context = {
        'title': 'Station Metadata Graphics',
        'icon':'ToolProduct.png'
    }
    station_id = request.GET.get('station_id', None)
    if station_id is None:
        form_meta = set_as_form(request,'MetaGraphForm')
    else:
        form_meta = set_as_form(request,'MetaGraphForm', init={'station_id':str(station_id)})
        context['station_id'] = station_id
    context['form_meta'] = form_meta

    if 'form_meta' in request.POST or request.method == 'GET':
        form_meta = set_as_form(request,'MetaGraphForm')
        context['form_meta']  = form_meta
        if form_meta.is_valid():
            identifier = find_id(form_meta.cleaned_data['station_id'],settings.MEDIA_DIR + 'json/US_coop_station_ids.json')
            context['station_id'] = form_meta.cleaned_data['station_id']
            params = {'sids':identifier}
            meta_request = AcisWS.StnMeta(params)
            #meta_request = WRCCClasses.DataJob('StnMeta', params).make_data_call()
            key_order = ['name','state','ll','elev','uid','sids']
            #station_meta = [[WRCCData.DISPLAY_PARAMS[key]] for key in key_order]
            if 'meta' in meta_request.keys():
                if len(meta_request['meta']) == 0:
                    station_meta = {'error': 'No metadata found for station: %s.' %str(form_meta.cleaned_data['station_id'])}
                else:
                    station_meta = WRCCUtils.metadict_to_display(meta_request['meta'][0], key_order)
            else:
                station_meta = {'error':'No meta data found for station: %s.' %station_id}
            context['station_meta'] = station_meta
            #Call perl script that generates gif graphs
            #FIX ME! Should be able to call it from html:
            #<img alt="MetaGraph" title="MetaGraph" src="{{settings.MEDIA_URL}}perl-scripts/csc_cliMETAgraph.pl?{{station_id}}">
            time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f_')
            context['time_stamp'] = time_stamp
            perl_out, perl_err = run_external_script("perl %sperl-scripts/csc_cliMETAgraph.pl %s %s" %(settings.MEDIA_DIR, identifier, time_stamp))
            context['perl_err'] = perl_err
            context['perl_out'] = perl_out
        else:
            station_id = None
            context['station_id'] = form_meta['station_id']
            station_meta = {'error':'No meta data found for station: %s.' %station_id}

    return render_to_response('scenic/apps/station/metagraph.html', context, context_instance=RequestContext(request))

def monthly_aves(request):
    context = {
        'title': 'Monthly Averages as Bar Charts',
        'icon':'ToolProduct.png'
    }
    initial, checkbox_vals = set_monthly_aves_initial(request)
    context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
    #context['search_params'] = initial

    if 'formData' in request.POST or (request.method == 'GET' and 'elements' in request.GET):
        if request.method == 'GET':
            context['form_message'] = True
            form_initial = set_form_old(request,clean=False)
            user_params_list, user_params_dict =set_user_params(form_initial, 'monthly_aves')
            context['user_params_list'] = user_params_list;context['user_params_dict']=user_params_dict
        form = set_form_old(request,clean=False)
        form_cleaned = set_form_old(request,clean=True)
        search_params ={}
        for key, val in form_cleaned.items():
            if key != 'formData':
                search_params[key] = val
        #Links
        params_list, params_dict =set_user_params(form, 'monthly_aves')
        context['params_list'] = params_list;context['params_dict']=params_dict
        search_params['select_stations_by'] = 'station_id'
        search_params['station_id'] = form['station_id']
        context['search_params'] = search_params
        fields_to_check = ['start_date', 'end_date','degree_days', 'elements']
        form_error = check_form(form_cleaned, fields_to_check)
        initial, checkbox_vals = set_monthly_aves_initial(form)
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
        if form_error:
            context['form_error'] = form_error
            return render_to_response('scenic/apps/station/monthly_aves.html', context, context_instance=RequestContext(request))
        params = {
            'sid':form_cleaned['station_id'],
            'sdate':form_cleaned['start_date'].lower(),
            'edate':form_cleaned['end_date'].lower(),
            'meta':'valid_daterange,name,state,sids,ll,elev,uid,county,climdiv'
        }
        elems = []
        for el in form['elements']:
            if 'units' in form.keys() and form['units'] == 'metric':
                el_strip, base_temp = WRCCUtils.get_el_and_base_temp(el,units='metric')
            else:
                el_strip, base_temp = WRCCUtils.get_el_and_base_temp(el)
            if base_temp:
                elems.append({'vX':WRCCData.ACIS_ELEMENTS_DICT[el_strip]['vX'], 'base':int(base_temp),'groupby':'year'})
            else:
                elems.append({'vX':WRCCData.ACIS_ELEMENTS_DICT[el]['vX'],'groupby':'year'})
        params['elems'] = elems
        #Data request
        #req = WRCCClasses.DataJob('StnData', params).make_data_call()
        req = AcisWS.StnData(params)
        #Sanity check
        if not req:
            context['error']= 'No data found for parameters. Please check your station ID.'
            return render_to_response('scenic/apps/station/monthly_aves.html', context, context_instance=RequestContext(request))
        if 'error' in req.keys():
            if req['error'] == 'Unknown sId':
                context['error'] = '%s is not a valid station identifyier.' %form_cleaned['station_id']
            else:
                context['error']= req['error']
            return render_to_response('scenic/apps/station/monthly_aves.html', context, context_instance=RequestContext(request))
        if 'data' not in req.keys() or 'meta' not in req.keys():
            context['error']= 'No data found for parameters. Please check your station ID, start and end dates.'
            return render_to_response('scenic/apps/station/monthly_aves.html', context, context_instance=RequestContext(request))
        #Find averages and write results dict
        monthly_aves = {el:[] for el in form['elements']}
        el_list = form['elements']
        results = [{} for k in el_list]
        try:
            monthly_aves = WRCCDataApps.monthly_aves(req,form)
        except:
            pass
        context['averaged_data'] = monthly_aves
        #Write results dict
        try:
            results = write_monthly_aves_results(req, form, monthly_aves)
        except:
            context['error'] = 'No data found for parameters. Please check your station ID, start and end dates.'
        context['results'] = results
        if 'meta' in req.keys():
            meta = write_monthly_aves_meta(req, form)
            context['meta'] = meta
        #save to json file (necessary since we can't pass list, dicts to js via hidden vars)
        #double quotes needed for jquery json.load

        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        json_file = '%s_monthly_aves_%s_%s_%s.json' \
        %(time_stamp, str(form_cleaned['station_id']), form_cleaned['start_date'], form_cleaned['end_date'])
        context['json_file'] = json_file
        WRCCUtils.load_data_to_json_file(settings.TEMP_DIR + json_file, results)
    return render_to_response('scenic/apps/station/monthly_aves.html', context, context_instance=RequestContext(request))

def temporal_summary(request):
    context = {
        'title': 'Temporal Summaries',
    }
    json_file = request.GET.get('json_file', None)
    #Check if we are coming in from other page, e.g. Gridded Data
    #Set initial accordingly
    if json_file is not None:
        json_data = WRCCUtils.load_json_data_from_file(settings.TEMP_DIR + json_file)
        if not json_data or not 'search_params' in json_data.keys():
            initial,checkbox_vals = set_temporal_summary_initial(request)
        else:
            initial,checkbox_vals = set_temporal_summary_initial(json_data['search_params'])
    else:
        initial,checkbox_vals = set_temporal_summary_initial(request)
    #Plot Options
    initial_plot, checkbox_vals_plot = set_map_plot_options(request)
    join_initials(initial, initial_plot, checkbox_vals, checkbox_vals_plot)
    context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
    if initial['select_grid_by'] != 'bounding_box':
        context['hide_bbox_map'] = True
    #Set up maps if needed
    #context['host'] = settings.HOST
    #context['area_type'] = initial['select_grid_by']
    context[initial['select_grid_by']] = WRCCData.AREA_DEFAULTS[initial['select_grid_by']]
    context[initial['overlay_state'] + '_selected'] = 'selected'

    #Link from other page
    if request.method == 'GET' and 'elements' in request.GET:
        form_cleaned = set_form_old(request,clean=True)
        form = set_form_old(request,clean=False)
        user_params_list, user_params_dict =set_user_params(form, 'temporal_summary')
        context['user_params_list'] = user_params_list;context['user_params_dict']=user_params_dict

    if 'formMap' in request.POST:
        context['hide_bbox_map'] = True
        form = set_form_old(request, clean=False)
        form_cleaned = set_form_old(request)
        initial, checkbox_vals = set_temporal_summary_initial(request)
        params_cleaned = set_form_old(initial)
        params_list, params_dict =set_user_params(form, 'temporal_summary')
        context['params_list'] = params_list;context['params_dict']=params_dict
        #Back Button/download files issue fix:
        #if select_grid_by none, find it
        if not 'select_grid_by' in form.keys():
            for key in WRCCData.SEARCH_AREA_FORM_TO_ACIS.keys():
                if key in form.keys():
                    form['select_grid_by'] = key
                    break

        #Form Check
        fields_to_check = ['start_date', 'end_date','degree_days','level_number', 'cmap', form['select_grid_by'], 'elements']
        form_error = check_form(form_cleaned, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            if form_cleaned['select_grid_by'] in ['basin','county','county_warning_area', 'climate_division']:
                context['need_overlay_map'] = True
            kml_file_path = create_kml_file(form['select_grid_by'], form['overlay_state'])
            context['kml_file_path'] = kml_file_path
            return render_to_response('scenic/apps/gridded/temporal_summary.html', context, context_instance=RequestContext(request))
        #Set initials
        initial,checkbox_vals = set_temporal_summary_initial(form)
        initial_plot, checkbox_vals_plot = set_map_plot_options(form)
        join_initials(initial, initial_plot, checkbox_vals, checkbox_vals_plot)
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
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
            'select_grid_by':WRCCData.SEARCH_AREA_FORM_TO_ACIS[form['select_grid_by']],
            WRCCData.SEARCH_AREA_FORM_TO_ACIS[form['select_grid_by']]:form[form['select_grid_by']],
            'grid': form['grid'],
            'sdate':form['start_date'],
            'edate':form['end_date'],
            'level_number':form['level_number'],
            'temporal_summary':form['temporal_summary'],
            'elems':[]
            }
        display_params = []
        for el_idx,element in enumerate(form_cleaned['elements'].replace(' ','').split(',')):
            pms={}
            for key, val in params.iteritems():
                pms[key] = params[key]
            pms['elems'] = [{'name':element,'smry':form_cleaned['temporal_summary'],'smry_only':1}]
            fig = WRCCClasses.GridFigure(pms)
            result = fig.get_grid()
            time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
            figure_file = 'clim_sum_map_' + time_stamp + '.png'
            file_path_big =settings.TEMP_DIR + figure_file
            fig.build_figure(result, file_path_big)
            figure_files.append(figure_file)
            d_p = []
            for key in ['start_date', 'end_date']:
                d_p.append([WRCCData.DISPLAY_PARAMS[key],form[key]])
            if 'units' in form_cleaned.keys() and form_cleaned['units'] == 'metric':
                el_strip, base_temp = WRCCUtils.get_el_and_base_temp(el,units='metric')
            else:
                el_strip, base_temp = WRCCUtils.get_el_and_base_temp(element)
            el_str = WRCCData.DISPLAY_PARAMS[el_strip] + ' (' + WRCCData.UNITS_ENGLISH[el_strip] + ')'
            if base_temp:
                d_p.insert(0,['Element', el_str + ' Base Temperature: ' + str(base_temp)])
            else:
                d_p.insert(0,['Element', el_str])
            d_p.insert(1,['Temporal Summary', WRCCData.DISPLAY_PARAMS[form['temporal_summary']]])
            d_p.insert(2, [WRCCData.DISPLAY_PARAMS[form['select_grid_by']], form[form['select_grid_by']].upper()])
            display_params.append(d_p)
        context['display_params'] = display_params
        context['JSON_URL'] = settings.TMP_URL
        context['figure_files'] = figure_files

    #overlay map generation
    if 'formOverlay' in request.POST:
        form = set_form_old(request, clean=False)
        context['need_overlay_map'] = True
        initial, checkbox_vals = set_temporal_summary_initial(request)
        initial_plot, checkbox_vals_plot = set_map_plot_options(form)
        join_initials(initial, initial_plot, checkbox_vals, checkbox_vals_plot)
        #Override initial where needed
        initial['select_grid_by'] = form['select_overlay_by']
        checkbox_vals[form['select_overlay_by'] + '_selected'] = 'selected'
        initial['area_type_value'] = WRCCData.AREA_DEFAULTS[form['select_overlay_by']]
        initial[form['select_overlay_by']] = WRCCData.AREA_DEFAULTS[form['select_overlay_by']]
        initial['area_type_label'] = WRCCData.DISPLAY_PARAMS[form['select_overlay_by']]
        initial['autofill_list'] = 'US_' + form['select_overlay_by']
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
        context[form['overlay_state'] + '_selected'] = 'selected'
        kml_file_path = create_kml_file(form['select_overlay_by'], form['overlay_state'])
        context['kml_file_path'] = kml_file_path
        context['area_type'] = form['select_overlay_by']
        context['host'] = settings.HOST

    return render_to_response('scenic/apps/gridded/temporal_summary.html', context, context_instance=RequestContext(request))

def clim_prob_maps(request):
    context = {
        'title': 'Climate Probability Maps',
        'icon':'ToolProduct.png'
    }
    return render_to_response('scenic/apps/gridded/clim_prob_maps.html', context, context_instance=RequestContext(request))

def spatial_summary(request):
    context = {
        'title': 'Spatial Summaries',
    }
    json_file = request.GET.get('json_file', None)
    #Check if we are coming in from other page, e.g. Gridded Data
    #Set initial accordingly
    if json_file is not None and json_file !='':
        with open(settings.TEMP_DIR + json_file, 'r') as f:
            try:
                json_data = WRCCUtils.u_convert(json.loads(f.read()))
                initial,checkbox_vals = set_spatial_summary_initial(json_data['search_params'])
                #Link from other page
                user_params_list, user_params_dict =set_user_params(json_data['search_params'], 'spatial_summary')
                context['user_params_list'] = user_params_list;context['user_params_dict']=user_params_dict
            except:
                initial,checkbox_vals = set_spatial_summary_initial(request)
    else:
        initial,checkbox_vals = set_spatial_summary_initial(request)

    if 'location' in initial.keys():
        context['need_gridpoint_map'] = True
    initial_plot, checkbox_vals_plot = set_plot_options(request)
    join_initials(initial, initial_plot, checkbox_vals, checkbox_vals_plot)
    context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
    #Set up maps if needed
    context['host'] = settings.HOST
    context['area_type'] = initial['select_grid_by']
    context[initial['select_grid_by']] = WRCCData.AREA_DEFAULTS[initial['select_grid_by']]
    context[initial['overlay_state'] + '_selected'] = 'selected'

    #Link from other page
    if request.method == 'GET' and 'elements' in request.GET:
        form_cleaned = set_form_old(request,clean=True)
        form = set_form_old(request,clean=False)
        user_params_list, user_params_dict = set_user_params(form, 'spatial_summary')
        context['user_params_list'] = user_params_list;context['user_params_dict'] = user_params_dict

    if 'formTS' in request.POST:
        context['need_gridpoint_map'] = False
        form = set_form_old(request, clean=False)
        form_cleaned = set_form_old(request)
        #Back Button/download files issue fix:
        #if select_grid_by none, find it
        if not 'select_grid_by' in form_cleaned.keys() or form_cleaned['select_grid_by'] not in form_cleaned.keys():
            for key in WRCCData.SEARCH_AREA_FORM_TO_ACIS.keys():
                if key in form.keys():
                    form['select_grid_by'] = key
                    form_cleaned['select_grid_by'] = key
                    break
        #Form Check
        fields_to_check = [form['select_grid_by'],'start_date', 'end_date','degree_days', 'elements']
        #,'connector_line_width', 'vertical_axis_min', 'vertical_axis_max']
        form_error = check_form(form_cleaned, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            if form_cleaned['select_grid_by'] in ['basin','county','county_warning_area', 'climate_division']:
                context['need_overlay_map'] = True
            kml_file_path = create_kml_file(form['select_grid_by'], form['overlay_state'])
            context['kml_file_path'] = kml_file_path
            return render_to_response('scenic/apps/gridded/spatial_summary.html', context, context_instance=RequestContext(request))
        #Set initials
        initial,checkbox_vals = set_spatial_summary_initial(form)
        initial_plot, checkbox_vals_plot = set_plot_options(form)
        join_initials(initial, initial_plot, checkbox_vals, checkbox_vals_plot)
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
        #Display liust and serach params
        search_params, display_params_list =  set_spatial_summary_params(form_cleaned)
        context['display_params_list'] = display_params_list
        #joins plot opts to search_params
        join_dicts(search_params,initial_plot)
        #Data Request
        #Skip data generation of it has already been performed
        json_file = request.GET.get('json_file', None)
        if json_file is not None:
            context['json_file'] =json_file
            context['JSON_URL'] = settings.TEMP_DIR
            with open(settings.TEMP_DIR + json_file, 'r') as f:
                try:
                    json_data = WRCCUtils.u_convert(json.loads(f.read()))
                    if not 'graph_data' in json_data.keys() or not 'download_data' in json_data.keys():
                        context['error'] = 'No data found in file %s' %json_file
                        return render_to_response('scenic/apps/gridded/spatial_summary.html', context, context_instance=RequestContext(request))
                except Exception, e:
                    context['error'] = 'Error when reading %s: %s' (json_file, str(e))
                    return render_to_response('scenic/apps/gridded/spatial_summary.html', context, context_instance=RequestContext(request))
            summary_time_series = json_data['graph_data']
            #Check that we have enough data to generate plot (enough > 2)
            if not summary_time_series:
                context['error'] = 'No data found to generate graph. Please check your input variables.'
                return render_to_response('scenic/apps/gridded/spatial_summary.html', context, context_instance=RequestContext(request))
            elif len(summary_time_series[0])<=2:
                context['error'] = 'Not enough data to generate graph. Please make sure to have a time range  larger than 2 days.'
                return render_to_response('scenic/apps/gridded/spatial_summary.html', context, context_instance=RequestContext(request))
            download_data = json_data['download_data']
        else:
            #set up bbox query for area_type
            data_request_params,shape_type,shape_coords,PointIn,poly  = set_params_for_shape_queries(search_params)

            #Find data
            try:
                req = AcisWS.GridData(data_request_params)
            except Exception, e:
                context['error'] = 'Error in data request: ' + str(e)
                return render_to_response('scenic/apps/gridded/spatial_summary.html', context, context_instance=RequestContext(request))
            if not 'data' in req.keys():
                context['error'] = 'No data found for this set of parameters.'
                return render_to_response('scenic/apps/gridded/spatial_summary.html', context, context_instance=RequestContext(request))
            #Generate time series from data request
            summary_time_series, download_data = compute_spatial_summary_summary(req,search_params,poly,PointIn)
            context['req']=req
            #Check that we have enough data to generate plot (enough > 2)
            if not summary_time_series:
                context['error'] = 'No data found to generate graph. Please check your input variables.'
                return render_to_response('scenic/apps/gridded/spatial_summary.html', context, context_instance=RequestContext(request))
            elif len(summary_time_series[0])<=2:
                context['error'] = 'Not enough data to generate graph. Please make sure to have a time range  larger than 2 days.'
                return render_to_response('scenic/apps/gridded/spatial_summary.html', context, context_instance=RequestContext(request))
        #Write data in download format
        #Set rest of search_params,context variables and save results
        search_params['spatial_summary'] = WRCCData.DISPLAY_PARAMS[form['spatial_summary']]
        context['search_params'] = search_params
        context['results']= summary_time_series
        context['width'] = WRCCData.IMAGE_SIZES[search_params['image_size']][0]
        context['height'] = WRCCData.IMAGE_SIZES[search_params['image_size']][1]

        #Write results to json file
        json_dict = {
            'search_params':search_params,
            'display_params_list':display_params_list,
            'download_data':download_data,
            'graph_data':summary_time_series
        }
        results_json = json.dumps(json_dict)
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        json_file = '%s_spatial_summary.json' %(time_stamp)
        f = open(settings.TEMP_DIR + '%s' %(json_file),'w+')
        f.write(results_json)
        f.close()
        context['JSON_URL'] = settings.TMP_URL
        context['json_file'] = json_file

    #overlay map generation
    if 'formOverlay' in request.POST:
        form = set_form_old(request, clean=False)
        context['form'] = form
        context['need_overlay_map'] = True
        context['need_gridpoint_map'] = False
        initial, checkbox_vals = set_spatial_summary_initial(request)
        initial_plot, checkbox_vals_plot = set_plot_options(form)
        join_initials(initial, initial_plot, checkbox_vals, checkbox_vals_plot)
        #Override initial where needed
        initial['select_grid_by'] = form['select_overlay_by']
        checkbox_vals[form['select_overlay_by'] + '_selected'] = 'selected'
        initial['area_type_value'] = WRCCData.AREA_DEFAULTS[form['select_overlay_by']]
        initial[form['select_overlay_by']] = WRCCData.AREA_DEFAULTS[form['select_overlay_by']]
        initial['area_type_label'] = WRCCData.DISPLAY_PARAMS[form['select_overlay_by']]
        initial['autofill_list'] = 'US_' + form['select_overlay_by']
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
        context[form['overlay_state'] + '_selected'] = 'selected'
        kml_file_path = create_kml_file(form['select_overlay_by'], form['overlay_state'])
        context['kml_file_path'] = kml_file_path
        context['area_type'] = form['select_overlay_by']
        context['host'] = settings.HOST

    #Downlaod Table Data
    if 'formDownload' in request.POST:
        data_format = request.POST.get('data_format', 'clm')
        delimiter = request.POST.get('delimiter', 'comma')
        output_file_name = request.POST.get('output_file_name', 'output')
        json_file = request.POST.get('json_file', None)
        with open(settings.TEMP_DIR + json_file, 'r') as f:
            json_dict =  json.load(f)
        DDJ = WRCCClasses.DownloadDataJob('spatial_summary',data_format,delimiter, output_file_name, request=request, json_in_file=settings.TEMP_DIR + json_file)
        return DDJ.write_to_file()

    return render_to_response('scenic/apps/gridded/spatial_summary.html', context, context_instance=RequestContext(request))

def station_locator_app(request):
    from subprocess import call
    call(["touch", settings.TEMP_DIR + "Empty.json"])
    context = {
        'title': 'Station Finder',
    }
    #Set up initial map (NV stations)
    #context['station_json'] = 'NV_stn.json'
    initial,checkbox_vals = set_station_locator_initial(request)
    context['initial'] = initial;context['checkbox_vals']=checkbox_vals
    #Set up maps if needed
    context['host'] = settings.HOST
    context['area_type'] = initial['select_stations_by']
    context[initial['select_stations_by']] = WRCCData.AREA_DEFAULTS[initial['select_stations_by']]
    context[initial['overlay_state'] + '_selected'] = 'selected'
    context['kml_file_path'] = create_kml_file(initial['select_stations_by'], 'nv')
    params_list, params_dict = set_user_params(initial, 'station_locator_app')
    context['params_list'] = params_list;context['params_dict'] = params_dict
    if request.method == "GET":
        #Generate initial map
        by_type = WRCCData.ACIS_TO_SEARCH_AREA['state']
        val = 'nv'
        date_range = [initial['start_date'],initial['end_date']]
        el_date_constraints = initial['elements_constraints'] + '_' + initial['dates_constraints']
        station_json, f_name = AcisWS.station_meta_to_json(by_type, val, el_list=['1','2','4'],time_range=date_range, constraints=el_date_constraints)

        #context['station_ids_for_datafind'] = WRCCUtils.get_station_ids('/tmp/' + f_name)
        #Write json file for link to data lister
        json_dict ={};
        for key,val in params_dict.iteritems():
            json_dict[key] = val
        json_dict['select_stations_by'] = 'station_ids'
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

    if 'formData' in request.POST:
        form_initial = set_form_old(request,clean=False)
        user_params_list, user_params_dict =set_user_params(form_initial, 'station_locator_app')
        context['user_params_list'] = user_params_list;context['user_params_dict']=user_params_dict
        #Turn request object into python dict
        form = set_form_old(request, app_name='station_locator_app',clean=False)
        form_cleaned = set_form_old(request,app_name='station_locator_app',clean=True)
        #Add params for link to station data
        params_list, params_dict = set_user_params(form, 'station_locator_app')
        context['params_list'] = params_list;context['params_dict'] = params_dict

        form = set_form_old(request, clean=False)
        fields_to_check = [form_cleaned['select_stations_by'],'start_date', 'end_date', 'elements']
        form_error = check_form(form_cleaned, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            if form_cleaned['select_stations_by'] in ['basin','county','county_warning_area', 'climate_division']:
                context['need_overlay_map'] = True
            return render_to_response('scenic/apps/station/station_locator_app.html', context, context_instance=RequestContext(request))
        initial,checkbox_vals = set_station_locator_initial(form)
        context['initial'] = initial;context['checkbox_vals']  = checkbox_vals
        #Define map title
        display_params_list, pd = set_station_locator_params(form)
        context['display_params_list']= display_params_list
        #context['params_dict']= params_dict
        element_list = form_cleaned['elements'].replace(' ','').split(',')
        #Convert element list to var majors
        el_vX_list = []
        for el_idx, element in enumerate(element_list):
            el,base_temp = WRCCUtils.get_el_and_base_temp(element)
            el_vX_list.append(str(WRCCData.ACIS_ELEMENTS_DICT[el]['vX']))
        #context['req']= el_vX_list
        #Set up params for station_json generation
        by_type = WRCCData.ACIS_TO_SEARCH_AREA[form_cleaned['select_stations_by']]
        val = form_cleaned[WRCCData.ACIS_TO_SEARCH_AREA[form_cleaned['select_stations_by']]]
        context['map_title'] = WRCCData.DISPLAY_PARAMS[by_type].upper() + ': ' + val
        date_range = [form_cleaned['start_date'],form_cleaned['end_date']]
        el_date_constraints = form_cleaned['elements_constraints'] + '_' + form_cleaned['dates_constraints']
        station_json, f_name = AcisWS.station_meta_to_json(by_type, val, el_list=el_vX_list,time_range=date_range, constraints=el_date_constraints)
        #context['station_ids_for_datafind'] = WRCCUtils.get_station_ids('/tmp/' + f_name)
        json_dict ={};
        for key,val in params_dict.iteritems():
            json_dict[key] = val
        json_dict['select_stations_by'] = 'station_ids'
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

    #overlay map generation
    if 'formOverlay' in request.POST:
        context['need_overlay_map'] = True
        context['station_json'] = False
        form = set_form_old(request,clean=False)
        initial, checkbox_vals = set_station_locator_initial(form)
        #Override initial where needed
        initial['select_stations_by'] = form['select_overlay_by']
        checkbox_vals[form['select_overlay_by'] + '_selected'] = 'selected'
        #FIX ME: not sure why state is selected as well as correct area choice
        checkbox_vals['state_selected'] = ''
        initial['area_type_value'] = WRCCData.AREA_DEFAULTS[form['select_overlay_by']]
        initial[form['select_overlay_by']] = WRCCData.AREA_DEFAULTS[form['select_overlay_by']]
        initial['area_type_label'] = WRCCData.DISPLAY_PARAMS[form['select_overlay_by']]
        initial['autofill_list'] = 'US_' + form['select_overlay_by']
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
        context[form['overlay_state'] + '_selected'] = 'selected'
        kml_file_path = create_kml_file(form['select_overlay_by'], form['overlay_state'])
        context['kml_file_path'] = kml_file_path
        context['area_type'] = form['select_overlay_by']
        context['host'] = settings.HOST
    return render_to_response('scenic/apps/station/station_locator_app.html', context, context_instance=RequestContext(request))

#######################
#Mixed Data Applications
######################
def likelihood(request):
    context = {
        'title': 'Likelihood'
    }
    initial,checkbox_vals = set_combined_analysis_initial(request,'likelihood')
    context['initial'] = initial; context['checkbox_vals'] = checkbox_vals
    return render_to_response('scenic/apps/combined/likelihood.html', context, context_instance=RequestContext(request))

def data_comparison(request):
    context = {
        'title': 'Data Comparison'
    }
    initial, checkbox_vals = set_combined_analysis_initial(request,'data_comparison')
    context['initial'] = initial; context['checkbox_vals'] = checkbox_vals
    if 'formComparison' in request.POST or (request.method == 'GET' and 'elements' in request.GET):
        context['form_message'] = True
        form = set_form_old(request, clean=False)
        form['select_grid_by'] = 'location'
        user_params_list, user_params_dict = set_user_params(form, 'data_comparison')
        context['user_params_list'] = user_params_list
        context['user_params_dict'] = user_params_dict
        DC = WRCCClasses.DataComparer(form)
        gdata,sdata = DC.get_data()
        context['results'] = {'grid_data':gdata,'station_data':sdata}
        graph_data = DC.get_graph_data(gdata,sdata)
        context['graph_data'] = graph_data
    return render_to_response('scenic/apps/combined/data_comparison.html', context, context_instance=RequestContext(request))

#######################
#SOD programs
######################

def sodxtrmts(request, app_type):
    '''
    app_type = 'station' or 'grid'
    Both are processed via this view
    '''
    context = {}
    if app_type == 'grid':
        context['title'] = 'Single gridpoint statistics'
        url ='scenic/apps/gridded/grid_sodxtrmts.html'
    else:
        url = 'scenic/apps/station/sodxtrmts.html'
        context['title'] = 'Station Statistics/Custom Time Series'
    json_dict =  None
    json_file = request.GET.get('json_file', None)
    if json_file is not None:
        context['json_file'] =json_file
    initial,checkbox_vals = set_sodxtrmts_initial(request,app_type)
    context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
    #Set graph and plot options
    initial_graph, checkbox_vals_graph = set_sodxtrmts_graph_initial(request, init=initial)
    initial_pl_opts, checkbox_vals_pl_opts = set_plot_options(request)
    #combine the graph options with the plot options
    join_initials(initial_graph,initial_pl_opts, checkbox_vals_graph,checkbox_vals_pl_opts)
    context['initial_graph'] = initial_graph;context['checkbox_vals_graph'] = checkbox_vals_graph

    #Time Serie Table Generation and graph if desired
    if 'formSodxtrmts' in request.POST or (request.method == 'GET' and 'elements' in request.GET):
        if request.method == 'GET':
            context['form_message'] = True
            form_initial = set_form_old(request,clean=False)
            user_params_list, user_params_dict = set_user_params(form_initial, 'sodxtrmts')
            context['user_params_list'] = user_params_list;context['user_params_dict'] = user_params_dict
        #Turn request object into python dict
        if app_type == 'station':
            form = set_form_old(request, app_name='sodxtrmts',clean=True)
        else:
            form = set_form_old(request, app_name='sodxtrmts_grid',clean=True)
        #Set initial form parameters for html
        initial,checkbox_vals = set_sodxtrmts_initial(request,app_type)
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
        #Set graph and plot options
        initial_graph, checkbox_vals_graph = set_sodxtrmts_graph_initial(request,init=initial)
        initial_pl_opts, checkbox_vals_pl_opts = set_plot_options(request)
        #combine the graph options with the plot options
        join_initials(initial_graph,initial_pl_opts, checkbox_vals_graph,checkbox_vals_pl_opts)
        context['initial_graph'] = initial_graph;context['checkbox_vals_graph'] = checkbox_vals_graph
        #show all plot options to user in case there are form errors
        if checkbox_vals['generate_graph_T_selected'] =='selected':
            initial['generate_graph'] = 'T'
        #Form sanity check
        #form_error = check_sodxtrmts_form(form)
        fields_to_check = ['start_year', 'end_year','max_missing_days']
        form_error = check_form(form, fields_to_check)
        fields_to_check = ['graph_start_year', 'graph_end_year', \
        'connector_line_width', 'vertical_axis_min', 'vertical_axis_max']
        form_graph_error = check_form(form, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            return render_to_response(url, context, context_instance=RequestContext(request))
        if form_graph_error:
            context['form_graph_error'] = form_graph_error
            return render_to_response(url, context, context_instance=RequestContext(request))
        #Define header for html display
        header = set_sodxtrmts_head(form)

        #Check if we should only generate graphics
        if json_file is None:
            json_file = request.POST.get('j_file', None)
        if json_file:
            with open(settings.TEMP_DIR + json_file, 'r') as f:
                json_dict = WRCCUtils.u_convert(json.loads(f.read()))
                context['json_dict'] = json_dict
            initial_old = json_dict['initial'];checkbox_vals_old = json_dict['checkbox_vals']
            #initial_graph_old = json_dict['initial_graph'];checkbox_vals_graph_old = json_dict['checkbox_vals_graph']
            #Check if analysis parameters where changed by user
            diff_init = [k for k in initial if initial[k] != initial_old[k] and k!= 'generate_graph']
            diff_check_vals = [k for k in checkbox_vals if checkbox_vals[k] != checkbox_vals_old[k] and k not in ['generate_graph_T_selected', 'generate_graph_F_selected']]
            if not diff_init and not diff_check_vals:
                #check if user wants to generate graph
                if 'generate_graph' in initial.keys() and initial['generate_graph'] == 'T':
                    context['generate_graph'] = True
                    context['width'] = WRCCData.IMAGE_SIZES[form['image_size']][0]
                    context['height'] = WRCCData.IMAGE_SIZES[form['image_size']][1]
                    initial_graph['image_width'] = WRCCData.IMAGE_SIZES[form['image_size']][0]
                    initial_graph['image_height'] = WRCCData.IMAGE_SIZES[form['image_size']][1]
                    #Override initials
                    json_dict['initial'] = initial;json_dict['checkbox_vals'] = checkbox_vals
                    json_dict['initial_graph'] = initial_graph;json_dict['checkbox_vals_graph'] = checkbox_vals_graph
                    context['json_dict'] = json_dict
                    #context['req'] =checkbox_vals_graph
                    results_json = json.dumps(json_dict)
                    with open(settings.TEMP_DIR + '%s' %(json_file),'w+') as f:
                        f.write(results_json)
                    context['json_file'] =json_file
                    return render_to_response(url, context, context_instance=RequestContext(request))
            else:
                #New data analysis
                context['json_dict'] = {}
                #initial['generate_graph']='F'
                checkbox_vals['generate_graph_T_selected'] = ''
                checkbox_vals['generate_graph_F_selected'] = 'selected'
                initial['generate_graph'] ='F'
                #Reset initial_graph
                #initial_graph, checkbox_vals_graph = set_sodxtrmts_graph_initial({'start_year':initial['start_year'], 'end_year':initial['end_year']})
                initial_graph, checkbox_vals_graph = set_sodxtrmts_graph_initial({})
                initial_pl_opts, checkbox_vals_pl_opts = set_plot_options({})
                #combine the graph options with the plot options
                join_initials(initial_graph,initial_pl_opts, checkbox_vals_graph,checkbox_vals_pl_opts)
                context['initial_graph'] = initial_graph;context['checkbox_vals_graph'] = checkbox_vals_graph
        #Data Table generation
        data_params = {
            'start_date':form['start_year'],
            'end_date':form['end_year'],
            'element':form['element']
        }
        if app_type == 'grid':
            data_params['location'] = form['location']
            data_params['grid'] = form['grid']
        else:
            data_params['sid'] = form['station_id']
        app_params = form
        for key in ['location','station_id', 'start_year', 'end_year']:
            try:
                del app_params[key]
            except:
                pass
        app_params['el_type'] = form['element']
        del app_params['element']
        #Run data retrieval job
        DJ = WRCCClasses.SODDataJob('Sodxtrmts', data_params)
        #Obtain metadata and data
        if app_type == 'station':
            meta_dict = DJ.get_station_meta()
            try:
                header.insert(0, ['Station Name', meta_dict['names'][0]])
            except:
                header.insert(0, ['Station Name', ''])
            data = DJ.get_data_station()
        else:
            meta_dict = DJ.get_grid_meta()
            header.insert(0, ['Location (lon, lat)', meta_dict['location_list']])
            data = DJ.get_data_grid()
        #Set dates list
        dates_list = DJ.get_dates_list()
        #Run application
        App = WRCCClasses.SODApplication('Sodxtrmts', data, app_specific_params=app_params)
        results = App.run_app()
        #format results to single station output
        if not results:
            results = []
        else:
            results = results[0][0]
        context['run_done'] = True
        months = WRCCData.MONTH_NAMES_SHORT_CAP
        start_month = int(form['start_month'])
        month_list = [mon for mon in months[(start_month -1):12]]
        if start_month != 1:
            month_list+=months[0:(start_month-1)]
        #generate Mean/Range Graphics
        if results:
            if app_params['units'] == 'english':
                units =  WRCCData.UNITS_ENGLISH[data_params['element']]
            else:
                units = WRCCData.UNITS_METRIC[data_params['element']]
            averages = [[mon] for mon in month_list]
            ranges = [[mon] for mon in month_list]

            if data_params['element'] == 'dtr':
                element_name = 'Temperature Range (' + units + ')'
            elif data_params['element'] == 'pet':
                element_name = 'Potential ET (' + units + ')'
            else:
                element_name = WRCCData.ACIS_ELEMENTS_DICT[data_params['element']]['name_long'] + ' (' + units + ')'
            if 'base_temperature' in form.keys():
                try:
                    base_temperature = int(form['base_temperature'])
                except:
                    base_temperature = ''
            else:
                base_temperature = ''
            for i in range(12):
                try:
                    averages[i].append(float(results[-6][2*(i+1) -1]))
                except:
                    averages[i].append(None)
                for k in [-2, -3]:
                    try:
                        ranges[i].append(float(results[k][2*(i+1) -1]))
                    except:
                        ranges[i].append(None)
            json_dict = {
                'element_name':element_name,
                'element':str(data_params['element']),
                'base_temperature':base_temperature,
                'averages':averages,
                'ranges':ranges,
                'stn_id':meta_dict['ids'][0],
                'stn_name':meta_dict['names'][0],
                'stn_network':meta_dict['networks'][0],
                'stn_state':meta_dict['states'][0],
                'monthly_statistic':WRCCData.DISPLAY_PARAMS[initial['monthly_statistic']],
                'month_list':month_list + ['ANN'],
                'data':results,
                'data_summary':results[-6:],
                'header':header,
                'initial':initial,
                'initial_graph':initial_graph,
                'checkbox_vals':checkbox_vals,
                'checkbox_vals_graph':checkbox_vals_graph
            }
            if dates_list:
                json_dict['start_date'] = dates_list[0][0:4]
                json_dict['end_date'] = dates_list[-1][0:4]
            else:
                json_dict['start_date'] = '----'
                json_dict['end_date'] = '----'
            time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
            if app_type == 'grid':
                name = '_'.join(meta_dict['location_list'])
            else:
                name = meta_dict['ids'][0]
            json_file = '%s_sodxtrmts_%s_%s_%s.json' \
            %(time_stamp, str(name), dates_list[0][0:4], dates_list[-1][0:4])
            json_dict['json_file'] = json_file
            json_dict['JSON_URL'] = settings.TEMP_DIR
            results_json = json.dumps(json_dict)
            with open(settings.TEMP_DIR + '%s' %(json_file),'w+') as f:
                f.write(results_json)
            context['json_dict'] = json_dict
            context['json_file'] = json_file

    #Downlaod Table Data
    if 'formDownload' in request.POST:
        data_format = request.POST.get('data_format', 'clm')
        delimiter = request.POST.get('delimiter', 'comma')
        output_file_name = request.POST.get('output_file_name', 'output')
        json_file = request.POST.get('json_file', None)
        with open(settings.TEMP_DIR + json_file, 'r') as f:
            json_dict =  json.load(f)
        context['json_dict'] = json_dict
        DDJ = WRCCClasses.DownloadDataJob('Sodxtrmts',data_format,delimiter, output_file_name, request=request, json_in_file=settings.TEMP_DIR + json_file)
        return DDJ.write_to_file()

    return render_to_response(url, context, context_instance=RequestContext(request))


def sodsumm(request):
    context = {
        'title': 'Station Climatology'
        }
    initial, checkbox_vals = set_sodsumm_initial(request)
    context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
    if 'formSodsumm' in request.POST or (request.method == 'GET' and 'station_id' in request.GET):
        if request.method == 'GET':
            context['form_message'] = True
        form_initial = set_form_old(request,app_name='sodsumm',clean=False)
        user_params_list, user_params_dict = set_user_params(form_initial, 'sodsumm')
        context['user_params_list'] = user_params_list;context['user_params_dict'] = user_params_dict
        form = set_form_old(request,app_name='sodsumm',clean=False)
        form_cleaned = set_form_old(request,app_name='sodsumm',clean=True)
        initial, checkbox_vals = set_sodsumm_initial(request)
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
        fields_to_check = ['start_year', 'end_year','max_missing_days']
        #Check for form errors
        form_error = check_form(form_cleaned, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            return render_to_response('scenic/apps/station/sodsumm.html', context, context_instance=RequestContext(request))
        data_params = {
                'sid':find_id(form['station_id'], settings.MEDIA_DIR + '/json/US_station_id.json'),
                'start_date':form['start_year'],
                'end_date':form['end_year'],
                'element':'all'
                }
        app_params = {
                'el_type':form['summary_type'],
                'max_missing_days':form['max_missing_days'],
                'units':form['units']
                }
        #Run data retrieval job
        DJ = WRCCClasses.SODDataJob('Sodsumm', data_params)
        #Obtain metadata and perform sanity check
        meta_dict = DJ.get_station_meta()
        if not meta_dict['names'] or not meta_dict['ids']:
            results = {}
            context['run_done']= True
            return render_to_response('scenic/apps/station/sodsumm.html', context, context_instance=RequestContext(request))
        dates_list = DJ.get_dates_list()
        data = DJ.get_data_station()
        if not data or not dates_list:
            results = {}
            context['run_done']= True
            return render_to_response('scenic/apps/station/sodsumm.html', context, context_instance=RequestContext(request))
        #Run application
        App = WRCCClasses.SODApplication('Sodsumm', data, app_specific_params=app_params)
        results = App.run_app()
        #format results to single station output
        if not results:
            results = {}
            context['run_done']= True
            return render_to_response('scenic/apps/station/sodsumm.html', context, context_instance=RequestContext(request))
        else:
            results = dict(results[0])
        context['results'] = results
        #Input parameters:
        context['station_id'] = data_params['sid']
        context['max_missing_days'] = app_params['max_missing_days']
        #Sodsumm table headers for html
        if form['generate_graphics'] == 'T':
            context['tab_names'] = WRCCData.TAB_NAMES_WITH_GRAPHICS[form['summary_type']]
            tab_list = WRCCData.TAB_LIST_WITH_GRAPHICS[form['summary_type']]
            table_list =WRCCData.TABLE_LIST_WITH_GRAPHICS[form['summary_type']]
        else:
            context['tab_names'] = WRCCData.TAB_NAMES_NO_GRAPHICS[form['summary_type']]
            tab_list = WRCCData.TAB_LIST_NO_GRAPHICS[form['summary_type']]
            table_list = WRCCData.TABLE_LIST_NO_GRAPHICS[form['summary_type']]
        context['table_list'] = table_list
        context['tab_list'] = tab_list
        #Define html content
        context['run_done'] = True
        #Check if dates_list is
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

        #Generate grahics
        if form['generate_graphics'] == 'T' and results:
            context['graphics'] = True

        json_list = []
        for tab_idx, tab in enumerate(tab_list):
            table = table_list[tab_idx]
            table_dict = {}
            if form['generate_graphics'] == 'T':
                table_dict = generate_sodsumm_graphics(results,tab,table,form['units'])
            else:
                table_dict = {
                    'table_name':tab,
                    'table_data':results[table]
                }
            #Add other params to table_dict
            table_dict['record_start'] = dates_list[0][0:4]
            table_dict['record_end'] = dates_list[-1][0:4]
            table_dict['stn_name'] = meta_dict['names'][0]
            table_dict['stn_network'] = meta_dict['networks'][0]
            table_dict['stn_state'] = meta_dict['states'][0]
            table_dict['stn_id'] = str(data_params['sid'])
            json_list.append(table_dict)
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        json_file = '%s_sodsumm_%s_%s_%s.json' \
        %(time_stamp, str(data_params['sid']), dates_list[0][0:4], dates_list[-1][0:4])
        WRCCUtils.load_data_to_json_file(settings.TEMP_DIR + json_file, json_list)
        context['JSON_URL'] = settings.TEMP_DIR
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
            DDJ = WRCCClasses.DownloadDataJob('Sodsumm',data_format,delimiter, output_file_name, request=request, json_in_file=settings.TEMP_DIR + json_in_file_name)
            return DDJ.write_to_file()

    return render_to_response('scenic/apps/station/sodsumm.html', context, context_instance=RequestContext(request))

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
    '''
    if not WRCCUtils.check_for_file(settings.TMP_DIR,kml_file_name):
        status = WRCCUtils.generate_kml_file(area_type, overlay_state, kml_file_name, settings.TEMP)
    '''
    return kml_file_path


def set_GET(request):
    if type(request) == dict:
        def Get(key, default):
            if key in request.keys():
                return request[key]
            else:
                return default
    elif request.method == 'GET':
        Get = getattr(request.GET, 'get')
    elif request.method == 'POST':
        Get = getattr(request.POST, 'get')
    return Get

def set_GET_list(request):
    if type(request) == dict:
        def Getlist(key, default):
            if key in request.keys():
                return request[key]
            else:
                return default
    elif request.method == 'GET':
        Getlist = getattr(request.GET, 'getlist')
    elif request.method == 'POST':
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

    return form_error

def find_id(form_name_field, json_file_path):
    '''
    Deals with autofill by station name.
    Note: Autofill sis set up to return name, id
    so we just pick up the id for data analysis
    '''
    i = str(form_name_field)
    name_id_list = i.rsplit(',',1)
    if len(name_id_list) == 1:
        name_id_list = i.rsplit(', ',1)
    name = None
    if len(name_id_list) >=2:
        i= str(name_id_list[-1]).replace(' ','')
        '''
        #Special case CWA --> json file list Las Vegas, NV as name
        #but form field is Las Vegas NV
        if len(i) ==3 and i.isalpha():
            sp = name_id_list[0].rsplit('  ',1)
            if len(sp) != 2:sp = name_id_list[0].rsplit(' ',1)
            name = ', '.join(sp)
        else:
            name = name_id_list[0]
        '''
        name = name_id_list[0]
        return i
    elif len(name_id_list) == 1:
        name_list= i.split(' ')
        #check for digits
        if bool(re.compile('\d').search(i)) and len(name_list) == 1:
            #User entered a station id
            return i
        else:
            name = str(form_name_field)
    if not os.path.isfile(json_file_path) or os.path.getsize(json_file_path) == 0:
        return str(form_name_field)
    #Find id in json file
    json_data = WRCCUtils.load_json_data_from_file(json_file_path)
    for entry in json_data:
        #check if i is id
        if entry['id'] == i:
            #Check that names match
            if name:
                #kml file names have special chars removed
                n = re.sub('[^a-zA-Z0-9\n\.]', ' ', entry['name'])
                if entry['name'].upper() != name.upper() and n.upper() != name.upper():
                    return str(form_name_field)
                else:
                    return i
            else:
                return i
        #Check if i is name
        if entry['name'].upper() == i.upper():
            return entry['id']
    return str(form_name_field)

def set_form_old(request,app_name=None,clean=True):
    '''
    Deals with unicode issues
    and autofill options for identifiers
    '''
    form = {}
    el_list = None
    if isinstance(request,dict):
        form_dict = dict(request)
    elif request.method == 'POST':
        form_dict = dict((x,y) for x,y in request.POST.items())
    elif request.method == 'GET':
        form_dict = dict((x,y) for x,y in request.GET.items())
    else:
        try:
            form_dict = dict((x,y) for x,y in request.items())
        except:
            form_dict = {}

    for key,val in form_dict.iteritems():
        if key == 'csrfmiddlewaretoken':
            continue
        form[str(key)] =str(val)
    #Resolve naming conflicts in data_station/data_gridded
    #similar fields appear in both, main form and download form
    if 'data_format_download' in form.keys():
        form['data_format'] = form['data_format_download']
    if 'delimiter_download' in form.keys():
        form['delimiter']= form['delimiter_download']
    if 'output_file_name_download' in form.keys():
        form['output_file_name'] = form['output_file_name_download']

    #Sanity check for optional inputs
    if 'data_format' not in form.keys():
        form['data_format'] = 'html'
    if 'date_format' not in form.keys():
        form['date_format'] = 'dash'
    if 'delimiter' not in form.keys():
        form['delimiter']= 'comma'
    if 'output_file_name' not in form.keys():
        form['output_file_name'] = 'Output'
    if 'units' not in form.keys():
        form['units']= 'english'
    if 'element' not in form.keys() and 'elements' not in form.keys():
        form['element'] = 'maxt'
        form['elements'] = 'maxt,mint,pcpn'
    if app_name in ['sodxtrmts','sodxtrmts_grid']:
        if app_name == 'sodxtrmts':
            form, checkbox_vals = set_sodxtrmts_initial(form,'station')
        else:
            form, checkbox_vals = set_sodxtrmts_initial(form,'grid')
        if 'element' not in form.keys() and 'elements' in form.keys():
            form['element'] = form['elements']
        form_graph, checkbox_vals = set_sodxtrmts_graph_initial(form)
        form = dict(form.items() + form_graph.items())
        form_pl_opts, checkbox = set_plot_options(form)
        form = dict(form.items() + form_pl_opts.items())
        #FIX ME: not sure why el_type defaults to maxt
        form['el_type'] = form['element']
    if app_name == 'sodsumm':
        if 'summary_type' not in form.keys():
            form['summary_type'] = 'all'
        if 'max_missing_days' not in form.keys():
            form['max_missing_days'] = '5'
        if 'generate_graphics' not in form.keys():
            form['generate_graphics'] = 'T'
        if 'start_date' in form.keys() and 'start_year' not in form.keys():
            form['start_year'] = form['start_date'][0:4]
        if 'end_date' in form.keys() and 'end_year' not in form.keys():
            form['end_year'] = form['end_date'][0:4]

    if app_name == 'station_locator_app':
        if 'elements_constraints' not in form.keys():
            form['elements_constraints'] = 'all'
        if 'dates_constraints' not in form.keys():
            form['dates_constraints'] = 'all'
        if 'elements' not in form.keys():
            form['elements'] = 'maxt,mint,pcpn'
    for key,val in form.iteritems():
        #Override element if needed, elements should be a list
        if str(key) == 'elements':
            try:
                el_list = request.POST.getlist('elements',[])
            except:
                el_list = []
            if el_list:
                #FIX ME!! deal with weird formatting of select multiple
                if len(el_list) == 1 and isinstance(el_list[0], basestring) and len(el_list[0].split(',')) >1:
                    el_list = [str(el) for el in el_list[0].replace(' ','').split(',')]
                else:
                    el_list = [str(el) for el in el_list]
                form[str(key)] = el_list
            else:
                if isinstance(val, list):
                    form[str(key)] = [str(v) for v in val]
                else:
                    form[str(key)] = val.replace(' ','').split(',')
    if not clean:
        #Add degree days as user inputs them
        if 'elements' in form.keys()  and 'add_degree_days' in form.keys() and form['add_degree_days']=='T':
            form['elements']= form['elements'] + form['degree_days'].replace(' ','').split(',')
        return form

    #Clean up form input
    #Check if user autofilled name, if so, change to id
    for key,val in form.iteritems():
        if str(key) in ['station_id','county', 'basin', 'county_warning_area', 'climate_division']:
            form[str(key)] = find_id(str(val),settings.MEDIA_DIR +'json/US_' + str(key) + '.json')
        if str(key) == 'station_ids':
            stn_ids = ''
            stn_list = val.rstrip(',').split(',')
            #Remove leading spaces from list items
            stn_list = [v.lstrip(' ').rstrip(' ') for v in stn_list]
            #Make sure that no station is entered twice
            id_previous = ''
            for idx, stn_name in enumerate(stn_list):
                stn_id = str(find_id(str(stn_name),settings.MEDIA_DIR +'json/US_' + 'station_id' + '.json'))
                if stn_id == id_previous:
                    continue
                id_previous = stn_id
                stn_ids+=stn_id + ','
            #Strip last comma
            stn_ids = stn_ids.rstrip(',')
            form[str(key)] = stn_ids
        #format start and end data
        if str(key) in ['start_date', 'end_date']:
            '''
            if val == 'por':
                if str(key) == 'start_date':idx = 0
                if str(key) == 'end_date':idx = 1
                stn_id = find_id(str(form['station_id']),settings.MEDIA_DIR +'json/US_station_id.json')
                form[str(key)] = WRCCUtils.find_valid_daterange(stn_id, start_date='por', end_date='por', max_or_min='max')[idx]
            else:
                form[str(key)] = str(val).replace('-','').replace(':','').replace('/','').replace(' ','')
            '''
            form[str(key)] = str(val).replace('-','').replace(':','').replace('/','').replace(' ','')
        #Deal with PRISM data and add degree day elements
        if str(key) == 'elements':
            el_list_new = val
            #form[str(key)] = str(val).replace(' ','')
            #if PRISM data, change element names if monthly/yearly data
            if 'grid' in form.keys() and form['grid'] == '21':
                if 'temporal_resolution' in form.keys() and form['temporal_resolution'] in ['yly','mly']:
                    for el_idx,el in enumerate(el_list_new):
                        el_list_new[el_idx] = '%s_%s' %(form['temporal_resolution'], el)
            #Add special degree days
            if 'add_degree_days' in form.keys() and form['add_degree_days'] == 'T':
                dd_list = form['degree_days'].replace(' ','').split(',')
                #Convert degree days temp to Fahreheit if units are metric
                if 'units' in form.keys() and form['units'] == 'metric':
                    for idx,dd in enumerate(dd_list):
                        el_strip, base_temp = WRCCUtils.get_el_and_base_temp(dd)
                        dd_list[idx] = el_strip + str(WRCCUtils.convert_to_english('maxt',base_temp))
                el_list_new+=dd_list
            form[str(key)] = ','.join(el_list_new)
    return form


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
    header_order =['station_id','start_year', 'end_year', '','element']
    if form['element'] in ['gdd', 'hdd', 'cdd']:header_order+=['base_temperature']
    header_order+=['monthly_statistic']
    if form['departures_from_averages'] == 'T':
         header_order+=['departures_from_averages', '']
    else:
        header_order+=['']
    if form['monthly_statistic'] == 'ndays':
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
        if key in ['less_greater_or_between','frequency_analysis_type','frequency_analysis', 'departures_from_averages', 'monthly_statistic', 'elements','element']:
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

#####################
#Results formatting
#####################
def compute_spatial_summary_summary(req, search_params, poly, PointIn):
    #Sanity check
    element_list = search_params['elements'].replace(' ','').split(',')
    if not 'meta' in req.keys():
        return []
    if not 'lat' in req['meta'].keys():
        return []
    if not 'data' in req.keys():
        return []
    if 'location' in search_params.keys() or isinstance(req['meta']['lat'],float):
        lats_bbox_unique = [req['meta']['lat']]
        lons_bbox_unique = [req['meta']['lon']]
    else:
        lats_bbox_unique=[lat_grid[0] for lat_grid in req['meta']['lat']]
        lons_bbox_unique = req['meta']['lon'][0]
    #Generate time series from data request
    summary_time_series = [[[str(dat[0])] for dat in req['data']] for el in element_list]
    download_data = [[str(dat[0])] for dat in req['data']]
    #list of list holding just the data values for each day at each gridpoint
    values_poly = [[[] for dat in req['data']] for el in element_list]
    #Check each bbox unique lat, lon combintation for containment in the polygon
    for lat_idx,lat in enumerate(lats_bbox_unique):
        for lon_idx, lon in enumerate(lons_bbox_unique):
            #see if lat/lon inside poly
            if not poly:
                point_in = True
            else:
                point_in = PointIn(lon, lat, poly)
            if point_in:
                #point lies witin shape, add data to data_poly
                for date_idx, date_data in enumerate(req['data']):
                    for el_idx, el in enumerate(element_list):
                        if 'location' in search_params.keys() or isinstance(req['meta']['lat'],float):
                            try:
                                if 'units' in search_params.keys() and search_params['units'] == 'metric':
                                    val = WRCCUtils.convert_to_metric(el, float(date_data[el_idx+1]))
                                else:
                                    val = float(date_data[el_idx+1])
                            except:
                                continue
                        else:
                            try:
                                if 'units' in search_params.keys() and search_params['units'] == 'metric':
                                    val = WRCCUtils.convert_to_metric(el,float(date_data[el_idx+1][lat_idx][lon_idx]))
                                else:
                                    val = float(date_data[el_idx+1][lat_idx][lon_idx])
                            except:
                                continue
                        if abs(val + 999.0) > 0.001 and abs(val - 999.0)>0.001:
                            values_poly[el_idx][date_idx].append(val)
    #Summarize data
    for el_idx, el in enumerate(element_list):
        if not values_poly[el_idx]:
            for date_idx, val_list in enumerate(values_poly[el_idx]):
                summary_time_series[el_idx][date_idx].append('-----')
                download_data[date_idx].append('-----')
        else:
            for date_idx, val_list in enumerate(values_poly[el_idx]):
                if not val_list:
                    summary_time_series[el_idx][date_idx].append('-----')
                    download_data[date_idx].append('-----')
                    continue
                if search_params['spatial_summary'] == 'sum':
                    summary_time_series[el_idx][date_idx].append(round(sum(val_list),2))
                    download_data[date_idx].append(round(sum(val_list),2))
                elif search_params['spatial_summary'] == 'max':
                    summary_time_series[el_idx][date_idx].append(round(max(val_list),2))
                    download_data[date_idx].append(round(max(val_list),2))
                elif search_params['spatial_summary'] == 'min':
                    summary_time_series[el_idx][date_idx].append(round(min(val_list),2))
                    download_data[date_idx].append(round(max(val_list),2))
                elif search_params['spatial_summary'] == 'mean':
                    if val_list:
                        summary_time_series[el_idx][date_idx].append(round(sum(val_list) / len(val_list),2))
                        download_data[date_idx].append(round(sum(val_list) / len(val_list),2))
                    else:
                        summary_time_series[el_idx][date_idx].append('-----')
                        download_data[date_idx].append('-----')
    return summary_time_series, download_data

def write_monthly_aves_results(req, form_data, monthly_aves):
    results = [{} for k in form_data['elements']]
    for el_idx, el in enumerate(form_data['elements']):
        if 'units' in form_data.keys() and form_data['units'] == 'metric':
            el_strip, base_temp = WRCCUtils.get_el_and_base_temp(el, units='metric')
        else:
            el_strip, base_temp = WRCCUtils.get_el_and_base_temp(el)
        if base_temp:
            results[el_idx] = {'element_long': WRCCData.ACIS_ELEMENTS_DICT[el_strip]['name_long'] + ' Base Temperature: ' + str(base_temp)}
        else:
            results[el_idx] = {'element_long': WRCCData.ACIS_ELEMENTS_DICT[el_strip]['name_long']}
        results[el_idx]['element'] = str(el)
        if form_data['units'] == 'metric':
            results[el_idx]['unit'] = WRCCData.UNITS_LONG[WRCCData.UNITS_METRIC[el_strip]]
        else:
            results[el_idx]['unit'] = WRCCData.UNITS_LONG[WRCCData.UNITS_ENGLISH[el_strip]]
        results[el_idx]['stn_id']= find_id(str(form_data['station_id']), settings.MEDIA_DIR +'json/US_station_id.json')

        if form_data['start_date'].lower() == 'por':
            if len(req['meta']['valid_daterange'][el_idx]) == 2:
                results[el_idx]['record_start'] = str(req['meta']['valid_daterange'][el_idx][0])
            else:
                #no valid daterange found
                results[el_idx]['record_start'] = ['0000-00-00']
        else:
            results[el_idx]['record_start'] = '%s-%s-%s' % (form_data['start_date'][0:4], form_data['start_date'][4:6], form_data['start_date'][6:8])

        if form_data['end_date'].lower() == 'por':
            if len(req['meta']['valid_daterange'][el_idx]) == 2:
                results[el_idx]['record_end'] = str(req['meta']['valid_daterange'][el_idx][1])
            else:
                results[el_idx]['record_end'] = ['0000-00-00']
        else:
            results[el_idx]['record_end'] = '%s-%s-%s' % (form_data['end_date'][0:4], form_data['end_date'][4:6], form_data['end_date'][6:8])
        #Check if user dates lie outside of POR of station
        if form_data['start_date'].lower() != 'por' and form_data['end_date'].lower() != 'por' and len(req['meta']['valid_daterange'][el_idx]) == 2:
            user_st = datetime.datetime(int(form_data['start_date'][0:4]), int(form_data['start_date'][4:6]), int(form_data['start_date'][6:8]))
            user_end = datetime.datetime(int(form_data['end_date'][0:4]), int(form_data['end_date'][4:6]), int(form_data['end_date'][6:8]))
            por_st = datetime.datetime(int(req['meta']['valid_daterange'][el_idx][0][0:4]), int(req['meta']['valid_daterange'][el_idx][0][5:7]), int(req['meta']['valid_daterange'][el_idx][0][8:10]))
            por_end = datetime.datetime(int(req['meta']['valid_daterange'][el_idx][1][0:4]), int(req['meta']['valid_daterange'][el_idx][1][5:7]), int(req['meta']['valid_daterange'][el_idx][1][8:10]))
            if (user_end < por_st and user_st <por_st) or (user_st >por_end and user_end >por_end):
                results[el_idx]['error'] = 'Start and End date lie outside of period of record for %s. Period of record is: %s - %s' %(el, req['meta']['valid_daterange'][el_idx][0], req['meta']['valid_daterange'][el_idx][1])
        results[el_idx]['data'] = monthly_aves[el]
        if 'meta' in req.keys():
            results[el_idx]['stn_name'] = str(req['meta']['name'])
            results[el_idx]['state'] = str(req['meta']['state'])
    return results

def write_monthly_aves_meta(req, form_data):
    #get rid of unicode and special chars in station name
    Meta = WRCCUtils.format_stn_meta(req['meta'])
    #format meta data
    el_list = form_data['elements']
    valid_dr = []
    for idx, el in enumerate(el_list):
        try:
            valid_dr.append('%s: %s - %s ' %(str(el),str(Meta['valid_daterange'][idx][0]),str(Meta['valid_daterange'][idx][1])))
        except:
            valid_dr.append(str(el))

    key_order = ['name', 'sids','valid_daterange', 'll', 'elev', 'state', 'county', 'climdiv', 'uid']
    meta = WRCCUtils.metadict_to_display(Meta, key_order)
    #Override valid daterange
    meta_vd = ['Valid Daterange']
    vd =''
    for idx,el in enumerate(el_list):
        try:
            v_el = str(Meta['valid_daterange'][idx])
        except:
            v_el = '[]'
        vd+= el + ': ' + v_el + ', '
    meta_vd.append(vd)
    meta[2] = meta_vd
    el_string = ''
    for el in el_list:
        if 'units' in form_data.keys() and form_data['units'] == 'metric':
            el_strip, base_temp = WRCCUtils.get_el_and_base_temp(el, units='metric')
        else:
            el_strip, base_temp = WRCCUtils.get_el_and_base_temp(el)
        if form_data['units'] == 'metric':unit = WRCCData.UNITS_METRIC[el_strip]
        else:unit = WRCCData.UNITS_ENGLISH[el_strip]
        if base_temp:
            el_string+= WRCCData.ACIS_ELEMENTS_DICT[el_strip]['name_long'] + '('+ unit + ')' + ' Base Temp: ' + str(base_temp) + ', '
        else:
            el_string+=WRCCData.ACIS_ELEMENTS_DICT[el_strip]['name_long'] + '('+ unit + ')' +  ', '
    meta.insert(2, ['Elements', el_string])
    meta.insert(3, ['Units', form_data['units']])
    return meta

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

def set_spatial_summary_params(form):
    key_order = ['Area Type','elements','start_date', 'end_date', 'summary', 'grid','running_mean_days']
    display_params_list = [[] for k in range(len(key_order))]
    search_params = {}
    el_string, el_list = set_el_string_and_list(form)
    '''
    if isinstance(form['elements'],list):
        el_list = [str(el) for el in form['elements']]
    elif isinstance(form['elements'],basestring):
        el_list = form['elements'].replace(' ','').split(',')
    else:
        try:
            el_list = form['elements_string'].replace('  ','').split(',')
        except:
            el_list = []
    '''
    el_list_display = []
    for el_idx, el in enumerate(el_list):
        if 'units' in form.keys() and form['units'] == 'metric':
            el_strip, base_temp = WRCCUtils.get_el_and_base_temp(el, units='metric')
        else:
            el_strip, base_temp = WRCCUtils.get_el_and_base_temp(el)
        if 'units' in form.keys() and form['units'] == 'metric':
            el_list_display.append(el + ' (' + WRCCData.UNITS_METRIC[el_strip]+ ')')
        if 'units' in form.keys() and form['units'] == 'english':
            el_list_display.append(el + ' (' + WRCCData.UNITS_ENGLISH[el_strip]+ ')')
    search_params['element_list'] = el_list_display
    if form['select_grid_by'] == 'shape' and len(form['shape'].split(',')) > 8:
        display_params_list[0]=['Area','Custom Shape']
        search_params['area_description'] = 'Custom Shape'
        search_params['shape_coords'] = form['shape'].split(',')
    else:
        search_params['area_description'] = WRCCData.DISPLAY_PARAMS[form['select_grid_by']] + ': ' + form[form['select_grid_by']]
        display_params_list[0]=[WRCCData.DISPLAY_PARAMS[form['select_grid_by']],form[form['select_grid_by']]]
    for key, val in form.iteritems():
        #Convert to string to avoid unicode issues
        search_params[key] = str(val)
        if key == 'grid':
            display_params_list[5] = [WRCCData.DISPLAY_PARAMS[key], WRCCData.GRID_CHOICES[val][0]]
        elif key == 'spatial_summary':
            display_params_list[4] = [WRCCData.DISPLAY_PARAMS[key], WRCCData.DISPLAY_PARAMS[val]]
            search_params['spatial_summary_long'] = WRCCData.DISPLAY_PARAMS[form[key]]
        elif key == 'elements':
            el_list_long =[]
            dd_list =[]
            if 'degree_days' in form.keys():
                dd_list = form['degree_days'].replace(' ','').split(',')
            for el_idx, el in enumerate(el_list):
                el_short, base_temp = WRCCUtils.get_el_and_base_temp(el)
                if 'units' in form.keys() and form['units'] == 'metric':
                    ut = WRCCData.UNITS_METRIC[el_short]
                else:
                    ut = WRCCData.UNITS_ENGLISH[el_short]
                if base_temp:
                    #if metric pick original user input base temp
                    if 'units' in form.keys() and form['units'] == 'metric':
                        if el in dd_list:
                            idx = dd_list.index(el)
                            base_temp = dd_list[dx][3:]
                        else:
                            base_temp = int(round(WRCCUtils.convert_to_metric('maxt', base_temp)))
                    bt = ' Base Temp: ' + str(base_temp) + ' (' +  ut + ')'
                else:
                    bt = ''
                try:
                    int(el[3:])
                    el_list_long.append(WRCCData.DISPLAY_PARAMS[el[0:3]] + ' ('+ ut + ')' + bt)
                except:
                    el_list_long.append(WRCCData.DISPLAY_PARAMS[el] + ' ('+ ut + ')' + bt)
            display_params_list[1] = [WRCCData.DISPLAY_PARAMS[key], ','.join(el_list_long)]
            search_params['element_list_long'] = el_list_long
        else:
            value = str(val)
            if val =='T':value='Yes'
            if val == 'F':value = 'No'
            try:
                idx = key_order.index(key)
                display_params_list[idx] = [WRCCData.DISPLAY_PARAMS[key], value]
            except ValueError:
                pass
    if form['show_running_mean'] == 'F':
        del display_params_list[-1]
    return search_params, display_params_list

def set_data_gridded_params(form):
    #display_params_list used to dispaly search params to user
    #params_dict used to link to relevant apps in html doc
    if not form:
        return {}

    #Set defaults in case we are linked from other pages
    if 'units' not in form.keys():
        form['units']='english'

    key_order = [form['select_grid_by'], 'elements','degree_days', 'grid', 'start_date', 'end_date','temporal_resolution', 'data_summary', 'units']
    display_params_list = [[] for k in range(len(key_order))]
    params_dict = {'area_type_value':form[form['select_grid_by']],'user_id': form[form['select_grid_by']]}
    for key, val in form.iteritems():
        #Convert to string to avoid unicode issues
        params_dict[key] = str(val)

        if key == 'grid':
            display_params_list[2] = [WRCCData.DISPLAY_PARAMS[key], WRCCData.GRID_CHOICES[val][0]]
        elif key in ['data_summary','temporal_resolution']:
            display_params_list[3] = [WRCCData.DISPLAY_PARAMS[key], WRCCData.DISPLAY_PARAMS[val]]
            #params_dict[WRCCData.DISPLAY_PARAMS[key]] = WRCCData.DISPLAY_PARAMS[val]
        elif key == 'elements':
            tr = form['temporal_resolution']
            pre_el =''
            if tr in ['yly','mly']:
                pre_el = tr + '_'
            if isinstance(val, list):
                el_list = val
            elif isinstance(val, basestring):
                el_list = val.replace(' ','').split(',')
            else:
                el_list = val
            unit_dict ={};base_temp_dict = {};base_el_dict={}
            params_dict['elements'] = ','.join(el_list)
            params_dict['element_list'] = el_list
            params_dict['elements_string'] = ','.join(el_list)
            if len(el_list) == 1:
                params_dict['element'] =  el_list[0]
            elems_long = []
            display_params_list[1] = [WRCCData.DISPLAY_PARAMS[key], '']
            #params_dict[key] = ''
            for el_idx, el in enumerate(el_list):
                if 'units' in form.keys() and form['units'] == 'metric':
                    el_strip, base_temp = WRCCUtils.get_el_and_base_temp(el,units='metric')
                    unit_dict[el] = WRCCData.UNITS_METRIC[el_strip]
                else:
                    el_strip, base_temp = WRCCUtils.get_el_and_base_temp(el)
                    unit_dict[el] = WRCCData.UNITS_ENGLISH[el_strip]
                base_el_dict[el] = el_strip
                if not base_temp:
                    BT=''
                    base_temp_dict[el] = ''
                else:
                    BT = ', Base Temp: ' + str(base_temp)
                    base_temp_dict[el] = str(base_temp)
                display_params_list[1][1]+= WRCCData.DISPLAY_PARAMS[pre_el + el_strip] + BT
                elems_long.append(WRCCData.DISPLAY_PARAMS[pre_el + el_strip] + BT)
            params_dict['unit_dict'] = unit_dict
            params_dict['base_temp_dict'] = base_temp_dict
            params_dict['base_el_dict'] = base_el_dict
            params_dict['elems_long'] = elems_long
            #determine which apps to link to
            if len(val) == 1:
                try:
                    int(val[3:5])
                    el = val[0:3]
                    if 'units' in form.keys() and form['units'] == 'metric':
                        base_temp = WRCCUtils.convert_to_english(val[3:5])
                    else:
                        base_temp = val[3:5]
                except:
                    el = val[0];base_temp=''
                if str(el) in ['maxt', 'mint', 'avgt', 'gdd', 'hdd', 'cdd', 'pcpn']:
                    params_dict['element'] = el + base_temp
        elif key == 'delimiter':
            params_dict['delimiter'] = WRCCData.DELIMITERS[val]
        else:
            try:
                idx = key_order.index(key)
                display_params_list[idx] = [WRCCData.DISPLAY_PARAMS[key], str(val)]
            except ValueError:
                if key in ['basin', 'county_warning_area', 'climate_division', 'state', 'bounding_box', 'shape']:
                    display_params_list.insert(1, [WRCCData.DISPLAY_PARAMS[key], str(val)])
    if 'delimiter' not in params_dict.keys():
        params_dict['delimiter'] = ' '
    if form['data_summary'] == 'temporal':
        display_params_list.append(['Temporal Summary', form['temporal_summary']])
    if form['data_summary'] == 'spatial':
        display_params_list.append(['Spatial Summary', form['temporal_summary']])
    return display_params_list, params_dict


def set_data_station_params(form):
    #display_params_list used to dispaly search params to user
    #params_dict iused to link to relevant apps in html doc
    if not form:
        return {}

    key_order = [form['select_stations_by'], 'elements', 'start_date', 'end_date', 'units']
    defaults = ['station_ids', 'maxt,mint,pcpn', fourtnight, yesterday,'english']
    display_params_list = [[] for k in range(len(key_order))]
    params_dict = {}
    for key_idx, key in enumerate(key_order):
        try:
            display_params_list[key_idx] = [WRCCData.DISPLAY_PARAMS[key],form[key]]
        except:
            display_params_list[key_idx] = [WRCCData.DISPLAY_PARAMS[key], defaults[key_idx]]
    for key, val in form.iteritems():
        #Need station list for missing data
        if key == form['select_stations_by'] and key not in  ['station_ids', 'state', 'shape']:
            params_dict[key] = find_id(val, settings.MEDIA_DIR + '/json/US_' + key +'.json')
            params_dict['user_id']= val
        elif key == form['select_stations_by'] and key == 'station_ids':
            params_dict['station_list'] = form['station_ids'].split(',')
        elif key == 'delimiter':
            if 'data_format' in form.keys() and form['data_format'] == 'html':
                params_dict['delimiter'] = WRCCData.DELIMITERS['space']
            else:
                params_dict['delimiter'] = WRCCData.DELIMITERS[val]
        elif key in ['show_flags', 'show_observation_time']:
            params_dict[key] = val
        elif key == 'elements':
            if isinstance(val, basestring):
                el_list = val.replace(' ', '').split(',')
            elif isinstance(val,list):
                el_list = val
            else:
                el_list = val
            params_dict[key] = val
            idx = key_order.index('elements')
            display_params_list[idx]=['Elements', '']
            unit_dict ={};base_temp_dict = {};base_el_dict={}
            params_dict['elements'] = ','.join(el_list)
            params_dict['element_list'] = el_list
            params_dict['elements_string'] = ','.join(el_list)
            if len(el_list) == 1:
                params_dict['element'] =  el_list[0]
            elems_long = []
            display_params_list[1] = [WRCCData.DISPLAY_PARAMS[key], '']
            #params_dict[key] = ''
            for el_idx, el in enumerate(el_list):
                if 'units' in form.keys() and form['units'] == 'metric':
                    el_strip, base_temp = WRCCUtils.get_el_and_base_temp(el,units='metric')
                    unit_dict[el] = WRCCData.UNITS_METRIC[el_strip]
                else:
                    el_strip, base_temp = WRCCUtils.get_el_and_base_temp(el)
                    unit_dict[el] = WRCCData.UNITS_ENGLISH[el_strip]
                base_el_dict[el] = el_strip
                if not base_temp:
                    BT=''
                    base_temp_dict[el] = ''
                else:
                    BT = ', Base Temp: ' + str(base_temp)
                    base_temp_dict[el] = str(base_temp)
                display_params_list[idx][1]+= WRCCData.DISPLAY_PARAMS[el_strip] + BT
                elems_long.append(WRCCData.DISPLAY_PARAMS[el_strip] + BT)
            params_dict['unit_dict'] = unit_dict
            params_dict['base_temp_dict'] = base_temp_dict
            params_dict['base_el_dict'] = base_el_dict
            params_dict['elems_long'] = elems_long

            '''
            elems_long = []
            params_dict[key] = val
            idx = key_order.index('elements')
            if isinstance(val, list):
                el_str_long = ''
                for v in val:
                    if 'units' in form.keys() and form['units'] == 'metric':
                        el_strip, base_temp = WRCCUtils.get_el_and_base_temp(v, units='metric')
                    else:
                        el_strip, base_temp = WRCCUtils.get_el_and_base_temp(v)
                    if base_temp:
                        el_str_long+=WRCCData.ACIS_ELEMENTS_DICT[el_strip]['name_long'] + '(' + str(base_temp) + '), '
                    else:
                        el_str_long+=WRCCData.ACIS_ELEMENTS_DICT[el_strip]['name_long'] + ', '
                el_str_long.rstrip(', ')
                display_params_list[idx]=['Elements',el_str_long]
            '''
        else:
            params_dict[key] = val
    return display_params_list, params_dict

def set_station_locator_params(form):
    #display_params_list used to dispaly search params to user
    #params_dict iused to link to relevant apps in html doc
    if not form:
        return {}

    key_order = ['select_stations_by', form['select_stations_by'], 'elements', 'elements_constraints','start_date', 'end_date', 'dates_constraints']
    display_params_list = [[] for k in range(len(key_order))]
    params_dict = {'units':'english'}
    for key, val in form.iteritems():
        if key == 'elements':
            if isinstance(val, basestring):
                el_list = val.replace(' ', '').split(',')
            elif isinstance(val,list):
                el_list = val
            else:
                el_list = val
            elems_long = []
            #display_params_list.insert(1, [WRCCData.DISPLAY_PARAMS[key], ''])
            params_dict[key] = ','.join(el_list)
            params_dict[key].rstrip(',')
            for el_idx, el in enumerate(el_list):
                try:
                    int(el[3:5])
                    #display_params_list[2] = [WRCCData.DISPLAY_PARAMS[key],WRCCData.DISPLAY_PARAMS[el[0:3]] + ' Base Temperature '+ el[3:5]]
                    elems_long.append(WRCCData.DISPLAY_PARAMS[el[0:3]] + ' Base Temperature '+ el[3:5])
                except:
                    #display_params_list[2] = [WRCCData.DISPLAY_PARAMS[key],WRCCData.DISPLAY_PARAMS[el]]
                    elems_long.append(WRCCData.DISPLAY_PARAMS[el])
                if el_idx != 0 and el_idx != len(form['elements']) - 1:
                    #display_params_list[2][1]+=', '
                    params_dict['elements']+=','
            display_params_list[2] = [WRCCData.DISPLAY_PARAMS[key],', \n'.join(elems_long)]
            params_dict['elements'].rstrip(',')
            params_dict['elems_long'] = elems_long
        elif key == 'select_stations_by':
            display_params_list[0] = [WRCCData.DISPLAY_PARAMS[key],WRCCData.DISPLAY_PARAMS[form[key]]]
        elif key == 'station_ids':
            #Deal with linebreaks
            display_params_list[1] = [WRCCData.DISPLAY_PARAMS[key],form[key]]
            stn_list = str(val).replace(' ','').split(',')
            num_stns = len(stn_list)
            if num_stns > 5:
                div = num_stns / 5
                for i in range(1,div):
                    stn_list[i*5]= '\n' + stn_list[i*5]
                    #stn_list.insert(i*5,'\n')
                display_params_list[1][1] = ','.join(stn_list)
        else:
            try:
                idx = key_order.index(key)
                display_params_list[idx] = [WRCCData.DISPLAY_PARAMS[key], str(val)]
                params_dict[key] = str(val)
            except ValueError:
                pass
                '''
                if key in ['station_id','station_ids', 'stnid', 'stn_id','basin', 'county_warning_area', 'climate_division', 'state', 'bounding_box', 'shape']:
                    display_params_list.insert(1, [WRCCData.DISPLAY_PARAMS[key], str(val)])
                '''
    return display_params_list, params_dict


def set_user_params(form, app_name):
    '''
    If user comes from different subpage,
    we set the user parameters for sidplay to user
    '''
    f = {}
    for key,val in form.iteritems():
        #Remove hash tags and extra quotes from strings, they give issue in request.GET
        if isinstance(val, basestring):
            f[key] =val.replace('#','').replace('\'','')
        else:
            f[key] = val
    if app_name in ['data_gridded', 'spatial_summary', 'temporal_summary']:
        area_select = 'select_grid_by'
        if app_name == 'temporal_summary':
            f['temporal_resolution'] = 'dly'
    elif app_name in ['monthly_aves','sodsumm','data_station']:
        area_select = 'select_stations_by'
        if not 'select_stations_by' in f.keys():
            f['select_stations_by'] = 'station_id'
    elif app_name == 'station_locator_app':
            area_select = 'select_stations_by'
            if not 'select_stations_by' in f.keys():
                try:
                    f['select_stations_by'] = f['area_select']
                except:
                    if 'station_id' in f.keys():f['select_stations_by']='station_id'
                    if 'station_ids' in f.keys():f['select_stations_by']='station_ids'
                    if 'state' in f.keys():f['select_stations_by']='state'
                    if 'county' in f.keys():f['select_stations_by']='county'
                    if 'county_warning_area' in f.keys():f['select_stations_by']='county_warning_area'
                    if 'basin' in f.keys():f['select_stations_by']='basin'
                    if 'climate_division' in f.keys():f['select_stations_by']='climate_division'
                    if 'shape' in f.keys():f['select_stations_by']='shape'
            if not 'select_stations_by' in f.keys():
                f['select_stations_by']='state'
                f['state'] = 'NV'
    elif app_name == 'sodxtrmts':
        area_select = 'select_stations_by'
        if not 'select_stations_by' in f.keys():
            f['select_stations_by'] = 'station_id'
        if 'location' in form.keys():
            area_select = 'select_grid_by'
            if not 'select_grid_by' in f.keys():
                f['select_grid_by'] = 'location'
    elif app_name == 'apps_station':
        area_select = 'select_stations_by'
        f[area_select] = 'station_id'
        if 'element' not in f.keys() and 'elements' not in f.keys():
            f['element'] = 'maxt'
            f['elements'] = 'maxt,mint,pcpn'
    elif app_name == 'data_comparison':
        area_select = 'select_grid_by'
        f['select_grid_by'] = 'location'
    else:
        area_select = 'select_stations_by'
    #Deal with elements
    el_list = []
    if 'elements' in f.keys():
        if isinstance(f['elements'], list):
            '''
            if app_name == 'station_locator_app':
                el_list = f['elements']
            else:
                el_list = f['elements']
            '''
            el_list = f['elements']
        elif isinstance(f['elements'], basestring):
            el_list = f['elements'].replace(' ','').split(',')
    elif 'element' in f.keys():
        el_list = [str(f['element'])]
    user_params_list = []
    user_params_dict ={
        'area_select':f[area_select],
        area_select:f[area_select],
        f[area_select]:f[f[area_select]],
        'elements':','.join(el_list).rstrip(','),
        'element_list':el_list
    }
    if app_name == 'sodxtrmts' and 'elements' in f.keys():
        user_params_dict['element'] = user_params_dict['elements']
    key_list = []
    if 'start_date' in f.keys():
        key_list = ['start_date','end_date']
    elif 'start_year' in f.keys():
        key_list = ['start_year','end_year']
    for key in key_list:
            user_params_dict[key] = f[key]
            user_params_list.append([WRCCData.DISPLAY_PARAMS[key],f[key]])
    if app_name in ['sodxtrmts','sodsumm'] and key_list == ['start_date','end_date']:
        user_params_dict['start_year'] = user_params_dict['start_date'][0:4]
        user_params_dict['end_year'] = user_params_dict['end_date'][0:4]
    els_long = ''
    for idx,el in enumerate(el_list):
        if 'units' in f.keys() and f['units'] == 'metric':
            el_strip,base_temp = WRCCUtils.get_el_and_base_temp(el,units='metric')
        else:
            el_strip,base_temp = WRCCUtils.get_el_and_base_temp(el)
        if base_temp:
            els_long+=WRCCData.ACIS_ELEMENTS_DICT[el_strip]['name_long'] + ' Base Temp.: ' + str(base_temp) + ', '
            if app_name == 'sodxtrmts' and el_strip in ['hdd','cdd','gdd']:
                user_params_dict['base_temperature'] = base_temp
        else:
            els_long+=WRCCData.ACIS_ELEMENTS_DICT[el_strip]['name_long'] + ', '
    user_params_list.insert(0,['Elements',els_long])
    try:
        user_params_list.insert(0,[WRCCData.DISPLAY_PARAMS[f[area_select]],f[f[area_select]]])
    except:
        pass
    #user_params_list.insert(0,[WRCCData.DISPLAY_PARAMS[f[area_select]],f[f[area_select]]])
    if 'temporal_resolution' in f.keys():
        user_params_dict['temporal_resolution'] = f['temporal_resolution']
    if 'temporal_summary' in f.keys():
        user_params_list.append(['Temporal Summary', WRCCData.DISPLAY_PARAMS[f['temporal_summary']]])
        user_params_dict['temporal_summary'] = f['temporal_summary']
        user_params_dict['data_summary'] = 'temporal'
    if 'spatial_summary' in f.keys():
        user_params_list.append(['Spatial Summary', WRCCData.DISPLAY_PARAMS[f['spatial_summary']]])
        user_params_dict['spatial_summary'] = f['spatial_summary']
        user_params_dict['data_summary'] = 'spatial'
    if 'grid' in f.keys():
        user_params_list.append(['Grid', WRCCData.GRID_CHOICES[f['grid']][0]])
        user_params_dict['grid'] = f['grid']
    if 'units' in f.keys():
        user_params_list.append(['Units', WRCCData.DISPLAY_PARAMS[f['units']]])
        user_params_dict['units'] = f['units']
    if 'add_degree_days' in f.keys() and 'degree_days' in f.keys() and f['add_degree_days'] =='T':
        user_params_dict['add_degree_days'] = f['add_degree_days']
        user_params_dict['degree_days'] = f['degree_days']
    #If link from station_locator, check for area type and value and add to params
    if 'select_stations_by'in f.keys():
        if f['select_stations_by'] == 'station_ids' or f[area_select] == 'station_ids':
            user_params_dict['station_list'] = f['station_ids'].split(',')
            for k in ['basin', 'climate_division','county', 'county_warning_area', 'state', 'shape']:
                if k in f.keys():
                    user_params_list.insert(0,[WRCCData.DISPLAY_PARAMS[k],f[k]])
    return user_params_list, user_params_dict

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

def set_plot_options(request):
    initial = {}
    checkbox_vals = {}
    Get = set_GET(request)
    initial['graph_title'] = Get('graph_title','Use default')
    initial['image_size'] = Get('image_size', 'medium')
    initial['major_grid']  = Get('major_grid', 'T')
    initial['minor_grid'] = Get('minor_grid', 'F')
    initial['connector_line'] = str(Get('connector_line', 'T'))
    initial['connector_line_width'] = Get('connector_line_width', '1')
    initial['markers'] = Get('markers', 'T')
    initial['marker_type'] = Get('marker_type', 'diamond')
    initial['vertical_axis_min']= Get('vertical_axis_min', 'Use default')
    initial['vertical_axis_max']= Get('vertical_axis_max', 'Use default')
    #set the check box values
    for bl in ['T','F']:
        for cbv in ['major_grid', 'minor_grid','connector_line', 'markers']:
            checkbox_vals[cbv + '_' + bl + '_selected'] = ''
            if initial[cbv] == bl:
                checkbox_vals[cbv + '_' + bl + '_selected'] = 'selected'
    for image_size in ['small', 'medium', 'large', 'larger', 'extra_large', 'wide', 'wider', 'widest']:
        checkbox_vals['image_size' + '_' + image_size + '_selected'] = ''
        if initial['image_size'] == image_size:
            checkbox_vals['image_size' + '_' + image_size + '_selected'] = 'selected'
    for marker_type in ['diamond', 'circle', 'square', 'triangle', 'triangle_down']:
        checkbox_vals['marker_type' + '_' + marker_type + '_selected'] = ''
        if initial['marker_type'] == marker_type:
            checkbox_vals['marker_type' + '_' + marker_type + '_selected'] = 'selected'
    return initial, checkbox_vals


def set_sodsumm_initial(request):
    Get = set_GET(request)
    initial = {};checkbox_vals = {};
    initial['autofill_list'] = 'US_station_id'
    initial['station_id'] = Get('station_id','RENO TAHOE INTL AP, 266779')
    initial['start_year'] = Get('start_year', Get('start_date','POR'))
    initial['end_year'] = Get('end_year', Get('end_date','POR'))
    if len(initial['start_year'])>4:initial['start_year'] = initial['start_year'][0:4]
    if len(initial['end_year'])>4:initial['end_year'] = initial['end_year'][0:4]
    initial['element'] = Get('element',Get('elements','pcpn').replace(' ','').split(',')[0])
    initial['units'] =  Get('units','english')
    initial['date_type'] = 'y'
    initial['summary_type'] = Get('summary_type','all')
    initial['max_missing_days'] = Get('max_missing_days','5')
    initial['generate_graphics'] = Get('generate_graphics','T')
    for st in ['all','temp','prsn','both','hc','g']:
        checkbox_vals[st + '_selected'] =''
        if st == initial['summary_type']:
            checkbox_vals[st + '_selected'] ='selected'
    for u in ['english', 'metric']:
        checkbox_vals['units_' + u + '_selected'] =''
        if u == initial['units']:
            checkbox_vals['units_' +u + '_selected'] ='selected'
    for bl in ['T','F']:
        checkbox_vals['generate_graphics' + '_' + bl + '_selected'] = ''
        if initial['generate_graphics'] == bl:
            checkbox_vals['generate_graphics' + '_' + bl + '_selected'] = 'selected'
    return initial,checkbox_vals

def set_sodxtrmts_initial(request,app_type):
    initial = {}
    checkbox_vals = {}
    Get = set_GET(request)
    if app_type == 'station':
        initial['station_id'] = Get('station_id','RENO TAHOE INTL AP, 266779')
        initial['start_year'] = Get('start_year', Get('start_date','POR'))
        initial['end_year'] = Get('end_year', Get('end_date','POR'))
        initial['autofill_list'] = 'US_station_id'
    else:
        initial['location'] = Get('location','-111,40')
        initial['grid'] = Get('grid','1')
        start_year = WRCCData.GRID_CHOICES[initial['grid']][3][0][0]
        end_year = WRCCData.GRID_CHOICES[initial['grid']][3][0][1]
        initial['start_year'] = Get('start_year', Get('start_date',start_year))
        initial['end_year'] = Get('end_year', Get('end_date',end_year))
    if len(initial['start_year'])>4:initial['start_year'] = initial['start_year'][0:4]
    if len(initial['end_year'])>4:initial['end_year'] = initial['end_year'][0:4]
    initial['element'] = Get('element',Get('elements','maxt').replace(' ','').split(',')[0])
    initial['monthly_statistic'] = Get('monthly_statistic', 'mave')
    initial['units'] =  Get('units','english')
    initial['max_missing_days'] = Get('max_missing_days', '5')
    initial['start_month'] = Get('start_month', '01')
    initial['departures_from_averages'] = Get('departures_from_averages', 'F')
    initial['frequency_analysis'] = Get('frequency_analysis', 'F')
    initial['less_greater_or_between']= Get('less_greater_or_between', None)
    initial['threshold_for_less_or_greater']= Get('threshold_for_less_or_greater', None)
    initial['threshold_low_for_between']= Get('threshold_low_for_between', None)
    initial['threshold_high_for_between']= Get('threshold_high_for_between', None)
    initial['generate_graph'] = Get('generate_graph', 'F')
    initial['base_temperature'] = Get('base_temperature','')
    if not initial['base_temperature'] and initial['element'] in ['hdd','cdd']:
        initial['base_temperature'] = '65'
    if not initial['base_temperature'] and initial['element'] in ['gdd']:
        initial['base_temperature'] = '50'
    #FIX ME request.POST.get does not return base_temperature and thresholds
    if type(request) != dict  and request.POST:
        ks = ['base_temperature','less_greater_or_between','threshold_for_less_or_greater','threshold_low_for_between','threshold_high_for_between']
        req_dict = dict(request.POST.items())
        for k in ks:
            if k in req_dict.keys():
                initial[k] = str(req_dict[k])

    #set the check box values
    for el in WRCCData.SXTR_ELEMENT_LIST:
        checkbox_vals[el + '_selected'] =''
        if el == initial['element']:
            checkbox_vals[el + '_selected'] ='selected'
    for start_month in ['01','02','03','04','05','06','07','08','09','10','11','12']:
        for mon_type in ['start_month']:
            checkbox_vals[mon_type + '_' + start_month + '_selected']=''
        if initial[mon_type] == start_month:
            checkbox_vals[mon_type + '_' + start_month + '_selected']='selected'
    for bl in ['T','F']:
        for cbv in ['departures_from_averages', 'frequency_analysis', 'generate_graph']:
            checkbox_vals[cbv + '_' + bl + '_selected'] = ''
            if initial[cbv] == bl:
               checkbox_vals[cbv + '_' + bl + '_selected'] = 'selected'
    for stat in ['mmax','mmin','mave','sd','ndays','rmon','msum']:
        checkbox_vals[stat + '_selected'] =''
        if initial['monthly_statistic'] == stat:
            checkbox_vals[stat + '_selected'] ='selected'
    for u in ['english', 'metric']:
        checkbox_vals['units_' + u + '_selected'] =''
        if u == initial['units']:
            checkbox_vals['units_' +u + '_selected'] ='selected'
    for lgb in ['l', 'g', 'b']:
        checkbox_vals[lgb + '_selected'] =''
        if initial['less_greater_or_between'] == lgb:
            checkbox_vals[lgb + '_selected'] ='selected'
    return initial, checkbox_vals

def set_sodxtrmts_graph_initial(request, init=None):
    initial = {}
    checkbox_vals = {}
    Get = set_GET(request)
    initial['graph_generate_graph']= str(Get('graph_generate_graph', 'F'))
    initial['graph_start_month'] = Get('graph_start_month', '01')
    initial['graph_end_month'] = Get('graph_end_month', '02')
    '''
    if init and 'start_year' in init.keys() and 'end_year' in init.keys():
        initial['graph_start_year'] = init['start_year']
        initial['graph_end_year'] = init['end_year']
    else:
        initial['graph_start_year'] = Get('graph_start_year', Get('start_year', 'POR'))
        initial['graph_end_year'] = Get('graph_end_year', Get('end_year', 'POR'))
    '''
    initial['graph_start_year'] = Get('graph_start_year', Get('start_year', 'POR'))
    initial['graph_end_year'] = Get('graph_end_year', Get('end_year', 'POR'))
    initial['graph_summary'] = Get('graph_summary', 'mean')
    initial['graph_show_running_mean'] = Get('graph_show_running_mean', 'T')
    initial['graph_running_mean_years'] = Get('graph_running_mean_years', '9')
    initial['graph_plot_incomplete_years'] = Get('graph_plot_incomplete_years', 'F')
    #initial['json_file'] = Get('json_file', None)
    #initial['JSON_URL'] = Get('JSON_URL', '/tmp/')
    for graph_month in ['01','02','03','04','05','06','07','08','09','10','11','12']:
        checkbox_vals['graph_start_month' + '_' + graph_month + '_selected']=''
        checkbox_vals['graph_end_month' + '_' + graph_month + '_selected']=''
        if initial['graph_start_month'] == graph_month:
            checkbox_vals['graph_start_month' + '_' + graph_month + '_selected']='selected'
        if initial['graph_end_month'] == graph_month:
            checkbox_vals['graph_end_month' + '_' + graph_month + '_selected']='selected'
    for bl in ['T','F']:
        for cbv in ['graph_show_running_mean', 'graph_plot_incomplete_years', 'graph_generate_graph']:
            checkbox_vals[cbv + '_' + bl + '_selected'] = ''
            if initial[cbv] == bl:
                checkbox_vals[cbv + '_' + bl + '_selected'] = 'selected'
    for graph_summary in ['max','min','mean','sum','individual']:
        checkbox_vals[ 'graph_summary_' + graph_summary + '_selected'] = ''
        if initial['graph_summary'] == graph_summary:
            checkbox_vals['graph_summary_' + graph_summary + '_selected'] = 'selected'
    return initial, checkbox_vals



def set_data_station_initial(request):
    initial = {}
    checkbox_vals = {}
    Get = set_GET(request)
    Getlist = set_GET_list(request)
    initial['s_date'] = fourtnight
    initial['e_date'] = yesterday
    initial['select_stations_by'] = Get('select_stations_by', 'station_id')
    initial[initial['select_stations_by']] = Get(initial['select_stations_by'], WRCCData.AREA_DEFAULTS[initial['select_stations_by']])
    #initial['area_type_label'] = Get('area_type_label', WRCCData.DISPLAY_PARAMS[initial['select_stations_by']])
    initial['area_type_label'] =  WRCCData.DISPLAY_PARAMS[initial['select_stations_by']]
    initial['area_type_value'] = initial[initial['select_stations_by']]
    #initial['area_type_value'] = Get('area_type_value', WRCCData.AREA_DEFAULTS[initial['select_stations_by']])
    initial['overlay_state'] = Get('overlay_state', 'nv')
    initial['autofill_list'] = 'US_' + initial['select_stations_by']
    el_str = Get('elements',None)
    if isinstance(el_str,basestring) and el_str:
        initial['elements']= el_str.replace(' ','').split(',')
    else:
        initial['elements'] = Getlist('elements', ['maxt','mint','pcpn'])
    initial['elements_string'] = ','.join(initial['elements'])
    initial['add_degree_days'] = Get('add_degree_days', 'F')
    initial['units'] = Get('units','english')
    if initial['units'] == 'metric':
        initial['degree_days'] = Get('degree_days', 'gdd13,hdd21')
    else:
        initial['degree_days'] = Get('degree_days', 'gdd55,hdd70')

    '''
    if initial['select_stations_by'] == 'station_id':
        initial['start_date'] = Get('start_date','POR')
        initial['end_date']  = Get('end_date','POR')
    else:
    '''
    initial['start_date']  = Get('start_date', fourtnight)
    initial['end_date']  = Get('end_date', yesterday)
    initial['show_flags'] = Get('show_flags', 'F')
    initial['show_observation_time'] = Get('show_observation_time', 'F')
    initial['data_format'] = Get('data_format', 'html')
    initial['date_format'] = Get('date_format', 'dash')
    initial['delimiter'] = Get('delimiter', 'space')
    initial['output_file_name'] = Get('output_file_name', 'Output')
    initial['user_name'] = Get('user_name', 'Your Name')
    initial['user_email'] = Get('user_email', 'Your Email')
    #set the check box values
    for area_type in WRCCData.SEARCH_AREA_FORM_TO_ACIS.keys():
        checkbox_vals[area_type + '_selected'] =''
        if area_type == initial['select_stations_by']:
            checkbox_vals[area_type + '_selected'] ='selected'
    for e in ['maxt','mint','avgt', 'obst', 'pcpn', 'snow', 'snwd', 'gdd','hdd','cdd', 'evap', 'wdmv']:
        checkbox_vals['elements_' + e + '_selected'] =''
        for el in initial['elements']:
            if el == e:
                checkbox_vals['elements_' + e + '_selected'] ='selected'
    for df in ['clm', 'dlm','xl', 'html']:
        checkbox_vals['data_format_' + df + '_selected'] =''
        if df == initial['data_format']:
            checkbox_vals['data_format_' + df + '_selected'] ='selected'
    for u in ['english', 'metric']:
        checkbox_vals['units_' + u + '_selected'] =''
        if u == initial['units']:
            checkbox_vals['units_' +u + '_selected'] ='selected'
    for df in ['none', 'dash','colon', 'slash']:
        checkbox_vals['date_format_' + df + '_selected'] =''
        if df == initial['date_format']:
            checkbox_vals['date_format_' + df + '_selected'] ='selected'
    for dl in ['comma', 'tab', 'space', 'colon', 'pipe']:
        checkbox_vals[dl + '_selected'] =''
        if dl == initial['delimiter']:
            checkbox_vals[dl + '_selected'] ='selected'
    for bl in ['T','F']:
        for cbv in ['show_flags', 'show_observation_time', 'add_degree_days']:
            checkbox_vals[cbv + '_' + bl + '_selected'] = ''
            if initial[cbv] == bl:
                checkbox_vals[cbv + '_' + bl + '_selected'] = 'selected'
    return initial, checkbox_vals

def set_data_gridded_initial(request):
    initial = {}
    checkbox_vals = {}
    Get = set_GET(request)
    Getlist = set_GET_list(request)
    initial['select_grid_by'] = Get('select_grid_by', 'location')
    initial[str(initial['select_grid_by'])] = Get(str(initial['select_grid_by']), WRCCData.AREA_DEFAULTS[initial['select_grid_by']])
    initial['area_type_label'] = WRCCData.DISPLAY_PARAMS[initial['select_grid_by']]
    initial['area_type_value'] = Get(str(initial['select_grid_by']), WRCCData.AREA_DEFAULTS[initial['select_grid_by']])
    #initial['area_type_value'] = Get('area_type_value', WRCCData.AREA_DEFAULTS[initial['select_grid_by']])
    initial['overlay_state'] = Get('overlay_state', 'nv')
    initial['autofill_list'] = 'US_' + initial['select_grid_by']
    initial['temporal_resolution'] = Get('temporal_resolution', 'dly')
    el_str = Get('elements',None)
    if isinstance(el_str,basestring) and el_str:
        initial['elements']= el_str.replace(' ','').split(',')
    else:
        initial['elements'] = Getlist('elements', ['maxt','mint','pcpn'])
    initial['elements_string'] = ','.join(initial['elements'])
    initial['add_degree_days'] = Get('add_degree_days', 'F')
    initial['units'] = Get('units','english')
    if initial['units'] == 'metric':
        initial['degree_days'] = Get('degree_days', 'gdd13,hdd21')
    else:
        initial['degree_days'] = Get('degree_days', 'gdd55,hdd70')
    initial['start_date']  = Get('start_date', fourtnight)
    initial['end_date']  = Get('end_date', yesterday)
    initial['grid'] = Get('grid', '1')
    initial['data_summary'] = Get('data_summary', 'none')
    initial['temporal_summary'] = Get('temporal_summary', 'mean')
    initial['spatial_summary'] = Get('spatial_summary', 'mean')
    initial['data_format'] = Get('data_format', 'html')
    initial['date_format'] = Get('date_format', 'dash')
    initial['delimiter'] = Get('delimiter', 'space')
    initial['output_file_name'] = Get('output_file_name', 'Output')
    initial['user_name'] = Get('user_name', 'Your Name')
    initial['user_email'] = Get('user_email', 'Your Email')
    #set the check box values
    for area_type in WRCCData.SEARCH_AREA_FORM_TO_ACIS.keys():
        checkbox_vals[area_type + '_selected'] =''
        if area_type == initial['select_grid_by']:
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
    for df in ['clm', 'dlm','xl', 'html']:
        checkbox_vals['data_format_' + df + '_selected'] =''
        if df == initial['data_format']:
            checkbox_vals['data_format_' + df + '_selected'] ='selected'
    for df in ['none', 'dash','colon', 'slash']:
        checkbox_vals['date_format_' + df + '_selected'] =''
        if df == initial['date_format']:
            checkbox_vals['date_format_' +df + '_selected'] ='selected'
    for dl in ['comma', 'tab', 'space', 'colon', 'pipe']:
        checkbox_vals['delimiter_' + dl + '_selected'] =''
        if dl == initial['delimiter']:
            checkbox_vals['delimiter_' + dl + '_selected'] ='selected'
    for u in ['english', 'metric']:
        checkbox_vals['units_' + u + '_selected'] =''
        if u == initial['units']:
            checkbox_vals['units_' +u + '_selected'] ='selected'
    for tr in ['dly','mly','yly']:
        checkbox_vals['temporal_resolution_' + tr + '_selected'] = ''
        if tr == initial['temporal_resolution']:
            checkbox_vals['temporal_resolution_' + tr + '_selected'] = 'selected'
    for ds in ['none','temporal', 'spatial']:
        checkbox_vals['data_summary_' + ds + '_selected'] =''
        if ds == initial['data_summary']:
            checkbox_vals['data_summary_' + ds + '_selected'] ='selected'
    for st in ['max','min','mean','sum']:
        checkbox_vals['temporal_summary_' + st + '_selected'] =''
        checkbox_vals['spatial_summary_' + st + '_selected'] =''
        if st == initial['temporal_summary']:
            checkbox_vals['temporal_summary_' + st + '_selected'] ='selected'
        if st == initial['spatial_summary']:
            checkbox_vals['spatial_summary_' + st + '_selected'] ='selected'
    for g in ['1','21','3','4','5','6','7','8','9','10','11','12','13','14','15','16']:
        checkbox_vals['grid_' + g + '_selected'] =''
        if initial['grid'] == g:
            checkbox_vals['grid_' + g + '_selected'] ='selected'
    return initial, checkbox_vals

def set_spatial_summary_initial(request):
    initial = {}
    checkbox_vals = {}
    Get = set_GET(request)
    Getlist = set_GET_list(request)
    initial['select_grid_by'] = Get('select_grid_by', 'location')
    initial[str(initial['select_grid_by'])] = Get(str(initial['select_grid_by']), WRCCData.AREA_DEFAULTS[initial['select_grid_by']])
    initial['area_type_label'] = WRCCData.DISPLAY_PARAMS[initial['select_grid_by']]
    initial['area_type_value'] = Get(str(initial['select_grid_by']), WRCCData.AREA_DEFAULTS[initial['select_grid_by']])
    #initial['area_type_value'] = Get('area_type_value', WRCCData.AREA_DEFAULTS[initial['select_grid_by']])
    initial['overlay_state'] = Get('overlay_state', 'nv')
    initial['autofill_list'] = 'US_' + initial['select_grid_by']
    el_str = Get('elements',None)
    if isinstance(el_str,basestring) and el_str:
        initial['elements']= el_str.replace(' ','').split(',')
    else:
        initial['elements'] = Getlist('elements', ['maxt','mint','pcpn'])
    initial['elements_string'] = ','.join(initial['elements'])
    initial['add_degree_days'] = Get('add_degree_days', 'F')
    initial['degree_days'] = Get('degree_days', 'gdd55,hdd70')
    initial['units'] = Get('units','english')
    initial['start_date']  = Get('start_date', fourtnight)
    initial['end_date']  = Get('end_date', yesterday)
    initial['grid'] = Get('grid', '1')
    initial['spatial_summary'] = Get('spatial_summary', 'mean')
    initial['show_running_mean'] = Get('show_running_mean', 'T')
    initial['running_mean_days'] = Get('running_mean_days', '9')
    initial['show_plot_opts'] = Get('show_plot_opts','F')
    #set the check box values
    for area_type in WRCCData.SEARCH_AREA_FORM_TO_ACIS.keys():
        checkbox_vals[area_type + '_selected'] =''
        if area_type == initial['select_grid_by']:
            checkbox_vals[area_type + '_selected'] ='selected'
    for e in ['maxt','mint','avgt', 'pcpn','gdd','hdd','cdd']:
        checkbox_vals['elements_' + e + '_selected'] =''
        for el in initial['elements']:
            if el == e:
                checkbox_vals['elements_' + e + '_selected'] ='selected'
    for u in ['english', 'metric']:
        checkbox_vals['units_' + u + '_selected'] =''
        if u == initial['units']:
            checkbox_vals['units_' +u + '_selected'] ='selected'
    for g in ['1','21','3','4','5','6','7','8','9','10','11','12','13','14','15','16']:
        checkbox_vals['grid_' + g + '_selected'] =''
        if initial['grid'] == g:
            checkbox_vals['grid_' + g + '_selected'] ='selected'
    for st in ['max','min','mean','sum']:
        checkbox_vals['spatial_summary_' + st + '_selected'] =''
        if st == initial['spatial_summary']:
            checkbox_vals['spatial_summary_' + st + '_selected'] ='selected'
    for bl in ['T','F']:
        for cbv in ['show_running_mean', 'add_degree_days']:
            checkbox_vals[cbv + '_' + bl + '_selected'] = ''
            if initial[cbv] == bl:
                checkbox_vals[cbv + '_' + bl + '_selected'] = 'selected'
    return initial, checkbox_vals

def set_temporal_summary_initial(request):
    initial = {}
    checkbox_vals = {}
    Get = set_GET(request)
    Getlist = set_GET_list(request)
    initial['select_grid_by'] = Get('select_grid_by', 'state')
    initial[str(initial['select_grid_by'])] = Get(str(initial['select_grid_by']), WRCCData.AREA_DEFAULTS[initial['select_grid_by']])
    initial['area_type_label'] = WRCCData.DISPLAY_PARAMS[initial['select_grid_by']]
    initial['area_type_value'] = Get(str(initial['select_grid_by']), WRCCData.AREA_DEFAULTS[initial['select_grid_by']])
    #initial['area_type_value'] = Get('area_type_value', WRCCData.AREA_DEFAULTS[initial['select_grid_by']])
    initial['overlay_state'] = Get('overlay_state', 'nv')
    initial['autofill_list'] = 'US_' + initial['select_grid_by']
    el_str = Get('elements',None)
    if isinstance(el_str,basestring) and el_str:
        initial['elements']= el_str.replace(' ','').split(',')
    else:
        initial['elements'] = Getlist('elements', ['maxt','mint','pcpn'])
    initial['elements_string'] = ','.join(initial['elements'])
    initial['add_degree_days'] = Get('add_degree_days', 'F')
    initial['degree_days'] = Get('degree_days', 'gdd55,hdd70')
    initial['start_date']  = Get('start_date', week)
    initial['end_date']  = Get('end_date', yesterday)
    initial['grid'] = Get('grid', '1')
    initial['temporal_summary'] = Get('temporal_summary', 'mean')
    initial['show_plot_opts'] = Get('show_plot_opts','T')
    #set the check box values
    for area_type in WRCCData.SEARCH_AREA_FORM_TO_ACIS.keys():
        checkbox_vals[area_type + '_selected'] =''
        if area_type == initial['select_grid_by']:
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
    for g in ['1','21','3','4','5','6','7','8','9','10','11','12','13','14','15','16']:
        checkbox_vals['grid_' + g + '_selected'] =''
        if initial['grid'] == g:
            checkbox_vals['grid_' + g + '_selected'] ='selected'
    for st in ['max','min','mean','sum']:
        checkbox_vals['temporal_summary_' + st + '_selected'] =''
        if st == initial['temporal_summary']:
            checkbox_vals['temporal_summary_' + st + '_selected'] ='selected'
    return initial, checkbox_vals

def set_station_locator_initial(request):
    initial = {}
    checkbox_vals = {}
    Get = set_GET(request)
    Getlist = set_GET_list(request)
    initial['select_stations_by'] = Get('select_stations_by', 'state')
    initial[str(initial['select_stations_by'])] = Get(str(initial['select_stations_by']), WRCCData.AREA_DEFAULTS[initial['select_stations_by']])
    initial['area_type_label'] = WRCCData.DISPLAY_PARAMS[initial['select_stations_by']]
    initial['area_type_value'] = Get(str(initial['select_stations_by']), WRCCData.AREA_DEFAULTS[initial['select_stations_by']])
    #initial['area_type_value'] = Get('area_type_value', WRCCData.AREA_DEFAULTS[initial['select_stations_by']])
    initial['overlay_state'] = Get('overlay_state', 'nv')
    initial['autofill_list'] = 'US_' + initial['select_stations_by']
    el_str = Get('elements',None)
    if isinstance(el_str,basestring) and el_str:
        initial['elements']= el_str.replace(' ','').split(',')
    else:
        initial['elements'] = Getlist('elements', ['maxt','mint','pcpn'])
    initial['elements_string'] = ','.join(initial['elements'])
    initial['units'] = 'english'
    initial['add_degree_days'] = False
    initial['degree_days'] = ''
    initial['date_format'] = 'yyyy-mm-dd'
    initial['data_format'] = 'html'
    initial['show_observation_time'] = 'F'
    initial['show_flags'] = 'F'
    initial['elements_constraints'] = Get('elements_constraints', 'all')
    initial['start_date']  = Get('start_date', '20140101')
    initial['end_date']  = Get('end_date', yesterday)
    initial['dates_constraints']  = Get('dates_constraints', 'all')
    #set the check box values
    for area_type in WRCCData.SEARCH_AREA_FORM_TO_ACIS.keys():
        checkbox_vals[area_type + '_selected'] =''
        if area_type == initial['select_stations_by']:
            checkbox_vals[area_type + '_selected'] ='selected'
    for e in ['maxt','mint','avgt', 'obst', 'pcpn', 'snow', 'snwd', 'gdd','hdd','cdd', 'evap','wdmv']:
        checkbox_vals['elements_' + e + '_selected'] =''
        for el in initial['elements']:
            if el == e:
                checkbox_vals['elements_' + e + '_selected'] ='selected'
    for b in ['any', 'all']:
        checkbox_vals['elements_' + b  + '_selected'] =''
        checkbox_vals['dates_' + b  + '_selected'] =''
        if initial['elements_constraints'] == b:
            checkbox_vals['elements_' + b  + '_selected'] ='selected'
        if initial['dates_constraints'] == b:
            checkbox_vals['dates_' + b  + '_selected'] ='selected'
    return initial, checkbox_vals

def set_monthly_aves_initial(request):
    initial = {}
    checkbox_vals = {}
    Get = set_GET(request)
    Getlist = set_GET_list(request)
    initial['station_id'] = Get('station_id', 'RENO TAHOE INTL AP, 266779')
    initial['autofill_list'] = 'US_' + 'station_id'
    el_str = Get('elements',None)
    if isinstance(el_str,basestring) and el_str:
        initial['elements']= el_str.replace(' ','').split(',')
    else:
        initial['elements'] = Getlist('elements', ['maxt','mint','pcpn'])
    initial['add_degree_days'] = Get('add_degree_days', 'F')
    initial['units'] = Get('units','english')
    if initial['units'] == 'metric':
        initial['degree_days'] = Get('degree_days', 'gdd13,hdd21')
    else:
        initial['degree_days'] = Get('degree_days', 'gdd55,hdd70')
    initial['start_date']  = Get('start_date', 'POR')
    initial['end_date']  = Get('end_date', 'POR')
    #Checkbox vals
    for e in ['maxt','mint','avgt', 'obst', 'pcpn', 'snow', 'snwd', 'gdd','hdd','cdd', 'evap', 'wdmv']:
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
    return initial, checkbox_vals

def set_combined_analysis_initial(request,app_name):
    initial = {}
    checkbox_vals = {}
    Get = set_GET(request)
    Getlist = set_GET_list(request)
    initial['location'] = Get('location','-119,40')
    initial['grid'] = Get('grid','1')
    initial['start_date'] = Get('start_date', fourtnight)
    initial['end_date'] = Get('end_date', yesterday)
    initial['elements'] =  Getlist('elements',None)
    #initial['elements_string'] = ','.join(initial['elements'])
    #Set threshold flags
    for el in initial['elements']:
        initial[el + '_show_threshold'] = True

    initial['units'] = Get('units','english')

    if app_name == 'data_comparison':
        initial['add_degree_days'] = Get('add_degree_days', 'F')
        if initial['units'] == 'metric':
            initial['degree_days'] = Get('degree_days', 'gdd13,hdd21')
        else:
            initial['degree_days'] = Get('degree_days', 'gdd55,hdd70')

    if app_name == 'likelihood':
        initial['start_year'] = Get('start_year', '1980')
        initial['end_year'] = Get('end_year', '2010')
        for el in ['maxt','mint','avgt','pcpn','snow','snwd','hdd','cdd','gdd']:
            key = el + '_threshold_low'
            initial[key] = Get(key, WRCCData.ELEMENT_THRESHOLDS[initial['units']][el][0])
            key = el + '_threshold_high'
            initial[key] = Get(key, WRCCData.ELEMENT_THRESHOLDS[initial['units']][el][1])
    #Checkbox vals
    for e in ['maxt','mint','avgt','pcpn', 'snow', 'snwd', 'gdd','hdd','cdd']:
        checkbox_vals['elements_' + e + '_selected'] =''
        for el in initial['elements']:
            if str(el) == e:
                checkbox_vals['elements_' + e + '_selected'] ='selected'
    for g in ['1','21','3','4','5','6','7','8','9','10','11','12','13','14','15','16']:
        checkbox_vals['grid_' + g + '_selected'] =''
        if initial['grid'] == g:
            checkbox_vals['grid_' + g + '_selected'] ='selected'
    if app_name == 'data_comparison':
        for bl in ['T','F']:
            for cbv in ['add_degree_days']:
                checkbox_vals[cbv + '_' + bl + '_selected'] = ''
                if initial[cbv] == bl:
                    checkbox_vals[cbv + '_' + bl + '_selected'] = 'selected'
    for u in ['english', 'metric']:
        checkbox_vals['units_' + u + '_selected'] =''
        if u == initial['units']:
            checkbox_vals['units_' +u + '_selected'] ='selected'
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

def convert_elements_to_list(elements):
    el_list = []
    if isinstance(elements, basestring):
        el_list = elements.replace(' ','').rstrip(',').split(',')
    elif isinstance(elements,list):
        el_list = [str(el) for el in elements]
    return el_list

def convert_elements_to_string(elements):
    el_str = ''
    if isinstance(elements, basestring):
        el_str = elements
    elif isinstance(elements,list):
        el_str = ','.join([str(el).rstrip(' ') for el in elements])
    return el_str

def set_form(request, clean=True):
    '''
    Coverts request input to usable form input:
    Deals with unicode issues
    and autofill options for identifiers
    NOTE: elements should always be a list (also wen clean = False)
    If Clean == True,
    We also clean up some form fields for submission:
        date fields, convert to yyyymmdd
        name strings are converted to ids
    '''
    form = {}
    #Convert request object to python dictionary
    if isinstance(request,dict):
        form_dict = dict(request)
    elif request.method == 'POST':
        form_dict = dict((x,y) for x,y in request.POST.items())
    elif request.method == 'GET':
        form_dict = dict((x,y) for x,y in request.GET.items())
    else:
        try:
            form_dict = dict((x,y) for x,y in request.items())
        except:
            form_dict = {}
    #Convert unicode to strings and elements to list
    for key,val in form_dict.iteritems():
        if key == 'csrfmiddlewaretoken':
            continue
        form[str(key)] =str(val)
        if str(key) == 'elements':
            #Convert elements to list
            form['elements'] = convert_elements_to_list(form['elements'])
    if  not clean:
        return form
    #Clean up form for submission
    #Clean Dates
    for key in ['start_date', 'end_date']:
        if key in form.keys():
            form[key] = form[key].replace('-','').replace(':','').replace('/','').replace(' ','')
    #Convert user input of area names to ids
    for key in ['station_id','county', 'basin', 'county_warning_area', 'climate_division']:
        if not key in form.keys():
            continue
        form[key] = find_id(form[key],settings.MEDIA_DIR +'json/US_' + key + '.json')
    #station_ids is special case
    if 'station_ids' in form.keys():
        stn_ids = ''
        stn_list = form['station_ids'].rstrip(',').split(',')
        #Remove leading spaces from list items
        stn_list = [v.lstrip(' ').rstrip(' ') for v in stn_list]
        #Make sure that no station is entered twice
        id_previous = ''
        for idx, stn_name in enumerate(stn_list):
            stn_id = str(find_id(str(stn_name),settings.MEDIA_DIR +'json/US_' + 'station_id' + '.json'))
            if stn_id == id_previous:
                continue
            id_previous = stn_id
            stn_ids+=stn_id + ','
        #Strip last comma
        stn_ids = stn_ids.rstrip(',')
        form['station_ids'] = stn_ids
    return form

def set_element_list(data_type):
    if data_type in ['station']:
        el_list = ['maxt','mint','avgt', 'obst', 'pcpn', 'snow', 'snwd', 'gdd','hdd','cdd', 'evap', 'wdmv']
    elif data_type in ['grid']:
        ['maxt','mint','avgt','pcpn','gdd','hdd','cdd']
    else:
        el_list = ['maxt','mint','pcpn']
    return el_list

#Initializers
def set_initial_lister(request, req_type):
    '''
    req_type == single or muti
    '''
    initial = {}
    checkbox_vals = {}
    Get = set_GET(request)
    Getlist = set_GET_list(request)
    if req_type == 'single':
        initial['area_type'] = Get('area_type', 'station_id')
    else:
        initial['area_type'] = Get('area_type', 'state')
    #Set up map parameters
    initial['host'] = settings.HOST
    initial['overlay_state'] = Get('overlay_state','NV')
    initial['kml_file_path'] = create_kml_file(initial['area_type'], initial['overlay_state'])
    initial['kml_file_name'] = initial['overlay_state'] + '_' + initial['area_type'] + '.kml'
    #Set form params
    initial['data_type'] = Get('data_type','station')
    initial[str(initial['area_type'])] = Get(str(initial['area_type']), WRCCData.AREA_DEFAULTS[initial['area_type']])
    initial['autofill_list'] = 'US_' + initial['area_type']
    initial['area_type_label'] = WRCCData.DISPLAY_PARAMS[initial['area_type']]
    initial['area_type_value'] = initial[str(initial['area_type'])]
    initial['elements'] =  Getlist('elements', ['maxt','mint','pcpn'])
    initial['add_degree_days'] = Get('add_degree_days', 'F')
    initial['units'] = Get('units','english')
    if initial['units'] == 'metric':
        initial['degree_days'] = Get('degree_days', 'gdd13,hdd21')
    else:
        initial['degree_days'] = Get('degree_days', 'gdd55,hdd70')
    initial['start_date']  = Get('start_date', fourtnight)
    initial['end_date']  = Get('end_date', yesterday)
    initial['show_flags'] = Get('show_flags', 'F')
    initial['show_observation_time'] = Get('show_observation_time', 'F')
    initial['data_format'] = Get('data_format', 'html')
    initial['date_format'] = Get('date_format', 'dash')
    initial['delimiter'] = Get('delimiter', 'space')
    initial['output_file_name'] = Get('output_file_name', 'Output')
    initial['user_name'] = Get('user_name', 'Your Name')
    initial['user_email'] = Get('user_email', 'Your Email')
    #Checkbox vals
    #Data Type
    for dt in ['station','grid','none']:
        checkbox_vals['data_type_' + dt + '_selected'] =''
        if dt == initial['data_type']:
            checkbox_vals['data_type_' + dt + '_selected'] ='selected'
    #Area
    for area_type in WRCCData.SEARCH_AREA_FORM_TO_ACIS.keys() + ['none']:
        checkbox_vals[area_type + '_selected'] =''
        if area_type == initial['area_type']:
            checkbox_vals[area_type + '_selected'] ='selected'
    #Elements
    el_list = set_element_list(initial['data_type'])
    for element in el_list:
        checkbox_vals['elements_' + element + '_selected'] =''
        for el in initial['elements']:
            if str(el) == element:
                checkbox_vals['elements_' + element + '_selected'] ='selected'
    for df in ['clm', 'dlm','xl', 'html']:
        checkbox_vals['data_format_' + df + '_selected'] =''
        if df == initial['data_format']:
            checkbox_vals['data_format_' + df + '_selected'] ='selected'
    for u in ['english', 'metric']:
        checkbox_vals['units_' + u + '_selected'] =''
        if u == initial['units']:
            checkbox_vals['units_' +u + '_selected'] ='selected'
    for df in ['none', 'dash','colon', 'slash']:
        checkbox_vals['date_format_' + df + '_selected'] =''
        if df == initial['date_format']:
            checkbox_vals['date_format_' + df + '_selected'] ='selected'
    for dl in ['comma', 'tab', 'space', 'colon', 'pipe']:
        checkbox_vals[dl + '_selected'] =''
        if dl == initial['delimiter']:
            checkbox_vals[dl + '_selected'] ='selected'
    for bl in ['T','F']:
        for cbv in ['show_flags', 'show_observation_time', 'add_degree_days']:
            checkbox_vals[cbv + '_' + bl + '_selected'] = ''
            if initial[cbv] == bl:
                checkbox_vals[cbv + '_' + bl + '_selected'] = 'selected'
    return initial,checkbox_vals

