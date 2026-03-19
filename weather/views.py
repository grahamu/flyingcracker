import datetime
from decimal import Decimal

import re

from django import forms
from django.conf import settings
from django.contrib import messages
from django.forms import ModelForm
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from zoneinfo import ZoneInfo

from fc3.utils import ElapsedTime
from weatherstation.models import Weather

from . import utils
from .noaa import (
    get_current_observations,
    get_zone_forecast,
    get_zone_name,
    lookup_zone_for_zip,
)
from .sunmoon import MoonPhases, SunMoon


def weather(request, noaa_zone=None, noaa_zip=None, noaa_lat=None, noaa_lon=None, noaa_tz=None, river_gauge=None):
    show_titles = request.COOKIES.get("curr_weather_show_titles")
    if show_titles is None:
        show_titles = "hidden"
    if show_titles == "hidden":
        title_state = "false"
    else:
        title_state = "true"
    show_units = request.COOKIES.get("curr_weather_show_units")
    if show_units is None:
        show_units = "none"
    if show_units == "none":
        unit_state = "false"
    else:
        unit_state = "true"

    # Get time in MT for forecast timestamp comparison
    mountain_tz = ZoneInfo("US/Mountain")
    now = datetime.datetime.now(mountain_tz)

    et = ElapsedTime()

    if noaa_zone is None:
        noaa_zone = request.COOKIES.get("noaa_zone", settings.NWS_DEFAULT_ZONE)
    if noaa_zip is None:
        noaa_zip = request.COOKIES.get("noaa_zip", "")
    use_local_data = noaa_zip in ("", "cbsouth")
    noaa = get_zone_forecast(noaa_zone)

    et.mark_time("forecasts")

    # Get location for sun/moon calculations
    location_kwargs = {}
    if not use_local_data:
        lat = noaa_lat or request.COOKIES.get("noaa_lat")
        lon = noaa_lon or request.COOKIES.get("noaa_lon")
        tz = noaa_tz or request.COOKIES.get("noaa_tz")
        if lat and lon:
            location_kwargs = {"lat": lat, "lon": lon, "elevation": 0}
            if tz:
                location_kwargs["timezone"] = tz

    sunmoon = SunMoon(**location_kwargs)
    moonphases = MoonPhases(**location_kwargs)

    if use_local_data:
        current_dict, current = get_current_weather(request)
    else:
        current_dict, current = get_nws_current_weather(request, noaa_zone)

    area_name = get_zone_name(noaa_zone)

    if river_gauge is None:
        river_gauge = request.COOKIES.get("river_gauge", "")

    context = dict(current_dict)
    context.update(
        {
            "current": current,
            "use_local_data": use_local_data,
            "area_name": area_name,
            "show_titles": show_titles,
            "title_state": title_state,
            "show_units": show_units,
            "unit_state": unit_state,
            "noaa": noaa,
            "noaa_zone": noaa_zone,
            "noaa_zip": noaa_zip,
            "default_zone": settings.NWS_DEFAULT_ZONE,
            "river_gauge": river_gauge,
            "sunmoon": sunmoon,
            "moonphases": moonphases,
            "elapsed": et.list(),
        }
    )

    return render(request, "weather/current.html", context)


def set_river_gauge(request):
    """
    POST: save river gauge ID to cookie, render weather page.
    GET with ?reset=1: clear cookie, render weather page.
    """
    if request.GET.get("reset"):
        response = weather(request, river_gauge="")
        response.delete_cookie("river_gauge")
        return response

    if request.method != "POST":
        return HttpResponseRedirect(reverse("weather:root"))

    gauge_id = request.POST.get("river_gauge", "").strip().upper()

    if not re.match(r"^[A-Z0-9]{3,8}$", gauge_id):
        messages.error(request, "Please enter a valid gauge identifier (3-8 alphanumeric characters).")
        return HttpResponseRedirect(reverse("weather:root"))

    response = weather(request, river_gauge=gauge_id)
    response.set_cookie(
        "river_gauge", gauge_id,
        max_age=90 * 24 * 60 * 60, path="/", httponly=False, samesite="Lax",
    )
    return response


