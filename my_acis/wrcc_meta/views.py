# Create your views here.
#Python imports
import datetime
from collections import defaultdict
import inspect
import os

#django Imports
from django.template import RequestContext
#from django.contrib.auth.models import User
#from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.db.models.query import QuerySet

#project/app imports
import models
import wrcc_meta.forms as mforms

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
import WRCCUtils


####################
#Useful tables/dicts
#####################

'''
primary_tables = { 'Station': models.Station, 'StationLocation': models.StationLocation, 'StationNetwork': models.StationNetwork, 'StationSubnetwork':models.StationSubnetwork, 'StationAltName': models.StationAltName, 'StationTimeZone': models.StationTimeZone, 'StationClimDiv': models.StationClimDiv, 'StationCounty': models.StationCounty,'StationDigital': models.StationDigital, 'StationEquipment': models.StationEquipment, 'StationMaintenance':models.StationMaintenance, 'StationPhysical': models.StationPhysical}
'''

primary_tables = {
    'Station': models.Station,
    'StationNetwork':models.StationNetwork,
    'StationLocation': models.StationLocation,
    'StationTimeZone': models.StationTimeZone,
    'StationClimDiv': models.StationClimDiv,
    'StationCounty': models.StationCounty,
}
secondary_tables = {
    'Variable': models.Variable,
    'StationDigital': models.StationDigital
}

common_keys =['begin_date_flag', 'begin_date', 'end_date_flag', 'end_date', 'history_flag', 'src_quality_code','last_updated','updated_by']
stn_keys  = ['ucan_station_id','station_best_name','country_key','fips_country_code','state','fips_state_abbr','fips_state_code']
key_list = {
    'Station': stn_keys + common_keys,
    'StationLocation': ['ucan_station_id','latitude','longitude','unit_key','best_elevation'] + common_keys[0:5] + ['src_quality_flag'] + common_keys[6:],
    'StationTimeZone': ['ucan_station_id', 'time_zone'] + common_keys,
    'StationClimDiv': ['ucan_station_id', 'clim_div','clim_div_code','fips_state_code','fips_state_abbr','ncdc_state_code'] + common_keys,
    'StationCounty': ['ucan_station_id','county','fips_state_code','fips_county_code','county_name'] + common_keys,
    'StationNetwork':['ucan_station_id','network_station_id','id_type'] + common_keys,
    'StationDigital': ['ucan_station_id','network_station_id','network_id','begin_date','end_date'],
    'Variable':['ucan_station_id','network_station_id','network','var_major_id','var_minor_id','begin_date','end_date']
}

load_tables_dir = '/www/apps/csc/dj-projects/my_acis/media/meta-load-tables/'
#load_tables_dir = '/tmp/'

load_tables = {
    'Station': 'raws_station.load',
    'StationLocation': 'raws_station_location.load',
    'StationTimeZone': 'raws_station_time_zone.load',
    'StationClimDiv': 'raws_station_climate_division.load',
    'StationCounty': 'raws_station_county.load',
    'StationNetwork':'raws_station_network.load',
    'StationDigital':'raws_station_digital.load',
    'Variable':'raws_variable.load'
}

today = datetime.datetime.today()
today_yr = str(today.year)
today_month = str(today.month)
if len(today_month) ==1:today_month='0'+today_month
today_month_word = datetime.date(int(today_yr),int(today_month) , 1).strftime('%B')
today_day = str(today.day)
if len(today_day) ==1:today_day='0'+today_day
#2261 station but maybe more
with open('/www/apps/csc/dj-projects/my_acis/media/json/lat_lon_stns_2.json', 'r') as f:
    lat_lon_stations = eval(f.read())

lat_lon_list = [key for key in lat_lon_stations.keys()]


def home_view(request):
    context = {
        'state_choices': mforms.STATE_CHOICES,
        'title': "Metadata Home",
        'lat_lon_list': lat_lon_list
    }
    return render_to_response('wrcc_meta/home.html', context, context_instance=RequestContext(request))



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
    return render_to_response('wrcc_meta/results.html', context, context_instance=RequestContext(request))


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
    return render_to_response('wrcc_meta/results.html', context, context_instance=RequestContext(request))

