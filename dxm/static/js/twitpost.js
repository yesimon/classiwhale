function twitpost(status) {
    if(status.length == 0) {
        alert("You haven't entered any text");
    } else {
        $.post(
	    "/status/post/",
            { status: status },
	    function(data) {
	       handleTwitResponse(data);
	    }
	       );
    }
}

function handleTwitResponse(data) {
    if(data.success == "True") {
	location.reload(true);
    } else {
        alert("Whoops, looks like Twitter is fail whaling");
    }
}