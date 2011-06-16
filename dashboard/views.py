from dashboard.models import Request

from django.template import Context
from django.shortcuts import render

def index(request):
    request_list = Request.objects.all()[:10]
    c = Context({
        'request_list': request_list
        })
    return render(request, 'index.html', c)
