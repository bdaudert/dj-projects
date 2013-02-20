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
    (r'^sw_ckn/main/$', 'my_data.views.main_map'),
    (r'^sw_ckn/main_maves/$', 'my_data.views.main_maves'),
    (r'^sw_ckn/home/$', 'my_data.views.home'),
    (r'^sw_ckn/about_us/$', 'my_data.views.about_us'),
    (r'^sw_ckn/contact_us/$', 'my_data.views.contact_us'),
    (r'^sw_ckn/who_we_are/$', 'my_data.views.who_we_are'),
    (r'^sw_ckn/what_we_do/$', 'my_data.views.what_we_do'),
    (r'^sw_ckn/focus_areas/$', 'my_data.views.focus_areas'),
    (r'^sw_ckn/projects/$', 'my_data.views.projects'),
    (r'^sw_ckn/publications/$', 'my_data.views.publications'),
    (r'^sw_ckn/news_events_announcements/$', 'my_data.views.news_events'),
    (r'^sw_ckn/dashboard/$', 'my_data.views.dashboard'),
    #(r'^my_data/(?P<tbl_id>\d+)$', 'my_data.views.home_view'),
    (r'^sw_ckn/help/$', 'my_data.views.help'),
    #(r'^sw_ckn/station_finder/$', 'my_data.views.station_finder'),
    (r'^sw_ckn/station_finder/$', 'my_data.views.station_locator_app'),
    (r'^sw_ckn/station_finder/by_state/$', 'my_data.views.by_state'),
    (r'^sw_ckn/station_finder/by_bounding_box/$', 'my_data.views.by_bounding_box'),
    (r'^sw_ckn/station_finder/by_id/$', 'my_data.views.by_id'),
    (r'^sw_ckn/station_finder/by_cwa/$', 'my_data.views.by_cwa'),
    (r'^sw_ckn/station_finder/by_county/$', 'my_data.views.by_county'),
    (r'^sw_ckn/station_finder/by_clim_div/$', 'my_data.views.by_clim_div'),
    (r'^sw_ckn/station_finder/by_basin/$', 'my_data.views.by_basin'),
    (r'^sw_ckn/data/$', 'my_data.views.data_home'),
    (r'^sw_ckn/data/(?P<stn_id>\d+)/$', 'my_data.views.data_home'),
    (r'^sw_ckn/data/historic/$', 'my_data.views.data_historic'),
    (r'^sw_ckn/data/historic/(?P<stn_id>\d+)(\&P<start_date>[\d{8}|por])(\&P<end_date>[\d{8}|por)(\&P<elements>[^,]+)$', 'my_data.views.data_historic'),
    (r'^sw_ckn/data/modeled/$', 'my_data.views.data_modeled'),
    (r'^sw_ckn/data/modeled/(?P<grid_selection>[state|bbox|point])(\&P<start_date>[\d{8}|por])(\&P<end_date>[\d{8}|por)(\&P<elements>[^,]+)(\&P<grid>[^,]+)(\&P<bounding_box>[^,]+)$', 'my_data.views.data_modeled'),
    (r'^sw_ckn/data/modeled/(?P<grid_selection>[state|bbox|point])(\&P<start_date>[\d{8}|por])(\&P<end_date>[\d{8}|por)(\&P<elements>[^,]+)(\&P<grid>[^,]+)(\&P<state>[^,]+)$', 'my_data.views.data_modeled'),
    (r'^sw_ckn/data/modeled/(?P<grid_selection>[state|bbox|point])(\&P<start_date>[\d{8}|por])(\&P<end_date>[\d{8}|por)(\&P<elements>[^,]+)(\&P<grid>[^,]+)(\&P<loc>[^,]+)$', 'my_data.views.data_modeled'),
    (r'^sw_ckn/apps/$', 'my_data.views.apps_home'),
    (r'^sw_ckn/apps/(?P<stn_id>\d+)/$', 'my_data.views.apps_home'),
    (r'^sw_ckn/apps/sw_ckn_station_apps/$', 'my_data.views.sw_ckn_station_apps'),
    (r'^sw_ckn/apps/sw_ckn_station_apps/(?P<stn_id>\d+)(\&P<start_date>[\d{8}|por])(\&P<end_date>[\d{8}|por)(\&P<elements>[^,]+)$', 'my_data.views.sw_ckn_station_apps'),
    (r'^sw_ckn/apps/metagraph/$', 'my_data.views.metagraph'),
    (r'^sw_ckn/apps/metagraph/(?P<stn_id>\d+)$', 'my_data.views.metagraph'),
    (r'^sw_ckn/apps/monthly_aves/$', 'my_data.views.monthly_aves'),
    (r'^sw_ckn/apps/monthly_aves/(?P<stn_id>[^,]+)(\&P<start_date>[\d{8}|por])(\&P<end_date>[\d{8}|por)(\&P<elements>[^,]+)$', 'my_data.views.monthly_aves'),
    (r'^sw_ckn/apps/grid_point_time_series/$', 'my_data.views.grid_point_time_series'),
    (r'^sw_ckn/apps/grid_point_time_series/(?P<lat>\-?(0|1-9+)\.?\d+)(\&P<lon>\-?(0|1-9+)\.?\d+)$', 'my_data.views.grid_point_time_series'),
    (r'^sw_ckn/apps/clim_sum_maps/$', 'my_data.views.clim_sum_maps'),
    (r'^sw_ckn/apps/station_locator/$', 'my_data.views.station_locator_app'),
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
