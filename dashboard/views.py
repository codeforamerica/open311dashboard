from open311dashboard.dashboard.models import Request, City, Geography, Street

from django.template import Context
from django.shortcuts import render
from django.db.models import Count

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

from open311dashboard.dashboard.utils import str_to_day, day_to_str, \
    date_range, dt_handler, render_to_geojson
from open311dashboard.dashboard.decorators import ApiHandler

import datetime
import qsstats
import time

def index(request):
    total_open = Request.objects.filter(status="Open").count()
    most_recent = Request.objects.latest('requested_datetime')

    c = Context({
        'open_tickets': total_open,
        'latest': most_recent.requested_datetime
        })
    return render(request, 'index.html', c)

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
