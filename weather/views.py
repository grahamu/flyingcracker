#!/usr/bin/env python
from datetime import *
from decimal import *
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from fc3.myjson import JsonResponse
from fc3.utils import ElapsedTime
from weatherstation.models import Weather
from noaa import get_NOAA_forecast
from cbac import CBAC
from cbtv import CBTV
import weather.utils as utils
from weather.models import ChartUrl
from weatherstation.tz import USTimeZone
from dateutil.tz import tzlocal

def weather(request):
    from django.utils import simplejson
    from django.core.serializers.json import DjangoJSONEncoder
    
    et = ElapsedTime()

    show_titles = request.COOKIES.get("curr_weather_show_titles")
    if show_titles == None:
        show_titles = "hidden"
    if show_titles == "hidden":
        title_state = "false"
    else:
        title_state = "true"
    show_units = request.COOKIES.get("curr_weather_show_units")
    if show_units == None:
        show_units = "none"
    if show_units == "none":
        unit_state = "false"
    else:
        unit_state = "true"

    # Get time in MT for forecast timestamp comparison
    mountain_tz = USTimeZone(-7, "Mountain", "MST", "MDT")
    now = datetime.now(tzlocal()).astimezone(mountain_tz)
    
    cbac = CBAC() # comment out for summer.
    # Don't display CBAC stuff if older than 36 hours.
    # In this case they are probably closed for the season.
    if cbac:
        if not cbac.timestamp or (now - cbac.timestamp) > timedelta(hours=36):
            cbac = None

    noaa = get_NOAA_forecast('CO', 12)     # Crested Butte area
    cbtv = CBTV()
    # Don't display CBTV stuff if older than 36 hours.
    # In this case they are probably down.
    if cbtv:
        if not cbtv.timestamp or (now - cbtv.timestamp) > timedelta(hours=36):
            cbtv = None

    et.mark_time('forecasts')

    current_dict, current = get_current_weather(request)
    c = RequestContext(request, {
        'weather': current_dict,
        'json_weather': simplejson.dumps(current_dict, cls=DjangoJSONEncoder),
        'current': current,
        'show_titles': show_titles,
        'title_state': title_state,
        'show_units': show_units,
        'unit_state': unit_state,
        'cbac': cbac,
        'noaa': noaa,
        'cbtv': cbtv,
        'elapsed': et.list(),
    })

    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or request.GET.has_key('iphone'):
        if request.GET.has_key('iui'):
            return render_to_response('weather/iphone/weather-iui.html', c)
        else:
            return render_to_response('weather/iphone/weather.html', c)
    else:
        return render_to_response('weather/current.html', c)

def current(request):
    if request.is_ajax():
        response_dict, current = get_current_weather(request)
        response = JsonResponse(response_dict)
        return response
    else:
        raise Http404

