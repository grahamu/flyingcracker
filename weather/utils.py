#!/usr/bin/env python
import datetime
import pytz
from decimal import Decimal
from weatherstation.models import Weather
from weather.models import ChartUrl
import fc3.gchart as gchart

TEMP_F = 'F'
TEMP_C = 'C'
temp_units = [TEMP_F, TEMP_C]

PRESS_IN = 'in'
PRESS_MB = 'mb'
baro_units = [PRESS_IN, PRESS_MB]

SPEED_MPH = 'mph'
SPEED_KTS = 'kts'
SPEED_KMH = 'km/h'
SPEED_MS = 'm/s'
SPEED_FTS = 'ft/s'
speed_units = [SPEED_MPH, SPEED_KTS, SPEED_KMH, SPEED_MS, SPEED_FTS]

def create_chart_url(date, data_type, size, plots, unit):
    '''
    Return a chart URL for the given parameters.
    
    '''
    if type(date) == datetime.date:
        date = datetime.datetime(date.year, date.month, date.day)
    mountain_timezone = pytz.timezone('US/Mountain')
    db_date = mountain_timezone.localize(date)
    
    plot_colors = []
    qs_list = []
    
    if ChartUrl.PLOT_TODAY in plots:
        wx_records = weather_on_date(db_date)
        qs_list.append(gchart.hourly_data(wx_records, date))
        if data_type == ChartUrl.DATA_TEMP:
            plot_colors.append('0000FF')
        elif data_type == ChartUrl.DATA_PRESS:
            plot_colors.append('D96C00')
        elif data_type == ChartUrl.DATA_HUMIDITY:
            plot_colors.append('00CC00')
        elif data_type == ChartUrl.DATA_WIND:
            plot_colors.append('6A006A')
        else:
            plot_colors.append('000000')
    
    if ChartUrl.PLOT_YESTERDAY in plots:
        one_day = datetime.timedelta(days=1)
        db_yesterday = db_date - one_day
        yesterday = date - one_day
        wx_records = weather_on_date(db_yesterday)
        qs_list.append(gchart.hourly_data(wx_records, yesterday))
        if data_type == ChartUrl.DATA_TEMP:
            plot_colors.append('87CEEB')
        elif data_type == ChartUrl.DATA_PRESS:
            plot_colors.append('FFCC99')
        elif data_type == ChartUrl.DATA_HUMIDITY:
            plot_colors.append('88FF88')
        elif data_type == ChartUrl.DATA_WIND:
            plot_colors.append('FF00FF')
        else:
            plot_colors.append('888888')

    if ChartUrl.PLOT_YEAR_AGO in plots:
        one_year = datetime.timedelta(days=365) # don't worry about leap years
        db_year_ago = db_date - one_year
        year_ago = date - one_year
        wx_records = weather_on_date(db_year_ago)
        qs_list.append(gchart.hourly_data(wx_records, year_ago))
        plot_colors.append('BEBEBE')
            
    WIDTH_DEFAULT = 300
    HEIGHT_DEFAULT = 110

    if data_type == ChartUrl.DATA_TEMP:
        if size == ChartUrl.SIZE_IPHONE:
            width = 260
            height = 100
            plot_func = gchart.day_chart_iphone
        elif size == ChartUrl.SIZE_NORMAL:
            width = 400
            height = 160
            plot_func = gchart.day_chart_normal
        else:
            width = WIDTH_DEFAULT
            height = HEIGHT_DEFAULT
            plot_func = gchart.day_chart_normal
        chart = day_temp_chart(qs_list, unit, plot_func, width, height, plot_colors)
        
    elif data_type == ChartUrl.DATA_PRESS:
        if size == ChartUrl.SIZE_IPHONE:
            width = 292
            height = 100
            plot_func = gchart.day_chart_iphone
        elif size == ChartUrl.SIZE_NORMAL:
            width = 418
            height = 160
            plot_func = gchart.day_chart_normal
        else:
            width = WIDTH_DEFAULT
            height = HEIGHT_DEFAULT
            plot_func = gchart.day_chart_normal
        chart = day_baro_chart(qs_list, unit, plot_func, width, height, plot_colors)
        
    elif data_type == ChartUrl.DATA_HUMIDITY:
        if size == ChartUrl.SIZE_IPHONE:
            width = 260
            height = 100
            plot_func = gchart.day_chart_iphone
        elif size == ChartUrl.SIZE_NORMAL:
            width = 400
            height = 160
            plot_func = gchart.day_chart_normal
        else:
            width = WIDTH_DEFAULT
            height = HEIGHT_DEFAULT
            plot_func = gchart.day_chart_normal
        chart = day_humidity_chart(qs_list, plot_func, width, height, plot_colors)
        
        
    elif data_type == ChartUrl.DATA_WIND:
        if size == ChartUrl.SIZE_IPHONE:
            width = 292
            height = 100
            plot_func = gchart.day_chart_iphone
        elif size == ChartUrl.SIZE_NORMAL:
            width = 418
            height = 160
            plot_func = gchart.day_chart_normal
        else:
            width = WIDTH_DEFAULT
            height = HEIGHT_DEFAULT
            plot_func = gchart.day_chart_normal
        chart = day_wind_chart(qs_list, unit, plot_func, width, height, plot_colors)

    else:
        return ''
    return chart.get_url()