def by_name_and_state(request):
    state_key = request.GET.get('state_key', None)
    q = request.GET.get('q', '')
    if state_key is None and state_key is None:
        stations = []
    else:
        stations = models.Station.objects.filter(state=int(state_key), station_best_name__icontains=q).order_by('station_best_name')
    context = {
        'stations': stations,
        'title': "Station Name and State Search Results",
    }
    return render_to_response('wrcc_meta/results.html', context, context_instance=RequestContext(request))
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
    return render_to_response('wrcc_meta/results.html', context, context_instance=RequestContext(request))

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
    return render_to_response('wrcc_meta/results.html', context, context_instance=RequestContext(request))


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
    return render_to_response('wrcc_meta/station_detail.html', context, context_instance=RequestContext(request))


def station_tables(request):
    ucan_id_list = request.GET.getlist('ucan_id', [])
    tbl_done_list = request.GET.getlist('tbl_done', [])
    context = {
        'title': "Primary tables for this Station",
        'tbl_done_list':tbl_done_list
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
    return render_to_response('wrcc_meta/station_tables.html', context, context_instance=RequestContext(request))

def station_tables_merge(request):
    tbl_name = request.GET.get('tbl_name', None)
    ucan_id_list = request.GET.getlist('ucan_id', [])
    ucan_id_list = [str(uid) for uid in ucan_id_list]
    tbl_done_list = request.GET.getlist('tbl_done', [])
    context = {
        'title': tbl_name + ' Table Merge Tool',
        'tbl_done_list':tbl_done_list
    }
    tbl_done = False
    if tbl_name in tbl_done_list:tbl_done=True;context['tbl_done']=True
    if not tbl_name or not ucan_id_list:
        return render_to_response('wrcc_meta/station_tables_merge.html', context, context_instance=RequestContext(request))
    context['ucan_id_list'] = ucan_id_list
    context['tbl_name'] = tbl_name
    table_dicts = {}
    #Find table instances for each ucan id
    ucan_station_id_acis = None
    ucan_station_id_form = None
    wrcc_id = None
    network_station_ids_dict = {}
    for idx, ucan_id in enumerate(ucan_id_list):
        if int(ucan_id) < 1000000:
            ucan_station_acis = ucan_id
        else:
            wrcc_id = ucan_id
        table_dicts[ucan_id] = []
        obj = primary_tables[tbl_name]
        if tbl_name == 'StationNetwork':
            network_station_ids_dict[ucan_id] = []
        instances = obj.objects.filter(ucan_station_id=ucan_id)
        for i, instance in enumerate(instances):
            inst_list = convert_query_set(instance,'python_list')
            table_dicts[ucan_id].append(inst_list)
            #Get network_station_id for Variable, StationDigital tables
            #if we are looking at the StationNetwork table
            if tbl_name == 'StationNetwork':
                inst_dict = convert_query_set(instance,'python_dict')
                network_station_ids_dict[ucan_id].append(str(inst_dict['network_station_id']))
    context['network_station_ids_dict'] = network_station_ids_dict

    #query station_table entries in db for wrcc id entry
    if wrcc_id:
        station = convert_query_set(models.Station.objects.filter(ucan_station_id=wrcc_id), 'python_dict')
        if ucan_station_id_acis:
            ucan_station_id_form = ucan_station_id_acis
        else:
            ucan_station_id_form = ucan_id_list[0]
    else:
        if ucan_station_id_acis:
            station = convert_query_set(models.Station.objects.filter(ucan_station_id=ucan_station_id_form), 'python_dict')
            ucan_station_id_form = ucan_station_id_acis
        else:
            station = convert_query_set(models.Station.objects.filter(ucan_station_id=ucan_id_list[0]), 'python_dict')
            ucan_station_id_form = ucan_id_list[0]

    #Reorder results for easy html formatting
    max_instances = max([len(table_dicts[uid]) for uid in ucan_id_list])
    if  max_instances == 0:
        #set up blank form for table
        #get station table for start, end dates and data flags
        init = {
            'ucan_station_id':ucan_station_id_form,
            'begin_date':WRCCUtils.convert_db_dates(station['begin_date']),
            'end_date':WRCCUtils.convert_db_dates(station['end_date']),
            'begin_date_flag':station['begin_date_flag'],
            'end_date_flag':station['end_date_flag'],
            'history_flag':station['history_flag'],
            'src_quality_code':station['src_quality_code'],
            'updated_by': 'WRCCsync',
            'last_updated':today_yr + '-' + today_month + '-' + today_day
            }
        form_class = getattr(mforms, tbl_name + 'Form')
        form = form_class(initial=init)
        for field in form.fields:
            if form[field].value():
                table_dicts[ucan_station_id_form].append([str(field), str(form[field].value())])
            else:
                table_dicts[ucan_station_id_form].append([str(field),''])
        results=[[table_dicts[ucan_station_id_form]]]
    else:
        #Format for html display
        results = [[[] for idx in range(len(ucan_id_list)+1)] for inst in range(max_instances)]
        for inst in range(max_instances):
            for idx, ucan_id in enumerate(ucan_id_list):
                if len(table_dicts[ucan_id]) > inst:
                    results[inst][idx]=table_dicts[ucan_id][inst]
                    if ucan_id >1000000:
                        results[inst][-1] = []
                        for idx, key_val in enumerate(table_dicts[ucan_id][inst]):
                            results[inst][-1].append([key_val[0], key_val[1]])
            if not results[inst][-1]:
                for idx, key_val in enumerate(table_dicts[ucan_id_list[-1]][inst]):
                    results[inst][-1].append([key_val[0], key_val[1]])
            #Overwrite editable form with wrcc values if they exist
            #and replace updated_by, last _updated and ucan_id
            context['x'] =  WRCCUtils.convert_db_dates(station['begin_date'])
            if tbl_done:
                for idx, key_val in enumerate(results[inst][-1]):
                    results[inst][-1][idx][1] = ''
            else:
                for idx, key_val in enumerate(results[inst][-1]):
                    if str(key_val[0]) == 'ucan_station_id': results[inst][-1][idx][1]= ucan_station_id_form
                    if str(key_val[0]) == 'begin_date_flag': results[inst][-1][idx][1]= station['begin_date_flag']
                    if str(key_val[0]) == 'begin_date': results[inst][-1][idx][1]= WRCCUtils.convert_db_dates(station['begin_date'])
                    if str(key_val[0]) == 'end_date_flag': results[inst][-1][idx][1]= station['end_date_flag']
                    if str(key_val[0]) == 'end_date': results[inst][-1][idx][1]= WRCCUtils.convert_db_dates(station['end_date'])
                    if str(key_val[0]) == 'history_flag': results[inst][-1][idx][1]= station['history_flag']
                    if str(key_val[0]) == 'src_quality_code': results[inst][-1][idx][1]= station['src_quality_code']
                    if str(key_val[0]) == 'last_updated':results[inst][-1][idx][1] = today_yr + '-' + today_month + '-' + today_day
                    if str(key_val[0]) == 'updated_by':results[inst][-1][idx][1]= 'WRCCSync'
    context['results'] = results

    #Write merge information to metadata.load file
    if 'form_merge' in request.POST:
        form_idx = int(request.POST['form_id']) - 1
        #Override merge table with new entries
        for key in request.POST:
            for idx,key_val in enumerate(results[form_idx][-1]):
                if str(key) == key_val[0]:
                    results[form_idx][-1][idx][1] = str(request.POST[key])
        meta_str = ''
        with open(load_tables_dir + load_tables[tbl_name],'a+') as f:
            for idx,key in enumerate(key_list[tbl_name]):
                if idx != len(key_list[tbl_name]) - 1:
                    meta_str+=str(request.POST[key]) + '|'
                else:
                    meta_str+=str(request.POST[key]) + '\n'
            f.write(meta_str)
        #Double check
        #os.chmod(load_tables_dir + load_tables[tbl_name], 0777)
        with open(load_tables_dir + load_tables[tbl_name], 'r') as f:
            if f.readlines()[-1] == meta_str:
                context['merge_successful'] = True
                context['form_id'] = int(request.POST['form_id'])
    return render_to_response('wrcc_meta/station_tables_merge.html', context, context_instance=RequestContext(request))

def sub_tables(request):
    tbl_name = request.GET.get('tbl_name', None)
    ucan_id = request.GET.get('ucan_id', None)
    network_station_ids_list = request.GET.getlist('network_station_id', [])
    network_station_ids_list = [str(n_id) for n_id in network_station_ids_list]
    context = {
        'title': 'Table ADD Tool',
        'tbl_name': tbl_name,
        'network_station_ids_list':network_station_ids_list,
        'ucan_id': ucan_id
    }
    obj = secondary_tables[tbl_name]
    table_dicts = {}
    max_instances = 0
    for idx, network_station_id in enumerate(network_station_ids_list):
        table_dicts[network_station_id] = []
        instances = obj.objects.filter(network_station_id=network_station_id)
        if len(instances) > max_instances:max_instances = len(instances)
        for inst_idx, inst in enumerate(instances):
            inst_list = convert_query_set(inst,'python_list')
            table_dicts[network_station_id].append(inst_list)
    #Format for html loop
    station = convert_query_set(models.Station.objects.filter(ucan_station_id=ucan_id), 'python_dict')
    init = {
        'ucan_station_id':ucan_id,
        'begin_date':WRCCUtils.convert_db_dates(station['begin_date']),
        'end_date':WRCCUtils.convert_db_dates(station['end_date']),
    }
    form_class = getattr(mforms, tbl_name)
    form = form_class()
    if max_instances == 0:
        results = [[[] for idx in range(len(network_station_ids_list)+1)] for inst in range(1)]
        for idx, network_station_id in enumerate(network_station_ids_list):
            init['network_station_id'] = network_station_id
            for key, val in form.__dict__.iteritems():
                if key[0]!= '_':
                    if key in init.keys():
                        results[0][idx].append([key, init[key]])
                    else:
                        results[0][idx].append([key, val])
        #results[0][-1] = results[0][-2]
        for idx in range(len(results[0]) - 1):
            results[0][idx] = []
    else:
        results = [[[] for idx in range(len(network_station_ids_list)+1)] for inst in range(max_instances)]
        for inst in range(max_instances):
            for idx, network_station_id in enumerate(network_station_ids_list):
                if len(table_dicts[network_station_id]) > inst:
                    results[inst][idx]=table_dicts[network_station_id][inst]
                else:
                    continue
        #add forms at end of each row
        for idx, network_station_id in enumerate(network_station_ids_list):
            if not table_dicts[network_station_id]:
                init['network_station_id'] = network_station_id
                for key, val in form.__dict__.iteritems():
                    if key[0]!= '_':
                        if key in init.keys():
                            results[idx][-1].append([key, init[key]])
                        else:
                            results[idx][-1].append([key, val])
            else:
                results[idx][-1]=results[idx][idx]

    #Write to metadata load file
    if 'form_add' in request.POST or 'form_edit' in request.POST:
        form_idx = int(request.POST['form_id']) - 1
        for key in request.POST:
            for idx,key_val in enumerate(results[form_idx][-1]):
                if str(key) == key_val[0]:
                    results[form_idx][-1][idx][1] = str(request.POST[key])
        meta_str = ''
        with open(load_tables_dir + load_tables[tbl_name],'a+') as f:
            for idx,key in enumerate(key_list[tbl_name]):
                if idx != len(key_list[tbl_name]) - 1:
                    end_char = '|'
                else:
                    end_char = '\n'
                try:
                    meta_str+=str(request.POST[key]) + end_char
                except:
                    #WTF?? Some db Variable tables have 'network' key but some have 'network_id' key
                    #instead
                    if key == 'network':
                        meta_str+=str(request.POST['network_id']) + end_char

            if 'form_edit' in request.POST:
                pass
            else:
                f.write(meta_str)
        #Double check
        #os.chmod(load_tables_dir + load_tables[tbl_name], 0777)
        with open(load_tables_dir + load_tables[tbl_name], 'r') as f:
            if f.readlines()[-1] == meta_str:
                context['merge_successful'] = True
                context['form_id'] = int(request.POST['form_id'])
    context['results'] = results
    return render_to_response('wrcc_meta/sub_tables.html', context, context_instance=RequestContext(request))

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

    return render_to_response('wrcc_meta/add.html', context, context_instance=RequestContext(request))


def station_tables_add(request):
    tbl_name = request.GET.get('tbl_name', None)
    context = {
        'title': tbl_name + 'Add Tool'
    }
    return render_to_response('wrcc_meta/station_tables_add.html', context, context_instance=RequestContext(request))

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
    context['station_maintenance'] = convert_query_set(models.StationMaintenance.objects.filter(ucan_station_id=ucan_id), 'table')
    return render_to_response('wrcc_meta/station_maintenance.html', context, context_instance=RequestContext(request))

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
    context['station_physical'] = convert_query_set(models.StationPhysical.objects.filter(ucan_station_id=ucan_id), 'table')
    return render_to_response('wrcc_meta/station_physical.html', context, context_instance=RequestContext(request))

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
    context['station_equipment'] = convert_query_set(models.StationEquipment.objects.filter(ucan_station_id=ucan_id), 'table')
    return render_to_response('wrcc_meta/station_equipment.html', context, context_instance=RequestContext(request))

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
            try:
                rows.append("<td>%s</td>" % break_text(getattr(qs, f.name)))
                out_dict[f.name] = getattr(qs, f.name)
                out_list.append([f.name, getattr(qs, f.name)])
            except:
                pass
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
