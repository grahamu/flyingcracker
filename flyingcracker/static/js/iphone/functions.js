(function() {
    var currentWidth = 0;
    var checkTimer;
    
    addEventListener("load", function(event) {
        setTimeout(checkOrientAndLocation, 100);
    }, false);
    
    checkTimer = window.setInterval(checkOrientAndLocation, 300);
    
    function checkOrientAndLocation() {
        if (window.innerWidth != currentWidth) {
            currentWidth = window.innerWidth;
            var orient = currentWidth < 480 ? "portrait" : "landscape";
            if (document.body) {
                document.body.setAttribute("orient", orient);
            }
            setTimeout(function() {	window.scrollTo(0,1); },100);
        }
    }
})();

function menuToggle() {
	curr = document.getElementById('menuBar').className;
	if (curr == 'toolBar open') {
        document.getElementById('menuBar').className = 'toolBar closed';
    }
	else if (curr == 'toolBar closed') {
        document.getElementById('menuBar').className = 'toolBar open';
    }
}
