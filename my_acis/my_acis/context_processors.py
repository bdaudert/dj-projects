#!/usr/bin/python

from django.conf import settings


def get_urls(request):
    return {'URL_PREFIX':settings.URL_PREFIX,
            'HOME_URL':settings.HOME_URL,
            'SW_CKN_URL':settings.SW_CKN_URL,
            'DASH_URL':settings.DASH_URL,
            'DATA_URL':settings.DATA_URL,
            'TOOLS_URL':settings.TOOLS_URL}

