#!/usr/bin/env python
from xml.etree.ElementTree import (
    ParseError,
    XML,
)
from xml.parsers.expat import ExpatError

from django.conf import settings

from forecast import Forecast
from utils import (
    get_URL_data,
    save_URL_data,
)


class CBAC(Forecast):

    url = 'http://cbavalanchecenter.org/feed/'
    filename = settings.WEATHER_ROOT.child('cbac.txt')

    def __init__(self, **kwargs):
        '''
        Obtain latest CBAC RSS feed
        Parse into the pieces we want (synopsis, today, tonight, tomorrow)
        Format nicely into parts
        '''
        super(CBAC, self).__init__(**kwargs)
        xml_text = get_URL_data(CBAC.url, CBAC.filename, max_file_age=10)
        if not xml_text:
            self.error = True
            self.add_section('Origin Data Error', 'No XML text found')
            return

        try:
            xml = XML(xml_text)
        except ExpatError:
            self.report_error('Bad XML')
            return
        except ParseError:
            self.report_error('Cannot parse XML')
            return

        rss = xml
        channel = rss.find('channel')
        if channel is None:
            self.report_error('No "channel"')
            return
        item = channel.find('item')
        if item is None:
            self.report_error('No "item"')
            return

        # Get the data we want
        pubdate = item.findtext('pubdate')
        if not pubdate:
            self.report_error('No "pubdate"')
            return

        report_el = item.find('report')
        if report_el is None:
            self.report_error('No "report"')
            return

        synopsis = report_el.findtext("weathersynopsis")
        reportedby = report_el.findtext("reportedby")

        forecast_el = report_el.find('forecast')
        if forecast_el is None:
            self.report_error('No "forecast"')
            return

        today = forecast_el.findtext('today')
        tonight = forecast_el.findtext('tonight')
        tomorrow = forecast_el.findtext('tomorrow')

        self.pubdate = pubdate
        self.set_timestamp()
        self.add_section('Synopsis', synopsis.strip())
        self.add_section('Today', today.strip())
        self.add_section('Tonight', tonight.strip())
        self.add_section('Tomorrow', tomorrow.strip())
        self.reported_by = reportedby.strip()


def save_data():
    save_URL_data(CBAC.url, CBAC.filename)


def test():
    cbac = CBAC()
    print repr(cbac)

if __name__ == '__main__':
    import optparse
    p = optparse.OptionParser()
    options, arguments = p.parse_args()

    if not arguments:
        test()
    else:
        for cmd in arguments:
            if cmd.lower() == 'save':
                save_data()