def day_temp_chart(qs_list, unit, plot_func, width, height, colors):
    '''
    Returns a URL which plots one line for each queryset in `qs_list`.
    
    '''
    data_list = []  # list of value lists
    for date_qs in qs_list:
        if date_qs: # only work on this if the queryset is not empty
            data_list.append(convert_qs_temps(date_qs, unit))

    floor = 200
    ceil = -200
    plot_list = [] # list of plot lines, each a list of values
    for val_list in data_list:
        # add list of temp values to list of plot lines
        plot_list.append(val_list)
        # determine the lowest and highest values seen for this unit type
        floor = gchart.int_floor(val_list, floor)
        ceil = gchart.int_ceil(val_list, ceil)
    chart = plot_func(plot_list, floor, ceil, width, height, colors, [4,2,2])
    return chart

def convert_qs_temps(qs, unit):
    '''
    Returns a list of values converted to `unit` if necessary
    from a queryset of Weather records.
    
    '''
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
        return round_temp((float(val)-32.0)/1.8)

def round_temp(val):
    if val is None:
        return None
    else:
        return int(round(float(val)))

def day_baro_chart(qs_list, unit, plot_func, width, height, colors):
    '''
    Returns a URL which produces one line for each queryset.
    
    '''
    data_list = []  # list of value lists
    for date_qs in qs_list:
        if date_qs: # only work on this if the queryset is not empty
            data_list.append(convert_qs_pressures(date_qs, unit))
            
    floor = 1500
    ceil = 0
    plot_list = [] # list of plot lines, each a list of values
    for val_list in data_list:
        # add list of temp values to list of plot lines
        plot_list.append(val_list)
        # determine the lowest and highest values seen for this unit type
        floor = gchart.flex_floor(val_list, floor)
        ceil = gchart.flex_ceil(val_list, ceil)
    chart = plot_func(plot_list, floor, ceil, width, height, colors, [4,2,2])
    return chart

def convert_qs_pressures(qs, unit):
    '''
    Returns a list of values converted to `unit` if necessary
    from a queryset of Weather records.
    
    '''
    press = []
    for rec in qs:
        if rec is None:
            press.append(None)
        else:
            if unit == PRESS_IN:    # default units
                press.append(float(rec.barometer))
            else:
                press.append(in_to_mb(rec.barometer))
    return press

def in_to_mb(val):
    if val is None:
        return None
    else:
        return int(round(float(val)*33.8639))

def day_humidity_chart(qs_list, plot_func, width, height, colors):
    '''
    Returns a URL which produces one line for each queryset.
    
    '''
    data_list = []  # list of value lists
    for date_qs in qs_list:
        humidity = []
        for rec in date_qs:
            if rec is None:
                humidity.append(None)
            else:
                humidity.append(rec.humidity)
        data_list.append(humidity)
            
    plot_list = [] # list of plot lines, each a list of values
    for val_list in data_list:
        # add list of humidity values to list of plot lines
        plot_list.append(val_list)
    chart = plot_func(plot_list, 0, 100, width, height, colors, [4,2,2])
    return chart