def set_zone(request):
    """
    POST: look up NWS zone from zip code, set cookie, redirect.
    GET with ?reset=1: clear cookie back to default, redirect.
    """
    if request.GET.get("reset"):
        response = weather(request, noaa_zone=settings.NWS_DEFAULT_ZONE, noaa_zip="")
        response.delete_cookie("noaa_zone")
        response.delete_cookie("noaa_zip")
        response.delete_cookie("noaa_lat")
        response.delete_cookie("noaa_lon")
        response.delete_cookie("noaa_tz")
        return response

    if request.method != "POST":
        return HttpResponseRedirect(reverse("weather:root"))

    zip_code = request.POST.get("zip_code", "").strip()

    # "cbsouth" → show local station data (default zone)
    if zip_code.lower() == "cbsouth":
        response = weather(request, noaa_zone=settings.NWS_DEFAULT_ZONE, noaa_zip=zip_code.lower())
        cookie_kwargs = dict(max_age=90 * 24 * 60 * 60, path="/", httponly=False, samesite="Lax")
        response.set_cookie("noaa_zip", zip_code.lower(), **cookie_kwargs)
        response.delete_cookie("noaa_zone")
        response.delete_cookie("noaa_lat")
        response.delete_cookie("noaa_lon")
        response.delete_cookie("noaa_tz")
        return response

    if not re.match(r"^\d{5}$", zip_code):
        messages.error(request, "Please enter a valid 5-digit zip code.")
        return HttpResponseRedirect(reverse("weather:root"))

    location = lookup_zone_for_zip(zip_code)
    if location is None:
        messages.error(
            request, f"Could not find a forecast zone for zip code {zip_code}."
        )
        return HttpResponseRedirect(reverse("weather:root"))

    zone_id = location["zone_id"]

    # Render weather page directly with the new zone to avoid
    # Railway's proxy following the redirect server-side.
    response = weather(
        request, noaa_zone=zone_id, noaa_zip=zip_code,
        noaa_lat=location["lat"], noaa_lon=location["lon"],
        noaa_tz=location["timezone"],
    )
    cookie_kwargs = dict(max_age=90 * 24 * 60 * 60, path="/", httponly=False, samesite="Lax")
    response.set_cookie("noaa_zone", zone_id, **cookie_kwargs)
    response.set_cookie("noaa_zip", zip_code, **cookie_kwargs)
    response.set_cookie("noaa_lat", str(location["lat"]), **cookie_kwargs)
    response.set_cookie("noaa_lon", str(location["lon"]), **cookie_kwargs)
    response.set_cookie("noaa_tz", location["timezone"], **cookie_kwargs)
    return response


def get_current_weather(request):
    """
    Returns a dictionary of weather information
    along with the latest Weather record.
    """
    from django.template.defaultfilters import date as date_filter
    from templatetags.as_timezone import as_timezone

    try:
        current = Weather.objects.latest()
    except Weather.DoesNotExist:
        return {}, None

    # Force this timestamp to be Mountain Time
    timestamp = as_timezone(current.timestamp, "US/Mountain")
    timestamp = date_filter(timestamp, r"H:i \M\T D M j")

    temp_unit = request.COOKIES.get("temp_unit")
    if temp_unit is None:
        temp_unit = utils.TEMP_F

    baro_unit = request.COOKIES.get("baro_unit")
    if baro_unit is None:
        baro_unit = utils.PRESS_IN

    if int(float(current.wind_speed)) < 1:
        wind = 0
        wind_dir = None
    else:
        wind = current.wind_speed
        wind_dir = "img/wind-%s.png" % utils.wind_dir_to_english(wind)
        wind_dir = wind_dir.lower()
    wind_list = utils.calc_speeds(wind)

    speed_unit = request.COOKIES.get("speed_unit")
    if speed_unit is None:
        speed_unit = utils.SPEED_MPH

    wind_val = wind_list[utils.speed_units.index(speed_unit)]

    windchill_list = utils.calc_temp_strings(current.windchill)
    windchill_val = windchill_list[utils.temp_units.index(temp_unit)]

    temp_list = utils.calc_temp_strings(current.temp)
    temp_val = temp_list[utils.temp_units.index(temp_unit)]
    baro_list = utils.calc_baro_strings(current.barometer)
    baro_val = baro_list[utils.baro_units.index(baro_unit)]
    trend_list = utils.calc_trend_strings(current.baro_trend)
    trend_val = trend_list[utils.baro_units.index(baro_unit)]

    today = utils.get_today_timestamp(request)
    morning = today.hour < 12

    response_dict = {
        "timestamp": timestamp,
        "temp_units": utils.temp_units,
        "baro_units": utils.baro_units,
        "speed_units": utils.speed_units,
        "temp_val": temp_val,
        "baro_val": baro_val,
        "trend_val": trend_val,
        "temp_unit": temp_unit,
        "baro_unit": baro_unit,
        "speed_unit": speed_unit,
        "temp": temp_list,
        "baro": baro_list,
        "trend": trend_list,
        "wind": wind_list,
        "wind_val": wind_val,
        "wind_dir": wind_dir,
        "windchill": windchill_list,
        "windchill_val": windchill_val,
        "humidity": current.humidity,
        "show_windchill": current.temp != current.windchill,
        "morning": morning,
        "chart_date": current.timestamp.strftime("%Y%m%d"),
    }
    return response_dict, current


