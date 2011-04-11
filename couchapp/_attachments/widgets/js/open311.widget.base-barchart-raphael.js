/**
 * Base Widget for Pie Charts with Raphael
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 *   raphael.js
 */
(function( $, undefined ) {

$.widget('Open311.barRaphael', $.Open311.base, {
  /**
   * Default options for the widget.  We need some way
   * of communicating the data source across all widgets.
   */
  options: {
    title: 'Raphael Bar Chart'
  },
  
  /**
   * Init functions for all barchart google widgets.
   */
  _init: function() {
    this.updateTitle();
    $(this.element).addClass('open311-bar-raphael');
  }
)( jQuery );
