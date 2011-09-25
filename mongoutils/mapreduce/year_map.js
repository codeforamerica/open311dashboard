function year_map() {
  var rt = this.requested_datetime;
  emit({ year: rt.getFullYear() }, {count : 1});
}
