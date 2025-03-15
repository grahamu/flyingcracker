/**
 * Modern weather utilities to replace YUI-based functionality
 */
document.addEventListener('DOMContentLoaded', () => {
    // Initialize Alpine.js data
    window.weatherData = {
        showTitles: localStorage.getItem('showTitles') === 'true',
        showUnits: localStorage.getItem('showUnits') === 'true',
        loading: false,

        toggleUnits() {
            this.showUnits = !this.showUnits;
            localStorage.setItem('showUnits', this.showUnits);

            // Update all units display
            document.querySelectorAll('.curr_units').forEach(el => {
                el.style.display = this.showUnits ? 'inline' : 'none';
            });
        },

        toggleTitles() {
            this.showTitles = !this.showTitles;
            localStorage.setItem('showTitles', this.showTitles);

            // Update all titles visibility
            document.querySelectorAll('.curr_title').forEach(el => {
                el.style.visibility = this.showTitles ? 'visible' : 'hidden';
            });
        },

        async refreshWeather() {
            this.loading = true;

            try {
                // Show loading overlay
                document.getElementById('weather-loading').classList.remove('hidden');

                // Make AJAX request using fetch instead of YAHOO.util.Connect
                const response = await fetch('/weather/current/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken() // Function to get CSRF token
                    }
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();

                // Update the weather content with a smooth transition
                const weatherDiv = document.getElementById('curr_weather');

                // Fade out
                fadeOut(weatherDiv, 300, () => {
                    // Update content
                    this.updateWeatherContent(data);

                    // Fade in
                    fadeIn(weatherDiv, 300, () => {
                        document.getElementById('weather-loading').classList.add('hidden');
                        this.loading = false;
                    });
                });
            } catch (error) {
                console.error('Error refreshing weather:', error);
                document.getElementById('weather-loading').classList.add('hidden');
                this.loading = false;
            }
        },

        updateWeatherContent(data) {
            // Update timestamp
            document.getElementById('curr_timestamp').textContent = data.timestamp;

            // Update temperature
            document.querySelector('.temp_value').textContent = data.temp_val + '°';

            // Update barometer
            document.querySelector('.baro_value').textContent = data.baro_val;

            // Update trend
            const trendEl = document.getElementById('curr_trend').querySelector('.baro_value');
            trendEl.textContent = data.trend_val;

            // Update chart backgrounds
            const tempChart = document.getElementById('curr-temp-block');
            tempChart.style.backgroundImage = `url(${data.temp_chart_val})`;

            const baroChart = document.getElementById('curr-barometer-block');
            baroChart.style.backgroundImage = `url(${data.baro_chart_val})`;

            // Update wind
            document.getElementById('curr_wind').querySelector('.speed_value').textContent = data.wind_val;

            if (data.wind_dir) {
                document.getElementById('curr_wind').style.backgroundImage = `url(${data.wind_dir})`;
            } else {
                document.getElementById('curr_wind').style.backgroundImage = 'none';
            }

            // Update windchill if different from temp
            const windchillEl = document.getElementById('curr_windchill');
            if (data.temp_val !== data.windchill_val) {
                windchillEl.querySelector('.temp_value').textContent = data.windchill_val + '°';
                windchillEl.style.display = 'block';
            } else {
                windchillEl.style.display = 'none';
            }

            // Update humidity
            document.getElementById('humidity_value').textContent = data.humidity + '%';

            // Update morning/afternoon classes
            const chartElements = document.querySelectorAll('.chart_am, .chart_pm');
            chartElements.forEach(el => {
                if (data.morning === 'false' && el.classList.contains('chart_am')) {
                    el.classList.replace('chart_am', 'chart_pm');
                } else if (data.morning === 'true' && el.classList.contains('chart_pm')) {
                    el.classList.replace('chart_pm', 'chart_am');
                }
            });
        }
    };

    // Helper functions
    function getCsrfToken() {
        return document.querySelector('input[name="csrfmiddlewaretoken"]')?.value ||
               document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    }

    function fadeOut(element, duration, callback) {
        element.style.opacity = 1;

        const start = performance.now();
        function step(timestamp) {
            const elapsed = timestamp - start;
            const progress = Math.min(elapsed / duration, 1);

            element.style.opacity = 1 - progress;

            if (progress < 1) {
                requestAnimationFrame(step);
            } else if (callback) {
                callback();
            }
        }

        requestAnimationFrame(step);
    }

    function fadeIn(element, duration, callback) {
        element.style.opacity = 0;

        const start = performance.now();
        function step(timestamp) {
            const elapsed = timestamp - start;
            const progress = Math.min(elapsed / duration, 1);

            element.style.opacity = progress;

            if (progress < 1) {
                requestAnimationFrame(step);
            } else if (callback) {
                callback();
            }
        }

        requestAnimationFrame(step);
    }

    // Attach event listeners for non-Alpine elements if needed
    document.getElementById('refresh-weather')?.addEventListener('click', () => {
        window.weatherData.refreshWeather();
    });
});

// Global functions for toggle buttons
function toggleUnits(el) {
    if (window.weatherData) {
        window.weatherData.toggleUnits();
    }
}

function toggleLabels(el) {
    if (window.weatherData) {
        window.weatherData.toggleTitles();
    }
}