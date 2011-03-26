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

$.widget( "Open311.map", {
	options: {
	},

  // Basic map parameters for initialization
  CENTER_LATITUDE: 37.76,
  CENTER_LONGITUDE: -122.44,
  INITIAL_ZOOM_LEVEL: 11,

	_create: function() {
		this.element
			.addClass( "ui-widget" )
			.attr({
				role: "map",
			});

		this.containerDiv = $( "<div id='map_container' style='width: 400px; height: 250px'></div>" )
			.appendTo( this.element );
    this._loadData();
	},

  _loadData: function() {
    jQuery.getJSON('data/ServiceRequests_Complete.json', this._initMap);
  },

  _initMap: function(data) {
    //Getting our custom map tiles from CloudMade.  We're using a special API key for Short Stack.
    var cloudmade = new CM.Tiles.CloudMade.Web({
      key: '90480db8a5a4470d87c3c21800806e02',
      styleId: 1714,
      copyright: 'Map tiles &copy; 2011 CloudMade Map data CC-BY-SA OpenStreetMap.org ',
      minZoomLevel: 9
    });

    //Creating and centering the map
    var map = new CM.Map('map_container', cloudmade);
    
    map.setCenter(new CM.LatLng(this.CENTER_LATITUDE, this.CENTER_LONGITUDE), this.INITIAL_ZOOM_LEVEL);

    //Using default map controls for now
    map.addControl(new CM.SmallMapControl());

    //Defining the marker icon
    var markerIcon = new CM.Icon();
    markerIcon.image = "images/samplemarker.png";
    markerIcon.iconSize = new CM.Size(8, 8);
    markerIcon.iconAnchor = new CM.Point(4, 3.5);

    //Defining a sample marker
    var sampleMarker = new CM.Marker(new CM.LatLng(this.CENTER_LATITUDE, this.CENTER_LONGITUDE), {
      //title: data.location[0].name,
      title: "hi",
      icon: markerIcon
    });

    //We can have infobubbles if we want.  Just place a string of html into the bindInfoWindow method.
    sampleMarker.bindInfoWindow("<h2 style='color:#10394b; text-align: center' >" + "hi" + "</h2>", {
      maxWidth: 180
    });

    //Adding the marker to the map
    map.addOverlay(sampleMarker);

    var markers = [];
    var len = data.requests.length;
    for (var i=0; i < len; i++){
        if(data.requests[i].status === "Open"){
          markers[i] = new CM.Marker(new CM.LatLng(data.requests[i].lat, data.requests[i].lon), {
						title: data.requests[i].service_name,
						icon: markerIcon
						});
					markers[i].bindInfoWindow("<h2 style='color:#10394b; text-align: center' >" + data.requests[i].service_name + " at " + data.requests[i].address + "</h2>", {
                    maxWidth: 180
					});
					map.addOverlay(markers[i]);
					}
				}
  },

	_destroy: function() {
		this.element
			.removeClass( "ui-widget" )
			.removeAttr( "role" );

		this.containerDiv.remove();
	}

});

$.extend( $.ui.progressbar, {
	version: "@VERSION"
});

})( jQuery );
