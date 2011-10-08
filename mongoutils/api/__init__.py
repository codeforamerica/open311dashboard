"""
Helper method(s) for handling API requests.
"""
try:
    import simplejson as json
except:
    import json

import re
import datetime

import bson

def api_query(collection, get_params, geo=False):
    """
    Formulate a query based on request parameters.
    """
    lookup = {}

    if geo:
        prefix = 'properties.'
    else:
        prefix = ''

    # Handle the special methods
    for k, v in get_params.iteritems():

        # Auto cast some stuff
        # http://stackoverflow.com/questions/7019283/automatically-type-cast-parameters-in-python
        for fn in (int, float):
            try:
                v = fn(v)
            except ValueError:
                pass

        # Handle dates.
        if re.search('date', k):
            year, month, day = v.split('-')
            v = datetime.datetime(int(year), int(month), int(day))

        # Ranges
        r = re.search('^(?P<key>.+)_(?P<side>start|end)$', k)
        if r:
            matches = r.groupdict()
            k = matches['key']
            map_dict = { 'start' : "$gte", 'end' : '$lte' }

            if k in lookup:
                lookup_v = lookup[k]
            else:
                lookup_v = {}

            lookup_v[map_dict[matches['side']]] = v
            v = lookup_v

        # IDs
        id_lookup = re.search('(?P<key>.+)_id$', k)
        if id_lookup:
            matches = id_lookup.groupdict()

            k = matches['key']
            v = bson.objectid.ObjectId(v)


        # Inside polygon.
        bounds = re.search('^(?P<key>.+)_bounds$', k)
        if bounds:
            if geo is True:
                prefix = 'geometry.'

            key = bounds.groups()[0]
            json_bounds = json.loads(v)
            lookup_type = '$box' if len(json_bounds) == 2 else '$polygon'

            k = key
            v = {'$within' : { lookup_type : json_bounds }}

        lookup['%s%s' % (prefix, k)] = v
    return lookup
