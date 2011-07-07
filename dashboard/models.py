from django.db import models
from open311dashboard.settings import CITY

class Request(models.Model):
    '''Model that holds all 311 request information. There is currently no
    planned way to update this model from the web interface. All updates
    should be run through the update_db script.'''
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

    class Meta:
        db_table = "dashboard_data_%s" % CITY['SHORTNAME']

class Page(models.Model):
    '''Pages are merely exist to hold widgets, they have a title and widgets
    associated with them.'''
    title = model.CharField(max_length=140)
    widgets = model.ManyToManyField('Widget')

    class Meta:
        db_table = "pages_%s" % CITY['SHORTNAME']

class Widget(models.Model):
    '''Widgets are attached to pages and have a column number and an order. All
    metadata should be serialized in JSON.'''
    page = model.ManyToManyField('Page')
    partial = model.CharField(max_length=255)
    column = model.IntegerField()
    order = model.IntegerField()

    class Meta:
        db_table = "widgets_%s" % CITY['SHORTNAME']

