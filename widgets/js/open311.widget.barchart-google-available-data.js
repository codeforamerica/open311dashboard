/**
 * Top ten open service requests for a given timespan for Open311 Dashboard
 *
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 */
(function( $, undefined ) {

$.widget('Open311.barchartGoogleAvailableData', $.Open311.barchartGoogle, {
  /**
   * Default options for the widget.  We need some way
   * of communicating the data source across all widgets.
   */
  options: {
    title: 'Open311 Data Available',
	  dataSource: "http://open311.couchone.com/service-requests/_design/requests/_view/allbymonth?group=true"
 },
     /**
   * Creation code for widget
   */
  _create: function() {
    var self = this;
    self._bindEvents();
        // Create container to put chart in.
    this.updateContent('');
    
    // Get the data
    $.ajax({
			url: self.options.dataSource,
			dataType: 'jsonp',
			success: function(data) {
					self._render(data);					
				} 
  	});

  },
  
  _bindEvents: function(){
    var self = this;
  },
  
  _render: function(data) {
    var self = this;
    
		if(data.rows.length > 0) {
			  // Parameters for the chart
 			 	var chart = {
		        title: "Available Data",
		        width: 500,
		        height: 100,
		        type: "bvg",
		        color: "4D89F9"
		    };
  
        /*
http://chart.apis.google.com/chart
   ?chxl=1:|November|March
   &chxr=0,0,1100|1,5,100
   &chxs=1,676767,11.5,0,_,676767
   &chxt=y,x
   &chbh=a
   &chs=300x225
   &cht=bvg
   &chco=A2C180
   &chds=0,1016.667
   &chd=t:1000,385
   &chma=|0,2
      */

	      // Create google chart data
		    var params = ['http://chart.apis.google.com/chart'];
		    params.push("?chxs=1,676767,11.5,0,_,676767");
		    params.push("&chxt=x,y&chbh=a");
		    params.push("&chs=" + chart.width + "x" + chart.height);
		    params.push("&cht=" + chart.type);
		    params.push("&chco=" + chart.color);

		    var dataPar = [],
		      axis = [],
		      dataLabels = [],
	      	maxValue = 0;

        for (var i = 0; i < data.rows.length; i++) {
          axis.push(data.rows[i].key);
          dataPar.push(data.rows[i].value);
          if (data.rows[i].value > maxValue) {
            maxValue = data.rows[i].value;
          }
        }
			
		    params.push("&chds=0," + maxValue + "&chxr=0,0,0|1,0," + maxValue);
		    params.push("&chd=t:" + dataPar.join(','));
		    
		    params.push("&chxl=0:|" + axis.join('|'));
		    
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

