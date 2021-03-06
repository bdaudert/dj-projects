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
    (r'^wrcc_apps/(?P<app_name>Sodsum)/$', 'wrcc_apps.views.sodsum'),
    (r'^wrcc_apps/(?P<app_name>[Soddyrec|Soddynorm|Soddd|Sodpad|Sodsumm|Sodrun|Sodrunr|Sodpct|Sodthr|Sodxtrmts|Sodpiii]*)/$', 'wrcc_apps.views.sods'),
    #(r'^wrcc_apps/(?P<app_name>[Sodmonline|Sodmonlinemy|Sodcnv]*)/$', 'wrcc_apps.views.sodlist'),
    (r'^wrcc_apps/Sodlist/$', 'wrcc_apps.views.sodlist_new'),
    (r'^wrcc_apps/Sodmonline/$', 'wrcc_apps.views.sodmonline_new'),
    (r'^wrcc_apps/Sodmonlinemy/$', 'wrcc_apps.views.sodmonlinemy_new'),
    #Redirect from swcke
    (r'^scenic/home/$', 'scenic.views.home'),
    (r'^scenic/$', 'scenic.views.home'),
    (r'^scenic/about/$', 'scenic.views.about'),
    (r'^scenic/monitoring/$', 'scenic.views.monitoring'),
    (r'^scenic/help/$', 'scenic.views.help'),
    (r'^scenic/data/$', 'scenic.views.data'),
    (r'^scenic/data/remote_sensing_data/$', 'scenic.views.remote_sensing_data'),
    (r'^scenic/data/gridded_data/loca/$', 'scenic.views.loca'),
    (r'^scenic/data/station_data/$', 'scenic.views.station_data'),
    (r'^scenic/data/gridded_data/$', 'scenic.views.gridded_data'),
    (r'^scenic/analysis/$', 'scenic.views.analysis'),
    (r'^scenic/analysis/station_finder/$', 'scenic.views.station_finder'),
    (r'^scenic/analysis/single/$', 'scenic.views.single_point_prods'),
    (r'^scenic/analysis/single/lister/$', 'scenic.views.single_lister'),
    (r'^scenic/analysis/single/monthly_summary/$', 'scenic.views.monthly_summary'),
    (r'^scenic/analysis/single/climatology/$', 'scenic.views.climatology'),
    (r'^scenic/analysis/single/seasonal_summary/$', 'scenic.views.seasonal_summary'),
    (r'^scenic/analysis/single/single_year/$', 'scenic.views.single_year'),
    (r'^scenic/analysis/single/data_comparison/$', 'scenic.views.data_comparison'),
    (r'^scenic/analysis/multi/$', 'scenic.views.multi_point_prods'),
    (r'^scenic/analysis/multi/lister/$', 'scenic.views.multi_lister'),
    (r'^scenic/analysis/multi/spatial_summary/$', 'scenic.views.spatial_summary'),
    (r'^scenic/analysis/multi/monthly_spatial_summary/$', 'scenic.views.monthly_spatial_summary'),
    (r'^scenic/analysis/multi/temporal_summary/$', 'scenic.views.temporal_summary'),
    (r'^scenic/analysis/cold/livneh/$', 'scenic.views.livneh'),
    (r'^scenic/analysis/cold/loca/CNRM-CM5/$', 'scenic.views.loca_model_1'),
    (r'^scenic/analysis/cold/loca/HadGEM2-CC/$', 'scenic.views.loca_model_2'),
    (r'^scenic/analysis/cold/loca/HadGEM2-ES/$', 'scenic.views.loca_model_3'),
    (r'^scenic/analysis/cold/loca/GFDL-CM3/$', 'scenic.views.loca_model_4'),
    (r'^scenic/analysis/cold/loca/CanESM2/$', 'scenic.views.loca_model_5'),
    (r'^scenic/analysis/cold/loca/MICRO5/$', 'scenic.views.loca_model_6'),
    (r'^scenic/analysis/cold/loca/CESM1-BGC/$', 'scenic.views.loca_model_7'),
    (r'^scenic/analysis/cold/loca/CMCC-CMS/$', 'scenic.views.loca_model_8'),
    (r'^scenic/analysis/cold/loca/ACCESS1-0/$', 'scenic.views.loca_model_9'),
    (r'^scenic/analysis/cold/loca/CCSM4/$', 'scenic.views.loca_model_10'),
    (r'^scenic/data/(?P<stn_id>\d+)/$', 'scenic.views.data'),
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
