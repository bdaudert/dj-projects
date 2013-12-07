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

#Python imports
import datetime
from collections import defaultdict
import json

import sys, os, stat, re

#My modules
import WRCCUtils, AcisWS, WRCCDataApps, WRCCClasses, WRCCData, WRCCFormCheck
import my_data.forms as forms

STATIC_URL = '/www/apps/csc/dj-projects/my_acis/static/'
MEDIA_URL = '/www/apps/csc/dj-projects/my_acis/media/'
STATIC_KML = '/csc/media/kml/'
WEB_SERVER_DIR = '/csc/media/tmp/'
TEMP_FILE_DIR = '/tmp/'

#Set dates
today = WRCCUtils.set_back_date(0)
begin_10yr = WRCCUtils.set_back_date(3660)
yesterday = WRCCUtils.set_back_date(1)
fourtnight = WRCCUtils.set_back_date(14)

def test(request):
    context = {
        'title': 'Southwest Climate Knowledge Exchange',
    }
    return render_to_response('my_data/index.html', context, context_instance=RequestContext(request))

def home(request):
    context = {
        'title': 'Southwest Climate Knowledge Exchange',
    }
    return render_to_response('my_data/home.html', context, context_instance=RequestContext(request))

def help(request):
    context = {
        'title': 'Help Tool',
        'icon':'Magnify.png'
    }
    return render_to_response('my_data/help/home.html', context, context_instance=RequestContext(request))

def main_map(request):
    context = {
        'title': 'Resources',
        'state_choices': ['AZ', 'CA', 'CO', 'NM', 'NV', 'UT'],
        'icon':'Network.png'
    }
    context['json_file'] = 'Network.json'
    return render_to_response('my_data/main_map.html', context, context_instance=RequestContext(request))

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
    return render_to_response('my_data/main_maves.html', context, context_instance=RequestContext(request))

def about_us(request):
    context = {
        'title': 'About Us',
        'icon':'AboutUs.png'
    }
    return render_to_response('my_data/about_us.html', context, context_instance=RequestContext(request))

def who_we_are(request):
    context = {
        'title': 'Who we are',
        'icon':'AboutUs.png'
    }
    return render_to_response('my_data/who_we_are.html', context, context_instance=RequestContext(request))

def what_we_do(request):
    context = {
        'title': 'What we do',
        'icon':'AboutUs.png'
    }
    return render_to_response('my_data/what_we_do.html', context, context_instance=RequestContext(request))

def contact_us(request):
    context = {
        'title': 'Contact Us',
        'icon':'AboutUs.png'
    }
    return render_to_response('my_data/contact_us.html', context, context_instance=RequestContext(request))

