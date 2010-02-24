#!/usr/bin/env python
from django.test import TestCase
from django.core.urlresolvers import reverse
import datetime

class PeriodicRecordsTestCase(TestCase):
    fixtures = ['fc3',]
    
    def setUp(self):
        from weather.utils import weather_on_date, get_today_timestamp
        
        self.start = get_today_timestamp(None)
        self.qs = weather_on_date(self.start)
        
    def testPeriodicRecords2Hours(self):
        from fc3.gchart import periodic_samples
        
        fudge = datetime.timedelta(minutes=5)
        interval = datetime.timedelta(hours=2)
        periods = 12
        d = periodic_samples(self.qs, self.start, fudge, interval, periods)
        #assertEqual(len(d), periods)
        
    def testPeriodicRecords10Minutes(self):
        from fc3.gchart import periodic_samples

        fudge = datetime.timedelta(minutes=5)
        interval = datetime.timedelta(minutes=10)
        periods = 24 * 6
        d = periodic_samples(self.qs, self.start, fudge, interval, periods)
        #assertEqual(len(d), periods)

    def testXhrRequestForCurrent(self):
        '''
        Ensure that XHR request succeeds and
        GET and POST requests fail with 404.
        
        '''
        from django.utils import simplejson

        response = self.client.get(reverse('weather-current'))
        self.assertEqual(response.status_code, 404)
        
        response = self.client.post(reverse('weather-current'))
        self.assertEqual(response.status_code, 404)
        
        # EXPENSE Account list
        response = self.client.post(reverse('weather-current'),
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                    )
        self.assertEqual(response.status_code, 200)
        
        # deserialize content
        obj = simplejson.loads(response.content)
