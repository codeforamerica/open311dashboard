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
	send("{\n");
	while(row = getRow()) {
		total_requests += row.value;
		json_obj = { service_request_id:row.key[1],service_name:row.key[0],open_requests:row.value}
		service_requests.push("\n\t\t"+JSON.stringify(json_obj,null,"\t\t\t"));		
	}
	send("\t'total_request':"+total_requests+",\n");
	send("\t'service_requests':["+service_requests+"]\n");
	send("}");
	
	send(head.toString());
}