def dashboard(request):
    context = {
        'title': 'Monitoring: Climate Dashboard',
        'icon':'Monitoring.png'
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
        context['month_nadm'] == '12'
    else:
        context['month_nadm'] = str(int(month.lstrip('0')) - 1)
    context['year'] = year
    context['year_short'] = '%s%s' % (year[-2], year[-1])

    return render_to_response('my_data/dashboard.html', context, context_instance=RequestContext(request))

def data_home(request):
    context = {
        'title': 'Data',
        'icon':'DataPortal.png'
    }
    return render_to_response('my_data/data/home.html', context, context_instance=RequestContext(request))

def sw_networks(request):
    context = {
        'title': 'Southwest Networks',
        'icon':'DataPortal.png'
    }
    return render_to_response('my_data/data/sw_networks.html', context, context_instance=RequestContext(request))

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
            context['errors'] = 'Thank you for your input!'
        else:
            context['errors'] = errors
    return render_to_response('my_data/feedback.html', context, context_instance=RequestContext(request))

def download(request):
    context = {
        'title': 'Download',
        'icon':'ToolProduct.png'
    }
    app_name = request.GET.get('app_name', None)
    json_file_name = request.GET.get('json_file', None)
    json_file = TEMP_FILE_DIR + json_file_name
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
                with open(json_file, 'r') as json_f:
                    json_data = WRCCUtils.u_convert(json.loads(json_f.read()))
                #find the correct data set corresponding to the tab name
                for idx, data_dict in enumerate(json_data):
                    if data_dict['table_name'] == tab:
                        #context['data_dict'] = data_dict
                        #Overwrite json_in_file
                        json_in_file_name = json_file_name + '_in'
                        with open(TEMP_FILE_DIR + json_in_file_name, 'w+') as json_f:
                            json.dump(data_dict,json_f)
                        break
            DDJ = WRCCClasses.DownloadDataJob(app_name,data_format,delimiter, output_file_name, request=request, json_in_file=TEMP_FILE_DIR + json_in_file_name)
            if data_format in ['clm', 'dlm','xl']:
                return DDJ.write_to_file()
            else:
                response = DDJ.write_to_file()
                context['response'] = response
    return render_to_response('my_data/download.html', context, context_instance=RequestContext(request))

def data_station(request):
    context = {
        'title': 'Historic Station Data',
    }
    #status = WRCCUtils.generate_kml_file('county_warning_area', 'nv' , 'nv_county_warning_area.kml', TEMP_FILE_DIR)
    initial, checkbox_vals = set_station_data_initial(request)
    context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
    #Set up maps if needed
    context['host'] = 'wrcc.dri.edu'
    context['area_type'] = initial['select_stations_by']
    context[initial['select_stations_by']] = WRCCData.AREA_DEFAULTS[initial['select_stations_by']]
    kml_file = initial['overlay_state'] + '_' + initial['select_stations_by'] + '.kml'
    context[initial['overlay_state'] + '_selected'] = 'selected'
    context['kml_file_path'] = WEB_SERVER_DIR +  kml_file
    #Check if kml file exists, if not generate it
    try:
        with open(TEMP_FILE_DIR + kml_file):
            if os.stat(TEMP_FILE_DIR + kml_file).st_size==0:
                status = WRCCUtils.generate_kml_file(initial['select_stations_by'], initial['overlay_state'] , kml_file, TEMP_FILE_DIR)
    except IOError:
        status = WRCCUtils.generate_kml_file(initial['select_stations_by'], initial['overlay_state'] , kml_file, TEMP_FILE_DIR)

    context[initial['select_stations_by']] = WRCCData.AREA_DEFAULTS[initial['select_stations_by']]

    if 'formData' in request.POST:
        #Turn request object into python dict
        form = set_form(request)
        fields_to_check = ['start_date', 'end_date','elements']
        form_error = check_form(form, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            return render_to_response('my_data/data/station/home.html', context, context_instance=RequestContext(request))
        if form['select_stations_by'] in ['basin', 'county_warning_area', 'climate_division', 'county']:
            context['host'] = 'wrcc.dri.edu'
            kml_file_name = form['overlay_state'] + '_' + form['select_stations_by'] + '.kml'
            context['kml_file_path'] = WEB_SERVER_DIR + kml_file_name
            context['area_type'] = form['select_stations_by']

        initial,checkbox_vals = set_station_data_initial(form)
        context['initial'] = initial;context['checkbox_vals']  = checkbox_vals
        display_params_list, params_dict = set_station_data_params(form)
        context['display_params_list'] = display_params_list;context['params_dict'] = params_dict
        #Check if data request is large,
        #if so, gather params and ask user for name and e-mail and notify user that request will be processed offline
        if form['start_date'].lower() == 'por':
            s_date = datetime.date(1900,01,01)
        else:
            s_date = datetime.date(int(form['start_date'][0:4]), int(form['start_date'][4:6]),int(form['start_date'][6:8]))
        if form['end_date'].lower() == 'por':
                e_date = datetime.date.today()
        else:
            e_date = datetime.date(int(form['end_date'][0:4]), int(form['end_date'][4:6]),int(form['end_date'][6:8]))
        days = (e_date - s_date).days
        #if time range > 1 year or user requests data for more than 1 station, large request via ftp
        if days > 366 and 'station_id' not in form.keys():
            context['large_request'] = \
            'At the moment we do not support data requests that exceed 1 year for multiple station.\
             Please limit your request to one station at a time or a date range of one year or less.\
             We will support larger requests in the near future. Thank you for your patience!'
            return render_to_response('my_data/data/station/home.html', context, context_instance=RequestContext(request))

        #Data request
        resultsdict = AcisWS.get_station_data(form, 'sodlist_web')
        context['results'] = resultsdict
        # If request successful, get params for link to apps page
        context['stn_idx'] = [i for i in range(len(resultsdict['stn_ids']))] #for html looping
        if form['data_format'] != 'html':
            return WRCCUtils.write_point_data_to_file(resultsdict['stn_data'], resultsdict['dates'], resultsdict['stn_names'], resultsdict['stn_ids'], resultsdict['elements'],params_dict['delimiter'], WRCCData.FILE_EXTENSIONS[str(form['data_format'])], request=request, output_file_name=str(form['output_file_name']), show_flags=params_dict['show_flags'], show_observation_time=params_dict['show_observation_time'])

    #overlay map generation
    if 'formOverlay' in request.POST:
        context['need_overlay_map'] = True
        form = set_form(request)
        initial, checkbox_vals = set_station_data_initial(request)
        #Override initial where needed
        initial['select_stations_by'] = form['select_overlay_by']
        checkbox_vals[form['select_overlay_by'] + '_selected'] = 'selected'
        initial['area_type_value'] = WRCCData.AREA_DEFAULTS[form['select_overlay_by']]
        initial[form['select_overlay_by']] = WRCCData.AREA_DEFAULTS[form['select_overlay_by']]
        initial['area_type_label'] = WRCCData.DISPLAY_PARAMS[form['select_overlay_by']]
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
        at = form['select_overlay_by']
        st = form['overlay_state']
        context[st + '_selected'] = 'selected'
        kml_file_name = st + '_' + at + '.kml'
        dir_location = TEMP_FILE_DIR
        status = WRCCUtils.generate_kml_file(at, st, kml_file_name, dir_location)
        if not status == 'Success':
            context['overlay_error'] = status
        else:
            context['host'] = 'wrcc.dri.edu'
            context['kml_file_path'] = WEB_SERVER_DIR + kml_file_name
            context['area_type'] = form['select_overlay_by']
    return render_to_response('my_data/data/station/home.html', context, context_instance=RequestContext(request))


def data_gridded(request):
    context = {
        'title': 'Gridded/Modeled Data',
    }
    initial, checkbox_vals = set_gridded_data_initial(request)
    context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
    #Set up maps if needed
    context['host'] = 'wrcc.dri.edu'
    context['area_type'] = initial['select_grid_by']
    context[initial['select_grid_by']] = WRCCData.AREA_DEFAULTS[initial['select_grid_by']]
    kml_file = initial['overlay_state'] + '_' + initial['select_grid_by'] + '.kml'
    context[initial['overlay_state'] + '_selected'] = 'selected'
    context['kml_file_path'] = WEB_SERVER_DIR +  kml_file
    #Check if kml file exists, if not generate it
    try:
        with open(TEMP_FILE_DIR + kml_file):
            if os.stat(TEMP_FILE_DIR + kml_file).st_size==0:
                status = WRCCUtils.generate_kml_file(initial['select_grid_by'], initial['overlay_state'] , kml_file, TEMP_FILE_DIR)
    except IOError:
        status = WRCCUtils.generate_kml_file(initial['select_grid_by'], initial['overlay_state'] , kml_file, TEMP_FILE_DIR)

    context[initial['select_grid_by']] = WRCCData.AREA_DEFAULTS[initial['select_grid_by']]

    if 'formData' in request.POST:
        #Turn request object into python dict
        form = set_form(request)
        fields_to_check = ['start_date', 'end_date','elements']
        form_error = check_form(form, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            return render_to_response('my_data/data/gridded/home.html', context, context_instance=RequestContext(request))
        if form['select_grid_by'] in ['basin', 'county_warning_area', 'climate_division', 'county']:
            context['host'] = 'wrcc.dri.edu'
            kml_file_name = form['overlay_state'] + '_' + form['select_grid_by'] + '.kml'
            context['kml_file_path'] = WEB_SERVER_DIR + kml_file_name
            context['area_type'] = form['select_grid_by']

        initial,checkbox_vals = set_gridded_data_initial(form)
        context['initial'] = initial;context['checkbox_vals']  = checkbox_vals
        display_params_list, params_dict = set_gridded_data_params(form)
        context['display_params_list'] = display_params_list;context['params_dict'] = params_dict
        #Check if data request is large,
        #if so, gather params and ask user for name and e-mail and notify user that request will be processed offline
        if form['start_date'].lower() == 'por':
            s_date = datetime.date(1900,01,01)
        else:
            s_date = datetime.date(int(form['start_date'][0:4]), int(form['start_date'][4:6]),int(form['start_date'][6:8]))
        if form['end_date'].lower() == 'por':
                e_date = datetime.date.today()
        else:
            e_date = datetime.date(int(form['end_date'][0:4]), int(form['end_date'][4:6]),int(form['end_date'][6:8]))
        days = (e_date - s_date).days
        #if time range > 1 month or user requests data for more than 1 grid point, large request via ftp
        if days > 31 and 'location' not in form.keys():
            context['large_request'] = \
            'At the moment we do not support data requests that exceed 1 month.\
             Please limit your request to one grid point at a time or a date range of one month or less.\
             We will support larger requests in the near future. Thank you for your patience!'
            return render_to_response('my_data/data/gridded/home.html', context, context_instance=RequestContext(request))

        #Data request
        if str(form['grid']) == '21':
            #PRISM data need to convert elements!!
            prism_elements = []
            for el in form['elements'].replace(' ','').split(','):
                prism_elements.append('%s_%s' %(str(form['temporal_resolution']), str(el)))
            form['elements'] = prism_elements
        req = AcisWS.get_grid_data(form, 'griddata_web')
        context['req'] = req
        if 'error' in req.keys():
            context['error'] = req['error']
            context['results'] = []
            return render_to_response('my_data/data/gridded/home.html', context, context_instance=RequestContext(request))
        #format data
        results = WRCCUtils.format_grid_data(req, form)
        context['results'] = results
        #If Spatial Summary, write json file forarea_time_series graph
        if form['data_summary'] == 'spatial':
            graph_data = [[[dat[0]] for dat in results]for el in form['elements'].replace(' ','').split(',')]
            for date_idx,date_data in enumerate(results):
                for el_idx,el_data in enumerate(date_data[1:]):
                    graph_data[el_idx][date_idx].append(el_data)
            json_dict = {
            'search_params':params_dict,
            'display_params_list':display_params_list,
            'download_data':results,
            'graph_data':graph_data
            }
            results_json = json.dumps(json_dict)
            time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            json_file = '%s_area_time_series.json' %(time_stamp)
            f = open(TEMP_FILE_DIR + '%s' %(json_file),'w+')
            f.write(results_json)
            f.close()
            context['JSON_URL'] = WEB_SERVER_DIR
            context['json_file'] = json_file
        #Render to page if html format was chosen, else save to file
        if form['data_format'] == 'html':
            return render_to_response('my_data/data/gridded/home.html', context, context_instance=RequestContext(request))
        else:
            return WRCCUtils.write_griddata_to_file(results,form,request=request)
            #return WRCCUtils.write_griddata_to_file(results, form['elements'].replace(' ','').split(','),params_dict['delimiter'],WRCCData.FILE_EXTENSIONS[form['data_format']], request=request,output_file_name =form['output_file_name'])


    if 'formOverlay' in request.POST:
        context['need_overlay_map'] = True
        form = set_form(request)
        initial, checkbox_vals = set_gridded_data_initial(request)
        #Override initial where needed
        initial['select_grid_by'] = form['select_overlay_by']
        checkbox_vals[form['select_overlay_by'] + '_selected'] = 'selected'
        initial['area_type_value'] = WRCCData.AREA_DEFAULTS[form['select_overlay_by']]
        initial[form['select_overlay_by']] = WRCCData.AREA_DEFAULTS[form['select_overlay_by']]
        initial['area_type_label'] = WRCCData.DISPLAY_PARAMS[form['select_overlay_by']]
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
        at = form['select_overlay_by']
        st = form['overlay_state']
        context[st + '_selected'] = 'selected'
        kml_file_name = st + '_' + at + '.kml'
        dir_location = TEMP_FILE_DIR
        status = WRCCUtils.generate_kml_file(at, st, kml_file_name, dir_location)
        if not status == 'Success':
            context['overlay_error'] = status
        else:
            context['host'] = 'wrcc.dri.edu'
            context['kml_file_path'] = WEB_SERVER_DIR + kml_file_name
            context['area_type'] = form['select_overlay_by']

    return render_to_response('my_data/data/gridded/home.html', context, context_instance=RequestContext(request))



def apps_home(request):
    context = {
        'title': 'Tools/Applications',
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
    return render_to_response('my_data/apps/home.html', context, context_instance=RequestContext(request))

def apps_station(request):
    context = {
        'title': 'Station Data Tools',
        'state_choices': ['AZ', 'CA', 'CO', 'NM', 'NV', 'UT'],
        'icon':'ToolProduct.png'
        }
    stn_id = request.GET.get('stn_id', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    elements = request.GET.get('elements', None)
    initial = {}
    if stn_id is not None:context['stn_id'] = stn_id;initial['stn_id'] = stn_id
    if start_date is not None:context['start_date'] = start_date;initial['start_date'] = start_date
    if end_date is not None:context['end_date'] = end_date;initial['end_date'] = end_date
    if elements is not None:context['elements'] = elements;initial['elements'] = elements
    context['initial'] = initial
    return render_to_response('my_data/apps/station/home.html', context, context_instance=RequestContext(request))

def apps_gridded(request):
    context = {
        'title': 'Gridded Data Tools',
        'icon':'ToolProduct.png'
        }
    return render_to_response('my_data/apps/gridded/home.html', context, context_instance=RequestContext(request))

def apps_gis(request):
    context = {
        'title': 'Geospatial Data Tools',
        'icon':'ToolProduct.png'
        }
    return render_to_response('my_data/apps/gis/home.html', context, context_instance=RequestContext(request))

def metagraph(request):
    context = {
        'title': 'Station Metadata Graphics',
        'icon':'ToolProduct.png'
    }
    stn_id = request.GET.get('stn_id', None)
    if stn_id is None:
        form_meta = set_as_form(request,'MetaGraphForm')
    else:
        form_meta = set_as_form(request,'MetaGraphForm', init={'stn_id':str(stn_id)})
        context['stn_id'] = stn_id
    context['form_meta'] = form_meta

    if 'form_meta' in request.POST:
        form_meta = set_as_form(request,'MetaGraphForm')
        context['form_meta']  = form_meta
        if form_meta.is_valid():
            context['station_id'] = form_meta.cleaned_data['station_id']
            params = {'sids':find_stn_id(form_meta.cleaned_data['station_id'])}
            meta_request = AcisWS.StnMeta(params)
            #meta_request = WRCCClasses.DataJob('StnMeta', params).make_data_call()
            key_order = ['name','state','ll','elev','uid','sids']
            #station_meta = [[WRCCData.DISPLAY_PARAMS[key]] for key in key_order]
            if 'meta' in meta_request.keys():
                if len(meta_request['meta']) == 0:
                    #station_meta['error'] = 'No metadata found for station: %s.' %stn_id
                    station_meta = {'error': 'No metadata found for station: %s.' %stn_id}
                else:
                    station_meta = WRCCUtils.metadict_to_display(meta_request['meta'][0], key_order)
            else:
                if 'error' in meta_request.keys():
                    station_meta = {'error': meta_request['error']}
                else:
                    station_meta = {'error':'No meta data found for station: %s.' %stn_id}

            context['station_meta'] = station_meta
            #Call perl script that generates gif graphs
            #FIX ME! Should be able to call it from html:
            #<img alt="MetaGraph" title="MetaGraph" src="{{MEDIA_URL}}perl-scripts/csc_cliMETAgraph.pl?{{station_id}}">
            time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_')
            context['time_stamp'] = time_stamp
            perl_out, perl_err = run_external_script("perl %sperl-scripts/csc_cliMETAgraph.pl %s %s" %(MEDIA_URL, find_stn_id(form_meta.cleaned_data['station_id']), time_stamp))
            context['perl_err'] = perl_err
            context['perl_out'] = perl_out
        else:
            stn_id = None

    return render_to_response('my_data/apps/station/metagraph.html', context, context_instance=RequestContext(request))

def monthly_aves(request):
    context = {
        'title': 'Monthly Averages',
        'icon':'ToolProduct.png',
        'acis_elements':dict(WRCCData.ACIS_ELEMENTS_DICT)
    }
    stn_id = request.GET.get('stn_id', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    elements = request.GET.get('elements', None)
    initial = {}
    search_params = {}
    if stn_id is not None:initial['stn_id']= str(stn_id);search_params['stn_id'] = stn_id
    if start_date is not None:initial['start_date']= str(start_date);search_params['start_date'] = start_date
    if end_date is not None:initial['end_date']= str(end_date);search_params['end_date'] = end_date
    if elements is not None:initial['elements']= elements;search_params['elements'] = elements
    context['search_params'] = search_params
    if initial:
        form = set_as_form(request,'MonthlyAveragesForm', init=initial)
    else:
        form = set_as_form(request,'MonthlyAveragesForm')
    context['form'] = form

    if 'form' in request.POST:
        form = set_as_form(request,'MonthlyAveragesForm')
        context['form']  = form
        if form.is_valid():
            s_date = str(form.cleaned_data['start_date'])
            e_date = str(form.cleaned_data['end_date'])
            stn_id = find_stn_id(form.cleaned_data['station_id'])
            context['search_params'] ={
                'stn_id':stn_id,
                'start_date':s_date,
                'end_date':e_date,
                'elems': ','.join(form.cleaned_data['elements'])
            }
            params = dict(sid=stn_id, sdate=s_date, edate=e_date, \
            meta='valid_daterange,name,state,sids,ll,elev,uid,county,climdiv', \
            elems=[dict(vX=WRCCData.ACIS_ELEMENTS_DICT[el]['vX'], groupby="year")for el in form.cleaned_data['elements']])
            #Data request
            #req = WRCCClasses.DataJob('StnData', params).make_data_call()
            req = AcisWS.StnData(params)
            #Sanity check
            if not req:
                context['error']= 'No data found for parameters. Please check your station ID.'
                return render_to_response('my_data/apps/station/monthly_aves.html', context, context_instance=RequestContext(request))
            if 'error' in req.keys():
                if req['error'] == 'Unknown sId':
                    context['error'] = '%s is not a valid station identifyier.' %form.cleaned_data['station_id']
                else:
                    context['error']= req['error']
                return render_to_response('my_data/apps/station/monthly_aves.html', context, context_instance=RequestContext(request))
            if 'data' not in req.keys() or 'meta' not in req.keys():
                context['error']= 'No data found for parameters.Please check your station ID, start and end dates.'
                return render_to_response('my_data/apps/station/monthly_aves.html', context, context_instance=RequestContext(request))
            if 'meta' not in req.keys():
                context['error']= 'No metadata found for parameters.Please check your station ID.'
                return render_to_response('my_data/apps/station/monthly_aves.html', context, context_instance=RequestContext(request))
            #Find averages and write results dict
            monthly_aves = {}
            for el in form.cleaned_data['elements']:
                monthly_aves[el] = []
            results = [{} for k in form.cleaned_data['elements']]
            try:
                monthly_aves = WRCCDataApps.monthly_aves(req, form.cleaned_data['elements'])
            except:
                pass
            context['averaged_data'] = monthly_aves
            #Write results dict
            try:
                results = write_monthly_aves_results(req, form.cleaned_data, monthly_aves)
            except:
                context['error'] = 'No data found for parameters.Please check your station ID, start and end dates.'
            context['results'] = results
            context['req'] = results
            '''
            if 'meta' in req.keys():
                meta = write_monthly_aves_meta(req, form.cleaned_data)
                context['meta'] = meta
            '''
            #save to json file (necessary since we can't pass list, dicts to js via hidden vars)
            #double quotes needed for jquery json.load
            results_json = json.dumps(results)
            #results_json = str(results).replace("\'", "\"")
            time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            json_file = '%s_monthly_aves_%s_%s_%s.json' \
            %(time_stamp, str(form.cleaned_data['station_id']), s_date, e_date)
            context['json_file'] = json_file
            with  open(TEMP_FILE_DIR + '%s' %(json_file),'w+') as f:
                f.write(results_json)
    return render_to_response('my_data/apps/station/monthly_aves.html', context, context_instance=RequestContext(request))

def clim_sum_maps(request):
    context = {
        'title': 'Climate Summary Maps',
        'icon':'ToolProduct.png'
    }
    lat = request.GET.get('lat', None)
    lon = request.GET.get('lon', None)
    element = request.GET.get('element', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    grid= request.GET.get('grid', None)
    state = request.GET.get('state', None)
    bounding_box = request.GET.get('bounding_box', None)
    initial = {}
    if element is not None:initial['element'] = str(element)
    if start_date is not None:initial['start_date'] = str(start_date)
    if end_date is not None:initial['end_date'] = str(end_date)
    if lat is not None and lon is not None:
        initial['lat']=str(lat);initial['lon']=str(lon)
        context['lat'] = lat;context['lon'] = lon
    if grid is not None:initial['grid'] = str(grid)
    if state is not None:initial['state'] = state
    if bounding_box is not None:initial['bounding_box'] = bounding_box

    if initial:
        if element and start_date and end_date:
            form1 = forms.ClimateMapForm1(initial=initial)
            context['form1'] = form1
            context['hide_form0'] = True
            context['form1_ready'] = True
        else:
            form0 = set_as_form(request,'ClimateMapForm0', init=initial)
            context['form0'] = form0
    else:
        form0 = set_as_form(request,'ClimateMapForm0')
        context['form0'] = form0

    if 'form0' in request.POST:
        form0 = set_as_form(request,'ClimateMapForm0')
        context['form0']  = form0
        context['hide_form0'] = True
        if form0.is_valid():
            context['form1_ready'] = True
            context['select_grid_by'] = form0.cleaned_data['select_grid_by']
            if form0.cleaned_data['select_grid_by'] == 'bbox':
                bounding_box = request.GET.get('bounding_box', None)
                if bounding_box is not None:
                    context['bbox'] = bounding_box
                else:
                    context['bbox'] = '-115,34,-114,35'
                context['need_map'] = True
            initial = {'select_grid_by':form0.cleaned_data['select_grid_by'], \
                      'element':form0.cleaned_data['element'], \
                      'time_period':form0.cleaned_data['time_period'], \
                      'x': form0.cleaned_data['x']}
            form1 = forms.ClimateMapForm1(initial=initial)
            context['form1'] = form1

    if 'form1' in request.POST:
        form1 = set_as_form(request,'ClimateMapForm1')
        context['form1'] = form1
        context['hide_form0'] = True
        if form1.is_valid():
            image = dict(type='png',proj='lcc',interp='cspline',cmap='jet',
                    overlays=['state','county:0.5:black'],width=500, height=400)
            params = {'image':image , 'output':'json', 'grid': form1.cleaned_data['grid'], \
                    'sdate': form1.cleaned_data['start_date'], \
                    'edate': form1.cleaned_data['end_date']}
            if form1.cleaned_data['element'] == 'gddxx':
                elem = 'gdd%s' %str(form1.cleaned_data['base_temperature_gddxx'])
                context['elems_long'] = WRCCData.ACIS_ELEMENTS_DICT['gdd']['name_long']
                context['base_temp'] = str(form1.cleaned_data['base_temperature_gddxx'])
            elif form1.cleaned_data['element'] == 'hddxx':
                elem = 'hdd%s' %str(form1.cleaned_data['base_temperature_hddxx'])
                context['elems_long'] = WRCCData.ACIS_ELEMENTS_DICT['hdd']['name_long']
                context['base_temp'] = str(form1.cleaned_data['base_temperature_hddxx'])
            elif form1.cleaned_data['element'] == 'cddxx':
                elem = 'cdd%s' %str(form1.cleaned_data['base_temperature_cddxx'])
                context['elems_long'] = WRCCData.ACIS_ELEMENTS_DICT['cdd']['name_long']
                context['base_temp'] = str(form1.cleaned_data['base_temperature_cddxx'])
            else:
                elem = str(form1.cleaned_data['element'])
                context['elems_long'] = WRCCData.ACIS_ELEMENTS_DICT[elem]['name_long']
            params['elems'] = [{'name':elem}]
            if 'state' in form1.cleaned_data.keys():
                params['state'] = form1.cleaned_data['state']
                region = 'state_%s' %form1.cleaned_data['state']
                context['state'] = form1.cleaned_data['state']
            elif 'bounding_box' in form1.cleaned_data.keys():
                context['need_map'] = True
                context['bbox'] = form1.cleaned_data['bounding_box']
                params['bbox'] = form1.cleaned_data['bounding_box']
                region = 'bbox_' + re.sub(',','_',form1.cleaned_data['bounding_box'])
                context['bbox'] = form1.cleaned_data['bounding_box']

            context['elems'] = elem
            context['start_date']= form1.cleaned_data['start_date']
            context['end_date'] = form1.cleaned_data['end_date']
            context['grid']= form1.cleaned_data['grid']
            context['select_grid_by'] = form1.cleaned_data['select_grid_by']
            context['params'] = params
            fig = WRCCClasses.GridFigure(params)
            results = fig.get_grid()
            time_stamp = datetime.datetime.now().strftime('%Y%m_%d_%H_%M_%S_')
            figure_file = time_stamp + 'acis_map_' + region + '.png'
            context['time_stamp'] = time_stamp
            context['region']= region
            file_path_big = MEDIA_URL + TEMP_FILE_DIR + figure_file
            #file_path_small = MEDIA_URL +'tmp/' + time_stamp + 'acis_map_small_' + region + '.png'
            #context['file_path_thumbnail'] = file_path_small
            fig.build_figure(results, file_path_big)
            context['figure_file'] = figure_file
            #fig.draw_thumbnail(results,file_path_small)
        #form1 not valid or we are done with computations
        form0 = forms.ClimateMapForm0()
        context['form0'] = form0
        form1 = set_as_form(request, 'ClimateMapForm1')
        context['form1_ready'] = True
        context['form1'] = form1
    return render_to_response('my_data/apps/gridded/clim_sum_maps.html', context, context_instance=RequestContext(request))

def clim_prob_maps(request):
    context = {
        'title': 'Climate Probability Maps',
        'icon':'ToolProduct.png'
    }
    return render_to_response('my_data/apps/gridded/clim_prob_maps.html', context, context_instance=RequestContext(request))

def area_time_series(request):
    context = {
        'title': 'Spatial Summary Time Series',
    }
    json_file = request.GET.get('json_file', None)
    #Check if we are coming in from other page, e.g. Gridded Data
    #Set initial accordingly
    if json_file is not None:
        with open(TEMP_FILE_DIR + json_file, 'r') as f:
            try:
                json_data = WRCCUtils.u_convert(json.loads(f.read()))
                initial,checkbox_vals = set_area_time_series_initial(json_data['search_params'])
            except:
                initial,checkbox_vals = set_area_time_series_initial(request)
    else:
        initial,checkbox_vals = set_area_time_series_initial(request)

    if 'location' in initial.keys():
        context['need_gridpoint_map'] = True
    initial_plot, checkbox_vals_plot = set_plot_options(request)
    join_initials(initial, initial_plot, checkbox_vals, checkbox_vals_plot)
    context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
    #Set up maps if needed
    context['host'] = 'wrcc.dri.edu'
    context['area_type'] = initial['select_grid_by']
    context[initial['select_grid_by']] = WRCCData.AREA_DEFAULTS[initial['select_grid_by']]
    kml_file = initial['overlay_state'] + '_' + initial['select_grid_by'] + '.kml'
    context[initial['overlay_state'] + '_selected'] = 'selected'
    context['kml_file_path'] = WEB_SERVER_DIR +  kml_file
    #Check if kml file exists, if not generate it
    try:
        with open(TEMP_FILE_DIR + kml_file):
            if os.stat(TEMP_FILE_DIR + kml_file).st_size==0:
                status = WRCCUtils.generate_kml_file(initial['select_grid_by'], initial['overlay_state'] , kml_file, TEMP_FILE_DIR)
    except IOError:
        status = WRCCUtils.generate_kml_file(initial['select_grid_by'], initial['overlay_state'] , kml_file, TEMP_FILE_DIR)

    if 'formTS' in request.POST:
        context['need_gridpoint_map'] = False
        form = set_form(request)
        #Form Check
        fields_to_check = ['start_date', 'end_date','elements','connector_line_width', 'vertical_axis_min', 'vertical_axis_max']
        form_error = check_form(form, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            return render_to_response('my_data/apps/gridded/area_time_series.html', context, context_instance=RequestContext(request))
        #Set initials
        initial,checkbox_vals = set_area_time_series_initial(form)
        initial_plot, checkbox_vals_plot = set_plot_options(form)
        join_initials(initial, initial_plot, checkbox_vals, checkbox_vals_plot)
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
        #Display liust and serach params
        search_params, display_params_list =  set_area_time_series_params(form)
        context['display_params_list'] = display_params_list
        context['req'] =display_params_list[1]
        #joins plot opts to search_params
        join_dicts(search_params,initial_plot)
        #Set overlay map if neded
        if form['select_grid_by'] in ['basin', 'county_warning_area', 'climate_division', 'county']:
            context['host'] = 'wrcc.dri.edu'
            kml_file_name = form['overlay_state'] + '_' + form['select_grid_by'] + '.kml'
            context['kml_file_path'] = WEB_SERVER_DIR + kml_file_name
            context['area_type'] = form['select_grid_by']
        #Data Request
        #Skip data generation of it has already been performed
        json_file = request.GET.get('json_file', None)
        if json_file is not None:
            context['json_file'] =json_file
            context['JSON_URL'] = TEMP_FILE_DIR
            with open(TEMP_FILE_DIR + json_file, 'r') as f:
                try:
                    json_data = WRCCUtils.u_convert(json.loads(f.read()))
                    if not 'graph_data' in json_data.keys() or not 'download_data' in json_data.keys():
                        context['error'] = 'No data found in file %s' %json_file
                        return render_to_response('my_data/apps/gridded/area_time_series.html', context, context_instance=RequestContext(request))
                except Exception, e:
                    context['error'] = 'Error when reading %s: %s' (json_file, str(e))
                    return render_to_response('my_data/apps/gridded/area_time_series.html', context, context_instance=RequestContext(request))
            summary_time_series = json_data['graph_data']
            download_data = json_data['download_data']
        else:
            #set up bbox query for area_type
            data_request_params,shape_type,shape_coords,PointIn,poly  = set_params_for_shape_queries(search_params)
            area_description = WRCCData.DISPLAY_PARAMS[shape_type]
            if shape_type !='polygon':
                area_description+= ': ' + form[form['select_grid_by']]
            search_params['area_description'] = area_description

            #Find data
            try:
                req = AcisWS.GridData(data_request_params)
            except Exception, e:
                context['error'] = 'Error in data request: ' + str(e)
                return render_to_response('my_data/apps/gridded/area_time_series.html', context, context_instance=RequestContext(request))
            if not 'data' in req.keys():
                context['error'] = 'No data found for this set of parameters.'
                return render_to_response('my_data/apps/gridded/area_time_series.html', context, context_instance=RequestContext(request))
            #Generate time series from data request
            summary_time_series, download_data = compute_area_time_series_summary(req,search_params,poly,PointIn)
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
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        json_file = '%s_area_time_series.json' %(time_stamp)
        f = open(TEMP_FILE_DIR + '%s' %(json_file),'w+')
        f.write(results_json)
        f.close()
        context['JSON_URL'] = WEB_SERVER_DIR
        context['json_file'] = json_file

    #overlay map generation
    if 'formOverlay' in request.POST:
        form = set_form(request)
        context['need_overlay_map'] = True
        context['need_gridpoint_map'] = False
        initial, checkbox_vals = set_station_data_initial(request)
        #Override initial where needed
        initial['select_grid_by'] = form['select_overlay_by']
        checkbox_vals[form['select_overlay_by'] + '_selected'] = 'selected'
        initial['area_type_value'] = WRCCData.AREA_DEFAULTS[form['select_overlay_by']]
        initial[form['select_overlay_by']] = WRCCData.AREA_DEFAULTS[form['select_overlay_by']]
        initial['area_type_label'] = WRCCData.DISPLAY_PARAMS[form['select_overlay_by']]
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
        at = form['select_overlay_by']
        st = form['overlay_state']
        context[st + '_selected'] = 'selected'
        kml_file_name = st + '_' + at + '.kml'
        dir_location = TEMP_FILE_DIR
        status = WRCCUtils.generate_kml_file(at, st, kml_file_name, dir_location)
        if not status == 'Success':
            context['overlay_error'] = status
        else:
            context['host'] = 'wrcc.dri.edu'
            context['kml_file_path'] = WEB_SERVER_DIR + kml_file_name
            context['area_type'] = form['select_overlay_by']
    #Downlaod Table Data
    if 'formDownload' in request.POST:
        data_format = request.POST.get('data_format', 'clm')
        delimiter = request.POST.get('delimiter', 'comma')
        output_file_name = request.POST.get('output_file_name', 'output')
        json_file = request.POST.get('json_file', None)
        with open(TEMP_FILE_DIR + json_file, 'r') as f:
            json_dict =  json.load(f)
        DDJ = WRCCClasses.DownloadDataJob('area_time_series',data_format,delimiter, output_file_name, request=request, json_in_file=TEMP_FILE_DIR + json_file)
        return DDJ.write_to_file()

    return render_to_response('my_data/apps/gridded/area_time_series.html', context, context_instance=RequestContext(request))

def old_area_time_series(request):
    context = {
        'title': 'Area Time Series',
    }
    element = request.GET.get('element', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    grid= request.GET.get('grid', None)
    state = request.GET.get('state', None)
    bounding_box = request.GET.get('bounding_box', None)
    initial = {}
    if element is not None:initial['element'] = str(element)
    if start_date is not None:initial['start_date'] = str(start_date)
    if end_date is not None:initial['end_date'] = str(end_date)
    if grid is not None:initial['grid'] = str(grid)
    if state is not None:initial['state'] = state
    if bounding_box is not None:
        initial['bbox'] = bounding_box
    if initial:
        if element and start_date and end_date:
            form1 = forms.AreaTimeSeriesForm1(initial=initial)
            context['form1'] = form1
            context['hide_form0'] = True
            context['form1_ready'] = True
        else:
            form0 = set_as_form(request,'AreaTimeSeriesForm0', init=initial)
            context['form0'] = form0
    else:
        form0 = set_as_form(request,'AreaTimeSeriesForm0')
        context['form0'] = form0

    if 'form0' in request.POST:
        form0 = set_as_form(request,'AreaTimeSeriesForm0')
        context['form0']  = form0
        context['hide_form0'] = True
        if form0.is_valid():
            initial = form0.cleaned_data
            context['form1'] = forms.AreaTimeSeriesForm1(initial=initial)
            context['form1_ready'] = True

            if form0.cleaned_data['select_grid_by'] == 'shape':
                context['need_polymap'] = True
            if form0.cleaned_data['select_grid_by'] == 'bbox':
                context['need_bbox_map'] = True
            if form0.cleaned_data['select_grid_by'] in ['basin', 'cwa', 'climdiv', 'county']:
                context['need_overlay_map'] = True
                form2 = forms.StateForm(initial = initial)
                context['form2'] = form2
                context['host'] = 'wrcc.dri.edu'
                context['type'] = form0.cleaned_data['select_grid_by']
                context['kml_file_path'] = STATIC_KML + 'nv_' + form0.cleaned_data['select_grid_by'] + '.kml'
            context[form0.cleaned_data['select_grid_by']] = WRCCData.AREA_DEFAULTS[form0.cleaned_data['select_grid_by']]

    if 'form1' in request.POST:
        context[request.POST['select_grid_by']] = str(request.POST[WRCCData.ACIS_TO_SEARCH_AREA[str(request.POST['select_grid_by'])]])
        #if 'shape' in request.POST.keys():context['shape'] = str(request.POST['shape'])
        #if 'bounding_box' in request.POST.keys():context['bbox'] = str(request.POST['bounding_box'])
        form1 = set_as_form(request,'AreaTimeSeriesForm1')
        context['form1']  = form1
        context['hide_form0'] = True
        context['form1_ready'] = True
        if form1.is_valid():
            search_params, display_params_list =  set_area_time_series_params(form1)
            smry = WRCCData.DISPLAY_PARAMS[form1.cleaned_data['summary']]
            #Set up data request params
            params = {
                'sdate':search_params['start_date'],
                'edate':search_params['end_date'],
                'grid':search_params['grid'],
                'meta':"ll,elev"
            }
            #find element parameter
            if search_params['element'] in ['hddxx','gddxx', 'cddxx']:
                element_name = WRCCData.ACIS_ELEMENTS_DICT[str(search_params['element'])[0:3]]['name_long'] + 'Base temperature ' + str(search_params['base_temperature'])
                yAxisText = smry + ' ' + search_params['element'][0:3] + search_params['base_temperature']
                params['elems'] = search_params['element'][0:3] + search_params['base_temperature']

            else:
                element_name = WRCCData.ACIS_ELEMENTS_DICT[search_params['element']]['name_long']
                yAxisText = smry + ' ' + WRCCData.ACIS_ELEMENTS_DICT[search_params['element']]['name_long']
                params['elems'] = search_params['element']

            #Find search area parameters, shape and bounding box if needed
            key, val, acis_param, name_long, search_type = WRCCUtils.get_search_area_values(search_params, 'gridded')
            if search_type == 'default':
                params[acis_param] = val
                poly = 'Not Needed'
                shape = None;shape_name = ''
            else:
                #search area county/climdiv/basin/cwa or custom shape
                # need to find coordinates of shape and enclosing bbox
                if key == 'shape':
                    shape = val.split(',')
                    shape = [float(s) for s in shape]
                    shape_name = ''
                    #find enclosing bounding box
                    shape_type, bbox = WRCCUtils.get_bbox(val)
                    if bbox is None:
                        context['results'] = 'No bounding box could be found!'
                        return render_to_response('my_data/apps/gridded/area_time_series.html', context, context_instance=RequestContext(request))
                    if shape_type == 'circle':
                        PointIn = getattr(WRCCUtils,'point_in_circle')
                        poly = shape
                    elif shape_type in ['polygon', 'bbox', 'point']:
                        if shape_type == 'bbox':
                            shape = [shape[0], shape[1], shape[2], shape[1], shape[0],shape[3], shape[2],shape[3]]
                        PointIn = getattr(WRCCUtils,'point_in_poly')
                        poly = [(shape[2*idx],shape[2*idx+1]) for idx in range(len(shape)/2)]
                        context['shape_coords'] = [[shape[2*idx],shape[2*idx+1]] for idx in range(len(shape)/2)]

                else:
                    #Need to find shape coordinates and enclosing bbox
                    #via ACIS general call
                    gen_params={'id':str(val),'meta':'geojson,bbox,name,id'}
                    try:
                        gen_req = AcisWS.General(acis_param, gen_params)
                        shape = gen_req['meta'][0]['geojson']['coordinates'][0][0]
                        context['shape_coords'] = shape
                        bbox = gen_req['meta'][0]['bbox']
                        shape_name = gen_req['meta'][0]['name']
                    except:
                        context['results'] = 'Shape or bounding box could not be found!'
                        return render_to_response('my_data/apps/gridded/area_time_series.html', context, context_instance=RequestContext(request))
                    poly = [(s[0],s[1]) for s in shape]
                    PointIn = getattr(WRCCUtils,'point_in_poly')

                params['bbox'] = bbox

            #Set graph title
            if search_params['graph_title'] != 'Use default':
                graph_title = search_params['graph_title']
            else:
                if 'shape' in search_params.keys():
                    graph_title = name_long + ': Polygon'
                else:
                    graph_title = name_long + ': ' + shape_name + ' (' + search_params[key] + ')'
            #Find data
            try:
                req = AcisWS.GridData(params)
                #Find unique lats,lons
                lats_bbox_unique = [lat_grid[0] for lat_grid in req['meta']['lat']]
                lons_bbox_unique = req['meta']['lon'][0]
            except Exception, e:
                context['results'] = 'Error in data request: ' + str(e)
                return render_to_response('my_data/apps/gridded/area_time_series.html', context, context_instance=RequestContext(request))

            if not lats_bbox_unique or not lons_bbox_unique:
                context['results'] = 'No data found!'
                return render_to_response('my_data/apps/gridded/area_time_series.html', context, context_instance=RequestContext(request))

            #Find data lying within shape
            data_poly = [[str(dat[0])] for dat in req['data']]
            values_poly = [[] for dat in req['data']] #list of list holding just the data values for each day at each gridpoint
            summary_time_series = [[str(dat[0])] for dat in req['data']]
            #Check each bbox unique lat, lon combintation for containment in the polygon
            for lat_idx,lat in enumerate(lats_bbox_unique):
                for lon_idx, lon in enumerate(lons_bbox_unique):
                    if poly == 'Not Needed':
                        point_in = True
                    else:
                        point_in = PointIn(lon, lat, poly)
                    if point_in:
                        #point lies witin shape, add data to data_poly
                        for date_idx, date_data in enumerate(req['data']):
                            if abs(date_data[1][lat_idx][lon_idx]+999.0) > 0.001 and abs(date_data[1][lat_idx][lon_idx]-999.0)>0.001:
                                data_poly[date_idx].append([round(lon,2), round(lat,2), date_data[1][lat_idx][lon_idx]])
                                values_poly[date_idx].append(date_data[1][lat_idx][lon_idx])
            #Perform Summary Analysis
            if not values_poly:
                summary_time_series[date_idx].append('-----')
            else:
                for date_idx, val_list in enumerate(values_poly):
                    if not val_list:
                        summary_time_series[date_idx].append('-----')
                        continue
                    if search_params['summary'] == 'sum':
                        summary_time_series[date_idx].append(round(sum(val_list),2))
                    elif search_params['summary'] == 'max':
                        summary_time_series[date_idx].append(round(max(val_list),2))
                    elif search_params['summary'] == 'min':
                        summary_time_series[date_idx].append(round(min(val_list),2))
                    elif search_params['summary'] == 'mean':
                        if val_list:
                            summary_time_series[date_idx].append(round(sum(val_list) / len(val_list),2))
                        else:
                            summary_time_series[date_idx].append('-----')
            #Set context variables
            context['results']= summary_time_series
            context['width'] = WRCCData.IMAGE_SIZES[search_params['image_size']][0]
            context['height'] = WRCCData.IMAGE_SIZES[search_params['image_size']][1]
            #context['bbox'] = bbox
            context['graph_title'] = graph_title
            context['graph_subtitle'] = smry + element_name
            context['display_params_list'] = display_params_list
            #Write results to json file
            if 'base_temperature' in search_params.keys():
                base_temperature = search_params['base_temperature']
            else:
                base_temperature = ''
            json_dict = {
                'search_params':search_params,
                'element_name':element_name,
                'yAxisText':yAxisText,
                'data':summary_time_series,
                'graph_title':graph_title,
                'summary':smry
            }
            results_json = json.dumps(json_dict)
            time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            json_file = '%s_climrisk.json' %(time_stamp)
            f = open(TEMP_FILE_DIR + '%s' %(json_file),'w+')
            f.write(results_json)
            f.close()
            context['JSON_URL'] = TEMP_FILE_DIR
            context['json_file'] = json_file

    #overlay map generation
    if 'form2' in request.POST:
        #context['req'] = request.POST
        form2 = set_as_form(request,'StateForm')
        context['form2'] = form2
        context['need_overlay_map'] = True
        if form2.is_valid():
            initial = {'select_grid_by':str(form2.cleaned_data['select_grid_by']), 'element':str(form2.cleaned_data['element'])}
            context[form2.cleaned_data['select_grid_by']] = WRCCData.AREA_DEFAULTS[form2.cleaned_data['select_grid_by']]
            context['type'] = form2.cleaned_data['select_grid_by']
            form1 = forms.AreaTimeSeriesForm1(initial=initial)
            context['form1']  = form1
            context['hide_form0'] = True
            context['form1_ready'] = True
            at = str(form2.cleaned_data['select_grid_by'])
            st = str(form2.cleaned_data['state']).lower()
            kml_file_name = st + '_' + at + '.kml'
            dir_location = TEMP_FILE_DIR
            status = WRCCUtils.generate_kml_file(at, st, kml_file_name, dir_location)
            if not status == 'Success':
                context['overlay_error'] = status
            else:
                context['host'] = 'wrcc.dri.edu'
                context['kml_file_path'] = WEB_SERVER_DIR + kml_file_name

    return render_to_response('my_data/apps/gridded/area_time_series.html', context, context_instance=RequestContext(request))

def grid_point_time_series(request):
    context = {
        'title': 'Grid Point Time Series',
        'icon':'ToolProduct.png'
    }
    location = request.GET.get('location', None)
    elements= request.GET.get('elements', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    grid = request.GET.get('grid', None)
    initial = {}
    if elements is not None:initial['elements'] = str(elements)
    if start_date is not None:initial['start_date'] = str(start_date)
    if end_date is not None:initial['end_date'] = str(end_date)
    if location is None:
        location= '-111.0,40.0'
    initial['location']= location
    initial['lat'] = location.replace(' ','').split(',')[1]
    initial['lon'] = location.replace(' ','').split(',')[0]
    if grid is not None:
        initial['grid'] = str(grid)

    if initial:
        form0 = set_as_form(request,'GPTimeSeriesForm', init=initial)
    else:
        form0 = set_as_form(request,'GPTimeSeriesForm')
    context['form0'] = form0
    context['search_params'] = initial

    if 'form0' in request.POST:
        form0 = set_as_form(request,'GPTimeSeriesForm')
        context['form0']  = form0

        if form0.is_valid():
            search_params = {}
            for key, val in form0.cleaned_data.iteritems():
                search_params[key]=str(val)
            #check for base temperature if gdd, hdd, cdd
            elements = ','.join(form0.cleaned_data['elements'])
            search_params['elements'] = elements
            search_params['element_list'] = form0.cleaned_data['elements']
            elements_long = ['' for el in form0.cleaned_data['elements']]
            base_temps = ['' for el in form0.cleaned_data['elements']]
            for el_idx, el in enumerate(form0.cleaned_data['elements']):
                element, base_temp = WRCCUtils.get_el_and_base_temp(el)
                if base_temp is not None:
                    base_temps[el_idx] = base_temp
                elements_long[el_idx] = WRCCData.ACIS_ELEMENTS_DICT[element]['name_long']
                if base_temp:
                    elements_long[el_idx]+=' ' + str(base_temp)
            search_params['elements_long'] = elements_long
            location = form0.cleaned_data['location']
            search_params['lat'] = location.replace(' ','').split(',')[1]
            search_params['lon'] = location.replace(' ','').split(',')[0]
            context['search_params'] = search_params
            #Note: acis takes lon, lat in that order
            req = AcisWS.get_grid_data(form0.cleaned_data, 'GPTimeSeries')
            if not 'data' in req.keys():
                context['error'] = 'No data found for this set of parameters. Check that your grid has data for the time period you are interested in.'
                return render_to_response('my_data/apps/gridded/grid_point_time_series.html', context, context_instance=RequestContext(request))
            data = [[] for el in search_params['element_list']]
            dates = []
            for date_idx, dat in enumerate(req['data']):
                for el_idx in range(1,len(search_params['element_list']) + 1):
                    if abs(req['data'][date_idx][el_idx] - 999.0) < 0.0001 or abs(req['data'][date_idx][el_idx] + 999.0) < 0.0001:
                        data[el_idx - 1].append(None)
                    else:
                        data[el_idx - 1].append(req['data'][date_idx][el_idx])
                dates.append('%s%s%s' %(str(req['data'][date_idx][0][0:4]), str(req['data'][date_idx][0][5:7]), str(req['data'][date_idx][0][8:10])))
            context['start_date'] = dates[0]
            context['end_date'] = dates[-1]
            datadict = {'data':data, 'dates':dates, 'search_params':search_params}
            context['datadict'] = datadict
            #results_json = str(datadict).replace("\'", "\"")
            results_json = json.dumps(datadict)
            time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            json_file = '%s_gp_ts_%s_%s_%s_%s.json' %(time_stamp, search_params['lat'], \
                search_params['lon'], form0.cleaned_data['start_date'], \
                form0.cleaned_data['end_date'])
            context['json_file'] = json_file
            JSON_URL = TEMP_FILE_DIR
            f = open('%s%s' %(JSON_URL,json_file),'w+')
            f.write(results_json)
            f.close()
    return render_to_response('my_data/apps/gridded/grid_point_time_series.html', context, context_instance=RequestContext(request))

def station_locator_app(request):
    from subprocess import call
    call(["touch", TEMP_FILE_DIR + "Empty.json"])
    context = {
        'title': 'Station Finder',
        'icon':'Magnify.png'
    }
    form0 = set_as_form(request,'StationLocatorForm0')
    context['form0'] = form0
    context['empty_json'] = False
    context['show_legend'] = True
    context['map_title'] = 'Map of Southwest US COOP stations!'

    if 'form0' in request.POST:
        context['map_title'] = ''
        context['empty_json'] = True
        form0 = set_as_form(request,'StationLocatorForm0')
        context['form0']  = form0
        context['show_legend'] = False
        if form0.is_valid():
            context['form1_ready'] = True
            initial_params= {}
            stn_id = request.GET.get('stn_id', None)
            if stn_id is not None:initial_params['station_id'] = str(stn_id)
            initial_params['select_stations_by'] = form0.cleaned_data['select_stations_by']
            initial_params['element_selection'] = form0.cleaned_data['element_selection']
            form1 = forms.StationLocatorForm1(initial=initial_params)
            context['form1'] = form1
            if form0.cleaned_data['select_stations_by'] == 'bbox':
                context['need_map_bbox'] = True
            if form0.cleaned_data['select_stations_by'] == 'shape':
                context['need_polymap'] = True
            if form0.cleaned_data['select_stations_by'] in ['basin', 'cwa', 'climdiv', 'county']:
                context['need_overlay_map'] = True
                initial = {
                    'select_stations_by':form0.cleaned_data['select_stations_by'],
                    'element_selection': form0.cleaned_data['element_selection']
                }
                form2 =forms.StateForm(initial=initial)
                context['form2'] = form2
                context['host'] = 'wrcc.dri.edu'
                context['type'] = form0.cleaned_data['select_stations_by']
                context['kml_file_path'] = STATIC_KML + 'nv_' + form0.cleaned_data['select_stations_by'] + '.kml'
            context[form0.cleaned_data['select_stations_by']] = WRCCData.AREA_DEFAULTS[form0.cleaned_data['select_stations_by']]

    if 'form1' in request.POST:
        context[request.POST['select_stations_by']] = str(request.POST[WRCCData.ACIS_TO_SEARCH_AREA[str(request.POST['select_stations_by'])]])
        context['empty_json'] = True
        form1 = set_as_form(request,'StationLocatorForm1')
        context['form1'] = form1
        context['form1_ready'] = True
        if form1.is_valid():
            context[form1.cleaned_data['select_stations_by']] = form1.cleaned_data[form1.cleaned_data['select_stations_by']]
            if 'elements' in form1.cleaned_data.keys():
                element_list = ','.join(form1.cleaned_data['elements'])
            else:
                element_list = 'Any climate element'
                context['elements']= 'Any climate element'

            by_type = WRCCData.ACIS_TO_SEARCH_AREA[form1.cleaned_data['select_stations_by']]
            val = form1.cleaned_data[WRCCData.ACIS_TO_SEARCH_AREA[form1.cleaned_data['select_stations_by']]]
            context['by_type'] = WRCCData.DISPLAY_PARAMS[WRCCData.ACIS_TO_SEARCH_AREA[form1.cleaned_data['select_stations_by']]] + str(val)
            context['map_title'] = by_type.upper() + ': ' + val

            date_range = [str(form1.cleaned_data['start_date']), str(form1.cleaned_data['end_date'])]
            context['start_date'] = form1.cleaned_data['start_date']
            context['end_date'] = form1.cleaned_data['end_date']
            constraints = WRCCData.DISPLAY_PARAMS[str(form1.cleaned_data['constraints'])]
            context['constraints'] = constraints
            if form1.cleaned_data['element_selection'] == 'T':
                context['map_title'] = by_type.upper() + ': ' + val + ', ELEMENTS: ' + \
                                ','.join(form1.cleaned_data['elements']) + \
                                ', FROM: ' + form1.cleaned_data['start_date'] + ' TO: '+ form1.cleaned_data['start_date'] + \
                                ', ' + constraints
                context['elements'] = ','.join(form1.cleaned_data['elements']) #tuple of elements
                #Convert element_list to list of var majors
                el_vX_list = []
                for el_idx, el in enumerate(form1.cleaned_data['elements']):
                    #Check if user entered a gddxx,hddxx,cddxx
                    el_strip = re.sub(r'(\d+)(\d+)', '', el)   #strip digits from gddxx, hddxx, cddxx
                    b = el[-2:len(el)] #base_temp
                    try:
                        int(b)
                        if el_strip in ['hdd', 'gdd']:
                            el_vX_list.append('45')
                        elif el_strip == 'cdd':
                            el_vX_list.append('45') #should be 44
                        else:
                            pass
                    except:
                        el_vX_list.append(str(WRCCData.ACIS_ELEMENTS_DICT[el]['vX']))

                stn_json, f_name = AcisWS.station_meta_to_json(by_type, val, el_list=el_vX_list,time_range=date_range, constraints=form1.cleaned_data['constraints'])
            else:
                context['map_title'] = by_type.upper() + ': ' + val + \
                                ', FROM: ' + form1.cleaned_data['start_date'] + ' TO: '+ form1.cleaned_data['start_date'] + \
                                ', ' + constraints
                el_vX_list = ['1', '2', '4', '10', '11', '45']
                context['elements'] = 'maxt, mint, pcpn, snow, snwd, hdd, cdd, gdd' #tuple of elements
                stn_json, f_name = AcisWS.station_meta_to_json(by_type, val, el_list=el_vX_list,time_range=date_range, constraints=form1.cleaned_data['constraints'])

            if 'error' in stn_json.keys():
                context['error'] = stn_json['error']
            if stn_json['stations'] == []:
                context['error'] = "No stations found for %s : %s, elements: %s."  %(by_type, val, element_list)
            context['json_file'] = f_name
            context['empty_json'] = False
            context['form1_ready'] = True
            context['show_legend'] = True

    #overlay map generation
    if 'form2' in request.POST:
        form2 = set_as_form(request,'StateForm')
        context['form2'] = form2
        context['need_overlay_map'] = True
        if form2.is_valid():
            initial = {'select_stations_by':str(form2.cleaned_data['select_stations_by']), 'element_selection':str(form2.cleaned_data['element_selection'])}
            context[form2.cleaned_data['select_stations_by']] = WRCCData.AREA_DEFAULTS[form2.cleaned_data['select_stations_by']]
            context['type'] = form2.cleaned_data['select_stations_by']
            form1 = forms.StationLocatorForm1(initial=initial)
            context['form1']  = form1
            context['form1_ready'] = True
            at = str(form2.cleaned_data['select_stations_by'])
            st = str(form2.cleaned_data['state']).lower()
            kml_file_name = st + '_' + at + '.kml'
            dir_location = TEMP_FILE_DIR
            status = WRCCUtils.generate_kml_file(at, st, kml_file_name, dir_location)
            if not status == 'Success':
                context['overlay_error'] = status
            else:
                context['host'] = 'wrcc.dri.edu'
                context['kml_file_path'] = WEB_SERVER_DIR + kml_file_name


    return render_to_response('my_data/apps/station/station_locator_app.html', context, context_instance=RequestContext(request))

#######################
#SOD programs
######################

def sodxtrmts(request):
    context = {
        'title': 'Monthly Summary Time Series',
        'icon':'ToolProduct.png'
    }
    json_dict =  None
    json_file = request.GET.get('json_file', None)
    if json_file is not None:
        context['json_file'] =json_file
        context['JSON_URL'] = TEMP_FILE_DIR
    initial,checkbox_vals = set_sodxtrmts_initial(request)
    context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
    #Set graph and plot options
    initial_graph, checkbox_vals_graph = set_sodxtrmts_graph_initial(request)
    initial_pl_opts, checkbox_vals_pl_opts = set_plot_options(request)
    #combine the graph options with the plot options
    join_initials(initial_graph,initial_pl_opts, checkbox_vals_graph,checkbox_vals_pl_opts)
    context['initial_graph'] = initial_graph;context['checkbox_vals_graph'] = checkbox_vals_graph

    #Time Serie Table Generation and graph if desired
    if 'formSodxtrmts' in request.POST:
        #Set initial form parameters for html
        initial,checkbox_vals = set_sodxtrmts_initial(request)
        context['initial'] = initial;context['checkbox_vals'] = checkbox_vals
        #Set graph and plot options
        initial_graph, checkbox_vals_graph = set_sodxtrmts_graph_initial(request)
        initial_pl_opts, checkbox_vals_pl_opts = set_plot_options(request)
        #combine the graph options with the plot options
        join_initials(initial_graph,initial_pl_opts, checkbox_vals_graph,checkbox_vals_pl_opts)
        context['initial_graph'] = initial_graph;context['checkbox_vals_graph'] = checkbox_vals_graph
        #Turn request object into python dict
        form = set_form(request)

        #Form sanity check
        #form_error = check_sodxtrmts_form(form)
        fields_to_check = ['start_year', 'end_year','max_missing_days', 'graph_start_year', 'graph_end_year', \
        'connector_line_width', 'vertical_axis_min', 'vertical_axis_max']
        form_error = check_form(form, fields_to_check)
        if form_error:
            context['form_error'] = form_error
            return render_to_response('my_data/apps/station/sodxtrmts.html', context, context_instance=RequestContext(request))

        #Define header for html display
        header = set_sodxtrmts_head(form)

        #Check if we should only generate graphics
        if json_file is None:
            json_file = request.POST.get('j_file', None)
        if json_file:
            with open(TEMP_FILE_DIR + json_file, 'r') as f:
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
                    with open(TEMP_FILE_DIR + '%s' %(json_file),'w+') as f:
                        f.write(results_json)
                    context['json_file'] =json_file
                    context['JSON_URL'] = TEMP_FILE_DIR
                    return render_to_response('my_data/apps/station/sodxtrmts.html', context, context_instance=RequestContext(request))
            else:
                #New data analysis
                initial['generate_graph']='F'
                checkbox_vals['generate_graph_T_selected'] = ''
                checkbox_vals['generate_graph_F_selected'] = 'selected'
                #Reset initial_graph
                initial_graph, checkbox_vals_graph = set_sodxtrmts_graph_initial({'start_year':initial['start_year'], 'end_year':initial['end_year']})
                initial_pl_opts, checkbox_vals_pl_opts = set_plot_options({})
                #combine the graph options with the plot options
                join_initials(initial_graph,initial_pl_opts, checkbox_vals_graph,checkbox_vals_pl_opts)
                context['initial_graph'] = initial_graph;context['checkbox_vals_graph'] = checkbox_vals_graph

        #Data Table generation
        data_params = {
            'sid':form['station_id'],
            'start_date':form['start_year'],
            'end_date':form['end_year'],
            'element':form['element']
        }
        app_params = form
        for key in ['station_id', 'start_year', 'end_year']:
            del app_params[key]
        app_params['el_type'] = form['element']
        del app_params['element']
        #Run data retrieval job
        DJ = WRCCClasses.SODDataJob('Sodxtrmts', data_params)
        #WARNING: station_ids, names need to be called before dates_list
        station_names, station_states, station_ids, station_networks, station_lls, station_elevs, station_uids, station_climdivs, station_counties  = DJ.get_station_meta()
        try:
            header.insert(0, ['Station Name', station_names[0]])
        except:
            header.insert(0, ['Station Name', ''])
        dates_list = DJ.get_dates_list()

        #Overwrite search params to reflect actuall start/end year
        data = DJ.get_data()
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
            averages = [[mon] for mon in month_list]
            ranges = [[mon] for mon in month_list]
            if data_params['element'] == 'dtr':
                element_name = 'Temperature Range (F)'
            else:
                element_name = WRCCData.ACIS_ELEMENTS_DICT[data_params['element']]['name_long']
            if 'base_temperature' in form.keys():
                base_temperature = int(form['base_temperature'])
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
                'stn_id':station_ids[0],
                'stn_name':station_names[0],
                'stn_network':station_networks[0],
                'stn_state':station_states[0],
                'month_list':month_list + ['ANN'],
                'data':results,
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
            time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            json_file = '%s_sodxtrmts_%s_%s_%s.json' \
            %(time_stamp, str(data_params['sid']), dates_list[0][0:4], dates_list[-1][0:4])
            json_dict['json_file'] = json_file
            json_dict['JSON_URL'] = TEMP_FILE_DIR
            results_json = json.dumps(json_dict)
            with open(TEMP_FILE_DIR + '%s' %(json_file),'w+') as f:
                f.write(results_json)
            context['json_dict'] = json_dict
            context['json_file'] = json_file
            context['JSON_URL'] = TEMP_FILE_DIR

    #Downlaod Table Data
    if 'formDownload' in request.POST:
        data_format = request.POST.get('data_format', 'clm')
        delimiter = request.POST.get('delimiter', 'comma')
        output_file_name = request.POST.get('output_file_name', 'output')
        json_file = request.POST.get('json_file', None)
        with open(TEMP_FILE_DIR + json_file, 'r') as f:
            json_dict =  json.load(f)
        context['json_dict'] = json_dict
        DDJ = WRCCClasses.DownloadDataJob('Sodxtrmts',data_format,delimiter, output_file_name, request=request, json_in_file=TEMP_FILE_DIR + json_file)
        return DDJ.write_to_file()

    return render_to_response('my_data/apps/station/sodxtrmts.html', context, context_instance=RequestContext(request))


def sodsumm(request):
    context = {
        'title': 'Sodsumm - Monthly and Seasonal Summaries of Daily Data',
        'icon':'ToolProduct.png'
        }
    initial = set_sod_initial(request, 'Sodsumm')
    form1 = set_as_form(request,'SodsummForm', init=initial)
    context['form1'] = form1

    if 'form1' in request.POST:
        form1 = set_as_form(request,'SodsummForm', init={'date_type':'y'})
        context['form1'] = form1
        if form1.is_valid():
            data_params = {
                    'sid':find_stn_id(form1.cleaned_data['station_id']),
                    'start_date':form1.cleaned_data['start_year'],
                    'end_date':form1.cleaned_data['end_year'],
                    'element':'all'
                    }
            app_params = {
                    'el_type':form1.cleaned_data['summary_type'],
                    'max_missing_days':form1.cleaned_data['max_missing_days'],
                    }
            #Run data retrieval job
            DJ = WRCCClasses.SODDataJob('Sodsumm', data_params)
            #WARNING: station_ids, names need to be called before dates_list
            #station_ids, station_names = DJ.get_station_ids_names()
            station_names, station_states, station_ids, station_networks, station_lls, station_elevs, station_uids, station_climdivs, station_counties  = DJ.get_station_meta()
            dates_list = DJ.get_dates_list()
            data = DJ.get_data()
            #Run application
            App = WRCCClasses.SODApplication('Sodsumm', data, app_specific_params=app_params)
            results = App.run_app()
            #format results to single station output
            if not results:
                results = {}
            else:
                results = dict(results[0])
            context['results'] = results
            #Input parameters:
            context['station_id'] = data_params['sid']
            context['max_missing_days'] = app_params['max_missing_days']
            #Sodsumm table headers for html
            if form1.cleaned_data['generate_graphics'] == 'T':
                context['tab_names'] = WRCCData.TAB_NAMES_WITH_GRAPHICS[form1.cleaned_data['summary_type']]
                tab_list = WRCCData.TAB_LIST_WITH_GRAPHICS[form1.cleaned_data['summary_type']]
                table_list =WRCCData.TABLE_LIST_WITH_GRAPHICS[form1.cleaned_data['summary_type']]
            else:
                context['tab_names'] = WRCCData.TAB_NAMES_NO_GRAPHICS[form1.cleaned_data['summary_type']]
                tab_list = WRCCData.TAB_LIST_NO_GRAPHICS[form1.cleaned_data['summary_type']]
                table_list =WRCCData.TABLE_LIST_NO_GRAPHICS[form1.cleaned_data['summary_type']]
            context['table_list'] = table_list
            context['tab_list'] = tab_list
            #Define html content
            context['run_done'] = True
            if dates_list:
                context['start_year'] = dates_list[0][0:4]
                context['end_year'] = dates_list[-1][0:4]
            else:
                context['start_year'] = '0000'
                context['end_year'] = '0000'
            context['station_name'] = station_names
            headers = set_sodsumm_headers(table_list)
            context['headers'] = headers

            #Generate grahics
            if form1.cleaned_data['generate_graphics'] == 'T' and results:
                context['graphics'] = True

            json_list = []
            for tab_idx, tab in enumerate(tab_list):
                table = table_list[tab_idx]
                table_dict = generate_sodsumm_graphics(results,tab,table)
                #Add other params to table_dict
                table_dict['record_start'] = dates_list[0][0:4]
                table_dict['record_end'] = dates_list[-1][0:4]
                table_dict['stn_name'] = station_names[0]
                table_dict['stn_network'] = station_networks[0]
                table_dict['stn_state'] = station_states[0]
                table_dict['stn_id'] = str(data_params['sid'])
                json_list.append(table_dict)
            results_json = json.dumps(json_list)
            time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            json_file = '%s_sodsumm_%s_%s_%s.json' \
            %(time_stamp, str(data_params['sid']), dates_list[0][0:4], dates_list[-1][0:4])
            f = open(TEMP_FILE_DIR + '%s' %(json_file),'w+')
            f.write(results_json)
            f.close()
            context['JSON_URL'] = TEMP_FILE_DIR
            context['json_file'] = json_file

    #Downlaod Table Data
    for table_idx in range(7):
        if 'formDownload' + str(table_idx) in request.POST:
            data_format = request.POST.get('data_format', 'clm')
            delimiter = request.POST.get('delimiter', 'comma')
            output_file_name = request.POST.get('output_file_name', 'output')
            json_file = request.POST.get('json_file', None)
            tab = request.POST.get('tab', None)
            with open(TEMP_FILE_DIR + json_file, 'r') as json_f:
                json_data = WRCCUtils.u_convert(json.loads(json_f.read()))
                #find the correct data set corresponding to the tab name
                for idx, data_dict in enumerate(json_data):
                    if data_dict['table_name'] == tab:
                        #Overwrite json_in_file
                        json_in_file_name = json_file + '_in'
                        with open(TEMP_FILE_DIR + json_in_file_name, 'w+') as json_f:
                            json.dump(data_dict,json_f)
                        break

            DDJ = WRCCClasses.DownloadDataJob('Sodsumm',data_format,delimiter, output_file_name, request=request, json_in_file=TEMP_FILE_DIR + json_in_file_name)
            return DDJ.write_to_file()

    return render_to_response('my_data/apps/station/sodsumm.html', context, context_instance=RequestContext(request))

##############################
#Utlities
##############################

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
            form_error[WRCCData.DISPLAY_PARAMS[field]] = err

    return form_error

def find_stn_id(form_input_stn):
    '''
    Deals with autofill by station name.
    Note: Autofill sis set up to return name, id
    so we just pick up the id for data analysis
    '''
    stn_id = str(form_input_stn)
    name_id_list = str(form_input_stn).replace(' ','').split(',')
    if len(name_id_list) >=2:
        stn_id= str(name_id_list[-1])
    return stn_id

def set_form(request):
    form = {}
    q_dict = {}
    if request.method == 'POST':
        q_dict = dict(request.POST.items())
    elif request.method == 'GET':
        q_dict = dict(request.GET.items())

    for key,val in q_dict.iteritems():
        form[str(key)] = str(val)
        #Check if user autofilled name, if so, change to id
        if key in ['station_id','county', 'basin', 'county_warning_area', 'climate_divison']:
            form[str(key)] = find_stn_id(str(val))
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
        elif key == '':
            #header.append([])
            pass
        else:
            header.append([WRCCData.DISPLAY_PARAMS[key], str(form[key])])
    return header

def set_sodsumm_headers(table_list):
    headers = {}
    def set_header(table):
        rows = []
        if table == 'temp':
            rows.append('<th colspan="16"> <b>Tempearture Statistics</b></th>')
            rows.append('<tr><td colspan="5">-------</td><td colspan="5">Averages</td><td colspan="4">------Daily Extremes </td><td colspan="4">--------Mean Extremes </td><td colspan="4">----------Number of Days</td></tr>')
        elif table == 'prsn':
            rows.append('<th colspan="15"><b>Precipitation/Snow Statistics</b></th>')
            rows.append('<tr><td colspan="6">--------------Total Precipitation </td><td colspan="2">----------------------</td><td colspan="2">Number of Days</td><td colspan="3">-----------Total Snowfall</td></tr>')

        elif table == 'hdd':
            rows.append('<th colspan="14"><b>Heating degree days</b></th>')
            rows.append('<tr><td colspan="14">Output is rounded, unlike NCDC values, which round input.</td></tr>')
            rows.append('<tr><td colspan="14">Degree Days to selected Base Temperatures(F)</td></tr>')
        elif table == 'cdd':
            rows.append('<th colspan="14"><b>Cooling degree days</b></th>')
            rows.append('<tr><td colspan="14">Output is rounded, unlike NCDC values, which round input.</td></tr>')
            rows.append('<tr><td colspan="14">Degree Days to selected Base Temperatures(F)</td></tr>')
        elif table == 'gdd':
            rows.append('<th colspan="15"><b>Growing degree days</b></th>')
            rows.append('<tr><td colspan="15">Output is rounded, unlike NCDC values, which round input.</td>')
            rows.append('<tr><td colspan="15">Growing Degree Days to selected Base Temperatures(F)</td></tr>')
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
def generate_sodsumm_graphics(results, tab, table):
    cats = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    if tab =='temp':
        legend = ['Extr Low','Ave Low','Mean', 'Ave High', 'Extr High']
        colors  = ['#FF0000', '#690000', '#00FF00', '#ADD8E6', '#0000FF']
        table_name_long = 'Temperatures (F)'
        units = 'Fahrenheit'
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
        units = 'Fahrenheit'
        colors = ['#87CEFA', '#00FFFF', '#14D8FF', '#143BFF', '#8A14FF']
        if table == 'hdd':
            legend = ['Base 65', 'Base 60', 'Base 57', 'Base 55', 'Base 50']
        else:
            legend = ['Base 55', 'Base 57', 'Base 60', 'Base 65', 'Base 70']
        table_name_long = WRCCData.ACIS_ELEMENTS_DICT[table]['name_long']
        graph_data = [[] for i in range(5)]
        for i in range(5):
            for k in range(len(cats)):
                try:
                    graph_data[i].append(float(results[table][i+1][k+1]))
                except:
                    graph_data[i].append(None)
    elif tab == 'gdd':
        units = 'Fahrenheit'
        colors = ['#87CEFA', '#00FFFF', '#14D8FF', '#143BFF', '#8A14FF']
        table_name_long = WRCCData.ACIS_ELEMENTS_DICT[table]['name_long']
        legend = ['Base 40', 'Base 45', 'Base 50', 'Base 55', 'Base 60']
        graph_data = [[] for i in range(5)]
        for i in range(5):
            for k in range(len(cats)):
                try:
                    graph_data[i].append(float(results[table][2*i+1][k+2]))
                except:
                    graph_data[i].append(None)
    elif tab == 'corn':
        units = 'Fahrenheit'
        colors = ['#14FFFF', '#00FFFF', '#14D8FF', '#143BFF', '#8A14FF']
        table_name_long = 'Corn Degree Days (F)'
        legend = ['Base 50']
        graph_data =[[]]
        for k in range(len(cats)):
            try:
                graph_data[0].append(float(results[table][1][k+2]))
            except:
                graph_data[0].append(None)
    elif  tab == 'pcpn':
        units = 'Inches'
        colors = ['#00FFFF','#00009B', ' #0000FF']
        legend = ['Ave Precip Low', 'Precip Mean', 'Ave Precip High']
        table_name_long = 'Precipitation(In)'
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
        units = 'Inches'
        colors = ['#00FFFF','#00009B']
        legend = ['Snow Mean', 'Ave Snow High']
        table_name_long = 'Snow Fall(In)'
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
        'units':units,
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
def compute_area_time_series_summary(req, search_params, poly, PointIn):
    #Sanity check
    element_list = search_params['elements'].replace(' ','').split(',')
    if not 'meta' in req.keys():
        return []
    if not 'lat' in req['meta'].keys():
        return []
    if not 'data' in req.keys():
        return []
    if 'location' in search_params.keys():
        lats_bbox_unique = [req['meta']['lat']]
        lons_bbox_unique = [req['meta']['lon']]
    else:
        lats_bbox_unique = [lat_grid[0] for lat_grid in req['meta']['lat']]
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
                        if 'location' in search_params.keys():
                            try:
                                val = float(date_data[el_idx+1])
                            except:
                                continue
                        else:
                            try:
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
        el_strip = re.sub(r'(\d+)(\d+)', '', el)   #strip digits from gddxx, hddxx, cddxx
        b = el[-2:len(el)]
        base_temp = ''
        try:
            base_temp = int(b)
        except:
            if b == 'dd' and el in ['hdd', 'cdd']:
                base_temp = '65'
            elif b == 'dd' and el == 'gdd':
                base_temp = '50'
        if base_temp:
            results[el_idx] = {'element_long': WRCCData.ACIS_ELEMENTS_DICT[el_strip]['name_long'] + 'Base Temperature: ' + base_temp}
        else:
            results[el_idx] = {'element_long': WRCCData.ACIS_ELEMENTS_DICT[el_strip]['name_long']}
        results[el_idx]['element'] = str(el)
        results[el_idx]['stn_id']= str(form_data['station_id'])

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
    Meta = WRCCUtils.format_stn_meta(req['meta'])
    #format meta data
    elements = ', '.join(form_data['elements'])
    valid_dr = []
    for idx, el in enumerate(form_data['elements']):
        try:
            valid_dr.append('%s: %s - %s ' %(str(el),str(Meta['valid_daterange'][idx][0]),str(Meta['valid_daterange'][idx][1])))
        except:
            valid_dr.append(str(el))

    key_order = ['name', 'valid_daterange', 'll', 'elev', 'state', 'county', 'climdiv', 'uid']
    meta = WRCCUtils.metadict_to_display(Meta, key_order)
    #Override valid daterange
    meta_vd = ['Valid Daterange']
    vd =''
    for idx,el in enumerate(form_data['elements']):
        try:
            v_el = str(Meta['valid_daterange'][idx])
        except:
            v_el = '[]'
        vd+= el + ': ' + v_el
    meta_vd.append(vd)
    meta[1] = meta_vd
    meta.insert(1, ['Elements', elements])
    '''
    meta = ['Station Name: ' +  Meta['name'],
            'Elements :' + elements,
            'Valid Daterange: ' + ', '.join(valid_dr),
            'Lat, Lon: ' +  str(Meta['ll']),
            'Elevation :' +  Meta['elev'],
            'State: ' + Meta['state'],
            'County: ' +  Meta['county'],
            'Climate Division: ' + Meta['climdiv'],
            'Unique Identifier: ' + Meta['uid']
            ]
    '''
    return meta

#############################
#Display and search params
##############################

def set_area_time_series_params(form):
    key_order = ['Area Type','elements','start_date', 'end_date', 'summary', 'grid','running_mean_days']
    display_params_list = [[] for k in range(len(key_order))]
    search_params = {}
    el_list = form['elements'].replace(' ','').split(',')
    search_params['element_list'] = el_list
    display_params_list[0]=[WRCCData.DISPLAY_PARAMS[form['select_grid_by']],form[form['select_grid_by']]]
    for key, val in form.iteritems():
        #Convert to string to avoid unicode issues
        search_params[key] = str(val)
        if key == 'grid':
            display_params_list[5] = [WRCCData.DISPLAY_PARAMS[key], WRCCData.GRID_CHOICES[val]]
        elif key == 'spatial_summary':
            display_params_list[4] = [WRCCData.DISPLAY_PARAMS[key], WRCCData.DISPLAY_PARAMS[val]]
            search_params['spatial_summary_long'] = WRCCData.DISPLAY_PARAMS[form[key]]
        elif key == 'elements':
            el_list_long =[]
            for el in el_list:
                el_short, base_temp = WRCCUtils.get_el_and_base_temp(el)
                if base_temp:
                    el_list_long.append(WRCCData.ACIS_ELEMENTS_DICT[el_short]['name_long'] + ' Base Temp.: ' + str(base_temp))
                else:
                    el_list_long.append(WRCCData.ACIS_ELEMENTS_DICT[el]['name_long'])
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

def set_gridded_data_params(form):
    #display_params_list used to dispaly search params to user
    #params_dict used to link to relevant apps in html doc
    if not form:
        return {}

    key_order = ['select_grid_by', 'elements', 'grid', 'start_date', 'end_date','temporal_resolution', 'data_summary']
    display_params_list = [[] for k in range(len(key_order))]
    params_dict = {'area_type_value':form[form['select_grid_by']]}
    for key, val in form.iteritems():
        #Convert to string to avoid unicode issues
        params_dict[key] = str(val)

        if key == 'grid':
            display_params_list[2] = [WRCCData.DISPLAY_PARAMS[key], WRCCData.GRID_CHOICES[val]]
        elif key in ['data_summary','temporal_resolution']:
            display_params_list[3] = [WRCCData.DISPLAY_PARAMS[key], WRCCData.DISPLAY_PARAMS[val]]
            #params_dict[WRCCData.DISPLAY_PARAMS[key]] = WRCCData.DISPLAY_PARAMS[val]
        elif key == 'elements':
            if isinstance(val, list):
                el_list = val
            elif isinstance(val, str):
                el_list = val.replace(' ','').split(',')
            else:
                el_list = val
            params_dict['element_list'] = el_list
            if len(el_list) == 1:
                params_dict['element'] =  el_list[0]
            elems_long = []
            display_params_list[1] = [WRCCData.DISPLAY_PARAMS[key], '']
            #params_dict[key] = ''
            for el_idx, el in enumerate(el_list):
                try:
                    int(el[3:5])
                    display_params_list[1][1]+=WRCCData.DISPLAY_PARAMS[el[0:3]] + ' Base Temperature '+ el[3:5]
                    elems_long.append(WRCCData.DISPLAY_PARAMS[el[0:3]] + ' Base Temperature '+ el[3:5])
                except:
                    display_params_list[1][1]+=WRCCData.DISPLAY_PARAMS[el]
                    elems_long.append(WRCCData.DISPLAY_PARAMS[el])
                if el_idx != 0 and el_idx != len(form['elements']) - 1:
                    display_params_list[1][1]+=', '
            params_dict['elems_long'] = elems_long
            #determine which apps to link to
            if len(val) == 1:
                try:
                    int(val[3:5])
                    el = val[0:3]
                    base_temp = val[3:5]
                except:
                    el = val[0];base_temp=''
                if str(el) in ['maxt', 'mint', 'avgt', 'gdd', 'hdd', 'cdd', 'pcpn']:
                    params_dict['element'] = el + base_temp
        if key == 'delimiter':
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


def set_station_data_params(form):
    #display_params_list used to dispaly search params to user
    #params_dict iused to link to relevant apps in html doc
    if not form:
        return {}

    key_order = ['select_stations_by', 'elements', 'start_date', 'end_date']
    display_params_list = [[] for k in range(len(key_order))]
    params_dict = {}
    for key, val in form.iteritems():
        #Convert to string to avoid unicode issues
        if key != 'elements':
            form[key] = str(val)

        if key == 'elements':
            if isinstance(val, str):
                el_list = val.replace(' ', '').split(',')
            else:
                el_list = val
            elems_long = []
            display_params_list[1] = [WRCCData.DISPLAY_PARAMS[key], '']
            params_dict[key] = ','.join(el_list)
            params_dict[key].rstrip(',')
            for el_idx, el in enumerate(el_list):
                try:
                    int(el[3:5])
                    display_params_list[1][1]+=WRCCData.DISPLAY_PARAMS[el[0:3]] + ' Base Temperature '+ el[3:5]
                    elems_long.append(WRCCData.DISPLAY_PARAMS[el[0:3]] + ' Base Temperature '+ el[3:5])
                except:
                    display_params_list[1][1]+=WRCCData.DISPLAY_PARAMS[el]
                    elems_long.append(WRCCData.DISPLAY_PARAMS[el])
                if el_idx != 0 and el_idx != len(form['elements']) - 1:
                    display_params_list[1][1]+=', '
                    params_dict[key]+=', '
            params_dict['elems_long'] = elems_long
            #determine which apps to link to
            if 'station_id' in form.keys():
                params_dict['stn_id'] = form['station_id']
        elif key == 'delimiter':
           params_dict['delimiter'] = WRCCData.DELIMITERS[val]
        elif key in ['show_flags', 'show_observation_time']:
            params_dict[key] = val
        else:
            try:
                idx = key_order.index(key)
                display_params_list[idx] = [WRCCData.DISPLAY_PARAMS[key], str(val)]
                params_dict[key] = str(val)
            except ValueError:
                if key in ['station_id','station_ids', 'stnid', 'stn_id','basin', 'county_warning_area', 'climate_division', 'state', 'bounding_box', 'shape']:
                    display_params_list.insert(1, [WRCCData.DISPLAY_PARAMS[key], str(val)])
    if 'delimiter' not in params_dict.keys():
        params_dict['delimiter'] = ' '
    return display_params_list, params_dict

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

def set_plot_options(request):
    initial = {}
    checkbox_vals = {}
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

def set_sod_initial(request, app_name):
    stn_id = request.GET.get('stn_id', None)
    start_date = request.GET.get('start_date', None)
    end_date  = request.GET.get('end_date', None)
    start_year = request.GET.get('start_year', None)
    end_year  = request.GET.get('end_year', None)
    element = request.GET.get('elements', None)
    if element is None:element = request.GET.get('element', None)
    initial ={}
    if element is not None:initial['element'] = element
    if stn_id is not None:initial['stn_id'] = stn_id
    if app_name in ['Sodsumm', 'Sodxtrmts']:
        initial['date_type'] = 'y'
        if start_year is not None:initial['start_year'] = start_year
        if end_year is not None:initial['end_year'] = end_year
        if start_date is not None and not start_year:initial['start_year'] = start_date[0:4]
        if end_date is not None and not end_year:initial['end_year'] = end_date[0:4]
    else:
        initial['date_type'] = 'd'
        if start_date is not None:initial['start_date'] = start_date
        if end_date is not None:initial['end_date'] = end_date
    return initial

def set_sodxtrmts_initial(request):
    initial = {}
    checkbox_vals = {}
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
    stn_id = Get('stn_id', None)
    if stn_id is not None:
        initial['station_id'] = stn_id
    else:
        initial['station_id'] = Get('station_id','266779')
    initial['start_year'] = Get('start_year', 'POR')
    initial['end_year']  = Get('end_year', yesterday[0:4])
    initial['monthly_statistic'] = Get('monthly_statistic', 'msum')
    initial['max_missing_days'] = Get('max_missing_days', '5')
    initial['start_month'] = Get('start_month', '01')
    initial['departures_from_averages'] = Get('departures_from_averages', 'F')
    initial['frequency_analysis'] = Get('frequency_analysis', 'F')
    initial['less_greater_or_between']= Get('less_greater_or_between', None)
    initial['threshold_for_less_or_greater']= Get('threshold_for_less_or_greater', None)
    initial['threshold_low_for_between']= Get('threshold_low_for_between', None)
    initial['threshold_high_for_between']= Get('threshold_high_for_between', None)
    initial['generate_graph'] = Get('generate_graph', 'F')
    #initial['generate_graph']= str(Get('generate_graph', 'F'))
    element = Get('elements', None)
    if element is None:element = Get('element', 'pcpn')
    initial['element'] = element
    initial['base_temperature'] = Get('base_temperature',None)
    #FIX ME request.POST.get does not return base_temperature and thresholds
    if request.POST:
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
    for lgb in ['l', 'g', 'b']:
        checkbox_vals[lgb + '_selected'] =''
        if initial['less_greater_or_between'] == lgb:
            checkbox_vals[lgb + '_selected'] ='selected'
    return initial, checkbox_vals

def set_sodxtrmts_graph_initial(request):
    initial = {}
    checkbox_vals = {}
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
    initial['graph_generate_graph']= str(Get('graph_generate_graph', 'F'))
    initial['graph_start_month'] = Get('graph_start_month', '01')
    initial['graph_end_month'] = Get('graph_end_month', '02')
    initial['graph_start_year'] = Get('graph_start_year', Get('start_year', 'POR'))
    initial['graph_end_year'] = Get('graph_end_year', Get('end_year', '2013'))
    initial['graph_summary'] = Get('graph_summary', 'mean')
    initial['graph_show_running_mean'] = Get('graph_show_running_mean', 'T')
    initial['graph_running_mean_years'] = Get('graph_running_mean_years', '9')
    initial['graph_plot_incomplete_years'] = Get('graph_plot_incomplete_years', 'F')
    #initial['json_file'] = Get('json_file', None)
    #initial['JSON_URL'] = Get('JSON_URL', '/tmp/')
    for graph_month in ['01','02','03','04','05','06','07','08','09','10','11','12']:
        for mon_type in ['graph_start_month', 'graph_end_month']:
            checkbox_vals[mon_type + '_' + graph_month + '_selected']=''
        if initial[mon_type] == graph_month:
            checkbox_vals[mon_type + '_' + graph_month + '_selected']='selected'
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

def set_station_data_initial(request):
    initial = {}
    checkbox_vals = {}
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
    initial['select_stations_by'] = Get('select_stations_by', 'station_id')
    initial[str(initial['select_stations_by'])] = Get(str(initial['select_stations_by']), WRCCData.AREA_DEFAULTS[initial['select_stations_by']])
    initial['area_type_label'] = WRCCData.DISPLAY_PARAMS[initial['select_stations_by']]
    if initial['select_stations_by'] in ['station_id', 'station_ids', 'basin', 'county', 'county_warning_area', 'climate_division']:
        initial['area_type_label']+='/Name'
    initial['area_type_value'] = Get(str(initial['select_stations_by']), WRCCData.AREA_DEFAULTS[initial['select_stations_by']])
    initial['overlay_state'] = Get('overlay_state', 'nv')
    initial['autofill_list'] = 'US_' + initial['select_stations_by']
    initial['elements'] = Get('elements', 'maxt,mint,pcpn')
    initial['start_date']  = Get('start_date', fourtnight)
    initial['end_date']  = Get('end_date', yesterday)
    initial['show_flags'] = Get('show_flags', 'F')
    initial['show_observation_time'] = Get('show_observation_time', 'F')
    initial['data_format'] = Get('data_format', 'html')
    initial['delimiter'] = Get('delimiter', ',')
    initial['output_file_name'] = Get('output_file_name', 'Output')
    #set the check box values
    for area_type in WRCCData.SEARCH_AREA_FORM_TO_ACIS.keys():
        checkbox_vals[area_type + '_selected'] =''
        if area_type == initial['select_stations_by']:
            checkbox_vals[area_type + '_selected'] ='selected'
    for df in ['clm', 'dlm','xl', 'html']:
        checkbox_vals[df + '_selected'] =''
        if df == initial['data_format']:
            checkbox_vals[df + '_selected'] ='selected'
    for dl in ['comma', 'tab', 'space', 'colon', 'pipe']:
        checkbox_vals[dl + '_selected'] =''
        if dl == initial['delimiter']:
            checkbox_vals[dl + '_selected'] ='selected'
    for bl in ['T','F']:
        for cbv in ['show_flags', 'show_observation_time']:
            checkbox_vals[cbv + '_' + bl + '_selected'] = ''
            if initial[cbv] == bl:
                checkbox_vals[cbv + '_' + bl + '_selected'] = 'selected'
    return initial, checkbox_vals

def set_gridded_data_initial(request):
    initial = {}
    checkbox_vals = {}
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
    initial['select_grid_by'] = Get('select_grid_by', 'location')
    initial[str(initial['select_grid_by'])] = Get(str(initial['select_grid_by']), WRCCData.AREA_DEFAULTS[initial['select_grid_by']])
    initial['area_type_label'] = WRCCData.DISPLAY_PARAMS[initial['select_grid_by']]
    if initial['select_grid_by'] in ['basin', 'county', 'county_warning_area', 'climate_division']:
        initial['area_type_label']+='/Name'
    initial['area_type_value'] = Get(str(initial['select_grid_by']), WRCCData.AREA_DEFAULTS[initial['select_grid_by']])
    initial['overlay_state'] = Get('overlay_state', 'nv')
    initial['autofill_list'] = 'US_' + initial['select_grid_by']
    initial['temporal_resolution'] = Get('temporal_resolution', 'dly')
    initial['elements'] = Get('elements', 'maxt,mint,pcpn')
    initial['start_date']  = Get('start_date', fourtnight)
    initial['end_date']  = Get('end_date', yesterday)
    initial['grid'] = Get('grid', '1')
    initial['data_summary'] = Get('data_summary', 'none')
    initial['temporal_summary'] = Get('temporal_summary', 'mean')
    initial['spatial_summary'] = Get('spatial_summary', 'mean')
    initial['data_format'] = Get('data_format', 'html')
    initial['delimiter'] = Get('delimiter', 'comma')
    initial['output_file_name'] = Get('output_file_name', 'Output')
    #set the check box values
    for area_type in WRCCData.SEARCH_AREA_FORM_TO_ACIS.keys():
        checkbox_vals[area_type + '_selected'] =''
        if area_type == initial['select_grid_by']:
            checkbox_vals[area_type + '_selected'] ='selected'
    for df in ['clm', 'dlm','xl', 'html']:
        checkbox_vals['data_format_' + df + '_selected'] =''
        if df == initial['data_format']:
            checkbox_vals['data_format_' + df + '_selected'] ='selected'
    for dl in ['comma', 'tab', 'space', 'colon', 'pipe']:
        checkbox_vals['delimiter_' + dl + '_selected'] =''
        if dl == initial['delimiter']:
            checkbox_vals['delimiter_' + dl + '_selected'] ='selected'
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
    return initial, checkbox_vals

def set_area_time_series_initial(request):
    initial = {}
    checkbox_vals = {}
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
    initial['select_grid_by'] = Get('select_grid_by', 'location')
    initial[str(initial['select_grid_by'])] = Get(str(initial['select_grid_by']), WRCCData.AREA_DEFAULTS[initial['select_grid_by']])
    initial['area_type_label'] = WRCCData.DISPLAY_PARAMS[initial['select_grid_by']]
    if initial['select_grid_by'] in ['basin', 'county', 'county_warning_area', 'climate_division']:
        initial['area_type_label']+='/Name'
    initial['area_type_value'] = Get(str(initial['select_grid_by']), WRCCData.AREA_DEFAULTS[initial['select_grid_by']])
    initial['overlay_state'] = Get('overlay_state', 'nv')
    initial['autofill_list'] = 'US_' + initial['select_grid_by']
    initial['elements'] = Get('elements', 'maxt,mint,pcpn')
    initial['start_date']  = Get('start_date', fourtnight)
    initial['end_date']  = Get('end_date', yesterday)
    initial['grid'] = Get('grid', '1')
    initial['spatial_summary'] = Get('spatial_summary', 'mean')
    initial['show_running_mean'] = Get('show_running_mean', 'T')
    initial['running_mean_days'] = Get('running_mean_days', '9')
    #set the check box values
    for area_type in WRCCData.SEARCH_AREA_FORM_TO_ACIS.keys():
        checkbox_vals[area_type + '_selected'] =''
        if area_type == initial['select_grid_by']:
            checkbox_vals[area_type + '_selected'] ='selected'
    for st in ['max','min','mean','sum']:
        checkbox_vals['spatial_summary_' + st + '_selected'] =''
        if st == initial['spatial_summary']:
            checkbox_vals['spatial_summary_' + st + '_selected'] ='selected'
    for bl in ['T','F']:
        for cbv in ['show_running_mean']:
            checkbox_vals[cbv + '_' + bl + '_selected'] = ''
            if initial[cbv] == bl:
                checkbox_vals[cbv + '_' + bl + '_selected'] = 'selected'
    return initial, checkbox_vals
