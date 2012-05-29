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
from my_meta.forms import *

#My  additions. FIX ME: get rid of from import *
from collections import defaultdict
import inspect
from models import acis_models, common
import models
from django.forms.models import modelformset_factory

def home_view(request):
#    return HttpResponse("Hello, you. You're at the my_acis/my_meta home page.")
    context = {
        'state_choices': STATE_CHOICES,
        'title': "Metadata Home",
    }
    return render_to_response('my_meta/home.html', context, context_instance=RequestContext(request))

def by_state(request):
    state_key = request.GET.get('state_key', None)
    if state_key is None:
        stations = []
    else:
        stations = Station.objects.filter(state=int(state_key)).order_by('station_best_name')

    context = {
        'stations': stations,
        'title': "Stations by State",
    }
    return render_to_response('my_meta/results.html', context, context_instance=RequestContext(request))
def by_name(request):
    q = request.GET.get('q', '')
    if not q:
        stations = []
    else:
        stations = Station.objects.filter(station_best_name__icontains=q).order_by('station_best_name')

    context = {
        'stations': stations,
        'title': "Station Name Search Results",
    }
    return render_to_response('my_meta/results.html', context, context_instance=RequestContext(request))

def by_id(request):
    q = request.GET.get('q', '')
    if not q:
        stations = []
    else:
        stations = StationNetwork.objects.filter(network_station_id__icontains=q)
        ucan_ids = [s.ucan_station_id for s in stations]
        stations = Station.objects.filter(ucan_station_id__in=ucan_ids)
    context = {
        'stations': stations,
        'title': "Station ID Search Results",
    }
    return render_to_response('my_meta/results.html', context, context_instance=RequestContext(request))

def by_location(request):
    lat = request.GET.get('lat', None)
    lon = request.GET.get('lon', None)
    delta = .51
    if not lat or not lon:
        stations = []
    else:
        lat = float(lat)
        lon = float(lon)
        stations = StationLocation.objects.filter(latitude__lte=lat+delta, latitude__gte=lat-delta,
                                                    longitude__lte=lon+delta, longitude__gte=lon-delta,
                                                    history_flag__icontains='L'
                                                )
        ucan_ids = [s.ucan_station_id for s in stations]
        stations = Station.objects.filter(ucan_station_id__in=ucan_ids)
    context = {
        'stations': stations,
        'title': "Station Location Search Results",
    }
    return render_to_response('my_meta/results.html', context, context_instance=RequestContext(request))

def station_detail(request):
    ucan_id = request.GET.get('ucan_id', None)
    context = {
        'title': "Station Detail",
    }

    if ucan_id:
        ucan_id = int(ucan_id)
        context['ucan_station_id'] = ucan_id
        context['station'] = set_as_table(Station.objects.get(pk=ucan_id))
        context['station_location'] = set_as_table(StationLocation.objects.filter(ucan_station_id=ucan_id))
        context['station_maintenance'] = set_as_table(StationMaintenance.objects.filter(ucan_station_id=ucan_id))
        context['station_equipment'] = set_as_table(StationEquipment.objects.filter(ucan_station_id=ucan_id))
        context['station_physical'] = set_as_table(StationPhysical.objects.filter(ucan_station_id=ucan_id))
    return render_to_response('my_meta/station_detail.html', context, context_instance=RequestContext(request))

def station_tables(request):
    ucan_id = request.GET.get('ucan_id', None)
    context = {
        'title': "Available tables"
    }
    if ucan_id:
        ucan_id = int(ucan_id)
        table_dir = defaultdict(list)
        table = {}
        for name, obj in inspect.getmembers(models):
            if inspect.isclass(obj) and hasattr(obj, 'pk'):
                instances = obj.objects.filter(pk=ucan_id)
                for i, instance in enumerate(instances):
                    if "ucan_station_id" in [ f.name for f in instance._meta.fields ]:
                        inst_name='%s_%d' % (name, i+1)
                        table_dir[name].append(inst_name)
                        table[inst_name] = set_as_table2(instance)
                        #table[inst_name] = set_as_form(request, name, ucan_id)
        context['ucan_station_id'] = ucan_id
        context['table'] = table
        context['table_dir'] = dict(table_dir)
    return render_to_response('my_meta/station_tables.html', context, context_instance=RequestContext(request))

def add(request):
    tbl_name = request.GET.get('tbl_name', None)
    context = {
        'title': tbl_name,
    }
    form = set_as_form(request, tbl_name)
    #if request.POST:
    #    form_call = "%sForm(request.POST)" % tbl_name
    #    form = eval(form_call)
    #    form_name = "%sForm"
    #    if form.is_valid():
    #        form.save()
    #        context['saved'] = "Information saved."
    #else:
    #    form_call = "%sForm(initial={'tble_name': %s})" % ( tbl_name, tbl_name )
    #    form = eval(form_call)
    context['tbl_name'] = tbl_name
    context['form'] = form
    return render_to_response('my_meta/add.html', context, context_instance=RequestContext(request))


