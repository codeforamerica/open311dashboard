var Map = {
  po: org.polymaps,
  layers: [],
  alwaysVisible: [],
  visibleIndex: null,

  /* Create the map element and add interaction */
  createmap: function (id, latlong) {
    if (id == undefined) {
      id = "map";
    }

    if (latlong == undefined) {
      latlong = {lat:37.7516, lon: -122.44};
    }

    this.map = this.po.map()
      .container(document.getElementById(id).appendChild(this.po.svg("svg")))
      .center(latlong)
      .zoom(12)
      .zoomRange([12,16])
      .add(this.po.interact());

    this.map.add(this.po.hash());

    this.map.add(this.po.image()
                 .url(this.po.url("http://{S}tile.cloudmade.com"
                    + "/1a193057ca6040fca68c4ae162bec2da"
                    + "/39534/256/{Z}/{X}/{Y}.png")
                    .hosts(["a.", "b.", "c.", ""])));
  },

  /* Add GeoJSON layer */
  addLayer: function(src, obj) {

    /* Set defaults */
    if (obj == undefined) { obj = {}; }
    if (obj.id == undefined) { obj.id = null; }
    if (obj.load == undefined) { obj.load = null; }
    if (obj.alwaysVisible == undefined) { obj.alwaysVisible = false; }
    if (obj.visible == undefined) { obj.visible = false; }

    /* What kind of layer are we adding? */
    if ((obj.type == undefined) || (obj.type == "geoJson")) {
      layer = this.po.geoJson().tile(false).url(src);
    } else if (obj.type == "image") {
      layer = this.po.image().url(this.po.url(src));
    }

    /* ID */
    layer = layer.id(obj.id);

    /* If there is a load event */
    if (obj.load != null) {
         layer = layer.on("load", obj.load);
    }

    /* Add the layer but set the visibility to false. */
    this.map.add(layer);
    layer.visible(false);

    /* If the layer is part of a group, add it to the group */
    if (typeof(obj.group) != "number") {
      layerId = this._addLayer(layer);
    } else {
      layerId = this._addLayerToGroup(layer, obj.group);
    }

    /* Show layers that we want to show */
    if ((obj.alwaysVisible == false) && (obj.visible == true)) {
      this.switchVisibleLayer(layerId);
    } else if (obj.alwaysVisible == true) {
      layer.visible(true);

      /* We need to save the alwaysVisible layers to reshow them whenever
       * we switch layers */
      this.alwaysVisible.push(layerId);
    }

    /* Return the layerID so we can save it */
    return layerId;
  },

  /* Switch visible layer */
  switchVisibleLayer: function(id) {
    /* If we're showing a layer, hide it. */
    if (this.visibleIndex != null) {

      /* Iterate through the layer array if there is one */
      if (this.layers[this.visibleIndex] instanceof Array) {
        for(i=0;i < this.layers[this.visibleIndex].length;i++) {
          this.layers[this.visibleIndex][i].visible(false);
        }
      } else {
        /* Otherwise, just hide the layer */
        this.layers[this.visibleIndex].visible(false);
      }
    }

    /* Iterate through the new layer array if there is one */
    if (this.layers[id] instanceof Array) {
      for(i=0; i < this.layers[id].length; i++) {
        this.layers[id][i].visible(true);
      }
    } else {
      this.layers[id].visible(true);
    }

    /* Reshow all the alwaysVisible layers */
    for (i = 0; i < this.alwaysVisible.length; i++) {
      this.layers[this.alwaysVisible[i]].visible(true);
    }

    /* Update the visibleIndex */
    this.visibleIndex = id;
  },

  /* Push the layer onto the stack and return the index. */
  _addLayer: function(layer) {
    this.layers.push(layer);
    return this.layers.indexOf(layer);
  },

  _addLayerToGroup: function(layer, index) {
    /* Convert the layer to a group if there isn't already a group. */
    if (!(this.layers[index] instanceof Array)) {
      this.layers[index] = [this.layers[index]];
    }

    this.layers[index].push(layer);
    return index;
  }
};
