from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'my_acis.views.home', name='home'),
    # url(r'^my_acis/', include('my_acis.foo.urls')),
    (r'^$', 'my_acis.views.home_view'),
    (r'^my_meta$', 'my_meta.views.home_view'),
    (r'^my_meta/by_state/$', 'my_meta.views.by_state'),
    (r'^my_meta/by_name/$', 'my_meta.views.by_name'),
    (r'^my_meta/by_id/$', 'my_meta.views.by_id'),
    (r'^my_meta/by_location/$', 'my_meta.views.by_location'),
    (r'^my_meta/station_detail/$', 'my_meta.views.station_detail'),
    (r'^my_meta/maintenance/(?P<ucan_id>\d+)/$', 'my_meta.views.station_maintenance'),
    (r'^my_meta/physical/(?P<ucan_id>\d+)/$', 'my_meta.views.station_physical'),
    (r'^my_meta/equipment/(?P<ucan_id>\d+)/$', 'my_meta.views.station_equipment'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
