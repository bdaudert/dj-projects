from django.db import models
from common import *

class WrccStation(models.Model):
    ucan_station_id = models.IntegerField(primary_key=True)
    station_best_name = models.CharField(maxlength=30)
    country_key = models.SmallIntegerField()
    fips_country_code = models.CharField(maxlength=2)
    state = models.ForeignKey(State, db_column="state_key")
    fips_state_abbr = models.CharField(maxlength=2)
    fips_state_code = models.CharField(maxlength=2)
    begin_date_flag = models.CharField(maxlength=2)
    begin_date = models.DateField()
    end_date_flag = models.CharField(maxlength=2)
    end_date = models.DateField()
    history_flag = models.CharField(maxlength=2)
    src_quality_code = models.CharField(maxlength=5)
    last_updated = models.DateField()
    updated_by = models.CharField(maxlength=8)
    remark = models.CharField(maxlength=254)
    class Meta:
	app_label = 'meta'
        db_table = 'wrcc_station'
    def __str__(self):
	return "[%s] %s, %s" % (self.ucan_station_id, self.station_best_name, self.state.fips_state_abbr)
    class Admin:
	list_display = ('ucan_station_id','station_best_name','state','begin_date','end_date')
	list_filter = ('state',)
	search_fields = ('ucan_station_id','station_best_name')

class WrccStationLocation(models.Model):
    ucan_station_id = models.IntegerField(primary_key=True) # Not the real pk
    longitude = models.FloatField(max_digits=11, decimal_places=8)
    latitude =  models.FloatField(max_digits=11, decimal_places=8)
    unit_key = models.SmallIntegerField()
    best_elevation = models.FloatField(max_digits=7, decimal_places=2)
    begin_date_flag = models.CharField(maxlength=2)
    begin_date = models.DateField()
    end_date_flag = models.CharField(maxlength=2)
    end_date = models.DateField()
    history_flag = models.CharField(maxlength=2)
    src_quality_flag = models.CharField(maxlength=5)
    last_updated = models.DateField()
    updated_by = models.CharField(maxlength=8)
    remark = models.CharField(maxlength=254)
    class Meta:
	app_label = 'meta'
        db_table = 'wrcc_station_location'
    def __str__(self):
	return "[ucan %s] %.4f %.4f" % (self.ucan_station_id, self.latitude, self.longitude)
    class Admin:
	list_display = ('ucan_station_id', 'latitude', 'longitude', 'best_elevation', 'begin_date', 'end_date')
	search_fields = ('ucan_station_id',)
    def get_station(self):
	return WrccStation.objects.get(pk=self.ucan_station_id)

class WrccStationMaintenance(models.Model):
    id = models.AutoField(primary_key=True)
    ucan_station_id = models.IntegerField()
    maintenance_date = models.DateField()
    remark = models.TextField()
    class Meta:
	app_label = 'meta'
        db_table = 'wrcc_station_maintenance'
    class Admin:
	list_display = ('ucan_station_id', 'maintenance_date')
	search_fields = ('ucan_station_id',)
    def __str__(self):
	return "[ucan %s] %s" % (self.ucan_station_id, self.maintenance_date)


class WrccStationEquipment(models.Model):
    id = models.AutoField(primary_key=True)
    ucan_station_id = models.IntegerField()
    equipment_type = models.CharField(maxlength=30)
    eq_manufacturer = models.CharField(maxlength=30)
    eq_model = models.CharField(maxlength=20)
    serial_num = models.CharField(maxlength=20)
    eq_description = models.TextField()
    install_date = models.DateField()
    remove_date = models.DateField(null=True)
    ref_height = models.IntegerField()
    sampling_interval = models.CharField(maxlength=10)
    remark = models.TextField()
    class Meta:
	app_label = 'meta'
        db_table = 'wrcc_station_equipment'
    class Admin:
	pass
    def __str__(self):
	return "[ucan %s] %s" % (self.ucan_station_id, self.equipment_type)

