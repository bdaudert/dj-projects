# Create your views here.
#Python imports
import datetime
from collections import defaultdict
import inspect

#django Imports
from django.template import RequestContext
#from django.contrib.auth.models import User
#from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
#from django.views.generic.list_detail import object_detail, object_list
from django.db.models.query import QuerySet

#project/app imports
import models
import my_meta.forms as mforms

#Imports for direct query to database
import sys
import sqlalchemy as SA
import sqlalchemy.orm as SAO
import wea
from acis_db import (
        get_session,
        Station,
        Subnetwork,
        StationLocation,
        )

####################
#Useful tables/dicts
#####################

'''
primary_tables = { 'Station': models.Station, 'StationLocation': models.StationLocation, 'StationNetwork': models.StationNetwork, 'StationSubnetwork':models.StationSubnetwork, 'StationAltName': models.StationAltName, 'StationTimeZone': models.StationTimeZone, 'StationClimDiv': models.StationClimDiv, 'StationCounty': models.StationCounty,'StationDigital': models.StationDigital, 'StationEquipment': models.StationEquipment, 'StationMaintenance':models.StationMaintenance, 'StationPhysical': models.StationPhysical}
'''

primary_tables = {
    'Station': models.Station,
    'StationLocation': models.StationLocation,
    'StationAltName': models.StationAltName,
    'StationTimeZone': models.StationTimeZone,
    'StationClimDiv': models.StationClimDiv,
    'StationCounty': models.StationCounty,
}
sub_tables = { 'Variable': models.Variable, 'Network': models.Network, 'StationDigital': models.StationDigital }

month_list = ['']

today = datetime.datetime.today()
today_yr = str(today.year)
today_month = str(today.month)
today_month_word = datetime.date(int(today_yr),int(today_month) , 1).strftime('%B')
today_day = str(today.day)

#2261 station but maybe more
with open('/www/apps/csc/dj-projects/my_acis/media/json/lat_lon_stns_2.json', 'r') as f:
    lat_lon_stations = eval(f.read())

#lat_lon_stations = {'49.02, -113.62': [1003210, 42832], '50.17, -114.72': [1003488, 42816], '49.82, -114.63': [1003325, 42834], '48.42, -123.23': [1011288, 41023], '38.14, -109.61': [1013591, 61851, 1018197], '49.62, -113.82': [1010326, 42609], '49.02, -113.65': [1003214, 42778], '49.58, -114.42': [1009742, 1012668], '63.25, -130.03': [1009743, 42100], '64.85, -147.80': [1014039, 1002370, 28876, 1017151, 20953, 20954], '47.87, -117.03': [1014451, 1003073, 1003037, 34082], '50.27, -117.82': [1009738, 41811, 41812, 26513], '51.08, -114.22': [1011287, 42639], '59.67, -151.65': [1014068, 20609], '46.22, -72.65': [1009739, 45189], '50.63, -115.28': [1003489, 42868], '50.95, -115.18': [1009740, 42873], '51.42, -105.25': [1008944, 43265], '49.62, -110.32': [1003135, 1003059, 42677], '52.93, -66.87': [1009343, 26628, 46254], '52.18, -127.47': [1010884, 41302, 26503], '61.92, -113.73': [1010327, 42162], '59.68, -151.37': [1014444, 1014457, 1011355, 1012263], '45.32, -75.67': [1010867, 1012975, 26838, 26832, 44394], '38.25, -75.16': [1004331, 1013743]}


lat_lon_list = [key for key in lat_lon_stations.keys()]


def home_view(request):
    context = {
        'state_choices': mforms.STATE_CHOICES,
        'title': "Metadata Home",
        'lat_lon_list': lat_lon_list
    }
    return render_to_response('my_meta/home.html', context, context_instance=RequestContext(request))



def by_state(request):
    state_key = request.GET.get('state_key', None)
    if state_key is None:
        stations = []
    else:
        stations = models.Station.objects.filter(state=int(state_key)).order_by('station_best_name')


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
        stations = models.Station.objects.filter(station_best_name__icontains=q).order_by('station_best_name')

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
        stations = models.StationNetwork.objects.filter(network_station_id__icontains=q)
        ucan_ids = [s.ucan_station_id for s in stations]
        stations = models.Station.objects.filter(ucan_station_id__in=ucan_ids)
    context = {
        'stations': stations,
        'title': "Station ID Search Results",
    }
    return render_to_response('my_meta/results.html', context, context_instance=RequestContext(request))

