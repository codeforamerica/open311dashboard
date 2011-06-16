from django.core.management.base import BaseCommand, CommandError
from open311dashboard.dashboard.models import Request

import httplib
import urllib2
import urllib
import datetime as dt
import xml.dom.minidom as dom

ONE_DAY = dt.timedelta(days=1)

def get_time_range(on_day=None):
    if on_day is None:
        on_day = dt.datetime.utcnow() - ONE_DAY

    # End at the begining of on_day; start at the beginning of the previous
    # day.
    end = on_day.replace(hour=0, minute=0, second=0, microsecond=0)
    start = end - ONE_DAY

    return (start, end)

def validate_dt_value(datetime):
    """
    Verify that the given datetime will not cause problems for the Open311 API.
    For the San Francisco Open311 API, start and end dates are ISO8601 strings,
    but they are expected to be a specific subset.
    """
    if datetime.microsecond != 0:
        raise ValueError('Microseconds on datetime must be 0: %s' % datetime)

    if datetime.tzinfo is not None:
        raise ValueError('Tzinfo on datetime must be None: %s' % datetime)

def get_requests_from_SF(start,end):
    """
    Retrieve the requests from the San Francisco 311 API within the time range
    specified by the dates start and end.

    Returns a stream containing the content from the API call.
    """

    validate_dt_value(start)
    validate_dt_value(end)

    #url = r'https://open311.sfgov.org/dev/Open311/v2/requests.xml' #dev
    url = r'https://open311.sfgov.org/Open311/v2/requests.xml'
    query_data = {
        'start_date' : start.isoformat() + 'Z',
        'end_date' : end.isoformat() + 'Z',
        'jurisdiction_id' : 'sfgov.org'
    }
    query_str = urllib.urlencode(query_data)

    requests_stream = urllib2.urlopen(url + '?' + query_str)
    return requests_stream

def parse_requests_doc(stream):
    """
    Converts the given file-like object, which presumably contains a service
    requests document, into a list of request dictionaries.
    """

    import xml.dom

    xml_string = stream.read()

    columns = [] #holding columns for a day's worth of incident data
    values = [] #holding values for a day's worth of incident data

    try:
        requests_root = dom.parseString(xml_string).documentElement
    except ExpatError:
        print(xml_string)
        raise

    for request_node in requests_root.childNodes:
        indiv_columns_list = []
        indiv_values_list = []

        if request_node.nodeType != xml.dom.Node.ELEMENT_NODE:
            continue

        if request_node.tagName != 'request':
            raise Exception('Unexpected node: %s' % requests_root.toprettyxml())

        for request_attr in request_node.childNodes:
            if request_attr.childNodes:
                indiv_columns_list.append(request_attr.tagName)
                indiv_values_list.append(request_attr.childNodes[0].data)

        columns.append(indiv_columns_list)
        values.append(indiv_values_list)
    return (columns,values)

def insert_data(requests):
    columns,values = requests

    for i in range(len(values)):

        # Put the key-value pairs into a dictionary and then an arguments list.
        request_dict = dict(zip(columns[i], values[i]))
        together = request_dict

        r = Request(**together)

        try:
            r.save()
            print "Successfully saved %s" % r.service_request_id
        except Request.ValidationError:
            raise CommandError('Request "%s" does not validate correctly' %
                    r.service_request_id)

# At runtime...
class Command(BaseCommand):

    def handle(self, *args, **options):
        if len(args) >= 2:
            start, end = get_time_range(dt.datetime.strptime(sys.argv[1], '%Y-%m-%d'))
        else:
            start, end = get_time_range()

        if len(args) >= 3:
            num_days = int(sys.argv[2])
        else:
            num_days = 1

        for _ in xrange(num_days):
            requests_stream = get_requests_from_SF(start, end)
            requests = parse_requests_doc(requests_stream) #returns tuple of columns and values
            insert_data(requests)

            start -= ONE_DAY
            end -= ONE_DAY

            print start
            print requests[1]


