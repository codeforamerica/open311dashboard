function(doc) { 
	if(doc.status) { 
		emit(doc.requested_datetime,doc);
	}
}