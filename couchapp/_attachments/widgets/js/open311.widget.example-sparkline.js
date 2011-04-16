/*
 * Sparkline example
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 */
(function( $, undefined ) {

$.widget('Open311.sparklineExample', $.Open311.sparklineGoogle, {
  options: {
      title: 'Number of Sidewalk Cleanings Per Month',
      dataSource: "http://open311.couchone.com/service-requests/_design/requests/_view/allsidewalk_cleaningsbymonth?group=true"
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
	var month_map = {January:1,February:2,March:3,April:4,May:5,June:6,July:7,August:8,September:9,October:10,November:11,December:12};
	//this.updateContent('');

	if(data.rows.length > 0) {
	    //data.service_requests.length
	    var old_monthly_values = [1360,500,750,1330,750,1200,1200,1500,2100,1203,1310]; //Sample data through February of this year
	    var new_monthly_values = [];

	    //Adding our live data from March and April; it is sorted on the server.
	    for(var i = 0; i < data.rows.length; i++){
		//new_monthly_values.push({count: data.rows[i].value, position: month_map["January"]});
		new_monthly_values.push({count: data.rows[i].value, position: month_map[data.rows[i].key.substring(5,data.rows[i].key.length)]});
	    }
	    console.log(new_monthly_values[0].value)
	    new_monthly_values.sort(function(a,b){return a.position - b.position}); //.count?
	    for(i in new_monthly_values){console.log(new_monthly_values[i].count)};
	    var new_monthly_values_sorted = [];
	    for(i in new_monthly_values){new_monthly_values_sorted[i] = new_monthly_values[i].count};
	    //console.log(new_monthly_values_sorted)
	    var monthly_values = [];
	    monthly_values = monthly_values.concat(old_monthly_values,new_monthly_values_sorted);
	    var last_month_count = new_monthly_values_sorted[new_monthly_values_sorted.length-1];

	    self.updateContent('<img src="http://chart.apis.google.com/chart?cht=lc&chs=400x70&chds=0,2438&chd=t:' + monthly_values.join(',') + '&chco=336699&chls=1,1,0&chm=o,990000,0,13,4&chxt=r,x,y&chxs=0,990000,11,0,_|1,990000,1,0,_|2,990000,1,0,_&chxl=0:|' + last_month_count + '|1:||2:||&chxp=0,45.80"></img>');

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