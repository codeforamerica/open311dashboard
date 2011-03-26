/**
 * Base Widget for Open311
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 */
(function( $, undefined ) {

$.widget('Open311.base', {
  /**
   * Default options for the widget.  We need some way
   * of communicating the data source across all widgets.
   */
  options: {
    title: 'Widget Title',
    titleClass: 'ui-widget-header',
    contentClass: 'ui-widget-content',
    dataSource: ''
  },

  /**
   * Update title
   */
  updateTitle: function(value) {
    var title = (typeof value == 'undefined') ? this.options.title : value;

    // Check for title, update or create.
    if (this.titleContainer) {
      $(this.titleContainer).val(title);
    } else {
      this.titleContainer = $('<h2 class="' + this.options.titleClass + '">' + title + '</h2>')
        .appendTo(this.element);
    }
  },

  /**
   * Update content
   */
  updateContent: function(value) {
    // Check for title, update or create.
    if (this.contentContainer) {
      $(this.contentContainer).html(value);
    } else {
      this.contentContainer = $('<div class="' + this.options.contentClass + '">' + value + '</div>')
        .appendTo(this.element);
    }
  }
});

})( jQuery );