function(head, req) {
	var row;
	var service_requests = [];
	var json_obj = {};
	var total_requests = 0;
	
	start({
		"headers": {
		  "Content-Type": "text/plain"
		 }
	});
	send('{');
	while(row = getRow()) {
		total_requests += row.value;
		json_obj = { service_request_id:row.key[1],service_name:row.key[0],open_requests:row.value}
		service_requests.push(JSON.stringify(json_obj));		
	}
	send('"total_request":'+total_requests+',');
	send('"service_requests":['+service_requests+']');
	send('}');
}