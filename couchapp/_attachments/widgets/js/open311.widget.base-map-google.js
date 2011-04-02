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
   * Init functions for all map google widgets.
   */
  _init: function() {
    this.updateTitle();
    $(this.element).addClass('open311-map-google');
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
  
  clearMarkers: function() {
    var i = 0;
    
    if (this.markers && this.markers.length){
      for (i=0; i<this.markers.length; i++){
        this.markers[i].setMap(null);
      }
    }
  },
  
  /**
   * Add markers, given map and data
   */
  addMarkers: function(data, self) {
    var map = this.map || self.map;
    var markers = this.markers = this.markers || [];
    var openWindow;
    
    $.each(data.service_requests, function(i, service_req) {
      if (service_req.lat && service_req.long) {
        // TODO: template this out
        var infoContent = "<h2 style='color:#10394b; text-align: center' >" + service_req.service_name + " at " + service_req.address + "</h2>";
        var latlng = new google.maps.LatLng(service_req.lat, service_req.long);
        var infowindow = new google.maps.InfoWindow({
          content: infoContent,
          position: latlng,
          maxWidth: 300
        });
        markers[i] = new google.maps.Marker({
          position: latlng,
          map: map,
          title: service_req.service_name
        });
        google.maps.event.addListener(markers[i], 'click', function() {
          if (openWindow) {
            openWindow.close();
          }
          
          openWindow = infowindow;
          infowindow.open(map, markers[i]);
        });
      }
    });
  }
});

})( jQuery );