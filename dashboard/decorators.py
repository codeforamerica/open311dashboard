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

        if format == 'json':
            response = self.func(*args, **kwargs)
            data = json.dumps(response)
            return_val = HttpResponse(data, content_type='application/json')

        return return_val
