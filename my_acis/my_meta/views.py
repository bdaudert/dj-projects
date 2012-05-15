# Create your views here.
import datetime
from django.template import RequestContext
#from django.contrib.auth.models import User
#from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic.list_detail import object_detail, object_list
from django.db.models.query import QuerySet

from my_meta.models import *
#from my_meta.forms import *


def home_view(request):
#    return HttpResponse("Hello, you. You're at the my_acis/my_meta home page.")
    context = {
        'state_choices': STATE_CHOICES,
        'title': "Metadata Home",
    }
    return render_to_response('my_meta/home.html', context, context_instance=RequestContext(request))
