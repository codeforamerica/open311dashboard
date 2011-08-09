from open311dashboard.dashboard.models import Request, City, Geography, Street

from django.template import Context
from django.shortcuts import render, redirect
from django.db.models import Count

from django.contrib.auth.decorators import login_required

from open311dashboard.dashboard.utils import str_to_day, day_to_str, \
    date_range, dt_handler, render_to_geojson, run_stats
from open311dashboard.dashboard.decorators import ApiHandler
from django.contrib.gis.geos import Point

import datetime
import qsstats
import time
import json
import urllib
import urllib2

def index(request):
    total_open = Request.objects.filter(status="Open").count()
    most_recent = Request.objects.latest('requested_datetime')
    minus_7 = most_recent.requested_datetime-datetime.timedelta(days=7)
    minus_14 = most_recent.requested_datetime-datetime.timedelta(days=14)

    this_week = Request.objects.filter(requested_datetime__range= \
            (minus_7, most_recent.requested_datetime))
    last_week = Request.objects.filter(requested_datetime__range= \
            (minus_14, minus_7))

    # Calculate the request delta from the latest 2 weeks of data.
    this_week_count = this_week.count()
    last_week_count = last_week.count()

    try:
        delta_count = int(round(((float(this_week_count)/last_week_count)-1) *
            100))
    except:
        delta_count = 100

    # Calculate the number of closed tickets in the last week.
    this_week_closed_count = this_week.filter(status="Closed").count()
    last_week_closed_count = last_week.filter(status="Closed").count()

    try:
        delta_closed_count = int(round(((float(this_week_closed_count) /
            last_week_closed_count)-1) * 100))
    except:
        delta_closed_count = 100

    # Calculate the responsiveness delta from the latest 2 weeks of data.
    this_week_time = this_week.filter(status="Closed") \
            .extra({"average": "avg(updated_datetime - requested_datetime)"}) \
            .values("average")
    last_week_time = last_week.filter(status="Closed") \
            .extra({"average": "avg(updated_datetime - requested_datetime)"}) \
            .values("average")

    this_week_days = this_week_time[0]["average"].days
    last_week_days = last_week_time[0]["average"].days

    try:
        delta_time = int(round(((float(this_week_days) /
            last_week_days)-1) * 100))
    except:
        delta_time = 100

    c = Context({
        'open_tickets': total_open,
        'latest': most_recent.requested_datetime,
        'delta_created_count': delta_count,
        'delta_closed_count': delta_closed_count,
        'this_week_created_count': this_week_count,
        'this_week_closed_count': this_week_closed_count,
        'this_week_time': this_week_days,
        'delta_time': delta_time,
        })
    return render(request, 'index.html', c)

# Neighborhood specific pages.
def neighborhood_list(request):
    neighborhoods = Geography.objects.all()

    c = Context({
        'neighborhoods': neighborhoods
        })

    return render(request, 'neighborhood_list.html', c)

def neighborhood_detail(request, neighborhood_id):
    neighborhood = Geography.objects.get(pk=neighborhood_id)

    # Get the requests inside the neighborhood, run the stats
    requests = Request.objects.filter(geo_point__contained=neighborhood.geo)
    stats = run_stats(requests)

    c = Context({
        'neighborhood': neighborhood,
        'stats': stats
        })
    return render(request, 'neighborhood_detail.html', c)

# Street specific pages.
def street_list(request):
    streets = Street.objects.filter(request__status="Open") \
            .annotate(count=Count('request__service_request_id')) \
            .order_by('-count')[:10]

    c = Context({
        'top_streets': streets
        })

    return render(request, 'street_list.html', c)

def street_view(request, street_id):
    street = Street.objects.get(pk=street_id)

    # Max/min addresses
    addresses = [street.left_low_address, street.left_high_address,
                 street.right_low_address, street.right_high_address]
    addresses.sort()

    # Requests
    requests = Request.objects.filter(street=street_id)
    request_types = requests.values('service_name') \
                .annotate(count=Count('service_name')).order_by('-count')
    open_requests = requests.filter(status="Open") \
            .order_by('-requested_datetime')[:10]

    try:
        request_averages = requests \
            .extra({"average": "avg(updated_datetime - requested_datetime)"}) \
            .values("average")
        request_averages = request_averages[0]['average'].days
    except:
        request_averages = None

    c = Context({
        'street': street,
        'addresses': addresses,
        'request_types': request_types,
        'averages': request_averages,
        'open_requests': open_requests
        })

    return render(request, 'street_detail.html', c)

# Search for an address!
def street_search(request):
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

            nearest_street = Street.objects.all().distance(point).order_by('distance')[:1]
            return redirect(nearest_street[0])
        else:
            c = Context({'error': True})
            return render(request, 'search.html', c)
    else:
        return render(request, 'search.html')

def map(request):
    return render(request, 'map.html')

# Admin Pages
@login_required
def admin(request):
    cities = City.objects.all()

    c = Context({
        'cities': cities
        })
    return render(request, 'admin/index.html', c)

@login_required
def city_admin(request, shortname=None):
    # try:
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
    # except:
        # return HttpResponseRedirect(reverse(admin))

@login_required
def city_add (request):
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
            temp_data = {'date': int(time.mktime(opened_data[i][0].timetuple())),
                    'open_count': opened_data[i][1],
                     'closed_count': closed_data[i][1],
                     }
            data.append(temp_data)
    return data

# Get service_name stats for a range of dates
@ApiHandler
def ticket_day(request, begin=day_to_str(datetime.date.today()), end=None):
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
    requests = Request.objects \
        .filter(requested_datetime__range=date_range(begin,end))

    data = [item for item in requests.values()]
    return data
