/**
 * Pie Chart by Type for Open311 Dashboard
 *
 * This provides a pie chart by open311 types.
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 *   raphael.js
 */
(function( $, undefined ) {

$.widget("widget.pieType", {
  /**
   * Default options for the widget.  We need some way
   * of communicating the data source across all widgets.
   */
  options: {
    data_source: "",
    pieces: [
      {status: "Open", fraction:.6}, 
      {status: "Closed", fraction:.4}
    ],
    colorArray: []
  },
  
  /**
   * Creation code for widget
   */
  _create: function() {
    // Check for Raphael
    if (typeof Raphael == 'undefined') {
      return;
    }
    
    // Deal with colors
    if (this.options.pieces.length === 2) {
      this.options.colorArray = ["#D2E9F3", "#1d8dc3"];
    } else if (this.options.pieces.length === 3) {
      this.options.colorArray = ["#1d8dc3","#449ac3","#6ba6c3"];
    } else if (this.options.pieces.length === 4) {
      this.options.colorArray = ["#1d8dc3","#3193c3", "#449ac3", "#58a0c3"];
    } else {
      // fix this later; implement some kind of spectrum for high number of sectors
      this.options.colorArray = ["#1d8dc3","#3193c3", "#449ac3", "#58a0c3","#6ba6c3"];
    }

    var startAngle = 0; //Start Angle of Each Slice
    var Radius = 50;
    var CENTER_X = 100; //X-coordinate of the circle's center
    var CENTER_Y = 100; //Y-coordinate of the circle's center

    //Compute the delta angles; the angles for each sector.
    var i = 0;
    deltaAngles = [];
    for (i = 0; i < this.options.pieces.length; i += 1) {
      deltaAngles[i] = this._convertProportionToDegreesRadian(this.options.pieces[i].fraction);
    }

    // Creates canvas 200 × 200 at 0, 0; canvas starts in the upper left hand corner of the browser
    var canvas = Raphael(this.element[0], 200, 200);
    // set() creates an array-like object, to deal with several elements at once.
    var sectorSet = canvas.set();  

    for (i = 0; i < this.options.pieces.length; i += 1){
      sector = this._drawSector(startAngle, Radius, CENTER_X, CENTER_Y, deltaAngles[i], {fill: this.options.colorArray[i], stroke: "#fff", opacity: 1}, canvas);
      sector.attr({title: this.options.pieces[i].fraction*100 + '% ' + this.options.pieces[i].status});
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