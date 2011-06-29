from django.http import HttpResponse

import json

class ApiHandler(object):
    """When passed lists or dicts, it will return them in various serialized
    forms. Defaults to JSON, can also do JSONP."""

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        request = args[0]
        format = request.GET.get('format')

        response = self.func(*args, **kwargs)
        if format == 'jsonp':
            data = json.dumps(response)
            callback = request.GET.get('callback')

            if callback:
                data = "%s(%s)" % (callback, data)
                mime_type = 'application/javascript'
        else:
            mime_type = 'application/json'
            data = json.dumps(response)

        return HttpResponse(data, content_type=mime_type)
