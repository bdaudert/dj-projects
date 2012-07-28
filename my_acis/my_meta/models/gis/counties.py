from django.contrib.gis.db import models

class CountyBorder(models.Model):
    area = models.FloatField()
    perimeter = models.FloatField()
    co99_d00_field = models.FloatField()
    co99_d00_i = models.FloatField()
    state = models.CharField(max_length=2)
    county = models.CharField(max_length=3)
    name = models.CharField(max_length=90)
    lsad = models.CharField(max_length=2)
    lsad_trans = models.CharField(max_length=50)
    geom = models.PolygonField(srid=4269)
    objects = models.GeoManager()

    class Meta:
        app_label = 'meta'
        db_table = 'county_borders'
        verbose_name_plural = "county borders"

    def __unicode__(self):
        return self.name

def load(verbose=True):
    from django.contrib.gis.utils import LayerMapping

    county_shp = '/home/gkwrcc/gis/co99_d00.shp'
    county_mapping = {
        'area' : 'AREA',
        'perimeter' : 'PERIMETER',
        'co99_d00_field' : 'CO99_D00_',
        'co99_d00_i' : 'CO99_D00_I',
        'state' : 'STATE',
        'county' : 'COUNTY',
        'name' : 'NAME',
        'lsad' : 'LSAD',
        'lsad_trans' : 'LSAD_TRANS',
        'geom' : 'POLYGON',
    }

    lm = LayerMapping(CountyBorder, county_shp, county_mapping, transform=False, encoding="iso-8859-1")
    lm.save(strict=True, verbose=verbose)
