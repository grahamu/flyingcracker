#!/usr/bin/env python
from xml.etree.ElementTree import XML
from xml.parsers.expat import ExpatError
from fc3.settings import WEATHER_ROOT
from forecast import Forecast
from utils import get_URL_data, save_URL_data


class CBTV(Forecast):

    url = 'http://www.cbtv.tv/RSS/CrestedButteCurrentWeatherReport.xml'
    filename = WEATHER_ROOT + 'cbtv.txt'

    def __init__(self, **kwargs):
        '''
        Obtain latest CBTV RSS feed
        Parse into the pieces we want (synopsis, today, tonight, tomorrow)
        Format nicely into parts
        '''
        super(CBTV, self).__init__(**kwargs)
        xml_text = get_URL_data(CBTV.url, CBTV.filename, max_file_age=10)
        if not xml_text:
            return None
        
        try:
            xml = XML(xml_text)
        except ExpatError, info:
            return None;    # fail silently
        
        rss = xml
        channel = rss.find('channel')
        item = channel.find('item')
        
        # Get the data we want
        pubdate = item.findtext('pubDate')
        synopsis = item.findtext("description")
    
        self.pubdate = pubdate
        self.set_timestamp()
        self.add_section('Synopsis', synopsis.strip())
    
def save_data():
    save_URL_data(CBTV.url, CBTV.filename)


def test():
    cbtv = CBTV()
    print repr(cbtv)
    
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
