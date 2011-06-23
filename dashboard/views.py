from open311dashboard.settings import CITY
from open311dashboard.dashboard.models import Request

from django.http import HttpResponse, HttpRequest
from django.template import Context
from django.shortcuts import render

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
    # passed, do the 30 days prior to that date. If both, do the range.
    if start == None and end == None:
        end = datetime.date.today()
        start = end - datetime.timedelta(days=30)
    elif end != None and num_days != None:
        end = datetime.datetime.strptime(end, '%Y-%m-%d')
        start = end - datetime.timedelta(days=int(num_days))
    elif end != None:
        end = datetime.datetime.strptime(end, '%Y-%m-%d')
        start = end
    else:
        start = datetime.datetime.strptime(start, '%Y-%m-%d')
        end = datetime.datetime.strptime(end, '%Y-%m-%d')

    raw_data = stats.time_series(start, end, engine='postgres')
    data = []

    for row in raw_data:
        temp_data = {'date': datetime.datetime.strftime(row[0], '%Y-%m-%d'),
                'count': row[1]}
        data.append(temp_data)

    json_data = json.dumps(data)

    return HttpResponse(json_data, content_type='application/json')
