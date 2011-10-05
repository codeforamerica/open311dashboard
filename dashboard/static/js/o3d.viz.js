/**
 * o3d.viz.js
 * @author Chris Barna <chris@unbrain.net>
 **/

// Visualizations namespace.
o3d.viz = {};

o3d.viz.sparkline = function (sparkData, id, w, h) {
  var x = d3.scale.linear().domain([0, sparkData.length - 1]).range([0, w]);
  var y = d3.scale.linear().domain([0, d3.max(sparkData)]).range([h, 0]);
  var max = d3.max(sparkData);
  var min = d3.min(sparkData);

  var vis = d3.select(id)
    .append("svg:svg")
      .attr("width", w + 40)
      .attr("height", h + 40)
    .append("svg:g")
        .attr("transform", "translate(" + 20 + ", " + 20 + ")");

  var new_circles = vis.selectAll("circle.area")
    .data(sparkData)
    .enter().append("svg:circle");

  var line = d3.svg.line()
    .x(function (d, i) {
      return x(i);
    })
    .y(function (d) {
      return y(d);
    })
    .interpolate("cardinal");

  //appending the line
  var initial_path = vis.append("svg:path").attr("d", line(sparkData)).attr("stroke-linecap", "round");

  var initial_circles = vis.selectAll("circle.area")
    .data(sparkData)
    .enter().append("svg:circle")
    .attr("class", function (d, i) {
      if (d === max) {
        return 'point max';
      } else if (d === min) {
        return 'point';
      } else {
        return 'point';
      }
    })
    .attr("cx", function (d, i) {
      return x(i);
    })
    .attr("cy", function (d, i) {
      return y(d);
    })
    .attr("r", function (d) {
      if (d === max) {
        return 3.5;
      } else {
        return 0;
      }
    });
};

