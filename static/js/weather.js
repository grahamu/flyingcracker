
Array.prototype.has = function(v) {
    // return index of 'v' in the array
    for (i=0; i<this.length; i++) {
        if (this[i]===v)
            return i;
    }
    return false;
}

Array.prototype.next = function(v) {
    // return the next array item after 'v'
    // return the first item if 'v' is last item in the array
    var first = this[0];
    var end = this.length-1;
    for (i=0; i<=end; i++) {
        if (this[i]===v) {
            if (i == end)
                return first;
            else
                return this[i+1];
        }
    }
    return first;
}

function toggleUnits(element) {
    var elements = YAHOO.util.Dom.getElementsByClassName('curr_units', 'span');
    
    if (elements) {
        var state = YAHOO.util.Dom.getStyle(elements[0], 'display');
        if (state == 'none')
            state = '';
        else
            state = 'none';
        YAHOO.util.Dom.setStyle(elements, 'display', state);
        Set_Cookie("curr_weather_show_units", state, 7, '/', '', '');
    }
    element.setAttribute("toggled", element.getAttribute("toggled") != "true");
}

function toggleLabels(element) {
    var elements = YAHOO.util.Dom.getElementsByClassName('curr_title', 'span');
    if (elements) {
        var state = YAHOO.util.Dom.getStyle(elements[0], 'visibility');
        if (state == 'hidden')
            state = 'visible';
        else
            state = 'hidden';
        YAHOO.util.Dom.setStyle(elements, 'visibility', state);
        Set_Cookie("curr_weather_show_titles", state, 7, '/', '', '');
    }
    element.setAttribute("toggled", element.getAttribute("toggled") != "true");
}

