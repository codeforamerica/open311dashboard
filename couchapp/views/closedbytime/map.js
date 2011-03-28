function(doc) { 
	if(doc.status == 'Closed') { 
		emit(doc.requested_datetime,doc);
	}
}