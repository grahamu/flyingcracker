import datetime
from decimal import Decimal

from zoneinfo import ZoneInfo

from fc3 import gchart
from weatherstation.models import Weather

TEMP_F = "F"
TEMP_C = "C"
temp_units = [TEMP_F, TEMP_C]

PRESS_IN = "in"
PRESS_MB = "mb"
baro_units = [PRESS_IN, PRESS_MB]

SPEED_MPH = "mph"
SPEED_KTS = "kts"
SPEED_KMH = "km/h"
SPEED_MS = "m/s"
SPEED_FTS = "ft/s"
speed_units = [SPEED_MPH, SPEED_KTS, SPEED_KMH, SPEED_MS, SPEED_FTS]


def get_chart_data(date, data_type, unit):
    """
    Return chart data as a dict suitable for Chart.js.
    Returns hourly data points for today, yesterday, and year-ago.
    """
    if type(date) is datetime.date:
        date = datetime.datetime(date.year, date.month, date.day)
    mountain_timezone = ZoneInfo("US/Mountain")
    db_date = date.replace(tzinfo=mountain_timezone)

    # Collect hourly data for today, yesterday, and year-ago
    datasets = []
    periods = [
        ("Today", db_date, 0),
        ("Yesterday", db_date - datetime.timedelta(days=1), 1),
        ("Year Ago", db_date - datetime.timedelta(days=365), 2),
    ]

    colors = {
        "temp": ["#0000FF", "#87CEEB", "#BEBEBE"],
        "pressure": ["#D96C00", "#FFCC99", "#BEBEBE"],
        "humidity": ["#00CC00", "#88FF88", "#BEBEBE"],
        "wind": ["#6A006A", "#FF00FF", "#BEBEBE"],
    }

    for label, d, idx in periods:
        wx_records = weather_on_date(d)
        hourly = gchart.hourly_data(wx_records, d)

        if data_type == "temp":
            values = convert_qs_temps(hourly, unit)
        elif data_type == "pressure":
            values = convert_qs_pressures(hourly, unit)
        elif data_type == "humidity":
            values = [rec.humidity if rec else None for rec in hourly]
        elif data_type == "wind":
            values = convert_qs_speeds(hourly, unit)
        else:
            values = []

        datasets.append({
            "label": label,
            "data": values,
            "borderColor": colors.get(data_type, ["#000"] * 3)[idx],
            "borderWidth": 3 if idx == 0 else 2,
            "pointRadius": 0,
            "tension": 0.3,
        })

    return {
        "labels": gchart.HOUR_LABELS,
        "datasets": datasets,
    }


def convert_qs_temps(qs, unit):
    """
    Returns a list of values converted to `unit` if necessary
    from a queryset of Weather records.

    """
    temps = []
    for rec in qs:
        if rec is None:
            temps.append(None)
        else:
            if unit == TEMP_F:  # default units
                temps.append(round_temp(rec.temp))
            else:
                temps.append(f_to_c(rec.temp))
    return temps


def f_to_c(val):
    if val is None:
        return None
    else:
        return round_temp((float(val) - 32.0) / 1.8)


def round_temp(val):
    if val is None:
        return None
    else:
        return int(round(float(val)))



def convert_qs_pressures(qs, unit):
    """
    Returns a list of values converted to `unit` if necessary
    from a queryset of Weather records.

    """
    press = []
    for rec in qs:
        if rec is None:
            press.append(None)
        else:
            if unit == PRESS_IN:  # default units
                press.append(float(rec.barometer))
            else:
                press.append(in_to_mb(rec.barometer))
    return press


def in_to_mb(val):
    if val is None:
        return None
    else:
        # TODO - make this value a named constant
        return int(round(float(val) * 33.8639))



def convert_qs_speeds(qs, unit):
    """
    Returns a list of values converted to `unit` if necessary
    from a queryset of Weather records.

    """
    speed = []
    for rec in qs:
        if rec is None:
            speed.append(None)
        else:
            speed.append(convert_speed(float(rec.wind_speed), unit))
    return speed


def calc_temp_values(value):
    """
    Return a list of temperature values equal to the given value,
    where each value in the list corresponds with a different temperature unit.

    """
    vlist = []
    for unit in temp_units:
        if unit == TEMP_C:
            nv = f_to_c(value)
        else:
            nv = round_temp(value)
        vlist.append(nv)
    return vlist


def calc_baro_values(value):
    """
    Return a list of pressure values equal to the given value,
    where each value in the list corresponds with a different pressure unit.

    """
    vlist = []
    for unit in baro_units:
        if unit == PRESS_MB:
            vlist.append(in_to_mb(value))
        else:
            vlist.append(float(value))
    return vlist


def calc_temp_strings(value):
    vlist = []
    vals = calc_temp_values(value)
    for v in vals:
        vlist.append("%d" % v)
    return vlist


