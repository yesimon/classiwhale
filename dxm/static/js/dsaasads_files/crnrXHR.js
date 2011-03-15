/*
$Id: crnrXHR.js 19911 2009-06-01 20:00:51Z pkarthik $
(c)2006 - 2007 The New York Times Company  */

function crnrXHR(){
	this.xhr = this.getXHRobject();
	this.serviceURL = "/svc/community/V2/requestHandler";
	this.responseData = null;
	this.requestData = null;
	this.callbacks = []; //array of functions to be called when new responses come in
	return this;
}

crnrXHR.prototype.getXHRobject = function() {
	var r = false;
        try {
       		r = new XMLHttpRequest();
        } catch (trymicrosoft) {
       		try {
               		r = new ActiveXObject("Msxml2.XMLHTTP");
		} catch (othermicrosoft) {
               		try {
                       		r = new ActiveXObject("Microsoft.XMLHTTP");
                        } catch (failed) { /* do nothing */ }
                }
        }
        return r;
}

crnrXHR.prototype.send = function(){
	if (this.xhr) {
		var myxhr = this; // handle to crnrXHR object
		this.xhr.open("post",this.serviceURL, true);
		this.xhr.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
		this.xhr.send(this.requestData);
		this.xhr.onreadystatechange = function() { myxhr.respond() };
	}
}

crnrXHR.prototype.respond = function(){
	if ((this.xhr.readyState == 4) && (this.xhr.status == 200)) {
		//cache response 
		this.responseData = eval("(" + this.xhr.responseText + ")");

		// invoke any callback functions
		for (var i=0; i < this.callbacks.length; i++){
			this.callbacks[i]();
		}

		// reset callbacks
		this.callbacks.length=0;
	} 
}
