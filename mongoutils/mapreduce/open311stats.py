import re
from pymongo import Connection
from pymongo.code import Code

from settings import SITE_ROOT
SCRIPT_BASE = "%s/mongoutils/mapreduce/" % SITE_ROOT

connection = Connection('localhost')
db = connection['open311']

def mreduce(map_file, reduce_file, query, finalize=None):
    map = Code(map_file)
    reduce = Code(reduce_file)

    if finalize is not None:
        finalize = Code(finalize)

    return db.requests.inline_map_reduce(map, reduce,
            query=query, finalize=finalize)

def day_counts(query={}):
    return mreduce(open(SCRIPT_BASE + 'day_map.js', 'r').read(),
            open(SCRIPT_BASE + 'day_reduce.js', 'r').read(),
            query)

def month_counts(query={}):
    return mreduce(open(SCRIPT_BASE + 'month_map.js', 'r').read(),
            open(SCRIPT_BASE + 'day_reduce.js','r').read(),
            query)

def year_counts(query={}):
    return mreduce(open(SCRIPT_BASE + 'year_map.js', 'r').read(),
            open(SCRIPT_BASE + 'day_reduce.js', 'r').read(),
            query)

def status_counts(query={}):
    return mreduce(open(SCRIPT_BASE + 'status_map.js', 'r').read(),
            open(SCRIPT_BASE + 'day_reduce.js', 'r').read(),
            query)

def service_counts(query={}):
    return mreduce(open(SCRIPT_BASE + 'service_map.js', 'r').read(),
            open(SCRIPT_BASE + 'day_reduce.js', 'r').read(),
            query)

def avg_response_time(query={}):
    """ Find how long the average response time is. """

    if "status" not in query or query['status'] != "Closed":
        query['status'] = "Closed"

    return mreduce(open(SCRIPT_BASE + 'map_avg_response.js', 'r').read(),
            open(SCRIPT_BASE + 'reduce_avg_response.js', 'r').read(),
            query, open(SCRIPT_BASE + 'finalize_avg_response.js', 'r').read())
