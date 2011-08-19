import datetime
import qsstats
import time
import json
import urllib
import urllib2

from django.template import Context
from django.shortcuts import render, redirect
from django.db.models import Count
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance as D

from dashboard.models import Request, City, Geography, Street
from dashboard.decorators import ApiHandler
from dashboard.utils import str_to_day, day_to_str, \
    date_range, dt_handler, render_to_geojson, run_stats, calculate_delta, \
    json_response_from


# Thirty minutes for caching.
CACHE_TIME = 30 * 60

@cache_page(CACHE_TIME)
def index(request, geography=None, is_json=False):
    """
    Homepage view. Can also return json for the city or neighborhoods.
    """
    if geography is None:
        requests = Request.objects.all()
    else:
        neighborhood = Geography.objects.get(pk=geography)
        requests = Request.objects.filter(geo_point__contained=neighborhood.geo)

    total_open = requests.filter(status="Open").count()
    most_recent = requests.latest('requested_datetime')
    minus_7 = most_recent.requested_datetime-datetime.timedelta(days=7)
    minus_14 = most_recent.requested_datetime-datetime.timedelta(days=14)

    this_week = requests.filter(requested_datetime__range= \
            (minus_7, most_recent.requested_datetime))
    last_week = requests.filter(requested_datetime__range= \
            (minus_14, minus_7))

    this_week_stats = run_stats(this_week, request_types=False,
            open_requests=False)
    last_week_stats = run_stats(last_week, request_types=False,
            open_requests=False)

    # Calculate deltas
    delta = {}
    delta['count'] = calculate_delta(this_week_stats['request_count'],
            last_week_stats['request_count'])
    delta['closed_count'] = calculate_delta( \
            this_week_stats['closed_request_count'],
            last_week_stats['closed_request_count'])
    delta['opened_count'] = calculate_delta( \
            this_week_stats['open_request_count'],
            last_week_stats['open_request_count'])
    delta['time'] = calculate_delta(this_week_stats['average_response'],
            last_week_stats['average_response'])

    # Put everything in a dict so we can do what we want with it.
    c_dict = {
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
        return HttpResponse(data, content_type='application/json')

# Neighborhood specific pages.
@cache_page(CACHE_TIME)
def neighborhood_list(request):
    """
    List the neighborhoods.
    """
    neighborhoods = Geography.objects.all()

    c = Context({
        'neighborhoods': neighborhoods
        })

    return render(request, 'neighborhood_list.html', c)

@cache_page(CACHE_TIME)
def neighborhood_detail(request, neighborhood_id):
    """

    Show detail for a specific neighborhood. Uses templates/geo_detail.html

    """
    neighborhood = Geography.objects.get(pk=neighborhood_id)
    nearby = Geography.objects.all().distance(neighborhood.geo) \
            .exclude(name=neighborhood.name).order_by('distance')[:5]

    # Get the requests inside the neighborhood, run the stats
    requests = Request.objects.filter(geo_point__contained=neighborhood.geo)
    stats = run_stats(requests)

    title = neighborhood.name

    neighborhood.geo.transform(4326)
    simple_shape = neighborhood.geo.simplify(.0003,
            preserve_topology=True)

    c = Context({
        'title': title,
        'geometry': simple_shape.geojson,
        'centroid': [simple_shape.centroid[0], simple_shape.centroid[1]],
        'extent': simple_shape.extent,
        'stats': stats,
        'nearby': nearby,
        'type': 'neighborhood',
        'id': neighborhood_id
        })

    return render(request, 'geo_detail.html', c)

@cache_page(CACHE_TIME)
def neighborhood_detail_json(request, neighborhood_id):
    """

    Download JSON of the requests that built the page. Caution: slow!

    TODO: Speed it up.

    """
    neighborhood = Geography.objects.get(pk=neighborhood_id)
    requests = Request.objects.filter(geo_point__contained=neighborhood.geo)
    return json_response_from(requests)

# Street specific pages.
@cache_page(CACHE_TIME)
def street_list(request):
    """

    List the top 10 streets by open service requests.

    """
    streets = Street.objects.filter(request__status="Open") \
            .annotate(count=Count('request__service_request_id')) \
            .order_by('-count')[:10]

    c = Context({
        'top_streets': streets
        })

    return render(request, 'street_list.html', c)

@cache_page(CACHE_TIME)
def street_view(request, street_id):
    """

    View details for a specific street. Renders geo_detail.html like
    neighborhood_detail does.
    """
    street = Street.objects.get(pk=street_id)
    nearby = Street.objects.all().distance(street.line) \
            .exclude(street_name=street.street_name).order_by('distance')[:5]
    neighborhood = Geography.objects.all() \
            .distance(street.line).order_by('distance')[:1]

    # Max/min addresses
    addresses = [street.left_low_address, street.left_high_address,
                 street.right_low_address, street.right_high_address]
    addresses.sort()

    title = "%s %i - %i" % (street.street_name, addresses[0], addresses[3])

    # Requests
    requests = Request.objects.filter(street=street_id)
    stats = run_stats(requests)

    street.line.transform(4326)

    c = Context({
        'title': title,
        'geometry': street.line.geojson,
        'centroid': [street.line.centroid[0], street.line.centroid[1]],
        'extent': street.line.extent,
        'stats': stats,
        'nearby': nearby,
        'neighborhood': neighborhood[0],
        'type': 'street',
        'id': street_id
        })

    return render(request, 'geo_detail.html', c)

def street_view_json(request, street_id):
    """

    Download the JSON for the requests that built the page.

    """
    requests = Request.objects.filter(street=street_id)
    return json_response_from(requests)


# Search for an address!
@cache_page(CACHE_TIME)
def street_search(request):
    """
    Do a San Francisco specific geocode and then match that against our street
    centerline data.

    TODO: Maybe cache the lookups?
    """
    query = request.GET.get('q','')

    if query:
        # Lookup the search string with Yahoo!
        url = "http://where.yahooapis.com/geocode"
        params = {"addr": query,
                "line2": "San Francisco, CA",
                "flags": "J",
                "appid": "1I9Jh.3V34HMiBXzxZRYmx.DO1JfVJtKh7uvDTJ4R0dRXnMnswRHXbai1NFdTzvC" }

        query_params = urllib.urlencode(params)
        data = urllib2.urlopen("%s?%s" % (url,
            query_params)).read()

        print data

        temp_json = json.loads(data)

        if temp_json['ResultSet']['Results'][0]['quality'] > 50:
            lon = temp_json['ResultSet']['Results'][0]["longitude"]
            lat = temp_json['ResultSet']['Results'][0]["latitude"]

            point = Point(float(lon), float(lat))
            point.srid = 4326
            point.transform(900913)

                    # .all() \
            nearest_street = Street.objects \
                    .filter(line__dwithin=(point, D(m=100))) \
                    .distance(point).order_by('distance')[:1]
            return redirect(nearest_street[0])
        else:
            c = Context({'error': True})
            return render(request, 'search.html', c)
    else:
        return render(request, 'search.html')

@cache_page(CACHE_TIME)
def map(request):
    """
    Simply render the map.

    TODO: Get the centroid and bounding box of the city and set that. (See
    neighborhood_detail and geo_detail.html for how this would look)
    """
    return render(request, 'map.html')

# Admin Pages
@login_required
def admin(request):
    """

    Admin home page. Just list the cities.

    """
    cities = City.objects.all()
    c = Context({'cities': cities})
    return render(request, 'admin/index.html', c)

@login_required
def city_admin(request, shortname=None):
    """

    Administer a specific city (and associated data)

    """
    city = City.objects.get(short_name=shortname)
    geographies = Geography.objects.filter(city=city.id).count()
    streets = Street.objects.filter(city=city.id).count()
    requests = Request.objects.filter(city=city.id).count()

    c = Context({
        'city': city,
        'geographies': geographies,
        'streets': streets,
        'requests': requests
        })

    return render(request, 'admin/city_view.html', c)

@login_required
def city_add (request):
    """

    Add a new city.

    """
    return render(request, 'admin/city_add.html')

# API Views
@ApiHandler
def ticket_days(request, ticket_status="open", start=None, end=None,
                num_days=None):
    '''Returns JSON with the number of opened/closed tickets in a specified
    date range'''

    # If no start or end variables are passed, do the past 30 days. If one is
    # passed, check if num_days and do the past num_days. If num_days isn't
    # passed, just do one day. Else, do the range.
    if start is None and end is None:
        num_days = int(num_days) if num_days is not None else 29

        end = datetime.date.today()
        start = end - datetime.timedelta(days=num_days)
    elif end is not None and num_days is not None:
        num_days = int(num_days) - 1
        end = str_to_day(end)
        start = end - datetime.timedelta(days=num_days)
    elif end is not None and start is None:
        end = str_to_day(end)
        start = end
    else:
        start = str_to_day(start)
        end = str_to_day(end)

    if ticket_status == "open":
        request = Request.objects.filter(status="Open") \
            .filter(requested_datetime__range=date_range(day_to_str(start),
                                                         day_to_str(end)))
        stats = qsstats.QuerySetStats(request, 'requested_datetime')
    elif ticket_status == "closed":
        request = Request.objects.filter(status="Closed")
        stats = qsstats.QuerySetStats(request, 'updated_datetime') \
            .filter(requested_datetime__range=date_range(day_to_str(start),
                                                         day_to_str(end)))
    elif ticket_status == "both":
        request_opened = Request.objects.filter(status="Open") \
            .filter(requested_datetime__range=date_range(day_to_str(start),
                                                         day_to_str(end)))
        stats_opened = qsstats.QuerySetStats(request_opened,
                                             'requested_datetime')

        request_closed = Request.objects.filter(status="Closed") \
            .filter(requested_datetime__range=date_range(day_to_str(start),
                                                         day_to_str(end)))
        stats_closed = qsstats.QuerySetStats(request_closed,
                                             'updated_datetime')

    data = []

    try:
        raw_data = stats.time_series(start, end)

        for row in raw_data:
            temp_data = {'date': int(time.mktime(row[0].timetuple())), 'count': row[1]}
            data.append(temp_data)
    except:
        opened_data = stats_opened.time_series(start, end)
        closed_data = stats_closed.time_series(start, end)
        for i in range(len(opened_data)):
            temp_data = {
                'date': int(time.mktime(opened_data[i][0].timetuple())),
                'open_count': opened_data[i][1],
                'closed_count': closed_data[i][1],
            }
            data.append(temp_data)
    return data

@ApiHandler
def ticket_day(request, begin=day_to_str(datetime.date.today()), end=None):
    """

    Get service_name stats for a range of dates.

    """
    if end == None:
        key = begin
    else:
        key = "%s - %s" % (begin, end)

    # Request and group by service_name.
    requests = Request.objects \
            .filter(requested_datetime__range=date_range(begin, end)) \
            .values('service_name').annotate(count=Count('service_name')) \
            .order_by('-count')

    data = {key: [item for item in requests]}
    return data

# List requests in a given date range
@ApiHandler
def list_requests(request, begin=day_to_str(datetime.date.today()), end=None):
    """

    List requests opened in a given date range

    """
    requests = Request.objects \
        .filter(requested_datetime__range=date_range(begin,end))

    data = [item for item in requests.values()]
    return data
