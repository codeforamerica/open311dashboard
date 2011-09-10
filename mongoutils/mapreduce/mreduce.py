from pymongo import Connection
from pymongo.code import Code

connection = Connection('localhost')
db = connection['open311']

map = Code(open('day_map.js', 'r').read())
reduce = Code(open('day_reduce.js', 'r').read())

results = db.requests.inline_map_reduce(map, reduce)

for r in results:
  print r
