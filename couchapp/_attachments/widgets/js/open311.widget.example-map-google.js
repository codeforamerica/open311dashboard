/*
 * jQuery UI Sparkline Widget @VERSION
 *
 * Copyright 2011, AUTHORS.txt (http://jqueryui.com/about)
 * Dual licensed under the MIT or GPL Version 2 licenses.
 * http://jquery.org/license
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 */
(function( $, undefined ) {

$.widget('Open311.mapGoogleExample', $.Open311.mapGoogle, {
	options: {
    title: 'Map of Incidents'
	},

	_create: function() {
	  var self = this;
    this.updateTitle();
    this.createMapContainer();
    this.createMap();
    
    self._bindEvents();
  },
  
  /**
   * Bind events
   */
  _bindEvents: function(){
    var self = this;
    this.loading();
    $($.Open311).bind('open311-data-update', function(event, data) {
      self._render(data);
    });
  },
  
  /**
   * Render function
   */
  _render: function(data) {
    this.addMarkers(data, this);
    this.loaded();
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
