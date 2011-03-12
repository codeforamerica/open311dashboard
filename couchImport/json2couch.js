var fs = require('fs'),
    sys = require('sys'),
    http = require('http');

var fileName = process.argv[2];
var database = process.argv[3];

var dataFeed = fs.readFileSync(fileName, encoding='utf8');

var requestData = JSON.parse(dataFeed);

var local = http.createClient(80, 'open311.couchone.com');

var requestCount = requestData.requests.length;

sys.puts("Importing " + requestCount + " records into http://open311.couchone.com/" + database + " from " + fileName);

for (var i = 0; i < requestCount; i++) { 
	var request = local.request('POST', '/' + database + '/', {'host': 'open311.couchone.com','Content-Type':'application/json'});
	request.write(JSON.stringify(requestData.requests[i]), encoding='utf8');
	request.end();
}