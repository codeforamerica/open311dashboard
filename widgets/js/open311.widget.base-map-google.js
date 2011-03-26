/**
 * Base Widget for Open311
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 *   Google Maps API
 */
(function( $, undefined ) {

$.widget('Open311.barchartGoogle', $.Open311.base, {
  /**
   * Default options for the widget.  We need some way
   * of communicating the data source across all widgets.
   */
  options: {
    title: 'Bar Chart',
    chartWidth: '300',
    chartWidth: '250'
  },
  
  /**
   * Init functions for all map google widgets.
   */
  _init: function() {
    this.updateTitle();
  },
});

})( jQuery );