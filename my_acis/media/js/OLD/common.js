/* 
   @function getElementsByClassName()
   To use:

   o  To get all a elements in the document with a info-links class.
       getElementsByClassName(document, "a", "info-links");

   o  To get all div elements within the element named container, with a col class.
       getElementsByClassName(document.getElementById("container"), "div", "col"); 

   o  To get all elements within in the document with a click-me class.
       getElementsByClassName(document, "*", "click-me"); 

*/

function getElementsByClassName(oElm, strTagName, strClassName){
    var arrElements = (strTagName == "*" && oElm.all)? oElm.all : oElm.getElementsByTagName(strTagName);
    var arrReturnElements = new Array();
    strClassName = strClassName.replace(/\-/g, "\\-");
    var oRegExp = new RegExp("(^|\\s)" + strClassName + "(\\s|$)");
    var oElement;
    for(var i=0; i<arrElements.length; i++){
        oElement = arrElements[i];      
        if(oRegExp.test(oElement.className)){
            arrReturnElements.push(oElement);
        }   
    }
    return (arrReturnElements)
}

/* 
    @function addLoadEvent()
    To use:

    o Named function
	addLoadEvent(nameOfSomeFunctionToRunOnPageLoad); Note: WITHOUT () on function name!

    o Anonymous function
	addLoadEvent(function() { });
*/

function addLoadEvent(func) {
  var oldonload = window.onload;
  if (typeof window.onload != 'function') {
    window.onload = func;
  } else {
    window.onload = function() {
      if (oldonload) {
        oldonload();
      }
      func();
    }
  }
} // End function addLoadEvent

function display_block(id) {
    obj = document.getElementById(id);
    obj.style.display = 'block';
}

function get_option_value(select) {
    for(var i=0; i<select.childNodes.length; i++)
    {
	option = select.childNodes[i];
	if (option.selected){
	    return option.value;
	}
    }
}

/*
json to string { return j.toJSONString(); }
string to json { return s.parseJSON(); }
*/
