/**
 * Base Widget for Google Gauge for Open311
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 */
(function( $, undefined ) {

$.widget('Open311.gaugeGoogle', $.Open311.base, {
  /**
   * Default options for the widget.  We need some way
   * of communicating the data source across all widgets.
   */
  options: {
    title: 'Gauge',
    chartWidth: '300',
    chartWidth: '250'
  },
  
  /**
   * Init functions for all gauge google widgets.
   */
  _init: function() {
    this.updateTitle();
  },
});

})( jQuery );