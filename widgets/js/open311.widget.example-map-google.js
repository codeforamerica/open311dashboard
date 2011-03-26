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
    title: 'Google Map of Incidents'
	},

	_create: function() {
	  var self = this;
    this.updateTitle();
    this.createMapContainer();
    this.createMap();
    
    // Load data.
    jQuery.getJSON(this.options.dataSource, function(data) {
      self.addMarkers(map, data, self);
    });
	}

});

})( jQuery );
