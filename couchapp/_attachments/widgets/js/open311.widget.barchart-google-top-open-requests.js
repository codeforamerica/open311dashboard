/**
 * Top ten open service requests for a given timespan for Open311 Dashboard -- these are ALL (open and closed) requests now
 *
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 */
 
(function( $, undefined ) {

$.widget('Open311.barchartGoogleTopOpenRequests', $.Open311.barchartGoogle, {
  /**
   * Default options for the widget.  We need some way
   * of communicating the data source across all widgets.
   */
  options: {
    title: 'Top Ten Frequency',
	  topX: 10
	},
  
  /**
   * Creation code for widget
   */
  _create: function() {
    var self = this;
    
    self._bindEvents();
  },
  
  _bindEvents: function(){
    var self = this;
    
    $($.Open311).bind('open311-data-update', function(event, data){
      self._render(data);
    });
  },
  
  _render: function(data) {
    var self = this;
    
		if(data.service_requests.length > 0) {
		    // Parameters for the chart
 		    var chart = {
		        title: "Open Requests by Type",
		        width: 290,
		        height: 200,
		        type: "bhs",
		        color: "1d8dc3"
		    };
  
		    // Create google chart data
		    var params = ['http://chart.apis.google.com/chart'];
		    params.push("?chxs=0,676767,11.5,0,l,FFFFFF|1,FFFFFF,11.5,0,_,FFFFFF");
		    params.push("&chxt=y,x&chbh=a");
		    params.push("&chs=" + chart.width + "x" + chart.height);
		    params.push("&cht=" + chart.type);
		    params.push("&chco=" + chart.color);

		    var dataPar = [],
		        axis = [],
		        dataLabels = [],
			maxValue = 0,
			totalServiceCount = 0,
			request_types = [];
			
			totalServiceCount = data.service_requests.length; //do a null test? This should be done on the server anyway.
		      
			var service_list = [];
				
			service_list[0] = data.service_requests[0].service_name;
			for (var i = 0; i < data.service_requests.length; i++){
				//do a null test for totalServiceCount here?
				if(service_list.indexOf(data.service_requests[i].service_name) == -1){
					service_list.push(data.service_requests[i].service_name);
				}
			}
			
			console.log(service_list); //Create a master list of service requests.
			
			var service_counts = [],
			    count = 0;

			 //TODO: Compare against an array of service request names in the master list.
			for(var j = 0; j < service_list.length; j++){ //switch up this loop
					for (i = 0; i < data.service_requests.length; i++){
						if (service_list[j] == data.service_requests[i].service_name){
							count++;
						}
					}
					service_counts[j] = {"service_name": service_list[j], "count": count};
					count = 0; //reset count
			}
			
			//console.log(service_counts[5].service_name + ' ' + service_counts[5].count);
			
			var topTen = service_counts.sort(function(a,b){ //pass in an anonymous function
				return b.count - a.count; //defines increasing order in the reverse: high to low
			});

  			topTen = topTen.slice(0,10);
  
			// Now that we have our top 10, we can stack the data points onto our Google Chart url
		    $(topTen).each(function(index, el) {
	      		if(el) {
					    var requestType = el; //why is this declared here?
			        dataPar.push((requestType.count/totalServiceCount)*100);
			        axis.push(requestType.service_name);
			        dataLabels.push("t+" + requestType.count + ',676767,0,' + index + ',11');
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
		    self.updateContent('<img src="' + params.join('') + '"></img>');
	    } else {
		    self.updateContent('No data found');
		  }
  },
  
  /**
   * Destroy widget
   */
  destroy: function() {
    // Default destroy
    $.Widget.prototype.destroy.apply(this, arguments);
  }
});

})( jQuery );