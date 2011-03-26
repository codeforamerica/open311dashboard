/**
 * Base Widget for Pie Charts with Raphael
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 *   raphael.js
 */
(function( $, undefined ) {

$.widget('Open311.pieRaphael', $.Open311.base, {
  /**
   * Default options for the widget.  We need some way
   * of communicating the data source across all widgets.
   */
  options: {
    title: 'Raphael Pie Chart'
  },
  
  /**
   * Init functions for all barchart google widgets.
   */
  _init: function() {
    this.updateTitle();
  },

  /**
   * Convert proportion to degree radians
   */
  convertProportionToDegreesRadian: function(proportion) {
    return proportion * 2 * Math.PI;
  },

  /**
   * Draw sector
   */
  drawSector: function(startAngle, Radius, CENTER_X, CENTER_Y, deltaAngle, displayParameters, canvas) {
    //Drawing a path; return it so we can do things to it later on.
    var secondX = CENTER_X + Radius * Math.cos(-startAngle);
    var secondY = CENTER_Y + Radius * Math.sin(-startAngle);

    var finalAngle = startAngle + deltaAngle;

    var thirdX = CENTER_X + Radius * Math.cos(-finalAngle);
    var thirdY = CENTER_Y + Radius * Math.sin(-finalAngle);

    // converts a boolean value to a 0 or a 1
    return canvas.path(["M",CENTER_X, CENTER_Y, "L", secondX, secondY, "A", Radius, Radius, 0, +(finalAngle - startAngle > Math.PI), 0, thirdX, thirdY, "z"]).attr(displayParameters);
  }
});

})( jQuery );