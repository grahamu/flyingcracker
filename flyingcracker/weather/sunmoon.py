#!/usr/bin/env python
import datetime
from dateutil import parser as dateutilparser
import ephem
import json
import pytz

from django.conf import settings

from .forecast import DataBlock
from .utils import get_URL_data


class SunMoonTimes(object):

    pubdate = None
    twilight_begin = None
    sunrise = None
    sunset = None
    twilight_end = None
    moonrise = None
    moonset = None


class SunMoon(DataBlock):

    today_rstt = SunMoonTimes()
    tomorrow_rstt = SunMoonTimes()
    current_phase = None

    def __init__(self, **kwargs):
        """
        Obtain "Rise Set Transit Times" for Sun and Moon, based
        on user location.
        """
        self.user = kwargs.pop('user')
        super(SunMoon, self).__init__(**kwargs)

        today = datetime.date.today()
        self.set_times(self.today_rstt, today)
        self.pubdate = self.today_rstt.pubdate
        self.set_timestamp()

        tomorrow = today + datetime.timedelta(days=1)
        self.set_times(self.tomorrow_rstt, tomorrow)

    def _get_observer(self, user):
        observer = ephem.Observer()
        observer.pressure = 0
        # Location is hard coded to Crested Butte for now
        # Someday convert to user's location.
        observer.lat, observer.lon = '38.813125', '-106.8972617'
        observer.elevation = '2600'  # meters ASL
        return observer

    def observed_time(self, date):
        """
        Convert an ephem.Date object, specified in UTC but without
        timezone awareness, to a timezone correct string.
        """
        utc_date = date.datetime().replace(tzinfo=pytz.UTC)
        # Convert to Mountain Time
        # Someday convert to user's timezone, as seen in
        # fcprofile.user_tags.user_time.
        mt_date = utc_date.astimezone(pytz.timezone('US/Mountain'))
        return mt_date.strftime('%I:%M %p')

    def set_times(self, times, date):
        """
        """
        observer = self._get_observer(self.user)
        observer.date = date.strftime('%Y/%m/%d 19:00')  # 7pm UTC, mid-day in Colorado

        # sun rise and set
        # See http://rhodesmill.org/pyephem/rise-set.html#naval-observatory-risings-and-settings
        observer.horizon = '-0:34'
        times.sunrise = self.observed_time(
            observer.previous_rising(ephem.Sun())
        )
        times.sunset = self.observed_time(
            observer.next_setting(ephem.Sun())
        )

        # moon rise and set
        times.moonrise = self.observed_time(
            observer.previous_rising(ephem.Moon())
        )
        times.moonset = self.observed_time(
            observer.next_setting(ephem.Moon())
        )

        # twilight
        # As per PyEphem suggestion, get time when Sun is 6 degrees
        # below the horizon, and use center of the Sun.
        # http://rhodesmill.org/pyephem/rise-set.html#computing-twilight
        observer.horizon = '-6'
        times.twilight_begin = self.observed_time(
            observer.previous_rising(ephem.Sun(), use_center=True)
        )
        times.twilight_end = self.observed_time(
            observer.next_setting(ephem.Sun(), use_center=True)
        )

        times.pubdate = date.strftime('%Y-%m-%d 00:00:01 -0700')

    def __repr__(self):
        s = ''
        if self.pubdate:
            s += "SunMoon pubdate: " + self.pubdate + "\n"
        if self.timestamp:
            s += "SunMoon timestamp: " + \
                self.timestamp.strftime("%H:%M %Z %a %b %d, %Y") + "\n"
        if self.error:
            s += "Data Error\n"
        return s


class MoonPhaseData(object):

    pubdate = None
    name = None
    date = None
    time = None
    image = None


class MoonPhases(DataBlock):

    url_pattern = ('http://api.usno.navy.mil/moon/phase?ID=CBSOUTH'
                   '&date={date}&nump=4')
    filename = settings.WEATHER_ROOT.child('moonphases.txt')

    def __init__(self, **kwargs):
        '''
        Obtain latest aa.usno.navy.mil "Phases of the Moon".
        '''
        super(MoonPhases, self).__init__(**kwargs)

        today = datetime.date.today()
        today_string = today.strftime("%m/%d/%Y")
        today_url = self.url_pattern.format(date=today_string)
        response = get_URL_data(today_url, self.filename,
                                max_file_age=12 * 60)
        phases = json.loads(response)
        self.phases = []
        self.set_phases(phases)
        self.pubdate = self.phases[0].pubdate
        self.set_timestamp()

    def set_phases(self, phases):

        if not phases or phases['error']:
            self.error = True
            self.add_section('Origin Data Error',
                             'computation (parameters?) unsuccessful')
            return

        for phase in phases['phasedata']:
            phase_data = MoonPhaseData()
            phase_data.pubdate = ("{}-{}-{} 00:00:01 -0700"
                                  .format(phases['year'],
                                          phases['month'],
                                          phases['day'])
                                  )
            phase_data.name = phase['phase']

            date = dateutilparser.parse(phase['date'] + ' ' + phase['time'])
            phase_data.date = date.date()
            phase_data.time = date.time()
            phase_data.image = ("http://api.usno.navy.mil/imagery/moon.png"
                                "?&date={date}&time={time}"
                                .format(date=date.strftime("%m/%d/%Y"),
                                        time=phase['time'])
                                )
            self.phases.append(phase_data)

    def __repr__(self):
        s = ''
        if self.pubdate:
            s += "MoonPhases pubdate: " + self.pubdate + "\n"
        if self.timestamp:
            s += "MoonPhases timestamp: " + \
                self.timestamp.strftime("%H:%M %Z %a %b %d, %Y") + "\n"
        if self.error:
            s += "Data Error\n"
        return s
