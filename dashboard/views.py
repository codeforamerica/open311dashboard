from open311dashboard.settings import CITY
from open311dashboard.dashboard.models import Request

from django.http import HttpResponse, HttpRequest
from django.template import Context
from django.shortcuts import render

import json
import datetime
import qsstats

def index(request):
    return render(request,'index.html')

def city(request):
    request_list = Request.objects.all()[:10]
    c = Context({
        'request_list': request_list,
        'city': CITY['NAME'],
        })
    return render(request, 'city.html', c)

def ticket_days(request, ticket_status="opened", start=None, end=None):
    if ticket_status == "opened":
        request = Request.objects.all()
        stats = qsstats.QuerySetStats(request, 'requested_datetime')
    elif ticket_status == "closed":
        request = Request.objects.filter(status="Closed")
        stats = qsstats.QuerySetStats(request, 'updated_datetime')

    if start == None:
        end = datetime.date.today()
        start = end - datetime.timedelta(days=30)
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

    return HttpResponse(json_data)# , content_type='application/json')
