function finalize_avg_response(key, values) {
  print(values);
  var avg = values.response_time / values.count;

  return { avg_time: avg };
}
