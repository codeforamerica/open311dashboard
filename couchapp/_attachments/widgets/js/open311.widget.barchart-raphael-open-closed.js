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
      self._render(data); //controlled by date control
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
      //console.log(daystring);
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
    //console.log(days);
            
    var CANVAS_HEIGHT = 200;
    var origin = 50;
    var barWidth = 10;
    var spacing = 1;

    var bottomLineLength = 22*(10) + 22 * 3; //28, 27
    var CANVAS_WIDTH = bottomLineLength + 50 + 200;

    // Check for Raphael
    if (typeof Raphael == 'undefined') {
      return;
    }
    
	var paper = Raphael(self.contentContainer[0], CANVAS_WIDTH, CANVAS_HEIGHT);
  	var barsTop = paper.set();
	var barsBottom = paper.set();
	
  	var bottomLine = paper.path("M0 70L" + bottomLineLength + " 70");
  	//bottomLine.toBack();
  	//https://github.com/DmitryBaranovskiy/raphael/blob/master/plugins/raphael.shadow.js
  	bottomLine.attr({fill:"grey", "stroke-width":"0"});

    var barTop, barBottom;
    var dayLen = dayOrder.length;
    for (var i = 0; i < dayLen; i++){
      var dayBar = days[dayOrder[i]];
      // Top bar
      barTop = paper.rect(origin+(barWidth+spacing)*i,70-(dayBar.open/10),barWidth,(dayBar.open/10));
      barTop.attr({cursor:"pointer", fill:"#1d8dc3", opacity:.9, href: "http://www.311dashboard.com/" + dayBar.open, stroke:"none"});		
      barsTop.push(barTop);
      // Bottom bar
      barBottom = paper.rect(origin+(barWidth+spacing)*i,70,barWidth,(dayBar.closed/10));
      barBottom.attr({cursor:"pointer", fill:"#ff0033", opacity:.9, href: "http://www.311dashboard.com/" + dayBar.closed, stroke:"none"});		
      barsBottom.push(barBottom);
    }
    
        var tooltip = paper.rect(10, 10, 110, 30); //draw as a path
	//M10 10L110 10L110 30L55 30L60 22L45 30L10 30
	//var tooltop = paper.path("M10 10L110 10L110 30L55 30L60 22L45 30L10 30L10 10");
	var tooltop = paper.path("M10 10L110 10L110 30L65 30L60 38L55 30L10 30L10 10");
	tooltop.attr({fill: "#DBDBDB", opacity: .8,stroke:"none"});
        var tooltip_text = paper.text(10,10,"hi"); //draw as a path
	tooltip.attr({fill: "#DBDBDB", opacity: .8,stroke:"none"});
	tooltip.hide();
        tooltip_text.hide();
	
	var graphWidth = (origin + dayLen*barWidth + (dayLen-1)*spacing);
	var index;
	
  	barsTop.mouseover(function () {
  		this.attr({fill:"white",stroke:"grey", opacity:.7, "stroke-width":1, "stroke-linecap":"square"});
		tooltip.show();
                tooltip_text.show();
		
		//Calculate index for bar text
		//graphWidth = (origin + dayLen*barWidth + (dayLen-1)*spacing); //Math.floor?? 357, 28 bars, 28 days
		//28 * 10 + (28 - 1)*1 + 50 = 357
		index = ((this.attr('x')/graphWidth) * graphWidth - origin)/(barWidth + spacing);
		console.log('index: ' + index);
		//alert(this.attr('y'));
		tooltip.attr({x: this.attr('x')-.5*tooltip.attr('width') + .5*barWidth,y: this.attr('y') - tooltip.attr('height') - 10});
                //tooltip_text.attr({text: this.attr('height') + ' Incidents\n ' + this.attr('x'), x: this.attr('x') + .5*barWidth, y:this.attr('y') - tooltip.attr('height') - 10 + 10});
		tooltip_text.attr({text: days[dayOrder[index]].open + ' Open Requests', x: this.attr('x') + .5*barWidth, y:this.attr('y') - tooltip.attr('height') + 5});
	});
	
	barsBottom.mouseover(function () {
  		this.attr({fill:"white",stroke:"grey", opacity:.7, "stroke-width":1, "stroke-linecap":"square"});
		tooltip.show();
		tooltip_text.show();
		
		//Calculate index
		index = ((this.attr('x')/graphWidth) * graphWidth - origin)/(barWidth + spacing);
		//alert(this.attr('y'));
		tooltip.attr({x: this.attr('x')-.5*tooltip.attr('width') + .5*barWidth,y: (this.attr('y')-20) + this.attr('height') + tooltip.attr('height') + 20 - 10});
                //tooltip_text.attr({text: this.attr('height') + ' Incidents\n ' + this.attr('x'), x: this.attr('x') + .5*barWidth, y: this.attr('y') + tooltip.attr('height') + 10 - 10});
		tooltip_text.attr({text: days[dayOrder[index]].closed + ' Closed Requests', x: this.attr('x') + .5*barWidth, y: (this.attr('y')-20) + this.attr('height') + tooltip.attr('height') +20 + 5});
	});
	
  	barsTop.mouseout(function() {
  		this.attr({fill:"#1d8dc3", stroke:"none", opacity:.9});
		tooltip.hide();
		tooltip_text.hide();
	});
	
	barsBottom.mouseout(function() {
		this.attr({fill:"#ff0033", stroke:"none", opacity:.9});
		tooltip.hide();
		tooltip_text.hide();
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
