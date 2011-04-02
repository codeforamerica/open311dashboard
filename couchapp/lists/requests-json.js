function(head, req) {
	var row;
	var is_first = true;
	
	// Start by sending the content-type header (should probably be changed to application.json
	start({
		"headers": {
		  "Content-Type": "text/plain"
		 }
	});
	
	send(req.query.callback+'(');
	
	// Begin formatting the requests
	send("{\n"+'"service_requests":[');
	
	// I use the following method to make sure their is no trailing comma in the array of service requests.
	// I'm open to another method - as long as it doesn't involve putting all of the rows into an array
	while(row = getRow()) {
		if(is_first) send(JSON.stringify(row.value,null,"\n\t\t"));
		else send(','+JSON.stringify(row.value,null,"\n\t\t"));	
		is_first = false;
	}
	
	// Close it all up
	send("]});");
}