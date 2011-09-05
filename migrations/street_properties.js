/**
 * street_properties.js
 * @author Chris Barna <chris@unbrain.net>
 * Normalize the properties of street centerlines
 **/

var cursor = db.geometries.find({"properties.type" : { $ne : "neighborhood" }})

while (cursor.hasNext()) {
  var doc = cursor.next();
  db.geometries.update({_id: doc._id}, { $set : { properties :
                       { name : doc.properties.STREETN_GC,
                         right_range : [ doc.properties.RT_FADD, doc.properties.RT_TOADD ],
                         left_range : [ doc.properties.LF_FADD, doc.properties.LF_TOADD ],
                         type : 'street'
                       } }});
}

