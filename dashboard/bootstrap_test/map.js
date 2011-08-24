/* jslint nomen:true */
var Map = {
  po: org.polymaps,
  layers: [],
  alwaysVisible: [],
  indices: [],
  visibleIndex: null,
  container: null,

  /* Create the map element and add interaction */
  createmap: function (id, latlong) {
    if (id === undefined) { id = "map"; }

    /* Default to San Francisco */
    if (latlong === undefined) { latlong = {lat: 37.7516, lon: -122.44}; }

    this.container = document.getElementById(id).appendChild(this.po.svg("svg"));

    this.map = this.po.map()
      .container(this.container)
      .center(latlong)
      .zoom(12)
      .zoomRange([12, 16])
      .add(this.po.interact());

    this.map.add(this.po.hash());

    this.map.add(this.po.image()
                 .url(this.po.url("http://{S}tile.cloudmade.com"
                    + "/1a193057ca6040fca68c4ae162bec2da"
                    + "/39534/256/{Z}/{X}/{Y}.png")
                    .hosts(["a.", "b.", "c.", ""])));
  },

  /* Add GeoJSON layer */
  addLayer: function (src, obj) {
    var layer, layerId;

    /* Set defaults */
    if (obj === undefined) { obj = {}; }
    if (obj.alwaysVisible === undefined) { obj.alwaysVisible = false; }
    if (obj.visible === undefined) { obj.visible = false; }

    /* What kind of layer are we adding? */
    if ((obj.type === undefined) || (obj.type === "geoJson")) {
      layer = this.po.geoJson().tile(false).url(src);
    } else if (obj.type === "image") {
      layer = this.po.image().url(this.po.url(src));
    }

    /* Layer dependent defaults */
    if (obj.load !== undefined) { layer = layer.on("load", obj.load); }
    if (obj.zoom !== undefined) { layer = layer.zoom(obj.zoom); }
    if (obj.id !== undefined) { layer = layer.id(obj.id); }
    if (obj.index !== undefined) { layer.index = obj.index; }

    /* Add the layer but set the visibility to false. */
    // this.map.add(layer);
    // layer.visible(false);

    /* If the layer is part of a group, add it to the group */
    if (typeof (obj.group) !== "number") {
      layerId = this._addLayer(layer);
    } else {
      layerId = this._addLayerToGroup(layer, obj.group);
    }

    /* Show layers that we want to show */
    if ((obj.alwaysVisible === false) && (obj.visible === true)) {
      this.switchVisibleLayer(layerId);
    } else if (obj.alwaysVisible === true) {
      layer.visible(true);

      /* We need to save the alwaysVisible layers to reshow them whenever
       * we switch layers */
      this.alwaysVisible.push(layer);
    }

    /* Return the layerID so we can save it */
    return layerId;
  },

  /* Switch visible layer */
  switchVisibleLayer: function (id) {
    /* If we're showing a layer, hide it. */
    if (this.visibleIndex !== null) {
      this._setVisibility(this.layers[this.visibleIndex], false);
    }

    this._setVisibility(this.layers[id], true);

    /* Update the visibleIndex */
    this.visibleIndex = id;
    this._rebuildLayers();

  },

  /* Push the layer onto the stack and return the index. */
  _addLayer: function (layer) {
    this.layers.push(layer);
    return this.layers.indexOf(layer);
  },

  _addLayerToGroup: function (layer, index) {
    /* Convert the layer to a group if there isn't already a group. */
    if (!(this.layers[index] instanceof Array)) {
      this.layers[index] = [this.layers[index]];
    }

    this.layers[index].push(layer);
    return index;
  },

  /* Set the visibility of a layer or set of layers */
  _setVisibility: function (layer, visibility) {
    if (layer instanceof Array) {
      for (var i = 0; i < layer.length; i += 1) {
        layer[i].visible(visibility);
        if (visibility === false) {
          this.map.remove(layer[i]);
        }
      }
    } else {
      layer.visible(visibility);
      if (visibility === false) { this.map.remove(layer); }
    }
  },

  /* Rebuild all of the layers on top of the base. */
  _rebuildLayers: function() {
    var tempSort = [];

    tempSort = tempSort.concat(this.layers[this.visibleIndex], this.alwaysVisible);
    tempSort = tempSort.sort(function(a, b) { return a.index - b.index; });

    for (var i = 0; i < tempSort.length; i += 1) {
      if (typeof(tempSort[i]) !== "undefined") {
        console.log(tempSort[i].index);
        // this.map.remove(tempSort[i]);
        this.map.add(tempSort[i]);
        tempSort[i].visible(true);
      }
    }
  },

  /* Various methods to handle events */
  event: {
    /**
     * [ { condition: .9,
     *     color: "#ccc" }]
     **/
    colorArray: [],

    /* Abstraction of the color event */
    color: function(e) {
      for (i = 0; i < e.features.length; i += 1) {
        for (j = 0; j < this.colorArray.length; j += 1) {
          if (e.features[i].data.properties.percentile > this.colorArray[j].condition) {
            e.features[i].element.setAttribute("stroke", this.colorArray[i].color);
          }
        }
      }
    }
  }
};
