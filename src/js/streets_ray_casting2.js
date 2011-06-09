var features_coordinates = []; //dom ready
var features_rect_bounds = [];
var neighborhood_features = [];
var highlighted = -1;
var $neighborhoodStats = $('#result_data');

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

    
    for (i=0; i<neighborhood_features.length; i++) {
      if (neighborhood_features[i].data.properties.rank === 1) {
        updateNeighborhoodStats(neighborhood_features[i]);
        break;
      }
    }
}

function updateNeighborhoodStats(feature) {
  var i, 
    html = '<div class="neighborhood-title">'+feature.data.properties.neighborhood+'</div>' + 
      '<table><tr><th class="stats-key">Total</th><th class="stats-val">Rank</th></tr>' + 
      '<tr class="total-stats-row"><td class="stats-key">'+feature.data.properties.total+'</td><td class="stats-val stats-rank">'+feature.data.properties.rank+'</td></tr>' + 
      '<tr><th class="stats-key">Request</th><th class="stats-val">Total</th></tr>';
    
    for (i=feature.data.properties.top_five.length-1; i>=0; i--) {
      html += '<tr><td class="stats-key">'+feature.data.properties.top_five[i][0]+'</td><td class="stats-val">'+feature.data.properties.top_five[i][1]+'</td></tr>';
    }
    
    html += '</table>';

  $neighborhoodStats.html(html);
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
    neighborhood_features[i].element.setAttribute('stroke-width','1px');
    //neighborhood_features[i].element.setAttribute('stroke','#3d3d3d');
    neighborhood_features[i].element.setAttribute('stroke','#050505');
    neighborhood_features[i].element.setAttribute('fill','#fff');
    neighborhood_features[i].element.setAttribute('fill-opacity','.4');
}

function unhighlightNeighborhood(i){
    neighborhood_features[i].element.setAttribute('stroke-opacity','0');
    neighborhood_features[i].element.setAttribute('fill-opacity','0');
    //neighborhood_features[i].setAttribute('stroke','#fff');
};

function follow(e){    
    $('#tooltip').css({
        top: (e.offsetY || e.layerY) + "px",
        left: ((e.offsetX || e.layerX) + 15) + "px"
    });
}

function setsparkline(score,months){
      var monthly_values = [months[11],months[0],months[1],months[2],months[3],months[4]];
      $('.dynamicsparkline1').sparkline(monthly_values,{width:100,fillColor:false,lineColor:"#336699",minSpotColor:"#990000",maxSpotColor:"#990000",spotColor:"#990000",lineWidth:1}); //why does this work here?
}

function setbarchart(score){
       //range is an array: range[0],range[1],range[2],range[3],range[4],range[5]

        range = [93,75,68,62,57,67];
        
        if (score < 96){
            cMap = ["red","green","green","green","green","green"];
        } else if (score < 192) {
            cMap = ["green","red","green","green","green","green"];
        } else if (score < 288) {
            cMap = ["green","green","red","green","green","green"];
        } else if (score < 384) {
            cMap = ["green","green","green","red","green","green"];
        } else if (score < 480){
            cMap = ["green","green","green","green","red","green"];
        } else {
            cMap = ["green","green","green","green","green","red"];
        };
       
      $('.dynamicbarchart').sparkline(range,{type:'bar',width:100,barSpacing:1,barWidth:5,colorMap:cMap}); //why does this work here?
}

