NYTD.WordReference = (function(){

	var selection, selectionText, selectionButtons=[], newRange, origRange, highlightRange, origArticleBody, articleBody;
	var rangeMarkup = '';

	var baseUrl = NYTD.Hosts.imageHost;

	var buttons = {
		"wordReference": {
			"mouseupHandler": exportSelection,
			"isEligible" : function(wordCount) { return (wordCount < 4); },
			"element": new Element(
				'span', {
					'className': 'nytd_selection_button',
					'id':		'nytd_selection_button_wordReference',
					'title':	'Lookup Word',
					'style':
						'margin:-20px 0 0 -20px; position:absolute;'
						+ 'background:url(' + baseUrl +'/images/global/word_reference/ref_bubble.png);'
						+ 'width:25px;height:29px;cursor:pointer;_background-image: none;'
						+ 'filter:progid:DXImageTransform.Microsoft.AlphaImageLoader(src="'+ baseUrl +'/images/global/word_reference/ref_bubble.png", sizingMethod="image");'
				}
			)
		},
		"timesQuotes": {
			"mouseupHandler": exportCitation,
			"isEligible" : function(wordCount) { return (wordCount > 4); },
			"element": new Element(
				'span', {
					'className':'nytd_selection_button',
					'id':		'nytd_selection_button_timesQuotes',
					'title':	'Make a clipping',
					'style':
						'margin:-20px 0 0 -20px; position:absolute;'
						+ 'background:url('+ baseUrl +'/images/global/times_quote/copy_bubble.png);background-repeat:none;'
						+ 'width:55px;height:30px;cursor:pointer;_background-image: none;'
						+ 'filter: progid:DXImageTransform.Microsoft.AlphaImageLoader(src="'+ baseUrl +'/images/global/times_quote/copy_bubble.png", sizingMethod="image");'
				}
			)
		}
	};
	var buttonsHash = $H( buttons );


	function handleCopy(e) {
		var wc = wordCount(selectionText);
		if(wc) {
			dcsMultiTrack('DCS.dcssip','www.nytimes.com','DCS.dcsuri','/contentCopyTracker.html','DCS.dcswc',wc,'WT.ti','contentCopyTracker','WT.z_dcsm','1');
		}
	}

	function wordCount(inStr) {
		var wc;
		wc = inStr && inStr.replace(/[^\s\w]+/g, "");			 // get rid of punctuation
		wc = wc && wc.replace(/^\s*/, "").replace(/\s*$/, "");	 // trim
		wc = wc && wc.length && wc.split(/\s+/).length;			 // split & count
		return Number(wc);
	}
	

	function handleMouseUp(e) {
		var target = e.element();

		if(selectionButtons.length) {
			clearButtons(e);
			unsetPersistentHighlight(e);
		}
		
		if($("nyt_tq_menu_container")) {
			closeTqMenu(e);
			if (target.id !== "nytd_selection_button_timesQuotes") {
				unsetPersistentHighlight(e);
			}	
		}
		
		testSelection = getSelection();
		if (testSelection && testSelection.toString().length) {

			// set the globals
			selection = testSelection;
			origArticleBody = articleBody.innerHTML;

			window.setTimeout( function(){
				buttonsHash.keys().each( function(name) {
					selectionText = getSelectionText(name);
					if(name === "wordReference") { 			// Temporary blogger test code
						insertButton(name);
					/* Temporary blogger test code */
					}
					else if(name === "timesQuotes") {
						var wc = wordCount(selectionText);
						if(buttons["timesQuotes"].isEligible(wc)) {

							var oldScriptTag = document.getElementById("tqBloggerTestQuery"); 
							if(oldScriptTag !== null) {
								document.getElementsByTagName('head')[0].removeChild(oldScriptTag)
							}

							var hostName = window.location.href.toString();
							hostName  = hostName.match(".*\.com");
							var url = hostName + "/gst/timesquotes/userWhitelist.html";
							var scriptTag = document.createElement("script");
							scriptTag.setAttribute("id","tqBloggerTestQuery");
							scriptTag.setAttribute("src", url);
							scriptTag.setAttribute("type","text/javascript");

							try { document.getElementsByTagName('head')[0].appendChild( scriptTag ); }
							catch(err) {
							}
						}
					}
					/* End Temporary blogger test code */
				} );
			}, 0);
		}
	}

	function getSelection() {
		return Try.these(
			function() { return window.getSelection() },
			function() { return document.getSelection() },
			function() {
				var selection = document.selection && document.selection.createRange();
				selection.toString = function() { return this.text };
				return selection;
			}
		) || false;
	}

	function isSelectionDirectionForward() {
		var order = selection.anchorNode.compareDocumentPosition(selection.focusNode);
		// order is a bitmask, 000010 means that the order is reversed.
		if((order & 2) === 2) { return 0; }
		else                  { return 1; }
	}

	function insertButton(buttonName) {
		var mouseupHandler = buttons[buttonName].mouseupHandler;
		var aSelectionButton = buttons[buttonName].element;
		var wc = wordCount(selectionText);
		
        /* here's where we check all the conditions that should stop us
	       from adding the quote button
	     */			
		if(buttonName === "timesQuotes") {
			if(!window.getShareHeadline){ return; }
			if(!window.getShareByline)  { return; }
			if(!window.getSharePubdate) { return; }
			if(!window.getShareURL)     { return; }
		}

		if(buttons[buttonName].isEligible(wc)) {
			var buttonInsertErrorFlag = 0;
			
			if (Prototype.Browser.IE) {
				var tmp = new Element('div');
				tmp.appendChild(aSelectionButton);
				newRange = selection.duplicate();
				newRange.setEndPoint( "StartToEnd", selection);
				newRange.pasteHTML(tmp.innerHTML);
				aSelectionButton = 'nytd_selection_button_' + buttonName;
			}
			else {
				var range = selection.getRangeAt(0);
				newRange = document.createRange();

				if(isSelectionDirectionForward()) {
					try { newRange.setStart(selection.focusNode, range.endOffset); } catch (e) {}
				}
				else {
					try { newRange.setStart(selection.anchorNode, range.endOffset); } catch (e) {}
				}

				if(!buttonInsertErrorFlag) {
					newRange.insertNode(aSelectionButton);
				}	
			}

			if(!buttonInsertErrorFlag) {
				Element.observe(aSelectionButton, 'mouseup', mouseupHandler, true);
				selectionButtons[selectionButtons.length] = buttonName;
			}	
		}
	}

	function clearButtons(e) {
		selection = null;
		for(var i = 0; i < selectionButtons.length; i++) {
			var button = $("nytd_selection_button_" + selectionButtons[i]);
			button.stopObserving('mouseup', exportSelection);
			button.remove();
			button = null;
		}
		selectionButtons.clear();
	}

	function closeTqMenu(e) {
		$('nyt_tq_menu_container') && NYTD.Citations.off('nyt_tq_menu_container');
	}	


	/* need to get the text ONLY from the selection, omitting anything from the article_inline element.
	 * Normally the browser will strip the markup from the selection, but we need to leave the markup
	 * in the selection long enough for us to identify the article-inline element, which means we then
	 * strip the markup out manually.
	 */
	function getSelectionText(buttonName) {
		var selection = getSelection();
		var childNodes, last;
		var tempDiv;
		tempDiv = window.document.createElement('div');
		
		if(buttonName === "wordReference") { 
			return (selection && selection.toString()) || "";
		}
			
		 if (Prototype.Browser.IE) {
			highlightRange = selection.duplicate();
			tempDiv.innerHTML =  selection.htmlText;
		 }
		 else {
			highlightRange = selection.getRangeAt(0);
			tempDiv.appendChild(highlightRange.cloneContents());
		}	
		rangeMarkup = tempDiv.innerHTML;
		
		childNodes = nodeListToArray(tempDiv.childNodes);
		
		// remove the left-hand Multimedia stuff, and any other extraneous
		// div tags
		childNodes.each( function(node) {
			if (node.nodeName === "DIV") {
				tempDiv.removeChild(node);	
			}
		});

		selectedText = tempDiv.toString();	

		// remove the jump links used for mobile platform:
		selectedText = selectedText.replace(/<a[^>]*jumpLink[^>]>[^<]*<\/a>/ig,"");

		var selectedTextArray = new Array();

		// we want to split the selection BEFORE each OPENING <p> tag and AFTER each CLOSING <p> tag.
		selectedText      = rangeMarkup.replace(/(<p[ >])/ig,"~~~$1");
		selectedTextArray = selectedText.replace(/(<\/p[ >])/ig,"$1~~~").split("~~~");
		if(selectedTextArray.length && selectedTextArray[0] === "") {
			selectedTextArray.shift();
		}	
		var last = selectedTextArray.length-1;
		if(selectedTextArray.length && selectedTextArray[last] === "") {
			selectedTextArray.pop();
			last--;
		}	
		var textOnly = "";

		var divCount = 0;
		var line = "";
		for(var i = 0; i < selectedTextArray.length; i++) {
			line = selectedTextArray[i];

			// do not take a <p> element if it is inside another div:
			divCount += line.match(/<div/ig)   && line.match(/<div/ig).length   || 0;
			if(divCount === 0) {
				textOnly += line.replace(/<[^>]*>/ig, "") + "<br/>";
			}	
			divCount -= line.match(/<\/div/ig) && line.match(/<\/div/ig).length || 0;
		}
		textOnly = textOnly.replace(/<br\/>$/, "");

		return textOnly;

	}
	
	/* Creating some special markup that reproduces the selection highlighting, so that the highlighting 
	 * can remain in place while the TQ Menu is open. To do this we wrap each bit of article text in 
	 * <span> tags. However, if the selection includes some or all of the article_inline element, we 
	 * will make sure not to put highlighting tags around any part of it.
	 */
	function setPersistentHighlight() {
		var rangeMarkupArray = new Array();
		rangeMarkup      = rangeMarkup.replace(/(<p[ >])/g,"~~~$1");
		rangeMarkupArray = rangeMarkup.replace(/(<\/p[ >])/g,"$1~~~").split("~~~");
		
		if(rangeMarkupArray.length && rangeMarkupArray[0] === "") {
			rangeMarkupArray.shift();
		}

		var last = rangeMarkupArray.length-1;
		if(rangeMarkupArray.length && rangeMarkupArray[last] === "") {
			rangeMarkupArray.pop();
			last--;
		}	
		if(rangeMarkupArray.length) {
			if(articleBody.innerHTML.indexOf(rangeMarkupArray[0]) == -1 ) {
				// remove opening tag
				rangeMarkupArray[0] = rangeMarkupArray[0].replace(/^<[^>]*>/, "");
			}
			if(articleBody.innerHTML.indexOf(rangeMarkupArray[last]) == -1) {
				// remove closing tag
				rangeMarkupArray[last] = rangeMarkupArray[last].replace(/<\/[^>]*>$/, "");
			}
		}
		origRange = rangeMarkupArray.join("").replace(/>\s*</g, "><");	

		var spanOpen  = "<span style=\"background:#316AC5;color:#FFFFFF\">";
		var spanClose = "</span>";

		start = 0;
		last = rangeMarkupArray.length-1;

		while(start < last && !rangeMarkupArray[start].match(/<\/p>$/i)) { 
			start++;
		}
		
		rangeMarkupArray[start] = rangeMarkupArray[start].replace(/^(<p[^>]*>)?(.*)/i, "$1" + spanOpen + "$2");
		rangeMarkupArray[start] = rangeMarkupArray[start].replace(/<\/p>$/i, spanClose + "</p>");
		
		while(last > start && !rangeMarkupArray[last].match(/^((<p>)|(<p\s[^>]*>))/i)) { 
			last--; 
		}	
		rangeMarkupArray[last] = rangeMarkupArray[last].replace(/^((<p>)|(<p\s[^>]*>))/i, "$1" + spanOpen) + spanClose;
		
		var divCount = 0;
		if (start < last) {
			for(var i = start + 1; i < last; i++) {
				// do not add <span> tags to a <p> if it is inside another div:
				divCount += rangeMarkupArray[i].match(/<div/ig) && rangeMarkupArray[i].match(/<div/ig).length || 0;
				divCount -= rangeMarkupArray[i].match(/<\/div/ig) && rangeMarkupArray[i].match(/<\/div/ig).length || 0;
				
				if(divCount === 0) {
					rangeMarkupArray[i] = rangeMarkupArray[i].replace(/^((<p>)|(<p\s[^>]*>))/i, "$1" + spanOpen);
					rangeMarkupArray[i] = rangeMarkupArray[i].replace(/<\/p>$/, spanClose + "</p>");
				}	
			}
		}

		var newHighlightRange = rangeMarkupArray.join("");	
		var articleBodyText = articleBody.innerHTML.replace(/>\s*</g, "><");

		if(articleBodyText.indexOf(origRange) === -1) { 
			// remove the jump links used for mobile platform:
			articleBodyText = articleBody.replace(/<a[^>]*jumpLink[^>]>[^<]*<\/a>/ig,"");
		}
		articleBodyText = articleBody.replace(origRange, newHighlightRange);
		articleBody.innerHTML = articleBodyText;
		
		Element.observe($('nytd_selection_button_timesQuotes'), 'mouseup', exportCitation, true);
	}


	function nodeListToArray(nodeList) { 
		var ret = []; 
		for(var i=0, len = nodeList.length; i < len; i++) { 
			ret.push(nodeList[i]); 
		} 
		return ret;
	} 

	function unsetPersistentHighlight(e) {
		if(origArticleBody.length) {
			articleBody.innerHTML = origArticleBody;
		}	
	 }

	function exportSelection(e) {
		var url = 'http://query.nytimes.com/search/query?srchst=ref&query=' + encodeURIComponent(selectionText);
		var newwin = window.open(url,'answersdotcom','height=450,width=820,location=false,menubar=false,toolbar=false,status=false,resizable, scrollbars');
		if (newwin) newwin.focus();
	}

	function exportCitation(e) {
		NYTD.WordReference.mouseX = e.pageX;
		NYTD.WordReference.mouseY = e.pageY;
		window.citeCallback = function() {
			NYTD.Citations.setup(selectionText);
			NYTD.Citations.showForm(e);
		};
		var scriptUrl = NYTD.Hosts.jsHost +'/js/common/screen/cites.js';

		var scriptTag = new Element(
			'script', {
				src : scriptUrl,
				id	: 'nyt_citations'
			}
		);

		document.getElementsByTagName('head')[0].appendChild( scriptTag );
		setPersistentHighlight();
		clearButtons(e);
	}

	return {

		turnOffHighlight: function() {
    		unsetPersistentHighlight();
		},

	/* Temporary blogger test code */
		tqBloggerTestCallBack: function(results) {
			if(typeof(results["tq_approved"]) === "number" && results["tq_approved"] === 1) {
				insertButton("timesQuotes");
			}
		},
	/* End Temporary blogger test code */

		initialize: function() {
			articleBody = $('articleBody') || $('article');
			if (articleBody){
				articleBody.observe('mouseup', handleMouseUp, true);
				// need to do it this way because of IE
				document.getElementsByTagName("html")[0].oncopy =	handleCopy;	
			}
		}
	};

})();

Event.observe(window, 'load', function(){
	NYTD.WordReference.initialize();
})


