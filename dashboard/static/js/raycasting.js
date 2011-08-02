var features_coordinates = []; //dom ready
var features_rect_bounds = [];
var neighborhood_features = [];
var highlighted = -1;

var tool_tip_up = false;

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
    var lon = [],
      lat = [],
      i;

    for(i = 0; i < e.features.length; i++) {

        neighborhood_features[i] = e.features[i];
        neighborhood_features[i].element.setAttribute('fill','#fff');
        neighborhood_features[i].element.setAttribute('fill-opacity','0');

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
    }
    highlighted = i;
    console.log('highlighted',highlighted);

};
var count = 0;

function highlightNeighborhood(i){
    neighborhood_features[i].element.setAttribute('style','stroke-width:1;stroke:#050505;stroke-opacity:.75;fill:#fff;fill-opacity:.4;');
}

function unhighlightNeighborhood(i){
    neighborhood_features[i].element.setAttribute('style','stroke-opacity:0;fill-opacity:0;');
};


function onload(e){
    var colorArray = ['#D92B04','#A61103'];

    for(var i = 0; i < e.features.length; i++) {
        //new
        e.features[i].element.setAttribute('fill-opacity',0);

        var streetMouseOver = function(score,start_street,end_street,street,months,top_request,index){
            return function(evt){
              setStreetContent(evt,score,start_street,end_street,street,months,top_request,index);  
            };
        }(e.features[i].data.properties.score,e.features[i].data.properties.RT_FADD,e.features[i].data.properties.RT_TOADD,e.features[i].data.properties.STREETN_GC,e.features[i].data.properties.months,e.features[i].data.properties.top_request_type,i);

        e.features[i].element.onmouseover = streetMouseOver;
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

function setStreetContent(e,score,start_street,end_street,street,months,top_request,index){
    testNeighborhood(e);
}

function hideStreetContent(e){
    testNeighborhood(e);
}

function onresponseload(e){
    var colorArray = ['#23677f','#15343f'];

    for(var i = 0; i < e.features.length; i++) {

        e.features[i].element.setAttribute('fill-opacity',0);

        var streetMouseOver = function(score,start_street,end_street,street,index){
            return function(evt){
              setResponseContent(evt,score,start_street,end_street,street,index);
            };
        }(e.features[i].data.properties.response_time,e.features[i].data.properties.RT_FADD,e.features[i].data.properties.RT_TOADD,e.features[i].data.properties.STREETN_GC,i);

        e.features[i].element.onmouseover = streetMouseOver;
        e.features[i].element.onmouseout = hideResponseContent;


        if (e.features[i].data.properties.response_time < 480){
            e.features[i].element.setAttribute("stroke",colorArray[0]);
            e.features[i].element.setAttribute("stroke-opacity", 0.65);
        } else {
            e.features[i].element.setAttribute("stroke",colorArray[1]);
            e.features[i].element.setAttribute("stroke-opacity", 0.7);
        }


        e.features[i].element.setAttribute("stroke-linecap","round");
    }
}

function setResponseContent(e,score,start_street,end_street,street){
    testNeighborhood(e);
}

function hideResponseContent(e){
    testNeighborhood(e);
}

var po = org.polymaps;

var map = po.map()
    .container(document.getElementById("map").appendChild(po.svg("svg")))
    .center({lat: 37.7516, lon: -122.44})
    .zoom(12)
    .zoomRange([12, 16])
    .add(po.interact());
map.add(po.hash());

//38747
//22677
map.add(po.image()
    .url(po.url("http://{S}tile.cloudmade.com"
    + "/1a193057ca6040fca68c4ae162bec2da"
    + "/39534/256/{Z}/{X}/{Y}.png")
    .hosts(["a.", "b.", "c.", ""])));

var response_time_map = po.image()
    .url(po.url("/static/tiles/{Z}/{X}/{Y}.png"));
map.add(response_time_map);
// response_time_map.visible(false);

var context_map = po.image()
    .url(po.url("http://{S}tile.cloudmade.com"
    + "/1a193057ca6040fca68c4ae162bec2da"
    + "/38965/256/{Z}/{X}/{Y}.png")
    .hosts(["a.", "b.", "c.", ""]));
map.add(context_map);
context_map.visible(false);

var sf_neighborhoods = po.geoJson()
    .url("/static/sf.json")
    .id("neighborhoods")
    .zoom(12)
    .tile(false)
    .on("load", onloadneighborhoods
    );
map.add(sf_neighborhoods);

var density_lines = po.geoJson()
    .url("/static/test.json")
    .id("streets")
    .zoom(12)
    .tile(false)
    .on("load", onload
    );

map.add(density_lines);
density_lines.visible(false);

var response_lines = po.geoJson()
    .url("/static/test.json")
    .id("responses")
    .zoom(12)
    .tile(false)
    .on("load", onresponseload
    );

map.add(response_lines);
// response_lines.visible(false);

map.add(po.compass()
    .pan("none"));

map.on("move", function(){if (map.zoom() >= 14) {
                                context_map.visible(true);
                            } else {
                                context_map.visible(false);
                            }});

