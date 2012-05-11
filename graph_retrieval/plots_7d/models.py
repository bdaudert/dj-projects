#create your models here
from django.db import models
#from django.contrib.localflavor.us.models import USStateField

class State(models.Model):
   state_key = models.IntegerField(primary_key=True)
   fips_state_abbr = models.CharField(max_length=2)
   def __unicode__(self):
       return self.fips_state_abbr

class Station(models.Model):
    state = models.ForeignKey(State)
    ucan_station_id = models.IntegerField(primary_key=True)
    station_alt_name = models.CharField(max_length=30)
    #state = USStateField()
    def __unicode__(self):
        return self.station_alt_name
