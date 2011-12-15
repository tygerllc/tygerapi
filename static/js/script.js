canvas = $("bench");
$(canvas).attr("width", $(document).width() - $("#sidebar").width());
$(canvas).attr("height", $(document).height() - $("header").height()-4);

$(".drop-down-container").each(function(){
	var distance = 11;
    var time = 250;
    var hideDelay = 500;

    var hideDelayTimer = null;

    var beingShown = false;
    var shown = false;
    
    var trigger = $(this);
    var popup = $('.drop-down-menu', this).css('opacity', 0);

    $(trigger,popup).mouseover(function(){
    	if (hideDelayTimer) clearTimeout(hideDelayTimer);

    	if (beingShown || shown) {
        	return;
      	} 
      	else {
	        beingShown = true;
	        popup.css({
	          top: 30,
	          display: 'block'
	        }).animate({
	          top: '+=' + distance + 'px',
	          opacity: 1
	        }, time, 'swing', function() {

	          beingShown = false;
	          shown = true;
	        });
    	}   	
    }).mouseout(function () {

      if (hideDelayTimer) clearTimeout(hideDelayTimer);
      
      hideDelayTimer = setTimeout(function () {
        hideDelayTimer = null;
        popup.animate({
          top: '+=' + distance + 'px',
          opacity: 0
        }, time, 'swing', function () {

          shown = false;
          popup.css('display', 'none');
        });

      }, hideDelay);

    });
});






















