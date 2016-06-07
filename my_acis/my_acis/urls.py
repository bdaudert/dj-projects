from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    #(r'^media/$', 'my_acis.views.media'),
    (r'^$', 'my_acis.views.home_view'),
    (r'^documentation/$', 'documentation.views.home'),
    (r'^documentation/acis/$', 'documentation.views.acis'),
    (r'^documentation/ee/$', 'documentation.views.ee'),
    (r'^documentation/ee/set_up/$', 'documentation.views.ee_set_up'),
    (r'^documentation/ee/hello_world/$', 'documentation.views.ee_hello_world'),
    (r'^documentation/ee/organizing_code/$', 'documentation.views.ee_organizing_code'),
    (r'^documentation/ee/ipython_notebooks/$', 'documentation.views.ee_ipython_notebooks'),
    (r'^documentation/acis/grid_acis/$', 'documentation.views.grid_acis'),
    (r'^documentation/acis/subdaily_acis/$', 'documentation.views.subdaily_acis'),
    (r'^documentation/scenic/$', 'documentation.views.scenic'),
    (r'^documentation/scenic/large_data_requests/$', 'documentation.views.large_data_requests'),
    (r'^wrcc_meta/$', 'wrcc_meta.views.home_view'),
    (r'^wrcc_meta/by_state/$', 'wrcc_meta.views.by_state'),
    (r'^wrcc_meta/by_name/$', 'wrcc_meta.views.by_name'),
    (r'^wrcc_meta/by_name_and_state/$', 'wrcc_meta.views.by_name_and_state'),
    (r'^wrcc_meta/by_id/$', 'wrcc_meta.views.by_id'),
    (r'^wrcc_meta/by_ucan_id/$', 'wrcc_meta.views.by_ucan_id'),
    (r'^wrcc_meta/by_location/$', 'wrcc_meta.views.by_location'),
    (r'^wrcc_meta/by_nina/$', 'wrcc_meta.views.by_location'),
    (r'^wrcc_meta/station_detail/$', 'wrcc_meta.views.station_detail'),
    (r'^wrcc_meta/station_tables/$', 'wrcc_meta.views.station_tables'),
    (r'^wrcc_meta/(?P<tbl_name>[Station][Location|AltName|TimeZone|ClimDiv|County|Digital|Equipment|Maintenance|Physical|Photo|Contact]*)/$', 'wrcc_meta.views.station_tables_merge'),
    (r'^wrcc_meta/sub_tables/$', 'wrcc_meta.views.sub_tables'),
    (r'^wrcc_meta/add/$', 'wrcc_meta.views.station_tables_add'),
    (r'^wrcc_meta/merge/$', 'wrcc_meta.views.station_tables_merge'),
    (r'^wrcc_apps/$', 'wrcc_apps.views.home_view'),
    (r'^wrcc_apps/cemp/$', 'wrcc_apps.views.cemp'),
    (r'^wrcc_apps/nevcan/$', 'wrcc_apps.views.nevcan'),
    (r'^wrcc_apps/(?P<app_name>Sodsum)/$', 'wrcc_apps.views.sodsum'),
    (r'^wrcc_apps/(?P<app_name>[Soddyrec|Soddynorm|Soddd|Sodpad|Sodsumm|Sodrun|Sodrunr|Sodpct|Sodthr|Sodxtrmts|Sodpiii]*)/$', 'wrcc_apps.views.sods'),
    (r'^wrcc_apps/(?P<app_name>[Sodmonline|Sodmonlinemy|Sodcnv]*)/$', 'wrcc_apps.views.sodlist'),
    (r'^wrcc_apps/Sodlist/$', 'wrcc_apps.views.sodlist_new'),
    #Redirect from swcke
    (r'^swcke/home/$', 'scenic.views.swcke_home'),
    (r'^swcke/\w+/$', 'scenic.views.swcke_home'),
    (r'^swcke/\w+/\w+/$', 'scenic.views.swcke_home'),
    (r'^swcke/\w+/\w+/\w+/$', 'scenic.views.swcke_home'),
    (r'^scenic/test/$', 'scenic.views.test'),
    (r'^scenic/download_map/$', 'scenic.views.download_map'),
    (r'^scenic/home/$', 'scenic.views.home'),
    (r'^scenic/$', 'scenic.views.home'),
    (r'^scenic/about_us/$', 'scenic.views.about_us'),
    (r'^scenic/contact_us/$', 'scenic.views.contact_us'),
    (r'^scenic/who_we_are/$', 'scenic.views.who_we_are'),
    (r'^scenic/what_we_do/$', 'scenic.views.what_we_do'),
    (r'^scenic/dashboard/$', 'scenic.views.dashboard'),
    (r'^scenic/gallery/$', 'scenic.views.gallery'),
    (r'^scenic/howto/$', 'scenic.views.howto'),
    (r'^scenic/resources/$', 'scenic.views.resources'),
    (r'^scenic/upload_test/$', 'scenic.views.upload_test'),
    (r'^scenic/help/$', 'scenic.views.help'),
    (r'^scenic/download/$', 'scenic.views.download'),
    (r'^scenic/data/$', 'scenic.views.data_home'),
    (r'^scenic/data/station_finder/$', 'scenic.views.station_finder'),
    (r'^scenic/data/single/$', 'scenic.views.single_point_prods'),
    (r'^scenic/data/single/lister/$', 'scenic.views.single_lister'),
    (r'^scenic/data/single/monthly_summary/$', 'scenic.views.monthly_summary'),
    (r'^scenic/data/single/climatology/$', 'scenic.views.climatology'),
    (r'^scenic/data/single/yearly_summary/$', 'scenic.views.yearly_summary'),
    (r'^scenic/data/single/intraannual/$', 'scenic.views.intraannual'),
    (r'^scenic/data/single/data_comparison/$', 'scenic.views.data_comparison'),
    (r'^scenic/data/multi/$', 'scenic.views.multi_point_prods'),
    (r'^scenic/data/multi/lister/$', 'scenic.views.multi_lister'),
    (r'^scenic/data/multi/spatial_summary/$', 'scenic.views.spatial_summary'),
    (r'^scenic/data/multi/monthly_spatial_summary/$', 'scenic.views.monthly_spatial_summary'),
    (r'^scenic/data/multi/temporal_summary/$', 'scenic.views.temporal_summary'),
    (r'^scenic/data/climate_engine/$', 'scenic.views.climate_engine'),
    (r'^scenic/data/sw_networks/$', 'scenic.views.sw_networks'),
    (r'^scenic/data/(?P<stn_id>\d+)/$', 'scenic.views.data_home'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    #import debug_toolbar
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT, 'show_indexes':True
        }),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT, 'show_indexes':True
        }),
   )
