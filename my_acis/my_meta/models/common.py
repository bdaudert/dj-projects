from django.db import models


class County(models.Model):
    county_key = models.SmallIntegerField(primary_key=True)
    fips_state_code = models.CharField(max_length=2)
    fips_state_abbr = models.CharField(max_length=2)
    fips_county_code = models.CharField(max_length=3)
    county_name = models.CharField(max_length=31)
    begin_date_flag = models.CharField(max_length=2)
    begin_date = models.DateField()
    end_date_flag = models.CharField(max_length=2)
    end_date = models.DateField()
    history_flag = models.CharField(max_length=2)
    last_updated = models.DateField()
    updated_by = models.CharField(max_length=8)
    remark = models.CharField(max_length=254, null=True, blank=True)
    def __str__(self):
	return "%s, %s" % (self.county_name, self.fips_state_abbr)
    class Admin:
	list_display = ('county_name','county_key','fips_state_abbr','begin_date','end_date')
	list_filter = ('fips_state_abbr',)
	search_fields = ('county_name')
    class Meta:
	app_label = 'my_meta'
        db_table = 'county'
	verbose_name_plural = "counties"


class State(models.Model):
    state_key = models.SmallIntegerField(primary_key=True)
    country_key = models.SmallIntegerField()
    fips_country_abbr = models.CharField(max_length=2)
    fips_state_code =   models.CharField(max_length=2)
    ncdc_state_code =   models.CharField(max_length=2)
    fips_state_abbr =   models.CharField(max_length=2)
    state_name = models.CharField(max_length=30)
    last_updated = models.DateField()
    updated_by = models.CharField(max_length=8)
    remark = models.CharField(max_length=254, null=True, blank=True)
    def __str__(self):
	return "%s" % self.fips_state_abbr
    class Admin: pass
    class Meta:
	app_label = 'my_meta'
        db_table = 'state'

STATE_CHOICES = [(s.state_key, s.state_name) for s in State.objects.all()]

class Zipcode(models.Model):
    zipcode = models.CharField(primary_key=True, max_length=5)
    longitude = models.FloatField()
    latitude =  models.FloatField()
    class Admin: pass
    class Meta:
	app_label = 'my_meta'
        db_table = 'zipcode'


class IdType(models.Model):
    id_type_key = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=254)
    controller_info = models.CharField(max_length=50)
    last_updated = models.DateField()
    updated_by = models.CharField(max_length=8)
    remark = models.CharField(max_length=254, null=True, blank=True)
    def __str__(self):
	return "[%s] %s" % (self.id_type_key, self.name)
    class Admin:
	list_display = ('name','id_type_key','description','controller_info','last_updated','updated_by','remark')
    class Meta:
	app_label = 'my_meta'
        db_table = 'id_type'


class Network(models.Model):
    network_key = models.SmallIntegerField(primary_key=True)
    network_code = models.CharField(max_length=8)
    name = models.CharField(max_length=30)
    description = models.TextField()
    id_type = models.ForeignKey(IdType, db_column="id_type_key")
    last_updated = models.DateField()
    updated_by = models.CharField(max_length=8)
    remark = models.CharField(max_length=254, null=True, blank=True)
    def __str__(self):
	return "[%s] %s" % (self.network_key, self.network_code)
    class Admin:
	list_display = ('name','network_key','network_code','name','description','id_type','last_updated','updated_by','remark')
    class Meta:
	app_label = 'my_meta'
        db_table = 'network'


class Variable(models.Model):
    ucan_station_id = models.IntegerField(primary_key=True) # Not the real pk
    network_station_id = models.CharField(max_length=20)
    network = models.ForeignKey(Network, db_column="network_key")
    var_major_id = models.SmallIntegerField()
    var_minor_id = models.SmallIntegerField()
    begin_date = models.DateField()
    end_date = models.DateField()
    def __str__(self):
	return "[ucan %s] %s in %s, %s::%s" % (self.ucan_station_id, self.network_station_id,
						self.network, self.var_major_id, self.var_minor_id)
    class Admin:
	list_display = ('ucan_station_id', 'network_station_id', 'network', 'var_major_id', 'var_minor_id', 'begin_date', 'end_date')
	search_fields = ('ucan_station_id', 'network_station_id')
    class Meta:
	app_label = 'my_meta'
        db_table = 'variable'


class StationDigital(models.Model):
    ucan_station_id = models.IntegerField(primary_key=True) # Not the real pk
    network_station_id = models.CharField(max_length=20)
    network = models.ForeignKey(Network, db_column="network_key")
    begin_date = models.DateField()
    end_date = models.DateField()
    def __str__(self):
	return "[ucan %s] %s in %s" % (self.ucan_station_id, self.network_station_id, self.network)
    class Admin:
	list_display = ('ucan_station_id','network_station_id','network','begin_date','end_date')
	list_filter = ('network',)
	search_fields = ('ucan_station_id', 'network_station_id')
    class Meta:
	app_label = 'my_meta'
        db_table = 'station_digital'
