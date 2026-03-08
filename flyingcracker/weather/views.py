import datetime
from decimal import Decimal

from django import forms
from django.forms import ModelForm
from django.http import JsonResponse
from django.shortcuts import render
from pytz import timezone

from fc3.utils import ElapsedTime
from weatherstation.models import Weather

from . import utils
from .noaa import get_NOAA_forecast
from .sunmoon import MoonPhases, SunMoon


def weather(request):
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
    mountain_tz = timezone("US/Mountain")
    now = datetime.datetime.now(mountain_tz)

    et = ElapsedTime()

    noaa = get_NOAA_forecast("CO", 12)  # Crested Butte area

    et.mark_time("forecasts")

    sunmoon = SunMoon(user=request.user)
    moonphases = MoonPhases(user=request.user)

    current_dict, current = get_current_weather(request)
    context = dict(current_dict)
    context.update(
        {
            "current": current,
            "show_titles": show_titles,
            "title_state": title_state,
            "show_units": show_units,
            "unit_state": unit_state,
            "noaa": noaa,
            "sunmoon": sunmoon,
            "moonphases": moonphases,
            "elapsed": et.list(),
        }
    )

    return render(request, "weather/current.html", context)


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
    timestamp = date_filter(timestamp, "H:i \M\T D M j")  # noqa:W605

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
        "morning": morning,
        "chart_date": current.timestamp.strftime("%Y%m%d"),
    }
    return response_dict, current


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
