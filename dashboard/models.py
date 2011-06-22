from django.db import models
from open311dashboard.settings import CITY

import datetime

NOW = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')
ONEMONTHAGO = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=30), '%Y-%m-%d')

class RequestManager(models.Manager):

    def status_count(self, startdate=ONEMONTHAGO, enddate=NOW, status='open'):
        '''
        Count the number of 311 requests that have been opened and closed in a
        specified window of time. Defaults to the past month.
        '''
        from django.db import connection
        cursor = connection.cursor()

        # Different tables and WHERE clauses depending on which we are checking
        if status == 'open':
            table = 'requested_datetime'
            where = "WHERE (%s >= '%s' AND %s <= '%s')" % (table, startdate, table,
                                                       enddate)
        else:
            table = 'updated_datetime'
            where = "WHERE (status = 'Closed' AND %s >= '%s' AND %s <= '%s')" % (table, startdate, table, enddate)

        cursor.execute("""
                       SELECT date_trunc('day', %s), COUNT(*)
                       FROM dashboard_data_sf %s GROUP BY date_trunc('day',
                       %s) ORDER BY date_trunc('day',
                       %s)
                       """ % (table, where, table, table))
        result_list = []
        for row in cursor.fetchall():
            r = self.model()
            r.date = row[0]
            r.count = int(row[1])
            result_list.append(r)
        return result_list


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

    objects = RequestManager()

    class Meta:
        db_table = "dashboard_data_%s" % CITY['SHORTNAME']
