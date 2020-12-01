#!/usr/bin/env python
from xml.etree.ElementTree import XML, ParseError
from xml.parsers.expat import ExpatError

from bs4 import BeautifulSoup
from django.conf import settings

from .forecast import Forecast
from .utils import get_URL_data, save_URL_data


class CBAC(Forecast):

    url = 'http://cbavalanchecenter.org/category/weather/feed/'
    filename = settings.WEATHER_ROOT.child('cbac.txt')

    def __init__(self, **kwargs):
        """
        Obtain latest CBAC RSS feed
        Parse into the pieces we want (synopsis, today, tonight, tomorrow)
        Format nicely into parts
        """
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
        pubdate = item.find('pubDate')
        if pubdate is None:
            self.report_error('No "pubDate"')
            return

        html_text = item.find('description')
        soup = BeautifulSoup(html_text.text, "html.parser")
        contents = soup.contents.get(4, None)
        if not contents:
            synopsis = ""
        else:
            synopsis = soup.contents[4].text

        self.pubdate = pubdate.text
        self.set_timestamp()
        self.add_section('Synopsis', synopsis)


def save_data():
    save_URL_data(CBAC.url, CBAC.filename)


def test():
    cbac = CBAC()
    print((repr(cbac)))


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
