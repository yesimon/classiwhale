$(document).ready(function() {
    addRateLinkHandlers();
});

/* Hotkeys reenabled*/
$(document).keydown(function(event) {
    if(shouldUseHotkeys()) {
        if (event.keyCode == 74) { // 'j'
	    hotkeyRateLike();
        }
        if (event.keyCode == 75) { // 'k'
            hotkeyRateDislike();
        }
        if (event.keyCode == 85) { // 'u'
            hotkeyPrevEntry();
        }
    }
});

function shouldUseHotkeys() {
	if (window.$is_post_form_focused == undefined) {
		return true;
	}
    return !$is_post_form_focused;
}


function hotkeyPrevEntry() {
    activeEntry = $(".entry-active");
    var statusHeight = activeEntry.height();
    prevEntry = activeEntry.prev();
    if (prevEntry.length == 0) return;
    activeEntry.removeClass("entry-active");
    prevEntry.addClass("entry-active");
    $("html, body").animate({"scrollTop":-200 + prevEntry.offset().top + "px"});
    
}

function hotkeyRateLike() {
    activeEntry = $(".entry-active");
    if (activeEntry.length == 0) {
        $(".status:first").addClass("entry-active");
		$("html, body").animate({"scrollTop":-200 + $(".status:first").offset().top + "px"});
        return;
    }
    nextEntry = activeEntry.next();

    entry = activeEntry.closest(".status");
    rate("up", entry.attr("data-id")); 	
    likeButton = entry.find(".like");
    likeButton.next().removeClass('active');
    likeButton.next().addClass('inactive');
    likeButton.addClass('active');
    likeButton.removeClass('inactive');

    computeScroll(nextEntry, activeEntry, true);
}

function computeScroll(next, active, down) {
    console.log(next);
    if (next.length != 0) {
        var statusHeight = active.height();
        active.removeClass("entry-active");
        next.addClass("entry-active");
		if (down) {
  			$("html, body").animate({"scrollTop":-200 + next.offset().top + "px"});
		}
    }
}

function hotkeyRateDislike() {
    activeEntry = $(".entry-active");
    if (activeEntry.length == 0) {
        $(".status:first").addClass("entry-active");
        return;
    }
    nextEntry = activeEntry.next();
        
    entry = activeEntry.closest(".status");
    rate("down", entry.attr("data-id")); 
    dislikeButton = entry.find(".dislike");
    dislikeButton.prev().removeClass('active');
    dislikeButton.prev().addClass('inactive');
    dislikeButton.addClass('active');
    dislikeButton.removeClass('inactive');	
	activeEntry.fadeOut('medium', function(){
		    computeScroll(nextEntry, activeEntry, true);		
			activeEntry.remove();
	});
}

function addRateLinkHandlers() {
	$(".status-container .like").unbind('click').click(rateLike);
	$(".status-container .dislike").unbind('click').click(rateDislike);
}

function rate(kind, status){
    $.post(
        "/status/ajax_rate/", 
        { rating: kind, status: status }, 
	function(data) {
	    
	    /* var photo = $(".whale-photo")[0];
	    if (photo.src != data.species) {
		photo.src = data.species;
		setWhaleProgress(data.exp, data['min-exp'], data['max-exp']);
		}*/
	    }
    );
}

function rateLike() {
    entry = $(this).closest(".status");

    activeEntry = $(".entry-active");
    rate("up", entry.attr("data-id"));

    /* if ($(this).hasClass('inactive') && $(this).next().hasClass('inactive'))
    {
	setWhaleProgress(whaleExp++, minExp, maxExp);
	}*/

    $(this).next().removeClass('active');
    $(this).next().addClass('inactive');
    
    $(this).addClass('active');
    $(this).removeClass('inactive');

    activeEntry.removeClass("entry-active");
    entry.addClass("entry-active");

   


    return false;
}

function rateDislike() {
    entry = $(this).closest(".status");
    rate("down", entry.attr("data-id"));
    activeEntry = $(".entry-active");
 
    /*    if ($(this).hasClass('inactive') && $(this).next().hasClass('inactive'))
    {
	setWhaleProgress(whaleExp++, minExp, maxExp);
	}*/

    $(this).prev().removeClass('active');
    $(this).prev().addClass('inactive');
    
    $(this).addClass('active');
    $(this).removeClass('inactive');

    activeEntry.removeClass("entry-active");
    entry.addClass("entry-active");

    entry.fadeOut('medium', function(){
	    entry.remove();
	});


    return false;	
}
