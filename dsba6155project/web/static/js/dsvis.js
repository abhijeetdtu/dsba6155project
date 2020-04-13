var d3app = (function() {
  return {
    getData: function(callback) {
      d3.json("/d3data", {
          crossOrigin: "anonymous"
        })
        .then(data => {
          callback(data);
        })
    },
    createPop: function(d) {
      console.log(d)
      d3.select("#popup")
        .on("mouseover", function(d) {
          d3.select("#popup")
            .style("right", function() {
              sr = d3.select("#popup").style("right");
              if (sr == "" || sr == "70%") {
                return "5%"
              } else {
                return "70%"
              }
            })
        })
        .text(d["fullText"])
    },
    network: function() {
      d3app.getData(d3app._network)
      //d3app.getData(d3app.)
    },
    _network: function(data) {
      var graph = data;
      const width = 960;
      const height = 500;
      var radius = 6;
      var svg = d3.select("#appd3")
        .append("svg")
        .attr("viewBox", [0, 0, width, height])
        .attr("preserveAspectRatio", "xMidYMid meet")
        .style("width", "100vw")
        .style("height", "100vh");

      var color = d3.scaleOrdinal(d3.schemeCategory10);
      var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function(d) {
          return d.id;
        }))
        .force("charge", d3.forceManyBody().strength(-20))
        .force("forceX", function(d) {
          d3.forceX().strength(d.year)
        })
        .force("center", d3.forceCenter(width / 2, height / 2));


      var link = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(graph.links)
        .enter().append("line")
        .attr("stroke", function(d, i) {
          return color(i % 10)
        })
        .attr("stroke-width", function(d) {
          return Math.sqrt(d.value);
        });

      var node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("g")
        .data(graph.nodes)
        .enter().append("g")

      var circles = node.append("circle")
        .attr("r", function(d) {
          return d["totalLinks"]
        })
        .attr("fill", function(d, i) {
          return color(d["group"] % 10);
        })
        .on("mouseover", d3app.createPop)
        .attr("data-legend", function(d) {
          return d.groupName
        })
        .attr("data-legend-color", function(d,i) {
          return color(d["group"] % 10)
        })
        .call(d3.drag()
          .on("start", d3app.dragstarted)
          .on("drag", d3app.dragged)
          .on("end", d3app.dragended));

      // var  legend = svg.append("g")
      //     .attr("class", "legend")
      //     .attr("transform", "translate(50,30)")
      //     .style("font-size", "12px")
      //     .call(d3.legend)
      //
      // var legend = svg.append("g")
      //   .attr("class", "legend")
      //   .attr("transform", "translate(150,130)")
      //   .style("font-size", "12px")
      //   .call(d3.legend)

      var lables = node.append("text")
        .text(function(d) {
          return d.id;
        })
        .attr("fill", "white")
        .attr("font-size", function(d) {
          return d["totalLinks"] + "%"
        })
        .attr('x', 6)
        .attr('y', 3);

      node.append("title")
        .text(function(d) {
          return d.id;
        });

      simulation
        .nodes(graph.nodes)
        .on("tick", ticked);

      simulation.force("link")
        .links(graph.links);

      function ticked() {

        node
          .attr("transform", function(d) {
            d.x = Math.max(radius, Math.min(width - radius, d.x));
            d.y = Math.max(radius, Math.min(height - radius, d.y));
            return "translate(" + d.x + "," + d.y + ")";
          })

        // node.attr("cx", function(d) { return  })
        //     .attr("cy", function(d) { return });

        link.attr("x1", function(d) {
            return d.source.x;
          })
          .attr("y1", function(d) {
            return d.source.y;
          })
          .attr("x2", function(d) {
            return d.target.x;
          })
          .attr("y2", function(d) {
            return d.target.y;
          });
      }
    },
    ptest: function() {

      d3app.getData(function(data) {
        data = data.sort(function(a, b) {
          if (a["startDate"] > b["startDate"]) {
            return 1
          }
          return -1
        })

        d3.select("#appd3")
          .selectAll("div")
          .data(data)
          .enter()
          .append("div")
          //.style("width" ,function(d,i){return Math.round(Math.random()*50) + 50 + "%" })
          .attr("class", function(d, i) {
            return "col-md-" + (i % 1 + 1)
          })
          .append("span")
          .text(function(d) {
            if ("startDate" in d) {
              return d["startDate"].split(" ")[0]
            }
          })
          .append("img")
          .style("width", "100%")
          .style("border-radius", "50%")
          .style("max-height", "50px")
          .style("max-width", "50px")
          .attr("src", function(d) {
            if ("media" in d) {
              return d["media"][0]["src"]
            }
          })
          .text(function(d) {
            return d.id
          })
      })

    },
    dragstarted: function(d) {
      if (!d3.event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    },

    dragged: function(d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    },

    dragended: function(d) {
      if (!d3.event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    },
    _sankeyChart: function(data) {
      graph = data
      var margin = {
          top: 10,
          right: 10,
          bottom: 10,
          left: 10
        },
        width = 960 - margin.left - margin.right,
        height = 5000 - margin.top - margin.bottom;

      // append the svg object to the body of the page
      var svg = d3.select("#appd3").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

      // Color scale used
      var color = d3.scaleOrdinal(d3.schemeCategory10);

      // Set the sankey diagram properties
      var sankey = d3.sankey()
        .nodeWidth(36)
        .nodePadding(290)
        .size([width, height]);

      var path = sankey.link();

      // load the data
      // Constructs a new Sankey generator with the default settings.
      sankey
        .nodes(graph.nodes)
        .links(graph.links)
      //.layout(1);

      // add in the links
      var link = svg.append("g")
        .selectAll(".link")
        .data(graph.links)
        .enter()
        .append("path")
        .attr("class", "link")
        .attr("d", path)
        .style("stroke-width", function(d) {
          return Math.max(1, d.dy);
        })
        .sort(function(a, b) {
          return b.dy - a.dy;
        });

      // add in the nodes
      var node = svg.append("g")
        .selectAll(".node")
        .data(graph.nodes)
        .enter().append("g")
        .attr("class", "node")
        .attr("transform", function(d) {
          return "translate(" + d.x + "," + d.y + ")";
        })
        .call(d3.drag()
          .subject(function(d) {
            return d;
          })
          .on("start", function() {
            this.parentNode.appendChild(this);
          })
          .on("drag", dragmove));

      // add the rectangles for the nodes
      node
        .append("rect")
        .attr("height", function(d) {
          return d.dy;
        })
        .attr("width", sankey.nodeWidth())
        .style("fill", function(d) {
          return d.color = color(d.name.replace(/ .*/, ""));
        })
        .style("stroke", function(d) {
          return d3.rgb(d.color).darker(2);
        })
        // Add hover text
        .append("title")
        .text(function(d) {
          return d.name + "\n" + "There is " + d.value + " stuff in this node";
        });

      // add in the title for the nodes
      node
        .append("text")
        .attr("x", -6)
        .attr("y", function(d) {
          return d.dy / 2;
        })
        .attr("dy", ".35em")
        .attr("text-anchor", "end")
        .attr("transform", null)
        .text(function(d) {
          return d.name;
        })
        .filter(function(d) {
          return d.x < width / 2;
        })
        .attr("x", 6 + sankey.nodeWidth())
        .attr("text-anchor", "start");

      // the function for moving the nodes
      function dragmove(d) {
        d3.select(this)
          .attr("transform",
            "translate(" +
            d.x + "," +
            (d.y = Math.max(
              0, Math.min(height - d.dy, d3.event.y))) + ")");
        sankey.relayout();
        link.attr("d", sankey.link());
      }
    }
  }
})()
