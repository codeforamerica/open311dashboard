/**
 * Base Widget for Global Inputs, like search
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 */
(function( $, undefined ) {

$.widget('Open311.globalInput', $.Open311.base, {
  /**
   * Default options for the widget.  We need some way
   * of communicating the data source across all widgets.
   */
  options: {
    title: 'Global Input'
  },
  
  /**
   * Init functions for all barchart google widgets.
   */
  _init: function() {
    this.updateTitle();
    $(this.element).addClass('open311-global-input');
  }
});

})( jQuery );