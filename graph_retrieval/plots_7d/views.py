# Create your views here.
from django.template import Context, loader
from plots_7d.models import State, Station
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.http import Http404
from datetime import date

def index(request):
    states = State.objects.all()
    return render_to_response('plots_7d/index.html', {'states': states})

def stations(request, state_name):
    try:
        stns = Station.objects.filter(state=state_name)
    except Station.DoesNotExist:
        raise Http404
    return render_to_response('plots_7d/stations.html', {'stations': stns, 'state_name': state_name})

def results(request, state_name, ucan_id):
    #return HttpResponse("Hello, world. Here is where you will see results soon")
    try:
        station =  Station.objects.get(state=state_name, ucan_station_id=ucan_id)
        stns = Station.objects.filter(state=state_name, ucan_station_id=ucan_id)
    except Station.DoesNotExist:
        raise Http404
    #station = get_object_or_404(Station, state=state_name, ucan_station_id=ucan_id)

    today = date.today()
    #FIX ME: don't hard code 2 digit year, covert 4 digit today.year somehow, python time modules are hard!
    #year = today.year
    year = 12
    month = int(today.month)
    if month < 10:
        month = '0%d' %month
    day = int(today.day)
    if day < 10:
        day = '0%d' %day

    if station.ucan_station_id == 1:
        print wrcc_id
        wrcc_id = 'AOPE'
    elif station.ucan_station_id == 2:
        wrcc_id = 'ASHK'
    elif station.ucan_station_id == 3:
        wrcc_id = 'CKET'
    elif station.ucan_station_id == 4:
        wrcc_id = 'CBEN'
    elif station.ucan_station_id == 5:
        wrcc_id = 'ACTC'
    elif station.ucan_station_id == 6:
        wrcc_id = 'ANOA'
    else:
        pass

    #return render_to_response('plots_7d/results.html', {'station' : station,'wrcc_id': wrcc_id, 'state_name': state_name, 'year': year, 'month': month, 'day': day })
    return render_to_response('plots_7d/results.html', {'state_name': state_name, 'station': station,'wrcc_id': wrcc_id,'year': year, 'month': month, 'day': day })
