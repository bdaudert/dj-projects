from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^plots_7d/$', 'plots_7d.views.index', name='index'),
    url(r'^plots_7d/results/$', 'plots_7d.views.results', name='results'),
    url(r'^plots_7d/(?P<state_name>[A-Z][A-Z]|\d+)/$', 'plots_7d.views.stations', name='stations'),
    # url(r'^$', 'graph_retrieval.views.home', name='home'),
    # url(r'^graph_retrieval/', include('graph_retrieval.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
