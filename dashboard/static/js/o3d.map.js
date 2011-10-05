/**
 * o3d.map.js
 * @author Chris Barna <chris@unbrain.net>
 **/

// Map namespace.
o3d.map = {};

// Pad a bounding box for a map.
o3d.map.padBox = function (box, padding) {
  box[0].lat -= padding;
  box[0].lon -= padding;
  box[1].lat += padding;
  box[1].lon += padding;
  return box;
};

