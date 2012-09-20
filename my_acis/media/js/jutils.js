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
    $('div.pop-up').hide();
});
$(function() {
  var moveLeft = 50;
  var moveDown = 0;

  $('a.trigger').hover(function(e) {
    $(this).next('div.pop-up').show();
   //$('div.pop-up').show();
      //.css('top', e.pageY + moveDown)
      //.css('left', e.pageX + moveLeft)
      //.appendTo('body');
  }, function() {
    $(this).next('div.pop-up').hide();
  });

  $('a.trigger').mousemove(function(e) {
    //$('div.pop-up').css('top', e.pageY + moveDown).css('left', e.pageX + moveLeft);
    $(this).next('div.pop-up').css('top', e.pageY + moveDown).css('left', e.pageX + moveLeft);
  });

}); 

//Testing popup in same window
function toggle(div_id) {
    var el = document.getElementById(div_id);
    if ( el.style.display == 'none' ) { el.style.display = 'block';}
    else {el.style.display = 'none';}
}

function window_pos(popUpDivVar) {
    if (typeof window.innerWidth != 'undefined') {
        viewportwidth = window.innerHeight;
    } else {
        viewportwidth = document.documentElement.clientHeight;
    }
    if ((viewportwidth > document.body.parentNode.scrollWidth) && (viewportwidth > document.body.parentNode.clientWidth)) {
        window_width = viewportwidth;
    } else {
        if (document.body.parentNode.clientWidth > document.body.parentNode.scrollWidth) {
            window_width = document.body.parentNode.clientWidth;
        } else {
            window_width = document.body.parentNode.scrollWidth;
        }
    }
    var popUpDiv = document.getElementById(popUpDivVar);
    window_width=window_width/2-150;//150 is half popup's width
    popUpDiv.style.left = window_width + 'px';
}

function popup(windowname) {
    window_pos(windowname);
    toggle(windowname);     
}
//End test
