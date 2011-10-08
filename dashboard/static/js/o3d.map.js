/**
 * o3d.map.js
 * @author Chris Barna <chris@unbrain.net>
 **/

// Map namespace.
o3d.map = {};

// Pad a bounding box for a map.
o3d.map.padBox = function (box, padding) {
  var min_i = 0;
  var min_lat = 1000;

  for (var i = 0; i < box.length; i += 1) {
    if (box[i].lat < min_lat) {
      min_lat = box[i].lat;
      min_i = i;
    }
  }

  box[min_i].lat -= padding;
  box[min_i].lon -= padding;
  box[min_i ^ 1].lat += padding;
  box[min_i ^ 1].lon += padding;
  return box;
};

