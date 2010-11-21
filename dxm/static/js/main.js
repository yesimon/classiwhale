


$(document).ready(function() {
    addRateLinkHandlers();
	autoRefreshStatuses();
});


function addRateLinkHandlers() {
	$(".status-container .like").click(rateLike);
	$(".status-container .dislike").click(rateDislike);
}


function autoRefreshStatuses() {
    setInterval("loadStatuses()", 5000);
}




function getFriendTimeline(user) {
    $.get(
        "/status/ajax_friend_timeline/",
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


function rate(kind, sid) {
    $.post(
        "/status/ajax_rate/", 
        { rating: kind, id: sid }
    );
}

function rateLike() {
    rate("up", $(this).closest(".entry").attr("id")); 	
    
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



function loadStatuses() {
	if ($(".status-container .entry").size() < 5) {
		$.get(
		"/status/ajax_recent_public_posts/",
		function(data) {
		    $(data).appendTo($(".status-container"));
		    addRateLinkHandlers();
		});
    } 
}
