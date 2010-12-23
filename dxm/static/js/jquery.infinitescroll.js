// Infinite Scroll
(function($) {
    $.fn.infinitescroll = function(options) {
        return $(this).each(function() {
            var el = $(this);
            var settings = $.extend({
                    url: null,
                    triggerAt: 150,
                    page: 2,
                    appendTo: '.list tbody',
                    container: $(document),
                    getParams: ''
                }, options);
            var req = null;
            var maxReached = false;
            var page = 1;

            var infinityRunner = function() {
                if (settings.url !== null) {
                    if  (settings.force || (settings.triggerAt >= (settings.container.height() - el.height() - el.scrollTop()))) {
                        settings.force = false;
                        // if the request is in progress, exit and wait for it to finish
                        if (req && req.readyState < 4 && req.readyState > 0) {
                            return;
                        }
                        $(settings.appendTo).trigger('infinitescroll.beforesend');
                        
                        //elements = $(".status-container .like:not(.active, .inactive)").size();
                        page ++;
                        
                        req = $.get(settings.url, settings.getParams + '&page='+page, function(data) {
                            if (data !== '') {
                                if (settings.page > 1) {
                                    $(settings.appendTo).append(data);
                                } else {
                                    $(settings.appendTo).html(data);
                                }
                                settings.page++;
                                $(el).trigger('infinitescroll.finish');
                            } else {
                                maxReached = true;
                                $(el).trigger('infinitescroll.maxreached');
                            }
                        }, 'html');
                    }
                }
            };
            
            el.bind('infinitescroll.scrollpage', function(e, page) {
                settings.page = page;
                settings.force = true;
                infinityRunner();
            });

            el.scroll(function(e) {
                if (!maxReached) {
                    infinityRunner();
                }
            });

            // Test initial page layout for trigger
            infinityRunner();
        });
    };
})(jQuery);