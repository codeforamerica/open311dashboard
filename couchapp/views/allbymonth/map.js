function(doc) { 
	if(doc.status) { 
    var date = doc.requested_datetime.split('-');
    var monthList = ['January','February','March','April','May','June','July','August','September','October','November','Decemeber'];
    var monthInt = (date[1])-1;
    var month = monthList[monthInt];
		emit(date[0] + ' ' + month,1);
	}
}
