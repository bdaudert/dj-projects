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
import re
from collections import defaultdict

#My modules
import AcisWS, WRCCDataApps, WRCCClasses, WRCCUtils
import my_data.forms as forms

state_choices = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', \
                'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', \
                'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', \
                'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', \
                'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

static_url = '/Users/bdaudert/DRI/dj-projects/my_acis/static/'
MEDIA_URL = '/Users/bdaudert/DRI/dj-projects/my_acis/media/'

month_names = ['January', 'February', 'March', 'April', 'May', 'June',\
               'July', 'August', 'September', 'October', 'November', 'December']

def home_view(request):
    context = {
        'title': 'Southwest CSC Portal',
        'state_choices': ['AZ', 'CA', 'CO', 'NM', 'NV', 'UT'],
        'home_page':True
    }
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
    return render_to_response('my_data/home.html', context, context_instance=RequestContext(request))

def about_us(request):
    context = {
        'title': 'About Us'
    }
    return render_to_response('my_data/about_us.html', context, context_instance=RequestContext(request))

def contact_us(request):
    context = {
        'title': 'Contact Us'
    }
    return render_to_response('my_data/contact_us.html', context, context_instance=RequestContext(request))

def data(request):
    context = {
        'title': 'Data Access',
        'data_page':True
    }
    stn_id = request.GET.get('stn_id', None)
    if stn_id is not None:
        form0_point = set_as_form(request,'PointData0Form', init={'stn_id':str(stn_id)})
    else:
        form0_point = set_as_form(request,'PointData0Form')
    form0_grid = set_as_form(request,'GridData0Form')
    context['form0_point'] = form0_point
    context['form0_grid'] = form0_grid

    if 'form0_point' in request.POST:
        form0_point = set_as_form(request,'PointData0Form')
        context['form0_point']  = form0_point

        if form0_point.is_valid():
            context['form1_point_ready'] = True
            initial = {'station_selection':form0_point.cleaned_data['station_selection'], \
                      'elements':form0_point.cleaned_data['elements'], \
                      'data_format':form0_point.cleaned_data['data_format']}
            if 'stn_id' in form0_point.cleaned_data.keys():
                initial['stn_id'] = form0_point.cleaned_data['stn_id']
            form1_point = forms.PointDataForm1(initial=initial)
            context['form1_point'] = form1_point
        else:
            elements = None
            station_selection = None
            data_format = None

    if 'form0_grid' in request.POST:
        form0_grid = set_as_form(request,'GridData0Form')
        context['form0_grid']  = form0_grid

        if form0_grid.is_valid():
            context['form1_grid_ready'] = True
            initial = {'grid_selection':form0_grid.cleaned_data['grid_selection'], \
                      'elements':form0_grid.cleaned_data['elements'], \
                      'data_format':form0_grid.cleaned_data['data_format']}
            form1_grid = forms.GridDataForm1(initial=initial)
            context['form1_grid'] = form1_grid
        else:
            elements = None
            grid_selection = None
            data_format = None


    if 'form1_point' in request.POST:
        form1_point = set_as_form(request,'PointDataForm1')
        context['form1_point'] = form1_point
        if form1_point.is_valid():
            context['cleaned'] = form1_point.cleaned_data
            (data, dates, elements, station_ids, station_names) = AcisWS.get_point_data(form1_point.cleaned_data, 'sodlist_web')
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
            if form1_point.cleaned_data['data_format'] == 'dlm':
                return export_to_file_point(request, data, dates, station_names, station_ids, elements, delimiter, 'dat')
            elif form1_point.cleaned_data['data_format'] == 'clm':
                return export_to_file_point(request, data, dates, station_names, station_ids, elements, delimiter, 'txt')
            elif form1_point.cleaned_data['data_format'] == 'xl':
                return export_to_file_point(request, data, dates, station_names, station_ids, elements, delimiter, 'xls')
            else:
                return render_to_response('my_data/data/home.html', context, context_instance=RequestContext(request))

    if 'form1_grid' in request.POST:
        form1_grid = set_as_form(request,'GridDataForm1')
        context['form1_grid'] = form1_grid
        if form1_grid.is_valid():
            (data, elements) = AcisWS.get_grid_data(form1_grid.cleaned_data, 'griddata_web')
            context['grid_data'] = dict(data)
            context['elements'] =  elements
            dates_dict = {}
            if 'delimiter' in form1_grid.cleaned_data.keys():
                if str(form1_grid.cleaned_data['delimiter']) == 'comma':delimiter = ','
                if str(form1_grid.cleaned_data['delimiter']) == 'tab':delimiter = '  '
                if str(form1_grid.cleaned_data['delimiter']) == 'colon':delimiter = ':'
                if str(form1_grid.cleaned_data['delimiter']) == 'space':delimiter = ' '
                if str(form1_grid.cleaned_data['delimiter']) == 'pipe':delimiter = '|'
            else:
                if form1_grid.cleaned_data['data_format'] == 'json':
                    delimiter = None
                    context['json'] = True
                else:
                    delimiter = ' '
            context['delimiter'] = delimiter

            #Output formats
            import re
            grid_selection = form1_grid.cleaned_data['grid_selection']
            if grid_selection == 'point':file_info =['location', re.sub(',','_',form1_grid.cleaned_data['location'])]
            if grid_selection == 'state':file_info = ['state', form1_grid.cleaned_data['state']]
            if grid_selection == 'bbox':file_info =['bounding_box', re.sub(',','_',form1_grid.cleaned_data['bounding_box'])]
            context['file_info'] = file_info
            if form1_grid.cleaned_data['data_format'] == 'dlm':
                return export_to_file_grid(request, data, elements, file_info,delimiter, 'dat')
            elif form1_grid.cleaned_data['data_format'] == 'clm':
                return export_to_file_grid(request, data, elements, file_info, delimiter, 'txt')
            elif form1_grid.cleaned_data['data_format'] == 'xl':
                return export_to_file_grid(request, data, elements, file_info, delimiter, 'xls')
            else:
                return render_to_response('my_data/data/home.html', context, context_instance=RequestContext(request))

    return render_to_response('my_data/data/home.html', context, context_instance=RequestContext(request))

