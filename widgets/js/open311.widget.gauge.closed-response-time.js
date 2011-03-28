/**
 * Example widget for Open311 Dashboard
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 */
 
 
(function( $, undefined ) {

$.widget('Open311.gaugeGoogleActualEstResponseTime', $.Open311.gaugeGoogle, {
  /**
   * Default options for the widget.  We need some way
   * of communicating the data source across all widgets.
   */
  options: {
	  dataSource: "ClosedServiceRequests_By_SingleServiceType_Slice.json"
  },
  
  /**
   * Creation code for widget
   */
  _create: function() {
	var self = this;
	self._bindEvents();
	  self._render();
},

 _bindEvents: function(){
     var self = this;
    
    $($.Open311).bind('open311-data-update', function(event, data){
   //   self._render(data);
    });
  },
  
   _loadData: function() {
    jQuery.getJSON('data/ServiceRequests_Complete.json', this._render(dataSource));
  },
  
   _render: function(data) {
  var dog = 0;   
   $.getJSON('data/ClosedServiceRequests_By_SingleServiceType_Slice.json', function(data) {
  var items = [];
  var count =0;
  var totaltime = 0.0;
  var expectedtime = 0.0;
  var closuretime = 0;
  expectedtime =  data.requests[1].updated_datetime - data.requests[1].expected_datetime;
  console.log("expected: " + expectedtime);
  $.each(data.requests, function(key, val) {
		if (val.status == "Closed"){
			count++;
			//closuretime = val.updated_datetime.getTime() - val.requested_datetime.getTime());
		}//end if
		
		});

});

 

    var self = this;
   
   //var numRequests = data.requests.length();
//   console.log(numRequests);
   var chart = {
     width: 200,
     height: 125,
     serviceType: 'Street Cleaning',
    serviceUnits: ' days',
    serviceEst: 3,
    serviceActual: 5,
    lowColor: 'D2E9F3',
    highColor: '1d8dc3'
    };
    
    var params = ['http://chart.apis.google.com/chart'];
    
    params.push('?chs=' + chart.width + 'x' + chart.height);
    params.push('&cht=gom&chd=t:' + chart.serviceEst + '|' + chart.serviceActual);
    params.push('&chls=3|2,8,8|10|0&chco=' + chart.lowColor + ',' + chart.highColor);
    params.push('&chxt=x&chx|0:|Actual|Estimated');
    
    
    $(self.element).empty();
    
     self.valueDiv = $('<img src="' + params.join('') + '"></img>')
				  .appendTo(self.element);

	//self.valueDiv = $('<img src="https://chart.googleapis.com/chart?chs=200x125&amp;cht=gom&amp;chd=t:70|50&chls=3|2,8,8|10|0&amp;chco=D2E9F3,1d8dc3&amp;chxt=x&amp;chxl=0:|Actual|Estimated"></img>')

   	//.appendTo( self.element );
    // can use this.options
  },
  
  _destroy: function(){ 
  	$.Widget.prototype.destroy.apply(this, arguments); // default destroy
      // now do other stuff particular to this widget
	}
});


})( jQuery );