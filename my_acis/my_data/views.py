#!/usr/bin/python
#django Imports
from django.template import RequestContext
#from django.contrib.auth.models import User
#from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic.list_detail import object_detail, object_list
from django.db.models.query import QuerySet
from django.contrib.localflavor.us.forms import USStateField


#My modules
import AcisWS, WRCCDataApps
import my_data.forms as forms

state_choices = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', \
                'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', \
                'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', \
                'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', \
                'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

def home_view(request):
    context = {
        'title': "Southwest CSC Portal",
    }
    return render_to_response('my_data/home.html', context, context_instance=RequestContext(request))

def data(request):
    context = {
        'title': "Data Access",
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
            context['data'] = dict(data)
            context['elements'] =  elements
            dates_dict = {}
            stn_ids_dict = {}
            stn_names_dict = {}
            #FIX ME!Need to convert to dict since lookup not working on lists
            for k, name in enumerate(station_names):
                stn_ids_dict[k] = station_ids[k]
                stn_names_dict[k] = station_names[k]
            for k, date in enumerate(dates):
                dates_dict[k] = date
            context['station_names'] = stn_names_dict
            context['station_ids'] = stn_ids_dict
            context['dates'] = dates_dict
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
                return export_to_file(request, data, dates, station_names, station_ids, elements, delimiter, 'dat')
            elif form1_point.cleaned_data['data_format'] == 'clm':
                return export_to_file(request, data, dates, station_names, station_ids, elements, delimiter, 'txt')
            elif form1_point.cleaned_data['data_format'] == 'xl':
                return export_to_file(request, data, dates, station_names, station_ids, elements, delimiter, 'xls')
            else:
                return render_to_response('my_data/data/home.html', context, context_instance=RequestContext(request))

    if 'form1_grid' in request.POST:
        form1_grid = set_as_form(request,'GridDataForm1')
        context['form1_grid'] = form1_grid
        if form1_grid.is_valid():
            (data, dates, elements, latlons) = AcisWS.get_grid_data(**form1_grid.cleaned_data)
            context['data'] = dict(data)
            context['elements'] =  elements
            dates_dict = {}
            context['dates'] = dates_dict
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
            if form1_grid.cleaned_data['data_format'] == 'dlm':
                return export_to_file(request, data, dates, station_names, latlonss, elements, delimiter, 'dat')
            elif form1_grid.cleaned_data['data_format'] == 'clm':
                return export_to_file(request, data, dates, station_names, latlons, elements, delimiter, 'txt')
            elif form1_grid.cleaned_data['data_format'] == 'xl':
                return export_to_file(request, data, dates, station_names, latlons, elements, delimiter, 'xls')
            else:
                return render_to_response('my_data/data/home.html', context, context_instance=RequestContext(request))

    return render_to_response('my_data/data/home.html', context, context_instance=RequestContext(request))

def apps(request):
    context = {
        'title': "Applications and Products",
    }
    return render_to_response('my_data/apps/home.html', context, context_instance=RequestContext(request))


def station_finder(request):
    stn_json = AcisWS.get_station_meta('state', "nv")
    context = {
        'title': "Station Finder",
        'stn_json': stn_json,
        'state_choices':state_choices,
    }
    return render_to_response('my_data/station_finder/home.html', context, context_instance=RequestContext(request))

def by_id(request):
    q = request.GET.get('q', '')
    if not q:
        stn_json = {}
    else:
        stn_json = AcisWS.get_station_meta('id', q)
    context = {
        'stn_json': stn_json,
        'title': "Search Results for Station ID %s" %q,
    }
    return render_to_response('my_data/station_finder/station_map.html', context, context_instance=RequestContext(request))


def by_county(request):
    q = request.GET.get('q', '')
    if not q:
        stn_json = {}
    else:
        stn_json = AcisWS.get_station_meta('county', q)

    context = {
        'stn_json': stn_json,
        'title': "Search Results for County %s" %q,
    }
    return render_to_response('my_data/station_finder/station_map.html', context, context_instance=RequestContext(request))

def by_cwa(request):
    q = request.GET.get('q', '')
    if not q:
        stn_json = {}
    else:
        stn_json = AcisWS.get_station_meta('county_warning_area', q)

    context = {
        'stn_json': stn_json,
        'title': "Search Results for County Warning Area %s" %q,
    }
    return render_to_response('my_data/station_finder/station_map.html', context, context_instance=RequestContext(request))

def by_clim_div(request):
    q = request.GET.get('q', '')
    if not q:
        stn_json = {}
    else:
        stn_json = AcisWS.get_station_meta('climate_division', q)

    context = {
        'stn_json': stn_json,
        'title': "Search Results for Climate Division %s" %q,
    }
    return render_to_response('my_data/station_finder/station_map.html', context, context_instance=RequestContext(request))

def by_basin(request):
    q = request.GET.get('q', '')
    if not q:
        stn_json = {}
    else:
        stn_json = AcisWS.get_station_meta('basin', q)

    context = {
        'stn_json': stn_json,
        'title': "Search Results for Basin %s" %q,
    }
    return render_to_response('my_data/station_finder/station_map.html', context, context_instance=RequestContext(request))

def by_state(request):
    state_key = request.GET.get('state_key', None)
    if state_key is None:
        stn_json = {}
    else:
        stn_json = AcisWS.get_station_meta('state', state_key)


    context = {
        'stn_json': stn_json,
        'title': "Search Results for State %s" %state_key,
    }
    return render_to_response('my_data/station_finder/station_map.html', context, context_instance=RequestContext(request))

def by_bounding_box(request):
    W = request.GET.get('W', None)
    S = request.GET.get('S', None)
    E = request.GET.get('E', None)
    N = request.GET.get('N', None)
    bbox ="%f, %f, %f, %f" % (float(W), float(S), float(E), float(N))
    if not W or not S or not E or not N:
        stn_json = {}
    else:
        stn_json = AcisWS.get_station_meta('bounding_box', bbox)
    context = {
        'stn_json': stn_json,
        'title': "Search Results for bounding box %s" %bbox,
    }
    return render_to_response('my_data/station_finder/station_map.html', context, context_instance=RequestContext(request))

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

def export_to_file(request, data, dates, station_names, station_ids, elements, delim, file_extension):
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

        response = HttpResponse(content_type='application/vnd.ms-excel;charset=<charset>')
        response['Content-Disposition'] = 'attachment;filename=export.%s' % file_extension
        wb.save(response)

    return response