def get_nws_current_weather(request, zone_id):
    """
    Returns a dictionary of weather information from NWS observations
    for a non-default zone. Same dict shape as get_current_weather().
    """
    from django.template.defaultfilters import date as date_filter
    from templatetags.as_timezone import as_timezone

    obs = get_current_observations(zone_id)
    if obs is None:
        return {}, None

    # Format timestamp
    timestamp = ""
    if obs["timestamp"]:
        ts = as_timezone(obs["timestamp"], "US/Mountain")
        timestamp = date_filter(ts, r"H:i \M\T D M j")

    temp_unit = request.COOKIES.get("temp_unit") or utils.TEMP_F
    baro_unit = request.COOKIES.get("baro_unit") or utils.PRESS_IN
    speed_unit = request.COOKIES.get("speed_unit") or utils.SPEED_MPH

    # Temperature
    if obs["temp"] is not None:
        temp_list = utils.calc_temp_strings(obs["temp"])
        temp_val = temp_list[utils.temp_units.index(temp_unit)]
    else:
        temp_list = ["\u2014"] * len(utils.temp_units)
        temp_val = "\u2014"

    # Barometer
    if obs["barometer"] is not None:
        baro_list = utils.calc_baro_strings(obs["barometer"])
        baro_val = baro_list[utils.baro_units.index(baro_unit)]
    else:
        baro_list = ["\u2014"] * len(utils.baro_units)
        baro_val = "\u2014"

    # Baro trend - not available from NWS
    trend_list = ["\u2014"] * len(utils.baro_units)
    trend_val = "\u2014"

    # Wind
    if obs["wind_speed"] is not None and float(obs["wind_speed"]) >= 1:
        wind_list = utils.calc_speeds(obs["wind_speed"])
        wind_val = wind_list[utils.speed_units.index(speed_unit)]
        if obs["wind_dir"] is not None:
            wind_dir = "img/wind-%s.png" % utils.wind_dir_to_english(obs["wind_dir"])
            wind_dir = wind_dir.lower()
        else:
            wind_dir = None
    else:
        wind_list = utils.calc_speeds(0)
        wind_val = wind_list[utils.speed_units.index(speed_unit)]
        wind_dir = None

    # Windchill
    if obs["windchill"] is not None:
        windchill_list = utils.calc_temp_strings(obs["windchill"])
        windchill_val = windchill_list[utils.temp_units.index(temp_unit)]
    else:
        windchill_list = temp_list
        windchill_val = temp_val

    today = utils.get_today_timestamp(request)
    morning = today.hour < 12

    response_dict = {
        "timestamp": timestamp,
        "temp_units": utils.temp_units,
        "baro_units": utils.baro_units,
        "speed_units": utils.speed_units,
        "temp_val": temp_val,
        "baro_val": baro_val,
        "trend_val": trend_val,
        "temp_unit": temp_unit,
        "baro_unit": baro_unit,
        "speed_unit": speed_unit,
        "temp": temp_list,
        "baro": baro_list,
        "trend": trend_list,
        "wind": wind_list,
        "wind_val": wind_val,
        "wind_dir": wind_dir,
        "windchill": windchill_list,
        "windchill_val": windchill_val,
        "humidity": obs["humidity"],
        "show_windchill": windchill_val != temp_val,
        "morning": morning,
        "chart_date": today.strftime("%Y%m%d"),
        "station_name": obs["station_name"],
        "description": obs["description"],
    }
    return response_dict, None


