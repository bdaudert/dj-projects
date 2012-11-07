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

import AcisWS

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
