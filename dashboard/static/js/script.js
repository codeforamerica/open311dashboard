/* Authors: @ctbarna, @evansml */
/* Helper methods for the open311dashboard */

// Define a global namespace.
Open311Dashboard = {};

// Map namespace.
Open311Dashboard.map = {};

// Pad a bounding box for a map.
Open311Dashboard.map.padBox = function (box, padding) {
  box[0].lat -= padding;
  box[0].lon -= padding;
  box[1].lat += padding;
  box[1].lon += padding;
  return box;
};

// API Namespace.
Open311Dashboard.API = {};
