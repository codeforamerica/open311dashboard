function status_map() {
  emit({ status: this.status }, { count: 1});
}
