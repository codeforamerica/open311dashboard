/**
 * neighborhood_properties.js
 * @author Chris Barna <chris@unbrain.net>
 *
 * Fix up the metadata from SF's imported data.
 **/
var cursor = db.geometries.find()

while (cursor.hasNext()) {
  var doc = cursor.next();
  print(doc.properties.NBRHOOD);
  db.geometries.update({_id : doc._id}, {$set : { properties :
                     { name : doc.properties.NBRHOOD,
                       type : "neighborhood" } } }) //,
}

