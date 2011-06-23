from open311dashboard.settings import CITY
from open311dashboard.dashboard.models import Request

from django.http import HttpResponse, HttpRequest
from django.template import Context
from django.shortcuts import render

from open311dashboard.dashboard.utils import str_to_day, day_to_str

import json
import datetime
import qsstats

def index(request):
    request_list = Request.objects.all()[:10]
    c = Context({
        'request_list': request_list,
        'city': CITY['NAME'],
        })
    return render(request, 'index.html', c)

# API Views
def ticket_days(request, ticket_status="opened", start=None, end=None,
        num_days=None):
    '''Returns JSON with the number of opened/closed tickets in a specified
    date range'''
    if ticket_status == "opened":
        request = Request.objects.all()
        stats = qsstats.QuerySetStats(request, 'requested_datetime')
    elif ticket_status == "closed":
        request = Request.objects.filter(status="Closed")
        stats = qsstats.QuerySetStats(request, 'updated_datetime')

    # If no start or end variables are passed, do the past 30 days. If one is
    # passed, check if num_days and do the past num_days. If num_days isn't
    # passed, just do one day. Else, do the range.
    if start == None and end == None:
        end = datetime.date.today()
        start = end - datetime.timedelta(days=30)
    elif end != None and num_days != None:
        end = str_to_day(end)
        start = end - datetime.timedelta(days=int(num_days))
    elif end != None:
        end = str_to_day(end)
        start = end
    else:
        start = str_to_day(start)
        end = str_to_day(end)

    raw_data = stats.time_series(start, end, engine='postgres')
    data = []

    for row in raw_data:
        temp_data = {'date': day_to_str(row[0]), 'count': row[1]}
        data.append(temp_data)

    json_data = json.dumps(data)

    return HttpResponse(json_data, content_type='application/json')

def ticket_day(request, day=day_to_str(datetime.date.today())):
    date = str_to_day(day)
    return
