from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'my_acis.views.home', name='home'),
    # url(r'^my_acis/', include('my_acis.foo.urls')),
    (r'^media/$', 'my_acis.views.media'),
    (r'^$', 'my_acis.views.home_view'),
    (r'^wrcc_meta/$', 'my_meta.views.home_view'),
    (r'^wrcc_meta/by_state/$', 'my_meta.views.by_state'),
    (r'^wrcc_meta/by_name/$', 'my_meta.views.by_name'),
    (r'^wrcc_meta/by_id/$', 'my_meta.views.by_id'),
    (r'^wrcc_meta/by_location/$', 'my_meta.views.by_location'),
    (r'^wrcc_meta/by_nina/$', 'my_meta.views.by_location'),
    (r'^wrcc_meta/station_detail/$', 'my_meta.views.station_detail'),
    (r'^wrcc_meta/station_tables/$', 'my_meta.views.station_tables'),
    (r'^wrcc_meta/station_tables_nina/$', 'my_meta.views.station_tables_nina'),
    (r'^wrcc_meta/(?P<tbl_name>[Station][Location|Network|Subnetwork|AltName|TimeZone|ClimDiv|County|Digital|Equipment|Maintenance|Physical|Photo|Contact]*)/(?P<tbl_id>\d+)/$', 'my_meta.views.sub_tables'),
    #(r'^my_meta/Station/(?P<tbl_id>\d+)/$', 'my_meta.views.sub_tables'),
    (r'^wrcc_meta/add/$', 'my_meta.views.add'),
    (r'^swcke/test/$', 'my_data.views.test'),
    (r'^swcke/main/$', 'my_data.views.main'),
    (r'^swcke/main_map/$', 'my_data.views.main_map'),
    (r'^swcke/home/$', 'my_data.views.home'),
    (r'^swcke/about_us/$', 'my_data.views.about_us'),
    (r'^swcke/contact_us/$', 'my_data.views.contact_us'),
    (r'^swcke/who_we_are/$', 'my_data.views.who_we_are'),
    (r'^swcke/what_we_do/$', 'my_data.views.what_we_do'),
    (r'^swcke/monitoring/$', 'my_data.views.dashboard'),
    #(r'^my_data/(?P<tbl_id>\d+)$', 'my_data.views.home_view'),
    (r'^swcke/help/$', 'my_data.views.help'),
    #(r'^swcke/station_finder/$', 'my_data.views.station_finder'),
    (r'^swcke/data/$', 'my_data.views.data_home'),
    (r'^swcke/data/sw_networks/$', 'my_data.views.sw_networks'),
    (r'^swcke/data/(?P<stn_id>\d+)/$', 'my_data.views.data_home'),
    (r'^swcke/data/station/$', 'my_data.views.data_station'),
    (r'^swcke/data/station/(?P<stn_id>\d+)(\&P<start_date>[\d{8,10}|por])(\&P<end_date>[\d{8,10}|por)(\&P<elements>[^,]+)$', 'my_data.views.data_station'),
    (r'^swcke/data/gridded/$', 'my_data.views.data_gridded'),
    (r'^swcke/data/gridded/(?P<start_date>[\d{8,10}|por])(\&P<end_date>[\d{8,10}|por)(\&P<elements>[^,]+)(\&P<grid>[^,]+)(\&P<bounding_box>[^,]+)(\&P<summary>[^,]+)(\&P<temporal_resolution>[^,]+)$', 'my_data.views.data_gridded'),
    (r'^swcke/data/gridded/(?P<start_date>[\d{8,10}|por])(\&P<end_date>[\d{8,10}|por)(\&P<elements>[^,]+)(\&P<grid>[^,]+)(\&P<state>[^,]+)(\&P<summary>[^,]+)(\&P<temporal_resolution>[^,]+)$', 'my_data.views.data_gridded'),
    (r'^swcke/data/gridded/(\?P<start_date>[\d{8,10}|por])(\&P<end_date>[\d{8,10}|por)(\&P<elements>[^,]+)(\&P<grid>[^,]+)(\&P<loc>[^,]+)(\&P<summary>[^,]+)(\&P<temporal_resolution>[^,]+)$', 'my_data.views.data_gridded'),
    (r'^swcke/apps/$', 'my_data.views.apps_home'),
    (r'^swcke/apps/(?P<stn_id>\d+)/$', 'my_data.views.apps_home'),
    (r'^swcke/apps/swcke_station_apps/$', 'my_data.views.swcke_station_apps'),
    (r'^swcke/apps/swcke_station_apps/(?P<stn_id>\d+)(\&P<start_date>[\d{8,10}|por])(\&P<end_date>[\d{8,10}|por)(\&P<elements>[^,]+)$', 'my_data.views.swcke_station_apps'),
    (r'^swcke/apps/station/$', 'my_data.views.apps_station'),
    (r'^swcke/apps/station/(?P<stn_id>\d+)/$', 'my_data.views.apps_station'),
    (r'^swcke/apps/station/station_finder/$', 'my_data.views.station_locator_app'),
    (r'^swcke/apps/gridded/$', 'my_data.views.apps_gridded'),
    (r'^swcke/apps/gis/$', 'my_data.views.apps_gis'),
    (r'^swcke/apps/station/metagraph/$', 'my_data.views.metagraph'),
    (r'^swcke/apps/station/metagraph/(?P<stn_id>\d+)$', 'my_data.views.metagraph'),
    (r'^swcke/apps/station/sodsumm/$', 'my_data.views.sodsumm'),
    (r'^swcke/apps/station/sodsumm/(?P<stn_id>[^,]+)(\&P<start_date>[\d{4}])(\&P<end_date>[\d{4})(\&P<element>[^,]+)$', 'my_data.views.sodsumm'),
    (r'^swcke/apps/station/monthly_aves/$', 'my_data.views.monthly_aves'),
    (r'^swcke/apps/monthly_aves/(?P<stn_id>[^,]+)(\&P<start_date>[\d{8,10}|por])(\&P<end_date>[\d{8,10}|por)(\&P<elements>[^,]+)$', 'my_data.views.monthly_aves'),

    (r'^swcke/apps/gridded/grid_point_time_series/$', 'my_data.views.grid_point_time_series'),
    (r'^swcke/apps/gridded/grid_point_time_series/(?P<lat>\-?(0|1-9+)\.?\d+)(\&P<lon>\-?(0|1-9+)\.?\d+)$', 'my_data.views.grid_point_time_series'),
    (r'^swcke/apps/gridded/clim_sum_maps/$', 'my_data.views.clim_sum_maps'),
    (r'^swcke/apps/gridded/clim_sum_maps/(?P<start_date>[\d{8,10}])(\&P<end_date>[\d{8,10})(\&P<element>[^,]+)(\&P<grid>[^,]+)(\&P<state>[^,]+)$', 'my_data.views.clim_sum_maps'),
    (r'^swcke/apps/gridded/clim_sum_maps/(\?P<start_date>[\d{8,10}])(\&P<end_date>[\d{8,10})(\&P<element>[^,]+)(\&P<grid>[^,]+)(\&P<bounding_box>[^,]+)$', 'my_data.views.clim_sum_maps'),
    (r'^swcke/apps/gridded/clim_risk_maps/$', 'my_data.views.clim_risk_maps'),
    (r'^swcke/apps/gridded/clim_risk_maps/(?P<start_date>[\d{8,10}])(\&P<end_date>[\d{8,10})(\&P<element>[^,]+)(\&P<grid>[^,]+)(\&P<state>[^,]+)$', 'my_data.views.clim_risk_maps'),
    (r'^swcke/apps/gridded/clim_risk_maps/(\?P<start_date>[\d{8,10}])(\&P<end_date>[\d{8,10})(\&P<element>[^,]+)(\&P<grid>[^,]+)(\&P<bounding_box>[^,]+)$', 'my_data.views.clim_risk_maps'),
    (r'^swcke/apps/station/station_locator/$', 'my_data.views.station_locator_app'),
    (r'^wrcc_apps/$', 'my_apps.views.home_view'),
    #sub process apps: FIX ME: Need to be converted to module approach
    #module approach apps
    (r'^wrcc_apps/(?P<app_name>Sodsum)/$', 'my_apps.views.sodsum'),
    (r'^wrcc_apps/(?P<app_name>[Soddyrec|Soddynorm|Soddd|Sodpad|Sodsumm|Sodrun|Sodrunr|Sodpct|Sodthr|Sodxtrmts|Sodpiii]*)/$', 'my_apps.views.sods'),
    (r'^wrcc_apps/(?P<app_name>[Sodlist|Sodmonline|Sodmonlinemy|Sodcnv]*)/$', 'my_apps.views.sodlist'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT, 'show_indexes':True
        }),
   )
