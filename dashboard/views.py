from open311dashboard.dashboard.models import Request

from django.http import HttpResponse, HttpRequest
from django.template import Context
from django.shortcuts import render
from django.core import serializers

def index(request):
    request_list = Request.objects.all()[:10]
    c = Context({
        'request_list': request_list
        })
    return render(request, 'index.html', c)

def json_test(request):
    if HttpRequest.is_ajax(request):
        data = serializers.serialize('json', Request.objects.all()[:10])
        return HttpResponse(data)
    else:
        return HttpResponse("Not ajax.")

