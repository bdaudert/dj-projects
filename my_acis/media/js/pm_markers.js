var po = org.polymaps;

var svg = document.getElementById("map").appendChild(po.svg("svg")),
    defs = svg.appendChild(po.svg("defs"));

/* Create three linear gradients for each category. */
defs.appendChild(gradient("#D90000", "#A30000")).setAttribute("id", "gradient-violent");
defs.appendChild(gradient("#23965E", "#1A7046")).setAttribute("id", "gradient-property");
defs.appendChild(gradient("#3489BA", "#27678B")).setAttribute("id", "gradient-quality");

/* Create a marker path.
defs.appendChild(icons.marker()).setAttribute("id", "marker");
*/


var map = po.map()
    .container(svg)
    .center({lat: 38.40, lon: -99.00})
    .zoomRange([1,16])
    .zoom(4.8)
    .add(po.interact());

map.add(po.image()
    .url(po.url("http://{S}tile.cloudmade.com"
    + "/1a1b06b230af4efdbb989ea99e9841af" // http://cloudmade.com/register
    + "/997/256/{Z}/{X}/{Y}.png")
    .hosts(["a.", "b.", "c.", ""])));


$.get("/media/json/CT_coop_stations.json", function(data) {
    map.add(po.geoJson().features(data.features))
    });

map.add(po.compass()
    .pan("none"));


/* Post-process the GeoJSON points and replace them with markers! */
function load(e) {
  e.features.sort(function(a, b) {
    return b.data.geometry.coordinates[1] - a.data.geometry.coordinates[1];
  });
  for (var i = 0; i < e.features.length; i++) {
    var f = e.features[i],
        d = f.data,
        c = f.element,
        p = c.parentNode,
        u = f.element = po.svg("use");
    u.setAttributeNS(po.ns.xlink, "href", "url(#marker)");
    p.removeChild(c);
    p.appendChild(u);
  }
}

/* Helper method for constructing a linear gradient. */
function gradient(a, b) {
  var g = po.svg("linearGradient");
  g.setAttribute("x1", 0);
  g.setAttribute("y1", 1);
  g.setAttribute("x2", 0);
  g.setAttribute("y2", 0);
  var s0 = g.appendChild(po.svg("stop"));
  s0.setAttribute("offset", "0%");
  s0.setAttribute("stop-color", a);
  var s1 = g.appendChild(po.svg("stop"));
  s1.setAttribute("offset", "100%");
  s1.setAttribute("stop-color", b);
  return g;
}
