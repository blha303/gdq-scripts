//Set up on-click listeners.

$(document).ready(function() {
  for(var i=0; i < 25; i++){
    $("#bg" +i).click({param1:i}, toggle);
  }

  function toggle(event){
    if ($('#bg'+event.data.param1).css("backgroundColor")=="rgb(255, 255, 255)"){
      $('#bg'+event.data.param1).css("backgroundColor", "rgb(255, 128, 128)");
    }
    else{
      $('#bg'+event.data.param1).css("backgroundColor", "white");
    }
  }
});