def get_current_weather(request):
    '''
    Returns a dictionary of weather information
    along with the latest Weather record.
    If no Weather record is found, returns an empty
    dictionary.
    
    '''
    from django.template.defaultfilters import date as date_filter
    
    # get latest weather reading
    try:
        current = Weather.objects.latest('timestamp')
    except Weather.DoesNotExist:
        return {}, None
    
    timestamp = date_filter(current.timestamp, "H:i \M\T D M j,Y")

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
        wind_dir = "wind-%s.png" % utils.wind_dir_to_english(wind)
        wind_dir = wind_dir.lower()
    wind_list = utils.calc_speeds(wind)
        
    if wind == 0:
        speed_unit = ""
        wind_units = [""]
    else:
        speed_unit = request.COOKIES.get("speed_unit")
        wind_units = utils.speed_units
        if speed_unit is None:
            speed_unit = utils.SPEED_MPH
    
    wind_val = wind_list[wind_units.index(speed_unit)]
    
    windchill_list = utils.calc_temp_strings(current.windchill)
    windchill_val = windchill_list[wind_units.index(speed_unit)]
    
    temp_list = utils.calc_temp_strings(current.temp)
    temp_val = temp_list[utils.temp_units.index(temp_unit)]
    baro_list = utils.calc_baro_strings(current.barometer)
    baro_val = baro_list[utils.baro_units.index(baro_unit)]
    trend_list = utils.calc_trend_strings(current.baro_trend)
    trend_val = trend_list[utils.baro_units.index(baro_unit)]
    
    today = utils.get_today_timestamp(request)
    if today.hour < 12:
        morning = True
    else:
        morning = False

    t_chart = []
    b_chart = []
    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or request.GET.has_key('iphone'):
        for unit in utils.temp_units:
            t_chart.append(get_chart(utils.get_today(request), ChartUrl.DATA_TEMP, ChartUrl.SIZE_IPHONE, ChartUrl.PLOT_TODAY+ChartUrl.PLOT_YESTERDAY+ChartUrl.PLOT_YEAR_AGO, unit))
        for unit in utils.baro_units:
            b_chart.append(get_chart(utils.get_today(request), ChartUrl.DATA_PRESS, ChartUrl.SIZE_IPHONE, ChartUrl.PLOT_TODAY+ChartUrl.PLOT_YESTERDAY+ChartUrl.PLOT_YEAR_AGO, unit))
    else:
        for unit in utils.temp_units:
            t_chart.append(get_chart(utils.get_today(request), ChartUrl.DATA_TEMP, ChartUrl.SIZE_NORMAL, ChartUrl.PLOT_TODAY+ChartUrl.PLOT_YESTERDAY+ChartUrl.PLOT_YEAR_AGO, unit))
        for unit in utils.baro_units:
            b_chart.append(get_chart(utils.get_today(request), ChartUrl.DATA_PRESS, ChartUrl.SIZE_NORMAL, ChartUrl.PLOT_TODAY+ChartUrl.PLOT_YESTERDAY+ChartUrl.PLOT_YEAR_AGO, unit))
    temp_chart_val = t_chart[utils.temp_units.index(temp_unit)]
    baro_chart_val = b_chart[utils.baro_units.index(baro_unit)]
    response_dict = {'timestamp': timestamp,
                     'temp_units': utils.temp_units,
                     'baro_units': utils.baro_units,
                     'speed_units': wind_units,
                     'temp_val': temp_val,
                     'baro_val': baro_val,
                     'trend_val': trend_val,
                     'temp_unit': temp_unit,
                     'baro_unit': baro_unit,
                     'speed_unit': speed_unit,
                     'temp': temp_list,
                     'baro': baro_list,
                     'trend': trend_list,
                     'wind': wind_list,
                     'wind_val': wind_val,
                     'wind_dir': wind_dir,
                     'windchill': windchill_list,
                     'windchill_val': windchill_val,
                     'humidity': current.humidity,
                     'temp_chart': t_chart,
                     'baro_chart': b_chart,
                     'temp_chart_val': temp_chart_val,
                     'baro_chart_val': baro_chart_val,
                     'morning': morning,
                    }
    return response_dict, current

def unit_change(request):
    '''
    Set the user preference for units.
    '''
    type = request.POST.get('type')
    unit = request.POST.get('unit')
    
    # set unit preference in user profile
    # ...
    
    # return same data, just for grins
    response_dict = {}
    response_dict.update({'type': type})
    response_dict.update({'unit': unit})
    response = JsonResponse(response_dict)
    return response


from fc3.weather.models import ChartUrl

def get_chart(date, data_type, size, plots, unit, force_create=False):
    if force_create:
        return utils.create_chart_url(date, data_type, size, plots, unit)
    
    now = datetime.now()
    try:
        chart = ChartUrl.objects.get(date=date, data_type=data_type, size=size, plots=plots, unit=unit)
    except ChartUrl.DoesNotExist:
        # create url
        chart = ChartUrl(date=date, timestamp=now, data_type=data_type, size=size, plots=plots, unit=unit)
        # BUGBUG - 2008-11-20 - move the following line up above the previous line,
        #          once we figure out the correct exception for a save overwrite.
        #          Restore the 'try' block when we have that exception type.
        url = utils.create_chart_url(date, data_type, size, plots, unit)
        chart.url = url
