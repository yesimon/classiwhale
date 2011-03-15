/*
 * $Id: common.js 55828 2011-01-20 20:10:14Z santep $
 * (c) 2006-2010 The New York Times Company
 */

(function(){if(window.location.protocol==="http:"){var c=String(String.fromCharCode(97+Math.round(Math.random()*25))+(new Date).getTime()),d=document.getElementsByTagName("head")[0],b,e=function(a){if(a&&a.counted){b=document.createElement("meta");b.name="WT.z_cad";b.content="1";d.appendChild(b);}window[c]=null};(function(){var a=document.createElement("script"),f="http://meter-svc.nytimes.com/meter.js?url="+encodeURIComponent(location.href)+"&referer="+encodeURIComponent(document.referrer)+"&callback="+ c;window[c]=e;a.src=f;a.type="text/javascript";d.appendChild(a)})()}})();

var _sf_startpt=(new Date()).getTime();

function nameIt() {
    window.name = 'nytimesmain';
    if ((navigator.appName == "Microsoft Internet Explorer") && (document.all.globalsearchform)){
        document.all.globalsearchform.style.visibility = "visible";
    }
}
 
function pop_me_up(pURL, features){
    new_window = window.open(pURL, "popup_window", features);
    new_window.focus();
}

function pop_me_up2(pURL,name, features){
    new_window = window.open(pURL, name, features);
    new_window.focus();
}

function changeImage(image_name, image_src) {
    document.images[image_name].src = image_src;
}

function goToURL(obj){
    var f = (obj.section) ? obj : obj.form;
    var selected = f.section.selectedIndex;
    var URL = f.section.options[selected].value;
    if (URL != "") document.location = URL;
    return false;
}

function goToURL2(sel){
// This only works for onChange events from select objects
// but select object can have any name, unlike goToURL() which requires 
// select object to be named "section"
    var selected = sel.selectedIndex;
    var url = sel.options[selected].value;
    if (url != "") document.location = url;
    return false;
}

/* bust all external framesets 
 * but save the original referrer for WebTrends
 */
