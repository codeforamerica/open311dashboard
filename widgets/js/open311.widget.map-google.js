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

$.widget( "Open311.mapGoogle", {
	options: {
    dataSource: '',
    id: 'map-google-container',
	},

	_create: function() {
    this.element
			.attr({role: "map"});
    // Add an element to create map on
		this.containerDiv = $('<div id="' + this.options.id + '" style="width: auto; height: 250px"></div>')
		  .appendTo(this.element);
    
    // Load data.
    this._loadData();
	},

  /**
   * Loads data from data source.
   */
  _loadData: function() {
    jQuery.getJSON(this.options.dataSource, this._initMap);
  },

  /**
   * Initialize the map.
   */
  _initMap: function(data) {
    map = new google.maps.Map(document.getElementById('map-google-container'), {
      zoom: 15,
      center: new google.maps.LatLng(37.7733, -122.417),
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });
    
    var markers = [];
    for (i = 0; i < data.requests.length; i++) {
      if (data.requests[i].status === "Open") {
        var infoContent = "<h2 style='color:#10394b; text-align: center' >" + data.requests[i].service_name + " at " + data.requests[i].address + "</h2>";
        var latlng = new google.maps.LatLng(data.requests[i].lat, data.requests[i].lon);
        var infowindow = new google.maps.InfoWindow({
          content: infoContent
        });
        markers[i] = new google.maps.Marker({
          position: latlng,
          map: map,
          title: data.requests[i].service_name
        });
        google.maps.event.addListener(markers[i], 'click', function() {
          infowindow.open(map, markers[i]);
        });
      }
    }
  },

	_destroy: function() {
		this.element
			.removeClass('ui-widget')
			.removeAttr('role');
		this.containerDiv.remove();
	}

});

})( jQuery );
