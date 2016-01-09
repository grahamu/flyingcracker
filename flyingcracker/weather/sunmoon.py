#!/usr/bin/env python
import datetime
from dateutil import parser as dateutilparser
import json

from django.conf import settings

from .forecast import DataBlock
from .utils import get_URL_data


"""
Sun and moon data obtained from
U.S. Naval Observatory Astronomical Applications Department.

Reference http://aa.usno.navy.mil/data/docs/api.php
"""

class SunMoonTimes(object):

    pubdate = None
    twilight_begin = None
    sunrise = None
    sunset = None
    twilight_end = None
    moonrise = None
    moonset = None


class SunMoon(DataBlock):

    url_pattern = ('http://api.usno.navy.mil/rstt/oneday?ID=CBSOUTH'
                   '&date={date}&loc=Crested%20Butte,CO')
    today_filename = settings.WEATHER_ROOT.child('sunmoon_today.txt')
    tomorrow_filename = settings.WEATHER_ROOT.child('sunmoon_tomorrow.txt')
    today_rstt = SunMoonTimes()
    tomorrow_rstt = SunMoonTimes()
    current_phase = None

    def __init__(self, **kwargs):
        '''
        Obtain latest aa.usno.navy.mil "Rise Set Transit Times" for
        Sun and Moon.
        '''
        super(SunMoon, self).__init__(**kwargs)

        today = datetime.date.today()
        today_string = today.strftime("%m/%d/%Y")
        today_url = self.url_pattern.format(date=today_string)
        response = get_URL_data(today_url, self.today_filename,
                                max_file_age=12*60)
        rstt = json.loads(response)
        self.set_times(rstt, self.today_rstt)
        self.pubdate = self.today_rstt.pubdate
        self.set_timestamp()

        # Get current moon phase
        if 'curphase' in rstt:
            self.current_phase = "{} ({})".format(rstt['curphase'],
                                                  rstt['fracillum'])
        else:
            self.current_phase = "{}".format(rstt['closestphase']['phase'])

        tomorrow = today + datetime.timedelta(days=1)
        tomorrow_string = tomorrow.strftime("%m/%d/%Y")
        tomorrow_url = self.url_pattern.format(date=tomorrow_string)
        response = get_URL_data(tomorrow_url, self.tomorrow_filename,
                                max_file_age=12*60)
        rstt = json.loads(response)
        self.set_times(rstt, self.tomorrow_rstt)

    def set_times(self, rstt, times):

        if not rstt or rstt['error']:
            self.error = True
            self.add_section('Origin Data Error',
                             'computation (parameters?) unsuccessful')
            return

        # Get the data we want
        times.pubdate = "{}-{}-{} 00:00:01 -0700".format(rstt['year'],
                                                         rstt['month'],
                                                         rstt['day'])

        try:
            for item in rstt['sundata']:
                if item['phen'] == 'BC':
                    times.twilight_begin = item['time'].rsplit(' ', 1)[0]
                elif item['phen'] == 'R':
                    times.sunrise = item['time'].rsplit(' ', 1)[0]
                elif item['phen'] == 'S':
                    times.sunset = item['time'].rsplit(' ', 1)[0]
                elif item['phen'] == 'EC':
                    times.twilight_end = item['time'].rsplit(' ', 1)[0]
        except KeyError:
            pass

        try:
            for item in rstt['moondata']:
                if item['phen'] == 'R':
                    times.moonrise = item['time'].rsplit(' ', 1)[0]
                elif item['phen'] == 'S':
                    times.moonset = item['time'].rsplit(' ', 1)[0]
        except KeyError:
            pass

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
                                max_file_age=12*60)
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
            phase_data.pubdate = "{}-{}-{} 00:00:01 -0700".format(phases['year'],
                                                                  phases['month'],
                                                                  phases['day'])
            phase_data.name = phase['phase']


            date = dateutilparser.parse(phase['date'] + ' ' + phase['time'])
            phase_data.date = date.strftime("%b %d, %Y")
            phase_data.time = date.strftime("%I:%M %p")
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
