import urllib2
import urllib
import datetime as dt
from dateutil import parser

ONE_DAY = dt.timedelta(days=1)

def get_data_from_endpoint(url_query, url_handler):
    """
    TBD
    """
    query_result_file = url_handler.urlopen(url_query)
    return query_result_file

def format_url_query(start, end, page, city):
    """
    Accept start, end datetimes, a paging indicator and a City model object
    format the passed in data to create a url suitable for calling 
    an open 311 endpoint 
    """

    # TODO:
    # classic version does data validation here
    # remember to add that back in when building the new command
    # function

    query_data = {
        'start_date' : start.isoformat() + 'Z',
        'end_date' : end.isoformat() + 'Z',
        'jurisdiction_id' : city.jurisdiction_id,
    }
    if page > 0:
        query_data['page'] = page

    query_str = urllib.urlencode(query_data)

    return city.url + '?' + query_str

def get_time_range(on_day=None):
    """
    Calculate a return a tuple of datetimes that are exactly 24
    hours apart, from midnight on the day passed in to the 
    midnight prior. If the passed in value is None, then use
    datetime.utcnow() by default.
    """

    # ensure that on_day is defaulted to the previous day
    if on_day is None:
        on_day = dt.datetime.utcnow() - ONE_DAY

    # End at the begining of on_day; start at the beginning of the previous
    # day relative to on_day.
    end = on_day.replace(hour=0, minute=0, second=0, microsecond=0)
    start = end - ONE_DAY

    # return tuple of start and end
    return (start, end)

def transform_date(date_string):
    """ 
    All Open311 date/time fields must be formatted in a common 
    subset of ISO 8601 as per the w3 note. Timezone information 
    (either Z meaning UTC, or an HH:MM offset from UTC) must be included.
    This method parses the Open311 date and transforms it into a simpler
    format and returns a string formatted as YYYY-MM-DD HH:MM.
    """

    new_date = parser.parse(date_string)
    return new_date.strftime("%Y-%m-%d %I:%M")


# TODO:
# Why is this test done every time? Why can't it be a unit test?
# If microsends are non-zero and tzinfo is not None the first time 
# then why would it ever change?
# The comments indicate that this is for the SF Open 311 API, is this
# really SF specific or should it be done for every endpoint
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