#        try:
        chart.save()
#        except: # someone else got it done first
#            pass
    else:
        # recreate url if timestamp hour is different than now
        if now.hour != chart.timestamp.hour:
            # re-create url
            chart.url = utils.create_chart_url(date, data_type, size, plots, unit)
            chart.timestamp = now
            chart.save()
    return chart.url

from django import forms
from django.forms import ModelForm


class WeatherForm(ModelForm):
    class Meta:
        model = Weather


class GenerateWeatherForm(WeatherForm):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()
    
    def clean(self):
        start = self.cleaned_data.get('start_date')
        end = self.cleaned_data.get('end_date')
        if start and end:
            if end < start:
                raise forms.ValidationError('Start date/time (%s) must be prior to end date/time (%s)' % (str(start), str(end)))
        return self.cleaned_data
            
    class Meta(WeatherForm.Meta):
        exclude = ('station_id', 'timestamp', 'temp_inside', 'rain', 'wind_peak', 'dewpoint', 'windchill')

def generate(request):
    if request.method == 'POST': # If the form has been submitted...
        form = GenerateWeatherForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            cd = form.cleaned_data
            interval = timedelta(minutes=5)
            start = cd['start_date']
            curr = start
            end = cd['end_date']
            inserted = attempts = 0
            et = ElapsedTime()
            while curr <= end:
                obj = Weather(station_id='GENERATED',
                              timestamp=curr,
                              wind_dir=cd['wind_dir'],
                              wind_speed=cd['wind_speed'],
                              wind_peak=0,
                              humidity=cd['humidity'],
                              temp=cd['temp'],
                              rain=0,
                              barometer=cd['barometer'],
                              dewpoint=0,
                              temp_inside=0,
                              baro_trend=cd['baro_trend'],
                              windchill=0)
                try:
                    obj.save()
                except Weather.IntegrityError:
                    pass    # leave the existing record in place
                else:
                    inserted += 1
                curr += interval
                attempts += 1
                
            et.mark_time('insertions')
            c = RequestContext(request, {
                    'elapsed': et.list(),
                    'message': 'Added %d Weather records in %d attempts, from %s to %s.' % (inserted, attempts, str(start), str(end)),
                    })
            return render_to_response('weather/after_action.html', c)
    else:
        form = GenerateWeatherForm() # An unbound form

    c = RequestContext(request, {
            'form': form,
        })
    return render_to_response('weather/generate.html', c)

class DeleteWeatherForm(forms.Form):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()
    
    def clean(self):
        start = self.cleaned_data.get('start_date')
        end = self.cleaned_data.get('end_date')
        if start and end:
            if end < start:
                raise forms.ValidationError('Start date/time (%s) must be prior to end date/time (%s)' % (str(start), str(end)))
        return self.cleaned_data

def delete(request):
    if request.method == 'POST': # If the form has been submitted...
        form = DeleteWeatherForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            cd = form.cleaned_data
            start = cd['start_date']
            end = cd['end_date']
            records = Weather.objects.filter(timestamp__range=(start, end))
            deleted = attempts = 0
            et = ElapsedTime()
            for obj in records:
                try:
                    obj.delete()
                except:
                    pass
                else:
                    deleted += 1
                attempts += 1
                
            et.mark_time('deletions')
            c = RequestContext(request, {
                    'elapsed': et.list(),
                    'message': 'Deleted %d Weather records in %d attempts, from %s to %s..' % (deleted, attempts, str(start), str(end)),
                    })

            return render_to_response('weather/after_action.html', c)
    else:
        form = DeleteWeatherForm() # An unbound form

    c = RequestContext(request, {
            'form': form,
        })
    return render_to_response('weather/delete.html', c)

