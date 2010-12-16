$(document).ready(function() {
    addRateLinkHandlers();
});



$(document).keydown(function(event) {
    if (event.keyCode == 74) { // 'j'
        hotkeyRateLike();
    }
    if (event.keyCode == 75) { // 'k'
        hotkeyRateDislike();
    }
    if (event.keyCode == 85) { // 'u'
        hotkeyPrevEntry();
    }

});

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
        $(".entry:first").addClass("entry-active");
        return;
    }
    nextEntry = activeEntry.next();

    entry = activeEntry.closest(".entry");
    rate("up", entry.attr("id")); 	
    likeButton = entry.find(".like");
    likeButton.next().removeClass('active');
    likeButton.next().addClass('inactive');
    likeButton.addClass('active');
    likeButton.removeClass('inactive');
 
    if (nextEntry.length != 0) {
        activeEntry.removeClass("entry-active");
        nextEntry.addClass("entry-active");
        $.scrollTo(nextEntry);
    }

}

function hotkeyRateDislike() {
    activeEntry = $(".entry-active");
    if (activeEntry.length == 0) {
        $(".entry:first").addClass("entry-active");
        return;
    }
    nextEntry = activeEntry.next();
        
    entry = activeEntry.closest(".entry");
    rate("down", entry.attr("id")); 
    dislikeButton = entry.find(".dislike");
    dislikeButton.prev().removeClass('active');
    dislikeButton.prev().addClass('inactive');
    dislikeButton.addClass('active');
    dislikeButton.removeClass('inactive');

    if (nextEntry.length != 0) {
        activeEntry.removeClass("entry-active");
        nextEntry.addClass("entry-active");
        $.scrollTo(nextEntry);
    }

}


function addRateLinkHandlers() {
	$(".status-container .like").click(rateLike);
	$(".status-container .dislike").click(rateDislike);
}


function rate(kind, sid, text, created_at) {
    $.post(
        "/status/ajax_rate/", 
        { rating: kind, id: sid, text: text, created_at: created_at }
    );
}

function rateLike() {
    entry = $(this).closest(".entry");
    rate("up", entry.attr("id"), entry.attr("data-text"), entry.attr("data-created_at")); 	
    
    $(this).next().removeClass('active');
    $(this).next().addClass('inactive');
    
    $(this).addClass('active');
    $(this).removeClass('inactive');
    return false;
}


function rateDislike() {
    entry = $(this).closest(".entry");
    rate("down", entry.attr("id"), entry.attr("data-text"), entry.attr("data-created_at"));
    //$(this).siblings().hide();
    //$(this).closest(".entry").slideUp('', moveToRatings);
    
    $(this).prev().removeClass('active');
    $(this).prev().addClass('inactive');
    
    $(this).addClass('active');
    $(this).removeClass('inactive');
    return false;	
}
