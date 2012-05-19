# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from common import *

class Station(models.Model):
    ucan_station_id = models.IntegerField(primary_key=True)
    station_best_name = models.CharField(max_length=30)
    country_key = models.SmallIntegerField()
    fips_country_code = models.CharField(max_length=2)
    state = models.ForeignKey(State, db_column="state_key")
    fips_state_abbr = models.CharField(max_length=2)
    fips_state_code = models.CharField(max_length=2)
    begin_date_flag = models.CharField(max_length=2)
    begin_date = models.DateField()
    end_date_flag = models.CharField(max_length=2)
    end_date = models.DateField()
    history_flag = models.CharField(max_length=2)
    src_quality_code = models.CharField(max_length=5)
    last_updated = models.DateField()
    updated_by = models.CharField(max_length=8)
    remark = models.CharField(max_length=254)
    class Meta:
	app_label = 'meta'
        db_table = 'station'
    def __str__(self):
	return "[%s] %s" % (self.ucan_station_id, self.station_best_name)
    class Admin:
	list_display = ('ucan_station_id','station_best_name','state','begin_date','end_date')
	list_filter = ('state',)
	search_fields = ('ucan_station_id','station_best_name')

class StationLocation(models.Model):
    ucan_station_id = models.IntegerField(primary_key=True) # Not the real pk
    longitude = models.FloatField()
    latitude =  models.FloatField()
    unit_key = models.SmallIntegerField()
    best_elevation = models.FloatField()
    begin_date_flag = models.CharField(max_length=2)
    begin_date = models.DateField()
    end_date_flag = models.CharField(max_length=2)
    end_date = models.DateField()
    history_flag = models.CharField(max_length=2)
    src_quality_flag = models.CharField(max_length=5)
    last_updated = models.DateField()
    updated_by = models.CharField(max_length=8)
    remark = models.CharField(max_length=254)
    class Meta:
	app_label = 'meta'
        db_table = 'station_location'
    def __str__(self):
	return "[ucan %s] %.4f %.4f" % (self.ucan_station_id, self.latitude, self.longitude)
    class Admin:
	list_display = ('ucan_station_id', 'latitude', 'longitude', 'best_elevation', 'begin_date', 'end_date')
	search_fields = ('ucan_station_id',)
    def get_station(self):
	return WrccStation.objects.get(pk=self.ucan_station_id)

class StationMaintenance(models.Model):
    id = models.AutoField(primary_key=True)
    ucan_station_id = models.IntegerField()
    maintenance_date = models.DateField()
    remark = models.TextField()
    class Meta:
	app_label = 'meta'
        db_table = 'station_maintenance'
    class Admin:
	list_display = ('ucan_station_id', 'maintenance_date')
	search_fields = ('ucan_station_id',)
    def __str__(self):
	return "[ucan %s] %s" % (self.ucan_station_id, self.maintenance_date)


class StationEquipment(models.Model):
    id = models.AutoField(primary_key=True)
    ucan_station_id = models.IntegerField()
    equipment_type = models.CharField(max_length=30)
    eq_manufacturer = models.CharField(max_length=30)
    eq_model = models.CharField(max_length=20)
    serial_num = models.CharField(max_length=20)
    eq_description = models.TextField()
    install_date = models.DateField()
    remove_date = models.DateField(null=True)
    ref_height = models.IntegerField()
    sampling_interval = models.CharField(max_length=10)
    remark = models.TextField()
    class Meta:
	app_label = 'meta'
        db_table = 'station_equipment'
    class Admin:
	pass
    def __str__(self):
	return "[ucan %s] %s" % (self.ucan_station_id, self.equipment_type)

class StationPhysical(models.Model):
    id = models.AutoField(primary_key=True)
    ucan_station_id = models.IntegerField()
    slope = models.IntegerField()
    aspect = models.IntegerField()
    gps = models.CharField(max_length=1)
    site_description = models.TextField()
    route_directions = models.TextField()
    remark = models.TextField()
    class Meta:
	app_label = 'meta'
        db_table = 'station_physical'
    class Admin:
	pass
    def __str__(self):
	return "[ucan %s] %s ..." % (self.ucan_station_id, str(self.site_description)[:80])


