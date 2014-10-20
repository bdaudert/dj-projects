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

HOST = 'wrcc.dri.edu'
STATIC_URL = '/www/apps/csc/dj-projects/my_acis/static/'
MEDIA_URL = '/www/apps/csc/dj-projects/my_acis/media/'
KML_URL = '/www/apps/csc/dj-projects/my_acis/media/kml/'
TMP_URL = '/www/apps/csc/dj-projects/my_acis/media/tmp'

def home(request):
    context = {
        'title': 'Documentation',
    }
    return render_to_response('documentation/home.html', context, context_instance=RequestContext(request))

def ee(request):
    context = {
        'title': 'Google Earth Engine/App Engine projects',
    }
    return render_to_response('documentation/ee/ee.html', context, context_instance=RequestContext(request))

def ee_set_up(request):
    context = {
        'title': 'Google Earth Engine/App Engine set up',
    }
    return render_to_response('documentation/ee/set_up.html', context, context_instance=RequestContext(request))

def ee_hello_world(request):
    context = {
        'title': 'Google Earth Engine/App Engine Hello World example',
    }
    return render_to_response('documentation/ee/hello_world.html', context, context_instance=RequestContext(request))

def ee_organizing_code(request):
    context = {
        'title': 'Organizing your code',
    }
    return render_to_response('documentation/ee/organizing_code.html', context, context_instance=RequestContext(request))

def acis(request):
    context = {
        'title': 'ACIS',
    }
    return render_to_response('documentation/acis/home.html', context, context_instance=RequestContext(request))

def grid_acis(request):
    context = {
        'title': 'GridACIS',
    }
    return render_to_response('documentation/acis/grid_acis.html', context, context_instance=RequestContext(request))

def subdaily_acis(request):
    context = {
        'title': 'SubDailyACIS',
    }
    return render_to_response('documentation/acis/subdaily_acis.html', context, context_instance=RequestContext(request))

def scenic(request):
    context = {
        'title': 'SCENIC',
    }
    return render_to_response('documentation/scenic/home.html', context, context_instance=RequestContext(request))

def large_data_requests(request):
    context = {
        'title': 'Large Data Request Methodology',
    }
    return render_to_response('documentation/scenic/large_data_requests.html', context, context_instance=RequestContext(request))
