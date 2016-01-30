import datetime

from django.db import models


class ChartUrl(models.Model):
    """
    Contains URL which will create a chart image
    for a specific data type on a particular day.
    """
    date = models.DateField(blank=False)  # date for the chart
    # timestamp is when the url was created
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    data_type = models.CharField(max_length=2, blank=False)
    unit = models.CharField(max_length=5, blank=False)
    size = models.CharField(max_length=2, blank=False)
    plots = models.CharField(max_length=10, blank=False)
    url = models.URLField(max_length=2000, blank=False)

    DATA_TEMP = 'T'
    DATA_PRESS = 'P'
    DATA_HUMIDITY = 'H'
    DATA_WIND = 'W'

    SIZE_IPHONE = 'I'
    SIZE_NORMAL = 'N'

    PLOT_TODAY = 'T'
    PLOT_YESTERDAY = 'D'
    PLOT_YEAR_AGO = 'Y'

    def __unicode__(self):
        return str(self.date) + '-' + \
            '-'.join([self.data_type, self.unit, self.size, self.plots]) + \
            '-' + str(self.timestamp)

    class Meta:
        ordering = ['-date']
        unique_together = ("date", "data_type", "unit", "size", "plots")