(function() {
    if (window.self != window.top && !document.referrer.match(/^https?:\/\/[^?\/]+\.nytimes\.com\//)) {
        var expTime = new Date();
        expTime.setTime(expTime.getTime() + 60000); // 1 min
        document.cookie = "FramesetReferrer=" + document.referrer + "; expires=" + expTime.toGMTString() + "; path=/";
        top.location.replace(window.location.pathname);
    }
})();

//  Begin functions for Travel flash slideshows
function writeFlashSlideShow(xmlFile){
    var swfFile = "/slideshow/swf/slideshow.swf?XMLfile=/slideshow/xml/travel/" + xmlFile;
    var HTMLstr = "";
    HTMLstr += "<object classid=\"clsid:d27cdb6e-ae6d-11cf-96b8-444553540000\" codebase=\"http://fpdownload.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,0,0\" width=\"390\" height=\"300\" id=\"slideshow\" align=\"middle\">";
    HTMLstr += "<param name=\"allowScriptAccess\" value=\"sameDomain\" />";
    HTMLstr += "<param name=\"movie\" value=\"" + swfFile + "\" />";
    HTMLstr += "<param name=\"quality\" value=\"high\" />";
    HTMLstr += "<param name=\"wmode\" value=\"transparent\" />";
    HTMLstr += "<embed src=\"" + swfFile + "\" wmode=\"transparent\" quality=\"high\" width=\"390\" height=\"300\" name=\"slideshow\" align=\"middle\" allowScriptAccess=\"sameDomain\" type=\"application/x-shockwave-flash\" pluginspage=\"http://www.macromedia.com/go/getflashplayer\" />";
    HTMLstr += "</object>";
    return HTMLstr;
}

function showFirstSlide(imgName, photoCredit, photoCaption){
    var HTMLstr = "";
    HTMLstr += "<!-- begin photo -->";
    HTMLstr += "<img src=\"http://graphics.nytimes.com/images/section/travel/slideshow/" + imgName + "\" width=\"390\" height=\"200\" alt=\"photo\" border=\"0\">";
    HTMLstr += "<!-- end photo -->";
    HTMLstr += "<div align=\"right\" class=\"photocredit\">" + photoCredit + "</div>";
    HTMLstr += "<div class=\"photocaption\">" + photoCaption + "</div>";
    return HTMLstr;
}
//  End functions for Travel flash slideshows

//  Begin functions for Global flash slideshows
function writeEmbeddedFlashSlideShow(xmlFile){
    var swfFile = "/slideshow/swf/slideshow.swf?XMLfile=/slideshow/xml/" + xmlFile;
    var HTMLstr = "";
    HTMLstr += "<object classid=\"clsid:d27cdb6e-ae6d-11cf-96b8-444553540000\" codebase=\"http://fpdownload.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,0,0\" width=\"390\" height=\"300\" id=\"slideshow\" align=\"middle\">";
    HTMLstr += "<param name=\"allowScriptAccess\" value=\"sameDomain\" />";
    HTMLstr += "<param name=\"movie\" value=\"" + swfFile + "\" />";
    HTMLstr += "<param name=\"quality\" value=\"high\" />";
    HTMLstr += "<param name=\"wmode\" value=\"transparent\" />";
    HTMLstr += "<embed src=\"" + swfFile + "\" wmode=\"transparent\" qualityaigh\" width=\"390\" height=\"300\" name=\"slideshow\" align=\"middle\" allowScriptAccess=\"sameDomain\" type=\"application/x-shockwave-flash\" pluginspage=\"http://www.macromedia.com/go/getflashplayer\" />";
    HTMLstr += "</object>";
    return HTMLstr;
}

function showFirstEmbeddedSlide(imgName, photoCredit, photoCaption){
    var HTMLstr = "";
    HTMLstr += "<!-- begin photo -->";
    HTMLstr += "<img src=\"" + imgName + "\" width=\"390\" height=\"200\" alt=\"photo\" border=\"0\">";
    HTMLstr += "<!-- end photo -->";
    HTMLstr += "<div align=\"right\" class=\"photocredit\">" + photoCredit + "</div>";
    HTMLstr += "<div class=\"photocaption\">" + photoCaption + "</div>";
    return HTMLstr;
}
//  End functions for Global flash slideshows

function preloadNavImages(imageNames, imagePath){
    var loadedImages = new Array();
    if (document.images) {
        for (var i=0; i < imageNames.length; i++){
            loadedImages[i] = new Image();
            loadedImages[i].src = imagePath + "nav_" + imageNames[i] + "_off.gif";
        }
    }

}

function readCookie(value){
    var allCookieVals = document.cookie.split(";");
    for (var i=0; i < allCookieVals.length; i++){ //loop through all cookies
        if (allCookieVals[i].indexOf(value) != -1) { //find target cookie
            var cookieVal = allCookieVals[i].split("="); //split name/value pair
            return cookieVal[1]; //return target cookie value
        }
    }
}

function expandMultimediaWindow(){
    if (window.resizeTo && window.moveTo) {
        window.resizeTo(screen.availWidth, screen.availHeight);
        window.moveTo(0,0);
    }
}

function shrinkMultimediaWindow(w,h){
    if (window.resizeTo) window.resizeTo(w,h);
    if (window.moveTo) {
        var winX = ((screen.availWidth/2) - (w/2));
        var winY = ((screen.availHeight/2) - (h/2));
        window.moveTo(winX,winY);
    }
}

function ieXLiquidWidth() {
    if (document.body.clientWidth < 774) {
        return "768px";
    } else if (document.body.clientWidth > 984) {
        return "980px";
    } else {
        return "auto";
    }
}

function setClientSizeCookies() {
    var client_w = document.body.clientWidth;
    var path = "/";
    var domain = "nytimes.com";
    document.cookie = "client_w=" + client_w + "; path= " + path + "; domain=" + domain;
}

//  Function for Classifieds and Most Popular modules
function Accordian(target) {
    typeof target == "object" ? this.element = target : this.element = document.getElementById(target); if (!this.element) return false;
    this.ul = this.element.getElementsByTagName("ul")[0];
    this.tabs = this.ul.getElementsByTagName("li");
    this.tabContent = this.getTabContent();
    this.bind();
}

Accordian.prototype.getTabContent = function() {
    tabContent= new Array();
    this.divs = this.element.getElementsByTagName("div");
    for (var i = 0; i < this.divs.length; i++) {
        if (/tabContent/i.test(this.divs[i].className)) {
            tabContent.push(this.divs[i]);
        }
    }
    return tabContent;
};

Accordian.prototype.bind = function() {
    var o = this;
    for (var i = 0; i < this.tabs.length; i++) {
        this.tabs[i].onclick = function() {
            if (this.className != 'selected') {
                o.open(this); return false;
                var a = this.getElementsByTagName("a")[0];
                if (a) a.onclick = function() {
                    return false;
                };
            }
        };
    }
};

Accordian.prototype.open = function(caller) {
    for (var i = 0; i < this.tabs.length; i++) {
        var tab = this.tabs[i];
        if (tab == caller) {
            this.collapse();
            tab.className = "selected";
            this.tabContent[i].style.display = "block";
        }
    }
};

Accordian.prototype.collapse = function() {
    for (var i = 0; i < this.tabs.length; i++) {
        this.tabs[i].className = "";
        this.tabContent[i].style.display = "none";
    }
};

// Function for Google ads links

function linkbox(url, winName) {
    window.open(url, winName, "location=yes,directories=yes,menubar=yes,toolbar=yes,status=yes,resizable=yes,scrollbars=yes");
}

function enhanceAccordians() {
    var divs = document.getElementsByTagName('div');
    for (var i = 0; i < divs.length; i++) {
        var element = divs[i];
        if (/accordian/i.test(element.className)) {
            new Accordian(element);
        }
    }
}

getMetaTagValue = function(name){
    if (document.getElementsByTagName) {
        var meta = document.getElementsByTagName("meta");
        for (var i=0; i < meta.length; i++) {
            if (meta[i].name == name) return meta[i].content;
        }
    }
};

var NYTD = NYTD || {};

NYTD.Hosts = (function(){
    var host, scripts = document.getElementsByTagName("script");
    for (var i = 0, script; script = scripts[i]; i++) {
        host = script.src && /^(.+\.nytimes.com)\/js\/common\.js/.test(script.src) ? RegExp.$1 : '';
        if (host) { break; };
    };

    var jsonHost = (host.indexOf('graphics8.nytimes.com') !== -1) ?
    'http://json8.nytimes.com' :
    'http://json.stg.nytimes.com';
    
    var wwwHost = (host.indexOf('graphics8.nytimes.com') !== -1) ? 'http://www.nytimes.com' : 'http://swww.nytimes.com'

    return {
        imageHost: host,
        jsHost: host,
        cssHost: host,
        jsonHost: jsonHost,
        wwwHost: wwwHost
    };
})();

// Duped in trackingTags_v1.1.js
(function(){

    var windowLoaded = false;
    var document_scripts;

    if (window.addEventListener) {
        window.addEventListener ("load", function(){ windowLoaded = true; }, false);
    } else if (window.attachEvent) {
        window.attachEvent ("onload", function(){ windowLoaded = true; });
    }

    function scriptLoaded(src) {
        document_scripts = document_scripts || {};
        if (document_scripts[src]) { return true; }
        else {
            var script_tags= document.getElementsByTagName("script");
            for (var i = 0, script; script = script_tags[i]; i++) {
                if(script.src) { document_scripts[script.src] = 1; }
            };
            if (document_scripts[src]) { return true; }
            else { return false; }
        }
    }

    NYTD.require = function(file, callback) {
        if (windowLoaded) { throw('Cannot require file, document is already loaded'); }
    //  If matches root relative url (single slash, not protocol-agnostic double slash)
        var url = /^\/[^\/]/.test(file) ? NYTD.Hosts.jsHost + file : file;
        var force = arguments[arguments.length - 1] === true;
        var needsCallbackScriptTag;

        if (force || !scriptLoaded(url)) {
            document.write('<script src="' + url + '" type="text/javascript" charset="utf-8" onerror="throw(\'NYTD.require: An error occured: \' + this.src)"><\/script>');
            document_scripts[url] = 1;
            needsCallbackScriptTag = true;
        }

        if (typeof callback == 'function') {
            if (document.addEventListener) {
                if (needsCallbackScriptTag) {
                    document.write('<script type="text/javascript" charset="utf-8">(' + callback.toString() + ')();<\/script>');
                } else {
                    window.setTimeout(function(){
                        callback();
                    }, 0);
                }
            } else {
                NYTD.require.callbacks = NYTD.require.callbacks || [];
                NYTD.require.callbacks.push(callback);
                NYTD.require.callbacks.count = (++NYTD.require.callbacks.count) || 0;
                document.write("<script id=__onAfterRequire" + NYTD.require.callbacks.count + " src=//:><\/script>");
                document.getElementById("__onAfterRequire" + NYTD.require.callbacks.count).onreadystatechange = function() {
                    if (this.readyState == "complete") {
                        this.onreadystatechange = null;
                        (NYTD.require.callbacks.pop())();
                        this.parentNode.removeChild(this);
                    }
                };
            }
        }
    };
})();

NYTD.require('/js/app/lib/env.js');

if (!window.location.hostname.match('monster')) {
    NYTD.require('/js/app/lib/prototype/1.6.0.2/prototype.js');
    NYTD.require('/js/app/lib/NYTD/0.0.1/template.js');
    NYTD.require('/js/adx/googleads.js');
}

if (!window.TimesPeople) {
    NYTD.require('/js/app/timespeople_1.5/lib/urilist.js');
    NYTD.require('/js/app/timespeople/toolbar/1.7/boot.js');
    NYTD.require('/js/app/timespeople/activities/1.6/boot.js');
}

(function() {
    var PT  = false;
    var PST = false;
    var metas = document.getElementsByTagName('meta');

    for (var i = 0, meta; meta = metas[i]; i++) {
        PT  = (meta.name == 'PT')  ? meta.content : PT;
        PST = (meta.name == 'PST') ? meta.content : PST;
        if (PT && PST) break;
    }

    if (PT === 'Article'){
        NYTD.require("/js2/lib/facebook/article/1.0/build.min.js");
    }

    if (PT === 'Article' || PST === 'Blog Post'){
        NYTD.require("/js/app/common/swipe/navigate.min.js");
        NYTD.require("/js/app/common/emphasis/app.js");
    }
})();
