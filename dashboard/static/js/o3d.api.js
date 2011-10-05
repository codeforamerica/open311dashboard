// API Namespace.
o3d.API = {};

o3d.API.query = {};

o3d.API.buildPage = function loadStats() {
  // Load top request types.
  $.get('/api/requests/count/?' + $.param(o3d.API.query) + '&page_size=10&sort=-count&keys=service_name',
    function (data) {
      $("#top-requests-table tbody").html('');
      for (var i = 0; i < data.length; i += 1) {
        var tmp_data = "<tr>";
        tmp_data += "<td>" + data[i]['service_name'].replace(/_/g, ' ') + "</td>";
        tmp_data += "<td>" + parseInt(data[i]['count']) + "</td>";
        tmp_data += "</tr>";
        $('#top-requests-table').append(tmp_data);
      }
  });

  // Load open request count.
  $.get('/api/requests/count/?'+$.param(o3d.API.query) + '&status=Open&keys=status',
    function(data){
      $('#open-request-value').html(data[0].count);
  });

  // Load average response.
  $.get('/api/requests/avg_response/?'+$.param(o3d.API.query),
    function(data) {
      $("#average-response-value").html(o3d.time.ms2human(data.avg_time));
  });

  // Load the map data.
  $.get('/api/requests/?'+$.param(o3d.API.query)+'&status=Open&page_size=10&sort=-requested_datetime',
    function(data) {
      var points = [];
      $("#requests table tbody").html('');

      for (var i = 0; i < data.length; i += 1) {
        // Generate the rows.
        var tmp_data = "<tr id=\""+data[i]['service_request_id']+ "-row\">";
        tmp_data += "<td>" + data[i]['service_request_id']+ "</td>";
        tmp_data += "<td>" + data[i]['service_name']+ "</td>";
        tmp_data += "<td>" + data[i]['status'] + "</td>";

        var requested_date = new Date(data[i]['requested_datetime']['$date']);

        tmp_data += "<td>" + requested_date.toString('MMM d, yyyy') + "</td>";
        tmp_data += "</tr>";
        $("#requests table tbody").append(tmp_data);

        // Push the features onto an array.
        points.push({ "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": data[i]['coordinates']
          }, "properties" : {
            "id": data[i]['service_request_id']
          }
        });

        // Show or hide points.
        $("#"+data[i]['service_request_id']+"-row").hover(function() {
          var sri = this.id.split('-')[0];
          $('#'+sri+"-point").show();
        }, function() {
          var sri = this.id.split('-')[0];
          $('#'+sri+"-point").hide();
        });
      }

      var loadPoints = function (e) {
        // Load the points, set the ID, class, and hide.
        for (var i = 0; i < e.features.length; i += 1) {
          e.features[i].element.id = e.features[i].data.properties.id + "-point";
          $(e.features[i].element).attr('class', 'request-point');
          $(e.features[i].element).hide();
        }
      }

      // Add the features.
      map.add(po.geoJson()
        .features(points)
        .id("points")
        .on("load", loadPoints));

  });
}
