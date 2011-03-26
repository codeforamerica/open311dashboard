/**
 * Comparison of open vs. closed requests for a given timespan for Open311 Dashboard
 *
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 */
(function( $, undefined ) {

$.widget("widget.openVsClosed", {
  /**
   * Default options for the widget.  We need some way
   * of communicating the data source across all widgets.
   */
  options: {
	startdate:"2010-11-11T00:00:00",
	enddate:"2010-11-15T00:00:00",
	topX:10,
    dataSource: "http://open311.couchone.com/service-requests/_design/requests/_list/requests-json/allbytime"
  },
  
  /**
   * Creation code for widget
   */
  _create: function() {
    var self = this;
    
    // Get the data
	$.ajax({
			url: this.options.dataSource,
		   	dataType: 'jsonp',
			data: {
				"startkey":'"'+this.options.startdate+'"',
				"endkey":'"'+this.options.enddate+'"'
			},	   	
		   	success: function(data) {
      			if(data.service_requests.length > 0) {
					var openReqs = closedReqs = 0;
					
					  // Loop through the returned data and count open vs closed
					$(data.service_requests).each(function(index, elm) {
						if(elm.status == "Open") openReqs++
						else if(elm.status == 'Closed') closedReqs++;
					});
					
					console.log(openReqs);
					console.log(closedReqs);
					
					totReqs = openReqs+closedReqs;
					
					pieces =  [
				      {status: "Open", fraction:(openReqs/totReqs)}, 
				      {status: "Closed", fraction:(closedReqs/totReqs)}
				    ];
					
				    colorArray: []
					
					// Check for Raphael
				    if (typeof Raphael == 'undefined') {
				      return;
				    }

				    // Deal with colors
				    if (pieces.length === 2) {
				      colorArray = ["#D2E9F3", "#1d8dc3"];
				    } else if (pieces.length === 3) {
				      colorArray = ["#1d8dc3","#449ac3","#6ba6c3"];
				    } else if (pieces.length === 4) {
				      colorArray = ["#1d8dc3","#3193c3", "#449ac3", "#58a0c3"];
				    } else {
				      // fix this later; implement some kind of spectrum for high number of sectors
				      colorArray = ["#1d8dc3","#3193c3", "#449ac3", "#58a0c3","#6ba6c3"];
				    }

				    var startAngle = 0; //Start Angle of Each Slice
				    var Radius = 50;
				    var CENTER_X = 100; //X-coordinate of the circle's center
				    var CENTER_Y = 100; //Y-coordinate of the circle's center

				    //Compute the delta angles; the angles for each sector.
				    var i = 0;
				    deltaAngles = [];
				    for (i = 0; i < pieces.length; i += 1) {
				      deltaAngles[i] = self._convertProportionToDegreesRadian(pieces[i].fraction);
				    }

				    // Creates canvas 200 × 200 at 0, 0; canvas starts in the upper left hand corner of the browser
				    var canvas = Raphael(self.element[0], 200, 200);
				    // set() creates an array-like object, to deal with several elements at once.
				    var sectorSet = canvas.set();  

				    for (i = 0; i < pieces.length; i += 1){
				      sector = self._drawSector(startAngle, Radius, CENTER_X, CENTER_Y, deltaAngles[i], {fill: colorArray[i], stroke: "#fff", opacity: 1}, canvas);
				      sector.attr({title: pieces[i].fraction*100 + '% ' + pieces[i].status});
				      sectorSet.push(sector);
				      startAngle = startAngle + deltaAngles[i];
				    }

				    // Text that describes various portions of the pie chart
				    var description = canvas.text(100, 180, "Open and Closed Service Requests");
				    description.attr({"font-size": 12});

				    //Handle the mouseover
				    sectorSet.mouseover(function () {
				      this.animate({scale: [1.05, 1.05, CENTER_X, CENTER_Y], stroke:"#cccccc"}, 250, "cubic-bezier(0.42, 0, 1.0, 1.0)");
				      description.attr({text:this.attr("title")});
				      // alert(typeof this.attr("title"));
				    })
				    .mouseout(function () {
				      this.animate({scale: [1, 1, CENTER_X, CENTER_Y], fill:this.attr("fill"), stroke: "#fff"}, 250, "cubic-bezier(0.42, 0, 1.0, 1.0)");
				      description.attr({text:"Open and Closed Service Requests"});
				    });
					
				} else {
					self.valueDiv = $('<div class="no-data">No data, sucka.</div>')
						.appendTo(self.element);
				}
    		}  
  	});
  },

  /**
   * Convert proportion to degree radians
   */
  _convertProportionToDegreesRadian: function(proportion) {
    return proportion * 2 * Math.PI;
  },

  /**
   * Draw sector
   */
  _drawSector: function(startAngle, Radius, CENTER_X, CENTER_Y, deltaAngle, displayParameters, canvas) {
    //Drawing a path; return it so we can do things to it later on.
    var secondX = CENTER_X + Radius * Math.cos(-startAngle);
    var secondY = CENTER_Y + Radius * Math.sin(-startAngle);

    var finalAngle = startAngle + deltaAngle;

    var thirdX = CENTER_X + Radius * Math.cos(-finalAngle);
    var thirdY = CENTER_Y + Radius * Math.sin(-finalAngle);

    // converts a boolean value to a 0 or a 1
    return canvas.path(["M",CENTER_X, CENTER_Y, "L", secondX, secondY, "A", Radius, Radius, 0, +(finalAngle - startAngle > Math.PI), 0, thirdX, thirdY, "z"]).attr(displayParameters);
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