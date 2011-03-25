function(doc) { 
	if(doc.status == 'Open') { 
		emit(doc.requested_datetime,doc);
	}
}