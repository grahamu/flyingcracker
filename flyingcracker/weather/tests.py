from __future__ import absolute_import
import datetime

from fc3.gchart import periodic_samples
from fc3.test import TestCase
from weather.utils import (
    weather_on_date,
    get_today_timestamp,
)


class PeriodicRecordsTestCase(TestCase):
    """
    Verify correct number of records from `periodic_samples` function.
    """
    fixtures = ['fc3']

    def setUp(self):
        self.start = get_today_timestamp(None)
        self.queryset = weather_on_date(self.start)

    def testPeriodicRecords2Hours(self):
        fudge = datetime.timedelta(minutes=5)
        interval = datetime.timedelta(hours=2)
        periods = 12
        d = periodic_samples(self.queryset,
                             self.start, fudge, interval, periods)
        self.assertEqual(len(d), periods)

    def testPeriodicRecords10Minutes(self):
        fudge = datetime.timedelta(minutes=5)
        interval = datetime.timedelta(minutes=10)
        periods = 24 * 6
        d = periodic_samples(self.queryset,
                             self.start, fudge, interval, periods)
        self.assertEqual(len(d), periods)


class CurrentWeather(TestCase):

    def testXhrRequestForCurrent(self):
        '''
        Ensure that XHR request succeeds and
        GET and POST requests fail with 404.

        '''
        import json

        response = self.get('weather-current')
        self.response_404(response)

        response = self.post('weather-current')
        self.response_404(response)

        # EXPENSE Account list
        response = self.post('weather-current', data={
            'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest',
        })
        self.response_200(response)

        # deserialize content
        obj = json.loads(response.content)
