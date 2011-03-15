function(doc) { 
	if(doc.status == 'Open') { 
		emit([doc.service_name.replace('_',' '),doc.service_code],1); 
	}
}