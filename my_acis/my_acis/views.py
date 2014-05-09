# Create your views here.
import datetime
from django.template import RequestContext
#from django.contrib.auth.models import User
#from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.db.models.query import QuerySet

from wrcc_meta.models import *
#from wrcc_meta.forms import *


def home_view(request):
    context = {
        'state_choices': STATE_CHOICES,
        'title': "WRCC Metadata Home",
    }
    return render_to_response('base.html', context, context_instance=RequestContext(request))


