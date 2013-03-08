#!/usr/bin/python
#django imports
from django.template import RequestContext
#from django.contrib.auth.models import User
#from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic.list_detail import object_detail, object_list
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
              'evap': {'name': 'evap', 'name_long':'Pan Evaporation (In)', 'vX':'7'}, \
              'dd': {'name': 'dd', 'name_long':'Degree Days (Days)', 'vX':'45'}, \
              'cdd': {'name': 'cdd', 'name_long':'Cooling Degree Days (Days)'}, 'vX':'45', \
              'hdd': {'name': 'hdd', 'name_long':'Heating Degree Days (Days)'}, 'vX':'45', \
              'gdd': {'name': 'gdd', 'name_long':'Growing Degree Days (Days)'}, 'vX':'45'}
              #bug fix needed for cdd = 44 (WAITING FOR BILL, ALSO IN PLACES BELOW, eg in station_locator_app, also in AcisWS.py)

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
        'title': 'Southwest Climate Knowledge Network',
        'home_page':True
    }
    return render_to_response('my_data/index.html', context, context_instance=RequestContext(request))

def home(request):
    context = {
        'title': 'Southwest Climate Knowledge Network',
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
        'title': 'Welcome to the SW-CKN',
        'state_choices': ['AZ', 'CA', 'CO', 'NM', 'NV', 'UT'],
        'home_page':True
    }
    context['json_file'] = 'CSC_Info.json'
    return render_to_response('my_data/main_map.html', context, context_instance=RequestContext(request))

