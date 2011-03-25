function(doc) {
	if (doc.status == "Open") {
    	emit({
        	type: "Point",
        	coordinates: [doc.lon, doc.lat]
    		}, 1);
	}
}