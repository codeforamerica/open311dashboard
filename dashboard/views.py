from open311dashboard.settings import CITY
from open311dashboard.dashboard.models import Request

from django.http import HttpResponse, HttpRequest
from django.template import Context
from django.shortcuts import render
from django.db.models import Count
from django.core import serializers

from open311dashboard.dashboard.utils import str_to_day, day_to_str, \
    date_range, dt_handler

import json
import datetime
import qsstats
import time

def index(request):
    return render(request, 'index.html')

def test(request):
    request_list = Request.objects.all()[:10]
    c = Context({
        'request_list': request_list,
        'city': CITY['NAME'],
        })
    return render(request, 'test.html', c)

# API Views
def ticket_days(request, ticket_status="opened", start=None, end=None,
        num_days=None):
    '''Returns JSON with the number of opened/closed tickets in a specified
    date range'''
    print ticket_status
    if ticket_status == "opened":
        request = Request.objects.all()
        stats = qsstats.QuerySetStats(request, 'requested_datetime')
    elif ticket_status == "closed":
        request = Request.objects.filter(status="Closed")
        stats = qsstats.QuerySetStats(request, 'updated_datetime')
    elif ticket_status == "both":
        request_opened = Request.objects.all()
        stats_opened = qsstats.QuerySetStats(request_opened,
                                             'requested_datetime')

        request_closed = Request.objects.filter(status="Closed")
        stats_closed = qsstats.QuerySetStats(request_closed,
                                             'updated_datetime')
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

    data = []

    try:
        raw_data = stats.time_series(start, end, engine='postgres')

        for row in raw_data:
            temp_data = {'date': int(time.mktime(row[0].timetuple())), 'count': row[1]}
            data.append(temp_data)
    except:
        opened_data = stats_opened.time_series(start, end, engine='postgres')
        closed_data = stats_closed.time_series(start, end, engine='postgres')

        for i in range(len(opened_data)):
            temp_data = {'date': int(time.mktime(opened_data[i][0].timetuple())),
                         'opened_count': opened_data[i][1],
                         'closed_count': closed_data[i][1],
                         }
            data.append(temp_data)

    json_data = json.dumps(data)

    return HttpResponse(json_data, content_type='application/json')

# Get service_name stats for a range of dates
def ticket_day(request, begin=day_to_str(datetime.date.today()), end=None):
    if end == None:
        key = begin
    else:
        key = "% - %" % [begin, end]

    # Request and group by service_name.
    requests = Request.objects \
            .filter(requested_datetime__range=date_range(begin, end)) \
            .values('service_name').annotate(count=Count('service_name'))

    data = {key: [item for item in requests]}
    json_data = json.dumps(data)

    return HttpResponse(json_data, content_type='application/json')

# List requests in a given date range
def list_requests(request, begin=day_to_str(datetime.date.today()), end=None):
    requests = Request.objects \
        .filter(requested_datetime__range=date_range(begin,end))

    data = [item for item in requests.values()]
    json_data = json.dumps(data, default=dt_handler)
    return HttpResponse(json_data, content_type='application/json')