def output_data(request):
    '''
    Expects GET parameters:
    `item` - sensor type: temp, wind, barometer, etc.
    `type` - type of data collection: average, highlow, hourly, etc.
    `start` - date (and optional time) for the start of data collection
    `end` - date (and optional time) for the end of data collection
    
    Returns a CSV file. The first line contains column titles.
    Subsequent lines contain data values.
    
    '''
    import csv
    from dateutil.parser import parse as dateparse
    
    item = request.GET.get('item')
    if item == 'pressure':
        attr = 'barometer'
    elif item == 'wind':
        attr = 'wind_speed'
    elif item == 'temp' or item == 'humidity' or item == 'windchill':
        attr = item
    else:
        return HttpResponse(content='Unsupported data item: "%s". Valid data items: "temp", "pressure", "humidity", "windchill" and "wind".' % str(item))
    
    today_str = date.today().strftime('%Y-%m-%d')
    start_str = request.GET.get('start', today_str)
    end_str = request.GET.get('end', today_str)
    try:
        # Force both of these to be type 'str', as dateutil parser
        # does not seem to parse unicode (as retrieved from GET dict).
        start = dateparse(str(start_str))
    except ValueError, e:
        return HttpResponse(content='start date error: %s' % e)
        
    try:
        end = dateparse(str(end_str))
    except ValueError, e:
        return HttpResponse(content='end date error: %s' % e)
    
    target = date(start.year, start.month, start.day)
    end = date(end.year, end.month, end.day)
    interval = timedelta(days=1)

    if target > end:
        return HttpResponse(content='start date cannot be later than end date' % (str(target), str(end)))
    
    type = request.GET.get('type')
    
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=fc3weather_%s_%s_%s-%s.csv' % (item, type, start_str, end_str)
    writer = csv.writer(response)
    
    if item == 'temp':
        if type == 'average':
            writer.writerow(['date', '%s:low (F)'%attr, '%s:high (F)'%attr, '%s:average (F)'%attr])
            
            # Get the high and low temp for each date.
            while target <= end:
                qs = Weather.objects.filter(timestamp__year=target.year, timestamp__month=target.month, timestamp__day=target.day)
                vals = [rec.__getattribute__(attr) for rec in qs]
                total = Decimal('0')
                if vals:
                    low = min(vals)
                    high = max(vals)
                    for temp in vals:
                        total += temp
                    avg = total / len(vals)
                    writer.writerow([str(target),
                                     str(low),
                                     str(high),
                                     str(avg.quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)),
                                     ])
                else:
                    writer.writerow([str(target),
                                     'N/A',
                                     'N/A',
                                     'N/A',
                                    ])
                target += interval
            return response
        elif type == 'hourly':
            from fc3.gchart import periodic_samples
            from utils import weather_on_date

            output = ['date']
            output.extend([time(n).strftime("%H:%M") for n in range(0,24)])
            writer.writerow(output)
            
            while target <= end:
                qs = weather_on_date(target)
                start = datetime(target.year, target.month, target.day)
                day_recs = periodic_samples(qs, start, timedelta(minutes=5), timedelta(hours=1), 24)
                def temp_string_or_blank(record):
                    if not record:
                        return ''
                    else:
                        return str(record.temp)
                temps = map(temp_string_or_blank, day_recs)
                output = [str(target)]
                output.extend(temps)
                writer.writerow(output)
                target += interval
            return response
        else:
            return HttpResponse(content='Unsupported report type: "%s". Valid report types: "average".' % str(type))
    elif item == 'wind':
        if type == 'average':
            writer.writerow(['date', '%s:average (mph)'%attr, '%s:peak (mph)'%attr])
            
            # Get the average and peak windspeed for each date.
            while target <= end:
                qs = Weather.objects.filter(timestamp__year=target.year, timestamp__month=target.month, timestamp__day=target.day)
                speed_vals = [rec.__getattribute__(attr) for rec in qs]
                total = Decimal('0')
                if speed_vals:
                    for speed in speed_vals:
                        total += speed
                    avg = total / len(speed_vals)
                    peak = max([rec.__getattribute__('wind_peak') for rec in qs])
                    writer.writerow([str(target),
                                     str(avg.quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)),
                                     str(peak.quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)),
                                    ])
                else:
                    writer.writerow([str(target),
                                     'N/A',
                                     'N/A',
                                    ])
                    
                target += interval
            return response
        else:
            return HttpResponse(content='Unsupported report type: "%s". Valid report types: "average".' % str(type))