def day_wind_chart(qs_list, unit, plot_func, width, height, colors):
    '''
    Returns a URL which produces one line for each queryset.
    
    '''
    data_list = []  # list of value lists
    for date_qs in qs_list:
        if date_qs: # only work on this if the queryset is not empty
            data_list.append(convert_qs_speeds(date_qs, unit))
            
    floor = 0
    ceil = 10
    plot_list = [] # list of plot lines, each a list of values
    for val_list in data_list:
        # add list of speed values to list of plot lines
        plot_list.append(val_list)
        # determine the lowest and highest values seen for this unit type
        ceil = gchart.flex_ceil(val_list, ceil)
    chart = plot_func(plot_list, floor, ceil, width, height, colors, [4,2,2])
    return chart

def convert_qs_speeds(qs, unit):
    '''
    Returns a list of values converted to `unit` if necessary
    from a queryset of Weather records.
    
    '''
    speed = []
    for rec in qs:
        if rec is None:
            speed.append(None)
        else:
            speed.append(convert_speed(float(rec.wind_speed), unit))
    return speed

def calc_temp_values(value):
    '''
    Return a list of temperature values equal to the given value,
    where each value in the list corresponds with a different temperature unit.
    
    '''
    vlist = []
    for unit in temp_units:
        if unit == TEMP_C:
            nv = f_to_c(value)
        else:
            nv = round_temp(value)
        vlist.append(nv)
    return vlist

def calc_baro_values(value):
    '''
    Return a list of pressure values equal to the given value,
    where each value in the list corresponds with a different pressure unit.
    
    '''
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
        if type(v) == int:
            vlist.append("%d" % v)
        else:
            vlist.append("%4.2f" % v)
    return vlist

def calc_trend_strings(value):
    vlist = calc_baro_strings(value)
    if value > Decimal(0):
        vlist = ['+'+v for v in vlist]
    elif value < Decimal("-0.09"):
        vlist = ['<span class="warning">'+v+'</span>' for v in vlist]
    return vlist

def calc_speeds(value):
    value = float(value)
    vlist = []
    for unit in speed_units:
        if value == 0:
            vlist.append('Calm')
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
        nv = value*1.609344
    elif unit == SPEED_MS:
        nv = value*0.44704
    elif unit == SPEED_FTS:
        nv = value*1.46667
    else:
        nv = value
    return nv

dir_table = {
    'NNE': 22.5,
    'NE': 45,
    'ENE': 67.5,
    'East': 90,
    'ESE': 112.5,
    'SE': 135,
    'SSE': 157.5,
    'South': 180,
    'SSW': 202.5,
    'SW': 225,
    'WSW': 247.5,
    'West': 270,
    'WNW': 292.5,
    'NW': 315,
    'NNW': 337.5
}

def wind_dir_to_english(dir):
    for key,val in dir_table.items():
        if dir >= (val-11.25) and dir < (val+11.25):
            return key
    return 'North'

def weather_on_date(date):
    '''
    Return all Weather records for a specific date.
    
    '''
    mountain_timezone = pytz.timezone('US/Mountain')
    if type(date) == datetime.datetime:
        date = date.date()
    start = datetime.datetime.combine(date, datetime.time.min)
    start = mountain_timezone.localize(start)
    end = datetime.datetime.combine(date, datetime.time.max)
    end = mountain_timezone.localize(end)

    return Weather.objects.filter(timestamp__range=(start, end)).\
           order_by('timestamp')

def request_is_local(request):
    if request:
        remote = request.META.get('REMOTE_ADDR')
    else:
        remote = None
    if remote is None or remote.startswith("192.168.5.") or \
       remote.startswith("10.0.1."):
        return True
    else:
        return False
    
