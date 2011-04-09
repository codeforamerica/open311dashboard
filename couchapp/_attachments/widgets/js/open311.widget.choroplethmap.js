/**
 * Choropleth Map widget for Open311 Dashboard
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 */
(function( $, undefined ) {

$.widget('Open311.choroplethMap', $.Open311.base, {
  /**
   * Default options for the widget.  We need some way
   * of communicating the data source across all widgets.
   */
  options: {
    title: 'Choropleth Map',
    gmapBaseStyle: {
      name: 'Styled Base Map',
      def: [ { featureType: 'road', elementType: 'all', stylers: [ { visibility: 'off' } ] },{ featureType: 'transit', elementType: 'all', stylers: [ { visibility: 'off' } ] },{ featureType: 'poi', elementType: 'all', stylers: [ { visibility: 'off' } ] },{ featureType: 'administrative', elementType: 'all', stylers: [ { visibility: 'off' } ] },{ featureType: 'all', elementType: 'labels', stylers: [ { visibility: 'off' } ] },{ featureType: 'poi.park', elementType: 'all', stylers: [ { visibility: 'simplified' }, { hue: '#00ff19' }, { lightness: -71 }, { saturation: -90 } ] },{ featureType: 'poi.park', elementType: 'labels', stylers: [ { visibility: 'off' } ] },{ featureType: 'water', elementType: 'all', stylers: [ { lightness: -100 } ] },{ featureType: 'landscape', elementType: 'all', stylers: [ { visibility: 'off' }, { lightness: -86 }, { hue: '#2a00ff' }, { saturation: -98 } ] } ]
    }
  },
  
  _getChoroplethStyle: function(min, max, prop, breakColors){
    var style = new OpenLayers.Style(),
      rules = [],
      diff = Math.round(max - min),
      breakSize = Math.round(diff/breakColors.length),
      curMin = min,
      i = 0;
    
    while (curMin < max) {
      rules.push(new OpenLayers.Rule({
        filter: new OpenLayers.Filter.Comparison({
            type: OpenLayers.Filter.Comparison.BETWEEN,
            property: prop,
            lowerBoundary: curMin,
            upperBoundary: (curMin + breakSize)
        }),
        symbolizer: {pointRadius: 10, fillColor: breakColors[i], fillOpacity: 0.5, strokeColor: '#000000'}
      }));
      
      curMin = curMin + breakSize + 1;
      i++;
    }

    style.addRules(rules);

    return style;
  },
  
  /**
   * Creation code for widget
   */
  _create: function() {
    var self = this,
      gmapStyledMapType, geoJsonFormat, vectorLayer, style;
    
    self._bindEvents();    
    self.updateTitle();
    $(self.element).append('<div id="open311-choropleth-map" class="ui-widget-content" style="height:250px;"></div>');
    
    gmapStyledMapType = new google.maps.StyledMapType(self.options.gmapBaseStyle.def, {name: self.options.gmapBaseStyle.name});
    
    self.map = new OpenLayers.Map({
      div: 'open311-choropleth-map',
      projection: new OpenLayers.Projection('EPSG:900913'),
      units: 'm',
      maxResolution: 156543.0339,
      maxExtent: new OpenLayers.Bounds(
          -20037508, -20037508, 20037508, 20037508.34
      )
    });

    var styledBaseLayer = new OpenLayers.Layer.Google('Styled Base Layer', { type: 'choropleth-base' });
    self.map.addLayers([styledBaseLayer]);
    styledBaseLayer.mapObject.mapTypes.set('choropleth-base', gmapStyledMapType);

    self.map.setCenter(new OpenLayers.LonLat(-13631059, 4545733), 12);

    style = self._getChoroplethStyle(1, 100, 'colorId', ['#EFF3FF', '#BDD7E7', '#6BAED6', '#2171B5']);
    geoJsonFormat = new OpenLayers.Format.GeoJSON();
    vectorLayer = new OpenLayers.Layer.Vector('choropleth', {
      styleMap: new OpenLayers.StyleMap(style)
    });

    self.map.addLayer(vectorLayer);
    
    $.getJSON('data/sfzipcodes.json', function(geoJson){
      vectorLayer.addFeatures(geoJsonFormat.read(geoJson));
    });
  },
  
  _bindEvents: function(){
    var self = this, min, max;
    
    $($.Open311).bind('open311-data-update', function(event, data){
      var layer = self.map.getLayersByName('choropleth')[0],
        counts = [],
        countsByGeography = {},
        i;

      $.each(data.service_requests, function(i, req){
        
        if (parseInt(req.zipcode)) {
          if (countsByGeography[req.zipcode]) {
            countsByGeography[req.zipcode]++;
          } else {
            countsByGeography[req.zipcode] = 1;
          }
        }
      });
      
      $.each(countsByGeography, function(zip, count) {
        counts.push(count);
      });
      
      min = Math.min.apply(null, counts);
      max = Math.max.apply(null, counts);

      $.each(layer.features, function(i, feat){
        feat.attributes.colorId = Math.round((countsByGeography[feat.attributes.ZIP_CODE.toString()] / max) * 100);
      });
      layer.redraw();
    });
  },  
  
  /**
   * Destroy widget
   */
  destroy: function() {
     $.Widget.prototype.destroy.apply(this, arguments); // default destroy
      // now do other stuff particular to this widget
  }
});

})( jQuery );