#!/usr/bin/python
#django imports
from django.template import RequestContext
#from django.contrib.auth.models import User
#from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response
#from django.views.generic.list_detail import object_detail, object_list
from django.db.models.query import QuerySet
from django.contrib.localflavor.us.forms import USStateField

#Python imports
import datetime
from collections import defaultdict
import json

import sys, os, stat, re

#My modules
import WRCCUtils
import AcisWS
import WRCCDataApps
import WRCCClasses
import my_data.forms as forms


acis_elements = defaultdict(dict)
acis_elements ={'maxt':{'name':'maxt', 'name_long': 'Maximum Daily Temperature (F)', 'vX':'1'}, \
              'mint':{'name':'mint', 'name_long': 'Minimum Daily Temperature (F)', 'vX':'2'}, \
              'avgt': {'name':'avgt', 'name_long': 'Average Daily Temperature (F)', 'vX':'43'}, \
              'obst':{'name':'obst', 'name_long': 'Observation Time Temperature (F)', 'vX':'3'}, \
              'pcpn': {'name': 'pcpn', 'name_long':'Precipitation (In)', 'vX':'4'}, \
              'snow': {'name': 'snow', 'name_long':'Snowfall (In)', 'vX':'10'}, \
              'snwd': {'name': 'snwd', 'name_long':'Snow Depth (In)', 'vX':'11'}, \
              'cdd': {'name': 'cdd', 'name_long':'Cooling Degree Days (F)', 'vX':'45'}, \
              'hdd': {'name': 'hdd', 'name_long':'Heating Degree Days (F)', 'vX':'45'}, \
              'gdd': {'name': 'gdd', 'name_long':'Growing Degree Days (F)', 'vX':'45'}}
              #bug fix needed for cdd = 44 (WAITING FOR BILL, ALSO IN PLACES BELOW, eg in station_locator_app, also in AcisWS.py)
acis_elements_list = [['maxt','Maximum Daily Temperature (F)'], ['mint','Minimum Daily Temperature (F)'],
                      ['avgt','Average Daily Temperature (F)'], ['obst', 'Observation Time Temperature (F)'], \
                      ['pcpn', 'Precipitation (In)'], ['snow', 'Snowfall (In)'], \
                      ['snwd', 'Snow Depth (In)'], ['cdd', 'Cooling Degree Days (F)'], \
                      ['hdd','Heating Degree Days (F)'], ['gdd', 'Growing Degree Days (F)']]

state_choices = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', \
                'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', \
                'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', \
                'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', \
                'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
STATIC_URL = '/www/apps/csc/dj-projects/my_acis/static/'
MEDIA_URL = '/www/apps/csc/dj-projects/my_acis/media/'

month_names = ['January', 'February', 'March', 'April', 'May', 'June',\
               'July', 'August', 'September', 'October', 'November', 'December']

mon_lens = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def test(request):
    context = {
        'title': 'Southwest Climate Knowledge Exchange',
        'home_page':True
    }
    return render_to_response('my_data/index.html', context, context_instance=RequestContext(request))

def home(request):
    context = {
        'title': 'Southwest Climate Knowledge Exchange',
        'home_page':True
    }
    return render_to_response('my_data/home.html', context, context_instance=RequestContext(request))

def help(request):
    context = {
        'title': 'Help Tool',
        'search_page':True
    }
    return render_to_response('my_data/help/home.html', context, context_instance=RequestContext(request))

def main_map(request):
    context = {
        'title': 'Resources',
        'state_choices': ['AZ', 'CA', 'CO', 'NM', 'NV', 'UT'],
        'main_page':True
    }
    context['json_file'] = 'Network.json'
    return render_to_response('my_data/main_map.html', context, context_instance=RequestContext(request))

