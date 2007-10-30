var current_weather = {
    init: function() {
        // Grab the elements we'll need.
        current_weather.weather_div = document.getElementById('CurrentWeather');
        
        // This is so we can fade it later.
        YAHOO.util.Dom.setStyle(current_weather.weather_div, 'opacity', 1);
        
        // Ask for data every so often.
        setInterval(current_weather.refresh_func, 300000);  // 5 minutes
    },
    
    refresh_func: function() {
        var cObj = YAHOO.util.Connect.asyncRequest('POST', '/weather/?xhr', current_weather.ajax_callback);
    },
    
    ajax_callback: {
        success: function(o) {
            // This turns the JSON string into a JavaScript object.
            var response_obj = eval('(' + o.responseText + ')');
            
            // Set up the animation on the results div.
            var weather_fade_out = new YAHOO.util.Anim(current_weather.weather_div,
                { opacity: { to: 0 } }, 0.5, YAHOO.util.Easing.easeOut);
            
            var weather_fade_in = new YAHOO.util.Anim(current_weather.weather_div,
                { opacity: { to: 1 } }, 0.5, YAHOO.util.Easing.easeIn);

			var val_timestamp = document.getElementById('current_timestamp');
            var val_temp = document.getElementById('current_temp');
            var val_humidity = document.getElementById('current_humidity');
            var val_barometer = document.getElementById('current_barometer');
            
            weather_fade_out.onComplete.subscribe(function() {
				val_timestamp.innerHTML = response_obj.timestamp;
				val_temp.innerHTML = response_obj.temp;
                val_humidity.innerHTML = response_obj.humidity;
                val_barometer.innerHTML = response_obj.barometer;
                weather_fade_in.animate();
                });
            
            weather_fade_out.animate();
        },
    
        failure: function(o) {
            var a = 1; // alert('An error has occurred');
        }
    
    }
};
YAHOO.util.Event.addListener(window, 'load', current_weather.init);