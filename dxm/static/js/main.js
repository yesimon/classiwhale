/**
 * jQuery.ScrollTo - Easy element scrolling using jQuery.
 **/
;(function(d){var k=d.scrollTo=function(a,i,e){d(window).scrollTo(a,i,e)};k.defaults={axis:'xy',duration:parseFloat(d.fn.jquery)>=1.3?0:1};k.window=function(a){return d(window)._scrollable()};d.fn._scrollable=function(){return this.map(function(){var a=this,i=!a.nodeName||d.inArray(a.nodeName.toLowerCase(),['iframe','#document','html','body'])!=-1;if(!i)return a;var e=(a.contentWindow||a).document||a.ownerDocument||a;return d.browser.safari||e.compatMode=='BackCompat'?e.body:e.documentElement})};d.fn.scrollTo=function(n,j,b){if(typeof j=='object'){b=j;j=0}if(typeof b=='function')b={onAfter:b};if(n=='max')n=9e9;b=d.extend({},k.defaults,b);j=j||b.speed||b.duration;b.queue=b.queue&&b.axis.length>1;if(b.queue)j/=2;b.offset=p(b.offset);b.over=p(b.over);return this._scrollable().each(function(){var q=this,r=d(q),f=n,s,g={},u=r.is('html,body');switch(typeof f){case'number':case'string':if(/^([+-]=)?\d+(\.\d+)?(px|%)?$/.test(f)){f=p(f);break}f=d(f,this);case'object':if(f.is||f.style)s=(f=d(f)).offset()}d.each(b.axis.split(''),function(a,i){var e=i=='x'?'Left':'Top',h=e.toLowerCase(),c='scroll'+e,l=q[c],m=k.max(q,i);if(s){g[c]=s[h]+(u?0:l-r.offset()[h]);if(b.margin){g[c]-=parseInt(f.css('margin'+e))||0;g[c]-=parseInt(f.css('border'+e+'Width'))||0}g[c]+=b.offset[h]||0;if(b.over[h])g[c]+=f[i=='x'?'width':'height']()*b.over[h]}else{var o=f[h];g[c]=o.slice&&o.slice(-1)=='%'?parseFloat(o)/100*m:o}if(/^\d+$/.test(g[c]))g[c]=g[c]<=0?0:Math.min(g[c],m);if(!a&&b.queue){if(l!=g[c])t(b.onAfterFirst);delete g[c]}});t(b.onAfter);function t(a){r.animate(g,j,b.easing,a&&function(){a.call(this,n,b)})}}).end()};k.max=function(a,i){var e=i=='x'?'Width':'Height',h='scroll'+e;if(!d(a).is('html,body'))return a[h]-d(a)[e.toLowerCase()]();var c='client'+e,l=a.ownerDocument.documentElement,m=a.ownerDocument.body;return Math.max(l[h],m[h])-Math.min(l[c],m[c])};function p(a){return typeof a=='object'?a:{top:a,left:a}}})(jQuery);



$(document).ready(function() {
    addRateLinkHandlers();
//	autoRefreshStatuses();

    $(window).infinitescroll({
    url: "/status/ajax_training_set_posts/",
    page: 2,
    appendTo: ".statuses",
    });
});

var lock_GetTrainingPosts = false;

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


function autoRefreshStatuses() {
    setInterval("loadStatuses()", 5000);
    setInterval("loadTrainingStatuses()", 5000);
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
    entry = $(this).closest(".entry");
    rate("up", entry.attr("id")); 	
    
    $(this).next().removeClass('active');
    $(this).next().addClass('inactive');
    
    $(this).addClass('active');
    $(this).removeClass('inactive');
    return false;
}


function rateDislike() {
    entry = $(this).closest(".entry");
    rate("down", entry.attr("id")); 
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
		    $(data).appendTo($(".statuses"));
		    addRateLinkHandlers();
		});
    } 
}

function loadTrainingStatuses() {
    if (lock_GetTrainingPosts == true) return;
	if ($(".status-container .like:not(.active, .inactive)").size() < 10) {
        lock_GetTrainingPosts = true;
		$.get(
		"/status/ajax_training_set_posts/",
		function(data) {
		    $(data).appendTo($(".statuses"));
		    addRateLinkHandlers();
            lock_GetTrainingPosts = false;
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
