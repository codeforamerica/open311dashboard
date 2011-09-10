from pymongo import Connection
from pymongo.code import Code

connection = Connection('localhost')
db = connection['open311']

def mreduce(map_file, reduce_file):
  map = Code(open(map_file, 'r').read())
  reduce = Code(open(reduce_file, 'r').read())
  return db.requests.inline_map_reduce(map, reduce)

def day_counts():
  return mreduce('day_map.js', 'day_reduce.js')

def month_counts():
  return mreduce('month_map.js', 'day_reduce.js')

def year_counts():
  return mreduce('year_map.js', 'day_reduce.js')

