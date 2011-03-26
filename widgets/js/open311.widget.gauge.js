/**
 * Example widget for Open311 Dashboard
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 */
(function( $, undefined ) {

$.widget("Open311.gauge", {
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
	this.element
		.addClass("ui-widget")
		.attr({
			role: "gauge",
		})
 _bindEvents: function(){
     var self = this;
    
    $($.Open311).bind('open311-data-update', function(event, data){
      self._render(data);
    });
  },
  
   $.getJSON(this.options.dataSource, function(data) {
        var requestCount = data.requests.length;
       
       console.log(requestCount);
        
        
        
})//close getJson
	this.valueDiv = $("<img src='https://chart.googleapis.com/chart?chs=200x125&amp;cht=gom&amp;chd=t:70|50&chls=3|2,8,8|10|0&amp;chco=FFFFFF,1d8dc3&amp;chxt=x&amp;chxl=0:|Actual|Estimated'></img>")

   	.appendTo( this.element );
    // can use this.options
  },
  
  _destroy: function(){ 
  	this.element
			.removeClass( "ui-widget" )
			.removeAttr( "role" );

		this.valueDiv.remove();
	}
});

$.extend( $.ui.progressbar, {
	version: "@VERSION"
});

})( jQuery );