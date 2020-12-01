import datetime

from dateutil import parser as dateutilparser
from dateutil.tz import tzlocal
from django.utils.encoding import smart_bytes
from pytz import timezone


class DataBlock(object):
    def __init__(self):
        self.pubdate = None
        self.sections = []
        self.timestamp = None
        self.stale = False
        self.error = False

    def add_section(self, title, body):
        self.sections.append({'title': title, 'body': body})

    def set_timestamp(self, pubdate=None):
        if pubdate is None:
            pubdate = self.pubdate
        if pubdate:
            mountain_tz = timezone('US/Mountain')
            timestamp = dateutilparser.parse(pubdate)
            self.timestamp = timestamp.astimezone(mountain_tz)

            # figure out if the publication time is not today
            now = datetime.datetime.now(tzlocal()).astimezone(mountain_tz)
            if now.day != self.timestamp.day:
                self.stale = True

    def report_error(self, error_str):
        self.error = True
        self.add_section('Problem obtaining valid data', error_str)
        self.timestamp = datetime.datetime.now(tzlocal())
        mountain_tz = timezone('US/Mountain')
        self.timestamp = self.timestamp.astimezone(mountain_tz)


class Forecast(DataBlock):
    def __init__(self):
        super(Forecast, self).__init__()
        self.area = None
        self.warning = None
        self.reported_by = None

    def __repr__(self):
        s = ''
        if self.pubdate:
            s += "Forecast pubdate: " + self.pubdate + "\n"
        if self.timestamp:
            s += "Forecast timestamp: " + self.timestamp.strftime("%H:%M %Z %a %b %d, %Y") + "\n"
        if self.area:
            s += "Forecast Area: " + smart_bytes(self.area) + "\n"
        if self.warning:
            s += "Warning: " + smart_bytes(self.warning) + "\n"
        for sec in self.sections:
            s += smart_bytes(sec['title']) + ": " + smart_bytes(sec['body']) + "\n"
        if self.reported_by:
            s += "Reported by: " + smart_bytes(self.reported_by) + "\n"
        if self.error:
            s += "Data Error\n"
        return s
