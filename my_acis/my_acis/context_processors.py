#!/usr/bin/python

from django.conf import settings


def get_urls(request):
    return {
            #SCENIC DIRS
            'HOST':settings.HOST,
            'BASE_DIR':settings.BASE_DIR,
            'SRC_BASE':settings.SRC_BASE,
            'JSON_DIR':settings.JSON_DIR,
            'KML_DIR':settings.KML_DIR,
            'HTML_DIR':settings.HTML_DIR,
            'TMP_DIR':settings.TMP_DIR,
            'TEMP_DIR':settings.TEMP_DIR,
            #SCENIC SERVER DIRS
            'STATIC_URL':settings.STATIC_URL,
            'MEDIA_URL':settings.MEDIA_URL,
            'JSON_URL':settings.JSON_URL,
            'HTML_URL':settings.HTML_URL,
            'KML_URL':settings.KML_URL,
            'TMP_URL':settings.TMP_URL,
            'IMG_URL':settings.IMG_URL,
            'URL_PREFIX':settings.URL_PREFIX,
            'HOME_URL':settings.HOME_URL,
            'SCENIC_URL':settings.SCENIC_URL,
            'ABOUT_URL':settings.ABOUT_URL,
            'WHO_URL':settings.WHO_URL,
            'WHAT_URL':settings.WHAT_URL ,
            'CONTACT_URL':settings.CONTACT_URL,
            'DASH_URL':settings.DASH_URL,
            'DATA_URL':settings.DATA_URL,
            }