function onload(e){
    var colorArray = ['#D92B04','#A61103'];
    
    for(var i = 0; i < e.features.length; i++) {
        var streetMouseOver = function(score,start_street,end_street,street,months,top_request,index){
            return function(evt){
              setStreetContent(evt,score,start_street,end_street,street,months,top_request,index);  
            };
        }(e.features[i].data.properties.score,e.features[i].data.properties.RT_FADD,e.features[i].data.properties.RT_TOADD,e.features[i].data.properties.STREETN_GC,e.features[i].data.properties.months,e.features[i].data.properties.top_request_type,i);

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

function setStreetContent(e,score,start_street,end_street,street,months,top_request,index){
    //console.log('e',e);

    testNeighborhood(e);


    if (map.zoom() >= 14){

        if (score < 600){
            score = 'Top 10%';
        } else {
            score = 'Top 5%';
        }
    
    $('#tooltip').html('<span id="dyn_title">'+parseInt(start_street,10) +' - ' + parseInt(end_street,10) + ' ' + street+'</span>' +
        '<div id="dens_score"><strong> '+score+'</strong></div>' +
        '<div id="sparkline_descrip">Total Requests ' +
            '<span class="dynamicsparkline1">Loading..</span>' +
            '<span id="month_color"> '+months[4] + ' </span>' +
            'during May 2011</span>' +
        '</div>' +
        '<div id="top_request">Top Request: <strong>'+top_request[1]+'</strong></div>');

        $('#tooltip').show();
    }
    
    setsparkline(score,months);
}

function hideStreetContent(e){
    testNeighborhood(e);
 
    //$('#tooltip').fadeOut(200);
    //tool_tip_up = false;
    //$('#streets path:hover').css({'stroke-width':'1.5px'});
    $('#tooltip').hide();
}

function onresponseload(e){
    var colorArray = ['#23677f','#15343f'];
    
    for(var i = 0; i < e.features.length; i++) {
        var streetMouseOver = function(score,start_street,end_street,street,index){
            return function(evt){
              setResponseContent(evt,score,start_street,end_street,street,index);  
            };
        }(e.features[i].data.properties.response_time,e.features[i].data.properties.RT_FADD,e.features[i].data.properties.RT_TOADD,e.features[i].data.properties.STREETN_GC,i);

        e.features[i].element.onmouseover = streetMouseOver;
        e.features[i].element.onmousemove = follow;
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

    if (map.zoom() >= 14){

        var barColors = '';


        if (score < 96){
            barColors = '6EAFCF|DBDBDB|DBDBDB|DBDBDB|DBDBDB|DBDBDB';
        } else if (score < 192) {
            barColors = 'DBDBDB|6EAFCF|DBDBDB|DBDBDB|DBDBDB|DBDBDB';
        } else if (score < 288) {
            barColors = 'DBDBDB|DBDBDB|6EAFCF|DBDBDB|DBDBDB|DBDBDB';
        } else if (score < 384) {
            barColors = 'DBDBDB|DBDBDB|DBDBDB|6EAFCF|DBDBDB|DBDBDB';
        } else if (score < 480){
            barColors = 'DBDBDB|DBDBDB|DBDBDB|DBDBDB|6EAFCF|DBDBDB';
        } else {
            barColors = 'DBDBDB|DBDBDB|DBDBDB|DBDBDB|DBDBDB|6EAFCF';
        }

        24,4,2,1,1,2
        
        $('#tooltip').html('<span id="dyn_title">'+parseInt(start_street,10) +' - ' + parseInt(end_street,10) + ' ' + street + '</span><br><span id="top_request">Average Response Time: <strong>'+Math.floor(score/24)+' days</strong></span><br><span class="gbar"><img class="gbar" src=\'http://chart.apis.google.com/chart?chxl=0:||Fast|||Slow&chxs=0,676767,9,0,l,676767|1,FFFFFF,0,0,_,FFFFFF&chxt=x,y&chbh=a&chs=100x60&cht=bvg&chco=' + barColors + '&chds=0,50&chd=t:192,32,16,8,8,16&chma=|0,5&chtt=Response+Times&chts=676767,9\' width="100" height="60"></span>');

        $('#tooltip').show();
    };
}

function hideResponseContent(e){
    testNeighborhood(e);
    $('#tooltip').hide();
}

var po = org.polymaps;

var map = po.map()
    .container(document.getElementById("map").appendChild(po.svg("svg")))
    .center({lat: 37.76, lon: -122.44})
    .zoom(12)
    .zoomRange([12, 16])
    .add(po.interact());
map.add(po.hash());

map.add(po.image()
    .url(po.url("http://{S}tile.cloudmade.com"
    + "/1a193057ca6040fca68c4ae162bec2da"
    + "/38747/256/{Z}/{X}/{Y}.png")
    .hosts(["a.", "b.", "c.", ""])));

var response_time_map = po.image().url(po.url("http://ec2-184-73-13-139.compute-1.amazonaws.com:8888/1.0.0/open311_response_times_final_345d14/{Z}/{X}/{T}.png"));
map.add(response_time_map);
response_time_map.visible(false);

var density_map = po.image().url(po.url("http://ec2-184-73-13-139.compute-1.amazonaws.com:8888/1.0.0/Open311_Density_Final_f3fe0d/{Z}/{X}/{T}.png"));
map.add(density_map);


var context_map = po.image()
    .url(po.url("http://{S}tile.cloudmade.com"
    + "/1a193057ca6040fca68c4ae162bec2da"
    + "/38965/256/{Z}/{X}/{Y}.png")
    .hosts(["a.", "b.", "c.", ""]));
map.add(context_map);
context_map.visible(false);

var sf_neighborhoods = map.add(po.geoJson()
    .url("data/sf_polygons_geojson_final.json")
    .id("neighborhoods")
    .zoom(12)
    .tile(false)
    .on("load", onloadneighborhoods
    ));

var density_lines = po.geoJson()
    .url("data/scored_centerlines_sub_final.json")
    .id("streets")
    .zoom(12)
    .tile(false)
    .on("load", onload
    );

map.add(density_lines);
var response_lines = po.geoJson()
    .url("data/avg_response_times_sub.json")
    .id("responses")
    .zoom(12)
    .tile(false)
    .on("load", onresponseload
    );

map.add(response_lines);
response_lines.visible(false);

map.add(po.compass()
    .pan("none"));

map.on("move", function(){if (map.zoom() >= 14) { 
                                context_map.visible(true);
                            } else { 
                                context_map.visible(false);
                            }});
