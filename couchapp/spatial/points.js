function(doc) {
	if(doc.lon && doc.lat) {
    	emit({
        	type: "Point",
        	coordinates: [doc.lon, doc.lat]
    		}, 1);
	}
}