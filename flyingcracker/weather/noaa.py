import datetime
from dateutil import parser as dateutilparser
import os
from urllib import urlopen

from django.conf import settings

from forecast import Forecast

##
## This code parses weather data from NOAA
##


class NOAAForecastPreamble(object):
    """
    Parses (eats) junk data before NOAA forecast.
    """

    def __init__(self, zname):
        self.zname = zname

    def parse_line(self, line, forecast):
        if line.startswith(self.zname):
            return NOAAForecastArea, False
        else:
            return False, False


class NOAAForecastArea(object):
    """
    Parses NOAA forecast area section.
    """

    def __init__(self):
        self.area = []

    def parse_line(self, line, forecast):
        if line.startswith('.'):
            self.parse_area(forecast)
            # recycle this line because it is the start
            # of a different section.
            return NOAAForecastBody, True
        else:
            line = line.strip()
            if len(line) > 0 and not line.startswith('$$'):
                self.area.append(line)
            return False, False

    def parse_area(self, forecast):
        '''
        Parse the area section of the NOAA forecast.
        The first line is always the area.
        Next is an optional line including cities of interest.
        Next is a timestamp.
        '''
        pubdate = self.area.pop()               # last item is pubdate
        time_of_day, remainder = pubdate.split(' ', 1)
        # insert colon so parser recognizes the time string
        time_of_day = time_of_day[0:-2] + ':' + time_of_day[-2:]
        pubdate = ' '.join([time_of_day, remainder])
        forecast.pubdate = pubdate
        forecast.timestamp = dateutilparser.parse(forecast.pubdate)

        area = self.area.pop(0).capitalize()    # first item is area
        if area.endswith('-'):
            area = area[:-1]

        if len(self.area) > 0:              # middle is cities of interest
            interest = ''.join(self.area)
            interest = interest.split('...')
            city_list = []
            for city in interest[1:]:
                city_list.append(capitalize_all(city))
            cities = ', '.join(city_list)
            area_list = [area]
            area_list.append(interest[0].lower())
            area_list.append(cities)
            area = ' '.join(area_list)

        forecast.area = area


def capitalize_all(str):
    l = str.split(' ')
    l = [word.capitalize() for word in l]
    return ' '.join(l)


class NOAAForecastBody(object):
    """
    Parses NOAA forecast body.
    """
    def __init__(self):
        self.title = ''
        self.body = []

    def parse_line(self, line, forecast):
        if len(line) == 0:     # ignore this line
            return False, False

        if line.startswith('...'):
            # recycle this line, it starts a warning.
            return NOAAForecastWarning, True

        if line == '$$':    # end of the forecast sections
            self.add_section(forecast)
            return False, False

        if line == '&&':
            # Indicates some extra NOAA data, ignore all subsequent lines.
            self.add_section(forecast)
            return NOAAForecastIgnore, False

        if line[0] == '.' and line[1] != ' ':   # start of a new section
            self.add_section(forecast)
            title, body = line.split('...', 1)
            self.title = title[1:]
            self.body.append(body)
        else:
            self.body.append(line)
        return False, False

    def add_section(self, forecast):
        if self.title != '':
            body_str = ' '.join(self.body)
            sentences = body_str.split('. ')
            sentences = [s.capitalize() for s in sentences]
            body_str = '. '.join(sentences)
            forecast.add_section(self.title.capitalize(), body_str)
            # reset temporary section info
            self.body = []
            self.title = ''


class NOAAForecastWarning(object):
    """
    Parses NOAA warnings.
    """
    def __init__(self):
        self.warning = []
        pass

    def parse_line(self, line, forecast):
        self.warning.append(line)
        if line.endswith('...'):
            self.warning = ' '.join(self.warning)
            self.warning.replace('...', '')
            forecast.warning = self.warning
            return NOAAForecastBody, False      # done with the warning
        else:
            return False, False     # ignore line for now


class NOAAForecastIgnore(object):

    def parse_line(self, line, forecast):
        return False, False


class NOAAForecast(Forecast):

    def __init__(self, zname):
        super(NOAAForecast, self).__init__()
        self.state = NOAAForecastPreamble(zname)

    def set_state(self, state):
        self.state = state

    def parse_line(self, line):
        '''
        Calls the ``parseLine`` method of class ``self.state``.
        If a new state is indicated, set self.state.
        Use recursion to recycle the input line if necessary.
        '''
        newState, recycle_line = self.state.parse_line(line, self)
        if newState is not False:
            self.set_state(newState())
            if recycle_line:
                self.parse_line(line)


def get_NOAA_forecast(state, zone):
    '''
    Obtain NOAA textual forecast.
    Parse into parts: area, [optional] warning, section array.
    Returns a Forecast object if successful, otherwise returns None.
    '''
    zname = state.upper() + "Z%03d" % zone
    lines = get_NOAA_data(state, zname)
    if not lines:
        return None

    forecast = NOAAForecast(zname)
    for line in lines:
        forecast.parse_line(line.strip())

    # when we're finished with all lines the forecast attributes should be set
    return forecast


def get_NOAA_data(state, zname):
    """
    Get data from disk file if it exists, but
    ignore the data if it is more than 4 hours old.
    """
    filename = settings.WEATHER_ROOT.child('noaa-' + zname + '.txt')
    if not os.path.isfile(filename):
        return save_NOAA_data(state, zname)

    filetime_t = os.path.getmtime(filename)
    filestamp = datetime.datetime.fromtimestamp(filetime_t)
    now = datetime.datetime.now()
    if (now - filestamp) > datetime.timedelta(hours=3) or (now < filestamp):
        return save_NOAA_data(state, zname)

    try:
        f = open(filename, 'r')
    except:
        lines = save_NOAA_data(state, zname)
    else:
        try:
            lines = f.read().splitlines()
        except:
            lines = save_NOAA_data(state, zname)
    return lines


def save_NOAA_data(state, zname):
    url = 'http://tgftp.nws.noaa.gov/data/forecasts/zone/' + \
        state.lower() + '/' + zname.lower() + '.txt'
    try:
        lines = urlopen(url).readlines()
    except IOError:
        return None
    else:
        # save the retrieved data
        filename = settings.WEATHER_ROOT.child('noaa-' + zname + '.txt')
        f = open(filename, "w")
        f.writelines(lines)
        f.close()
        return lines


def test():
    forecast = get_NOAA_forecast('CO', 12)
    print repr(forecast)
    forecast = get_NOAA_forecast('CA', 1)
    print repr(forecast)
    forecast = get_NOAA_forecast('OR', 1)
    print repr(forecast)

if __name__ == '__main__':
    import optparse
    p = optparse.OptionParser()
    p.add_option('--zone', '-z', type="int", default=12)
    p.add_option('--state', '-s', default='CO')
    options, arguments = p.parse_args()

    if not arguments:
        test()
    else:
        for cmd in arguments:
            if cmd.lower() == 'save':
                state = options.state.upper()
                save_NOAA_data(state, state + "Z%03d" % options.zone)
            elif cmd.lower() == 'get':
                state = options.state.upper()
                print get_NOAA_data(state, state + "Z%03d" % options.zone)
