import datetime
import re

from pymongo import Connection
from pymongo.code import Code

from settings import SITE_ROOT, MONGODB
SCRIPT_BASE = "%s/mongoutils/mapreduce/" % SITE_ROOT

connection = Connection(MONGODB['host'])
db = connection[MONGODB['db']]

def count(keys=[], query={}):
    """
    Calculate the counts across multiple keys.
    """
    map_key = '{ '
    print "Hi"

    if len(keys) is 0:
        count = db.requests.find(query).count()
        return [{"_id": {}, 'value': {'count': count}}]

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

def pad_day_range(mapreduce, start_date, end_date):
    """
    Turn a date count into a list with a value per day/month/year
    """
    time_between = end_date - start_date
    days = time_between.days + 1

    data_list = [0 for i in range(1, days)]

    for day in mapreduce:
        date = datetime.datetime(int(day['_id']['requested_datetime_year']),
                int(day['_id']['requested_datetime_month'])+1,
                int(day['_id']['requested_datetime_day']))

        day_num = (date - start_date).days
        if day_num <= days and day_num > -1:
            data_list[day_num - 1] = day['value']['count']

    return data_list

def avg_response_time(query={}):
    """ Find how long the average response time is. """
    tmp_query = query.copy()

    if "status" not in tmp_query or tmp_query['status'] != "Closed":
        tmp_query['status'] = "Closed"

    return db.requests.inline_map_reduce(
            Code(open(SCRIPT_BASE + 'map_avg_response.js', 'r').read()),
            Code(open(SCRIPT_BASE + 'reduce_avg_response.js', 'r').read()),
            query=tmp_query,
            finalize=Code(open(SCRIPT_BASE + 'finalize_avg_response.js',
                'r').read()))
