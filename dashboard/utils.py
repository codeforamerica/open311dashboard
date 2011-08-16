import datetime

import qsstats
from io import StringIO
from django.db.models import Model
from django.db.models.query import QuerySet
from django.utils.encoding import smart_unicode
from django.utils.simplejson import dumps
from django.contrib.gis.db.models.fields import GeometryField
from django.utils import simplejson
from django.http import HttpResponse
from django.db.models import Count

def run_stats(request_obj, **kwargs):
    """

    Returns stats on a given request set.


    """
    stats = {}


    try:
        # Average response time.
        stats['average_response'] = request_obj.filter(status="Closed") \
            .extra({"average": "avg(updated_datetime - requested_datetime)"}) \
            .values("average")
        stats['average_response'] = stats['average_response'][0]["average"].days

        # Total request count.
        stats['request_count'] = request_obj.count()

        # Request types.
        if kwargs.has_key('request_types') is False:
            stats['request_types'] = request_obj.values('service_name') \
                    .annotate(count=Count('service_name')).order_by('-count')[:10]

        # Opened requests by day (limit: 30)
        time_delta = datetime.timedelta(days=30)
        latest = request_obj.latest('requested_datetime')
        qss = qsstats.QuerySetStats(request_obj, 'requested_datetime')
        time_series = qss.time_series(latest.requested_datetime - time_delta,
               latest.requested_datetime)
        stats['opened_by_day'] = [t[1] for t in time_series]

        # Open request count.
        stats['open_request_count'] = request_obj.filter(status="Open").count()

        # Closed request count.
        stats['closed_request_count'] = request_obj.filter(status="Closed").count()

        # Recently opened requests.
        if kwargs.has_key('open_requests') is False:
            stats['open_requests'] = request_obj.filter(status="Open") \
                    .order_by('-requested_datetime')[:10]

    except:
      stats['average_response'] = 0
      stats['request_count'] = 0
      stats['request_types'] = []
      stats['open_request_count'] = 0
      stats['closed_request_count'] = 0
      stats['opened_by_day'] = [0]

    # Return
    return stats

def calculate_delta(new, old):
    try:
        delta = int(round(((float(new) / old)-1) * 100))
    except:
        delta = 100

    return delta

# Handle string/date conversion.
def str_to_day(date):
    """Convert a YYYY-MM-DD string to a datetime object"""
    return datetime.datetime.strptime(date, '%Y-%m-%d')

def day_to_str(date):
    """Convert a datetime object into a YYYY-MM-DD string"""
    return datetime.datetime.strftime(date, '%Y-%m-%d')

def date_range(begin, end=None):
    """Returns a tuple of datetimes spanning the given range"""
    if end == None:
        date = str_to_day(begin)
        begin = datetime.datetime.combine(date, datetime.time.min)
        end = datetime.datetime.combine(date, datetime.time.max)
    else:
        begin = str_to_day(begin)
        end = str_to_day(end)

    return (begin, end)