#@login_required
def station_maintenance(request, ucan_id):
    ucan_id = int(ucan_id)
    context = {
        'title': "Station Maintenance",
        'ucan_id': ucan_id,
    }
    if request.POST:
        form = StationMaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            context['saved'] = "Information saved."
        else:
            context['saved'] = "Information NOT saved."
    else:
        form = StationMaintenanceForm(initial={'ucan_station_id': ucan_id})

    context['form'] = form
    context['station_maintenance'] = set_as_table(StationMaintenance.objects.filter(ucan_station_id=ucan_id))
    return render_to_response('my_meta/station_maintenance.html', context, context_instance=RequestContext(request))

#@login_required
def station_physical(request, ucan_id):
    ucan_id = int(ucan_id)
    context = {
        'title': "Station Physical",
        'ucan_id': ucan_id,
    }
    if request.POST:
        form = StationPhysicalForm(request.POST)
        if form.is_valid():
            form.save()
            context['saved'] = "Information saved."
    else:
        form = StationPhysicalForm(initial={'ucan_station_id': ucan_id})

    context['form'] = form
    context['station_physical'] = set_as_table(StationPhysical.objects.filter(ucan_station_id=ucan_id))
    return render_to_response('my_meta/station_physical.html', context, context_instance=RequestContext(request))

#@login_required
def station_equipment(request, ucan_id):
    ucan_id = int(ucan_id)
    context = {
        'title': "Station Equipment",
        'ucan_id': ucan_id,
    }
    if request.POST:
        form = StationEquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            context['saved'] = "Information saved."
    else:
        form = StationEquipmentForm(initial={'ucan_station_id': ucan_id})

    context['form'] = form
    context['station_equipment'] = set_as_table(StationEquipment.objects.filter(ucan_station_id=ucan_id))
    return render_to_response('my_meta/station_equipment.html', context, context_instance=RequestContext(request))

#
# Utility functions
#
def set_as_table(qs):
    """
    Return a query set as an HTML table without <table> tags.
    """
    first = True
    headers = []
    rows = []

    if isinstance(qs, QuerySet):
        for i in qs:
            if first:
                first = False
                headers.append("<tr>")
                for f in i._meta.fields:
                    headers.append("<th>%s</th>" % f.name)
                headers.append("</tr>")
            rows.append("<tr>")
            for f in i._meta.fields:
                rows.append("<td>%s</td>" % break_text(getattr(i, f.name)))
            rows.append("</tr>")
    elif hasattr(qs, '_meta'):
        headers.append("<tr>")
        rows.append("<tr>")
        for f in qs._meta.fields:
            headers.append("<th>%s</th>" % f.name)
            rows.append("<td>%s</td>" % break_text(getattr(qs, f.name)))
        headers.append("</tr>")
        rows.append("</tr>")
    else:
        raise
    return "\n".join(headers + rows)

def set_as_table2(qs):
    """
    Return a query set as an HTML table of attribute/value pairs without <table> tags.
    """
    first = True
    headers = ["<tr>", "<th>ATTRIBUTE</th>", "<th>VALUE</th>", "</tr>"]
    rows = []

    if isinstance(qs, QuerySet):
        for i in qs:
            if first:
                first = False
                for f in i._meta.fields:
                    rows.append("<tr>")
                    rows.append("<td><b>%s</b></td>" % f.name)
                    rows.append("<td>%s</td>" % break_text(getattr(i, f.name)))
                    rows.append("</tr>")
    elif hasattr(qs, '_meta'):
        for f in qs._meta.fields:
            rows.append("<tr>")
            rows.append("<td><b>%s</b></td>" % f.name)
            rows.append("<td>%s</td>" % break_text(getattr(qs, f.name)))
            rows.append("</tr>")
    else:
        raise
    return "\n".join(headers + rows)

def set_as_form(request, tbl_name, ucan_station_id = None):
    if ucan_station_id is None:
        if request.POST:
            form_call = "%sForm(request.POST)" % tbl_name
        else:
            form_call = "%sForm(initial={'tble_name': %s})" % ( tbl_name, tbl_name )
    else:
        tbl_call = "%s.objects.get(ucan_station_id=%s)" % ( tbl_name, ucan_station_id )
        tbl = eval(tbl_call)
        if request.POST:
            form_call = "%sForm(request.POST, instance = %s )" % ( tbl_name, tbl )
        else:
            form_call = "%sForm(initial={'tble_name': %s})" % ( tbl_name, tbl_name )
    form = eval(form_call)
    if form.is_valid():
        form.save()
        print "Information safed"
    return form

def set_as_dict(qs):
    """
    Return a query set as a dictionary of key value pairs.
    """
    first = True
    dic = {}

    if isinstance(qs, QuerySet):
        for i in qs:
            if first:
                first = False
                for f in i._meta.fields:
                    dic[f.name] = getattr(i, f.name)
    elif hasattr(qs, '_meta'):
        for f in qs._meta.fields:
            dic[f.name] = getattr(qs, f.name)
    else:
        raise
    return dic

def get_keys(q):
    """
    Return the keys of a query as list
    """
    L = []
    if hasattr(q, '_meta'):
       for f in q._meta.fields:
           L.append(f.name)
    return L

def break_text(s,num=60,sep="<br />"):
    """ Return string s with separator every num words."""
    from django.utils.text import wrap
    from django.utils.safestring import mark_safe
    return wrap(mark_safe(s), num).replace('\n', sep)
