/* $Id: mothController.js 46051 2010-09-23 18:51:19Z donohoe $ */

/* class for the slide player */
NYTD.MOTH = function(mothContainerId, visibleAtOnce, scrollIncrementAmount, alternateImageSource) {
	if (window.browser && (window.browser instanceof InsideNYTimesBrowser)) {return;}
	var totalColumns, imagesLoaded = false, firstRowCells = $$("#"+mothContainerId+" tr:first-child td"), allCells = $$("#"+mothContainerId+" td");
	var itemIndex = 0;
	var imgSrc    = alternateImageSource || "http://graphics8.nytimes.com/images/global/buttons/";
	var distance  = $$("#insideNYTimesBrowser td").first().offsetWidth + 1;
	var images    = { leftOff: "moth_reverse_off.gif", leftOn: "moth_reverse.gif", rightOff: "moth_forward_off.gif", rightOn: "moth_forward.gif" };
	var isTouch   = (typeof document.ontouchmove == "object") || location.hash.indexOf('isTouch')>0;

	this.load = function() {
		allCells.invoke("removeClassName","hidden");
		totalColumns = firstRowCells.length;
		if (isTouch) {
			this.addSwipe();
		} else {
			this.activateButtons();
			this.showButtons();
		}
		$("insideNYTimesScrollWrapper").scrollLeft = 0; 
	};

	function tooFarRight() {
		return itemIndex + visibleAtOnce >= totalColumns;
	}

	function tooFarLeft() {
		return itemIndex == 0;
	}

	function loadUnloadedImages() {
		if (imagesLoaded) return;
		$$("#"+mothContainerId+" td").each(function(td){
			var span = td.select('span.img[src]')[0];
			if (span) {
				var image = new Element("img", {
					src:    span.getAttribute("src"),
					alt:    span.getAttribute("alt"),
					height: span.getAttribute("height"),
					width:  span.getAttribute("width")
				});
				span.up("a").insert(image);
			}
			if (isTouch) {
				td.removeClassName('hidden');
			}
		});
		imagesLoaded = true;
	}

	this.activateButtons = function() {
		$("mothReverse").observe('click', this.goLeft.bind(this));
		$("mothForward").observe('click', this.goRight.bind(this));
	};

	this.disableButtons = function() {
		$("mothReverse").stopObserving('click');
		$("mothForward").stopObserving('click');
	};

	this.showButtons = function() {
		$("mothReverse").src = tooFarLeft()  ? imgSrc + images.leftOff  : imgSrc + images.leftOn;
		$("mothForward").src = tooFarRight() ? imgSrc + images.rightOff : imgSrc + images.rightOn;
	};

	this.goRight = function() {
		if (tooFarRight()) return;
		this.disableButtons();
		itemIndex += scrollIncrementAmount;
		this.update("right");
	};

	this.goLeft = function() {
		if (tooFarLeft()) return;
		this.disableButtons();
		itemIndex -= scrollIncrementAmount;
		this.update("left");
	};

	this.update = function(direction) {
		loadUnloadedImages();
		var incrementAmount = (direction == "right") ? distance : - distance;
		var that = this;
		new Effect.Scroll($("insideNYTimesScrollWrapper"), {
			x: incrementAmount,
			y: 0,
			mode: 'relative',
			duration: 0.4,
			afterFinish: function() { that.activateButtons(); } });
		this.showButtons();
	};

	this.addSwipe = function() {

		var nav = $('insideNYTimesHeader').select('.navigation')[0];
		if (nav) { nav.remove(); }

		var moth = $(mothContainerId);
		moth.style.width = moth.getWidth() + "px";

		loadUnloadedImages();
		var sc = new iScroll(mothContainerId, { scrollbarClass: 'mothTouchScroll', vScrollBar: false, hScrollBar: false, checkDOMChanges: false });
	};
};

Event.observe(window, 'load', function(){
	var insideNYT = $('insideNYTimesBrowser');
	if (insideNYT) {
		var count = insideNYT.down(1).select("td").select(function(cell) { return cell.getStyle("display") != "none"; }).length;
		var moth = new NYTD.MOTH("insideNYTimesBrowser", count, 1).load();
	}
});