def dt_handler(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    else:
        return None

##
# Taken from http://geodjango-basic-apps.googlecode.com/svn/trunk/projects/alpha_shapes/clustr/shortcuts.py
##
def render_to_geojson(query_set, geom_field=None, mimetype='text/plain', pretty_print=True, exclude=[]):
    '''

    Shortcut to render a GeoJson FeatureCollection from a Django QuerySet.
    Currently computes a bbox and adds a crs member as a sr.org link

    '''
    collection = {}

    # Find the geometry field
    # qs.query._geo_field()

    fields = query_set.model._meta.fields
    geo_fields = [f for f in fields if isinstance(f, GeometryField)]

    #attempt to assign geom_field that was passed in
    if geom_field:
        geo_fieldnames = [x.name for x in geo_fields]
        try:
            geo_field = geo_fields[geo_fieldnames.index(geom_field)]
        except:
            raise Exception('%s is not a valid geometry on this model' % geom_field)
    else:
        geo_field = geo_fields[0] # no support yet for multiple geometry fields

    #remove other geom fields from showing up in attributes
    if len(geo_fields) > 1:
        for gf in geo_fields:
            if gf.name not in exclude: exclude.append(gf.name)
        exclude.remove(geo_field.name)

    # Gather the projection information
    crs = {}
    crs['type'] = "link"
    crs_properties = {}
    crs_properties['href'] = 'http://spatialreference.org/ref/epsg/%s/' % geo_field.srid
    crs_properties['type'] = 'proj4'
    crs['properties'] = crs_properties
    collection['crs'] = crs

    # Build list of features
    features = []
    if query_set:
      for item in query_set:
         feat = {}
         feat['type'] = 'Feature'
         d= item.__dict__.copy()
         g = getattr(item,geo_field.name)
         d.pop(geo_field.name)
         for field in exclude:
             d.pop(field)
         feat['geometry'] = simplejson.loads(g.geojson)
         feat['properties'] = d
         features.append(feat)
    else:
        pass #features.append({'type':'Feature','geometry': {},'properties':{}})

    # Label as FeatureCollection and add Features
    collection['type'] = "FeatureCollection"
    collection['features'] = features

    # Attach extent of all features
    #if query_set:
    #    #collection['bbox'] = [x for x in query_set.extent()]
    #    agg = query_set.unionagg()
    #    collection['bbox'] = [agg.extent]
    #    collection['centroid'] = [agg.point_on_surface.x,agg.point_on_surface.y]

    # Return response
    response = HttpResponse()
    if pretty_print:
        response.write('%s' % simplejson.dumps(collection, indent=1))
    else:
        response.write('%s' % simplejson.dumps(collection))
    response['Content-length'] = str(len(response.content))
    response['Content-Type'] = mimetype
    return response

##
# JSON SERIALIZER FROM:
##
class UnableToSerializeError(Exception):
    """ Error for not implemented classes """
    def __init__(self, value):
        self.value = value
        Exception.__init__(self)

    def __str__(self):
        return repr(self.value)

class JSONSerializer():
    boolean_fields = ['BooleanField', 'NullBooleanField']
    datetime_fields = ['DatetimeField', 'DateField', 'TimeField']
    number_fields = ['IntegerField', 'AutoField', 'DecimalField', 'FloatField', 'PositiveSmallIntegerField']

    def serialize(self, obj, **options):
        self.options = options

        self.stream = options.pop("stream", StringIO())
        self.selectedFields = options.pop("fields", None)
        self.ignoredFields = options.pop("ignored", None)
        self.use_natural_keys = options.pop("use_natural_keys", False)
        self.currentLoc = ''

        self.level = 0

        self.start_serialization()

        self.handle_object(obj)

        self.end_serialization()
        return self.getvalue()

    def get_string_value(self, obj, field):
        """Convert a field's value to a string."""
        return smart_unicode(field.value_to_string(obj))

    def start_serialization(self):
        """Called when serializing of the queryset starts."""
        pass

    def end_serialization(self):
        """Called when serializing of the queryset ends."""
        pass

    def start_array(self):
        """Called when serializing of an array starts."""
        self.stream.write(u'[')
    def end_array(self):
        """Called when serializing of an array ends."""
        self.stream.write(u']')

    def start_object(self):
        """Called when serializing of an object starts."""
        self.stream.write(u'{')

    def end_object(self):
        """Called when serializing of an object ends."""
        self.stream.write(u'}')

    def handle_object(self, object):
        """ Called to handle everything, looks for the correct handling """
        if isinstance(object, dict):
            self.handle_dictionary(object)
        elif isinstance(object, list):
            self.handle_list(object)
        elif isinstance(object, Model):
            self.handle_model(object)
        elif isinstance(object, QuerySet):
            self.handle_queryset(object)
        elif isinstance(object, bool):
            self.handle_simple(object)
        elif isinstance(object, int) or isinstance(object, float) or isinstance(object, long):
            self.handle_simple(object)
        elif isinstance(object, basestring):
            self.handle_simple(object)
        else:
            raise UnableToSerializeError(type(object))

    def handle_dictionary(self, d):
        """Called to handle a Dictionary"""
        i = 0
        self.start_object()
        for key, value in d.iteritems():
            self.currentLoc += key+'.'
            #self.stream.write(unicode(self.currentLoc))
            i += 1
            self.handle_simple(key)
            self.stream.write(u': ')
            self.handle_object(value)
            if i != len(d):
                self.stream.write(u', ')
            self.currentLoc = self.currentLoc[0:(len(self.currentLoc)-len(key)-1)]
        self.end_object()

    def handle_list(self, l):
        """Called to handle a list"""
        self.start_array()

        for value in l:
            self.handle_object(value)
            if l.index(value) != len(l) -1:
                self.stream.write(u', ')

        self.end_array()

    def handle_model(self, mod):
        """Called to handle a django Model"""
        self.start_object()

        for field in mod._meta.local_fields:
            if field.rel is None:
                if self.selectedFields is None or field.attname in self.selectedFields or field.attname:
                    if self.ignoredFields is None or self.currentLoc + field.attname not in self.ignoredFields:
                        self.handle_field(mod, field)
            else:
                if self.selectedFields is None or field.attname[:-3] in self.selectedFields:
                    if self.ignoredFields is None or self.currentLoc + field.attname[:-3] not in self.ignoredFields:
                        self.handle_fk_field(mod, field)
        for field in mod._meta.many_to_many:
            if self.selectedFields is None or field.attname in self.selectedFields:
                if self.ignoredFields is None or self.currentLoc + field.attname not in self.ignoredFields:
                    self.handle_m2m_field(mod, field)
        self.stream.seek(self.stream.tell()-2)
        self.end_object()

    def handle_queryset(self, queryset):
        """Called to handle a django queryset"""
        self.start_array()
        it = 0
        for mod in queryset:
            it += 1
            self.handle_model(mod)
            if queryset.count() != it:
                self.stream.write(u', ')
        self.end_array()

    def handle_field(self, mod, field):
        """Called to handle each individual (non-relational) field on an object."""
        self.handle_simple(field.name)
        if field.get_internal_type() in self.boolean_fields:
            if field.value_to_string(mod) == 'True':
                self.stream.write(u': true')
            elif field.value_to_string(mod) == 'False':
                self.stream.write(u': false')
            else:
                self.stream.write(u': undefined')
        else:
            self.stream.write(u': ')
            self.handle_simple(field.value_to_string(mod))
        self.stream.write(u', ')

    def handle_fk_field(self, mod, field):
        """Called to handle a ForeignKey field."""
        related = getattr(mod, field.name)
        if related is not None:
            if field.rel.field_name == related._meta.pk.name:
                # Related to remote object via primary key
                pk = related._get_pk_val()
            else:
                # Related to remote object via other field
                pk = getattr(related, field.rel.field_name)
            d = {
                    'pk': pk,
                }
            if self.use_natural_keys and hasattr(related, 'natural_key'):
                d.update({'natural_key': related.natural_key()})
            if type(d['pk']) == str and d['pk'].isdigit():
                d.update({'pk': int(d['pk'])})

            self.handle_simple(field.name)
            self.stream.write(u': ')
            self.handle_object(d)
            self.stream.write(u', ')

    def handle_m2m_field(self, mod, field):
        """Called to handle a ManyToManyField."""
        if field.rel.through._meta.auto_created:
            self.handle_simple(field.name)
            self.stream.write(u': ')
            self.start_array()
            hasRelationships = False
            for relobj in getattr(mod, field.name).iterator():
                hasRelationships = True
                pk = relobj._get_pk_val()
                d = {
                        'pk': pk,
                    }
                if self.use_natural_keys and hasattr(relobj, 'natural_key'):
                    d.update({'natural_key': relobj.natural_key()})
                if type(d['pk']) == str and d['pk'].isdigit():
                    d.update({'pk': int(d['pk'])})

                self.handle_simple(d)
                self.stream.write(u', ')
            if hasRelationships:
                self.stream.seek(self.stream.tell()-2)
            self.end_array()
            self.stream.write(u', ')

    def handle_simple(self, simple):
        """ Called to handle values that can be handled via simplejson """
        self.stream.write(unicode(dumps(simple)))

    def getvalue(self):
        """Return the fully serialized object (or None if the output stream is  not seekable).sss """
        if callable(getattr(self.stream, 'getvalue', None)):
            return self.stream.getvalue()

def json_response_from(response):
    jsonSerializer = JSONSerializer()
    return HttpResponse(jsonSerializer.serialize(response, use_natural_keys=True), mimetype='application/json')
