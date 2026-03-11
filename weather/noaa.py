import datetime
import json
import logging
from decimal import Decimal
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.cache import cache

from .forecast import Forecast

logger = logging.getLogger(__name__)

NWS_API_BASE = "https://api.weather.gov"
FORECAST_CACHE_TIMEOUT = 3 * 60 * 60  # 3 hours
ZONE_NAME_CACHE_TIMEOUT = 30 * 24 * 60 * 60  # 30 days
ZIP_ZONE_CACHE_TIMEOUT = 30 * 24 * 60 * 60  # 30 days
STATION_CACHE_TIMEOUT = 30 * 24 * 60 * 60  # 30 days
OBSERVATION_CACHE_TIMEOUT = 15 * 60  # 15 minutes


def _nws_get(url):
    """Fetch JSON from the NWS API with required User-Agent header."""
    req = Request(url)
    req.add_header("User-Agent", settings.NWS_API_USER_AGENT)
    req.add_header("Accept", "application/geo+json")
    response = urlopen(req, timeout=10)
    return json.loads(response.read().decode())


def get_zone_forecast(zone_id):
    """
    Fetch the NWS zone forecast for the given zone ID (e.g., 'COZ012').
    Returns a Forecast object. Uses 3-hour cache.
    """
    cache_key = f"nws-forecast-{zone_id}"
    forecast = cache.get(cache_key)
    if forecast is not None:
        return forecast

    forecast = _fetch_zone_forecast(zone_id)
    if forecast and not forecast.error:
        cache.set(cache_key, forecast, timeout=FORECAST_CACHE_TIMEOUT)
    return forecast


def _fetch_zone_forecast(zone_id):
    """Fetch and parse zone forecast from NWS API."""
    forecast = Forecast()
    url = f"{NWS_API_BASE}/zones/forecast/{zone_id}/forecast"
    try:
        data = _nws_get(url)
    except (URLError, HTTPError, json.JSONDecodeError, OSError) as e:
        logger.warning("NWS forecast fetch failed for %s: %s", zone_id, e)
        forecast.report_error(f"Unable to fetch forecast for zone {zone_id}")
        return forecast

    props = data.get("properties", {})

    # Set timestamp from 'updated' field (ISO 8601)
    updated = props.get("updated")
    if updated:
        forecast.pubdate = updated
        forecast.set_timestamp(updated)

    # Set area name from zone metadata
    forecast.area_name = get_zone_name(zone_id)
    forecast.area = forecast.area_name

    # Parse periods into sections
    for period in props.get("periods", []):
        title = period.get("name", "")
        body = period.get("detailedForecast", "")
        if title and body:
            forecast.add_section(title, body)

    if not forecast.sections:
        forecast.report_error(f"No forecast periods available for zone {zone_id}")

    return forecast


def get_zone_name(zone_id):
    """
    Get the human-readable name for a forecast zone.
    Cached for 30 days since zone names rarely change.
    """
    cache_key = f"nws-zone-name-{zone_id}"
    name = cache.get(cache_key)
    if name is not None:
        return name

    url = f"{NWS_API_BASE}/zones/forecast/{zone_id}"
    try:
        data = _nws_get(url)
        name = data.get("properties", {}).get("name", zone_id)
    except (URLError, HTTPError, json.JSONDecodeError, OSError) as e:
        logger.warning("NWS zone name fetch failed for %s: %s", zone_id, e)
        name = zone_id  # Fallback to zone ID as display name

    cache.set(cache_key, name, timeout=ZONE_NAME_CACHE_TIMEOUT)
    return name


def lookup_zone_for_zip(zip_code):
    """
    Convert a US zip code to an NWS forecast zone ID and coordinates.
    Uses pgeocode for offline lat/lon lookup, then NWS /points API.
    Returns dict with 'zone_id', 'lat', 'lon', 'timezone' keys, or None on failure.
    Cached for 30 days.
    """
    cache_key = f"nws-zip-zone-{zip_code}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    import pgeocode

    nomi = pgeocode.Nominatim("us")
    result = nomi.query_postal_code(zip_code)

    if result is None or result.latitude != result.latitude:  # NaN check
        return None

    lat, lon = round(result.latitude, 4), round(result.longitude, 4)

    # Call NWS points API
    url = f"{NWS_API_BASE}/points/{lat},{lon}"
    try:
        data = _nws_get(url)
    except (URLError, HTTPError, json.JSONDecodeError, OSError) as e:
        logger.warning(
            "NWS points lookup failed for %s (%s,%s): %s", zip_code, lat, lon, e
        )
        return None

    # Extract zone ID from forecastZone URL
    # e.g., "https://api.weather.gov/zones/forecast/COZ012"
    props = data.get("properties", {})
    forecast_zone_url = props.get("forecastZone", "")
    if forecast_zone_url:
        zone_id = forecast_zone_url.rstrip("/").split("/")[-1]
        timezone = props.get("timeZone", "US/Mountain")
        result = {"zone_id": zone_id, "lat": lat, "lon": lon, "timezone": timezone}
        cache.set(cache_key, result, timeout=ZIP_ZONE_CACHE_TIMEOUT)
        return result

    return None


