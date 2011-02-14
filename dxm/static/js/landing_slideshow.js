

$(function()
{
    var currentSlide = 1;
    var slideout = setTimeout(nextSlide, 5000);
    
    $('#landingSlideshow .controls .page').click(function(){
        gotoSlide($(this).attr('slide'));
        slideout = setTimeout(nextSlide, 10000);
        return false;
    });
    
    
    function gotoSlide(s)
    {
        clearTimeout(slideout);
        currentSlide = s;
            
        switch(currentSlide) {
            case '1':
                $('#landingSlideshow .slide.active').removeClass('active').fadeOut(500, function(){
                    $('#landingSlideshow .slide.one').addClass('active').fadeIn(500);
                    $('#landingSlideshow .controls .page').removeClass('active');
                    $('#landingSlideshow .controls .one').addClass('active');
                });
                break;
                
            case '2':
                $('#landingSlideshow .slide.active').removeClass('active').fadeOut(500, function(){
                    $('#landingSlideshow .slide.two').addClass('active').fadeIn(500);
                    $('#landingSlideshow .controls .page').removeClass('active');
                    $('#landingSlideshow .controls .two').addClass('active');
                });
                break;
                
            case '3':
                $('#landingSlideshow .slide.active').removeClass('active').fadeOut(500, function(){
                    $('#landingSlideshow .slide.three').addClass('active').fadeIn(500);
                    $('#landingSlideshow .controls .page').removeClass('active');
                    $('#landingSlideshow .controls .three').addClass('active');
                });
                break;
        }
    }
    
    function nextSlide() 
    {
        currentSlide ++;
        if (currentSlide == 4) currentSlide = 1;
        gotoSlide(currentSlide + '');
        slideout = setTimeout(nextSlide, 6000);
    }
});
