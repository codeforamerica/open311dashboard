/**
 * Comparison of open vs. closed requests for a given timespan for Open311 Dashboard
 *
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 */
(function( $, undefined ) {

$.widget('widget.pieRaphaelOpenClosed', $.Open311.pieRaphael, {
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
    var openReqs = closedReqs = 0;
    
      // Loop through the returned data and count open vs closed
    $(data.service_requests).each(function(index, elm) {
      if (elm.status == "Open") {
        openReqs++;
      } else if (elm.status == 'Closed'){ 
        closedReqs++;
      }
    });
            
    var origin = 5;
    var barWidth = 10;
    var spacing = 2;

    var bottomLineLength = 28*(10) + 27 * 3;
    var CANVAS_WIDTH = bottomLineLength + 50;

    var sampleArray = [.5,.5,1,1,2,2,2,3,3,3,4,5,6,7,6,5,5,4,4,3,3,3,2,2,2,1,1,1,.5,.5];

    var colorArray = [];
            
      // Check for Raphael
    if (typeof Raphael == 'undefined') {
      return;
    }

  	var bars = paper.set();
	
  	var bottomLine = paper.path("M0 70L" + bottomLineLength + " 70");
  	//bottomLine.toBack();
  	//https://github.com/DmitryBaranovskiy/raphael/blob/master/plugins/raphael.shadow.js
  	bottomLine.attr({fill:"black", "stroke-width":"2"});

    // Up bars
    var openReqLen = openReqs.length;
    for (var i=0; i < openReqLen; i++){
      var bar = paper.rect(origin+(10+spacing)*i,70-10*sampleArray[i],barWidth,10*sampleArray[i]);
  		bar.attr({cursor:"pointer", fill:"#0000ff", title:"Intensity: " + sampleArray[i], opacity:"1",stroke:"none"});		
      bars.push(bar);
    }

    // Down bars
    var closedReqLen = closedReqs.length;
    for (var i = 0; i < closedReqLen; i++) {
      var bar = paper.rect(origin+(10+spacing)*i,70,barWidth,10*sampleArray[i]);
  		bar.attr({cursor:"pointer", fill:"#ff0000", title:"Intensity: " + sampleArray[i], opacity:"1",stroke:"none"});		
      bars.push(bar);
    }
	
  	//Mouse Events for bars
  	bars.mouseover(function () {
  		this.attr({fill:"white",stroke:"grey"});
  	});
	
  	bars.mouseout(function() {
  		this.attr({fill:"#DBDBDB",stroke:"none"});
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