def calc_baro_strings(value):
    vlist = []
    vals = calc_baro_values(value)
    for v in vals:
        if type(v) is int:
            vlist.append("%d" % v)
        else:
            vlist.append("%4.2f" % v)
    return vlist


def calc_trend_strings(value):
    vlist = calc_baro_strings(value)
    if value > Decimal(0):
        vlist = ["+" + v for v in vlist]
    elif value < Decimal("-0.09"):
        vlist = ['<span class="warning">' + v + "</span>" for v in vlist]
    return vlist


def calc_speeds(value):
    value = float(value)
    vlist = []
    for unit in speed_units:
        if value == 0:
            vlist.append("Calm")
        else:
            nv = convert_speed(value, unit)
            vlist.append("%d" % int(round(nv)))
    return vlist


def convert_speed(value, unit):
    if unit == SPEED_MPH:
        nv = value
    elif unit == SPEED_KTS:
        nv = value * 0.868391
    elif unit == SPEED_KMH:
        nv = value * 1.609344
    elif unit == SPEED_MS:
        nv = value * 0.44704
    elif unit == SPEED_FTS:
        nv = value * 1.46667
    else:
        nv = value
    return nv


dir_table = {
    "NNE": 22.5,
    "NE": 45,
    "ENE": 67.5,
    "East": 90,
    "ESE": 112.5,
    "SE": 135,
    "SSE": 157.5,
    "South": 180,
    "SSW": 202.5,
    "SW": 225,
    "WSW": 247.5,
    "West": 270,
    "WNW": 292.5,
    "NW": 315,
    "NNW": 337.5,
}


def wind_dir_to_english(dir):
    for key, val in list(dir_table.items()):
        # TODO make this value a named constant
        if dir >= (val - 11.25) and dir < (val + 11.25):
            return key
    return "North"


def weather_on_date(date):
    """
    Return all Weather records for a specific date.

    """
    mountain_timezone = ZoneInfo("US/Mountain")
    if type(date) is datetime.datetime:
        date = date.date()
    start = datetime.datetime.combine(date, datetime.time.min)
    start = start.replace(tzinfo=mountain_timezone)
    end = datetime.datetime.combine(date, datetime.time.max)
    end = end.replace(tzinfo=mountain_timezone)

    return Weather.objects.filter(timestamp__range=(start, end))


def request_is_local(request):
    if request:
        remote = request.META.get("REMOTE_ADDR")
    else:
        remote = None
    if (
        remote is None
        or remote.startswith("192.168.5.")
        or remote.startswith("192.168.1.")
        or remote.startswith("10.0.1.")
    ):
        return True
    else:
        return False


def get_date(request=None, date=None):
    """
    Returns a datetime.date object corresponding to `date`.
    If the date is not provided or is invalid, today is returned.
    """
    mountain_timezone = ZoneInfo("US/Mountain")
    today = datetime.datetime.now(mountain_timezone).date()

    if not date:
        return today
    else:
        # parse the YYYYMMDD date string
        try:
            year = int(date[0:4])
            month = int(date[4:6])
            day = int(date[6:8])
        except ValueError:
            return today
        else:
            try:
                specified_date = datetime.date(year, month, day)
            except ValueError:
                return today
            else:
                return specified_date


def get_today(request=None):
    """
    Returns a datetime.date object corresponding to today.
    """
    mountain_timezone = ZoneInfo("US/Mountain")
    return datetime.datetime.now(mountain_timezone).date()


def get_today_timestamp(request=None):
    """
    Returns a datetime.datetime object corresponding to today.
    """
    mountain_timezone = ZoneInfo("US/Mountain")
    return datetime.datetime.now(mountain_timezone)



def temp_dict(weather_records):
    """
    Return a dictionary of temperature lists from a list of Weather
    records.
    The dictionary is keyed by temp_units and each value is a list
    of temperatures in that unit.
    """
    data = []
    for rec in weather_records:
        if rec is None or rec.temp is None:
            v = None
        else:
            v = int(rec.temp)
        data.append(calc_temp_values(v))

    # transpose the 2-dimensional array, p.161 Python Cookbook
    data = list(map(list, zip(*data)))

    i = 0
    unit_dict = {}
    for unit in temp_units:
        unit_dict[unit] = data[i]
        i += 1

    return unit_dict


def baro_dict(weather_records):
    """
    Return a list of pressure lists from a list of Weather records.
    Each list corresponds to a unit type.
    """
    data = []
    for rec in weather_records:
        if rec is None or rec.barometer is None:
            v = None
        else:
            v = float(rec.barometer)
        data.append(calc_baro_values(v))

    # transpose the 2-dimensional array, p.161 Python Cookbook
    data = map(list, zip(*data))

    i = 0
    unit_dict = {}
    for unit in baro_units:
        unit_dict[unit] = data[i]
        i += 1
    return unit_dict


