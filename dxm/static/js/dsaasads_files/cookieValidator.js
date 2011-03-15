/**
 $Id: cookieValidator.js 52744 2010-12-13 20:41:38Z vishal $
 author: Aditya
 used to validate the cookie for email tool
 */
var NYTD = window.NYTD || {};
NYTD.email = {};

NYTD.email.CookieValidation = Class.create({
    initialize: function(){
        this.url = '/mem/emailthis/validateUser';
        this.methodName = 'post';
    },
    validate: function(requestData){            
	    var referenceObj = this;
            var request = new Ajax.Request(this.url, {
            method: this.methodName,
            parameters: requestData,
            onSuccess: function(transport){
            },
            onFailure: function(transport){
                      referenceObj.redirectToLogin(requestData.hostName,requestData.fallBackUrl);
            },
            onException: function(transport, exception){
                     referenceObj.redirectToLogin(requestData.hostName,requestData.fallBackUrl);
            },
            onComplete: function(transport){
				var json_obj = transport.responseText.evalJSON(true);
                try {
                   if(json_obj.status == '1') {
					   referenceObj.formSubmit(this.requestParams.formName);
				   } else {
				   	   referenceObj.redirectToLogin(requestData.hostName,requestData.fallBackUrl);  
				   }
                } catch (e) {
					   referenceObj.redirectToLogin(requestData.hostName,requestData.fallBackUrl);
                }
            }
        });
    },
	redirectToLogin: function(hostName,fallBackUrl) {
		window.location = 'http://'+hostName+'/auth/login?URI='+fallBackUrl;
	},
	formSubmit: function(formName) {
		var form = $('emailThis') || $('emailThisForm');
		form && form.submit();
		if (formName) { 
		    $(formName).submit();
		}
	}
});

Event.observe(window, 'load', function(){
var element;
if($$('a#emailThis')[0]) {
   element = $$('a#emailThis')[0];
} else if($$('a#emailThisLink')[0]) {
   element = $$('a#emailThisLink')[0];
}
if( element ) {
element.href = "javascript:void(0);";
var baseUrl = window.location.hostname;
Event.observe(element, 'click', function(event){
        requestParams = {
            fallBackUrl: window.location,
            hostName: 'www.nytimes.com',
            baseUrl: 'http://'+baseUrl
        }
        var validationObj = new NYTD.email.CookieValidation();
        validationObj.validate(requestParams);
});
}
});