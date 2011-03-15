/* $Id: articleCommentCount.js 30909 2010-02-05 16:19:17Z patras $
/js/app/article/articleCommentCount.js
(c) 2009 The New York Times Company */

NYTD.require('/js/app/lib/NYTD/0.0.1/template.js');

/* Used by article template v 700, >= July 2009 */
NYTD.ArticleCommentCount = function(){
    // settings
    var assetUrl        = window.location.hostname + window.location.pathname;
    var assetId         = getMetaTagValue('articleid');
    var requestObject   = encodeURIComponent('{"userContentSummary":{"request":{"requestType":"UserContentSummary","status":"was-approved","url":"http://' + assetUrl + '","excerpt":"1"},"response":{}}}');
    var serviceUri      = '/svc/community/V2/requestHandler';
    var api             = {};
    
    // get count spans in article tools
    var toolCounts      = $$('.articleTools .commentCount');
    toolCounts          = (toolCounts.length > 0) ? toolCounts : $$('#commentCount'); // backwards compatability
    var readerComment   = $('readerscomment');
    
    var readerHtml      = '\
    <h3>Readers\' Comments</h3>\
    <div class="content">\
        <blockquote><%= msg %></blockquote>\
        <% if(cite !== false) { %>\
            <cite><%= cite %></cite>\
        <% } %>\
        <ul class="more">\
            <% if(cite !== false) { %>\
                <li><a href="<%= url %>?permid=<%= commentId %>#comment<%= commentId %>" rel="2v">Read Full Comment &#187;</a></li>\
                <% if (canSubmit == true) { %>\
                    <li><a href="<%= url %>#postComment" rel="2p">Post a Comment &#187;</a></li>\
                <% } %>\
            <% } else { %>\
                <% if (canSubmit == true) { %>\
                    <li><a href="<%= url %>#postComment" rel="2p">Post a Comment &#187;</a></li>\
                    <% if(count > 0) { %>\
                        <li><a href="<%= url %>" rel="3v">Read All Comments (<%= count %>) &#187;</a></li>\
                    <% } %>\
                <% } else { %>\
                    <li><a href="<%= url %>" rel="3v">Read All Comments <% if (count > 0) { %>(<%= count %>)<% } %> &#187;</a></li>\
                <% } %>\
            <% } %>\
        </ul>\
    </div>';
    
    function updateFromRequest(transport) {
        var json    = transport.responseText.strip().evalJSON();
        var obj     = json.userContentSummary.response.UserContentSummary;
        var count   = (obj.commentCount) ? obj.commentCount : 0;
        var showBox = (readerComment !== null && (obj.excerpts || obj.commentQuestion || obj.canSubmit));

        if(count > 0) {
            toolCounts.invoke('update', '(' + count + ')');
        }
        
        // Showing "blue box"
        if(showBox) {
            var excerpt         = (obj.hasExcerpt) ? obj.excerpts[0] : false;
            var communityHost   = (obj.communityHost) ? obj.communityHost : 'http://community.nytimes.com';            
            var values          = {
                url:            communityHost + '/comments/' + assetUrl,
                count:          count,
                msg:            '',
                canSubmit:      obj.canSubmit,
                commentId:      (excerpt) ? excerpt.commentSequence : 0,
                cite:           false
            };

            if(excerpt) {
                values.msg  = '"' + excerpt.commentExcerpt + '"'
                values.cite = (excerpt.display_name.length > 0 && excerpt.location.length > 0) ?
                    excerpt.display_name + ', ' + excerpt.location : false;
            } else if ( obj.commentQuestion && obj.canSubmit ) {
                values.msg = obj.commentQuestion;
            } else {
                values.msg = 'Readers shared their thoughts on this article.';
            }

            var output = NYTD.Template(readerHtml, values);
            readerComment.update(output);
            
            // attach tracking
            readerComment.select('a').each(function(anchor){
                switch(anchor.readAttribute('rel')) {
                    case '2v':
                        anchor.observe('click', dcsMultiTrack.bind('DCS.dcssip','www.nytimes.com','DCS.dcsuri','/article comments/view-promo2.html','WT.ti','Article Comments View Promo2','WT.z_aca','Promo2-View','WT.gcom','Com'));
                        break;
                    case '2p':
                        anchor.observe('click', dcsMultiTrack.bind('DCS.dcssip','www.nytimes.com','DCS.dcsuri','/article comments/post-promo2.html','WT.ti','Article Comments Post Promo2','WT.z_aca','Promo2-Post','WT.gcom','Com'));
                        break;
                    case '3v':
                        anchor.observe('click', dcsMultiTrack.bind('DCS.dcssip','www.nytimes.com','DCS.dcsuri','/article comments/view-promo3.html','WT.ti','Article Comments View Promo3','WT.z_aca','Promo3-View','WT.gcom','Com'));
                        break;
                }
            });
        }
    }
    
    function showDefault() {
        // Showing default blue box           
        var values          = {
            url:           '/comments/' + assetUrl,
            count:          0,
            msg:            'Share your thoughts.',
            canSubmit:      true,
            cite:           false
        };

        var output = NYTD.Template(readerHtml, values);
        readerComment.update(output);
    }
    
    api.update = function(){
        new Ajax.Request(serviceUri, {
            'method':       'post',
            'parameters':   'requestData=' + requestObject,
            'onSuccess':    updateFromRequest,
            'onFailure':    showDefault
        });
    }
    
    api.update();
    return api;
}

Event.observe(window, 'load', function(){
    var acm = new NYTD.ArticleCommentCount(); 
});