var current_weather = {
    
    init: function() {
        current_weather.current = null;     // this holds all current weather data
        current_weather.retrieve_current(); // ask for the latest data
        
        // Grab an elements we'll need so we can fade it later.
        current_weather.weather_div = document.getElementById('curr_weather');
        YAHOO.util.Dom.setStyle(current_weather.weather_div, 'opacity', 1);
        
        // find all temp_value elements, assign a click handler
        current_weather.assign_listener('temp_value', 'curr_weather', current_weather.temp_change_units);
        current_weather.assign_listener('baro_value', 'curr_weather', current_weather.baro_change_units);
        current_weather.assign_listener('speed_value', 'curr_weather', current_weather.speed_change_units);
        
        YAHOO.util.Event.addListener("refresh-button", 'click', current_weather.retrieve_current);
    },
    
    retrieve_current: function() {
        var post_url = '{% url weather-current %}';
        var cObj = YAHOO.util.Connect.asyncRequest('POST', post_url, current_weather.retrieve_current_callback);
    },
    
    retrieve_current_callback: {
        success: function(o) {
            // This turns the JSON string into a JavaScript object.
            try {
                var response_obj = YAHOO.lang.JSON.parse(o.responseText);
            }
            catch (e) {
                alert("Invalid server response in retrieve_current_callback "+o.responseText+", please contact flyingcracker.com")
                alert(e);
            }
            if (response_obj) {
                current_weather.current = response_obj;
                
                // Set up the animation on the results div.
                var weather_fade_out = new YAHOO.util.Anim(current_weather.weather_div,
                    { opacity: { to: 0 } }, 0.5, YAHOO.util.Easing.easeOut);
                
                var weather_fade_in = new YAHOO.util.Anim(current_weather.weather_div,
                    { opacity: { to: 1 } }, 0.5, YAHOO.util.Easing.easeIn);
                
                weather_fade_out.onComplete.subscribe(function() {
                    current_weather.update_all();
                    weather_fade_in.animate();
                    });
                
                weather_fade_out.animate();
            }
        },
    
        failure: function(o) {
            var a = 1; // alert('An error has occurred');
        },
        
        scope: current_weather
    },

    assign_listener: function(cl, root, func) {
        // find all temp_value elements, assign a click handler
        var elements = YAHOO.util.Dom.getElementsByClassName(cl, '', root);
        for (i=0; i<elements.length; i++) {
            YAHOO.util.Event.addListener(elements[i], 'click', func, elements[i]);
        }
    },
    
    temp_change_units: function(e, el) {
        // cycle through the list to the next unit
        current_weather.current.temp_unit = current_weather.current.temp_units.next(current_weather.current.temp_unit);
        current_weather.update_temps();
        current_weather.update_temp_chart();
        unit = current_weather.current.temp_unit;
        Set_Cookie("temp_unit", unit, 7, '/', '', '');
        current_weather.update_server_units('T', unit);
    },
    
    baro_change_units: function(e, el) {
        current_weather.current.baro_unit = current_weather.current.baro_units.next(current_weather.current.baro_unit);
        current_weather.update_baros();
        current_weather.update_baro_chart();
        unit = current_weather.current.baro_unit;
        Set_Cookie("baro_unit", unit, 7, '/', '', '');
        current_weather.update_server_units('B', unit);
    },
    
    speed_change_units: function(e, el) {
        if (current_weather.current.speed_unit != '') {
            current_weather.current.speed_unit = current_weather.current.speed_units.next(current_weather.current.speed_unit);
            current_weather.update_speeds();
            unit = current_weather.current.speed_unit;
            Set_Cookie("speed_unit", unit, 7, '/', '', '');
            current_weather.update_server_units('S', unit);
        }
    },
        
    update_temps: function() {
        var arr = YAHOO.util.Dom.getElementsByClassName('temp_value', '', 'curr_weather');
        var val_index = current_weather.current.temp_units.has(current_weather.current.temp_unit)
        for (i=0; i<arr.length; i++) {
            var parent = arr[i].parentNode;
            unit_els = YAHOO.util.Dom.getElementsByClassName('curr_units', '', parent);
            unit_els[0].innerHTML = current_weather.current.temp_unit;
            switch (parent.id) {
                case 'curr_temp':
                    arr[i].innerHTML = current_weather.current.temp[val_index]+"&#186;"
                    break;
                case 'curr_windchill':
                    arr[i].innerHTML = current_weather.current.windchill[val_index]+"&#186;"
                    break;
                default:
                    break;
            }
        }
    },
        
    update_baros: function() {
        var arr = YAHOO.util.Dom.getElementsByClassName('baro_value', '', 'curr_weather');
        var val_index = current_weather.current.baro_units.has(current_weather.current.baro_unit)
        for (i=0; i<arr.length; i++) {
            var parent = arr[i].parentNode;
            unit_els = YAHOO.util.Dom.getElementsByClassName('curr_units', '', parent);
            unit_els[0].innerHTML = current_weather.current.baro_unit;
            switch (parent.id) {
                case 'curr_baro':
                    arr[i].innerHTML = current_weather.current.baro[val_index]
                    break;
                case 'curr_trend':
                    arr[i].innerHTML = current_weather.current.trend[val_index]
                    break;
                default:
                    break;
            }
        }
    },
        
    update_speeds: function() {
        var arr = YAHOO.util.Dom.getElementsByClassName('speed_value', '', 'curr_weather');
        var val_index = current_weather.current.speed_units.has(current_weather.current.speed_unit)
        for (i=0; i<arr.length; i++) {
            var parent = arr[i].parentNode;
            unit_els = YAHOO.util.Dom.getElementsByClassName('curr_units', '', parent);
            unit_els[0].innerHTML = current_weather.current.speed_unit;
            switch (parent.id) {
                case 'curr_wind':
                    arr[i].innerHTML = current_weather.current.wind[val_index]
                    break;
                default:
                    break;
            }
        }
    },

    update_temp_chart: function() {
        var index = current_weather.current.temp_units.has(current_weather.current.temp_unit)
        el = document.getElementById('curr-temp-block');
        if (el) {
            YAHOO.util.Dom.setStyle(el, 'background', "url("+current_weather.current.temp_chart[index]+") no-repeat top");
        }
    },
    
    update_baro_chart: function() {
        var index = current_weather.current.baro_units.has(current_weather.current.baro_unit)
        el = document.getElementById('curr-barometer-block');
        if (el) {
            YAHOO.util.Dom.setStyle(el, 'background', "url("+current_weather.current.baro_chart[index]+") no-repeat top");
        }
    },
    
    update_charts: function() {
        current_weather.update_temp_chart();
        current_weather.update_baro_chart();
    },
    
    update_data_position: function() {
        el = document.getElementById('curr_temp');
        if (el) {
            if ((current_weather.current.morning == 'false') && YAHOO.util.Dom.hasClass(el, 'chart_am'))
                YAHOO.util.Dom.replaceClass(el, 'chart_am', 'chart_pm');
            else if ((current_weather.current.morning == 'true') && YAHOO.util.Dom.hasClass(el, 'chart_pm'))
                YAHOO.util.Dom.replaceClass(el, 'chart_pm', 'chart_am');
        }
        
        el = document.getElementById('curr_baro');
        if (el) {
            el = el.parentNode;
            if ((current_weather.current.morning == 'false') && YAHOO.util.Dom.hasClass(el, 'chart_am'))
                YAHOO.util.Dom.replaceClass(el, 'chart_am', 'chart_pm');
            else if ((current_weather.current.morning == 'true') && YAHOO.util.Dom.hasClass(el, 'chart_pm'))
                YAHOO.util.Dom.replaceClass(el, 'chart_pm', 'chart_am');
        }
    },
    
    update_all: function() {
        var el = document.getElementById('curr_timestamp');
        if (el) {
            el.innerHTML = current_weather.current.timestamp;
        }
        current_weather.update_temps();
        current_weather.update_baros();
        current_weather.update_speeds();
        
        el = document.getElementById('curr_humidity');
        if (el) {
            el.innerHTML = current_weather.current.humidity+"%";
        }
        
        el = document.getElementById('curr_wind');
        if (el) {
            if (current_weather.current.wind_dir != null) {
                YAHOO.util.Dom.setStyle(el, 'background', "url(/static/img/"+current_weather.current.wind_dir+") no-repeat top");
            }
            else {
                YAHOO.util.Dom.setStyle(el, 'background', "none");
            }
        }
        current_weather.update_data_position();
        current_weather.update_charts();
    },
    
    update_server_units: function(type, unit) {
        // async call to server
        var post_url = '{% url weather-unit-change %}';
        var post_data = "type=" + type;
        post_data += "&unit=" + unit;
        var cObj = YAHOO.util.Connect.asyncRequest('POST', post_url, current_weather.update_server_callback, post_data);
    },
    
    update_server_callback: {
        success: function(o) {
            ;   // dont care about response
        },
    
        failure: function(o) {
            ;
        }
    }
};

YAHOO.util.Event.addListener(window, 'load', current_weather.init);