#Temp home page fpr Kelly to look at
def main(request):
    context = {
        'title': 'Resources',
        'state_choices': ['AZ', 'CA', 'CO', 'NM', 'NV', 'UT'],
        'main_page':True
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
    day  = str(mon_lens[month -1])
    if len(day) == 1:
        day = '0%s' %day
    context['day'] = day
    context['month'] = month
    context['mon'] = mon
    context['month_name'] = month_names[month - 1]
    context['state'] = state
    context['element'] = element
    return render_to_response('my_data/main_maves.html', context, context_instance=RequestContext(request))

def about_us(request):
    context = {
        'title': 'About Us',
        'intro_page':True
    }
    return render_to_response('my_data/about_us.html', context, context_instance=RequestContext(request))

def who_we_are(request):
    context = {
        'title': 'Who we are',
        'intro_page':True
    }
    return render_to_response('my_data/who_we_are.html', context, context_instance=RequestContext(request))

def what_we_do(request):
    context = {
        'title': 'What we do',
        'intro_page':True
    }
    return render_to_response('my_data/what_we_do.html', context, context_instance=RequestContext(request))

def contact_us(request):
    context = {
        'title': 'Contact Us',
        'intro_page':True
    }
    return render_to_response('my_data/contact_us.html', context, context_instance=RequestContext(request))

def dashboard(request):
    context = {
        'title': 'Monitoring: Climate Dashboard',
        'monitor_page':True
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
        'title': 'Data Portal',
        'data_page':True
    }
    return render_to_response('my_data/data/home.html', context, context_instance=RequestContext(request))

def sw_networks(request):
    context = {
        'title': 'Southwest Networks',
        'data_page':True
    }
    return render_to_response('my_data/data/sw_networks.html', context, context_instance=RequestContext(request))

def data_station(request):
    context = {
        'title': 'Historic Station Data',
        'data_page':True
    }
    context['json_file'] = 'SW_stn.json'
    stn_id = request.GET.get('stn_id', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    elements = request.GET.get('elements', None)
    initial_params_0 = {}
    if stn_id is not None:
        initial_params_0['select_stations_by'] = 'stn_id'
        context['stn_id'] = stn_id
    if start_date is not None:context['start_date'] = start_date
    if end_date is not None:context['end_date'] = end_date
    if elements is not None:initial_params_0['elements'] = str(elements);context['elements'] = elements

    if initial_params_0:
        form0_point = set_as_form(request,'StationDataForm0', init=initial_params_0)
    else:
        form0_point = set_as_form(request,'StationDataForm0')
    context['form0_point'] = form0_point

    if 'form0_point' in request.POST or stn_id is not None:
        if form0_point.is_valid() or stn_id is not None:
            context['form1_point_ready'] = True
            initial_params_1 = {}
            stn_id = request.GET.get('stn_id', None)
            start_date = request.GET.get('start_date', None)
            end_date = request.GET.get('end_date', None)
            elements = request.GET.get('elements', None)
            if stn_id is not None:initial_params_1['station_id'] = str(stn_id);context['stn_id'] = stn_id
            if start_date is not None:initial_params_1['start_date'] = str(start_date);context['start_date'] = start_date
            if end_date is not None:initial_params_1['end_date'] = str(end_date);context['end_date'] = end_date
            if elements is not None:initial_params_1['elements'] = elements;context['elements'] = elements
            if stn_id is not None:
                initial_params_1['select_stations_by'] = 'stn_id'
            else:
                initial_params_1['select_stations_by'] = form0_point.cleaned_data['select_stations_by']

            if 'form0_point' in request.POST:
                if form0_point.cleaned_data['select_stations_by'] == 'bbox':
                    context['need_map_bbox'] = True
                    context['bounding_box'] = '-115,34,-114,35'
            form1_point = forms.StationDataForm1(initial=initial_params_1)
            context['form1_point'] = form1_point

    if 'form1_point' in request.POST:
        form1_point = set_as_form(request,'StationDataForm1')
        context['form1_point'] = form1_point
        context['form1_point_ready'] = True
        stn_id = request.GET.get('stn_id', None)
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        elements = request.GET.get('elements', None)
        if stn_id is not None:context['stn_id'] = stn_id
        if start_date is not None:context['start_date'] = start_date
        if end_date is not None:context['end_date'] = end_date
        if elements is not None:context['elements'] = elements

        if form1_point.is_valid():
            if 'show_flags' in form1_point.cleaned_data.keys() and form1_point.cleaned_data['show_flags'] == 'T':
                context['show_flags'] = True
                show_flags = 'T'
            else:
                show_flags = 'F'
            if 'show_observation_time' in form1_point.cleaned_data.keys() and form1_point.cleaned_data['show_observation_time'] == 'T':
                context['show_observation_time'] = True
                show_observation_time = 'T'
            else:
                show_observation_time = 'F'
            if form1_point.cleaned_data['select_stations_by'] == 'bbox':
                context['need_map_bbox'] = True
                context['bounding_box'] = form1_point.cleaned_data['bounding_box']
            context['cleaned'] = form1_point.cleaned_data
            #Check if data request is large,
            #if so, gather params and ask user for name and e-mail and notify user that request will be processed offline
            if form1_point.cleaned_data['start_date'].lower() == 'por':
                s_date = datetime.date(1900,01,01)
            else:
                s_date = datetime.date(int(form1_point.cleaned_data['start_date'][0:4]), int(form1_point.cleaned_data['start_date'][4:6]),int(form1_point.cleaned_data['start_date'][6:8]))
            if form1_point.cleaned_data['end_date'].lower() == 'por':
                e_date = datetime.date.today()
            else:
                e_date = datetime.date(int(form1_point.cleaned_data['end_date'][0:4]), int(form1_point.cleaned_data['end_date'][4:6]),int(form1_point.cleaned_data['end_date'][6:8]))
            days = (e_date - s_date).days
            #if time range > 1 year or user requests data for more than 1 station, large request via ftp
            if days > 366 and 'station_id' not in form1_point.cleaned_data.keys() and 'station_ids' not in form1_point.cleaned_data.keys():
                context['large_request'] = \
                'At the moment we do not support data requests that exceed 1 year for multiple station. Please limit your request to one station at a time or a date range of one year or less. We will support larger requests in the near future. Thank you for your patience!'

                '''
                context['form3_point_ready'] = True
                context['large_request'] = 'You requested a large amount of data.Please enter your name and e-mail address.We will notify you once your request has been processed and your data is availiable on our ftp server.'
                initial_params_2 = form1_point.cleaned_data
                #keep MultiElements format and MultiStnField format
                initial_params_2['elements'] = ','.join(initial_params_2['elements'])
                if 'station_ids' in initial_params_2.keys():
                    initial_params_2['station_ids'] = ','.join([str(stn) for stn in initial_params_2['station_ids']])
                form3_point = forms.StationDataForm3(initial=initial_params_2)
                context['form3_point'] = form3_point
                '''
                return render_to_response('my_data/data/station/home.html', context, context_instance=RequestContext(request))
            elif 'station_ids' in form1_point.cleaned_data.keys() and len(form1_point.cleaned_data['station_ids']) > 20:
                context['large_request'] ='At the moment we do not support data requests that exceed 50 stations. Please limit your request to one station at a time or a date range of one year or less. We will support larger requests in the near future. Thank you for your patience!'
                '''
                context['form3_point_ready'] = True
                context['large_request'] = 'You requested a large amount of data. Please enter your name and e-mail address.We will notify you once your request has been processed and your data is availiable on our ftp server.'
                initial_params_2 = form1_point.cleaned_data
                #keep MultiElements format and MultiStnField format
                initial_params_2['elements'] = ','.join(initial_params_2['elements'])
                if 'station_ids' in initial_params_2.keys():
                    initial_params_2['station_ids'] = ','.join([str(stn) for stn in initial_params_2['station_ids']])
                form3_point = forms.StationDataForm3(initial=initial_params_2)
                context['form3_point'] = form3_point
                '''
                return render_to_response('my_data/data/station/home.html', context, context_instance=RequestContext(request))
            else:
                resultsdict = AcisWS.get_station_data(form1_point.cleaned_data, 'sodlist_web')
                context['results'] = resultsdict
                # If request successful, get params for link to apps page
                if 'stn_data' in resultsdict.keys() and resultsdict['stn_data']:
                    context['elements'] = ','.join(form1_point.cleaned_data['elements'])
                    context['start_date'] = form1_point.cleaned_data['start_date']
                    context['end_date'] = form1_point.cleaned_data['end_date']
                    if 'station_id' in form1_point.cleaned_data.keys():
                        context['stn_id']= form1_point.cleaned_data['station_id']
                        context['link_to_mon_aves'] = True
                        if 'stn_ids' in resultsdict.keys() and resultsdict['stn_ids'][0][0].split(' ')[1] == 'COOP':
                            context['link_to_metagraph'] = True
                context['stn_idx'] = [i for i in range(len(resultsdict['stn_ids']))] #for html looping
                if 'delimiter' in form1_point.cleaned_data.keys():
                    if str(form1_point.cleaned_data['delimiter']) == 'comma':delimiter = ','
                    if str(form1_point.cleaned_data['delimiter']) == 'tab':delimiter = ' '
                    if str(form1_point.cleaned_data['delimiter']) == 'colon':delimiter = ':'
                    if str(form1_point.cleaned_data['delimiter']) == 'space':delimiter = ' '
                    if str(form1_point.cleaned_data['delimiter']) == 'pipe':delimiter = '|'
                else:
                    if form1_point.cleaned_data['data_format'] == 'json':
                        delimiter = None
                        context['json'] = True
                    else:
                        delimiter = ' '
                context['delim'] = form1_point.cleaned_data['delimiter']
                context['delimiter'] =  delimiter
                #Output formats
                select_stations_by = form1_point.cleaned_data['select_stations_by']
                if select_stations_by == 'stnid':
                    file_info =['StnId', form1_point.cleaned_data['station_id']]
                    context['by_type'] = 'Individual Station: %s' %str(form1_point.cleaned_data['station_id'])
                elif select_stations_by == 'stn_id':
                    file_info =['StnId',',',form1_point.cleaned_data['station_id']]
                    context['by_type'] = 'Individual Station: %s' %str(form1_point.cleaned_data['station_id'])
                elif select_stations_by == 'stnids':
                    file_info = ['Multi','Stations']
                    stn_list = []
                    stn_tuple = ', '.join(form1_point.cleaned_data['station_ids'])
                    context['by_type'] = 'Multiple Stations: %s' %stn_tuple
                elif select_stations_by == 'county':
                    file_info =['county', form1_point.cleaned_data['county']]
                    context['by_type'] = 'County: %s' %str(form1_point.cleaned_data['county'])
                elif select_stations_by == 'climdiv':
                    file_info =['climdiv', form1_point.cleaned_data['climate_division']]
                    context['by_type'] = 'Climate Division: %s' %str(form1_point.cleaned_data['climate_division'])
                elif select_stations_by == 'cwa':
                    file_info =['cwa', form1_point.cleaned_data['county_warning_area']]
                    context['by_type'] = 'Couny Warning Area: %s' %str(form1_point.cleaned_data['county_warning_area'])
                elif select_stations_by == 'basin':
                    file_info =['basin', form1_point.cleaned_data['basin']]
                    context['by_type'] = 'Basin: %s' %str(form1_point.cleaned_data['basin'])
                elif select_stations_by == 'state':
                    file_info =['state', form1_point.cleaned_data['state']]
                    context['by_type'] = 'State: %s' %str(form1_point.cleaned_data['state'])
                elif select_stations_by == 'bbox':
                    file_info =['bbox', re.sub(',','_',form1_point.cleaned_data['bounding_box'])]
                    context['by_type'] = 'Bounding Box: %s' %str(form1_point.cleaned_data['bounding_box'])
                else:
                    file_info =['Undefined','export']
                context['file_info'] = file_info

                if form1_point.cleaned_data['data_format'] == 'dlm':
                    return WRCCUtils.write_point_data_to_file(resultsdict['stn_data'], resultsdict['dates'], resultsdict['stn_names'], resultsdict['stn_ids'], resultsdict['elements'],delimiter, 'dat', request=request, file_info=file_info, show_flags=show_flags, show_observation_time=show_observation_time)
                elif form1_point.cleaned_data['data_format'] == 'clm':
                    return WRCCUtils.write_point_data_to_file(resultsdict['stn_data'], resultsdict['dates'], resultsdict['stn_names'], resultsdict['stn_ids'], resultsdict['elements'],delimiter, 'txt', request=request, file_info=file_info, show_flags=show_flags, show_observation_time=show_observation_time)
                elif form1_point.cleaned_data['data_format'] == 'xl':
                    return WRCCUtils.write_point_data_to_file(resultsdict['stn_data'], resultsdict['dates'], resultsdict['stn_names'], resultsdict['stn_ids'], resultsdict['elements'],delimiter, 'xls', request=request, file_info=file_info, show_flags=show_flags, show_observation_time=show_observation_time)
                else:
                    return render_to_response('my_data/data/station/home.html', context, context_instance=RequestContext(request))
    if 'form3_point' in request.POST:
        form3_point = set_as_form(request,'StationDataForm3')
        context['form3_point'] = form3_point
        context['form3_point_ready'] = True
        if form3_point.is_valid():
            context['hide_form3'] = True
            user_name = form3_point.cleaned_data['user_name']
            time_stamp = datetime.datetime.now().strftime('_%Y_%m_%d_%H_%M_%S')
            f = '/tmp/data_requests/' + user_name + time_stamp + '_params.json'
            context['json'] = f
            #check if directory /tmp/data_requests exists, else create it
            dr = os.path.dirname(f)
            try:
                os.stat(dr)
            except:
                os.mkdir(dr)
            with open( f, 'w+') as j_file:
                json.dump(form3_point.cleaned_data, j_file)
            mode = os.stat(f).st_mode
            os.chmod(f, mode | stat.S_IWOTH)
            context['user_info'] = 'You will receive an email from csc-data-request@dri.edu with instructions when the data request has been processed. You provided following e-mail address: %s' % (form3_point.cleaned_data['email'])
        else:
            context['user_info'] ='Form not valid'
            context['invalid_form'] = form3_point
        return render_to_response('my_data/data/station/home.html', context, context_instance=RequestContext(request))

    return render_to_response('my_data/data/station/home.html', context, context_instance=RequestContext(request))

def data_gridded(request):
    context = {
        'title': 'Gridded/Modeled Data',
        'data_page':True
    }

    elements = request.GET.get('elements', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    elements = request.GET.get('elements', None)
    bbox = request.GET.get('bbox', None)
    state = request.GET.get('state', None)
    loc = request.GET.get('loc', None)
    grid = request.GET.get('grid', None)
    data_summary = request.GET.get('data_summary', None)
    temporal_resolution = request.GET.get('temporal_resolution', None)
    initial_1 = {}
    if temporal_resolution is not None:context['temporal_resolution'] = temporal_resolution;initial_1['temporal_resolution'] = temporal_resolution
    if data_summary is not None:context['data_summary'] = data_summary;initial_1['data_summary'] = data_summary
    if start_date is not None:context['start_date'] = start_date;initial_1['start_date'] = start_date
    if end_date is not None:context['end_date'] = end_date;initial_1['end_date'] = end_date
    if bbox is not None:
        context['bbox'] = bbox;initial_1['bounding_box'] = bbox
        context['select_grid_by'] = 'bbox';initial_1['select_grid_by'] = 'bbox'
    if state is not None:
        context['state'] = state;initial_1['state'] = state
        context['select_grid_by'] = 'state';initial_1['select_grid_by'] = 'state'
    if loc is not None:
        context['location'] = loc;initial_1['location'] = loc
        context['select_grid_by'] = 'point';initial_1['select_grid_by'] = 'point'
        context['lat'] = loc.split(',')[0]; context['lon'] = loc.split(',')[1]
        context['map_loc'] = loc
    else:
        context['lat'] = '39'; context['lon'] = '-119'
        context['map_loc'] = '-119,39'

    if elements is not None:
        context['elements'] = elements;initial_1['elements'] = elements
    if temporal_resolution is not None:
        context['temporal_resolution'] = elements;initial_1['temporal_resolution'] = temporal_resolution
    if loc is not None or state is not None or bbox is not None:
        context['hide_form_0'] = True
        context['form1_grid_ready'] = True
        form1_grid = forms.GridDataForm1(initial=initial_1)
        context['form1_grid'] = form1_grid
    else:
        form0_grid = set_as_form(request,'GridDataForm0')
        context['form0_grid'] = form0_grid

    if 'form0_grid' in request.POST:
        if form0_grid.is_valid():
            if form0_grid.cleaned_data['temporal_resolution'] in ['mly', 'yly']:
                context['prism_flag'] = True # flag for correct element docu
            context['temporal_resolution'] = form0_grid.cleaned_data['temporal_resolution']
            context['form1_grid_ready'] = True
            initial_1 = {
                'select_grid_by':form0_grid.cleaned_data['select_grid_by'],
                'temporal_resolution':form0_grid.cleaned_data['temporal_resolution'],
                'data_summary':form0_grid.cleaned_data['data_summary']
            }
            if initial_1['select_grid_by'] == 'point':
                context['need_map'] = True
                if loc is not None:
                    context['lat'] = loc.split(',')[0]; context['lon'] = loc.split(',')[1]
                    context['map_loc'] = loc
                else:
                    context['lat'] = '39'; context['lon'] = '-119'
                    context['map_loc'] = '-119,39'
            if initial_1['select_grid_by'] == 'bbox':
                context['need_map_bbox'] = True
                bounding_box = request.GET.get('bounding_box', None)
                if bounding_box is not None:
                    context['bounding_box'] = bounding_box
                else:
                    context['bounding_box'] = '-115,34,-114,35'

            form1_grid = forms.GridDataForm1(initial=initial_1)
            context['form1_grid'] = form1_grid

    if 'form1_grid' in request.POST:
        form1_grid = set_as_form(request,'GridDataForm1')
        context['form1_grid'] = form1_grid
        context['form1_grid_ready'] = True
        if form1_grid.is_valid():
            context['temporal_resolution'] = form1_grid.cleaned_data['temporal_resolution']
            context['data_summary'] = form1_grid.cleaned_data['data_summary']
            el_list = form1_grid.cleaned_data['elements']
            context['elements'] =  el_list
            #Check if data request is large,
            #if so, gather params and ask user for name and e-mail and notify user that request will be processed offline
            s_date = datetime.date(int(form1_grid.cleaned_data['start_date'][0:4]), int(form1_grid.cleaned_data['start_date'][4:6]), \
            int(form1_grid.cleaned_data['start_date'][6:8]))
            e_date = datetime.date(int(form1_grid.cleaned_data['end_date'][0:4]), int(form1_grid.cleaned_data['end_date'][4:6]), \
            int(form1_grid.cleaned_data['end_date'][6:8]))
            days = (e_date - s_date).days
            #if time range > 1 day and user requests data for more than 1 station, large request via ftp
            #if (days > 1 and  'location' not in form1_grid.cleaned_data.keys()) or (days > 366 and 'location' in form1_grid.cleaned_data.keys()):

            if ('data_summary' in form1_grid.cleaned_data.keys() and form1_grid.cleaned_data['data_summary'] == 'none' and form1_grid.cleaned_data['temporal_resolution'] == 'dly') or ('data_summary' not in form1_grid.cleaned_data.keys()):
                if (days > 7 and  'location' not in form1_grid.cleaned_data.keys()):
                    context['large_request'] = \
                    'At the moment we do not support data requests that exceed 7 days for multiple station. Please limit your request to one grid point at a time or a date range of one week or less. Alternatively, you could summarize your data by using the data summary option. We will support larger requests in the near future. Thank you for your patience!'
                    '''
                    context['form3_grid_ready'] = True
                    context['large_request'] = \
                    'You requested a large amount of data. Please enter your name and e-mail address. We will notify you once your request has been processed and your data is availiable on our ftp server.'
                    initial_params_2 = form1_grid.cleaned_data
                    #keep MultiElements format and MultiStnField format
                    initial_params_2['elements'] = ','.join(initial_params_2['elements'])
                    form3_grid = forms.GridDataForm3(initial=initial_params_2)
                    context['form3_grid'] = form3_grid
                    '''
                    return render_to_response('my_data/data/gridded/home.html', context, context_instance=RequestContext(request))

            if 'location' in form1_grid.cleaned_data.keys():
                location = form1_grid.cleaned_data['location']
                context['need_map'] = True
                context['map_loc'] = location
                context['lat'] = location.split(',')[1]
                context['lon'] = location.split(',')[0]
            elif 'bounding_box' in form1_grid.cleaned_data.keys():
                context['need_map_bbox'] = True
                bounding_box = form1_grid.cleaned_data['bounding_box']
                context['bounding_box'] = bounding_box
            elif 'state' in form1_grid.cleaned_data.keys():
                state = form1_grid.cleaned_data['state']
                context['state'] = state
            context['start_date'] = form1_grid.cleaned_data['start_date'];start_date= form1_grid.cleaned_data['start_date']
            context['end_date'] = form1_grid.cleaned_data['end_date'];end_date= form1_grid.cleaned_data['end_date']
            context['element'] = str(form1_grid.cleaned_data['elements'][0])
            elems_long = []
            element_list = form1_grid.cleaned_data['elements']
            context['element_list'] = element_list
            for el in element_list:
                elems_long.append(acis_elements[el]['name_long'])
            context['elems_long'] = elems_long
            context['grid'] = str(form1_grid.cleaned_data['grid']);grid=str(form1_grid.cleaned_data['grid'])

            #Generate Data
            form_input = form1_grid.cleaned_data
            if str(form1_grid.cleaned_data['grid']) == '21':
                #PRISM data need to convert elements!!
                prism_elements = []
                for el in form1_grid.cleaned_data['elements']:
                    prism_elements.append('%s_%s' %(str(form1_grid.cleaned_data['temporal_resolution']), str(el)))
                form_input['elements'] = prism_elements
            req = AcisWS.get_grid_data(form_input, 'griddata_web')

            if 'visualize' in form1_grid.cleaned_data.keys() and form1_grid.cleaned_data['visualize'] == 'T':
                #Generate figures for each element, store in figure files
                figure_files = []
                image = dict(type='png',proj='lcc',interp='cspline',
                    overlays=['state','county:0.5:black'],width=500, height=400)
                params = {
                    'image':image , 'output':'json', 'grid': grid,
                    'sdate': start_date,
                    'edate': end_date,
                    }
                if 'state' in form1_grid.cleaned_data.keys():params['state']= state
                if 'bounding_box' in form1_grid.cleaned_data.keys():params['bbox']= bounding_box
                #Loop over element and generate figure
                for el_idx, elem in enumerate(element_list):
                    '''
                    if 'smry' in req.keys() and len(req['smry']) > el_idx:
                        params['data'] = {'smry':[req['smry'][el_idx]]}
                    '''
                    if elem in ['pcpn', 'snow', 'snwd']:
                        if form1_grid.cleaned_data['data_summary'] != 'sum':
                            params['image']['levels'] =[0,0.1, 0.2, 0.5, 0.7, 1.0, 2.0, 3.0, 4.0, 5.0]
                        else:
                            params['image']['levels'] =[1, 2, 3, 4,5,6,7,8,9,10,15,20,30]
                        params['image']['cmap'] = 'Spectral'
                    elif elem in ['maxt', 'avgt']:
                        if form1_grid.cleaned_data['data_summary'] != 'sum':
                            params['image']['levels'] =[-50,-20,-10,0,10,20,30,40,50,60,70,80,90,100,120]
                        params['image']['cmap'] = 'jet'
                    elif elem == 'mint':
                        if form1_grid.cleaned_data['data_summary'] != 'sum':
                            params['image']['levels'] =[-70,-50,-20,0,10,20,30,40,50,60,70,80,90]
                        params['image']['cmap'] = 'jet'
                    elif elem in ['hdd','cdd', 'gdd']:
                        if form1_grid.cleaned_data['data_summary'] != 'sum':
                            params['image']['levels'] =[0, 10, 20, 30, 50, 70,80,90,100]
                        params['image']['cmap'] = 'jet'
                    params['elems'] = [{'name':elem}]
                    fig = WRCCClasses.GridFigure(params)
                    results = fig.get_grid()
                    time_stamp = datetime.datetime.now().strftime('%Y%m_%d_%H_%M_%S')
                    figure_file = 'acis_map_' + time_stamp + '.png'
                    file_path_big ='/tmp/' + figure_file
                    fig.build_figure(results, file_path_big)
                    figure_files.append(figure_file)
                context['figure_files'] = figure_files
            #format data
            if form1_grid.cleaned_data['data_format'] == 'json':
                delimiter = None
                context['json'] = True
                context['grid_data']  = req
            else:
                data = WRCCUtils.format_grid_data(req, form1_grid.cleaned_data)
                context['grid_data'] = data

            #Link to relevant apps
            if 'elements' in form1_grid.cleaned_data.keys() and len(form1_grid.cleaned_data['elements'])==1:
                if req or data:
                    if 'location' in form1_grid.cleaned_data.keys():
                        if str(form1_grid.cleaned_data['elements'][0]) in ['maxt', 'mint', 'avgt', 'gdd', 'hdd', 'cdd', 'pcpn']:
                            context['link_to_gp_ts'] = True
                            context['lat'] = form1_grid.cleaned_data['location'].split(',')[1]
                            context['lon'] = form1_grid.cleaned_data['location'].split(',')[0]
                    else:
                        if str(form1_grid.cleaned_data['elements'][0]) in ['maxt', 'mint', 'avgt', 'gdd', 'hdd', 'cdd', 'pcpn']:
                            context['link_to_clim_sum_map'] = True
                            if 'bounding_box' in form1_grid.cleaned_data.keys():
                                context['bounding_box'] = form1_grid.cleaned_data['bounding_box']
                            else:
                                context['state'] = form1_grid.cleaned_data['state']

            if 'delimiter' in form1_grid.cleaned_data.keys():
                if str(form1_grid.cleaned_data['delimiter']) == 'comma':delimiter = ','
                if str(form1_grid.cleaned_data['delimiter']) == 'tab':delimiter = ' '
                if str(form1_grid.cleaned_data['delimiter']) == 'colon':delimiter = ':'
                if str(form1_grid.cleaned_data['delimiter']) == 'space':delimiter = ' '
                if str(form1_grid.cleaned_data['delimiter']) == 'pipe':delimiter = '|'
            else:
                delimiter = ' '
            context['delimiter'] = delimiter

            #Output formats
            select_grid_by = form1_grid.cleaned_data['select_grid_by']
            if select_grid_by == 'point':file_info =['location', re.sub(',','_',form1_grid.cleaned_data['location'])]
            if select_grid_by == 'state':file_info = ['state', form1_grid.cleaned_data['state']]
            if select_grid_by == 'bbox':file_info =['bounding_box', re.sub(',','_',form1_grid.cleaned_data['bounding_box'])]
            context['file_info'] = file_info
            if form1_grid.cleaned_data['data_format'] == 'dlm':
                #return export_to_file_grid(request, data, el_list, file_info, delimiter, 'dat')
                return WRCCUtils.write_griddata_to_file(data, el_list,delimiter,'dat', request=request,file_info=file_info)
            elif form1_grid.cleaned_data['data_format'] == 'clm':
                #return export_to_file_grid(request, data, el_list, file_info, delimiter, 'txt')
                return WRCCUtils.write_griddata_to_file(data, el_list,delimiter,'txt', request=request,file_info=file_info)

            elif form1_grid.cleaned_data['data_format'] == 'xl':
                #return export_to_file_grid(request, data, el_list, file_info, delimiter, 'xls')
                return WRCCUtils.write_griddata_to_file(data, el_list,delimiter,'xls', request=request,file_info=file_info)
            else:
                return render_to_response('my_data/data/gridded/home.html', context, context_instance=RequestContext(request))

    if 'form3_grid' in request.POST:
        form3_grid = set_as_form(request,'GridDataForm3')
        context['form3_grid'] = form3_grid
        context['form3_grid_ready'] = True
        if form3_grid.is_valid():
            context['hide_form3'] = True
            user_name = form3_grid.cleaned_data['user_name']
            time_stamp = datetime.datetime.now().strftime('_%Y_%m_%d_%H_%M_%S')
            f = '/tmp/data_requests/' + user_name + time_stamp + '_params.json'
            context['json'] = f
            #check if directory /tmp/data_requests exists, else create it
            dr = os.path.dirname(f)
            try:
                os.stat(dr)
            except:
                os.mkdir(dr)
            with open(f, 'w+') as j_file:
                json.dump(form3_grid.cleaned_data, j_file)
            mode = os.stat(f).st_mode
            os.chmod(f, mode | stat.S_IWOTH)
            context['user_info'] = 'You will receive an email from csc-data-request@dri.edu with instructions when the data request has been processed. You provided following e-mail address: %s' % (form3_grid.cleaned_data['email'])
        return render_to_response('my_data/data/gridded/home.html', context, context_instance=RequestContext(request))

    return render_to_response('my_data/data/gridded/home.html', context, context_instance=RequestContext(request))



def apps_home(request):
    context = {
        'title': 'Tools/Applications',
        'state_choices': ['AZ', 'CA', 'CO', 'NM', 'NV', 'UT'],
        'apps_page':True
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
    context['month_name'] = month_names[month - 1]
    context['state'] = state
    context['element'] = element
    return render_to_response('my_data/apps/home.html', context, context_instance=RequestContext(request))

def apps_station(request):
    context = {
        'title': 'Station Data Tools',
        'state_choices': ['AZ', 'CA', 'CO', 'NM', 'NV', 'UT'],
        'apps_page':True
        }
    return render_to_response('my_data/apps/station/home.html', context, context_instance=RequestContext(request))

def apps_gridded(request):
    context = {
        'title': 'Gridded Data Tools',
        'apps_page':True
        }
    return render_to_response('my_data/apps/gridded/home.html', context, context_instance=RequestContext(request))

def apps_gis(request):
    context = {
        'title': 'Geospatial Data Tools',
        'apps_page':True
        }
    return render_to_response('my_data/apps/gis/home.html', context, context_instance=RequestContext(request))

def swcke_station_apps(request):
    context = {
        'title': 'Historic Station Data Tools',
        'state_choices': ['AZ', 'CA', 'CO', 'NM', 'NV', 'UT'],
        'apps_page':True

    }
    stn_id = request.GET.get('stn_id', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    elements = request.GET.get('elements', None)
    if stn_id is not None:context['stn_id'] = stn_id
    if start_date is not None:context['start_date'] = start_date
    if end_date is not None:context['end_date'] = end_date
    if elements is not None:context['elements'] = elements

    return render_to_response('my_data/apps/swcke_station_apps.html', context, context_instance=RequestContext(request))

def metagraph(request):
    context = {
        'title': 'Station Metadata Graphics',
        'apps_page':True
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
            station_meta = {}
            params = {'sids':str(form_meta.cleaned_data['station_id'])}
            meta_request = AcisWS.StnMeta(params)
            #meta_request = WRCCClasses.DataJob('StnMeta', params).make_data_call()
            if 'meta' in meta_request.keys():
                if len(meta_request['meta']) == 0:
                    station_meta['error'] = 'No meta data found for station: %s.' %stn_id
                else:
                    for key, val in meta_request['meta'][0].iteritems():
                        if key == 'sids':
                            sid_list = []
                            for sid in val:
                                sid_l = sid.split()
                                if sid_l[1] == '2':
                                    station_meta['coop_id'] = str(sid_l[0])
                                sid_list.append(sid.encode('ascii', 'ignore'))
                            station_meta['sids'] = sid_list
                        else:
                            station_meta[key] = str(val)
            else:
                if 'error' in meta_request.keys():
                    station_meta['error'] = meta_request['error']
                else:
                    station_meta['error'] = 'No meta data found for station: %s.' %stn_id
            context['station_meta'] = station_meta
            #Call perl script that generates gif graphs
            #FIX ME! Should be able to call it from html:
            #<img src="{{MEDIA_URL}}perl-scripts/csc_cliMETAgraph.pl?{{station_id}}">
            time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_')
            context['time_stamp'] = time_stamp
            perl_out, perl_err = run_external_script("perl %sperl-scripts/csc_cliMETAgraph.pl %s %s" %(MEDIA_URL, str(form_meta.cleaned_data['station_id']), time_stamp))
            context['perl_err'] = perl_err
            context['perl_out'] = perl_out
        else:
            stn_id = None

    return render_to_response('my_data/apps/station/metagraph.html', context, context_instance=RequestContext(request))

def monthly_aves(request):
    context = {
        'title': 'Monthly Averages',
        'apps_page':True,
        'acis_elements':dict(acis_elements)
    }
    stn_id = request.GET.get('stn_id', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    elements = request.GET.get('elements', None)
    initial = {}
    if stn_id is not None:initial['stn_id']= str(stn_id);context['stn_id'] = stn_id
    if start_date is not None:initial['start_date']= str(start_date);context['start_date'] = start_date
    if end_date is not None:initial['end_date']= str(end_date);context['end_date'] = end_date
    if elements is not None:initial['elements']= elements;context['elements'] = elements
    if initial:
        form_graphs = set_as_form(request,'MonthlyAveragesForm', init=initial)
    else:
        form_graphs = set_as_form(request,'MonthlyAveragesForm')
    context['form_graphs'] = form_graphs
    if 'form_graphs' in request.POST:
        form_graphs = set_as_form(request,'MonthlyAveragesForm')
        context['form_graphs']  = form_graphs
        if form_graphs.is_valid():
            s_date = str(form_graphs.cleaned_data['start_date'])
            e_date = str(form_graphs.cleaned_data['end_date'])
            stn_id = form_graphs.cleaned_data['station_id']
            context['stn_id'] = stn_id
            context['start_date'] = s_date
            context['end_date'] = e_date
            context['elems'] = ','.join(form_graphs.cleaned_data['elements'])
            params = dict(sid=stn_id, sdate=s_date, edate=e_date, \
            meta='valid_daterange,name,state,sids,ll,elev,uid,county,climdiv', \
            elems=[dict(name=el, groupby="year")for el in form_graphs.cleaned_data['elements']])
            monthly_aves = {}
            results = [{} for k in form_graphs.cleaned_data['elements']]
            #results = defaultdict(dict)

            #req = WRCCClasses.DataJob('StnData', params).make_data_call()
            req = AcisWS.StnData(params)
            if not req:
                context['error']= 'Bad Data request for parameters: %s' %str(params)
            elif 'data' not in req.keys() or 'meta' not in req.keys():
                context['error']= 'Bad Data request for parameters: %s' %str(params)
            else:
                context['raw_data'] = req['data']

                try:
                    monthly_aves = WRCCDataApps.monthly_aves(req, form_graphs.cleaned_data['elements'])
                    context['averaged_data'] = dict(monthly_aves)
                except:
                    pass

                for el_idx, el in enumerate(form_graphs.cleaned_data['elements']):
                    el_strip = re.sub(r'(\d+)(\d+)', '', el)   #strip digits from gddxx, hddxx, cddxx
                    b = el[-2:len(el)]
                    try:
                        base_temp = int(b)
                    except:
                        if b == 'dd' and el in ['hdd', 'cdd']:
                            base_temp = '65'
                        elif b == 'dd' and el == 'gdd':
                            base_temp = '50'

                    if el_strip == 'pcpn':
                        results[el_idx] = {'element_long': 'Total Rainfall', 'units':'in'}
                    elif el_strip == 'snow':
                        results[el_idx] = {'element_long': 'Total Snowfall', 'units':'in'}
                    elif el_strip == 'maxt':
                        results[el_idx] = {'element_long': 'Maximum Temperature', 'units':'F'}
                    elif el_strip == 'mint':
                        results[el_idx] = {'element_long': 'Minimum Temperature', 'units':'F'}
                    elif el_strip == 'avgt':
                        results[el_idx] = {'element_long': 'Mean Temperature', 'units':'F'}
                    elif el_strip == 'obst':
                        results[el_idx] = {'element_long': 'Observation Time Temperature', 'units':'F'}
                    elif el_strip == 'snwd':
                        results[el_idx] = {'element_long': 'Snow Depth', 'units':'in'}
                    elif el_strip == 'cdd':
                        results[el_idx] = {'element_long': 'Growing Degree Days, Base Temp %s' %base_temp, 'units':'days'}
                    elif el_strip == 'hdd':
                        results[el_idx] = {'element_long': 'Heading Degree Days, Base Temp %s' %base_temp, 'units':'days'}
                    elif el_strip == 'gdd':
                        results[el_idx] = {'element_long': 'Cooling Degree Days, Base Temp %s' %base_temp, 'units':'days'}
                    else:
                        results[el_idx] = {'element_long':str(el)}
                    results[el_idx]['element'] = str(el)
                    results[el_idx]['stn_id']= str(form_graphs.cleaned_data['station_id'])
                    if form_graphs.cleaned_data['start_date'].lower() == 'por':
                        if len(req['meta']['valid_daterange'][el_idx]) == 2:
                            results[el_idx]['record_start'] = str(req['meta']['valid_daterange'][el_idx][0])
                        else:
                            #no valid daterange found
                            results[el_idx]['record_start'] = ['0000-00-00']
                    else:
                        results[el_idx]['record_start'] = '%s-%s-%s' % (s_date[0:4], s_date[4:6], s_date[6:8])
                    if form_graphs.cleaned_data['end_date'].lower() == 'por':
                        if len(req['meta']['valid_daterange'][el_idx]) == 2:
                            results[el_idx]['record_end'] = str(req['meta']['valid_daterange'][el_idx][1])
                        else:
                            results[el_idx]['record_end'] = ['0000-00-00']
                    else:
                        results[el_idx]['record_end'] = '%s-%s-%s' % (e_date[0:4], e_date[4:6], e_date[6:8])
                    results[el_idx]['data'] = monthly_aves[el]
                    if 'meta' in req.keys():
                        results[el_idx]['stn_name'] = str(req['meta']['name'])
                        results[el_idx]['state'] = str(req['meta']['state'])
                if 'meta' in req.keys():
                    Meta = WRCCUtils.format_stn_meta(req['meta'])
                    #format meta data
                    elements = ', '.join(form_graphs.cleaned_data['elements'])
                    valid_dr = []
                    for idx, el in enumerate(form_graphs.cleaned_data['elements']):
                        try:
                            valid_dr.append('%s: %s - %s ' %(str(el),str(Meta['valid_daterange'][idx][0]),str(Meta['valid_daterange'][idx][1])))
                        except:
                            valid_dr.append(str(el))

                    meta = ['Station Name: ' +  Meta['name'],
                            'Elements :' + elements,
                            'Valid Daterange: ' + ', '.join(valid_dr),
                            'Lat, Lon: ' +  str(Meta['ll']),
                            'Elevation :' +  Meta['elev'],
                            'State: ' + Meta['state'],
                            'County: ' +  Meta['county'],
                            'Climate Division: ' + Meta['climdiv'],
                            'Unique Identifyer: ' + Meta['uid']
                        ]
                    context['meta'] = meta
                context['results'] = results
                #save to json file (necessary since we can't pass list, dicts to js via hidden vars)
                #double quotes needed for jquery json.load
                results_json = str(results).replace("\'", "\"")
                time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                json_file = '%s_monthly_aves_%s_%s_%s.json' \
                %(time_stamp, str(form_graphs.cleaned_data['station_id']), s_date, e_date)
                context['json_file'] = json_file
                f = open('/tmp/%s' %(json_file),'w+')
                f.write(results_json)
                f.close()

        #else:
        #    stn_id = None

    return render_to_response('my_data/apps/station/monthly_aves.html', context, context_instance=RequestContext(request))

def clim_sum_maps(request):
    context = {
        'title': 'Climate Summary Maps',
        'apps_page':True
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

        if form0.is_valid():
            context['form1_ready'] = True
            context['select_grid_by'] = form0.cleaned_data['select_grid_by']
            if form0.cleaned_data['select_grid_by'] == 'bbox':
                bounding_box = request.GET.get('bounding_box', None)
                if bounding_box is not None:
                    context['bounding_box'] = bounding_box
                else:
                    context['bounding_box'] = '-115,34,-114,35'
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
        if form1.is_valid():
            image = dict(type='png',proj='lcc',interp='cspline',cmap='jet',
                    overlays=['state','county:0.5:black'],width=500, height=400)
            params = {'image':image , 'output':'json', 'grid': form1.cleaned_data['grid'], \
                    'sdate': form1.cleaned_data['start_date'], \
                    'edate': form1.cleaned_data['end_date']}
            if form1.cleaned_data['element'] == 'gddxx':
                elem = 'gdd%s' %str(form1.cleaned_data['base_temperature_gddxx'])
                context['elems_long'] = acis_elements['gdd']['name_long']
                context['base_temp'] = str(form1.cleaned_data['base_temperature_gddxx'])
            elif form1.cleaned_data['element'] == 'hddxx':
                elem = 'hdd%s' %str(form1.cleaned_data['base_temperature_hddxx'])
                context['elems_long'] = acis_elements['hdd']['name_long']
                context['base_temp'] = str(form1.cleaned_data['base_temperature_hddxx'])
            elif form1.cleaned_data['element'] == 'cddxx':
                elem = 'cdd%s' %str(form1.cleaned_data['base_temperature_cddxx'])
                context['elems_long'] = acis_elements['cdd']['name_long']
                context['base_temp'] = str(form1.cleaned_data['base_temperature_cddxx'])
            else:
                elem = str(form1.cleaned_data['element'])
                context['elems_long'] = acis_elements[elem]['name_long']
            params['elems'] = [{'name':elem}]
            if 'state' in form1.cleaned_data.keys():
                params['state'] = form1.cleaned_data['state']
                region = 'state_%s' %form1.cleaned_data['state']
                context['state'] = form1.cleaned_data['state']
            elif 'bounding_box' in form1.cleaned_data.keys():
                context['need_map'] = True
                context['bounding_box'] = form1.cleaned_data['bounding_box']
                params['bbox'] = form1.cleaned_data['bounding_box']
                region = 'bbox_' + re.sub(',','_',form1.cleaned_data['bounding_box'])
                context['bounding_box'] = form1.cleaned_data['bounding_box']

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
            file_path_big = MEDIA_URL +'tmp/' + figure_file
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

def clim_risk_maps(request):
    context = {
        'title': 'Climate Risk Maps',
        'apps_page':True
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
    if bounding_box is not None:initial['bounding_box'] = bounding_box

    if initial:
        if element and start_date and end_date:
            form1 = forms.ClimateMapForm1(initial=initial)
            context['form1'] = form1
            context['hide_form0'] = True
            context['form1_ready'] = True
        else:
            form0 = set_as_form(request,'ClimateRiskForm0', init=initial)
            context['form0'] = form0
    else:
        form0 = set_as_form(request,'ClimateRiskForm0')
        context['form0'] = form0

    if 'form0' in request.POST:
        form0 = set_as_form(request,'ClimateRiskForm0')
        context['form0']  = form0

        if form0.is_valid():
            pass

    if 'form1' in request.POST:
        form1 = set_as_form(request,'ClimateRiskForm1')
        context['form1']  = form1

        if form1.is_valid():
            pass
    return render_to_response('my_data/apps/gridded/clim_risk_maps.html', context, context_instance=RequestContext(request))
def grid_point_time_series(request):
    context = {
        'title': 'Grid Point Time Series',
        'apps_page':True
    }
    lat = request.GET.get('lat', None)
    lon = request.GET.get('lon', None)
    element = request.GET.get('element', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    grid = request.GET.get('grid', None)
    initial = {}
    if element is not None:initial['element'] = str(element)
    if start_date is not None:initial['start_date'] = str(start_date)
    if end_date is not None:initial['end_date'] = str(end_date)
    if lat is not None and lon is not None:
        initial['lat']=str(lat);initial['lon']=str(lon)
        context['lat'] = str(lat);context['lon'] = str(lon)
    else:
        context['lat'] = '39.82'; context['lon'] = '-98.57'
    if grid is not None:
        initial['grid'] = str(grid)

    if initial:
        form0 = set_as_form(request,'GPTimeSeriesForm', init=initial)
    else:
        form0 = set_as_form(request,'GPTimeSeriesForm')
    context['form0'] = form0


    if 'form0' in request.POST:
        form0 = set_as_form(request,'GPTimeSeriesForm')
        context['form0']  = form0

        if form0.is_valid():
            #check for base temperature if gdd, hdd, cdd
            element, base_temp = WRCCUtils.get_el_and_base_temp(form0.cleaned_data['element'])
            if base_temp is not None:
                context['base_temp'] = base_temp
            context['element_long'] = acis_elements[element]['name_long']
            context['element'] = form0.cleaned_data['element']
            context['lat'] = form0.cleaned_data['lat']
            context['lon'] = form0.cleaned_data['lon']
            #Note: acis takes lon, lat in that order
            location = '%s,%s' %(str(form0.cleaned_data['lon']), str(form0.cleaned_data['lat']))
            context['select_grid_by'] = 'point'
            context['s_date'] = form0.cleaned_data['start_date']
            context['e_date'] = form0.cleaned_data['end_date']
            context['elems'] = form0.cleaned_data['element']
            context['grid'] = form0.cleaned_data['grid']
            form_input = {'location':location, 'element': form0.cleaned_data['element'], \
            'start_date':form0.cleaned_data['start_date'], \
            'end_date':form0.cleaned_data['end_date'], 'grid':form0.cleaned_data['grid']}

            req = AcisWS.get_grid_data(form_input, 'GPTimeSeries')
            try:
                data = []
                dates = []
                for date_idx, dat in enumerate(req['data']):
                    data.append(req['data'][date_idx][1])
                    #dates.append(str(req['data'][date_idx][0]))
                    dates.append('%s%s%s' %(str(req['data'][date_idx][0][0:4]), str(req['data'][date_idx][0][5:7]), str(req['data'][date_idx][0][8:10])))
                context['start_date'] = dates[0]
                context['end_date'] = dates[-1]
                datadict = {'data':data, 'dates':dates}
                context['datadict'] = datadict
            except:
                datadict = {}
                context['datadict'] = datadict
                if 'error' in req.keys():
                    context['error'] = str(req['error'])
                else:
                    context['error'] = 'Unknown error ocurred when getting data'
            results_json = str(datadict).replace("\'", "\"")
            time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            json_file = '%s_gp_ts_%s_%s_%s_%s.json' %(time_stamp, str(form0.cleaned_data['lat']), \
                str(form0.cleaned_data['lon']), form0.cleaned_data['start_date'], \
                form0.cleaned_data['end_date'])
            context['json_file'] = json_file
            JSON_URL = '/tmp/'
            f = open('%s%s' %(JSON_URL,json_file),'w+')
            f.write(results_json)
            f.close()
    return render_to_response('my_data/apps/gridded/grid_point_time_series.html', context, context_instance=RequestContext(request))

def station_locator_app(request):
    from subprocess import call
    call(["touch", "/tmp/Empty.json"])
    context = {
        'title': 'Station Finder',
        'search_page':True
    }
    form0 = set_as_form(request,'StationLocatorForm0')
    context['form0'] = form0
    context['empty_json'] = False
    context['show_legend'] = True
    context['map_title'] = 'Map of Southwest US COOP stations!'

    if 'form0' in request.POST:
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
                context['bounding_box'] = '-115,34,-114,35'

    if 'form1' in request.POST:
        context['empty_json'] = True
        form1 = set_as_form(request,'StationLocatorForm1')
        context['form1'] = form1
        context['form1_ready'] = True
        if form1.is_valid():
            if 'elements' in form1.cleaned_data.keys():
                element_list = ','.join(form1.cleaned_data['elements'])
            else:
                element_list = 'Any climate element'
                context['elements']= 'Any climate element'
            select_stations_by = form1.cleaned_data['select_stations_by']
            if 'station_id' in form1.cleaned_data.keys():
                by_type = 'station_id';val = form1.cleaned_data['station_id']
                context['by_type'] = 'Individual Station: %s' %str(val)
            if 'station_ids' in form1.cleaned_data.keys():
                by_type = 'station_ids';val = form1.cleaned_data['station_ids']
                context['by_type'] = 'Multiple Stations: %s' %str(val)
            if 'county' in form1.cleaned_data.keys():
                by_type = 'county';val = form1.cleaned_data['county']
                context['by_type'] = 'County FIPS Code: %s' %str(val)
            if 'climate_division' in form1.cleaned_data.keys():
                by_type = 'climate_division';val = form1.cleaned_data['climate_division']
                context['by_type'] = 'Climate Division: %s' %str(val)
            if 'county_warning_area' in form1.cleaned_data.keys():
                by_type = 'county_warning_area';val = form1.cleaned_data['county_warning_area']
                context['by_type'] = 'County Warning Area: %s' %str(val)
            if 'basin' in form1.cleaned_data.keys():
                by_type = 'basin';val = form1.cleaned_data['basin']
                context['by_type'] = 'Basin: %s' %str(val)
            if 'state' in form1.cleaned_data.keys():
                by_type = 'state';val = form1.cleaned_data['state']
                context['by_type'] = 'State: %s' %str(val)
            if 'states' in form1.cleaned_data.keys():
                by_type = 'states';val = form1.cleaned_data['states']
                context['by_type'] = 'States: %s' %str(val)
            if 'bounding_box' in form1.cleaned_data.keys():
                by_type = 'bounding_box';val = form1.cleaned_data['bounding_box']
                context['by_type'] = 'Bounding Box: %s' %str(val)

            context['map_title'] = by_type.upper() + ': ' + val

            if form1.cleaned_data['element_selection'] == 'T':
                date_range = [str(form1.cleaned_data['start_date']), str(form1.cleaned_data['end_date'])]
                context['start_date'] = form1.cleaned_data['start_date']
                context['end_date'] = form1.cleaned_data['end_date']
                context['elements'] = ','.join(form1.cleaned_data['elements']) #tuple of elements
                if form1.cleaned_data['constraints']=='all_all':
                    constraints = 'All Elements, All Dates'; context['constraints'] = constraints
                if form1.cleaned_data['constraints']=='any_any':
                    constraints = 'Any Elements, Any Dates'; context['constraints'] = constraints
                if form1.cleaned_data['constraints']=='all_any':
                    constraints = 'All Elements, Any Dates'; context['constraints'] = constraints
                if form1.cleaned_data['constraints']=='any_all':
                    constraints = 'Any Elements, All Dates'; context['constraints'] = constraints
                context['map_title'] = by_type.upper() + ': ' + val + ', ELEMENTS: ' + \
                                   ','.join(form1.cleaned_data['elements']) + \
                                   ', FROM: ' + form1.cleaned_data['start_date'] + ' TO: '+ form1.cleaned_data['start_date'] + \
                                   ', ' + constraints
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
                        el_vX_list.append(acis_elements[el]['vX'])

                stn_json, f_name = AcisWS.station_meta_to_json(by_type, val, el_list=el_vX_list,time_range=date_range, constraints=form1.cleaned_data['constraints'])
            else:
                stn_json, f_name = AcisWS.station_meta_to_json(by_type, val)

            if 'error' in stn_json.keys():
                context['error'] = stn_json['error']
            if stn_json['stations'] == []:
                context['error'] = "No stations found for %s : %s, elements: %s."  %(by_type, val, element_list)
            context['json_file'] = f_name
            context['empty_json'] = False
            context['form1_ready'] = True
            context['show_legend'] = True
    return render_to_response('my_data/apps/station/station_locator_app.html', context, context_instance=RequestContext(request))

######################################
#SOD programs
######################################
##SOD Utils
def set_sod_initial(request, app_name):
    stn_id = request.GET.get('stn_id', None)
    start_date = request.GET.get('start_date', None)
    end_date  = request.GET.get('end_date', None)
    start_year = request.GET.get('start_year', None)
    end_year  = request.GET.get('end_year', None)
    initial ={}
    if stn_id is not None:initial['stn_id'] = stn_id
    if app_name in ['Sodsumm']:
        initial['date_type'] = 'y'
        if start_year is not None:initial['start_year'] = start_year
        if end_year is not None:initial['end_year'] = end_year
    else:
        initial['date_type'] = 'd'
        if start_date is not None:initial['start_date'] = start_date
        if end_date is not None:initial['end_date'] = end_date
    return initial

#SOD views
def sodsumm(request):
    context = {
        'title': 'Sodsumm - Monthly and Seasonal Summaries of Daily Data',
        'apps_page':True
        }
    initial = set_sod_initial(request, 'Sodsumm')
    form1 = set_as_form(request,'SodsummForm', init=initial)
    context['form1'] = form1

    if 'form1' in request.POST:
        form1 = set_as_form(request,'SodsummForm', init={'date_type':'y'})
        context['form1'] = form1
        if form1.is_valid():
            data_params = {
                    'sid':form1.cleaned_data['station_ID'],
                    'start_date':form1.cleaned_data['start_year'],
                    'end_date':form1.cleaned_data['end_year'],
                    'element':'all'
                    }
            app_params = {
                    'el_type':form1.cleaned_data['summary_type'],
                    'max_missing_days':form1.cleaned_data['max_missing_days'],
                    }
            #Run data retrieval job
            DJ = WRCCClasses.SodDataJob('Sodsumm', data_params)
            #WARNING: station_ids, names need to be called before dates_list
            station_ids, station_names = DJ.get_station_ids_names()
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
            context['station_ID'] = data_params['sid']
            context['max_missing_days'] = app_params['max_missing_days']
            #Sodsumm table headers for html
            if form1.cleaned_data['summary_type'] == 'all':
                if form1.cleaned_data['generate_graphics'] == 'T':
                    context['tab_names'] = ['Temp', 'Precip', 'Snow', 'Hdd', 'Cdd', 'Gdd', 'Corn']
                    tab_list = ['temp', 'pcpn', 'snow', 'hdd', 'cdd', 'gdd', 'corn']
                    table_list = ['temp', 'prsn', 'prsn', 'hdd', 'cdd', 'gdd', 'corn']
                else:
                    context['tab_names'] = ['Temp', 'Precip/Snow', 'Hdd', 'Cdd', 'Gdd', 'Corn']
                    tab_list = ['temp', 'prsn', 'hdd', 'cdd', 'gdd', 'corn']
                    table_list = ['temp','prsn', 'hdd', 'cdd', 'gdd', 'corn']
            elif form1.cleaned_data['summary_type'] == 'both':
                if form1.cleaned_data['generate_graphics'] == 'T':
                    context['tab_names'] = ['Temperature', 'Precip', 'Snow']
                    tab_list = ['temp', 'pcpn', 'snow']
                    table_list = ['temp', 'prsn', 'prsn']
                else:
                    context['tab_names'] = ['Temp', 'Precip/Snow']
                    tab_list = ['temp', 'prsn']
                    table_list = ['temp''prsn']
            elif form1.cleaned_data['summary_type'] == 'temp':
                table_list = ['temp']
                context['tab_names'] = ['Temperature']
                tab_list = ['temp']
                table_list = ['temp']
            elif form1.cleaned_data['summary_type'] == 'prsn':
                if form1.cleaned_data['generate_graphics'] == 'T':
                    context['tab_names'] = ['Precip', 'Snow']
                    tab_list = ['pcpn', 'snow']
                    table_list = ['prsn', 'prsn']
                else:
                    context['tab_names'] = ['Precip/Snow']
                    tab_list = ['prsn']
                    table_list = ['prsn']
            elif form1.cleaned_data['summary_type'] == 'hc':
                context['tab_names'] =  ['Hdd', 'Cdd']
                tab_list = ['hdd', 'cdd']
                table_list = ['hdd', 'cdd']
            elif form1.cleaned_data['summary_type'] == 'g':
                table_list = ['gdd', 'corn']
                context['tab_names'] =  ['Gdd', 'Corn']
                tab_list = ['gdd', 'corn']
                table_list = ['gdd', 'corn']
            else:
                table_list = []
                tab_list = []
            context['table_list'] = table_list
            context['tab_list'] = tab_list
            #Define html content
            context['run_done'] = True
            if dates_list:
                context['start_year'] = dates_list[0]
                context['end_year'] = dates_list[-1]
            else:
                context['start_year'] = '0000'
                context['end_year'] = '0000'
            context['station_name'] = station_names
            context['headers'] = set_sodsumm_headers(table_list)

            #Generate grahics
            if form1.cleaned_data['generate_graphics'] == 'T' and results:
                context['graphics'] = True
                cats = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
                json_list = []
                for tab_idx, tab in enumerate(tab_list):
                    table = table_list[tab_idx]
                    if tab =='temp':
                        legend = ['Extr Low','Ave Low','Mean', 'Ave High', 'Extr High']
                        colors  = ['#FF0000', '#690000', '#00FF00', '#ADD8E6', '#0000FF']
                        table_name_long = 'Temperatures (F)'
                        units = 'Fahrenheit'
                        table_data = [[] for i in range(12)]
                        #table_data = [[] for i in range(5)] # low, ave min, ave mean,ave max, high
                        for idx, row in enumerate(results[table][1:13]):
                            for i in range(5):
                                if i == 0:k = 6 #low
                                if i == 1:k = 2 #mean low
                                if i == 2:k = 3 #mean ave
                                if i == 3:k = 1 #mean high
                                if i == 4:k = 4 #high
                                try:
                                    table_data[idx].append(float(row[k]))
                                except:
                                    table_data[idx].append(None)
                            '''
                                if i == 4:k = 6 #low
                                if i == 3:k = 2;l = 6 #mean low
                                if i == 2:k = 3;l = 2 #mean ave
                                if i == 1:k = 1;l = 3 #mean high
                                if i == 0:k = 4;l = 1 #high
                                if i == 4 :
                                    table_data[i].append(float(row[k]))
                                else:
                                    table_data[i].append(float(row[k]) - float(row[l]))
                            '''
                    elif tab in ['hdd', 'cdd']:
                        units = 'Fahrenheit'
                        colors = ['#87CEFA', '#00FFFF', '#14D8FF', '#143BFF', '#8A14FF']
                        if table == 'hdd':
                            legend = ['Base 65', 'Base 60', 'Base 57', 'Base 55', 'Base 50']
                        else:
                            legend = ['Base 55', 'Base 57', 'Base 60', 'Base 65', 'Base 70']
                        table_name_long = acis_elements[table]['name_long']
                        table_data = [[] for i in range(5)]
                        for i in range(5):
                            for k in range(len(cats)):
                                try:
                                    table_data[i].append(float(results[table][i+1][k+1]))
                                except:
                                    table_data[i].append(None)
                    elif tab == 'gdd':
                        units = 'Fahrenheit'
                        colors = ['#87CEFA', '#00FFFF', '#14D8FF', '#143BFF', '#8A14FF']
                        table_name_long = acis_elements[table]['name_long']
                        legend = ['Base 40', 'Base 45', 'Base 50', 'Base 55', 'Base 60']
                        table_data = [[] for i in range(5)]
                        for i in range(5):
                            for k in range(len(cats)):
                                try:
                                    table_data[i].append(float(results[table][2*i+1][k+2]))
                                except:
                                    table_data[i].append(None)
                    elif tab == 'corn':
                        units = 'Fahrenheit'
                        colors = ['#14FFFF', '#00FFFF', '#14D8FF', '#143BFF', '#8A14FF']
                        table_name_long = 'Corn Degree Days (F)'
                        legend = ['Base 50']
                        table_data =[[]]
                        for k in range(len(cats)):
                            try:
                                table_data[0].append(float(results[table][1][k+2]))
                            except:
                                table_data[0].append(None)
                    elif  tab == 'pcpn':
                        units = 'Inches'
                        colors = ['#00FFFF','#00009B', ' #0000FF']
                        legend = ['Ave Precip Low', 'Precip Mean', 'Ave Precip High']
                        table_name_long = 'Precipitation(In)'
                        table_data = [[] for k in range(3)]
                        for idx, row in enumerate(results[table][1:13]):
                            for i in range(3):
                                if i == 0:k=4
                                if i == 1:k=1
                                if i == 2:k=2
                                try:
                                    table_data[i].append(float(row[k]))
                                except:
                                    table_data[i].append(None)
                    elif tab == 'snow':
                        colors = ['#00FFFF','#00009B']
                        legend = ['Snow Mean', 'Ave Snow High']
                        table_name_long = 'Snow Fall(In)'
                        table_data = [[] for k in range(2)]
                        for idx, row in enumerate(results[table][1:13]):
                            for i in range(2):
                                if i == 0:k=12
                                if i == 1:k=13
                                try:
                                    table_data[i].append(float(row[k]))
                                except:
                                    table_data[i].append(None)
                                    '''
                                    #stacked bar
                                    if i == 2:k = 4 #low
                                    if i == 1:k = 1;l = 4 #ave mean
                                    if i == 0:k = 2;l = 1 #high
                                    if i == 2:
                                        table_data[i].append(float(row[k]))
                                    else:
                                        table_data[i].append(float(row[k])- float(row[l]))
                                    '''

                                    '''
                                    #boxplot
                                    if i == 1:
                                        if tbl == 'pcpn':k = 4 #low
                                        if tbl == 'snow':k = 0
                                    if i == 2:
                                        if tbl == 'pcpn':k = 1#ave mean
                                        if tbl == 'snow':k = 12
                                    if i == 3:
                                        if tbl == 'pcpn':k = 2#high
                                        if tbl == 'snow':k = 13
                                    if i == 4:
                                        if tbl == 'pcpn':k = 6#1-day max
                                        if tbl == 'snow':k = 13
                                    '''
                    table_dict = {
                        'cats':cats,
                        'units':units,
                        'record_start':dates_list[0][0:4],
                        'record_end':dates_list[-1][0:4],
                        'stn_name':station_names[0],
                        'stn_id':str(data_params['sid']),
                        'table_name':tab,
                        'table_name_long':table_name_long,
                        'legend':legend,
                        'colors': colors,
                        'table_data': table_data
                        }
                    json_list.append(table_dict)
                results_json = str(json_list).replace("\'", "\"")
                time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                json_file = '%s_sodsumm_%s_%s_%s.json' \
                %(time_stamp, str(data_params['sid']), dates_list[0][0:4], dates_list[-1][0:4])
                f = open('/tmp/%s' %(json_file),'w+')
                f.write(results_json)
                f.close()
                context['JSON_URL'] = '/tmp/'
                context['json_file'] = json_file
    return render_to_response('my_data/apps/station/sodsumm.html', context, context_instance=RequestContext(request))

#Utlities
def set_sodsumm_headers(table_list):
    headers = {}
    def set_header(table):
        rows = []
        if table == 'temp':
            rows.append('<th colspan="16"> <b>Temperature Statistics</b>:</th>')
            rows.append('<th colspan="2"></th><th colspan="4">Averages, </th><th colspan="4">Daily Extremes, </th><th colspan="4">Mean Extremes, </th><th colspan="2"> >= =<  =<  =< </th>')
        elif table == 'prsn':
            rows.append('<th colspan="15"><b>Precipitation/Snow Statistics</b>:</th>')
            rows.append('<th colspan="6">Total Precipitation, </th><th colspan="2">Precipitation, </th><th colspan="2"> >= =<  =<  =< </th><th colspan="3">Total Snowfall</th>')

        elif table == 'hdd':
            rows.append('<th colspan="14"><b>Heating degree days</b>:</th>')
            rows.append('<tr><td colspan="14">Output is rounded, unlike NCDC values, which round input.</td></tr>')
            rows.append('<tr><td colspan="14">Degree Days to selected Base Temperatures(F)</td></tr>')
        elif table == 'cdd':
            rows.append('<th colspan="14"><b>Cooling degree days</b>:</th>')
            rows.append('<tr><td colspan="14">Output is rounded, unlike NCDC values, which round input.</td></tr>')
            rows.append('<tr><td colspan="14">Degree Days to selected Base Temperatures(F)</td></tr>')
        elif table == 'gdd':
            rows.append('<th colspan="15"><b>Growing degree days</b>:</th>')
            rows.append('<tr><td colspan="15">Output is rounded, unlike NCDC values, which round input.</td>')
            rows.append('<tr><td colspan="15">Growing Degree Days to selected Base Temperatures(F)</td></tr>')
        elif table == 'corn':
            rows.append('<th colspan="15"><b>Corn Growing Degree Days</b></th>')
        return "\n".join(rows)

    for table in table_list:
         headers[table] = set_header(table)
    return headers

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

def export_to_file_point(request, data, dates, station_names, station_ids, elements, file_info, delim, file_extension):
    if file_extension in ['dat', 'txt']:
        import csv
        response = HttpResponse(mimetype='text/csv')
        #response = HttpResponse(mimetype='text/csv')
        #response['Content-Disposition'] = 'attachment;filename=export.%s' % file_extension
        response['Content-Disposition'] = 'attachment;filename=%s_%s.%s' % (file_info[0], file_info[1],file_extension)
        writer = csv.writer(response, delimiter=delim )
        for stn, dat in data.iteritems():
            row = ['Station ID: %s' %str(station_ids[stn]), 'Station_name: %s' %str(station_names[stn])]
            writer.writerow(row)
            row = ['date']
            for el in elements:row.append(el)
            writer.writerow(row)
            for j, vals in enumerate(dat):
                row = [dates[j]]
                if len(station_ids) == 1:
                    for val in vals[1:]:row.append(val)
                else:
                    for val in vals:row.append(val)
                writer.writerow(row)
    else: #Excel
        from xlwt import Workbook
        wb = Workbook()
        for stn, dat in data.iteritems():
            ws = wb.add_sheet('Station_%s %s' %(str(station_ids[stn]), str(stn)))
            #Header
            ws.write(0, 0, 'Date')
            for k, el in enumerate(elements):ws.write(0, k+1, el)
            #Data
            for j, vals in enumerate(dat):
                ws.write(j+1, 0, dates[j])
                if len(station_ids) == 1:
                    for l,val in enumerate(vals[1:]):ws.write(j+1, l+1, val) #row, column, label
                else:
                    for l,val in enumerate(vals):ws.write(j+1, l+1, val) #row, column, label
        response = HttpResponse(content_type='application/vnd.ms-excel;charset=UTF-8')
        #response = HttpResponse(content_type='application/vnd.ms-excel;charset=UTF-8')
        response['Content-Disposition'] = 'attachment;filename=%s_%s.%s' % (file_info[0], file_info[1],file_extension)
        wb.save(response)

    return response


def export_to_file_grid(request, data, elements, file_info, delim, file_extension):
    if file_extension in ['dat', 'txt']:
        import csv
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment;filename=%s_%s.%s' % (file_info[0], file_info[1],file_extension)
        writer = csv.writer(response, delimiter=delim )
        row = ['Date', 'Lat', 'Lon', 'Elev']
        for el in elements:row.append(el)
        writer.writerow(row)
        for date_idx, date_vals in enumerate(data):
            writer.writerow(date_vals)
    else: #Excel
        from xlwt import Workbook
        wb = Workbook()
        #Note row number limit is 65536 in some excel versions
        row_number = 0
        flag = 0
        sheet_counter = 0
        for date_idx, date_vals in enumerate(data): #row
            for j, val in enumerate(date_vals):#column
                if row_number == 0:
                    flag = 1
                else:
                    row_number+=1
                if row_number == 65535:flag = 1

                if flag == 1:
                    sheet_counter+=1
                    #add new workbook sheet
                    ws = wb.add_sheet('Sheet_%s' %sheet_counter)
                    #Header
                    ws.write(0, 0, 'Date')
                    ws.write(0, 1, 'Lat')
                    ws.write(0, 2, 'Lon')
                    ws.write(0, 3, 'Elev')
                    for k, el in enumerate(elements):ws.write(0, k+4, el)
                    row_number = 1
                    flag = 0


                ws.write(date_idx+1, j, str(val))#row, column, label
        response = HttpResponse(content_type='application/vnd.ms-excel;charset=UTF-8')
        response['Content-Disposition'] = 'attachment;filename=%s_%s.%s' % (file_info[0], file_info[1], file_extension)
        wb.save(response)

    return response

def run_external_script(cmd):
    """ Capture a command's standard output."""
    import subprocess
    out, err = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    return out, err