def apps(request):
    context = {
        'title': 'Applications and Products',
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
                    for key, val in meta_request['meta'][0].items():
                        if key == 'sids':
                            sid_list = []
                            for sid in val:sid_list.append(sid.encode('ascii', 'ignore'))
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
            perl_out, perl_err = run_external_script("perl %sperl-scripts/csc_cliMETAgraph.pl %s" %(MEDIA_URL, str(form_meta.cleaned_data['station_id'])))
            context['perl_err'] = perl_err
            context['perl_out'] = perl_out
        else:
            stn_id = None

    return render_to_response('my_data/apps/metagraph.html', context, context_instance=RequestContext(request))

def monthly_aves(request):
    context = {
        'title': 'Monthly Averages',
    }
    stn_id = request.GET.get('stn_id', None)
    if stn_id is None:
        form_graphs = set_as_form(request,'MonthlyAveragesForm')
    else:
        form_graphs = set_as_form(request,'MonthlyAveragesForm', init={'stn_id':str(stn_id)})
    context['form_graphs'] = form_graphs
    if 'form_graphs' in request.POST:
        form_graphs = set_as_form(request,'MonthlyAveragesForm')
        context['form_graphs']  = form_graphs
        if form_graphs.is_valid():
            s_date = str(form_graphs.cleaned_data['start_date'])
            e_date = str(form_graphs.cleaned_data['end_date'])
            params = dict(sid=form_graphs.cleaned_data['station_id'], sdate=s_date, edate=e_date, \
            meta='valid_daterange,name,state,sids,ll,elev,uid,county,climdiv', \
            elems=[dict(name=el, groupby="year")for el in form_graphs.cleaned_data['elements']])
            monthly_aves = {}

            #req = WRCCClasses.DataJob('StnData', params).make_data_call()
            req = AcisWS.StnData(params)
            context['raw_data'] = req['data']
            try:
                monthly_aves = WRCCDataApps.monthly_aves(req, form_graphs.cleaned_data['elements'])
                context['averaged_data'] = monthly_aves
            except:
                pass

            results = [{} for k in form_graphs.cleaned_data['elements']]
            #results = defaultdict(dict)
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
                    results[el_idx] = {'element_long': 'Total Snowfall', 'units':'in'}
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
                    results[el_idx]['record_start'] = str(req['meta']['valid_daterange'][el_idx][0])
                else:
                    results[el_idx]['record_start'] = '%s-%s-%s' % (s_date[0:4], s_date[4:6], s_date[6:8])
                if form_graphs.cleaned_data['end_date'] == 'por':
                    results[el_idx]['record_end'] = str(req['meta']['valid_daterange'][el_idx][1])
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
            json_file = 'monthly_aves.json'
            context['json_file'] = json_file
            f = open('%sjson/%s' %(MEDIA_URL,json_file),'w+')
            f.write(results_json)
            f.close()

        else:
            stn_id = None

    return render_to_response('my_data/apps/monthly_aves.html', context, context_instance=RequestContext(request))

def station_finder(request):
    context = {
        'title': 'Station Finder',
        'state_choices':state_choices,
        'station_finder_page':True
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
        stn_json = AcisWS.station_meta_to_json('id', q)
        if 'error' in stn_json.keys():
            context['error'] = stn_json['error']
    context['json_file'] = 'stn.json'
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
        stn_json = AcisWS.station_meta_to_json('county', q)
        if 'error' in stn_json.keys():
            context['error'] = stn_json['error']
    context['json_file'] = 'stn.json'
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
        stn_json = AcisWS.station_meta_to_json('county_warning_area', q)
        if 'error' in stn_json.keys():
            context['error'] = stn_json['error']
    context['json_file'] = 'stn.json'
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
        stn_json = AcisWS.station_meta_to_json('climate_division', q)
        if 'error' in stn_json.keys():
            context['error'] = stn_json['error']
    context['json_file'] = 'stn.json'
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
        stn_json = AcisWS.station_meta_to_json('basin', q)
        if 'error' in stn_json.keys():
            context['error'] = stn_json['error']
    context['json_file'] = 'stn.json'
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
        stn_json = AcisWS.station_meta_to_json('state', state_key)
        if 'error' in stn_json.keys():
            context['error'] = stn_json['error']
    context['json_file'] = 'stn.json'
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
    else:
        try:
            bbox ="%f, %f, %f, %f" % (float(W), float(S), float(E), float(N))
            stn_json = AcisWS.station_meta_to_json('bounding_box', bbox)
            if 'error' in stn_json.keys():
                context['error'] = stn_json['error']
        except:
            bbox = ''
            pass
    context['title'] = "Search Results for bounding box %s" %bbox
    context['json_file'] = 'stn.json'
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

def export_to_file_point(request, data, dates, station_names, station_ids, elements, delim, file_extension):
    if file_extension in ['dat', 'txt']:
        import csv
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment;filename=export.%s' % file_extension
        writer = csv.writer(response, delimiter=delim )
        for stn, dat in data.items():
            row = ['Station ID: %s' %str(station_ids[stn]), 'Station_name: %s' %str(station_names[stn])]
            writer.writerow(row)
            row = ['date']
            for el in elements:row.append(el)
            writer.writerow(row)
            for j, vals in enumerate(dat):
                row = [dates[j]]
                for val in vals:row.append(val)
                writer.writerow(row)
    else: #Excel
        from xlwt import Workbook
        wb = Workbook()
        for stn, dat in data.items():
            ws = wb.add_sheet('%s %s' %(station_ids[stn], station_names[stn]))
            #Header
            ws.write(0, 0, 'Date')
            for k, el in enumerate(elements):ws.write(0, k+1, el)
            #Data
            for j, vals in enumerate(dat):
                ws.write(j+1, 0, dates[j])
                for l,val in enumerate(vals):ws.write(j+1, l+1, val) #row, column, label

        response = HttpResponse(content_type='application/vnd.ms-excel;charset=UTF-8')
        response['Content-Disposition'] = 'attachment;filename=export.%s' % file_extension
        wb.save(response)

    return response


def export_to_file_grid(request, data, elements, file_info, delim, file_extension):
    if file_extension in ['dat', 'txt']:
        import csv
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment;filename=%s_%s.%s' % (file_info[0], file_info[1],file_extension)
        writer = csv.writer(response, delimiter=delim )
        for stn, dat in data.items():
            row = ['Date', 'Lat', 'Lon', 'Elev']
            for el in elements:row.append(el)
            writer.writerow(row)
            for date_idx, date_vals in data.items():
                writer.writerow(date_vals)
    else: #Excel
        from xlwt import Workbook
        wb = Workbook()
        ws = wb.add_sheet('GRIDDED DATA RESULTS')
        #Header
        ws.write(0, 0, 'Date')
        ws.write(0, 1, 'Lat')
        ws.write(0, 2, 'Lon')
        ws.write(0, 3, 'Elev')
        for k, el in enumerate(elements):ws.write(0, k+4, el)

        #Data
        for date_idx, date_vals in data.items():
            for j, val in enumerate(date_vals):
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
