function map_avg_response() {
  emit('response', {
    count: 1,
    response_time: this.updated_datetime - this.requested_datetime
  });
}
