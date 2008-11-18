import datetime
from django.utils.encoding import smart_str
from dateutil import parser as dateutilparser
from dateutil.tz import tzlocal
from fc3.weatherstation.tz import USTimeZone

class Forecast(object):
    
    def __init__(self):
        self.pubdate = None
        self.area = None
        self.warning = None
        self.sections = []
        self.reported_by = None
        self.timestamp = None
        self.stale = False
        
    def add_section(self, title, body):
        self.sections.append({'title': title, 'body': body})

    def set_timestamp(self, pubdate = None):
        if pubdate == None:
            pubdate = self.pubdate
        if pubdate:
            self.timestamp = dateutilparser.parse(pubdate)
            mountain_tz = USTimeZone(-7, "Mountain", "MST", "MDT")
            self.timestamp = self.timestamp.astimezone(mountain_tz)
            
            # figure out if the publication time is old
            now = datetime.datetime.now(tzlocal()).astimezone(mountain_tz)
            if (now - self.timestamp) > datetime.timedelta(hours=24):
                self.stale = True
        
    def __repr__(self):
        s = ''
        if self.pubdate:
            s += "Forecast pubdate: " + self.pubdate + "\n"
        if self.timestamp:
            s += "Forecast timestamp: " + self.timestamp.strftime("%H:%M %Z %a %b %d, %Y") + "\n"
        if self.area:
            s += "Forecast Area: " + smart_str(self.area) + "\n"
        if self.warning:
            s += "Warning: " + smart_str(self.warning) + "\n"
        for sec in self.sections:
            s += smart_str(sec['title']) + ": " + smart_str(sec['body']) + "\n"
        if self.reported_by:
            s += "Reported by: " + smart_str(self.reported_by) + "\n"
        return s

