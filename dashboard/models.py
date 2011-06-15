from django.db import models

class Request(models.Model):
    service_request_id = models.IntegerField()
    status = models.CharField(max_length=10)
    status_notes = models.TextField()
    service_name = models.CharField(max_length=100)
    service_code = models.IntegerField()
    description = models.TextField()
    agency_responsible = models.CharField(max_length=255)
    service_notice = models.CharField(max_length=255)
    requested_datetime = models.DateTimeField()
    updated_datetime = models.DateTimeField(null=True, blank=True)
    expected_datetime = models.DateTimeField(null=True, blank=True)
    address = models.CharField(max_length=255)
    address_id = models.IntegerField()
    zipcode = models.IntegerField()
    lat = models.FloatField()
    long = models.FloatField()
