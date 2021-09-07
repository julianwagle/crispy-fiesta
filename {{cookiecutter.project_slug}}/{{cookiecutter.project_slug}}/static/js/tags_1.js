$(document).ready(function() {
    if(!$('#myCanvas').tagcanvas({
      textColour : '#335EEA',
      outlineThickness : 0.7,
      outlineColour : '#506690',
      maxSpeed : 0.06,
      freezeActive:true,
      shuffleTags:true,
      shape:'sphere',
      zoom:0.8,
      wheelZoom:true,
      noSelect:true,
      freezeDecel:true,
      fadeIn:3000,
      initial: [0.3,-0.1],
      depth : 1.1
    },'tags')) {
      // something went wrong, hide the canvas container
      $('#myCanvasContainer').hide();
    }
  });
