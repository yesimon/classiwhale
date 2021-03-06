pageType = null;
$loading = null;
pageIndex = null;
opts = null;
maxid = null;
waypointInterval = null;
numStatuses = null;

$(document).ready(function() {
    $('#loginButton').click(function(){
        $.oauthpopup({
            path: '/twitterauth/login/popup/',
	    callback: function(){
		window.location.replace("/");
		}
	    });
        });
    // $('a.track').click(linktrack());

    if(numStatuses) ajaxTimelineHandlers();
});


function linktrack() {
    $.post('/status/linktrack/', {text:this.text});
    return true;
}

function ajaxTimelineHandlers(){
    $loading = $("<div class='loading'><p>Loading more items&hellip;</p><img src='/static/img/spinner.gif'></img></div>");

    opts = {
        offset: function() {
            return $.waypoints('viewportHeight') - $(this).outerHeight() + 200;
        },
    }

    if (numStatuses == 0) {
        pageIndex = 1;
        $(".statuses").append($loading);
        ajaxGetTimeline(null);
    }
    else {
        pageIndex = 2;
    }

    $("#statuses_end").waypoint(ajaxWaypointCallback, opts);
}


function ajaxWaypointCallback(event, direction) {
    maxid = $(".status:last").attr("data-id");
	$("#statuses_end").waypoint('remove');
    $(".statuses").append($loading);
    ajaxGetTimeline(null);
    //    waypointInterval = window.setInterval(ajaxGetTimeline, 1000);
}

function ajaxGetTimeline(data){
    $.get("/status/ajax_timeline/", {page: pageIndex, id: maxid, timeline: pageType}, function(data) {
            if (data == 'Loading') {
                return;
            }
            if (data != '') {
                // window.clearInterval(waypointInterval);
                $loading.detach();
                pageIndex++;
                $(".statuses").append(data);
                addRateLinkHandlers();
                $("#statuses_end").waypoint(opts);
            }
        });
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