def by_location(request):
    lat = request.GET.get('lat', None)
    lon = request.GET.get('lon', None)
    lat_lon = request.GET.get('lat_lon', None)
    delta = .02
    if lat_lon:
        try:
            lat = float(lat_lon.split(',')[0]);lon = float(lat_lon.split(',')[1])
        except:
            lat = None;lon=None
    elif lat and lon:
        try:
            lat = float(lat);lon = float(lon)
        except:
            lat = None;lon=None

    if lat and lon:
        stations = models.StationLocation.objects.filter(latitude__lte=lat+delta, latitude__gte=lat-delta,
                                                    longitude__lte=lon+delta, longitude__gte=lon-delta,
                                                    history_flag__icontains='L'
                                                )
        ucan_ids = [s.ucan_station_id for s in stations]
        stations = models.Station.objects.filter(ucan_station_id__in=ucan_ids)
    else:
        stations = []

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
        context['station'] = convert_query_set(models.Station.objects.get(pk=ucan_id), 'table')
        context['station_location'] = convert_query_set(models.StationLocation.objects.filter(ucan_station_id=ucan_id), 'table')
        context['station_maintenance'] = convert_query_set(models.StationMaintenance.objects.filter(ucan_station_id=ucan_id), 'table')
        context['station_equipment'] = convert_query_set(models.StationEquipment.objects.filter(ucan_station_id=ucan_id), 'table')
        context['station_physical'] = convert_query_set(models.StationPhysical.objects.filter(ucan_station_id=ucan_id), 'table')
        '''
        context['station'] = set_as_table(models.Station.objects.get(pk=ucan_id))
        context['station_location'] = set_as_table(models.StationLocation.objects.filter(ucan_station_id=ucan_id))
        context['station_maintenance'] = set_as_table(models.StationMaintenance.objects.filter(ucan_station_id=ucan_id))
        context['station_equipment'] = set_as_table(models.StationEquipment.objects.filter(ucan_station_id=ucan_id))
        context['station_physical'] = set_as_table(models.StationPhysical.objects.filter(ucan_station_id=ucan_id))
        '''
    return render_to_response('my_meta/station_detail.html', context, context_instance=RequestContext(request))

'''
def station_tables_nina(request):
    ucan_id_list = request.GET.getlist('ucan_id', [])
    context = {
        'title': "Primary tables for this Station"
    }
    context['ucan_id_list'] = ucan_id_list
    if ucan_id_list:
        #put in list
        table_dict = defaultdict(list)
        for name, obj in primary_tables.iteritems():
            for idx, ucan_id in enumerate(ucan_id_list):
                instances = obj.objects.filter(ucan_station_id=ucan_id)
                for i, instance in enumerate(instances):
                    inst_name = '%s_%d' % (name, i)
                    form = set_as_form(request, name, q=instance, ucan_station_id=ucan_id)
                    if inst_name in table_dict.keys():
                        table_dict[inst_name].append(form)
                    else:
                        table_dict[inst_name] =['No Table' for k in range(idx)]
                        table_dict[inst_name].append(form)
        context['table_dict'] = dict(table_dict)
    return render_to_response('my_meta/station_tables.html', context, context_instance=RequestContext(request))
'''

def station_tables(request):
    ucan_id_list = request.GET.getlist('ucan_id', [])
    context = {
        'title': "Primary tables for this Station"
    }
    context['ucan_id_list'] = ucan_id_list
    if ucan_id_list:
        #put in list
        table_dict = defaultdict(list)
        results_dict = {}
        for name, obj in primary_tables.iteritems():
            results_dict[name] = []
            for idx, ucan_id in enumerate(ucan_id_list):
                instances = obj.objects.filter(ucan_station_id=ucan_id)
                results_dict[name].append(len(instances))
                context['results_dict']= results_dict
    return render_to_response('my_meta/station_tables.html', context, context_instance=RequestContext(request))

