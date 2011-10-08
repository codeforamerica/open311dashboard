/**
 * o3d.viz.js
 * @author Chris Barna <chris@unbrain.net>
 **/

// Visualizations namespace.
o3d.viz = {};

o3d.viz.sparkline = function (sparkData, id, w, h) {
  var max = d3.max(sparkData);

  if (max === 0) {
    max = 10;
  }

  var x = d3.scale.linear().domain([0, sparkData.length - 1]).range([20, 35+w]);
  var y = d3.scale.linear().domain([0, max]).range([h, 0]);
  var min = d3.min(sparkData);

  var vis = d3.select(id)
    .append("svg:svg")
      .attr("width", w + 40)
      .attr("height", h+20)
    .append("svg:g")
        .attr("transform", "translate(" + 0 + ", " + 10 + ")");

  // Ticks
  var ticks = vis.selectAll('.ticks')
    .data(y.ticks(3));

  ticks
    .enter()
    .append("svg:g")
      .attr("class", "ticks")
    .append("svg:line")
      .attr("x1", 15)
      .attr("x2", w+40)
      .attr("y1", function(d) { return  y(d); })
      .attr("y2", function(d) { return  y(d); });

  ticks.append("svg:text")
    .attr("y", function(d) { return y(d) + 3; })
    .attr("x", 10)
    .attr("text-anchor", "middle")
    .text(function (d) { return d; });

  var line = d3.svg.line()
    .x(function (d, i) {
      return x(i);
    })
    .y(function (d) {
      return y(d);
    })
    .interpolate("cardinal").tension(0.8);

  //appending the line
  var initial_path = vis.append("svg:path").attr("d", line(sparkData)).attr("stroke-linecap", "round");

  var initial_circles = vis.selectAll("circle.area")
    .data(sparkData)
    .enter().append("svg:circle")
    .attr("class", function (d, i) {
      if (d === max) {
        return 'point max';
      } else if ((d === min)) {
        return 'point';
      } else {
        return 'point';
      }
    })
    .attr("cx", function (d, i) {  return x(i);  })
    .attr("cy", function (d, i) {  return y(d);  })
    .attr("r", function (d) {
      if ((d === max)) {
        return 3.5;
      } else {
        return 0;
      }
    });



};

// Pie chart for the status.
o3d.viz.status_pie = function (data, id, size) {
  var radius = size / 2;
  var color = d3.scale.category20c();

  var viz = d3.select(id)
    .append("svg:svg")
    .attr("width", size)
    .attr("height", size)
    .data([data])
    .append("svg:g")
    .attr("transform", "translate(" + radius + "," + radius + ")");

  var arc = d3.svg.arc()
    .outerRadius(radius);

  var pie = d3.layout.pie()
    .value(function(d) {  return d.count; });

  var arcs = viz.selectAll('g.slice')
    .data(pie)
    .enter()
    .append("svg:g")
    .attr("class", "slice")
    .on("mousemove", function (d, i) { 
        var selector = "#top-requests-info";
        $(selector).show();
        $(selector).css({
          position: "absolute",
          top: (d3.event.pageY - 5) + "px",
          left: (15+(d3.event.pageX)) + "px"
        });
        $(selector).html("<strong>"+d.data.status.replace(/_/g, ' ')+":</strong> "+d.data.count);
      })
      .on("mouseout", function() {
        $("#top-requests-info").hide();
      });

  arcs.append("svg:path")
    .attr("fill", function(d, i) { return color(i); })
    .attr("d", arc);
};

o3d.viz.top_requests_histo = function (data, id, width, height) {
  var leftPadding = 40;
  var verticalPadding = 5;
  var chartHeight = height - verticalPadding;
  var x = d3.scale.linear().domain([0, data.length]).range([0, width-leftPadding]);
  var y = d3.scale.linear().domain([0, d3.max(data,function(d) { return d.count; })])
    .range([0, height- (2*verticalPadding)]);
  var barWidth = (width - leftPadding) / data.length;
  var color = d3.scale.category20c();

  var viz = d3.select(id)
    .append("svg:svg")
    .attr("width", width)
    .attr("height", height + 100)
    .append("svg:g");
    // .data([data])

  // Ticks
  var ticks = viz.selectAll('.ticks')
    .data(y.ticks(4));

  ticks
    .enter()
    .append("svg:g")
      .attr("class", "ticks")
    .append("svg:line")
      .attr("x1", leftPadding - 5)
      .attr("x2", width)
      .attr("y1", function(d) { return chartHeight - y(d); })
      .attr("y2", function(d) { return chartHeight - y(d); });

  ticks.append("svg:text")
    .attr("y", function(d) { return chartHeight - y(d)+3; })
    .attr("x", leftPadding - 8)
    .attr("text-anchor", "end")
    .text(function (d) { return d; });

  // Bars.
  var bars = viz.selectAll('rect')
    .data(data, function (d) { return d.count; });

  bars.enter()
    .append("svg:g")
      .attr("class", "bar")
    .append("svg:rect")
      .attr("x", function (d, i) { return i * barWidth + leftPadding; })
      .attr("y", function (d) { return chartHeight - y(d.count); })
      .attr("width", barWidth - 5)
      .attr("height", function (d) { return y(d.count); })
      .attr("fill", function(d, i) { return color(i); })
      .on("mousemove", function (d, i) { 
        var selector = "#top-requests-info";
        $(selector).show();
        $(selector).css({
          position: "absolute",
          top: ((d3.event.pageY) - 5) + "px",
          left: (15+d3.event.pageX) + "px"
        });
        $(selector).html("<strong>"+d.service_name.replace(/_/g, ' ')+":</strong> "+d.count);
      })
      .on("mouseout", function() {
        $("#top-requests-info").hide();
      });

  // Labels
  bars.append("svg:g")
    .append("svg:text")
    .attr("text-anchor", "end")
    .attr("class", "graph-label")
    .attr("transform", function (d, i) {
      var text_x = (i*barWidth+leftPadding+(barWidth/2));
      var text_y = (chartHeight+5);
      return "scale(1, 1) rotate(290,"+text_x+", "+ text_y +") translate(" + text_x + ", " + text_y + ")";
    })
    .text(function(d) {
      if(d.service_name.length > 20) {
        d.service_name = d.service_name.substring(0,19)+"...";
      }

      return d.service_name.replace(/_/g, ' ');
    });

  // y-axis
  viz.append("svg:line")
    .attr("x1", leftPadding - 4)
    .attr("x2", leftPadding - 4)
    .attr("y1", chartHeight)
    .attr("y2", verticalPadding)
    .attr("class", "axis");
};
