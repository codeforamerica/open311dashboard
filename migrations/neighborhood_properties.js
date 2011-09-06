/**
 * neighborhood_properties.js
 * @author Chris Barna <chris@unbrain.net>
 *
 * Fix up the metadata from SF's imported data.
 **/

var slugify = function (str) {
    return str.toLowerCase().replace(/ /g, '-')
        .replace(/\./g, '').replace(/\//g, '').replace(/--/g, '-');
  };
var cursor = db.polygons.find();

while (cursor.hasNext()) {
  var doc = cursor.next();
  print(doc.properties.NBRHOOD);
  db.polygons.update({_id : doc._id}, {$set : { properties :
                     { name : doc.properties.NBRHOOD,
                       type : "neighborhood",
                       slug : slugify(doc.properties.NBRHOOD) } } });
}

db.polygons.ensureIndex({ 'geometry.coordinates.0' : '2d' });
db.polygons.ensureIndex({ 'properties.slug' : 1 });
