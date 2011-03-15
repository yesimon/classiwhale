/* $Id: articleShareController.js 57935 2011-02-11 08:09:26Z shahmeet.singh $
(c) 2008 The New York Times Company */

/**
 * Pops up window for network share
 *
 * @param string network Name of network (matches key in openers object)
 * @param object meta Meta data object
 */
NYTD.ArticleShareToolsPostToNetwork = function(network, meta){
  function postPopUp(url, name, params) {
    var win = window.open(url, name, params);
  }

  var openers = {
        newsvine : function () {
                var keywords = meta.getSection();
                if(typeof(getShareSubSection) == 'function') {
                    if(meta.getSubSection() != '') {
                        keywords += ',' + meta.getSubSection();
                    }
                }
                if (meta.getKeywords() != '') {
                    keywords += ',' + meta.getKeywords();
                }
                postPopUp('http://www.newsvine.com/_wine/save?ver=2&popoff=0&aff=nytimes&t=' + keywords + '&e=' + meta.getDescription() + '&h=' + meta.getHeadline() + '&u=' + meta.getURL('newsvine'), 'newsvine', 'toolbar=0,status=0,height=445,width=650,scrollbars=yes,resizable=yes');
                s_code_linktrack('Article-Tool-Share-Newsvine');
        },

        facebook : function() {
                postPopUp('http://www.facebook.com/sharer.php?u=' + meta.getURL() + '&t=' + meta.getHeadline(), 'facebook', 'toolbar=0,status=0,height=436,width=646,scrollbars=yes,resizable=yes');
                s_code_linktrack('Article-Tool-Share-Facebook');
        },

        digg : function () {
                postPopUp('http://digg.com/remote-submit?phase=2&url=' + meta.getURL() + '&title=' + meta.getHeadline() + '&bodytext=' + meta.getDescription(), 'digg', 'toolbar=0,status=0,height=450,width=650,scrollbars=yes,resizable=yes');
                s_code_linktrack('Article-Tool-Share-Digg');
        },

        permalink : function () {
                postPopUp('http://' + window.location.hostname + '/export_html/common/new_article_post.html?url=' + decodeURIComponent(meta.getURL()) + '&title=' + meta.getHeadline()+ '&summary=' + meta.getDescription() + '&section=' + meta.getSectionDisplay() + '&pubdate=' + meta.getPubdate() + '&byline=' + meta.getByline(), 'permalink', 'toolbar=0,status=0,height=410,width=490,scrollbars=yes,resizable=no');
                s_code_linktrack('Article-Tool-Share-Permalink');
        },

        delicious : function () {
                postPopUp('http://del.icio.us/post?v=4&partner=nyt&noui&jump=close&url=' + meta.getURL() + '&title=' + meta.getHeadline() + '&bodytext=' + meta.getDescription(), 'delicious', 'toolbar=0,status=0,height=400,width=700,scrollbars=yes,resizable=no');
                s_code_linktrack('Article-Tool-Share-Delicious');
        },

        mixx : function () {
            try {
                var popUpUrl = meta.getURL();
                var otherParams =
                    '?title='       + meta.getHeadline()
                + '&description=' + meta.getDescription()
                + '&tags='        + meta.getKeywords()
                + '&partner='     + 'NYT';
                postPopUp(
                'http://mini.mixx.com/submit/story'
                + '?page_url='    + meta.getURL()
                + otherParams,
                'mixx',
                'toolbar=0,status=0,height=550,width=700,scrollbars=yes,resizable=no'
                );
            } catch(e) {
                postPopUp(
                'http://mini.mixx.com/submit/story'
                + '?page_url='    + meta.getURL()
                + '&title='       + meta.getHeadline()
                + '&partner='     + 'NYT'
                ,
                'mixx',
                'toolbar=0,status=0,height=550,width=700,scrollbars=yes,resizable=no'
                );
            }
            s_code_linktrack('Article-Tool-Share-Mixx');
        },

        linkedin : function () {
            //http://www.linkedin.com/shareArticle?mini=true&url={articleUrl}&title={articleTitle}&summary={articleSummary}&source={articleSource}
            postPopUp(
            'http://www.linkedin.com/shareArticle?mini=true'
            + '&url='         + meta.getURL()
            + '&title='       + meta.getHeadline()
            + '&summary='     + meta.getDescription()
            + '&source='      + 'The New York Times'
            ,
            'Linkedin',
            'toolbar=0,status=0,height=550,width=700,scrollbars=yes,resizable=no'
            );
            s_code_linktrack('Article-Tool-Share-LinkedIn');
        },

        myspace: function () {
            postPopUp('http://www.myspace.com/index.cfm?fuseaction=postto&u=' + meta.getURL() + '&t=' + meta.getHeadline() + '&c=' + meta.getDescription(), 'myspace', 'toolbar=0,status=0,height=436,width=880,scrollbars=yes,resizable=yes');
            s_code_linktrack('Article-Tool-Share-MySpace');
        },

        twitter: function () {
            postPopUp('http://twitter.com/index.cfm?fuseaction=postto&u=' + meta.getURL() + '&t=' + meta.getHeadline() + '&c=' + meta.getDescription(), 'myspace', 'toolbar=0,status=0,height=436,width=880,scrollbars=yes,resizable=yes');
            s_code_linktrack('Article-Tool-Share-MySpace');
        }
    }

  openers[network]();
};

