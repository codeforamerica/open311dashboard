function service_map() {
  emit({ service_name: this.service_name }, { count: 1 });
}
