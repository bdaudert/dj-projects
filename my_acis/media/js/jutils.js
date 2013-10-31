
function populateFormField(form_name, form_id, label, value){
    //var formFields = document.getElementById(form_name).getElementsByTagName('input');
    var formFields = document.getElementById(form_id).getElementsByTagName('input');
    for (i=0;i<formFields.length;i++){
        if (formFields[i].name == label) {
            formFields[i].value =value;
        }
    }   
}


function precise_round(num,decimals){
    return Math.round(num*Math.pow(10,decimals))/Math.pow(10,decimals);
}

function printNode(ID){
  var NodeToPrint=document.getElementById(ID);
  newWin= window.open("");
  newWin.document.write(NodeToPrint.outerHTML);
  newWin.print();
  newWin.close();
}


//Highlights node by setting border, hides  all elements of class DivClass
//and unsets the boder of all other nodes of same class type
function HighLight(node,DivClass,DivId) {
    //node is qmark, divclass is 'docu', DivId is corresponding docu;
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
        node.style.border ="4px solid #006666";
        //Unborder all other nodes of same class name
        for (i=0;i<nodes_to_blur.length;i++){     
            if (nodes_to_blur[i] != node){
                //qmarks_to_turn_off[i].blur();
                nodes_to_blur[i].style.border="none";
            }
            else{
                nodes_to_blur[i].style.border="4px solid #006666";
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

function ShowPopupDocu(DivId){
    $( '#' + DivId ).dialog();
}

function ShowHelpText(divId){
    var pop_up = document.createElement('div');
    pop_up.setAttribute("class", "pop-up");
    pop_up.setAttribute("id", 'help_' + divId);
    pop_up.innerHTML = $("#" + 'help_' + divId).load("/csc/media/html/commons.html #" + divId );
    //$( "#"+divId ).show();
    if (pop_up.style.display == "none"){
        pop_up.style.display = "block";
    }
    else{
        pop_up.style.display = "none";
    }
    document.body.appendChild(pop_up);
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

//Shows documentation in pop up box upon hover
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
