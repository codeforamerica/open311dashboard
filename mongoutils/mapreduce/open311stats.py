from pymongo import Connection
from pymongo.code import Code

connection = Connection('localhost')
db = connection['open311']

def mreduce(map_file, reduce_file):
  map = Code(map_file)
  reduce = Code(reduce_file)
  return db.requests.inline_map_reduce(map, reduce)

def day_counts():
  return mreduce(open('day_map.js', 'r').read(), open('day_reduce.js', 'r').read())

def month_counts():
  return mreduce(open('month_map.js', 'r').read(), open('day_reduce.js','r').read())

def year_counts():
  return mreduce(open('year_map.js', 'r').read(), open('day_reduce.js', 'r').read())

def avg_response_time(start_time=null, end_time=null):
  map_str = """
      function(){
        var diff = new Date();
        if (this.updated_datetime != null && this.requested_datetime != null){
  """
  if start_time == null and end_time == null:
    map_str += """
          var u_date = new Date(this.updated_datetime);
          var r_date = new Date(this.requested_datetime);
          diff.setTime(r_date - u_date);
        }
      }
    """
