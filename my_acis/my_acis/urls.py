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

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