def get_date(request=None, date=None):
    '''
    Returns a datetime.date object corresponding to the date
    provided, unless the requesting address is local in which case
    we return a specific date (for which our local database has
    weather records).
    If the date is not provided or is invalid, today is returned.
    
    '''
    mountain_timezone = pytz.timezone('US/Mountain')
    today = datetime.datetime.now(mountain_timezone).date()
    
    if request_is_local(request):
        return datetime.date(2008,4,1)
    else:
        if not date:
            return today
        else:
            # parse the YYYYMMDD date string
            try:
                year = int(date[0:4])
                month = int(date[4:6])
                day = int(date[6:8])
            except:
                return today
            else:
                try:
                    specified_date = datetime.date(year, month, day)
                except ValueError:
                    return today
                else:
                    return specified_date
    
def get_today(request=None):
    '''
    Returns a datetime.date object corresponding to today,
    unless the requesting address is local in which case
    we return a date for which our local database has weather records.
    '''
    if request_is_local(request):
        return datetime.date(2008,4,1)
    else:
        mountain_timezone = pytz.timezone('US/Mountain')
        return datetime.datetime.now(mountain_timezone).date()

def get_today_timestamp(request=None):
    '''
    Returns a datetime.datetime object corresponding to today,
    unless the requesting address is local in which case
    we return a date for which our local database has weather records.
    
    '''
    if request_is_local(request):
        today = datetime.datetime(2008,4,1,10,11,12)
    else:
        mountain_timezone = pytz.timezone('US/Mountain')
        today = datetime.datetime.now(mountain_timezone)
    return today

def temp_chart_filename(unit, date, type, extra):
    return weather_chart_filename(unit, date, 'temp', type, extra)

def baro_chart_filename(unit, date, type, extra):
    return weather_chart_filename(unit, date, 'baro', type, extra)

def weather_chart_filename(unit, date, title, type, extra):
    return '%d-%02d-%02d_%s_%s_%s%s.png' % (date.year, date.month, date.day, title, unit, type, extra)


def temp_dict(l):
    '''
    Return a dictionary of temperature lists from a list of Weather records.
    The dictionary is keyed by temp_units and each value is a list of temperatures in that unit.
    '''
    data = []
    for rec in l:
        if rec is None or rec.temp is None:
            v = None
        else:
            v = int(rec.temp)
        data.append(calc_temp_values(v))
    data = map(list, zip(*data))    # transpose the 2-dimensional array, p.161 Python Cookbook
    
    i = 0
    unit_dict = {}
    for unit in temp_units:
        unit_dict[unit] = data[i]
        i = i+1

    return unit_dict

def baro_dict(l):
    '''
    Return a list of pressure lists from a list of Weather records.
    Each list corresponds to a unit type.
    '''
    data = []
    for rec in l:
        if rec is None or rec.barometer is None:
            v = None
        else:
            v = float(rec.barometer)
        data.append(calc_baro_values(v))
    data = map(list, zip(*data))    # transpose the 2-dimensional array, p.161 Python Cookbook
    
    i = 0
    unit_dict = {}
    for unit in baro_units:
        unit_dict[unit] = data[i]
        i = i+1
    return unit_dict


def get_URL_data(url, filename, max_file_age=60):
    '''
    Given a URL and a filename, if the file exists and it's timestamp
    is not older than 'max_file_age' minutes, return file contents.
    If the file does not exist or is older than 'max_file_age' minutes
    obtain data from the URL and save in filename before returning.
    
    '''
    import os
    if not os.path.isfile(filename):
        return save_URL_data(url, filename)

    filetime_t = os.path.getmtime(filename)
    filestamp = datetime.datetime.fromtimestamp(filetime_t)
    now = datetime.datetime.now()
    if (now - filestamp) > datetime.timedelta(minutes=max_file_age) or (now < filestamp):
        return save_URL_data(url, filename)
    
    try:
        f = open(filename, 'r')
    except:
        lines = save_URL_data(url, filename)
    else:
        try:
            lines = f.read()
        except:
            lines = save_URL_data(url, filename)
    return lines

def save_URL_data(url, filename):
    from urllib import urlopen
    
    try:
        xml_text = urlopen(url).read()
    except IOError:
        return None
    else:
        # save the retrieved data
        f = open(filename, "w")
        f.write(xml_text)
        f.close()
        return xml_text


if __name__=='__main__':
    today = get_today_timestamp(None)
    today_wx = weather_on_date(today)
    print gchart.hourly_data(today_wx, today)
    print gchart.halfhour_data(today_wx, today)
