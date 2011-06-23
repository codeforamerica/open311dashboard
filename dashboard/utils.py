import datetime

def str_to_day(date):
    """Convert a YYYY-MM-DD string to a datetime object"""
    return datetime.datetime.strptime(date, '%Y-%m-%d')

def day_to_str(date):
    return datetime.datetime.strftime(date, '%Y-%m-%d')