def station_tables_merge(request):
    table_name = request.GET.get('tbl_name', None)
    ucan_id_list = request.GET.getlist('ucan_id', [])
    context = {
        'title': table_name + ' Table Merge Tool'
    }
    if not table_name or not ucan_id_list:
        return render_to_response('my_meta/station_tables_merge.html', context, context_instance=RequestContext(request))
    context['ucan_id_list'] = ucan_id_list
    context['table_name'] = table_name
    table_instances = {}
    table_dicts = {}
    #Find table instances for each ucan id
    ucan_station_id_form = ucan_id_list[0]
    for idx, ucan_id in enumerate(ucan_id_list):
        if int(ucan_id) < 100000:
            ucan_station_id_form = ucan_id
        table_instances[ucan_id] = []
        table_dicts[ucan_id] = []
        obj = primary_tables[table_name]
        instances = obj.objects.filter(ucan_station_id=ucan_id)
        for i, instance in enumerate(instances):
            inst_name = '%s_%d' % (table_name, i)
            form = set_as_form(request, table_name, q=instance, ucan_station_id=ucan_id)
            inst_list = convert_query_set(instance,'python_list')
            inst_dict = convert_query_set(instance,'python_dict')
            table_dicts[ucan_id].append(inst_list)
            table_instances[ucan_id].append(form)
    context['table_dicts']= table_dicts
    #Reorder results for easy html formatting
    max_instances = max([len(table_instances[uid]) for uid in ucan_id_list])
    if  max_instances == 0:
        return render_to_response('my_meta/station_tables_merge.html', context, context_instance=RequestContext(request))
    results = [[[] for idx in range(len(ucan_id_list)+1)] for inst in range(max_instances)]
    results_2 = [[[] for idx in range(len(ucan_id_list)+1)] for inst in range(max_instances)]
    for inst in range(max_instances):
        wrcc_id = None
        for idx, ucan_id in enumerate(ucan_id_list):
            if len(table_dicts[ucan_id]) > inst:
                results[inst][idx]=table_instances[ucan_id][inst]
                results[inst][-1]=table_instances[ucan_id][inst]
                results_2[inst][idx]=table_dicts[ucan_id][inst]
                results_2[inst][-1]=table_dicts[ucan_id][inst]
                #Check if WRCC entry is in list, if so
                #we want to use this entry as the editable form at the end of
                #the page. If not, we choose the first ucan_id
                if int(ucan_id) >=1000000:
                    wrcc_id = ucan_id
        #Overwrite editable form with wrcc values if they exist
        #and replace updated_by, last _updated and ucan_id
        if wrcc_id:
            results[inst][-1]= table_instances[wrcc_id][inst]
            results_2[inst][-1]= table_dicts[wrcc_id][inst]
            context['test'] = results_2[inst][-1]
            for idx, key_val in enumerate(results_2[inst][-1]):
                if str(key_val[0]) == 'ucan_station_id':pass
                if str(key_val[0]) == 'ucan_station_id': results_2[inst][-1][idx][1]= ucan_station_id_form
                if str(key_val[0]) == 'updated_by':results_2[inst][-1][idx][1] = 'WRCCsync'
                if str(key_val[0]) == 'last_updated':results_2[inst][-1][idx][1] = today_month_word + ' ' + today_day + ', ' + today_yr
        context['results'] = results
        context['results_2'] = results_2
    return render_to_response('my_meta/station_tables_merge.html', context, context_instance=RequestContext(request))

def station_tables_add(request):
    table_name = request.GET.get('tbl_name', None)
    context = {
        'title': table_name + 'Add Tool'
    }
    return render_to_response('my_meta/station_tables_add.html', context, context_instance=RequestContext(request))

def station_tables_old(request):
    ucan_id = request.GET.get('ucan_id', None)
    context = {
        'title': "Primary tables for this Station"
    }
    if ucan_id:
        ucan_id = int(ucan_id)
        table_dir = defaultdict(list)
        errors = defaultdict(dict)
        for name, obj in primary_tables.iteritems():
            instances = obj.objects.filter(ucan_station_id=ucan_id)
            if not instances:
                table_dir[name]= []
                continue
            for i, instance in enumerate(instances):
                inst_name = '%s_%d' % (name, i)
                table_dir[name].append(inst_name)
        context['ucan_station_id'] = ucan_id
        context['table_dir'] = dict(table_dir)

    return render_to_response('my_meta/station_tables.html', context, context_instance=RequestContext(request))

def sub_tables(request, tbl_name, tbl_id):
    ucan_id = request.GET.get('ucan_id', None)
    context = {
        'title': "Secondary tables for this Station"
    }
    context['primary_table'] = "%s_%d" % (tbl_name, int(tbl_id))
    if ucan_id:
        tables = {}
        errors = defaultdict(dict)
        tbl_name_idxed = "%s_%d" % ( tbl_name, int(tbl_id))
        context['primary_table_name'] = tbl_name_idxed
        obj = primary_tables[tbl_name]
        primary_inst = obj.objects.filter(ucan_station_id=ucan_id)[int(tbl_id) - 1]
        form = set_as_form(request, tbl_name, q=primary_inst, ucan_station_id=ucan_id)
        primary_table = form
        context['primary_table'] = primary_table
        errors[tbl_name_idxed] = form.errors
        if tbl_name == "StationNetwork":
            var_s = models.Variable.objects.filter(ucan_station_id=ucan_id, network_station_id=primary_inst.network_station_id)
            for j, v in enumerate(var_s):
                var_name = 'Variable_%d_%d' % (int(tbl_id), j)
                form = set_as_form(request, 'Variable', q=v, ucan_station_id=ucan_id)
                tables[var_name] = form
                errors[var_name] = form.errors
        context['ucan_station_id'] = ucan_id
        context['errors'] = dict(errors)
        context['tables'] = tables
    return render_to_response('my_meta/sub_tables.html', context, context_instance=RequestContext(request))

