$(document).ready(function() {
    addRateLinkHandlers();
});


/* Hotkeys disabled for now
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
*/

function shouldUseHotkeys() {
	if(window.$is_post_form_focused == undefined) return true;
    return !$is_post_form_focused;
}

function hotkeyPrevEntry() {
    activeEntry = $(".entry-active");
    prevEntry = activeEntry.prev();
    if (prevEntry.length == 0) return;
    activeEntry.removeClass("entry-active");
    prevEntry.addClass("entry-active");
    $.scrollTo(prevEntry);
}

function hotkeyRateLike() {
    activeEntry = $(".entry-active");
    if (activeEntry.length == 0) {
        $(".status:first").addClass("entry-active");
        return;
    }
    nextEntry = activeEntry.next();

    entry = activeEntry.closest(".status");
    rate("up", entry.attr("data-status")); 	
    likeButton = entry.find(".like");
    likeButton.next().removeClass('active');
    likeButton.next().addClass('inactive');
    likeButton.addClass('active');
    likeButton.removeClass('inactive');

    computeScroll(nextEntry, activeEntry);
}

function computeScroll(next, active) {
    console.log(next);
    if (next.length != 0) {
        active.removeClass("entry-active");
        next.addClass("entry-active");
        $.scrollTo(next);
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
    rate("down", entry.attr("data-status")); 
    dislikeButton = entry.find(".dislike");
    dislikeButton.prev().removeClass('active');
    dislikeButton.prev().addClass('inactive');
    dislikeButton.addClass('active');
    dislikeButton.removeClass('inactive');

    computeScroll(nextEntry, activeEntry);
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
	    setWhaleProgress(data.exp, data['min-exp'], data['max-exp']);
	    var photo = $(".whale-photo")[0];
	    if (photo.src != data.species)
		photo.src = data.species;
	}
    );
}

function rateLike() {
    entry = $(this).closest(".status");
    rate("up", entry.attr("data-status"));

    $(this).next().removeClass('active');
    $(this).next().addClass('inactive');
    
    $(this).addClass('active');
    $(this).removeClass('inactive');
    return false;
}


function rateDislike() {
    entry = $(this).closest(".status");
    rate("down", entry.attr("data-status"));
    
    $(this).prev().removeClass('active');
    $(this).prev().addClass('inactive');
    
    $(this).addClass('active');
    $(this).removeClass('inactive');
    return false;	
}
