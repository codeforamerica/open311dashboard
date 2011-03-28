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
    title: 'Open vs Closed',
    startdate: "2010-11-11T00:00:00",
    enddate: "2010-11-15T00:00:00",
    topX: 10,
    dataSource: "http://open311.couchone.com/service-requests/_design/requests/_list/requests-json/allbytime"
  },
  
  /**
   * Creation code for widget
   */
  _create: function() {
    // Create container to put chart in.
    this.updateContent('');
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
        if (data.service_requests.length > 0) {
          var openReqs = closedReqs = 0;
          // Loop through the returned data and count open vs closed
					$(data.service_requests).each(function(index, elm) {
						if(elm.status == "Open") openReqs++
						else if(elm.status == 'Closed') closedReqs++;
					});
					
					totReqs = openReqs+closedReqs;
          pieces = [
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
			      deltaAngles[i] = self.convertProportionToDegreesRadian(pieces[i].fraction);
			    }

			    var canvas = Raphael(self.contentContainer[0], 200, 200);
			    // set() creates an array-like object, to deal with several elements at once.
			    var sectorSet = canvas.set();  

			    for (i = 0; i < pieces.length; i += 1){
			      sector = self.drawSector(startAngle, Radius, CENTER_X, CENTER_Y, deltaAngles[i], {fill: colorArray[i], stroke: "#fff", opacity: 1}, canvas);
			      sector.attr({title: (pieces[i].fraction*100).toFixed(2) + '% ' + pieces[i].status});
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
					self.valueDiv = $('<div class="no-data">No data found.</div>')
						.appendTo(self.element);
				}
      }  
  	});
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