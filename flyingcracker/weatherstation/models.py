from django.db import models
from datetime import *

class Weather(models.Model):
    station_id = models.CharField(max_length=10)
    timestamp = models.DateTimeField('Date of reading', unique=True)

    wind_dir = models.IntegerField(null=True)
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    wind_peak = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    humidity = models.IntegerField(null=True)
    temp = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    rain = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    barometer = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    dewpoint = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    temp_inside = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    baro_trend = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    windchill = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def __unicode__(self):
        if self.timestamp is not None:
            return datetime.ctime(self.timestamp)
        else:
            return u"no time"

    class Meta:
        ordering = ['timestamp']
        get_latest_by = 'timestamp'
