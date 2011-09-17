function reduce_avg_response(key, values) {
  var total_count = 0,
    total_time = 0;

  for (var i = 0; i < values.length; i += 1) {
    total_count += values[i].count;
    total_time += values[i].response_time;
  }

  return { count: total_count, response_time: total_time };
}
