// Time namespace
o3d.time = {};

o3d.time.nearest = function (value, number) {
  var remainder = value % number;
  if (remainder > 0) {
    value = value - remainder + number;
  }
  return value;
};

// Scale milliseconds into a human readable scale.
o3d.time.ms2human = function (milliseconds) {
  if (milliseconds < 86400000) {
    value = Math.round(milliseconds / 3600000);
    unit = "hour";
  } else if (milliseconds < 604800000) {
    value = o3d.time.nearest(milliseconds / 86400000, 0.5);
    unit = "day";
  } else if (milliseconds < 2592000000) {
    value = o3d.time.nearest(milliseconds / 604800000, 0.5);
    unit = "week";
  } else {
    value = o3d.time.nearest(milliseconds / 2592000000, 0.25);
    unit = "month";
  }

  if (value != 1) {
    unit += 's';
  }

  return value + ' ' + unit;
};

