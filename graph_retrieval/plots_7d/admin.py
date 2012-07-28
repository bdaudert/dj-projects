#admin pages
from models import State, Station
from django.contrib import admin

class StationInline(admin.StackedInline):
    model = Station
    extra = 3

class StateInline(admin.StackedInline):
    model = State
    extra = 3

class StateAdmin(admin.ModelAdmin):
    fields = ['state_key', 'fips_state_abbr']
    #inlines = [StateInline] #REMARK: not working for me

class StationAdmin(admin.ModelAdmin):
    fields = ['ucan_station_id', 'station_alt_name', 'state']
    #inlines = [StationInline]

admin.site.register(State, StateAdmin)
admin.site.register(Station, StationAdmin)