def chartdata(request):
    """
    JSON endpoint for Chart.js.
    GET parameters:
      type - temp, pressure, humidity, wind
      unit - F/C for temp, in/mb for pressure, mph/kts/etc for wind
      date - YYYYMMDD (optional, defaults to latest weather record's date)
    """
    data_type = request.GET.get("type", "temp")
    unit = request.GET.get("unit", "F")
    date_str = request.GET.get("date")
    if date_str:
        chart_date = utils.get_date(request, date_str)
    else:
        try:
            latest = Weather.objects.latest()
            chart_date = latest.timestamp.date()
        except Weather.DoesNotExist:
            chart_date = utils.get_date(request)
    data = utils.get_chart_data(chart_date, data_type, unit)
    return JsonResponse(data)


def unit_change(request):
    """
    Set the user preference for units.
    """
    type = request.POST.get("type")
    unit = request.POST.get("unit")
    response_dict = {"type": type, "unit": unit}
    return JsonResponse(response_dict)


class WeatherForm(ModelForm):
    class Meta:
        model = Weather
        fields = "__all__"


class GenerateWeatherForm(WeatherForm):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()

    def clean(self):
        start = self.cleaned_data.get("start_date")
        end = self.cleaned_data.get("end_date")
        if start and end:
            if end < start:
                raise forms.ValidationError(
                    "Start date/time (%s) must be "
                    "prior to end date/time (%s)" % (str(start), str(end))
                )
        return self.cleaned_data

    class Meta(WeatherForm.Meta):
        exclude = (
            "station_id",
            "timestamp",
            "temp_inside",
            "rain",
            "wind_peak",
            "dewpoint",
            "windchill",
        )


def generate(request):
    if request.method == "POST":
        form = GenerateWeatherForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            interval = datetime.timedelta(minutes=5)
            start = cd["start_date"]
            curr = start
            end = cd["end_date"]
            inserted = attempts = 0
            et = ElapsedTime()
            while curr <= end:
                obj = Weather(
                    station_id="GENERATED",
                    timestamp=curr,
                    wind_dir=cd["wind_dir"],
                    wind_speed=cd["wind_speed"],
                    wind_peak=0,
                    humidity=cd["humidity"],
                    temp=cd["temp"],
                    rain=0,
                    barometer=cd["barometer"],
                    dewpoint=0,
                    temp_inside=0,
                    baro_trend=cd["baro_trend"],
                    windchill=0,
                )
                try:
                    obj.save()
                except Weather.IntegrityError:
                    pass
                else:
                    inserted += 1
                curr += interval
                attempts += 1

            et.mark_time("insertions")
            context = {
                "elapsed": et.list(),
                "message": "Added %d Weather records in %d attempts,"
                " from %s to %s." % (inserted, attempts, str(start), str(end)),
            }
            return render(request, "weather/after_action.html", context)
    else:
        form = GenerateWeatherForm()

    context = {"form": form}
    return render(request, "weather/generate.html", context)


class DeleteWeatherForm(forms.Form):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()

    def clean(self):
        start = self.cleaned_data.get("start_date")
        end = self.cleaned_data.get("end_date")
        if start and end:
            if end < start:
                raise forms.ValidationError(
                    "Start date/time (%s) must be"
                    " prior to end date/time (%s)" % (str(start), str(end))
                )
        return self.cleaned_data


def delete(request):
    if request.method == "POST":
        form = DeleteWeatherForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            start = cd["start_date"]
            end = cd["end_date"]
            records = Weather.objects.filter(timestamp__range=(start, end))
            deleted = attempts = 0
            et = ElapsedTime()
            for obj in records:
                try:
                    obj.delete()
                except Weather.DoesNotExist:
                    pass
                else:
                    deleted += 1
                attempts += 1

            et.mark_time("deletions")
            context = {
                "elapsed": et.list(),
                "message": "Deleted %d Weather records in %d attempts,"
                " from %s to %s.." % (deleted, attempts, str(start), str(end)),
            }

            return render(request, "weather/after_action.html", context)
    else:
        form = DeleteWeatherForm()

    context = {"form": form}
    return render(request, "weather/delete.html", context)
