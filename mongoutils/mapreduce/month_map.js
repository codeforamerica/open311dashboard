function month_map() {
  var rt = this.requested_datetime;
  emit({ year: rt.getFullYear(), month: rt.getMonth() }, {count : 1});
}
