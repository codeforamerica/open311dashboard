import datetime

def str_to_day(date):
    """Convert a YYYY-MM-DD string to a datetime object"""
    return datetime.datetime.strptime(date, '%Y-%m-%d')

def day_to_str(date):
    """Convert a datetime object into a YYYY-MM-DD string"""
    return datetime.datetime.strftime(date, '%Y-%m-%d')

def date_range(begin, end=None):
    """Returns a tuple of datetimes spanning the given range"""
    if end == None:
        date = str_to_day(begin)
        begin = datetime.datetime.combine(date, datetime.time.min)
        end = datetime.datetime.combine(date, datetime.time.max)
    else:
        begin = str_to_day(begin)
        end = str_to_day(end)

    return (begin, end)
