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
    (r'^my_meta/$', 'my_meta.views.home_view'),
    (r'^my_meta/by_state/$', 'my_meta.views.by_state'),
    (r'^my_meta/by_name/$', 'my_meta.views.by_name'),
    (r'^my_meta/by_id/$', 'my_meta.views.by_id'),
    (r'^my_meta/by_location/$', 'my_meta.views.by_location'),
    (r'^my_meta/station_detail/$', 'my_meta.views.station_detail'),
    (r'^my_meta/station_tables/$', 'my_meta.views.station_tables'),
    (r'^my_meta/(?P<tbl_name>[Station][Location|Network|Subnetwork|AltName|TimeZone|ClimDiv|County|Digital|Equipment|Maintenance|Physical|Photo|Contact]*)/(?P<tbl_id>\d+)/$', 'my_meta.views.sub_tables'),
    #(r'^my_meta/Station/(?P<tbl_id>\d+)/$', 'my_meta.views.sub_tables'),
    (r'^my_meta/add/$', 'my_meta.views.add'),
    (r'^my_data/$', 'my_data.views.home_view'),
    (r'^my_data/about_us/$', 'my_data.views.about_us'),
    (r'^my_data/contact_us/$', 'my_data.views.contact_us'),
    #(r'^my_data/(?P<tbl_id>\d+)$', 'my_data.views.home_view'),
    (r'^my_data/station_finder/$', 'my_data.views.station_finder'),
    (r'^my_data/station_finder/by_state/$', 'my_data.views.by_state'),
    (r'^my_data/station_finder/by_bounding_box/$', 'my_data.views.by_bounding_box'),
    (r'^my_data/station_finder/by_id/$', 'my_data.views.by_id'),
    (r'^my_data/station_finder/by_cwa/$', 'my_data.views.by_cwa'),
    (r'^my_data/station_finder/by_county/$', 'my_data.views.by_county'),
    (r'^my_data/station_finder/by_clim_div/$', 'my_data.views.by_clim_div'),
    (r'^my_data/station_finder/by_basin/$', 'my_data.views.by_basin'),
    (r'^my_data/data/$', 'my_data.views.data'),
    (r'^my_data/data/(?P<stn_id>\d+)/$', 'my_data.views.data'),
    (r'^my_data/apps/$', 'my_data.views.apps'),
    (r'^my_data/apps/(?P<stn_id>\d+)/$', 'my_data.views.apps'),
    (r'^my_data/apps/metagraph/$', 'my_data.views.metagraph'),
    (r'^my_data/apps/monthly_aves/$', 'my_data.views.monthly_aves'),
    (r'^my_data/apps/clim_sum_maps/$', 'my_data.views.clim_sum_maps'),
    (r'^my_apps/$', 'my_apps.views.home_view'),
    #sub process apps: FIX ME: Need to be converted to module approach
    #module approach apps
    (r'^my_apps/(?P<app_name>Sodsum)/$', 'my_apps.views.sodsum'),
    (r'^my_apps/(?P<app_name>[Soddyrec|Soddynorm|Soddd|Sodpad|Sodsumm|Sodrun|Sodrunr|Sodpct|Sodthr|Sodxtrmts|Sodpiii]*)/$', 'my_apps.views.sods'),
    (r'^my_apps/(?P<app_name>[Sodlist|Sodmonline|Sodmonlinemy|Sodcnv]*)/$', 'my_apps.views.sodlist'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