class StationAltName(models.Model):
    ucan_station_id = models.IntegerField(primary_key=True) # Not the real pk
    station_alt_name = models.CharField(max_length=30)
    name_type_key = models.SmallIntegerField()
    begin_date_flag = models.CharField(max_length=2)
    begin_date = models.DateField()
    end_date_flag = models.CharField(max_length=2)
    end_date = models.DateField()
    history_flag = models.CharField(max_length=2)
    src_quality_code = models.CharField(max_length=5)
    last_updated = models.DateField()
    updated_by = models.CharField(max_length=8)
    remark = models.CharField(max_length=254)
    def __str__(self):
	return "[ucan %s] %s" % (self.ucan_station_id, self.station_alt_name)
    class Admin:
	list_display = ('station_alt_name', 'ucan_station_id', 'begin_date', 'end_date')
	search_fields = ('station_alt_name', 'ucan_station_id')
    class Meta:
	app_label = 'meta'
        db_table = 'station_alt_name'

class StationCounty(models.Model):
    ucan_station_id = models.IntegerField(primary_key=True) # Not the real pk
    county = models.ForeignKey(County, db_column="county_key")
    fips_state_code =  models.CharField(max_length=2)
    fips_county_code = models.CharField(max_length=3)
    county_name = models.CharField(max_length=31)
    begin_date_flag = models.CharField(max_length=2)
    begin_date = models.DateField()
    end_date_flag = models.CharField(max_length=2)
    end_date = models.DateField()
    history_flag = models.CharField(max_length=2)
    src_quality_code = models.CharField(max_length=5)
    last_updated = models.DateField()
    updated_by = models.CharField(max_length=8)
    remark = models.CharField(max_length=254)
    def __str__(self):
	return "[ucan %s] %s" % (self.ucan_station_id, self.county)
    class Admin:
	list_display = ('ucan_station_id', 'county', 'begin_date', 'end_date')
	search_fields = ('ucan_station_id','county_name')
    class Meta:
	app_label = 'meta'
        db_table = 'station_county'

class StationNetwork(models.Model):
    ucan_station_id = models.IntegerField(primary_key=True) # Not the real pk
    network_station_id = models.CharField(max_length=20)
    id_type = models.ForeignKey(IdType, db_column="id_type_key")
    begin_date_flag = models.CharField(max_length=2)
    begin_date = models.DateField()
    end_date_flag = models.CharField(max_length=2)
    end_date = models.DateField()
    history_flag = models.CharField(max_length=2)
    src_quality_code = models.CharField(max_length=5)
    last_updated = models.DateField()
    updated_by = models.CharField(max_length=8)
    remark = models.CharField(max_length=254)
    def __str__(self):
	return "[ucan %s] %s in %s" % (self.ucan_station_id, self.network_station_id, self.id_type)
    class Admin:
	list_display = ('ucan_station_id', 'network_station_id', 'id_type', 'begin_date', 'end_date')
	search_fields = ('ucan_station_id', 'network_station_id')
    class Meta:
	app_label = 'meta'
        db_table = 'station_network'

#class GlobalVariableMajMin(models.Model):
#    major_id = models.SmallIntegerField()
#    minor_id = models.SmallIntegerField()
#    long_name = models.CharField(max_length=127)
#    method = models.CharField(max_length=8)
#    measure_interval = models.CharField(max_length=8)
#    report_interval = models.CharField(max_length=8)
#    default_units = models.CharField(max_length=20)
#    data_source = models.CharField(max_length=20)
#    remark = models.CharField(max_length=254)
#    class Admin: pass
#    class Meta:
#	app_label = 'meta'
#        db_table = 'global_variable_maj_min'

class StationTimeZone(models.Model):
    ucan_station_id = models.IntegerField(primary_key=True) # Not the real pk
    time_zone = models.FloatField()
    begin_date_flag = models.CharField(max_length=2)
    begin_date = models.DateField()
    end_date_flag = models.CharField(max_length=2)
    end_date = models.DateField()
    history_flag = models.CharField(max_length=2)
    src_quality_code = models.CharField(max_length=5)
    last_updated = models.DateField()
    updated_by = models.CharField(max_length=8)
    remark = models.CharField(max_length=254)
    def __str__(self):
	return "[ucan %s] %s" % (self.ucan_station_id, self.time_zone)
    class Admin:
	search_fields = ('ucan_station_id',)
    class Meta:
	app_label = 'meta'
        db_table = 'station_time_zone'

