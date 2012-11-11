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
    stn_id = None
    if stn_id is not None:
        form0_point = set_as_form(request,'PointData0Form', init={'stn_id':stn_id})
    else:
        form0_point = set_as_form(request,'PointData0Form')
    context['form0_point'] = form0_point

    if 'form0_point' in request.POST:
        if stn_id is not None:
            form0_point = set_as_form(request,'PointData0Form', init={'stn_id':stn_id})
        else:
            form0_point = set_as_form(request,'PointData0Form')
        context['form0_point']  = form0_point

        if form0_point.is_valid():
            context['form1_ready'] = '1ready'
            initial = {'station_selection':form0_point.cleaned_data['station_selection'], \
                      'elements':form0_point.cleaned_data['elements'], \
                      'data_format':form0_point.cleaned_data['data_format']}
            form1_point = forms.PointDataForm1(initial=initial)
            context['form1_point'] = form1_point
            context['initial'] = initial
        else:
            elements = None
            station_selection = None
            data_format = None

    if 'form1_point' in request.POST:
        context['form0_done']= '0Done'
        form1_point = set_as_form(request,'PointDataForm1')
        context['form1_point'] = form1_point
        if form1_point.is_valid():
            #context['cleaned'] = form1_point.cleaned_data
            #(data, dates, elements, coop_station_ids, station_names) = AcisWS.get_sod_data(form1_point.cleaned_data, 'sodlist_web')
            #app_args = {'data':data, 'dates':dates, elements:'elements', \
            #'coop_station_ids':coop_station_ids, 'data_format': form1_point.cleaned_data['data_format']}
            app_args={}
            if 'delimiter' in form1_point.cleaned_data.keys():
                app_args['delimiter'] = form1_point.cleaned_data['delimiter']
            results = WRCCDataApps.get_csc_point_data(**app_args)

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
