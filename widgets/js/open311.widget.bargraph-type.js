/**
 * Bar Graph by Type for Open311 Dashboard
 *
 * This provides a bar graph by open311 types.
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 */
(function( $, undefined ) {

$.widget("widget.bargraph-type", {
  /**
   * Default options for the widget.  We need some way
   * of communicating the data source across all widgets.
   */
  options: {
    dataSource: "open_requests_by_type.json"
  },
  
  /**
   * Creation code for widget
   */
  _create: function() {
    // Draw on DOM element?
    $.getJSON(this.options.dataSource, function(data) {
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

      var serviceCount = data.service_requests.length;
      var dataPar = [];
      var axis = [];
      var dataLabels = [];
      var maxValue = 0;
      
      for (var i = 0; i < serviceCount; i++) {
        var requestType = data.service_requests[i];
        dataPar.push((requestType.open_requests/data.total_request) * 100);
        axis.push(requestType.service_name);
        dataLabels.push("t+" + requestType.open_requests + ',676767,0,' + i + ',11')
        // find the largest value for the xmax caluclation
        maxValue = maxValue < requestType.open_requests ? requestType.open_requests : maxValue;
      }

      params.push("&chds=0,100&chxr=0,0,100");
      params.push("&chd=t:" + dataPar.join(','));
      var reverseAxis = axis.reverse();
      params.push("&chxl=0:|" + reverseAxis.join('|'));
      var reverseDataLabels = dataLabels.reverse();
      params.push("&chm=" + reverseDataLabels.join('|'));
      
      // &chm=t+Service+One,676767,0,4,11|t+Service+Two,676767,0,3,11|t+Service+Three,676767,0,2,11|t+Service+Four,676767,0,1,11|t+Service+Five,676767,0,0,11

      // Add image to widget
      this.element.append('<img src="' + params.join('') + '"></img>');
    })  
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