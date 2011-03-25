/**
 * Top ten open service requests for a given timespan for Open311 Dashboard
 *
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 */
(function( $, undefined ) {

$.widget("widget.topOpenRequests", {
  /**
   * Default options for the widget.  We need some way
   * of communicating the data source across all widgets.
   */
  options: {
	startdate:"2010-11-11T00:00:00",
	enddate:"2010-11-15T00:00:00",
	topX:10,
    dataSource: "http://open311.couchone.com/service-requests/_design/requests/_list/requests-json/openbytime"
  },
  
  /**
   * Creation code for widget
   */
  _create: function() {
    var self = this;
    
    // Get the data
	$.ajax({
			url: this.options.dataSource,
		   	dataType: 'jsonp',
			data: {
				"startkey":'"'+this.options.startdate+'"',
				"endkey":'"'+this.options.enddate+'"'
			},	   	
		   	success: function(data) {
      			if(data.service_requests.length > 0) {
					// Parameters for the chart
     			 	var chart = {
				        title: "Open Requests by Type",
				        width: 400,
				        height: 200,
				        type: "bhs",
				        color: "4D89F9"
				    };
      
				      // Create google chart data
				    var params = ['http://chart.apis.google.com/chart'];
				    params.push("?chxs=0,676767,11.5,0,l,FFFFFF|1,FFFFFF,11.5,0,_,FFFFFF");
				    params.push("&chxt=y,x&chbh=a");
				    params.push("&chs=" + chart.width + "x" + chart.height);
				    params.push("&cht=" + chart.type);
				    params.push("&chco=" + chart.color);

				    var dataPar = [];
				    var axis = [];
				    var dataLabels = [];
			      	var maxValue = 0;
			      	var serviceCount = 0;
					var request_types = [];
					
					  // Loop through the returned data and determine the frequency of each service type
					$(data.service_requests).each(function(index, elm) {
						if(request_types[elm.service_code] == undefined) {
							x = { 'service_name':elm.service_name, 'count':1}
							request_types[elm.service_code] = x;
						} else {
							request_types[elm.service_code].count++;
						}
						serviceCount++;
					});

					// Determine the top ten frequencies
					var topTen = [];
					$(request_types).each(function(index, el) {
				      	if(el != undefined) { topTen.push(el); }
					});

					topTen.sort(function(a,b) {
						if (a.count > b.count) return -1;
						if (a.count < b.count) return 1;
						return 0;
					});

					topTen = topTen.slice(0,10);
      
					// Now that we have our top 10, we can stack the data points onto our Google Chart url
				    $(topTen).each(function(index, el) {
			      		if(el != undefined) {
							var requestType = el;
					        dataPar.push((requestType.count/serviceCount)*100);
					        axis.push(requestType.service_name);
					        dataLabels.push("t+" + requestType.count + ',676767,0,' + index + ',11')
					        // find the largest value for the xmax caluclation
					        maxValue = maxValue < requestType.count ? requestType.count : maxValue;
						}
			      	});

				    params.push("&chds=0,100&chxr=0,0,100");
				    params.push("&chd=t:" + dataPar.join(','));
				    var reverseAxis = axis.reverse();
				    params.push("&chxl=0:|" + reverseAxis.join('|'));
				    var reverseDataLabels = dataLabels.reverse();
				    params.push("&chm=" + reverseDataLabels.join('|'));
      
				    // Add image to widget
				    self.valueDiv = $('<img src="' + params.join('') + '"></img>')
						.appendTo(self.element);
				} else {
					self.valueDiv = $('<div class="no-data">No data, sucka.</div>')
						.appendTo(self.element);
				}
    		}  
  	});
  },
  
  /**
   * Destroy widget
   */
  destroy: function() {
     $.Widget.prototype.destroy.apply(this, arguments); // default destroy
      // now do other stuff particular to this widget
  }
});

})( jQuery );