class ClimDiv(models.Model):
    clim_div_key = models.SmallIntegerField(primary_key=True)
    clim_div_code = models.CharField(max_length=2)
    fips_state_code = models.CharField(max_length=2, blank=True, null=True)
    fips_state_abbr = models.CharField(max_length=2, blank=True, null=True)
    ncdc_state_code = models.CharField(max_length=2)
    clim_div_name = models.CharField(max_length=30)
    last_updated = models.DateField()
    updated_by = models.CharField(max_length=8)
    remark = models.CharField(max_length=254)
    def __str__(self):
	return "[%s] %s, %s" % (self.clim_div_key, self.clim_div_name, self.fips_state_abbr)
    class Admin:
	list_display = ('clim_div_name','clim_div_key','fips_state_abbr','ncdc_state_code')
	list_filter = ('fips_state_abbr',)
	search_fields = ('clim_div_name')
    class Meta:
	app_label = 'meta'
        db_table = 'clim_div'
	verbose_name_plural = "climate divisions"

class StationClimDiv(models.Model):
    ucan_station_id = models.IntegerField(primary_key=True)
    clim_div = models.ForeignKey(ClimDiv, db_column="clim_div_key")
    clim_div_code = models.CharField(max_length=2)
    fips_state_code = models.CharField(max_length=2)
    fips_state_abbr = models.CharField(max_length=2)
    ncdc_state_code = models.CharField(max_length=2)
    begin_date_flag = models.CharField(max_length=2)
    begin_date = models.DateField()
    end_date_flag = models.CharField(max_length=2)
    end_date = models.DateField()
    history_flag = models.CharField(max_length=2)
    src_quality_code = models.CharField(max_length=5)
    last_updated = models.DateField()
    updated_by = models.CharField(max_length=8)
    remark = models.CharField(max_length=254)
    def __str__(self):
	return "[ucan %s] [climdiv %s]" % (self.ucan_station_id,self.clim_div)
    class Admin:
	list_display = ('ucan_station_id','clim_div','fips_state_abbr','ncdc_state_code')
	list_filter = ('fips_state_abbr',)
	search_fields = ('ucan_station_id')
    class Meta:
	app_label = 'meta'
        db_table = 'station_clim_div'



class Subnetwork(models.Model):
    subnetwork_key = models.IntegerField(primary_key=True)
    network_key = models.IntegerField()
    network_subnetwork_id = models.CharField(max_length=16)
    subnetwork_name = models.CharField(max_length=30)
    description = models.TextField()
    class Meta:
	app_label = 'meta'
        db_table = 'subnetwork'
    class Admin:
	pass
    def __str__(self):
	return "<Subnetwork:%s> %s" % (self.subnetwork_key, self.subnetwork_name)

    def station_set(self):
	from django.db import connection
	cursor = connection.cursor()
	sql = "SELECT ucan_station_id FROM subnetwork_stations WHERE subnetwork_key = %s"
	cursor.execute(sql, (self.subnetwork_key,))
	id_list = [r[0] for r in cursor.fetchall()]
	return Station.objects.filter(ucan_station_id__in=id_list)

    def station_id_set(self):
	from django.db import connection
	cursor = connection.cursor()
	sql = "SELECT ucan_station_id, network_station_id FROM subnetwork_stations WHERE subnetwork_key = %s"
	cursor.execute(sql, (self.subnetwork_key,))
	return cursor.fetchall()


class StationSubnetwork(models.Model):
    subnetwork_key = models.IntegerField(primary_key=True)
    ucan_station_id = models.IntegerField()
    network_station_id = models.CharField(max_length=20)
    class Meta:
	app_label = 'meta'
        db_table = 'subnetwork_stations'

## class Contact(models.Model):
##     contact_key = models.IntegerField(primary_key=True)
##     full_name = models.CharField(max_length=127)
##     organization = models.CharField(max_length=127)
##     contact_type = models.CharField(max_length=63)
##     position_title = models.CharField(max_length=63)
##     address = models.CharField(max_length=127)
##     city = models.CharField(max_length=63)
##     state = models.TextField() # This field type is a guess.
##     zip_code = models.CharField(max_length=10)
##     country = models.CharField(max_length=32)
##     email = models.CharField(max_length=63)
##     work_phone = models.CharField(max_length=32)
##     contact_notes = models.TextField()
##     class Meta:
## 	app_label = 'meta'
##         db_table = 'contact'
