/**
 * request_dates.js
 * @author Chris Barna <chris@unbrain.net>
 *
 * Change imported strings to Date() format.
 **/

var cursor = db.requests.find()

while (cursor.hasNext()) {
  var doc = cursor.next();
  db.requests.update({_id : doc._id},
                     {$set :
                       { requested_datetime : ISODate(doc.requested_datetime),
                         updated_datetime : ISODate(doc.updated_datetime),
                         expected_datetime : ISODate(doc.expected_datetime)
                    }});
}
