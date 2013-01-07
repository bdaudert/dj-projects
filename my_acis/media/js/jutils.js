var MEDIA_URL = document.getElementById("MEDIA_URL").value;

function Toggle(node)
{
	// Unfold the branch if it isn't visible
	if (node.nextSibling.style.display == 'none')
	{
		// Change the image (if there is an image)
		if (node.children.length > 0)
		{
			if (node.children.item(0).tagName == "img")
			{
				node.children.item(0).src = MEDIA_URL + "img/minus.gif";
			}
		}

		node.nextSibling.style.display = '';
	}
	// Collapse the branch if it IS visible
	else
	{
		// Change the image (if there is an image)
		if (node.children.length > 0)
		{
			if (node.children.item(0).tagName == "img")
			{
				node.children.item(0).src = MEDIA_URL + "img/plus.gif"; 
			}
		}

		node.nextSibling.style.display = 'none';
	}

}



function popup_window(mylink, windowname)
{
	if (! window.focus)
	{
		return true;
		var href;
	}
	if (typeof(mylink) == 'string')
	{
		href=mylink;
	}
	else
	{
		href=mylink.href;
	}
	window.open(href, windowname, 'width=400,height=200,scrollbars=yes');
	return false;
}

// [client side code for showing/hiding content]
function ShowHide(divId)
{
        obj = document.getElementById(divId);
        if (obj.style.display == 'none')
        {
                obj.style.display = 'block';
        } 
        else 
        {
                obj.style.display = 'none';
        }
}


$(function() {
  var moveLeft = 50;
  var moveDown = 0;

  $('.trigger').hover(function(e) {
    $(this).next('div.pop-up').show();
   //$('div.pop-up').show();
      //.css('top', e.pageY + moveDown)
      //.css('left', e.pageX + moveLeft)
      //.appendTo('body');
  }, function() {
    $(this).next('div.pop-up').hide();
  });

  $('.trigger').mousemove(function(e) {
    //$('div.pop-up').css('top', e.pageY + moveDown).css('left', e.pageX + moveLeft);
    $(this).next('div.pop-up').css('top', e.pageY + moveDown).css('left', e.pageX + moveLeft);
  });

}); 


function showIt(Id)
{
document.getElementById(Id).style.display="inline";
}


function hideIt(Id)
{
document.getElementById(Id).style.display='none';
}


function initialize_grid_point_map() {
    var map;
    var center_lat = document.getElementById("center_lat").value;
    var center_lon = document.getElementById("center_lon").value;
    var zoom_level = document.getElementById("zoom_level").value;
    var myLatlng = new google.maps.LatLng(center_lat,center_lon);
    var mapOptions = {
    //center: ll,
    center: myLatlng,
    zoom: 4,
    mapTypeId: google.maps.MapTypeId.HYBRID
    };
    map = new google.maps.Map(document.getElementById("map"),mapOptions);
    infowindow = new google.maps.InfoWindow({
        content: 'oi'
    });
    
    var marker = new google.maps.Marker({
        draggable: true,
        position: myLatlng, 
        map: map,
        title: "Your location"
    });

    google.maps.event.addListener(marker, 'click', function (event) {
        infowindow.close();
        var contentString = '<div id="MarkerWindow">'+
            '<p><b>Lat: </b>' + event.latLng.lat() + '<br/>'+
            '<b>Lon: </b>' + event.latLng.lng() + '<br/>' +
            '<a href="/my_data/apps/climate/grid_point_time_series/?lat=' + 
            event.latLng.lat() + '&lon=' + event.latLng.lng() + 
            '">Use this location</a></div>';
        infowindow.setContent(contentString);
        infowindow.open(map, marker);
        document.getElementById("latbox").value = event.latLng.lat();
        document.getElementById("lonbox").value = event.latLng.lng();
        myLatlng = google.maps.LatLng(event.latLng.lat(),event.latLng.lng());
    });
}//close initialize_grid_point_map 


function initialize_station_finder() {

    var MEDIA_URL = document.getElementById("MEDIA_URL").value;
    var json_file = document.getElementById("json_file").value;
    $.getJSON(MEDIA_URL + 'json/' + json_file, function(data) {


        //for (first in data.stations) var ll = new google.maps.LatLng(first.lat,first.lon);
        var ll = new google.maps.LatLng(data.stations[0].lat, data.stations[0].lon);
        var mapOptions = {
        center: ll,
        //center: new google.maps.LatLng(39.8282, -98.5795),
        zoom: 7,
        mapTypeId: google.maps.MapTypeId.HYBRID
        };

        map = new google.maps.Map(document.getElementById("map"),mapOptions);
        var bounds=new google.maps.LatLngBounds();
        infowindow = new google.maps.InfoWindow({
            content: 'oi'
        });
        var markers = [];
        $.each(data.stations, function(index, c) {
            var latlon = new google.maps.LatLng(c.lat,c.lon);
            var marker = new google.maps.Marker({
                map: map,
                position: latlon,
                title:'Name:'+c.name
            });

            markers.push(marker)
            bounds.extend(latlon);

            google.maps.event.addListener(marker, 'click', function() {
                infowindow.close();
                var contentString = '<div id="MarkerWindow">'+
                '<p><b>Name: </b>' + c.name + '<br/>'+
                '<b>State: </b>' + c.state + '<br/>' +
                '<b>UID: </b>' + c.uid + '<br/>' +
                '<b>SIDS: </b>' + c.sids + '<br/>' +
                '<b>Elevation: </b>' + c.elevation + '<br/>' +
                '</p>' +
                '<a href="/my_data/data/historic/?stn_id=' + c.sids[0] + 
                '">Get Data for this Station</a> <br/>'+
                '<a href="/my_data/apps/climate/?stn_id=' + c.sids[0] + 
                '">Run a climate application for this Station</a>'+ 
                '</div>';
                infowindow.setContent(contentString);
                infowindow.open(map, marker);
                });
        });//close each
    
        var markerCluster = new MarkerClusterer(map, markers);
        map.fitBounds(bounds);
    });//close getjson
}//close initialize_station_finder

function load_script() {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = "http://maps.googleapis.com/maps/api/js?key=AIzaSyDIdA3G_Mv7P7OV9jqX2rzChCFu-ut23n0&sensor=false&callback=initialize_map";
  $(".center").append(script);
  //document.body.appendChild(script)
  //document.getElementById("map_js").appendChild(script)
}
