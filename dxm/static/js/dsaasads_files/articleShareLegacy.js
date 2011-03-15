/* $Id: articleShareLegacy.js 20906 2009-06-24 18:41:45Z nickc $
(c) 2008 The New York Times Company */

function writePost(excludeList) {
	var shareTools = new NYTD.ArticleShareTools();
	shareTools.writePost(excludeList);
	
	var toolsBox = $$('.articleTools');
	if(toolsBox.length <= 1) return;
	
	if(toolsBox[0].select('#adxToolSponsor').length === 0) {
        $('shareMenu').addClassName('last');
	} else {
        toolsBox[1].select('li').last().addClassName('last');
	}
}

// FIXME This probably needs to be exposed for those other pages.
function toggleShareTab(shareButton, postList, excludeList) {
		writePost(excludeList);	
}