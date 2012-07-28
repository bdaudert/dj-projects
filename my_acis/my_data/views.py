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


def home_view(request):
    context = {
        'title': "STATION FINDER",
    }
    return render_to_response('my_data/home.html', context, context_instance=RequestContext(request))
