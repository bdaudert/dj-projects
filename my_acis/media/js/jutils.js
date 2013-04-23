//Highlights node by setting border, hides  all elements of class DivClass
//and unsets the boder of all other nodes of same class type
function HighLight(node,DivClass,DivId) {
    //node is qmark, DivId is corresponding docu;
    var div_to_show = document.getElementById(DivId)
    var divs_to_hide = document.getElementsByClassName(DivClass);
    var NodeClassName = node.className
    var nodes_to_blur= document.getElementsByClassName(NodeClassName);
    if (node.style.border != "none"){
        //HIDE
        //turn off this qmark
        node.style.border = "none";
        //turn off of the corresponding div
        div_to_show.style.display = "none";
    }
    else {
        //SHOW
        node.style.border ="4px solid #FF007F";
        //Unborder all other nodes of same class name
        for (i=0;i<nodes_to_blur.length;i++){     
            if (nodes_to_blur[i] != node){
                //qmarks_to_turn_off[i].blur();
                nodes_to_blur[i].style.border="none";
            }
            else{
                nodes_to_blur[i].style.border="4px solid #FF007F";
            }
        }
        //Hide all divs with class name DivClass except show the one of id=DivId 
        for (i=0;i<divs_to_hide.length;i++){
            if (divs_to_hide[i] != div_to_show){
                divs_to_hide[i].style.display ="none";
            }
            else{
                divs_to_hide[i].style.display ="block";
            }
        }
    }
}

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
    }
    var href;
    if (typeof(mylink) == 'string')
    {
        href=mylink;
    }
    else
    {
        href=mylink.href;
    }
    //var height = 800;
    //var width = 800;
    var height = window.height - 50;
    var width = window.width - 50;
    window.open(href, windowname, 'width=' + width + ',height=' + height + ',scrollbars=yes');
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
  }, function() {
    $(this).next('div.pop-up').hide();
  });
  //$(this).next('div.pop-up').css('top', e.pageY).css('left', e.pageX );
  // $(this).next('div.pop-up').show().css('top', e.pageY - moveDown).css('left', e.pageX + moveLeft);
  //});
  $('.trigger').click(function(e) {
    var display = $(this).next('div.pop-up').css('display');
    if (display != 'none') {
        $(this).next('div.pop-up').css('display','none');
    }
    else {
        $(this).next('div.pop-up').css('display','block');
    }
  });
    /*
    $(this).next('div.pop-up').css("display","block");
  }, function() {
    $(this).next('div.pop-up').css("display","none");
  });
    */
}); 


function showIt(Id)
{
document.getElementById(Id).style.display="inline";
}


function hideIt(Id)
{
document.getElementById(Id).style.display='none';
}
