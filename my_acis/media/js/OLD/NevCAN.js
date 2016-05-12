var xmlURL = document.getElementById('xmlURL')
var xmlhttp=false;
var xmlDoc;

if (!xmlhttp && typeof XMLHttpRequest!='undefined') {
    xmlhttp = new XMLHttpRequest();
}
if (!xmlhttp) {
    alert('This page requires a more modern web browser. Please upgrade your web browser.');
}

function getxml(){
    xmlhttp.open("GET", xmlURL+Math.random(),true);
    xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4) {
            xmlDoc = xmlhttp.responseXML;
        }
    }
    xmlhttp.send(null);
}
