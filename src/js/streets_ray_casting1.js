var features_coordinates = []; //dom ready
var features_rect_bounds = [];
var neighborhood_features = [];
var highlighted = -1;
var $neighborhoodStats = $('#result_data');

function insideRectBounds(feature_rect_bounds,mp_ll){
    var lon = mp_ll[0];
    var lat = mp_ll[1];
    var max_lon = feature_rect_bounds[0];
    var min_lon = feature_rect_bounds[1];
    var max_lat = feature_rect_bounds[2];
    var min_lat = feature_rect_bounds[3];
    
    if((lon > max_lon) || (lon < min_lon) || (lat > max_lat) || (lat < min_lat)){
        return false;
    } else {
        return true;
    }
};

function insidePolygon(mp_ll,index){
    if (!insideRectBounds(features_rect_bounds[index],mp_ll)){
        return false;
    }

    var verticesCount = features_coordinates[index].length;
    var inside = false;
    var i;
    var j = verticesCount - 1;
    var vertexA;
    var vertexB;

    for(i=0; i < verticesCount; i++){
        vertexA = features_coordinates[index][i];
        vertexB = features_coordinates[index][j];

          if(((vertexA[0] < mp_ll[0]) && (vertexB[0] >= mp_ll[0])) || ((vertexB[0] < mp_ll[0]) && (vertexA[0] >= mp_ll[0]))) {
      if(vertexA[1] + (((mp_ll[0] - vertexA[0]) / (vertexB[0] - vertexA[0])) * (vertexB[1] - vertexA[1])) < mp_ll[1]) {
           inside = !inside;
      }
    }
    j = i;
    }

    return inside;
};

function onloadneighborhoods(e){
    var lon = [];
    var lat = [];
    for(var i = 0; i < e.features.length; i++) {
        neighborhood_features[i] = e.features[i];

        features_coordinates[i] = e.features[i].data.geometry.coordinates;
        
        for (var j=0; j < e.features[i].data.geometry.coordinates.length; j++){
            lon[j] = e.features[i].data.geometry.coordinates[j][0];
            lat[j] = e.features[i].data.geometry.coordinates[j][1];
        }
        features_rect_bounds[i] = [Math.max.apply(Math,lon),Math.min.apply(Math,lon),Math.max.apply(Math,lat),Math.min.apply(Math,lat)];

        e.features[i].element.onmouseover = testNeighborhood;
        e.features[i].element.onmousemove = testNeighborhood;
        e.features[i].element.onmouseout = testNeighborhood;
    }
}

function updateNeighborhoodStats(feature) {
  $neighborhoodStats.html(feature.data.properties.neighborhood);
}

function testNeighborhood(e){
    var mp_ll = [map.pointLocation(map.mouse(e)).lon,map.pointLocation(map.mouse(e)).lat];

    for(var i = 0; i < features_coordinates.length; i++){
        if (insidePolygon(mp_ll,i)){
            handleHighlight(i);
            return;
        }
    }

    handleHighlight(-1);
};

function handleHighlight(i){
    if (highlighted === i){
        return;
    } else if (highlighted !== -1){
        unhighlightNeighborhood(highlighted);
    };

    if (i !== -1){
        highlightNeighborhood(i);
        updateNeighborhoodStats(neighborhood_features[i]);
    }
    highlighted = i;

};

function highlightNeighborhood(i){
    //console.log('i',i);
    neighborhood_features[i].element.setAttribute('stroke-opacity','.75');
    neighborhood_features[i].element.setAttribute('stroke-width','2px');
    neighborhood_features[i].element.setAttribute('stroke','#fff');
}

function unhighlightNeighborhood(i){
    neighborhood_features[i].element.setAttribute('stroke-opacity','0');
    //neighborhood_features[i].setAttribute('stroke','#fff');
};

function follow(e){

//    var myvalues = [10,8,5,7,4,4,1];
  //  $('.dynamicsparkline1').sparkline(myvalues) //why does this work here?
    console.log(e.target.offset);
    
    $('#tooltip').css({
        top: (e.offsetY || e.layerY) + "px",
        left: ((e.offsetX || e.layerX) + 15) + "px"
    });
}

