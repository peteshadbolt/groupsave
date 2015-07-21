function start(){
    var settings = { enableHighAccuracy: true, timeout: timeoutVal, maximumAge: 0 };
    if (navigator.geolocation) {
      var timeoutVal = 10 * 1000 * 1000;
      navigator.geolocation.getCurrentPosition(
        displayPosition, 
        displayError,
        settings
      );
    }
    else {
      alert("Geolocation is not supported by this browser");
    }
}

function displayPosition(position) {
  $("#output").fadeIn(500);

  setTimeout(function(){
    $("#output-text").html("We found 1 other person...");
  }, 3000);

  setTimeout(function(){
    $("#output-text").html("We found 2 other people...");
  }, 8000);

  setTimeout(function(){
    $("#output-text").html("We found 3 other people! Go and meet them at Costa!");
    $("#spinner").hide();
    $("#costa").fadeIn(500);
  }, 12000);

}

function displayError(error){
  alert(error);
}
