/**
 * Comparison of open vs. closed requests for a given timespan for Open311 Dashboard
 *
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 */
(function( $, undefined ) {

$.widget('widget.barRaphaelOpenClosed', $.Open311.barRaphael, {
  /**
   * Default options for the widget.  We need some way
   * of communicating the data source across all widgets.
   */
  options: {
    title: 'Open vs Closed'
  },

  /**
   * Creation code for widget
   */
  _create: function() {
    // Create container to put chart in.
    this.updateContent('');
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
  this.updateContent('');
      
  if(data.service_requests.length > 0) {
    //var openReqs = closedReqs = [];
    var days = {};
    var dayOrder = [];
    // Loop through the returned data and count open vs closed
    for (var i = 0; i < data.service_requests.length; i++) {
      var elm = data.service_requests[i];
      var day = elm.requested_datetime.split(' ')[0].split('-');
      var daystring = day[0] + day[1] + day[2];
      console.log(daystring);
      if (days[daystring]) {
        if (elm.status == "Open") {
          days[daystring].open++;
        } else if (elm.status == "Closed") {
          days[daystring].closed++;
        }
      } else {
        days[daystring] = {open:0,closed:0};
        dayOrder.push(daystring);
      }
    }
    console.log(days);
            
    var CANVAS_HEIGHT = 200;
    var origin = 5;
    var barWidth = 10;
    var spacing = 1;

    var bottomLineLength = 22*(10) + 22 * 3; //28, 27
    var CANVAS_WIDTH = bottomLineLength + 50;

    // Check for Raphael
    if (typeof Raphael == 'undefined') {
      return;
    }
    
    var paper = Raphael(self.contentContainer[0], CANVAS_WIDTH, CANVAS_HEIGHT);
  	var bars = paper.set();
	var bars2 = paper.set();
	
  	var bottomLine = paper.path("M0 70L" + bottomLineLength + " 70");
  	//bottomLine.toBack();
  	//https://github.com/DmitryBaranovskiy/raphael/blob/master/plugins/raphael.shadow.js
  	bottomLine.attr({fill:"grey", "stroke-width":"1"});

    var bar1, bar2;
    var dayLen = dayOrder.length;
    for (var i = 0; i < dayLen; i++){
      var dayBar = days[dayOrder[i]];
      // Up bar
      bar1 = paper.rect(origin+(10+spacing)*i,70-(dayBar.open/10),barWidth,(dayBar.open/10));
      bar1.attr({cursor:"pointer", fill:"#1d8dc3", opacity:.9, title:dayBar.open + " open cases", href: "http://www.311dashboard.com/" + dayBar.open, stroke:"none"});		
      bars.push(bar1);
      // Down bar
      bar2 = paper.rect(origin+(10+spacing)*i,70,barWidth,(dayBar.closed/10));
  		bar2.attr({cursor:"pointer", fill:"#ff0033", opacity:.9, title:dayBar.closed + " closed cases", href: "http://www.311dashboard.com/" + dayBar.closed, stroke:"none"});		
      bars2.push(bar2);
    }
	
  	//Mouse Events for bars
  	bars.mouseover(function () {
  		this.attr({fill:"white",stroke:"grey"});
  	});
	
	bars2.mouseover(function () {
  		this.attr({fill:"white",stroke:"grey"});
  	});
	
  	bars.mouseout(function() {
  		this.attr({fill:"#1d8dc3", stroke:"none"});
  	});
	
	bars2.mouseout(function() {
		this.attr({fill:"#ff0033", stroke:"none"});
  	});
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
