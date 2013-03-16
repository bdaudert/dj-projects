var MEDIA_URL = document.getElementById("MEDIA_URL").value;

function changeBackgroundColor(DivID) { 
            var backColor = new String(); 
            backColor = document.getElementById(DivID).style.background;
            // IE works with hex code of color e.g.: #FFFFFF 
            // Firefox works with rgb color code e.g.: rgb(255, 255, 255) 
            // Thats why both types are used in If-condition below 
            if (backColor.toLowerCase() == '#FFFFFF' || backColor.toLowerCase() == 'rgb(255, 255, 255)') { 
                document.getElementById(DivID).style.background = '#FF007F';
                //Turn all other  classes of the same type off off
                divs_to_turn_off =  document.getElementsByClassName("docu"); 
                for (div in divs_to_turn_off){   
                    if (div.style.display == 'block'){
                        div.style.display == 'none';
                    }
                } 
            } 
            else { 
                document.getElementById(DivID).style.background = '#FFFFFF'; 
            } 
        }
/* 
//Highlights node, hides and blurs all other elements of class DivClass
function HighLight(node,DivClass) {
    node.focus();
    //Turn all other  classes of the same type off off
    divs_to_turn_off = document.getElementsByClassName(DivClass);
    for (k in divs_to_turn_off.length; k++){
        if (divs_to_turn_off[k].style.display == "block"){
            divs_to_turn_off[k].style.display = "none";
        }
    qmarks_to_turn_off = document.getElementsByClassName("qmark");
    for (i in qmarks_to_turn_off.length:i++){ 
        if (qmarks_to_turn_of[i] != node){
            qmarks_to_turn_of[i].blur();
        }
    }
}
*/

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
  var moveLeft = 0.1;
  var moveDown = 0.1;

  $('.trigger').hover(function(e) {
    $(this).next('div.pop-up').show();
   //$('div.pop-up').show();
      //.css('top', e.pageY + moveDown)
      //.css('left', e.pageX + moveLeft)
      //.appendTo('body');
  }, function() {
    $(this).next('div.pop-up').hide();
  });
  /*
  $('.trigger').click(function(e) {
    //$(this).next('div.pop-up').css('top', e.pageY).css('left', e.pageX );
    $(this).next('div.pop-up').show().css('top', e.pageY - moveDown).css('left', e.pageX + moveLeft);
  });
  */
}); 

//TRY THIS
/*
$(function() {
  var moveLeft = 0.1;
  var moveDown = 0.1;

  $('.trigger').hover(function(e) {
    $(this).next('div.pop-up').show();
   //$('div.pop-up').show();
      //.css('top', e.pageY + moveDown)
      //.css('left', e.pageX + moveLeft)
      //.appendTo('body');
   }, function() {
    $(this).next('div.pop-up').hide();
  });
 
  $('.trigger').click(function(e) {
    //$(this).next('div.pop-up').css('top', e.pageY).css('left', e.pageX );
    $(this).next('div.pop-up').show().css('top', e.pageY - moveDown).css('left', e.pageX + moveLeft);
  }, function() {
    $(this).next('div.pop-up').hide();
  });
}); 
*/


function showIt(Id)
{
document.getElementById(Id).style.display="inline";
}


function hideIt(Id)
{
document.getElementById(Id).style.display='none';
}