def add(request):
    tbl_name = request.GET.get('tbl_name', None)
    ucan_id = request.GET.get('ucan_id', None)
    context = {
        'title': "Add"
    }
    form = set_as_form(request, tbl_name, init={'ucan_station_id': ucan_id})
    if form and not form.errors:
        context['saved'] = "Information saved :-)."
    else:
        context['saved'] = "Following errors occurred:"
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
        form = mforms.StationMaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            context['saved'] = "Information saved."
        else:
            context['saved'] = "Information NOT saved."
    else:
        (form, ucan_found) = mforms.StationMaintenanceForm(initial={'ucan_station_id': ucan_id})
    context['ucan_found'] = ucan_found
    context['form'] = form
    context['station_maintenance'] = set_as_table(models.StationMaintenance.objects.filter(ucan_station_id=ucan_id))
    return render_to_response('my_meta/station_maintenance.html', context, context_instance=RequestContext(request))

#@login_required
def station_physical(request, ucan_id):
    ucan_id = int(ucan_id)
    context = {
        'title': "Station Physical",
        'ucan_id': ucan_id,
    }
    if request.POST:
        form = mforms.StationPhysicalForm(request.POST)
        if form.is_valid():
            form.save()
            context['saved'] = "Information saved."
    else:
        form = mforms.StationPhysicalForm(initial={'ucan_station_id': ucan_id})

    context['form'] = form
    context['station_physical'] = set_as_table(models.StationPhysical.objects.filter(ucan_station_id=ucan_id))
    return render_to_response('my_meta/station_physical.html', context, context_instance=RequestContext(request))

#@login_required
def station_equipment(request, ucan_id):
    ucan_id = int(ucan_id)
    context = {
        'title': "Station Equipment",
        'ucan_id': ucan_id,
    }
    if request.POST:
        form = mforms.StationEquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            context['saved'] = "Information saved."
    else:
        form = mforms.StationEquipmentForm(initial={'ucan_station_id': ucan_id})

    context['form'] = form
    #context['station_equipment'] = set_as_table(models.StationEquipment.objects.filter(ucan_station_id=ucan_id))
    context['station_equipment'] = convert_query_set(models.StationEquipment.objects.filter(ucan_station_id=ucan_id), 'table')
    return render_to_response('my_meta/station_equipment.html', context, context_instance=RequestContext(request))

#
# Utility functions
#

def convert_query_set(qs, obj):
    """
    Return a query set as obj.
    Obj can be one out of table, python_dict
    """
    if obj not in ['table', 'python_dict', 'python_list']:
        return qs
    first = True
    headers = ["<tr>", "<th>ATTRIBUTE</th>", "<th>VALUE</th>", "</tr>"]
    rows = []
    out_dict = {}
    out_list = []
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
                out_dict[f.name] = getattr(i, f.name)
                out_list.append([f.name, getattr(i, f.name)])
            rows.append("</tr>")
    elif hasattr(qs, '_meta'):
        headers.append("<tr>")
        rows.append("<tr>")
        for f in qs._meta.fields:
            headers.append("<th>%s</th>" % f.name)
            rows.append("<td>%s</td>" % break_text(getattr(qs, f.name)))
            out_dict[f.name] = getattr(qs, f.name)
            out_list.append([f.name, getattr(qs, f.name)])
        headers.append("</tr>")
        rows.append("</tr>")
    else:
        raise

    if obj == 'table':
        return "\n".join(headers + rows)
    elif obj == 'python_dict':
        return out_dict
    elif obj == 'python_list':
        return out_list
    else:
        return qs

'''
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
'''

def set_as_form(request, tbl_name, q= None,  ucan_station_id = None, init = None):
    form_name = "%sForm" % tbl_name
    form_class = getattr(mforms, form_name)
    if ucan_station_id is None and q is None:
        if request.POST:
            form = form_class(request.POST)
            if form.is_valid():
                form.save()
        else:
            if init is not None:
                form = form_class(initial=init)
            else:
                form = form_class(initial={'tble_name': tbl_name})
    else:
        if q is None or ucan_station_id is None:
            raise

        if request.POST:
            form = form_class(request.POST,instance=q)
            if form.is_valid():
                form.save()
        else:
            form = form_class(instance=q)
    return form

def break_text(s,num=60,sep="<br />"):
    """ Return string s with separator every num words."""
    from django.utils.text import wrap
    from django.utils.safestring import mark_safe
    return wrap(mark_safe(s), num).replace('\n', sep)
