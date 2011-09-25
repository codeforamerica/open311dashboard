import re

from pymongo import Connection
from pymongo.code import Code

from settings import SITE_ROOT
SCRIPT_BASE = "%s/mongoutils/mapreduce/" % SITE_ROOT

connection = Connection('localhost')
db = connection['open311']

def count(keys, query={}):
    """
    Calculate the counts across multiple keys.
    """
    map_key = '{ '

    for key in keys:
        if re.search('_year$', key):
            key = re.sub('_year$', '', key)
            map_key += "%s_year: this.%s.getFullYear(), " % (key, key)
        elif re.search('_month$', key):
            key = re.sub('_month$', '', key)
            map_key += "%s_year: this.%s.getFullYear(), " % (key, key)
            map_key += "%s_month: this.%s.getMonth(), " % (key, key)
        elif re.search('_day$', key):
            key = re.sub('_day$', '', key)
            map_key += "%s_year: this.%s.getFullYear(), " % (key, key)
            map_key += "%s_month: this.%s.getMonth(), " % (key, key)
            map_key += "%s_day: this.%s.getDate(), " % (key, key)
        elif re.search('_hour$', key):
            key = re.sub('_hour$', '', key)
            map_key += "%s_hour: this.%s.getHours(), " % (key, key)
        else:
            map_key += "%s: this.%s, " % (key, key)

    map_key += " }"

    map_function = Code("""function() {
        emit(%s, {count: 1});
    }""" % map_key)

    reduce_function = Code("""function day_reduce(key, values){
        var total = 0;
        for (var i=0; i< values.length; i++){
            total += values[i].count;
        }
        return {count: total};
    }""")

    return db.requests.inline_map_reduce(map_function, reduce_function,
            query=query)

def calculate_delta(date_range):
    """
    Calculate the from a date range to the same number of days previous.
    """

def avg_response_time(query={}):
    """ Find how long the average response time is. """
    tmp_query = query.copy()

    if "status" not in tmp_query or tmp_query['status'] != "Closed":
        tmp_query['status'] = "Closed"

    return db.requests.inline_map_reduce(
            Code(open(SCRIPT_BASE + 'map_avg_response.js', 'r').read()),
            Code(open(SCRIPT_BASE + 'reduce_avg_response.js', 'r').read()),
            query=query,
            finalize=Code(open(SCRIPT_BASE + 'finalize_avg_response.js',
                'r').read()))
