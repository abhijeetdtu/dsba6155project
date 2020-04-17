var d3bubbleForce = (function() {

  svgId = "#appd3"
  width = 960
  height = 700
  radius = 5
  ticked = function() {
    // bubbles
    //   .attr('cx', d => d.x)
    //   .attr('cy', d => d.y)

    bubbles
      .attr("transform", function(d) {
        d.x = Math.max(radius, Math.min(width - radius, d.x));
        d.y = Math.max(radius, Math.min(height - radius, d.y));
        return "translate(" + d.x + "," + d.y + ")";
      })

    labels
      .attr('x', d => d.x)
      .attr('y', d => d.y)
  }

  return {
    getData: function(callback) {
      d3.json("/d3bookdata/PERSON", {
          crossOrigin: "anonymous"
        })
        .then(data => {
          callback(data);
        })
    },
    createNodes: function(rawData) {
      // use max size in the data as the max in the scale's domain
      // note we have to ensure that size is a number
      console.log(rawData)
      const maxSize = d3.max(rawData, d => +d.count);

      // size bubbles based on area
      const radiusScale = d3.scaleSqrt()
        .domain([0, maxSize])
        .range([0, 80])

      // use map() to convert raw data into node data
      const myNodes = rawData.map(d => ({
        radius: radiusScale(+d.count),
        size: +d.count,
        x: Math.random() * 900,
        y: Math.random() * 800,
        text: d.text,
        category: d.category
      }))

      return myNodes;
    },
    prepareSimulation: function() {
      function charge(d) {
        return Math.pow(d.radius, 2.0) * 0.01
      }
      centre = {
        x: width / 2,
        y: height / 2
      };
      forceStrength = 0.03;
      simulation = d3.forceSimulation()
        .force('charge', d3.forceManyBody().strength(charge))
        // .force('center', d3.forceCenter(centre.x, centre.y))
        .force('x', d3.forceX().strength(forceStrength).x(centre.x))
        .force('y', d3.forceY().strength(forceStrength).y(centre.y))
        .force('collision', d3.forceCollide().radius(d => d.radius + 1));

      return simulation;
    },
    draw: function() {
      d3bubbleForce.getData(function(data) {
        heirarchy = d3.hierarchy({children: data}).sum(d => d.count);
        pack = d3.pack(data).size([width, height])
        root = pack(heirarchy)

        color = d3.scaleOrdinal(data.map(d => d.category), d3.schemeCategory10)
        const svg = d3.select(svgId)
          .append("svg")
          .attr("viewBox", [0, 0, width, height])
          .attr("width", width)
          .attr("height", height)
          .attr("font-size", 10)
          .attr("font-family", "sans-serif")
          .attr("text-anchor", "middle");

        const leaf = svg.selectAll("g")
          .data(root.leaves())
          .join("g")
          .attr("transform", d => `translate(${d.x + 1},${d.y + 1})`);

        leaf.append("circle")
          //.attr("id", d => (d.leafUid = DOM.uid("leaf")).id)
          .attr("r", d => d.r)
          .attr("fill-opacity", 0.7)
          .attr("fill", d => color(d.data.category));

        // leaf.append("clipPath")
        //   //.attr("id", d => (d.clipUid = DOM.uid("clip")).id)
        //   .append("use")
        //   //.attr("xlink:href", d => d.leafUid.href);
        //
        leaf.append("text")
            .attr('dy', '.3em')
            .style('text-anchor', 'middle')
            .style('font-size', 10)
            .text(function(d){
              console.log(d)
              return d.data.text;
            })

      })
    }

  }
})()