function setsparkline(score,months){
      var monthly_values = [months[11],months[0],months[1],months[2],months[3],months[4]];
      $('.dynamicsparkline1').sparkline(monthly_values,{width:100}); //why does this work here?
}

function onload(e){
    var scores = [];

    var colorArray = ['#D92B04','#A61103'];
    
    for(var i = 0; i < e.features.length; i++) {
        var streetMouseOver = function(score,months, index){
            return function(evt){
              setStreetContent(evt,score,months,index);  
            };
        }(e.features[i].data.properties.score,e.features[i].data.properties.months,i);

        e.features[i].element.onmouseover = streetMouseOver;
        e.features[i].element.onmousemove = follow;
        e.features[i].element.onmouseout = hideStreetContent;
        

        if (e.features[i].data.properties.score < 600){
            e.features[i].element.setAttribute("stroke",colorArray[0]);
            e.features[i].element.setAttribute("stroke-opacity", 0.75);
        } else {
            e.features[i].element.setAttribute("stroke",colorArray[1]);
            e.features[i].element.setAttribute("stroke-opacity", 0.8);
        }


        e.features[i].element.setAttribute("stroke-linecap","round");
    }
}

function setStreetContent(e,score,months,index){
    //console.log('e',e);

    testNeighborhood(e);

    var myvalues = [10,8,5,7,4,4,1];
    $('.dynamicsparkline1').sparkline(myvalues);

    $('#tooltip').html('<strong>'+score+'</strong></br><span class="dynamicsparkline1">Loading..</span>');
    $('#tooltip').show();
    setsparkline(score,months);
}

function hideStreetContent(e){
    //this is not getting called
    testNeighborhood(e);

    $('#tooltip').hide();
}

var po = org.polymaps;

var color = pv.Scale.linear()
    .domain(0, 1, 5, 40)
    .range("#F00", "#930", "#FC0", "#3B0");

var map = po.map()
    .container(document.getElementById("map").appendChild(po.svg("svg")))
    .center({lat: 37.76, lon: -122.44})
    .zoom(13)
    .zoomRange([12, 17])
    .add(po.interact());

map.add(po.image()
    .url(po.url("http://{S}tile.cloudmade.com"
    + "/1a193057ca6040fca68c4ae162bec2da"
    + "/38747/256/{Z}/{X}/{Y}.png")
    .hosts(["a.", "b.", "c.", ""])));

//var density_map = po.image().url(po.url("http://ec2-184-73-13-139.compute-1.amazonaws.com:8888/1.0.0/open311_test/{Z}/{X}/{T}.png"));
var density_map = po.image().url(po.url("http://ec2-184-73-13-139.compute-1.amazonaws.com:8888/1.0.0/Open311_Density_Final/{Z}/{X}/{T}.png"));
map.add(density_map);

//http://ec2-184-73-13-139.compute-1.amazonaws.com:8888/1.0.0/open311_test/{Z}/{X}/{T}.png

//http://ec2-184-73-13-139.compute-1.amazonaws.com:8888/1.0.0/open311_test2_548404/{z}/{x}/{y}

//map.add(po.image().url(po.url("http://ec2-184-73-13-139.compute-1.amazonaws.com:8888/1.0.0/open311_test2_548404/{Z}/{X}/{T}.png")));

map.add(po.geoJson()
    .url("data/sf_polygons_geojson.json")
    .id("neighborhoods")
    .zoom(12)
    .tile(false)
    .on("load", onloadneighborhoods
    //.on("load", po.stylist()
    //.attr("stroke", function(d) { return color(d.properties.score).color; })
    //.title(function(d) { return d.properties.STREET + ": " + d.properties.PCI + " PCI"; })
    ));

map.add(po.geoJson()
    .url("data/scored_centerlines_sub_final.json")
    .id("streets")
    .zoom(12)
    .tile(false)
    .on("load", onload
    //.on("load", po.stylist()
    //.attr("stroke", function(d) { return color(d.properties.score).color; })
    //.title(function(d) { return d.properties.STREET + ": " + d.properties.PCI + " PCI"; })
    ));

map.add(po.compass()
    .pan("none"));
