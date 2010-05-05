from datetime import datetime
from decimal import Decimal
import traceback
from pytz import timezone, utc
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from fc3.weatherstation.models import Weather

def upload_data(request):
    """
    Upload weather data view.

    Templates: ``<app_label>/weather_action.html``
    Context:
        none
    """

    dbtimestamp = None
    urltimestamp = request.GET.get('timestamp', None)
    dateutc = request.GET.get('datemtn', None)

    mountain_tz = timezone('US/Mountain')
    
    if urltimestamp is not None:
        dbtimestamp = datetime.fromtimestamp(int(urltimestamp), mountain_tz)
    elif dateutc is not None:
        dateutc = dateutc.replace(':',' ').replace('-',' ').replace('+',' ')
        year,month,day,hour,minute,second = dateutc.split()
        dbtimestamp = datetime(int(year),int(month),int(day),int(hour),int(minute),int(second))
        dbtimestamp = mountain_tz.localize(dbtimestamp)
    
    if dbtimestamp:
        wind_dir    = request.GET.get('winddir', None)
        wind_speed  = request.GET.get('windspeedmph', None)
        wind_peak   = request.GET.get('windgustmph', None)
        temp        = request.GET.get('tempf', None)
        barometer   = request.GET.get('baromin', None)
        dewpoint    = request.GET.get('dewptf', None)
        humidity    = request.GET.get('humidity', None)
        temp_inside = request.GET.get('tempinf', None)
        baro_trend  = request.GET.get('baromtrendin', None)
        windchill   = request.GET.get('windchillf', None)
        rain        = request.GET.get('rainin', None)
        station_id  = request.GET.get('ID', None)

        defaults = {}
        if wind_dir:
            defaults['wind_dir'] = wind_dir
        if wind_speed:
            defaults['wind_speed'] = wind_speed
        if wind_peak:
            defaults['wind_peak'] = wind_peak
        if temp:
            defaults['temp'] = temp
        if barometer:
            defaults['barometer'] = barometer
        if dewpoint:
            defaults['dewpoint'] = dewpoint
        if humidity:
            defaults['humidity'] = humidity
        if temp_inside:
            defaults['temp_inside'] = temp_inside
        if baro_trend:
            defaults['baro_trend'] = baro_trend
        if windchill:
            defaults['windchill'] = windchill
        if rain:
            defaults['rain'] = rain
        if station_id:
            defaults['station_id'] = station_id
        try:
            rec,created = Weather.objects.get_or_create(
                             timestamp = dbtimestamp,
                             defaults = defaults,
                            )
            if created is not True:
                # Record already exists, replace with good values and save.
                if wind_dir:
                    rec.wind_dir = int(wind_dir)
                if wind_speed:
                    rec.wind_speed = Decimal(wind_speed)
                if wind_peak:
                    rec.wind_peak = Decimal(wind_peak)
                if temp:
                    rec.temp = Decimal(temp)
                if barometer:
                    rec.barometer = Decimal(barometer)
                if dewpoint:
                    rec.dewpoint = Decimal(dewpoint)
                if humidity:
                    rec.humidity = int(humidity)
                if temp_inside:
                    rec.temp_inside = Decimal(temp_inside)
                if baro_trend:
                    rec.baro_trend = Decimal(baro_trend)
                if windchill:
                    rec.windchill = Decimal(windchill)
                if rain:
                    rec.rain = rain
                if station_id:
                    rec.station_id = station_id
                rec.save()
                success_str = "weather record updated"
            else:
                success_str = "weather record created"
        except:
            response=HttpResponse("upload_data failed: '%s'" % traceback.format_exc())
        else:
            response = HttpResponse(success_str)
    else:
        response = HttpResponse('failed: missing "datemtn" or "timestamp" field in URL')
    return response
    
def download_data(request):
    pass
