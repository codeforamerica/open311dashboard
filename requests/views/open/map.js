function(doc) { 
	if (doc.status == 'Open') {  
		emit(null, doc) 
	}
}