def get_observation_station(zone_id):
    """
    Get the best observation station for a forecast zone.
    Returns (station_id, station_name) tuple or None.
    Prefers ICAO-style stations (4-letter, starts with K).
    Cached for 30 days.
    """
    cache_key = f"nws-station-{zone_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    url = f"{NWS_API_BASE}/zones/forecast/{zone_id}"
    try:
        data = _nws_get(url)
    except (URLError, HTTPError, json.JSONDecodeError, OSError) as e:
        logger.warning("NWS zone fetch failed for %s: %s", zone_id, e)
        return None

    stations = data.get("properties", {}).get("observationStations", [])
    if not stations:
        return None

    # Extract station IDs from URLs
    # e.g., "https://api.weather.gov/stations/KGUC" -> "KGUC"
    station_ids = [s.rstrip("/").split("/")[-1] for s in stations]

    # Prefer ICAO-style (4-letter, starts with K)
    station_id = next(
        (sid for sid in station_ids if len(sid) == 4 and sid.startswith("K")),
        station_ids[0],
    )

    # Fetch station name
    station_name = station_id
    try:
        station_data = _nws_get(f"{NWS_API_BASE}/stations/{station_id}")
        station_name = station_data.get("properties", {}).get("name", station_id)
    except (URLError, HTTPError, json.JSONDecodeError, OSError):
        pass

    result = (station_id, station_name)
    cache.set(cache_key, result, timeout=STATION_CACHE_TIMEOUT)
    return result


def get_current_observations(zone_id):
    """
    Fetch latest NWS observation for the given zone.
    Returns a dict with values in base units (F, inches, mph) or None on error.
    Cached for 15 minutes.
    """
    cache_key = f"nws-obs-{zone_id}"
    obs = cache.get(cache_key)
    if obs is not None:
        return obs

    station_info = get_observation_station(zone_id)
    if station_info is None:
        return None
    station_id, station_name = station_info

    url = f"{NWS_API_BASE}/stations/{station_id}/observations/latest"
    try:
        data = _nws_get(url)
    except (URLError, HTTPError, json.JSONDecodeError, OSError) as e:
        logger.warning("NWS observation fetch failed for %s: %s", station_id, e)
        return None

    props = data.get("properties", {})

    def _val(key):
        """Extract numeric value from an NWS measurement object."""
        obj = props.get(key)
        if obj is None:
            return None
        return obj.get("value")

    temp_c = _val("temperature")
    pressure_pa = _val("barometricPressure")
    wind_kmh = _val("windSpeed")
    wind_dir_deg = _val("windDirection")
    humidity_pct = _val("relativeHumidity")
    windchill_c = _val("windChill")
    description = props.get("textDescription", "")
    timestamp_str = props.get("timestamp", "")

    # Unit conversions to base units (F, inches, mph)
    temp_f = Decimal(str(round(temp_c * 1.8 + 32, 1))) if temp_c is not None else None
    baro_in = (
        Decimal(str(round(pressure_pa / 3386.39, 2)))
        if pressure_pa is not None
        else None
    )
    wind_mph = (
        Decimal(str(round(wind_kmh / 1.609344, 1)))
        if wind_kmh is not None
        else None
    )
    humidity_int = round(humidity_pct) if humidity_pct is not None else None
    if windchill_c is not None:
        windchill_f = Decimal(str(round(windchill_c * 1.8 + 32, 1)))
    else:
        windchill_f = temp_f
    wind_dir_int = round(wind_dir_deg) if wind_dir_deg is not None else None

    # Parse timestamp
    ts = None
    if timestamp_str:
        try:
            ts = datetime.datetime.fromisoformat(timestamp_str)
        except ValueError:
            pass

    obs = {
        "temp": temp_f,
        "barometer": baro_in,
        "baro_trend": None,
        "wind_speed": wind_mph,
        "wind_dir": wind_dir_int,
        "humidity": humidity_int,
        "windchill": windchill_f,
        "timestamp": ts,
        "station_name": station_name,
        "description": description,
    }

    cache.set(cache_key, obs, timeout=OBSERVATION_CACHE_TIMEOUT)
    return obs
