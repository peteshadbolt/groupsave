document.addEventListener("DOMContentLoaded", setup);

// TODO: just sort that station list in terms of frequency of use haha
function matchStation(s) {
    var output = [];    
    if (s.length==0) return output;
    for ( var i = 0; i < stations.length; i++) {
        var station = stations[i];
        if (station.name.toLowerCase().indexOf(s) != -1 || station.crs == s) {
           output.push(station.name);
        }
        if (output.length>5){return output;}
    }
    return output;
}

function updateFrom(args) {
    var search = this.value.trim().toLowerCase();
    var s = matchStation(search).join(" / ");

    //if (search.length<3) {
        //document.getElementById("showfrom").innerHTML="";
        //return;
    //}
    //var result = fuse.search(search);
    //var names = [];
    //for (var i=0; i < result.length; ++i) {
        //names.push(result[i].name);
    //}
    //var s = names.join(" / ");
    document.getElementById("showfrom").innerHTML = s;
}

function updateTo(args) {
    var search = this.value.trim();
    if (search.length<3) {
        document.getElementById("showto").innerHTML = "";
        return;
    }
    var result = fuse.search(search);
    var names = [];
    for (var i=0; i < result.length; ++i) {
        names.push(result[i].name);
    }
    var s = names.join(" / ");
    document.getElementById("showto").innerHTML = s;
}

function updateWhen(args) {
    var search = this.value.trim();
    var result = Date.parse(search);
    var s = result;
    document.getElementById("showwhen").innerHTML = s;
}

function setup(argument) {
    // Initiate fuse
    //fuse = new Fuse(stations, fuseOptions); 

    // Bind events
    document.getElementById('from').addEventListener("input", updateFrom);
    //document.getElementById('to').addEventListener("input", updateTo);
    //document.getElementById('when').addEventListener("input", updateWhen);
}

