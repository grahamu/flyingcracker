/**
 * Requires the following scripts & css
 * <script type="text/javascript" src="http://yui.yahooapis.com/2.2.2/build/yahoo-dom-event/yahoo-dom-event.js"></script>
 * <script type="text/javascript" src="http://yui.yahooapis.com/2.2.2/build/logger/logger-min.js"></script> 
 * <link type="text/css" rel="stylesheet" href="http://yui.yahooapis.com/2.2.2/build/logger/assets/logger.css"> 
 */

YAHOO.namespace("extension");

YAHOO.extension.Debugger = function(id, cfg) {
	this.init(id, cfg);
};

YAHOO.extension.Debugger.prototype = {	
	init: function(id, cfg) {
		YAHOO.extension.Debugger.debug = this;
		var logReader = new YAHOO.widget.LogReader(null, {
				left: "30%", 
				top: "100px", 
				width: "400px",
				draggable: true,
				outputBuffer: 100,
				newestOnTop:false
		});
		logReader.formatMsg = function(oLogMsg) {
		      var category = oLogMsg.category;
		      return '<p><span class="'+category+'">'+category+'</span> '+ oLogMsg.msg+'</p>';
		};
		YAHOO.widget.Logger.reset();
		var inputDiv = document.createElement("div");
		logReader._elContainer.appendChild(inputDiv);
		inputDiv.innerHTML = '<form onsubmit="YAHOO.extension.Debugger.debug.evalit();return false;"><input style="width:330px;font-size:122%" type="text" id="jsinput"/><input type="button" value="OK" style="margin-left:10px;" onclick="YAHOO.extension.Debugger.debug.evalit()"/></form>';
	},
	
	evalit: function(evalStr) {

		if(!evalStr) {
			var inp = YAHOO.util.Dom.get("jsinput");
			evalStr = inp.value;
			inp.value = "";
		}
		try {
			YAHOO.log(YAHOO.extension.Debugger.debug.globaleval(evalStr));
		} catch (e) {
			YAHOO.log(e);
		}
		return false;		
	},

	// This should execute the eval in the global scope
	globaleval: function(evalStr) {
		YAHOO.log(evalStr);
		var result = window.eval(evalStr);

		if(typeof(result) == "object") {

			// go through and dump the properties
			var props = "<p>{</p>"; //variable which will hold property values
			for(prop in result)
			{
				if(typeof (result[prop]) != "function"){
					//result[prop].toJSONString();
					if(typeof(result[prop]) == "object") {
						props += '<p><a href="#" onclick="YAHOO.extension.Debugger.debug.evalit(\'' + evalStr + '.' + prop + '\')">' + prop + '</a>' + ':' + result[prop]+ '</p>';
					} else {
						props += '<p><strong>' + prop + '</strong>:' + result[prop]+ '</p>';
					}
				}
			}
			props += "<p>}</p>"
			return props;

		} else {

			if (typeof(result) == "undefined") {
				return "";
			} else {
				return result;
			}
		}
	}
};


