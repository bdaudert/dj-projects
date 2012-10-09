var po = org.polymaps;

var svg = document.getElementById("map").appendChild(po.svg("svg")),
    defs = svg.appendChild(po.svg("defs"));


/*Create a marker pat */
defs.appendChild(icons.marker()).setAttribute("id", "marker");

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
    map.add(po.geoJson().features(data.features)).on("load", load)
    });

map.add(po.compass()
    .pan("none"));


/* Post-process the GeoJSON points and replace them with markers! */
function load(e) {
  e.features.sort(function(a, b) {
    return b.data.geometry.coordinates[1] - a.data.geometry.coordinates[1];
  });
  var r = 20 * Math.pow(2, e.tile.zoom - 12);
  for (var i = 0; i < e.features.length; i++) {
    var f = e.features[i],
        d = f.data,
        c = f.element,
        p = f.parentNode,
        point = c.appendChild(po.svg("circle"));
        
        point.setAttribute("cx", d.geometry.coordinates[0]);
        point.setAttribute("cy", d.geometry.coordinates[1]);
        point.setAttribute("r", r); 
        
  }
}
    /*
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
*/
