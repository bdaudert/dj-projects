"""
WSGI config for my_acis project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys

# Add virtualenv
import site
site.addsitedir('/usr/local/pythonenv/csc/lib/python2.7/site-packages')

# Calculate the path based on the location of the WSGI script.
apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
# Add directories to the PYTHONPATH
sys.path.append(project)
# Manually add in python library files. Could be a package later...
sys.path.append("/www/apps/csc/my-python-lib")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_acis.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)

#class Debugger:
#    "From http://code.google.com/p/modwsgi/wiki/DebuggingTechniques"
#    def __init__(self, object):
#        self.__object = object
#
#    def __call__(self, *args, **kwargs):
#        import pdb, sys
#        debugger = pdb.Pdb()
#        debugger.use_rawinput = 0
#        debugger.reset()
#        sys.settrace(debugger.trace_dispatch)
#
#        try:
#            return self.__object(*args, **kwargs)
#        finally:
#            debugger.quitting = 1
#            sys.settrace(None)

#application = Debugger(application)
