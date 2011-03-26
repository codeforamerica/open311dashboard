/**
 * Search widget for Open311 Dashboard
 * This is widget queries for Open311 data and
 * then publishes it to whoever is listening.
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 */
(function( $, undefined ) {

$.widget("Open311.searchType", {
  /**
   * Default options for the widget.  We need some way
   * of communicating the data source across all widgets.
   */
  options: {
    /* None */
  },
  
  //Create the widget
  _create: function() {
    var self = this, dates;
    
    $('<label for="open311-fromdate">From</label><input type="text" class="open311-fromdate" name="open311-fromdate"/>' +
      '<label for="open311-todate">to</label><input type="text" class="open311-todate" name="open311-todate"/>' +
      '<button class="open311-search-button">Search</button></div>')
      .appendTo(this.element);
        
    dates = $( '.open311-fromdate, .open311-todate', this.element ).datepicker({
			changeMonth: true,
			onSelect: function( selectedDate ) {
				var $this = $(this),
				    option = $this.hasClass('open311-fromdate') ? 'minDate' : 'maxDate',
					  instance = $this.data( 'datepicker' ),
					  date = $.datepicker.parseDate(
						  instance.settings.dateFormat ||
  						$.datepicker._defaults.dateFormat,
  						selectedDate, instance.settings );
				    
				    dates.not(this).datepicker('option', option, date );
			}
		});

    self._bindEvents();
  },
  
  //Bind any needed events
  _bindEvents: function() {
    //hack to keep access to the widget instance inside of the click callback
    var self = this;
    
    $('.open311-search-button', this.element).click(function(){
      var fromDate = $('.open311-fromdate', this.element).datepicker('getDate'), 
          toDate = $('.open311-todate', this.element).datepicker('getDate');
      self.search(fromDate, toDate);
    });
  },
  
  //Search for 311 requests by date range and publish them
  search: function(fromDate, toDate){
    var self = this,
      toRfc3339 = function(d){
  	 	  function pad(n){return n<10 ? '0'+n : n;};

    		return d.getUTCFullYear()+'-' + 
          pad(d.getUTCMonth()+1)+'-' + 
          pad(d.getUTCDate())+'T' + 
          pad(d.getUTCHours())+':' + 
          pad(d.getUTCMinutes())+':' + 
          pad(d.getUTCSeconds())+'Z';
    	};
    
    $.ajax({
      url: 'http://open311.couchone.com/service-requests/_design/requests/_list/requests-json/openbytime',
      dataType: 'jsonp',
      data: {
  			startkey:'"'+toRfc3339(fromDate)+'"',
  			endkey:'"'+toRfc3339(toDate)+'"'
  		},
	   	success: function(data) {
        $($.Open311).trigger('open311-data-update', [data]);
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