/**
 * Article Share Tools
 */
NYTD.ArticleShareTools = function(rootId, meta) {
    var NYTShareAdScript = 'http://www.nytimes.com/adx/bin/adx_remote.html?type=fastscript&page=www.nytimes.com/yr/mo/day/&posall=Frame6A&query=qstring&keywords=?',
        imageHost = "http://graphics8.nytimes.com",
        imagePath = "/images/article/functions/",
        parentElement,
        postElement,
        postLink,
        closeLink,
        postList,
        closeTimerId;

    // Functions that extract meta information about the asset in question. Can be overridden.\
    var meta = meta || {
        getDescription: function() { return getShareDescription(); },
        getURL: function() { return getShareURL(); },
        getHeadline: function() { return getShareHeadline(); },
        getKeywords: function() { return getShareKeywords(); },
        getSection: function() { return getShareSection(); },
        getSectionDisplay: function() { return getShareSectionDisplay();},
        getByline: function() { return getShareByline();},
        getSubSection: function() { return getShareSubSection();},
        getPubdate: function() { return getSharePubdate();}
    };

    if ( closeLink !== undefined ) {
    $(document).observe("click", function(event) {
        if (closeLink.hasClassName("closeButton") && outsideShareTools(event.target)) {
            closeShareTools();
        }
    });
    }

    // Write the share tools content onto the page.
    this.writePost = function(excludedShareTypes) {
        parentElement = getShareRootElement();
        postElement = this.makePostElement(parentElement);
        postElement.style.width = "168px";
        postLink = makePostLink();
        closeLink = makeCloseLink();
        postList = makePostList();

        postElement.appendChild(postLink);
        postElement.appendChild(closeLink);

        if (excludedShareTypes) {
            window.shareToolsExcludeList = excludedShareTypes;
        }

        addShareTargets(postList);

        postElement.appendChild(postList);
        parentElement.appendChild(postElement);
        
        addTwitter();
        if (window.XMLHttpRequest) {
          addFacebook();
        }
    }

    this.writeLinks = function(sList, excludedShareTypes) {
    if (excludedShareTypes) {
            window.shareToolsExcludeList = excludedShareTypes;
        }
        addShareLinks(sList);
    }

    this.makePostElement = function(root) {
        if (root === undefined) getShareRootElement();
        if (root.id == "toolsList") {
            return new Element( "LI", {id:"shareMenu"}).addClassName('closed');     // create li for articles, slideshows
        } else if (root.id == "shareToolButton") {
            return new Element("SPAN", {id:"shareMenu"}).addClassName('closed');   // create span for xsl/php page
        } else {
            throw("Couldn't find share tool element.");
        }
    }

    function getShareRootElement() {
        var root;
        if (rootId) {
            return $(rootId);
        }
        if (root = $("toolsList")) { // Articles and slide shows.
            return root;
        } else if (root = $("shareToolButton")) { // XSL/PHP
            root.update("");
            return root;
        }
    }

    function makePostLink() {
        var postLink = new Element("a", {href:"#"}).update("Share").addClassName("shareButton");
        postLink.observe("click", function(event) {
            if ( typeof NYTD_PlaylistMgr == 'object' ) {
                var video_permalink = $('video_permalink');
                if (video_permalink) video_permalink.setAttribute( 'value', NYTD_PlaylistMgr.getCurrentUrl() );

                var embed_code = $('embed_code');
                if (embed_code) embed_code.setAttribute( 'value', NYTD.Video.Share.getEmbedCode( NYTD_PlaylistMgr.getKnewsTitleRefId() ));
            }
            displayShareTools(postElement);
            event.stop();
            return false;
        });
        return postLink;
    }

    function makeCloseLink() {
        closeLink = new Element("a", {"href":"#"}).update("Close").addClassName("hidden");
        closeLink.style.opacity = 0;
        closeLink.observe("click", function(event){ closeShareTools(); event.stop(); return false;});
        return closeLink;
    }

    function makePostList() {
        var postList = new Element("ul", {"id":"shareList"}).addClassName("hidden");
        postList.style.opacity = 0;
        return postList;
    }

    function displayShareTools(element) {
        if (element.hasClassName("closed")) {
            if (parentElement.id=="shareToolButton"||parentElement.hasClassName("toolsList")) {
                parentElement.addClassName("shareMenuOpened"); // class to prevent article tools from collapsing and to remove border in xsl pages
            }
            element.className="opened";
            if ( typeof NYTD_PlaylistMgr == 'object' ) {
              var orgHeight = 149;
            } else {
              var orgHeight = 114;
            }
            new Effect.Scale (element, 200, {duration:0.5,scaleContent:false,scaleMode:{originalWidth:167.5,originalHeight:orgHeight},
                afterFinish: function() {
                    closeLink.className="closeButton"; // display CLOSE link
                    $("shareList").className=""; // display the list of Share links
                    toggleShareAd("show");
                    new Effect.Opacity(closeLink,{duration:0.5,from:0,to:1});
                    new Effect.Opacity($("shareList"), {duration:0.5,from:0,to:1});
                    var numEvent=0;
                    $(document).observe("mouseover", function(event) { // close window after 5 seconds of mousing outside share tools
                        if(closeLink.hasClassName("closeButton")&&outsideShareTools(event.target)&&numEvent==0) {
                            closeTimerId = window.setTimeout(closeShareTools,5000); numEvent++;
                        }
                        event.stop(); return false;
                    });
                } });
        } else {
            closeShareTools();
        }
    }

    function closeShareTools() {
        clearTimeout(closeTimerId);
        closeLink.className="hidden"; // hide CLOSE link
        new Effect.Opacity($("shareList"), {duration:0.5,from:1,to:0,
            afterFinish: function() {
                $("shareList").className="hidden"; // hide the list of Share links
                toggleShareAd("hide");
                if ( typeof NYTD_PlaylistMgr == 'object' ) {
                  var orgHeight = 296;
                } else {
                  var orgHeight = 228;
                }
                new Effect.Scale($("shareMenu"),50,{duration:0.5,scaleMode:{originalWidth:335,originalHeight:orgHeight},scaleContent:false,
                    afterFinish: function() {
                        $("shareMenu").className="closed";
                        if(parentElement.hasClassName("shareMenuOpened")) parentElement.removeClassName("shareMenuOpened");
                    } }); } });
        new Effect.Opacity(closeLink,{from:1,to:0});
    }

    function outsideShareTools(target) {
        var bool = ! (target.id=="shareMenu" || target.id=="shareList");
        for (var i=0; i < $("shareMenu").childNodes.length; i++) {
            if(target==$("shareMenu").childNodes[i])
                bool = false;
        }

        for (var i=0; i < $("shareList").childNodes.length; i++) {
            var node = $("shareList").childNodes[i];
            if(target==node||target==node.childNodes[0])
                bool = false;
        }

        for (var i=0; i < $("shareMenuAd").childNodes.length; i++) {
            var node = $("shareMenuAd").childNodes[i];
            if(target==node||target==node.childNodes[0])
                bool = false;
        }

        return bool;
    }

    function toggleShareAd(state) {
        if (typeof adxpos_Frame6A != 'undefined') {
            state == "show"
                ? displayShareAd()
                : hideShareAd();
        } else {
            $("shareMenu").className="opened noAd"; // height is different if there is no ad. The height will be controlled through css
        }
    }

    function displayShareAd() {
        $( "shareMenuAd" ).update("<span class='shareSponsor'></span>"+adxads[adxpos_Frame6A]);
    }

    function hideShareAd() {
        $( "shareMenuAd" ).update('');
        //reload ad script to count the next opening of the Share Button as another ad impression.
        var reloadScript = new Element("script", {src:NYTShareAdScript});
        $( "shareMenuAd" ).appendChild(reloadScript);
    }

    function postPopUp(url, name, params) {
        var win = window.open(url, name, params);
    }

    function itemInExcludeList(sharelinkName) {
        return typeof window.shareToolsExcludeList !='undefined' && typeof window.shareToolsExcludeList[sharelinkName] !='undefined';
    }

    function addLibraryShare (parentElement) { // for video library pageaddShareLink(sList, "digg", "Digg");
            var libraryShareEmbeds = new Element("div").addClassName("embeds").addClassName("clearfix");
            var select = function (event) {
                var element = Event.element(event);
                element.select();
            }
            libraryShareEmbeds.appendChild(new Element("label", {"for":"video_permalink"}).update("Permanent URL"));
            var permalink_input = new Element("input", {"id":"video_permalink", "name":"video_permalink", "type":"text"});
            permalink_input.setAttribute( "value", meta.getURL() );
            permalink_input.observe('focus', select);
            permalink_input.observe('click', select);
            libraryShareEmbeds.appendChild( permalink_input );
            libraryShareEmbeds.appendChild(new Element("label", {"for":"embed_code"}).update("Embed Code"));
            var embedcode_input = new Element("input", {"id":"embed_code", "name":"embed_code", "type":"text"});
            embedcode_input.setAttribute( "value",  NYTD.Video.Share.getEmbedCode( NYTD_PlaylistMgr.getKnewsTitleRefId() ));
            embedcode_input.observe('focus', select);
            embedcode_input.observe('click', select);
            libraryShareEmbeds.appendChild( embedcode_input );
            parentElement.appendChild(libraryShareEmbeds); 
    }

    function addShareLink(parentElement, sharelinkName, sharelinkText) {
        if(itemInExcludeList(sharelinkName)){ return; }
        var postItem = new Element("li").addClassName(sharelinkName);
        var itemLink = new Element("a", {href:"#"}).update(sharelinkText);
        itemLink.style.backgroundImage = "url(" + imageHost + imagePath + sharelinkName + ".gif)";
        itemLink.observe("click", function(e) {
            NYTD.ArticleShareToolsPostToNetwork(sharelinkName, meta);
            e.stop();
        });

        postItem.appendChild(itemLink);
        parentElement.appendChild(postItem);
    }

    function addShareLinks(sList) {
        var typeMeta = $$('meta[name="PT"]')[0];
        
        addShareLink(sList, "linkedin", "Linkedin");
        addShareLink(sList, "digg", "Digg");
        if (!typeMeta || typeMeta.content != 'Article') {
          addShareLink(sList, "facebook", "Facebook");
        }
        addShareLink(sList, "mixx", "Mixx");
        addShareLink(sList, "myspace", "MySpace");
        addShareLink(sList, "permalink", "Permalink");
    }

    function addShareTargets(shareList) {
        var sList = $(shareList);

    if ( typeof NYTD_PlaylistMgr == 'object' ) addLibraryShare(sList);

        addShareLinks(sList);

        //add another li for ad
        var shareMenuAd = new Element("li", {id:"shareMenuAd"});

        //append the remote ad script
        var loadScript = new Element('SCRIPT', {"src":NYTShareAdScript});
        shareMenuAd.appendChild(loadScript);
        sList.appendChild(shareMenuAd);
    }
    
    function addFacebook() {
      var target = $('toolsList');
      if (target) {
		if (NYTD.Facebook && NYTD.Facebook.facebookTool) {
			NYTD.Facebook.facebookTool.initialize(target, 'top')
		}
        // var postItem = new Element("li").addClassName("facebook");
        // var itemLink = new Element("a", {href:"#"}).update('Facebook');
        // itemLink.style.backgroundImage = "url(" + NYTD.Hosts.imageHost + '/images/article/functions/facebook-dark.gif)';
        // itemLink.style.backgroundRepeat = "no-repeat";
        // itemLink.style.backgroundPosition = "-1px -1px";
        // itemLink.style.padding = '0 0 3px 20px';
        // itemLink.observe("click",  function(e) {
        //   window.open('http://www.facebook.com/sharer.php?u=' + meta.getURL() + '&t=' + meta.getHeadline(), 'facebook', 'toolbar=0,status=0,height=436,width=646,scrollbars=yes,resizable=yes');
        //   s_code_linktrack('Article-Tool-Share-Facebook');
        //   e.stop();
        // });
        // 
        // postItem.appendChild(itemLink);
        // target.insert({top:postItem});
      } 
    }
    
    function addTwitter() {
      var target = $('toolsList');
      if (target) {
        TimesPeople.TwitterTool.initialize(target, 'top')
      }
    }

};

