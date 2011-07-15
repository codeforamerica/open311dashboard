from django.contrib.gis.db import models
from open311dashboard.settings import CITY

class Request(models.Model):
    service_request_id = models.CharField(max_length=200)
    status = models.CharField(max_length=10)
    status_notes = models.TextField(blank=True, null=True)
    service_name = models.CharField(max_length=100)
    service_code = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    agency_responsible = models.CharField(max_length=255, blank=True, null=True)
    service_notice = models.CharField(max_length=255, blank=True, null=True)
    requested_datetime = models.DateTimeField()
    updated_datetime = models.DateTimeField(null=True, blank=True)
    expected_datetime = models.DateTimeField(null=True, blank=True)
    address = models.CharField(max_length=255)
    address_id = models.IntegerField(blank=True, null=True)
    zipcode = models.IntegerField(blank=True, null=True)
    lat = models.FloatField()
    long = models.FloatField()
    media_url = models.URLField(blank=True, null=True)
    geo_point = models.PointField(srid=4326)

    objects = models.GeoManager()

    class Meta:
        db_table = "dashboard_data_%s" % CITY['SHORTNAME']

class Service(models.Model):
    service_code = models.CharField(max_length=100)
    metadata = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    keywords = models.TextField(blank=True, null=True)
    group = models.CharField(max_length=100)
    service_name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        db_table = "dashboard_service_%s" % CITY['SHORTNAME']

# This is an auto-generated Django model module created by ogrinspect.
class Neighborhoods(models.Model):
    objectid = models.FloatField()
    neighborho = models.CharField(max_length=25)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.neighborho

# Auto-generated `LayerMapping` dictionary for Neighborhoods model
neighborhoods_mapping = {
    'objectid' : 'OBJECTID',
    'neighborho' : 'NEIGHBORHO',
    'geom' : 'MULTIPOLYGON',
}
