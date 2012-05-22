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
    (r'^my_meta$', 'my_meta.views.home_view'),
    (r'^my_meta/by_state/$', 'my_meta.views.by_state'),
    (r'^my_meta/by_name/$', 'my_meta.views.by_name'),
    (r'^my_meta/by_id/$', 'my_meta.views.by_id'),
    (r'^my_meta/by_location/$', 'my_meta.views.by_location'),
    (r'^my_meta/station_detail/$', 'my_meta.views.station_detail'),
    (r'^my_meta/station_tables/$', 'my_meta.views.station_tables'),
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