/**
 * Adds permalink / email this ad to passed position and overrides email this form
 * with new data
 *
 * @param string position ADX Position Name
 * @param object form_data New form data as JSON object (keys match to input name)
 */
NYTD.ArticleShareAd = function(position, form_data) {
  var el      = $(position);
  var etaForm = $(document.forms.emailThis);
  if(!el || !etaForm) {
    return;
  }

  function popupPermalink(e) {
    e.stop();
    NYTD.ArticleShareToolsPostToNetwork('permalink', meta);
  }

  function overloadETAForm(e) {
    e.stop();

    etaForm.getElements().each(function(input) {
      if(typeof form_data[input.name] != 'undefined')
      input.setValue(form_data[input.name]);
    });
    etaForm.submit();
  }

  // setup
  var meta = {
    getDescription: function() { return form_data.description },
    getURL: function() { return form_data.url; },
    getHeadline: function() { return form_data.title; },
    getKeywords: function() { return ''; },
    getSection: function() { return 'Advertisement'; },
    getSectionDisplay: function() { return 'Advertisement'; },
    getByline: function() { return '' },
    getSubSection: function() { return ''; },
    getPubdate: function() { return '' }
  };
  var wrapper   = new Element('ul').addClassName('articleAdTools clearfix');
  var permalink = new Element('li').update('<a href="#">Link To This Ad</a>').addClassName('perma')
  var emaillink = new Element('li').update('<a href="#">E-Mail This Ad &#187;</a>').addClassName('email');

  $(permalink.getElementsByTagName('a')[0]).observe('click', popupPermalink.bindAsEventListener());
  $(emaillink.getElementsByTagName('a')[0]).observe('click', overloadETAForm.bindAsEventListener());

  wrapper.insert(permalink);
  wrapper.insert(emaillink);
  el.insert({bottom: wrapper});
};

