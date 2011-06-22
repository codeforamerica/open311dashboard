from open311dashboard.dashboard.models import Request

from django.http import HttpResponse, HttpRequest
from django.template import Context
from django.shortcuts import render

import json
import datetime

def index(request):
    request_list = Request.objects.all()[:10]
    c = Context({
        'request_list': request_list
        })
    return render(request, 'index.html', c)

def ticket_days(request, ticket_status="open", start=None, end=None):
    if start == None:
        tickets_opened = Request.objects.status_count(status=ticket_status)
    else:
        tickets_opened = Request.objects.status_count(status=ticket_status,
                startdate=start,
                enddate=end)

    tickets = []
    for ticket in tickets_opened:
        formatted_date = datetime.datetime.strftime(ticket.date,
                "%Y-%m-%d")
        row = {'date': formatted_date,
                'count': ticket.count }
        tickets.append(row)

    data = json.dumps(tickets)

    return HttpResponse(data)
