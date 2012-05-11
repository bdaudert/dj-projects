# Create your views here.
from django.template import Context, loader
from plots_7d.models import State, Station
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import Http404

def index(request):
    states = State.objects.all()
    return render_to_response('plots_7d/index.html', {'states': states})

def stations(request, state_name):
    try:
        stns = Station.objects.filter(state=state_name)
    except Station.DoesNotExist:
        raise Http404
    return render_to_response('plots_7d/stations.html', {'stations': stns})

def results(request, ucan_id):
    return HttpResponse("Hello, world. Here is where you will see results soon")