/**
 * Displays expired advertisement window
 */
NYTD.ArticleShareAdExpiredAlert = function() {
  var body = $(document.getElementsByTagName('body')[0]);
  var bodySize = body.getDimensions();

  var background = new Element('div').setStyle({
    'backgroundColor': '#000000',
    'width': bodySize.width + 'px',
    'height': bodySize.height + 'px',
    'position': 'absolute',
    'top': 0,
    'left': 0,
    'zIndex': 900000
  }).setOpacity('0.7');

  var top = Math.floor((document.documentElement.clientHeight - 90) / 2);
  var left = Math.floor((document.documentElement.clientWidth - 400) / 2);

  var a_alert = new Element('div').update('<p>Sorry, the advertising campaign you are looking for has ended.</p><a href="#" class="close">Close</a>').setStyle({'top': top + 'px', 'left': left + 'px'}).addClassName('expiredAd');

  function removeAlert(e) {
    e.stop();
    background.remove();
    a_alert.remove();
  }

  // needs to be set as onload for MSIE, since DOM hasn't finished with body
  // by the time this is called. sigh.
  Event.observe(window, 'load', function(){
      window.scrollTo(0,0);
      body.appendChild(background);
      body.appendChild(a_alert);
      $(a_alert.getElementsByTagName('a')[0]).observe('click', removeAlert.bindAsEventListener());
  });
};
