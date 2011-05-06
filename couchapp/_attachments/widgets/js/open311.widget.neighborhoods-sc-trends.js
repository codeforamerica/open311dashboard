/*
 * Sparkline example
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 */
(function( $, undefined ) {
//refactor this code for new event handling
$.widget('Open311.neighborhoodsSCTrends', $.Open311.neighborhoodsTrends, {
  options: {
      title: 'Sidewalk Cleaning Trends in SF Neighborhoods',
      dataSource: "http://open311.couchone.com/service-requests-neighborhoods/_design/requests/_view/allsidewalk_cleaningsbyneighborhood?group=true"
	},

	_create: function() {
	    var self = this;
	    self._bindEvents();
	    //Create Container to put chart in.
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

    _render: function(data){
	    var self = this;
	//this.updateContent('');
  console.log("DATA ROWS LENGTH " + data.rows.length);

	if(data.rows.length > 0) {
    
      var neighborhood_counts = [];

	    for(var i = 0; i < data.rows.length; i++){
        neighborhood_counts.push({key: data.rows[i].key, value: data.rows[i].value}); 
	    }

      neighborhood_counts = neighborhood_counts.map(function(elem) { 
        elem.key = elem.key.replace(/\s/g, "%20");
        return elem;
      });

      // Sorts in reverse order by count value. 
      neighborhood_counts.sort(function(a, b){ return b.value - a.value });
      
      //Take the top ten counts.
      neighborhood_counts = neighborhood_counts.slice(0,10); 

      var data_points = [];
      var labels = [];
      var data_bars = [];

      for (var i = 0; i < neighborhood_counts.length; i++) {
        var elem = neighborhood_counts[i];
        data_points.push(elem.value);

        labels.push(elem.key);
        data_bars.push("t+" + elem.value + ',676767,0,' + i + ',11');

        //console.log("(" + elem.key + "," + elem.value + ")");
      }

      var img_query_string = '<img src=' + '\"' + 'http://chart.apis.google.com/chart?chxs=0,676767,11.5,0,l,FFFFFF|1,FFFFFF,11.5,0,_,FFFFFF&cht=bhs&chxt=y,x&chbh=a&chs=290x200&chco=1d8dc3&chds=0,400&chxr=0,0,400&chd=t:' + data_points.join(',') + '&chxl=0:|' + labels.reverse().join('|') + '&chm=' + data_bars.reverse().join('|') + '\"></img>';

      //console.log(img_query_string);

      self.updateContent(img_query_string);



	} else {
	    self.valueDiv = $('<div class="no-data">No data.</div>')
	    .appendTo(self.contentContainer);
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
