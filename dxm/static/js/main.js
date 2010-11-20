


$(document).ready(function() {
    addRateLinkHandlers();
	autoRefreshStatuses();
});


function getFriendTimeline(user) {
    $.get(
        "{% url status.views.ajax_friend_timeline %}",
        { screenname: $.trim(user.text()) },
        function(data) {
            $(".statuses").remove();
            $(data).hide().appendTo($(".status-container")).fadeIn();
        }
    );
}

function addFriendTimelineHandlers() {
    $(".friend-container .user").click(
    	function(e) {
    	    e.preventDefault();
    	    getFriendTimeline($(this));
    	}
    );
}


function rate(kind, foundid) {
    $.post(
        "{% url status.views.ajax_rate %}", 
        { rating: kind, id: foundid }
    );
}

function rateLike() {
    rate("up", $(this).closest(".entry").attr("id")); 
    //$(this).siblings().hide();
    //$(this).closest(".entry").slideUp('', moveToRatings);	
    
    $(this).next().removeClass('active');
    $(this).next().addClass('inactive');
    
    $(this).addClass('active');
    $(this).removeClass('inactive');
    return false;
}

function rateDislike() {
    rate("down", $(this).closest(".entry").attr("id")); 
    //$(this).siblings().hide();
    //$(this).closest(".entry").slideUp('', moveToRatings);
    
    $(this).prev().removeClass('active');
    $(this).prev().addClass('inactive');
    
    $(this).addClass('active');
    $(this).removeClass('inactive');
    return false;	
}

function addRateLinkHandlers() {
	$(".status-container .like").click(rateLike);
	$(".status-container .dislike").click(rateDislike);
}

function moveToRatings() {
    //$(this).prependTo($(".rating-container>.ratings")).slideDown();
}

function loadStatuses() {
	if ($(".status-container .entry").size() < 5) {
		$.get(
		"{% url status.views.ajax_recent_public_posts %}",
		function(data) {
		    $(data).appendTo($(".status-container"));
		    addRateLinkHandlers();
		});
    } 
}

function autoRefreshStatuses() {
    setInterval("loadStatuses()", 5000);
}