def chart(request):
    '''
    Expects GET parameters:
    `item` - sensor type: temp, pressure, humidity
    `type` - chart type: multiday
    `units` - Units for the requested data item. Temp: 'F', 'C'. Pressure: 'in', 'mb'.
    `force` - indicates desire to force creation of a URL and not use saved URL
    
    Returns a URL for a chart of the specified type.
    
    '''
    force_create = request.GET.get('force', False)
    
    item_list = ['temp', 'pressure', 'humidity', 'wind']
    
    item = request.GET.get('item')
    if item not in item_list:
        return HttpResponse(content='Unsupported data item: "%s". Valid data items are: %s.' % (str(item), ', '.join(item_list)))
        
    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or request.GET.has_key('iphone'):
        size = ChartUrl.SIZE_IPHONE
    else:
        size = ChartUrl.SIZE_NORMAL
    
    type = request.GET.get('type', None)
    units = request.GET.get('units', None)
    date = request.GET.get('date', None)
    
    chart_date = utils.get_date(request, date)
        
    if item == 'temp':
        if units not in utils.temp_units:
            return HttpResponse(content='Unsupported temp units: "%s". Valid units: %s.' % (str(units), ', '.join(utils.temp_units)))
        if type != 'multiday':
            return HttpResponse(content='Unsupported chart type: "%s". Valid chart types: "multiday".' % str(type))
        
        chart = get_chart(chart_date, ChartUrl.DATA_TEMP, size, ChartUrl.PLOT_TODAY+ChartUrl.PLOT_YESTERDAY+ChartUrl.PLOT_YEAR_AGO, units, force_create=force_create)
    elif item == 'pressure':
        if units not in utils.baro_units:
            return HttpResponse(content='Unsupported pressure units: "%s". Valid units: %s.' % (str(units), ', '.join(utils.baro_units)))
        if type != 'multiday':
            return HttpResponse(content='Unsupported chart type: "%s". Valid chart types: "multiday".' % str(type))
        
        chart = get_chart(chart_date, ChartUrl.DATA_PRESS, size, ChartUrl.PLOT_TODAY+ChartUrl.PLOT_YESTERDAY+ChartUrl.PLOT_YEAR_AGO, units, force_create=force_create)
    elif item == 'humidity':
        if type != 'multiday':
            return HttpResponse(content='Unsupported chart type: "%s". Valid chart types: "multiday".' % str(type))
        
        chart = get_chart(chart_date, ChartUrl.DATA_HUMIDITY, size, ChartUrl.PLOT_TODAY+ChartUrl.PLOT_YESTERDAY+ChartUrl.PLOT_YEAR_AGO, '%', force_create=force_create)
    elif item == 'wind':
        if units not in utils.speed_units:
            return HttpResponse(content='Unsupported speed units: "%s". Valid units: %s.' % (str(units), ', '.join(utils.speed_units)))
        if type != 'multiday':
            return HttpResponse(content='Unsupported chart type: "%s". Valid chart types: "multiday".' % str(type))
        
        chart = get_chart(chart_date, ChartUrl.DATA_WIND, size, ChartUrl.PLOT_TODAY+ChartUrl.PLOT_YESTERDAY+ChartUrl.PLOT_YEAR_AGO, units, force_create=force_create)
    else:
        chart = 'none'
    return HttpResponse(content=chart)