class WrccStationPhysical(models.Model):
    id = models.AutoField(primary_key=True)
    ucan_station_id = models.IntegerField()
    slope = models.IntegerField()
    aspect = models.IntegerField()
    gps = models.CharField(maxlength=1)
    site_description = models.TextField()
    route_directions = models.TextField()
    remark = models.TextField()
    class Meta:
	app_label = 'meta'
        db_table = 'wrcc_station_physical'
    class Admin:
	pass
    def __str__(self):
	return "[ucan %s] %s ..." % (self.ucan_station_id, str(self.site_description)[:80])


## class WrccStationClimDiv(models.Model):
##     ucan_station_id = models.IntegerField()
##     clim_div_key = models.SmallIntegerField()
##     clim_div_code = models.TextField() # This field type is a guess.
##     fips_state_code = models.TextField() # This field type is a guess.
##     fips_state_abbr = models.TextField() # This field type is a guess.
##     ncdc_state_code = models.TextField() # This field type is a guess.
##     begin_date_flag = models.TextField() # This field type is a guess.
##     begin_date = models.DateField()
##     end_date_flag = models.TextField() # This field type is a guess.
##     end_date = models.DateField()
##     history_flag = models.TextField() # This field type is a guess.
##     src_quality_code = models.TextField() # This field type is a guess.
##     last_updated = models.DateField()
##     updated_by = models.TextField() # This field type is a guess.
##     remark = models.CharField(maxlength=254)
##     class Meta:
## 	app_label = 'meta'
##         db_table = 'wrcc_station_clim_div'
## 
## class WrccStationCounty(models.Model):
##     ucan_station_id = models.IntegerField()
##     county_key = models.SmallIntegerField()
##     fips_state_code = models.TextField() # This field type is a guess.
##     fips_county_code = models.TextField() # This field type is a guess.
##     county_name = models.CharField(maxlength=31)
##     begin_date_flag = models.TextField() # This field type is a guess.
##     begin_date = models.DateField()
##     end_date_flag = models.TextField() # This field type is a guess.
##     end_date = models.DateField()
##     history_flag = models.TextField() # This field type is a guess.
##     src_quality_code = models.TextField() # This field type is a guess.
##     last_updated = models.DateField()
##     updated_by = models.TextField() # This field type is a guess.
##     remark = models.CharField(maxlength=254)
##     class Meta:
## 	app_label = 'meta'
##         db_table = 'wrcc_station_county'
## 
## class WrccStationNetwork(models.Model):
##     ucan_station_id = models.IntegerField()
##     network_station_id = models.CharField(maxlength=20)
##     id_type_key = models.SmallIntegerField()
##     begin_date_flag = models.TextField() # This field type is a guess.
##     begin_date = models.DateField()
##     end_date_flag = models.TextField() # This field type is a guess.
##     end_date = models.DateField()
##     history_flag = models.TextField() # This field type is a guess.
##     src_quality_code = models.TextField() # This field type is a guess.
##     last_updated = models.DateField()
##     updated_by = models.TextField() # This field type is a guess.
##     remark = models.CharField(maxlength=254)
##     class Meta:
## 	app_label = 'meta'
##         db_table = 'wrcc_station_network'
## 
## class WrccSubnetworkStations(models.Model):
##     subnetwork_key = models.IntegerField()
##     ucan_station_id = models.IntegerField()
##     network_station_id = models.CharField(maxlength=20)
##     class Meta:
## 	app_label = 'meta'
##         db_table = 'wrcc_subnetwork_stations'
## 
## class StationContact(models.Model):
##     ucan_station_id = models.IntegerField()
##     contact_key = models.IntegerField()
##     class Meta:
## 	app_label = 'meta'
##         db_table = 'station_contact'
## 
## class WrccStationContact(models.Model):
##     ucan_station_id = models.IntegerField()
##     contact_key = models.IntegerField()
##     class Meta:
## 	app_label = 'meta'
##         db_table = 'wrcc_station_contact'
## 
## 
## class SpatialRefSys(models.Model):
##     srid = models.IntegerField(primary_key=True)
##     auth_name = models.CharField(maxlength=256)
##     auth_srid = models.IntegerField()
##     srtext = models.CharField(maxlength=2048)
##     proj4text = models.CharField(maxlength=2048)
##     class Meta:
## 	app_label = 'meta'
##         db_table = 'spatial_ref_sys'
## 
## class GeometryColumns(models.Model):
##     f_table_catalog = models.CharField(maxlength=256)
##     f_table_schema = models.CharField(maxlength=256)
##     f_table_name = models.CharField(maxlength=256)
##     f_geometry_column = models.CharField(maxlength=256)
##     coord_dimension = models.IntegerField()
##     srid = models.IntegerField()
##     type = models.CharField(maxlength=30)
##     class Meta:
## 	app_label = 'meta'
##         db_table = 'geometry_columns'
## 
## 
## class WrccContact(models.Model):
##     contact_key = models.IntegerField()
##     full_name = models.CharField(maxlength=127)
##     organization = models.CharField(maxlength=127)
##     contact_type = models.CharField(maxlength=63)
##     position_title = models.CharField(maxlength=63)
##     address = models.CharField(maxlength=127)
##     city = models.CharField(maxlength=63)
##     state = models.TextField() # This field type is a guess.
##     zip_code = models.CharField(maxlength=10)
##     country = models.CharField(maxlength=32)
##     email = models.CharField(maxlength=63)
##     work_phone = models.CharField(maxlength=32)
##     contact_notes = models.TextField()
##     class Meta:
## 	app_label = 'meta'
##         db_table = 'wrcc_contact'
## 
## class StationPhysical(models.Model):
##     ucan_station_id = models.IntegerField()
##     slope = models.IntegerField()
##     aspect = models.IntegerField()
##     gps = models.TextField() # This field type is a guess.
##     site_description = models.TextField()
##     route_directions = models.TextField()
##     remark = models.TextField()
##     class Meta:
## 	app_label = 'meta'
##         db_table = 'station_physical'
## 
## class StationMaintenance(models.Model):
##     ucan_station_id = models.IntegerField()
##     maintenance_date = models.DateField()
##     remark = models.TextField()
##     class Meta:
## 	app_label = 'meta'
##         db_table = 'station_maintenance'
## 
## class StationEquipment(models.Model):
##     ucan_station_id = models.IntegerField()
##     equipment_type = models.CharField(maxlength=30)
##     eq_manufacturer = models.CharField(maxlength=30)
##     eq_model = models.CharField(maxlength=20)
##     serial_num = models.CharField(maxlength=20)
##     eq_description = models.TextField()
##     install_date = models.DateField()
##     remove_date = models.DateField()
##     ref_height = models.IntegerField()
##     sampling_interval = models.CharField(maxlength=10)
##     remark = models.TextField()
##     class Meta:
## 	app_label = 'meta'
##         db_table = 'station_equipment'
## 
## class WrccStationAltName(models.Model):
##     ucan_station_id = models.IntegerField()
##     station_alt_name = models.CharField(maxlength=30)
##     name_type_key = models.SmallIntegerField()
##     begin_date_flag = models.TextField() # This field type is a guess.
##     begin_date = models.DateField()
##     end_date_flag = models.TextField() # This field type is a guess.
##     end_date = models.DateField()
##     history_flag = models.TextField() # This field type is a guess.
##     src_quality_code = models.TextField() # This field type is a guess.
##     last_updated = models.DateField()
##     updated_by = models.TextField() # This field type is a guess.
##     remark = models.CharField(maxlength=254)
##     class Meta:
## 	app_label = 'meta'
##         db_table = 'wrcc_station_alt_name'
## 
