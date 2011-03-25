/**
 * Example widget for Open311 Dashboard
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 */
(function( $, undefined ) {

$.widget("widget.example-widget", {
  /**
   * Default options for the widget.  We need some way
   * of communicating the data source across all widgets.
   */
  options: {
    option1: "defaultValue",
    hidden: true
  },
  
  /**
   * Creation code for widget
   */
  _create: function() {
    // can use this.options
    if (this.options.hidden) {
      // and this.element
      this.element.hide();
    }
  },
  
  /**
   * Internal methods
   *
   * IMPORTANT: internal functions should be named with a leading underscore
   * manipulate the widget
   */
  _doSomething: function() {
    // does something
  },
  
  /**
   * External function
   */
  doSomethingElse: function() {
   // calculate some value and return it
   return this._doSomething();
  },
  
  /**
   * Destroy widget
   */
  destroy: function() {
     $.Widget.prototype.destroy.apply(this, arguments); // default destroy
      // now do other stuff particular to this widget
  }
});

});