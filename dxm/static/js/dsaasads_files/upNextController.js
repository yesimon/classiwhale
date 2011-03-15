/* $Id: upNext.js 37493 2010-04-30 20:38:05Z mtam $ */

// http://prototypejs.org/assets/2009/8/31/prototype.js
// The following is copied and minified from Prototype 1.6.1 to fix a bug
// in 1.6.0.2 for Opera 10.
document.viewport={getDimensions:function(){return{width:this.getWidth(),height:this.getHeight()};},getScrollOffsets:function(){return Element._returnOffset(window.pageXOffset||document.documentElement.scrollLeft||document.body.scrollLeft,window.pageYOffset||document.documentElement.scrollTop||document.body.scrollTop);}};(function(viewport){var B=Prototype.Browser,doc=document,element,property={};function getRootElement(){if(B.WebKit&&!doc.evaluate)return document;if(B.Opera&&window.parseFloat(window.opera.version())<9.5)return document.body;return document.documentElement;}function define(D){if(!element)element=getRootElement();property[D]='client'+D;viewport['get'+D]=function(){return element[property[D]]};return viewport['get'+D]();}viewport.getWidth=define.curry('Width');viewport.getHeight=define.curry('Height');})(document.viewport);

var NYTD = NYTD || {};

NYTD.UpNext = (function () {
  var upNextImgRoot = NYTD.Hosts.imageHost + '/images/article/upNext/';
  var today = new Date();
  var cookie_date = new Date(today.getFullYear()+1, today.getMonth(), today.getDate());
  var feedUrl, popUpEl, popUpElWidth, popUpElHeight, isPositionFixed,
    articleEl, cColumnEl, bottomY, isEnabled = true, isHidden = true, 
    toggleWidth, toggleControl = '.toggleControl', img_upnext_rest = upNextImgRoot+'upnext_rest.png', img_upnext_ro = upNextImgRoot+'upnext_ro.png';

  var getPopUpEl = function (data) {
    var articles    = data.items,
      numOfArticles = articles.length;
      rank          = 0;
    
    // Find next article in the list, defaults to the first article if no match
    var nextArticleData = (function (articles) {
      var currentUrl = $$('head link[rel=canonical]')[0].readAttribute('href');
      
      for (var i=0; i<numOfArticles; i++) {
        if (currentUrl.indexOf(articles[i].guid) !== -1) {
          rank = (numOfArticles - 1 == i) ? 0 : i + 1;
          break;
        }
      }
      
      return articles[rank];
    })(articles);
    
    var sectionName   = data.title.replace('NYT > ', '').escapeHTML(),
      preposition     = (sectionName.toLowerCase() == 'home page') ? 'on the' : 'in',
      articleRankText = (rank + 1) + ' of ' + numOfArticles + ' article' +
        ((numOfArticles > 1) ? 's' : ''),
      nextArticleUrl  = nextArticleData.guid,
      queryObj        = {
        'src': 'un',
        'feedurl': feedUrl
      };
    
    nextArticleUrl += '?' + Object.toQueryString(queryObj);
    
    var toggleImg = '<div class="toggleHolder element1"><img width="13" class="toggleControl" src="' + img_upnext_rest + '"/></div>';
    var el = new Element('div', {id: 'upNext'});
    
    el.innerHTML = '<div class="wrapper opposingFloatControl">' + toggleImg + '<div style="width:310px;" class="element1"><h6>More ' + preposition + ' ' +
      sectionName + ' <span class="num">(' + articleRankText + ')</span></h6>' +
      '<h3><a href="' + nextArticleUrl +'">' + nextArticleData.title +
      '</a></h3><p class="refer"><a href="' + nextArticleUrl +
      '">Read More &raquo;</a></p><button type="button">Close</button></div><br style="clear:both;"/></div>';
    
    el.select('div.toggleHolder')[0].setStyle({
    	'width' : '50px'
    });
    
    el.select('button')[0].observe('click', function (e) {
      setCookie('upnext', 0, {
    	  'domain' : 'nytimes.com',
    	  'path' : '/',
    	  'expires' : cookie_date
      });
      hidePopUp();
      //isEnabled = false;
      //document.body.style.paddingBottom = '';
    });
    
    return el;
  };
  
  var getBottomY = function () {
    var getElBottomY = function (el) {
      return el.getHeight() + el.cumulativeOffset()[1];
    };
    
    articleEl = articleEl || $$('#article .first')[0] || $$('#content .hentry')[0] || $$('#main .hentry')[0];
    cColumnEl = cColumnEl || $$('#main .cColumn')[0] || $$('#cCol')[0] || $$('#main .cColumn')[0];
    
    // Compensate for extra space on ads for cColumnBottomY
    var articleBottomY = getElBottomY(articleEl),
      cColumnBottomY   = getElBottomY(cColumnEl) + popUpElHeight - 30; 
    
    return (articleBottomY > cColumnBottomY) ? articleBottomY : cColumnBottomY;
  };
  
  var getCookie = function(name) {
	  return new RegExp(name + '=([^;]+)').test(unescape(document.cookie)) ? RegExp.$1 : null;
  };

  var setCookie = function(name, value, options) {
	  var newcookie = [escape(name) + "=" + escape(value)];
	  if(options) {
		if (options.expires) newcookie.push("expires=" + options.expires.toGMTString());
		if (options.path)    newcookie.push("path=" + options.path);
		if (options.domain)  newcookie.push("domain=" + options.domain);
		if (options.secure)  newcookie.push("secure");
	  }
	  document.cookie = newcookie.join('; ');
  };
  
  var showPopUp = function () {
    // Don't show the popup yet if the article height has changed since
    // page load
    var currentBottomY = getBottomY();
    if (bottomY != currentBottomY) {
      bottomY = currentBottomY;
      return false;
    }
    
    if(getCookie('upnext') == 0) {
	    new Effect.Morph(popUpEl, {
	    	duration: 0.3,
	    	style: 'right: ' + (-toggleWidth) + 'px'
	    });
	    
	    $$(toggleControl)[0].removeClassName('hidden');
	} 
    else if(getCookie('upnext') == null || getCookie('upnext') == 1) {
	    new Effect.Morph(popUpEl, {
	    	duration: 0.3,
	    	style: 'right: 0',
	    	afterFinish: function() {
	    		$$(toggleControl)[0].addClassName('hidden');
	    	}
	    });
	}

    isHidden = false;
  };
  
  var hidePopUp = function () {
	var scrolledHeight = document.viewport.getHeight()+document.viewport.getScrollOffsets()[1];
	var offset = scrolledHeight - getBottomY();
	
	if(getCookie('upnext') == 0 && offset > 0) {
	    new Effect.Morph(popUpEl, {
	        duration: 0.5,
	        style: 'right: ' + (-toggleWidth) + 'px'
	      });
	    $$(toggleControl)[0].removeClassName('hidden');
	} 
	else if(getCookie('upnext') == 0 && offset < 0) {
	    new Effect.Morph(popUpEl, {
		      duration: 0.5,
		      style: 'right: ' + (-popUpElWidth) + 'px'
		    });
	}
	else if(getCookie('upnext') == null || getCookie('upnext') == 1) {
	    new Effect.Morph(popUpEl, {
	      duration: 0.5,
	      style: 'right: ' + (-popUpElWidth) + 'px'
	    });
	}
    isHidden = true;
  };
  
  var setupPopUp = function (data) {
    // Set up and insert popup element
    popUpEl = getPopUpEl(data);
    var popUpWrapperEl = new Element('div', {'id': 'upNextWrapper'});
    popUpWrapperEl.appendChild(popUpEl);
    document.body.appendChild(popUpWrapperEl);
    
    popUpElHeight = popUpEl.getHeight();
    popUpElWidth = popUpEl.getWidth() + 20; // Pad 20px for box shadow
    toggleWidth = popUpElWidth - 50;

    popUpEl.setStyle({'right': -(popUpElWidth) + 'px'});
    document.body.style.paddingBottom = popUpElHeight + 10 + 'px';
    
    isPositionFixed = (popUpEl.getStyle('position') == 'fixed');
    if (!isPositionFixed) {
      popUpWrapperEl.setStyle({'width': popUpElWidth + 'px'});
      popUpWrapperEl.setStyle({'height': popUpElHeight + 'px'});
    }
    
    // Show popup when the bottom of either the article or the c-col shows in
    // the viewport, whichever comes later.
    bottomY = getBottomY();
    Event.observe(window, 'scroll', function (e) {
      var scrolledHeight = document.viewport.getHeight() +
        document.viewport.getScrollOffsets()[1];
      
      // Magic sauce to emulate position:fixed in IE6
      if (!isPositionFixed) {
        popUpWrapperEl.setStyle({'top': scrolledHeight - popUpElHeight + 'px'});
      }
      
      var offset = scrolledHeight - bottomY;
      if (offset > 0 && isHidden && isEnabled) {
    	  showPopUp();
      } 
      else if(offset < 0 && !isHidden) {
    	  hidePopUp();
      }
    });
    
    popUpEl.select(toggleControl)[0].observe('mouseover', function(e) {
    	$$(toggleControl)[0].writeAttribute('src', img_upnext_ro);
    });
    
    popUpEl.select(toggleControl)[0].observe('mouseout', function(e) {
		$$(toggleControl)[0].writeAttribute('src', img_upnext_rest);
    });
    
    popUpEl.select(toggleControl)[0].observe('click', function(e) {
		isEnabled = true;
		setCookie('upnext', 1, {
			'domain' : 'nytimes.com',
			'path' : '/',
			'expires' : cookie_date
		});
		showPopUp();
    	
    });
    

	
  };
  
  return {
    init: function () {
      // Only activate on the last page on paginated articles. We test this
      // by checking if the last page is linked or not.
      var pageNumbersEl = $('pageNumbers');
      if (pageNumbersEl && pageNumbersEl.select('li:last-child a').length!=0) {
        return false;
      }
      
      // If a user clicks through a ranked Fashion article from the Business
      // section front, we want to:
      // 1. show the next article from Business, not Fashion,
      // 2. continue pulling the next articles from Business on subsequent
      //    click throughs.
      // 
      // In other cases, simply use the section assigned to the article.
      //
      // NOTE: "Today's Paper" is temporarily excluded because it doesn't have an
      //       RSS feed.
      var referrer           = document.referrer,
          isFromSectionFront = /.+nytimes\.com\/pages\/.+\/index\.html/.test(referrer);
      
      if (isFromSectionFront && referrer.indexOf('pages/todayspaper') == -1) {
        feedUrl = referrer.replace('.html', '.jsonp').
          replace(/http:\/\/.+\.nytimes\.com/, NYTD.Hosts.jsonHost);
        
      } else {
        var queryFeedUrl = window.location.search.toQueryParams().feedurl || '',
            sfMetaTag    = $$('head meta[name=sectionfront_jsonp]')[0],
            metaTagSfUrl = sfMetaTag && sfMetaTag.readAttribute('content');
            
        feedUrl = queryFeedUrl || metaTagSfUrl || '';
      }
      
      // This should only be triggered on articles that doesn't have the
      // "sectionfront_url" meta tag published
      if (!feedUrl) {
        return false;
      }
      
      // Try (sub)section feed first, fallback to homepage feed otherwise
      new NYTD.JsonpFeed(feedUrl, {
        onSuccess: setupPopUp,
        onFailure : function () {
          var fallbackFeedUrl = NYTD.Hosts.jsonHost + '/pages/index.jsonp';
          new NYTD.JsonpFeed(fallbackFeedUrl, {
            onSuccess: setupPopUp
          });
        }
      });
    }
  };
})();

if (!/(iphone|ipod|ipad|android).+applewebkit/i.test(navigator.userAgent)) {
  Event.observe(window, 'load', NYTD.UpNext.init);
}
