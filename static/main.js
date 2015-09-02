var from, to, showfrom, showto;

function matchStation(s) {
    var output = [];    
    s = s.trim().toLowerCase();
    if (s.length===0) return output;
    for ( var i = 0; i < stations.length; i++) {
        var station = stations[i];
        if (station[1].toLowerCase().indexOf(s) != -1 || station[0] == s) {
           output.push(station);
        }
        if (output.length>5){return output;}
    }
    return output;
}

function autocomplete(field, output) {
    var stationAsLink = function (station){
        var a = document.createElement('a');
        var linkText = document.createTextNode(station[1]);
        a.appendChild(linkText);
        a.href = "#";
        a.onclick = function () { 
            field.value = station[1]; 
            output.innerHTML="";
        };
        return a;
    };

    var autocompleteListener = function() {
        var matches = matchStation(field.value);
        var links = matches.map(stationAsLink);
        output.innerHTML = "";
        if (links[0]) links[0].className="hi";
        for (var i=0; i < links.length; ++i) {
            output.appendChild(links[i]);
            output.appendChild(document.createTextNode(" "));
        };
        if (links.length>5) {output.appendChild(document.createTextNode("..."));}
    };

    field.addEventListener("input", autocompleteListener);
    autocompleteListener();
}

function setup(argument) {
    from = document.getElementById("from");
    to = document.getElementById("to");
    showfrom = document.getElementById("showfrom");
    showto = document.getElementById("showto");
    autocomplete(from, showfrom);
    autocomplete(to, showto);
}

function go(){
    var fromCRS = matchStation(from.value)[0][0];
    var toCRS = matchStation(to.value)[0][0];
    var when = document.getElementById("when").value;
    console.log(fromCRS, toCRS, when);
    window.location.href = "/view/"+fromCRS+"/"+toCRS+"/"+when;
}

document.addEventListener("DOMContentLoaded", setup);

