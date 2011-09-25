function day_map() {
  var rt = this.requested_datetime;
  emit({ year: rt.getFullYear(), month: rt.getMonth(),
       day: rt.getDate() }, {count : 1});
}
