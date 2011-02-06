function twitpost(status) {
    if(status.length == 0) {
    	$('.status-post .status-post-alert').replaceWith('<span class="status-post-alert"> Please enter a message </span>');
    	$('#postinput').focus();
    	setTimeout('$(".status-post .status-post-alert").fadeOut("slow")', 750);
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

function setPostCount() {
	var charCount = $('#postinput').val().length;
	var charsRemaining = 140 - charCount;
	$('.status-post .status-post-char-count').replaceWith('<span class="status-post-char-count">' + charsRemaining.toString() + '</div>');
}


// Attaches the click handler for input text.
// Gets input out of the text box and sends it
// to the twitpost function.
function startPostHandler(myarray) {
    $('.status-post .status-post-button').unbind('click').click(
          function() {
             $input_text = $('#postinput').val();
             twitpost($input_text);
             return false;
          });
    $is_post_form_focused = false;
	$('#postinput').unbind('autocomplete').autocomplete({ 
	source: function(request, response) {
		var last_at_index = request.term.lastIndexOf("@");
		var cur_at_mention = "";
		if(last_at_index >= 0) cur_at_mention = request.term.substr(last_at_index + 1);
		
		if(cur_at_mention.length > 0) {
        	var re = $.ui.autocomplete.escapeRegex(cur_at_mention);
        	var matcher = new RegExp( "^" + re, "i" );
        	var grep_array = $.grep( myarray, function(item,index){
            	return (matcher.test(item.screen_name) || matcher.test(item.name));
        	});
			response( grep_array );
		} else {
			response(new Array());
		}
	},
	focus: function() {
		// prevent value inserted on focus
		return false;
	},
	select: function( event, ui ) {
		var last_at_index = this.value.lastIndexOf("@");
		this.value = this.value.substr(0, last_at_index) + "@" + ui.item.screen_name;
		return false;
	}
	
	})
	.data('autocomplete')._renderItem = function( ul, item ) {
		return $( "<li></li>" )
				.data( "item.autocomplete", item )
				.append( "<a> <div class='autocomplete-entry'> " +
						"<div class='autocomplete-image'> <img src='" + item.image_url + "' width='40' height='40' /> </div>" +
						"<div class='autocomplete-names'><div class='autocomplete-screen_name'>" + item.screen_name + "</div> <div class='autocomplete-name'>" + item.name + "</div> </div>" +
						"</div> </a>" )
				.appendTo( ul );
	};
    $('#postinput').unbind('focus').focus(function() { $is_post_form_focused = true; });
    $('#postinput').unbind('blur').blur(function() { $is_post_form_focused = false; });
    $('#postinput').unbind('keyup').keyup(setPostCount);
}