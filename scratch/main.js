var fuse;

var fuseOptions = {
  caseSensitive: false,
  includeScore: false,
  shouldSort: true,
  threshold: 0.1,
  location: 0,
  distance: 100,
  maxPatternLength: 32,
  keys: ["name"]
};

document.addEventListener("DOMContentLoaded", setup);

function updateFrom(args) {
    console.log(args);
    var search = $(this).val().trim();
    if (search.length<3) {
        document.getElementById("showfrom").innerHTML="";
        return;
    }
    var result = fuse.search(search);
    var names = [];
    for (var i=0; i < result.length; ++i) {
        names.push(result[i].name);
    }
    var s = names.join(" / ");
    document.getElementById("showfrom").innerHTML = s;
}

function updateTo(args) {
    var search = $(this).val().trim();
    if (search.length<3) {
        document.getElementById("showto").text("");
        return;
    }
    var result = fuse.search(search);
    var names = [];
    for (var i=0; i < result.length; ++i) {
        names.push(result[i].name);
    }
    var s = names.join(" / ");
    document.getElementById("showto").text(s);
}

function updateWhen(args) {
    var search = $(this).val().trim();
    var result = Date.parse(search);
    var s = result;
    document.getElementById("showwhen").text(s);
}

function setup(argument) {
    // Initiate fuse
    fuse = new Fuse(stations, fuseOptions); 

    // Bind events
    document.getElementById('from').addEventListener("change", updateFrom);
    document.getElementById('to').addEventListener("change", updateTo);
    document.getElementById('when').addEventListener("change", updateWhen);
}

