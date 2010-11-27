


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
		"/status/ajax_public_posts/",
		function(data) {
		    $(data).appendTo($(".status-container"));
		    addRateLinkHandlers();
		});
    } 
}

function relative_time(time_value) {
   var parsed_date = Date.parse(time_value);

   var relative_to = (arguments.length > 1) ? arguments[1] : new Date();
   var delta = parseInt((relative_to.getTime() - parsed_date) / 1000);

   if(delta < 60) {
       return 'less than a minute ago';
   } else if(delta < 120) {
       return 'about a minute ago';
   } else if(delta < (45*60)) {
       return (parseInt(delta / 60)).toString() + ' minutes ago';
   } else if(delta < (90*60)) {
           return 'about an hour ago';
       } else if(delta < (24*60*60)) {
       return 'about ' + (parseInt(delta / 3600)).toString() + ' hours ago';
   } else if(delta < (48*60*60)) {
       return '1 day ago';
   } else {
       return (parseInt(delta / 86400)).toString() + ' days ago';
   }
}