#Temp home page fpr Kelly to look at
def main(request):
    context = {
        'title': 'Welcome to the SW-CKN',
        'state_choices': ['AZ', 'CA', 'CO', 'NM', 'NV', 'UT'],
        'home_page':True
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

def focus_areas(request):
    context = {
        'title': 'Focus Areas',
        'intro_page':True
    }
    return render_to_response('my_data/focus_areas.html', context, context_instance=RequestContext(request))

def projects(request):
    context = {
        'title': 'Projects',
        'intro_page':True
    }
    return render_to_response('my_data/projects.html', context, context_instance=RequestContext(request))

def publications(request):
    context = {
        'title': 'Publications',
        'intro_page':True
    }
    return render_to_response('my_data/publications.html', context, context_instance=RequestContext(request))

def news_events(request):
    context = {
        'title': 'News, Events and Announcements',
        'intro_page':True
    }
    return render_to_response('my_data/news_events.html', context, context_instance=RequestContext(request))

def contact_us(request):
    context = {
        'title': 'Contact Us',
        'intro_page':True
    }
    return render_to_response('my_data/contact_us.html', context, context_instance=RequestContext(request))

def dashboard(request):
    context = {
        'title': 'Dashboard',
        'home_page':True
    }
    return render_to_response('my_data/dashboard.html', context, context_instance=RequestContext(request))

def data_home(request):
    context = {
        'title': 'Data Access',
        'data_page':True
    }
    return render_to_response('my_data/data/home.html', context, context_instance=RequestContext(request))

def data_historic(request):
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
        form0_point = set_as_form(request,'PointDataForm0', init=initial_params_0)
    else:
        form0_point = set_as_form(request,'PointDataForm0')
    context['form0_point'] = form0_point

    if 'form0_point' in request.POST or stn_id is not None:
        #form0_point = set_as_form(request,'PointDataForm0')
        #context['form0_point']  = form0_point

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
            if elements is not None:context['elements'] = elements
            #initial_params_1['elements'] = form0_point.cleaned_data['elements']
            #initial_params_1['data_format'] = form0_point.cleaned_data['data_format']
            if stn_id is not None:
                initial_params_1['select_stations_by'] = 'stn_id'
            else:
                initial_params_1['select_stations_by'] = form0_point.cleaned_data['select_stations_by']


            form1_point = forms.PointDataForm1(initial=initial_params_1)
            context['form1_point'] = form1_point

    if 'form1_point' in request.POST:
        form1_point = set_as_form(request,'PointDataForm1')
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
            context['cleaned'] = form1_point.cleaned_data
            #Check if data request is large,
            #if so, gather params and ask user for name and e-mail and notify user that request will be processed offline
            if form1_point.cleaned_data['start_date'] == 'por':
                s_date = datetime.date(1900,01,01)
            else:
                s_date = datetime.date(int(form1_point.cleaned_data['start_date'][0:4]), int(form1_point.cleaned_data['start_date'][4:6]),int(form1_point.cleaned_data['start_date'][6:8]))
            if form1_point.cleaned_data['end_date'] == 'por':
                e_date = datetime.date.today()
            else:
                e_date = datetime.date(int(form1_point.cleaned_data['end_date'][0:4]), int(form1_point.cleaned_data['end_date'][4:6]),int(form1_point.cleaned_data['end_date'][6:8]))
            days = (e_date - s_date).days
            #if time range > 1 month or user requests data for more than 1 station, large request via ftp
            if days > 10000:
            #if days > 31 or 'station_id' not in form1_point.cleaned_data.keys():
                context['form3_point_ready'] = True
                context['large_request'] = 'You requested a large amount of data.Please enter your name and e-mail address. We will notify you once your request has been processed and your data is availiable on our ftp server.'
                initial_params_2 = form1_point.cleaned_data
                #keep MultiElements format and MultiStnField format
                initial_params_2['elements'] = ','.join(initial_params_2['elements'])
                if 'station_ids' in initial_params_2.keys():
                    initial_params_2['station_ids'] = ','.join([str(stn) for stn in initial_params_2['station_ids']])
                form3_point = forms.PointDataForm3(initial=initial_params_2)
                context['form3_point'] = form3_point
                return render_to_response('my_data/data/historic/home.html', context, context_instance=RequestContext(request))
            else:
                (data, dates, elements, station_ids, station_names, errors) = AcisWS.get_point_data(form1_point.cleaned_data, 'sodlist_web')
                context['errors'] = errors
                context['point_data'] = dict(data)
                context['elements'] =  elements
                context['station_names'] = station_names
                context['station_ids'] = station_ids
                context['dates'] = dates
                if 'delimiter' in form1_point.cleaned_data.keys():
                    if str(form1_point.cleaned_data['delimiter']) == 'comma':delimiter = ','
                    if str(form1_point.cleaned_data['delimiter']) == 'tab':delimiter = '  '
                    if str(form1_point.cleaned_data['delimiter']) == 'colon':delimiter = ':'
                    if str(form1_point.cleaned_data['delimiter']) == 'space':delimiter = ' '
                    if str(form1_point.cleaned_data['delimiter']) == 'pipe':delimiter = '|'
                else:
                    if form1_point.cleaned_data['data_format'] == 'json':
                        delimiter = None
                        context['json'] = True
                    else:
                        delimiter = ' '
                context['delimiter'] = delimiter

                #Output formats
                select_stations_by = form1_point.cleaned_data['select_stations_by']
                if select_stations_by == 'stnid':
                    file_info =['StnId', form1_point.cleaned_data['station_id']]
                elif select_stations_by == 'stn_id':
                    file_info =['StnId',',',form1_point.cleaned_data['station_id']]
                elif select_stations_by == 'stnids':
                    file_info = ['Multi','Stations']
                elif select_stations_by == 'county':
                    file_info =['county', form1_point.cleaned_data['county']]
                elif select_stations_by == 'climdiv':
                    file_info =['climdiv', form1_point.cleaned_data['climate_division']]
                elif select_stations_by == 'cwa':
                    file_info =['cwa', form1_point.cleaned_data['county_warning_area']]
                elif select_stations_by == 'basin':
                    file_info =['basin', form1_point.cleaned_data['basin']]
                elif select_stations_by == 'state':
                    file_info =['state', form1_point.cleaned_data['state']]
                elif select_stations_by == 'bbox':
                    file_info =['bbox', re.sub(',','_',form1_point.cleaned_data['bounding_box'])]
                else:
                    file_info =['Undefined','export']
                context['file_info'] = file_info

                if form1_point.cleaned_data['data_format'] == 'dlm':
                    #return export_to_file_point(request, data, dates, station_names, station_ids, elements, file_info, delimiter, 'dat')
                    return WRCCUtils.write_point_data_to_file(data, dates, station_names, station_ids, elements,delimiter, 'dat', request=request, file_info=file_info)
                elif form1_point.cleaned_data['data_format'] == 'clm':
                    #return export_to_file_point(request, data, dates, station_names, station_ids, elements, file_info, delimiter, 'txt')
                    return WRCCUtils.write_point_data_to_file(data, dates, station_names, station_ids, elements,delimiter, 'txt', request=request, file_info=file_info)
                elif form1_point.cleaned_data['data_format'] == 'xl':
                    #return export_to_file_point(request, data, dates, station_names, station_ids, elements, file_info, delimiter, 'xls')
                    return WRCCUtils.write_point_data_to_file(data, dates, station_names, station_ids, elements,delimiter, 'xls', request=request, file_info=file_info)
                else:
                    return render_to_response('my_data/data/historic/home.html', context, context_instance=RequestContext(request))
            #form1_point not valid or form1_point valid and we are done with computation
            #needed to show validation error in form1_point
            #form1_point = set_as_form(request,'PointDataForm1')
            #context['form1_point'] = form1_point
            #context['form1_point_ready'] = True
    if 'form3_point' in request.POST:
        form3_point = set_as_form(request,'PointDataForm3')
        context['form3_point'] = form3_point
        context['form3_point_ready'] = True
        if form3_point.is_valid():
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
        return render_to_response('my_data/data/historic/home.html', context, context_instance=RequestContext(request))

    return render_to_response('my_data/data/historic/home.html', context, context_instance=RequestContext(request))

def data_modeled(request):
    context = {
        'title': 'Modeled Data',
        'data_page':True
    }

    initial_0 = {}
    select_grid_by = request.GET.get('select_grid_by', None)
    elements = request.GET.get('elements', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    elements = request.GET.get('elements', None)
    bounding_box = request.GET.get('bounding_box', None)
    state = request.GET.get('state', None)
    loc = request.GET.get('loc', None)
    grid = request.GET.get('grid', None)
    if select_grid_by is not None:initial_0['select_grid_by'] = select_grid_by
    if elements is not None:initial_0['elements'] = str(elements);context['elements'] = elements
    if start_date is not None:context['start_date'] = start_date
    if end_date is not None:context['end_date'] = end_date
    if bounding_box is not None:context['bounding_box'] = bounding_box
    if state is not None:context['state'] = state
    if loc is not None:context['location'] = loc
    if initial_0:
        form0_grid = set_as_form(request,'GridDataForm0', init=initial_0)
    else:
        form0_grid = set_as_form(request,'GridDataForm0')
    context['form0_grid'] = form0_grid
    if 'form0_grid' in request.POST:
        #form0_grid = set_as_form(request,'GridDataForm0')
        #context['form0_grid']  = form0_grid
        if form0_grid.is_valid():
            context['form1_grid_ready'] = True
            select_grid_by = request.GET.get('select_grid_by', None)
            start_date = request.GET.get('start_date', None)
            end_date = request.GET.get('end_date', None)
            elements = request.GET.get('elements', None)
            bounding_box = request.GET.get('bounding_box', None)
            state = request.GET.get('state', None)
            loc = request.GET.get('loc', None)
            grid = request.GET.get('grid', None)
            initial_1 = {}
            if elements is not None:context['elements'] = elements
            if start_date is not None:initial_1['start_date'] = start_date;context['start_date'] = start_date
            if end_date is not None:initial_1['end_date'] = end_date;context['end_date'] = end_date
            if bounding_box is not None:initial_1['bounding_box'] = bounding_box;context['bounding_box'] = bounding_box
            if state is not None:initial_1['state'] = state;context['state'] = state
            if loc is not None:initial_1['location'] = loc;context['location'] = loc
            if select_grid_by is None:
                initial_1['select_grid_by'] = form0_grid.cleaned_data['select_grid_by']
            else:
                initial_1['select_grid_by'] = select_grid_by
            if elements is None:
                initial_1['elements'] = form0_grid.cleaned_data['elements']
            else:
                initial_1['elements'] = elements
            initial_1['data_format']  = form0_grid.cleaned_data['data_format']

            '''
            initial_1 = {'select_grid_by':form0_grid.cleaned_data['select_grid_by'], \
                      'elements':form0_grid.cleaned_data['elements'], \
                      'data_format':form0_grid.cleaned_data['data_format']}
            '''
            context['initial_1'] = initial_1
            form1_grid = forms.GridDataForm1(initial=initial_1)
            context['form1_grid'] = form1_grid

    if 'form1_grid' in request.POST:
        form1_grid = set_as_form(request,'GridDataForm1')
        context['form1_grid'] = form1_grid
        context['form1_grid_ready'] = True
        if form1_grid.is_valid():
            el_list = form1_grid.cleaned_data['elements']
            context['elements'] =  el_list
            #Check if data request is large,
            #if so, gather params and ask user for name and e-mail and notify user that request will be processed offline
            s_date = datetime.date(int(form1_grid.cleaned_data['start_date'][0:4]), int(form1_grid.cleaned_data['start_date'][4:6]), \
            int(form1_grid.cleaned_data['start_date'][6:8]))
            e_date = datetime.date(int(form1_grid.cleaned_data['end_date'][0:4]), int(form1_grid.cleaned_data['end_date'][4:6]), \
            int(form1_grid.cleaned_data['end_date'][6:8]))
            days = (e_date - s_date).days
            #if time range > 1 month or user requests data for more than 1 station, large request via ftp
            if days > 31 or 'location' not in form1_grid.cleaned_data.keys():
                context['form3_grid_ready'] = True
                context['large_request'] = \
                'You requested a large amount of data.Please enter your name and e-mail address. We will notify you once your request has been processed and your data is availiable on our ftp server.'
                initial_params_2 = form1_grid.cleaned_data
                #keep MultiElements format and MultiStnField format
                initial_params_2['elements'] = ','.join(initial_params_2['elements'])
                form3_grid = forms.GridDataForm3(initial=initial_params_2)
                context['form3_grid'] = form3_grid
                return render_to_response('my_data/data/modeled/home.html', context, context_instance=RequestContext(request))
            else:
                req = AcisWS.get_grid_data(form1_grid.cleaned_data, 'griddata_web')
                #format data
                if form1_grid.cleaned_data['data_format'] == 'json':
                    delimiter = None
                    context['json'] = True
                    context['grid_data']  = req
                else:
                    data = WRCCUtils.format_grid_data(req, form1_grid.cleaned_data)
                    context['grid_data'] = data
                '''
                if 'error' in req.keys():
                    context['error']  = req
                else:
                    if form1_grid.cleaned_data['data_format'] == 'json':
                        delimiter = None
                        context['json'] = True
                        context['grid_data']  = req
                    else:
                        if 'location' in form1_grid.cleaned_data.keys():
                            lats = [[req['meta']['lat']]]
                            lons = [[req['meta']['lon']]]
                            elevs = [[req['meta']['elev']]]
                            data = [[] for i in range(len(req['data']))]
                        else:
                            lats = req['meta']['lat']
                            lons = req['meta']['lon']
                            elevs = req['meta']['elev']
                            lat_num = 0
                            for lat_idx, lat_grid in enumerate(req['meta']['lat']):
                               lat_num+=len(lat_grid)
                            length = len(req['data']) * lat_num
                            #length = len(req['data'])
                            data = [[] for i in range(length)]
                        idx = -1
                        for date_idx, date_vals in enumerate(req['data']):
                            if 'location' in form1_grid.cleaned_data.keys():
                                data[date_idx].append(str(date_vals[0]))
                                data[date_idx].append(lons[0][0])
                                data[date_idx].append(lats[0][0])
                                data[date_idx].append(elevs[0][0])

                                for el_idx in range(1,len(el_list) + 1):
                                    data[date_idx].append(str(date_vals[el_idx]).strip(' '))
                            else:
                                #idx+=1
                                for grid_idx, lat_grid in enumerate(lats):
                                    for lat_idx, lat in enumerate(lat_grid):
                                        idx+=1
                                        data[idx].append(str(date_vals[0]))
                                        data[idx].append(lons[grid_idx][lat_idx])
                                        data[idx].append(lat)
                                        data[idx].append(elevs[grid_idx][lat_idx])

                                        for el_idx in range(1,len(el_list) + 1):
                                            data[idx].append(date_vals[el_idx][grid_idx][lat_idx])
                        context['grid_data'] = data
                '''

                if 'delimiter' in form1_grid.cleaned_data.keys():
                    if str(form1_grid.cleaned_data['delimiter']) == 'comma':delimiter = ','
                    if str(form1_grid.cleaned_data['delimiter']) == 'tab':delimiter = '  '
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
                    return render_to_response('my_data/data/modeled/home.html', context, context_instance=RequestContext(request))
            #form1_grid not valid or form1_grid valid and we are done with computation
            #needed to show validation error in form1_grid
            #context['form1_grid_ready'] = True
            #form1_grid = set_as_form(request,'GridDataForm1')
            #context['form1_grid'] = form1_grid

    if 'form3_grid' in request.POST:
        form3_grid = set_as_form(request,'GridDataForm3')
        context['form3_grid'] = form3_grid
        context['form3_grid_ready'] = True
        if form3_grid.is_valid():
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
            context['user_info'] = 'You will receive an email from csc-data-request@dri.edu with instructions when the data request has been processed. You provided following -mail address: %s' % (form3_grid.cleaned_data['email'])
        return render_to_response('my_data/data/modeled/home.html', context, context_instance=RequestContext(request))

    return render_to_response('my_data/data/modeled/home.html', context, context_instance=RequestContext(request))



def apps_home(request):
    context = {
        'title': 'Climate Data Tools',
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

def sw_ckn_station_apps(request):
    context = {
        'title': 'SW-CKN Historic Station Data Applications',
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

    return render_to_response('my_data/apps/sw_ckn_station_apps.html', context, context_instance=RequestContext(request))

def metagraph(request):
    context = {
        'title': 'Station Metadata graphs',
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
            meta_request = WRCCClasses.DataJob('StnMeta', params).make_data_call()
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

    return render_to_response('my_data/apps/metagraph.html', context, context_instance=RequestContext(request))

def monthly_aves(request):
    context = {
        'title': 'Monthly Averages',
        'apps_page':True
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
                    context['averaged_data'] = monthly_aves
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
                    if form_graphs.cleaned_data['start_date'] == 'por':
                        if len(req['meta']['valid_daterange'][el_idx]) == 2:
                            results[el_idx]['record_start'] = str(req['meta']['valid_daterange'][el_idx][0])
                        else:
                            #no valid daterange found
                            results[el_idx]['record_start'] = ['0000-00-00']
                    else:
                        results[el_idx]['record_start'] = '%s-%s-%s' % (s_date[0:4], s_date[4:6], s_date[6:8])
                    if form_graphs.cleaned_data['end_date'] == 'por':
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
                    context['meta'] = Meta
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

    return render_to_response('my_data/apps/monthly_aves.html', context, context_instance=RequestContext(request))

def clim_sum_maps(request):
    context = {
        'title': 'Climate Summary Maps',
        'apps_page':True
    }
    form0 = set_as_form(request,'ClimateMapForm0')
    context['form0'] = form0

    if 'form0' in request.POST:
        form0 = set_as_form(request,'ClimateMapForm0')
        context['form0']  = form0

        if form0.is_valid():
            context['form1_ready'] = True
            context['select_grid_by'] = form0.cleaned_data['select_grid_by']
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
    return render_to_response('my_data/apps/clim_sum_maps.html', context, context_instance=RequestContext(request))

def grid_point_time_series(request):
    context = {
        'title': 'Grid Point Time Series',
        'apps_page':True
    }
    lat = request.GET.get('lat', None)
    lon = request.GET.get('lon', None)
    context['lat'] = lat


    if lat is not None and lon is not None:
        form0 = set_as_form(request,'GPTimeSeriesForm', init={'lat':str(lat), 'lon':str(lon)})
        context['form0'] = form0
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
                context['start_date'] = str(req['data'][0][0])
                context['end_date'] = str(req['data'][-1][0])
                for date_idx, dat in enumerate(req['data']):
                    data.append(req['data'][date_idx][1])
                    dates.append(str(req['data'][date_idx][0]))
                datadict = {'data':data, 'dates':dates}
                context['datadict'] = datadict
            except:
                if 'error' in request.keys():
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
    return render_to_response('my_data/apps/grid_point_time_series.html', context, context_instance=RequestContext(request))

def station_locator_app(request):
    from subprocess import call
    call(["touch", "/tmp/Empty.json"])
    context = {
        'title': 'Station Finder',
        'station_finder_page':True
    }
    form0 = set_as_form(request,'StationLocatorForm0')
    context['form0'] = form0
    context['empty_json'] = False

    if 'form0' in request.POST:
        context['empty_json'] = True
        form0 = set_as_form(request,'StationLocatorForm0')
        context['form0']  = form0

        if form0.is_valid():
            context['form1_ready'] = True
            initial_params= {}
            stn_id = request.GET.get('stn_id', None)
            if stn_id is not None:initial_params['station_id'] = str(stn_id)
            initial_params['select_stations_by'] = form0.cleaned_data['select_stations_by']
            initial_params['element_selection'] = form0.cleaned_data['element_selection']
            form1 = forms.StationLocatorForm1(initial=initial_params)
            context['form1'] = form1

    if 'form1' in request.POST:
        context['empty_json'] = True
        form1 = set_as_form(request,'StationLocatorForm1')
        context['form1'] = form1
        context['form1_ready'] = True
        if form1.is_valid():
            select_stations_by = form1.cleaned_data['select_stations_by']
            if 'station_id' in form1.cleaned_data.keys():by_type = 'station_id';val = form1.cleaned_data['station_id']
            if 'station_ids' in form1.cleaned_data.keys():by_type = 'station_ids';val = form1.cleaned_data['station_ids']
            if 'county' in form1.cleaned_data.keys():by_type = 'county';val = form1.cleaned_data['county']
            if 'climate_division' in form1.cleaned_data.keys():by_type = 'climate_division';val = form1.cleaned_data['climate_division']
            if 'county_warning_area' in form1.cleaned_data.keys():by_type = 'county_warning_area';val = form1.cleaned_data['county_warning_area']
            if 'basin' in form1.cleaned_data.keys():by_type = 'basin';val = form1.cleaned_data['basin']
            if 'state' in form1.cleaned_data.keys():by_type = 'state';val = form1.cleaned_data['state']
            if 'bounding_box' in form1.cleaned_data.keys():by_type = 'bounding_box';val = form1.cleaned_data['bounding_box']

            if form1.cleaned_data['element_selection'] == 'T':
                date_range = [str(form1.cleaned_data['start_date']), str(form1.cleaned_data['end_date'])]
                context['start_date'] = form1.cleaned_data['start_date']
                context['end_date'] = form1.cleaned_data['end_date']
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
                        el_vX_list.append(acis_elements[el]['vX'])

                stn_json, f_name = AcisWS.station_meta_to_json(by_type, val, el_list=el_vX_list,time_range=date_range)
            else:
                stn_json, f_name = AcisWS.station_meta_to_json(by_type, val)

            if 'error' in stn_json.keys():
                context['error'] = stn_json['error']
            if stn_json['stations'] == []:
                context['error'] = "No stations found for %s : %s, elements: %s and date range %s!"  %(by_type, val, element_list, date_range)
            context['json_file'] = f_name
            context['empty_json'] = False
            context['form1_ready'] = False
        #form1 = set_as_form(request,'StationLocatorForm1')
        #context['form1'] = form1
        #context['form1_ready'] = True
    return render_to_response('my_data/apps/station_locator_app.html', context, context_instance=RequestContext(request))

def apps_hydro(request):
    context = {
        'title': 'Hydrology Products',
        'apps_page':True
    }
    return render_to_response('my_data/apps/hydro/home.html', context, context_instance=RequestContext(request))

def apps_eco(request):
    context = {
        'title': 'Ecosystem Products',
        'apps_page':True
    }
    return render_to_response('my_data/apps/eco/home.html', context, context_instance=RequestContext(request))

def station_finder(request):
    context = {
        'title': 'Station Finder',
        'state_choices':state_choices,
        'station_finder_page':True,
    }
    context['json_file'] = 'SW_stn.json'
    return render_to_response('my_data/station_finder/home.html', context, context_instance=RequestContext(request))

def by_id(request):
    q = request.GET.get('q', '')
    context = {
        'title': "Search Results for Station ID %s" %q,
        'state_choices':state_choices
    }
    if not q:
        stn_json = {}
    else:
        stn_json, f_name = AcisWS.station_meta_to_json('id', q)
        if 'error' in stn_json.keys():
            context['error'] = stn_json['error']
        if stn_json['stations'] == []:
            context['error'] = "No station found for the given Id: %s" %q
    context['json_file'] = f_name
    return render_to_response('my_data/station_finder/home.html', context, context_instance=RequestContext(request))


def by_county(request):
    q = request.GET.get('q', '')
    context = {
        'title': "Search Results for County %s" %q,
        'state_choices':state_choices
    }
    if not q:
        stn_json = {}
    else:
        stn_json, f_name = AcisWS.station_meta_to_json('county', q)
        if 'error' in stn_json.keys():
            context['error'] = stn_json['error']
        if stn_json['stations'] == []:
            context['error'] = "No stations found for the given County: %s" %q
    context['json_file'] = f_name
    return render_to_response('my_data/station_finder/home.html', context, context_instance=RequestContext(request))

def by_cwa(request):
    q = request.GET.get('q', '')
    context = {
        'title': "Search Results for County Warning Area %s" %q,
        'state_choices':state_choices
        }
    if not q:
        stn_json = {}
    else:
        stn_json, f_name = AcisWS.station_meta_to_json('county_warning_area', q)
        if 'error' in stn_json.keys():
            context['error'] = stn_json['error']
        if stn_json['stations'] == []:
            context['error'] = "No stations found for the given County Warning Area: %s" %q
    context['json_file'] = f_name
    return render_to_response('my_data/station_finder/home.html', context, context_instance=RequestContext(request))

def by_clim_div(request):
    q = request.GET.get('q', '')
    context = {
        'title': "Search Results for Climate Division %s" %q,
        'state_choices':state_choices
    }
    if not q:
        stn_json = {}
    else:
        stn_json, f_name = AcisWS.station_meta_to_json('climate_division', q)
        if 'error' in stn_json.keys():
            context['error'] = stn_json['error']
        if stn_json['stations'] == []:
            context['error'] = "No stations found for the given Climate Division: %s" %q
    context['json_file'] = f_name
    return render_to_response('my_data/station_finder/home.html', context, context_instance=RequestContext(request))

def by_basin(request):
    q = request.GET.get('q', '')
    context = {
        'title': "Search Results for Basin %s" %q,
        'state_choices':state_choices
    }
    if not q:
        stn_json = {}
    else:
        stn_json, f_name = AcisWS.station_meta_to_json('basin', q)
        if 'error' in stn_json.keys():
            context['error'] = stn_json['error']
        if stn_json['stations'] == []:
            context['error'] = "No stations found for the given Basin: %s" %q
    context['json_file'] = f_name
    return render_to_response('my_data/station_finder/home.html', context, context_instance=RequestContext(request))

def by_state(request):
    state_key = request.GET.get('state_key', None)
    context = {
        'title': "Search Results for State %s" %state_key,
        'state_choices':state_choices
    }
    if state_key is None:
        stn_json = {}
    else:
        stn_json, f_name = AcisWS.station_meta_to_json('state', state_key)
        if 'error' in stn_json.keys():
            context['error'] = stn_json['error']
        if stn_json['stations'] == []:
            context['error'] = "No stations found for the given State: %s" %state_key
    context['json_file'] = f_name
    return render_to_response('my_data/station_finder/home.html', context, context_instance=RequestContext(request))

def by_bounding_box(request):
    W = request.GET.get('W', None)
    S = request.GET.get('S', None)
    E = request.GET.get('E', None)
    N = request.GET.get('N', None)
    context = {
        'state_choices':state_choices
    }
    if not W or not S or not E or not N:
        stn_json = {}
        bbox = ' '
        context['error'] = "Not a valid Bounding Box!"
    else:
        try:
            bbox ="%f, %f, %f, %f" % (float(W), float(S), float(E), float(N))
            stn_json, f_name = AcisWS.station_meta_to_json('bounding_box', bbox)
            if 'error' in stn_json.keys():
                context['error'] = stn_json['error']
            if stn_json['stations'] == []:
                context['error'] = "No stations found for the given Bounding Box: %s" %bbox
        except:
            bbox = ''
            if stn_json['stations'] == []:
                context['error'] = "No stations found for the given Bounding Box: None"
    context['title'] = "Search Results for bounding box %s" %bbox
    context['json_file'] = f_name
    return render_to_response('my_data/station_finder/home.html', context, context_instance=RequestContext(request))


#Utlities
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
