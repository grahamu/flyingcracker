import json
import logging
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
    Convert a US zip code to an NWS forecast zone ID.
    Uses pgeocode for offline lat/lon lookup, then NWS /points API.
    Returns zone ID string (e.g., 'COZ012') or None on failure.
    Cached for 30 days.
    """
    cache_key = f"nws-zip-zone-{zip_code}"
    zone_id = cache.get(cache_key)
    if zone_id is not None:
        return zone_id

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
    forecast_zone_url = data.get("properties", {}).get("forecastZone", "")
    if forecast_zone_url:
        zone_id = forecast_zone_url.rstrip("/").split("/")[-1]
        cache.set(cache_key, zone_id, timeout=ZIP_ZONE_CACHE_TIMEOUT)
        return zone_id

    return None
