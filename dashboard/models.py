from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance as D
from open311dashboard.settings import ENABLE_GEO

class Request(models.Model):
    """

    The actual meat-n-potatoes of the 311 dashboard, all the data.
    Implementations are different so most of these fields are optional.

    Optional: PostGIS component set in settings.py

    """
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

    city = models.ForeignKey('City')


    # Super top secret geographic data.
    if ENABLE_GEO is True:
        geo_point = models.PointField(srid=900913, null=True)
        street = models.ForeignKey('Street', null=True)
        objects = models.GeoManager()

        def save(self):
            if (float(self.long) != 0.0 and float(self.lat) != 0.0):
                # Save the geo_point.
                point = Point(float(self.long), float(self.lat), srid=4326)
                point.transform(900913)

                self.geo_point = point

                # Lookup the nearest street
                street = Street.objects.filter(line__dwithin=(point, D(m=100))) \
                        .distance(point).order_by('distance')[:1]

                if len(street) > 0:
                    self.street = street[0]

            super(Request, self).save()

# class Service(models.Model):
    """

    In a perfect world, this would be related to each Request but separate
    implementations are, again, different.

    """
    # service_code = models.CharField(max_length=100)
    # metadata = models.CharField(max_length=100)
    # type = models.CharField(max_length=50)
    # keywords = models.TextField(blank=True, null=True)
    # group = models.CharField(max_length=100)
    # service_name = models.CharField(max_length=100)
    # description = models.TextField()

    # city = models.ForeignKey('City')
    # street = models.ForeignKey('Street')

class City(models.Model):
    """

    Give an ID to each city so everything can relate.

    """
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255)
    jurisdiction_id = models.CharField(max_length=100)
    paginated = models.BooleanField()

    def natural_key(self):
        return self.name

if ENABLE_GEO is True:
    class Geography(models.Model):
        """

        You can import any geographical shapes you want here and associate them
        with a city.

        """
        name = models.CharField(max_length=25)
        geo = models.MultiPolygonField(srid=900913)

        city = models.ForeignKey('City')
        #geo_type = models.ForeignKey('GeographyType')

        objects = models.GeoManager()

        def __unicode__(self):
            return self.name

        def get_absolute_url(self):
            return "/neighborhood/%i/" %  self.id

    # class GeographyType(models.Model):
        """

        Ex: Neighborhood, Congressional Districts...

        """
        # name = models.CharField(max_length=25)

        # Thank @ravoreyer for recommending this.
        # city = models.ForeignKey('City')

    class Street(models.Model):
        """

        Street centerline data.

        """
        street_name = models.CharField(max_length=100)
        line = models.LineStringField(srid=900913)
        city = models.ForeignKey("City")

        left_low_address = models.IntegerField(default=0)
        left_high_address = models.IntegerField(default=0)
        right_low_address = models.IntegerField(default=0)
        right_high_address = models.IntegerField(default=0)

        objects = models.GeoManager()

        def __unicode__(self):
            return self.street_name

        def natural_key(self):
            return self.street_name

        def get_absolute_url(self):
            return "/street/%i/" % self.id
