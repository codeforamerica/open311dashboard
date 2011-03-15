function(doc) { 
	if (doc.status == 'Closed') {  
		emit(null, doc) 
	}
}