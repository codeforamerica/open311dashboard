/**
 * Base Widget for Open311
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 *   Google Maps API
 */
(function( $, undefined ) {

$.widget('Open311.mapGoogle', $.Open311.base, {
  /**
   * Default options for the widget.  We need some way
   * of communicating the data source across all widgets.
   */
  options: {
    title: 'Google Map',
    containerID: 'open311-map-google-container',
    mapWidth: 'auto',
    mapHeight: '250px',
    centerLat: 37.7733,
    centerLon: -122.417,
    map: null
  },

  /**
   * Create map container
   */
  createMapContainer: function() {
    // Add an element to create map on
		this.updateContent('<div id="' + this.options.containerID + '" style="width: ' + this.options.mapWidth + '; height: ' + this.options.mapHeight + '"></div>');
  },

  /**
   * Create map
   */
  createMap: function() {
    if (typeof google != 'undefined') {
      map = new google.maps.Map(document.getElementById(this.options.containerID), {
        zoom: 15,
        center: new google.maps.LatLng(this.options.centerLat, this.options.centerLon),
        mapTypeId: google.maps.MapTypeId.ROADMAP
      });
      this.map = map;
    } else {
      this.map = null;
    }
  },
  
  /**
   * Add markers, given map and data
   */
  addMarkers: function(map, data, self) {
    var markers = [];
    for (i = 0; i < data.requests.length; i++) {
      if (data.requests[i].status === 'Open') {
        // TODO: template this out
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
  }
});

})( jQuery );