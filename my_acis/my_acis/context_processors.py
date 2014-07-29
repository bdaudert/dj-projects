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
            'GRID_DATA_URL':settings.GRID_DATA_URL,
            'STATION_DATA_URL':settings.STATION_DATA_URL,
            'TOOLS_URL':settings.TOOLS_URL,
            'GRID_TOOLS_URL':settings.GRID_TOOLS_URL,
            'GRID_SPATIAL_SUMMARY_URL':settings.GRID_SPATIAL_SUMMARY_URL,
            'GRID_TEMPORAL_SUMMARY_URL':settings.GRID_TEMPORAL_SUMMARY_URL,
            'GRID_SODXTRMTS_URL':settings.GRID_SODXTRMTS_URL,
            'GRID_GP_TIME_SERIES_URL':settings.GRID_GP_TIME_SERIES_URL,
            'STATION_TOOLS_URL':settings.STATION_TOOLS_URL,
            'STATION_SODXTRMTS_URL':settings.STATION_SODXTRMTS_URL,
            'STATION_SODSUMM_URL':settings.STATION_SODSUMM_URL,
            'STATION_MON_AVES_URL':settings.STATION_MON_AVES_URL,
            'STATION_FINDER_URL':settings.STATION_FINDER_URL,
            'STATION_METAGRAPH_URL':settings.STATION_METAGRAPH_URL,
            'GIS_TOOLS_URL':settings.GIS_TOOLS_URL
            }

