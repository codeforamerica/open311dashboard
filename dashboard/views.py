try:
    import simplejson as json
except:
    import json

import urllib
import urllib2

from django.template import Context
from django.shortcuts import render # , redirect
# from django.http import HttpResponse

from pymongo.connection import Connection

from settings import MONGODB

# Set up the database connection as a global variable
connection = Connection(MONGODB['host'])
db = connection[MONGODB['db']]

def index(request, geography=None, is_json=False):
    """
    Homepage view. Can also return json for the city or neighborhoods.
    """

    """c_dict = {
        'open_tickets': total_open,
        'this_week_stats': this_week_stats,
        'last_week_stats': last_week_stats,
        'delta': delta,
    }

    if is_json is False:
        neighborhoods = Geography.objects.all()
        c_dict['neighborhoods'] = neighborhoods
        c_dict['latest'] = most_recent.requested_datetime
        c = Context(c_dict)
        return render(request, 'index.html', c)
    else:
        data = json.dumps(c_dict, True)
        return HttpResponse(data, content_type='application/json')"""


# Neighborhood specific pages.
def neighborhood_list(request):
    """
    List the neighborhoods.
    """
    # neighborhoods = Geography.objects.all()
    neighborhoods = db.polygons.find({ 'properties.type' : 'neighborhood' })

    c = Context({
        'neighborhoods': neighborhoods
        })

    return render(request, 'neighborhood_list.html', c)


def neighborhood_detail(request, neighborhood_slug):
    """

    Show detail for a specific neighborhood. Uses templates/geo_detail.html

    """
    neighborhood = db.polygons \
            .find_one({ 'properties.slug' : neighborhood_slug})
    requests = db.requests.find({'coordinates' :
        { '$within' : neighborhood['geometry']['coordinates'] }
        }).limit(10)

    c = Context({
        'neighborhood' : neighborhood,
        'json' : json.dumps(neighborhood['geometry']),
        'requests' : requests
        })
    return render(request, 'neighborhood_test.html', c)
    """c = Context({
        'title': title,
        'geometry': simple_shape.geojson,
        'centroid': [simple_shape.centroid[0], simple_shape.centroid[1]],
        'extent': simple_shape.extent,
        'stats': stats,
        'nearby': nearby,
        'type': 'neighborhood',
        'id': neighborhood_id
        })

    return render(request, 'geo_detail.html', c) """


def neighborhood_detail_json(request, neighborhood_id):
    """

    Download JSON of the requests that built the page. Caution: slow!

    TODO: Speed it up.

    """

# Street specific pages.
def street_list(request):
    """

    List the top 10 streets by open service requests.

    """
    streets = db.streets.find({}).limit(25)
    c = Context({
        'streets' : streets
        })

    return render(request, 'street_list.html', c)


def street_view(request, street_name, min_val, max_val):
    """
    View details for a specific street. Renders geo_detail.html like
    neighborhood_detail does.
    """
    street = db.streets.find_one( {
        'properties.slug' : street_name,
        'properties.min' : int(min_val),
        'properties.max' : int(max_val) }
        )

    c = Context({
        'street': street,
        'json' : json.dumps(street['geometry'])
        })

    return render(request, 'street_test.html', c)

# Search for an address!
def street_search(request):
    """
    Do a San Francisco specific geocode and then match that against our street
    centerline data.
    """
    query = request.GET.get('q')
    lat = request.GET.get('lat')
    lon = request.GET.get('lng')
    if not query:
        # They haven't searched for anything.
        return render(request, 'search.html')
    elif query and not lat:
        # Lookup the search string with Yahoo!
        url = "http://where.yahooapis.com/geocode"
        params = {"addr": query,
                "line2": "San Francisco, CA",
                "flags": "J",
                "appid": "1I9Jh.3V34HMiBXzxZRYmx.DO1JfVJtKh7uvDTJ4R0dRXnMnswRHXbai1NFdTzvC" }

        query_params = urllib.urlencode(params)
        data = urllib2.urlopen("%s?%s" % (url, query_params)).read()

        print data

        temp_json = json.loads(data)

        if temp_json['ResultSet']['Results'][0]['quality'] > 50:
            lon = temp_json['ResultSet']['Results'][0]["longitude"]
            lat = temp_json['ResultSet']['Results'][0]["latitude"]
        else:
            lat, lon = None, None

    """ if lat and lon:
        nearest_street = Street.objects \
                               .filter(line__dwithin=(point, D(m=100))) \
                               .distance(point).order_by('distance')[:1]
        try:
            return redirect(nearest_street[0])
        except IndexError:
            pass
    c = Context({'error': True})
    return render(request, 'search.html', c) """


def map(request):
    """
    Simply render the map.

    TODO: Get the centroid and bounding box of the city and set that. (See
    neighborhood_detail and geo_detail.html for how this would look)
    """
    return render(request, 'map.html')
