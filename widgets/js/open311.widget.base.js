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
    dataSource: '',
    titleClass: 'ui-widget-header',
    contentClass: 'ui-widget-content',
    loadingClass: 'ui-loading',
    loadedClass: 'ui-loaded'
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
        .prependTo(this.element);
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
  },

  /**
   * Loading
   */
  loading: function(value) {
    $(this.element).removeClass(this.options.loadedClass)
      .addClass(this.options.loadingClass)
      .trigger('loading');
  },

  /**
   * Loaded
   */
  loaded: function(value) {
    $(this.element).removeClass(this.options.loadingClass)
      .addClass(this.options.loadedClass)
      .trigger('loaded');
  }
});

})( jQuery );