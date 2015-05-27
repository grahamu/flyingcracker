#!/usr/bin/env python
import datetime
import math
from pygooglechart import (
    Axis,
    XYLineChart,
)

DAY_EVERY_HOUR_DATA = [i for i in range(0, 24 + 1)]
DAY_EVERY_HALFHOUR_DATA = [i for i in range(0, (24 * 2) + 1)]
DAY_EVERY_10_MINUTES_DATA = [i for i in range(0, (24 * 6) + 1)]
DAY_EVERY_3HOURS_LABELS = ['', '3a', '6a', '9a', '12', '3p', '6p', '9p', '']
DAY_EVERY_2HOURS_LABELS = ['', '2a', '4a', '6a', '8a', '10a',
                           '12', '2p', '4p', '6p', '8p', '10p', '']
DAY_EVERY_HOUR_LABELS = ['', '1a', '2a', '3a', '4a', '5a', '6a',
                         '7a', '8a', '9a', '10a', '11a', '12',
                         '1p', '2p', '3p', '4p', '5p', '6p',
                         '7p', '8p', '9p', '10p', '11p', '',
                         ]


def xchart(x_data, x_labels, data_lists,
           y_floor, y_ceil,
           width, height, colors, line_widths):
    """
    Returns the URL for a chart where all datasets use the same X-axis values.
    Y-axis labels are shown on both sides of the graph.
    """
    data_list = [i for i in x_data if i is not None]
    x_floor = min(data_list)
    x_ceil = max(data_list)
    chart = XYLineChart(width, height,
                        x_range=(x_floor, x_ceil), y_range=(y_floor, y_ceil))
    for data in data_lists:
        chart.add_data(x_data)
        chart.add_data(data)
    axis_left_index = chart.set_axis_range(Axis.LEFT, y_floor, y_ceil)
    axis_right_index = chart.set_axis_range(Axis.RIGHT, y_floor, y_ceil)
    axis_bottom_index = chart.set_axis_labels(Axis.BOTTOM, x_labels)
    chart.set_axis_style(axis_left_index, '909090')
    chart.set_axis_style(axis_right_index, '909090')
    chart.set_axis_style(axis_bottom_index, 'B0B0B0')
    chart.set_colours(colors)
    index = 0
    for width in line_widths:
        chart.set_line_style(index, width)
        index += 1
    return chart


def day_chart_iphone(data_lists, floor, ceil,
                     width, height, colors, line_widths):
    '''
    Returns URL for a chart which expects 24 data points, one for each hour.
    X-axis labels are the hour of day every three hours.

    '''
    return xchart(DAY_EVERY_HOUR_DATA,
                  DAY_EVERY_3HOURS_LABELS,
                  data_lists, floor, ceil,
                  width, height, colors, line_widths)


def day_chart_normal(data_lists, floor, ceil,
                     width, height, colors, line_widths):
    '''
    Returns URL for a chart which expects 24*2 data points,
    one for every half hour.
    X-axis labels are the hour of day every hour.

    '''
    return xchart(DAY_EVERY_HOUR_DATA,
                  DAY_EVERY_2HOURS_LABELS,
                  data_lists, floor, ceil,
                  width, height, colors, line_widths)


def periodic_samples(qs, start, fudge, interval, periods):
    '''
    Returns a list of arbitrary type records (containing attribute
    'timestamp') from `qs`, one record for each target window during
    a total of 'periods' windows beginning at 'start'.

    `target` = `start` plus a (0 to `periods`) multiple of `interval`.
    A target window is defined as: `target`-`fudge` to `target`+`fudge`.
    The first record found in a target window is saved in the list
    and all other records in that window are ignored. If no record is
    found in the target window then None is placed in the list instead
    of a record.

    For instance if `start`=12:00, `fudge`=5 minutes, `interval`=30
    minutes, and `periods`=2, record timestamps must fall in the ranges
    11:55 - 12:05 and 12:25 - 12:35.

    Parameter types:
    `qs` = Queryset of records which have a "timestamp" field
    `start` = datetime.datetime
    `fudge` = datetime.timedelta
    `interval` = datetime.timedelta
    `periods` = integer

    '''
    dataset = []
    if len(qs):
        target = start
        end = start + (periods * interval)
        for rec in qs:
            if target >= end:
                break
            ts = rec.timestamp
            while ts > (target + fudge):
                dataset.append(None)
                target += interval
            if ts < (target - fudge):
                pass
            else:
                dataset.append(rec)
                target += interval
        # no more records, fill out the dataset with None values
        while target < end:
            dataset.append(None)
            target += interval
    return dataset


def hourly_data(qs, start):
    # normalize the starting date to midnight
    start = start.replace(hour=6, minute=0, second=0, microsecond=0)
    return periodic_samples(qs, start,
                            datetime.timedelta(minutes=5),
                            datetime.timedelta(hours=1), 24 + 1)


def halfhour_data(qs, start):
    # normalize the starting date to midnight
    start = start.replace(hour=6, minute=0, second=0, microsecond=0)
    return periodic_samples(qs, start,
                            datetime.timedelta(minutes=5),
                            datetime.timedelta(minutes=30), (24 * 2) + 1)


def ten_minute_data(qs, start):
    # normalize the starting date to midnight
    start = start.replace(hour=6, minute=0, second=0, microsecond=0)
    return periodic_samples(qs, start,
                            datetime.timedelta(minutes=2, seconds=30),
                            datetime.timedelta(minutes=10), (24 * 6) + 1)


def flex_floor(vals, prev):
    '''
    Returns the smallest value of the values in the vals list and prev.
    Formats the result according to the type of the first element in vals.

    '''
    vlist = [i for i in vals if i is not None]
    if not vlist:
        return prev
    else:
        if type(vlist[0]) == int:
            return int_floor(vals, prev)
        else:
            return float_floor(vals, prev)


def flex_ceil(vals, prev):
    '''
    Returns the largest value of the values in the vals list and prev.
    Formats the result according to the type of the first element in vals.

    '''
    vlist = [i for i in vals if i is not None]
    if not vlist:
        return prev
    else:
        if type(vlist[0]) == int:
            return int_ceil(vals, prev)
        else:
            return float_ceil(vals, prev)


def int_floor(vals, prev):
    '''
    Returns the smallest value in vals and prev in integer format.

    '''
    vlist = [i for i in vals if i is not None]
    vlist.append(prev)
    # Round down to nearest ten
    return int(math.floor(float(min(vlist)) / 10.0) * 10)


def int_ceil(vals, prev):
    '''
    Returns the largest value in vals and prev in integer format.

    '''
    top = max(max(vals), prev)
    # Round up to nearest ten
    return int(math.ceil(float(top) / 10.0) * 10)


def float_floor(vals, prev):
    '''
    Returns the smallest value in vals and prev in float format.

    '''
    vlist = [i for i in vals if i is not None]
    vlist.append(prev)
    # round down to nearest tenth
    return math.floor(float(min(vlist)) * 10.0) / 10.0


def float_ceil(vals, prev):
    '''
    Returns the largest value in vals and prev in float format.

    '''
    top = max(max(vals), prev)
    # round up to nearest tenth
    return math.ceil(float(top) * 10.0) / 10.0


def test(date=datetime.datetime.now()):
    from fc3.utils import ElapsedTime
    from weatherstation.models import Weather

    def get_and_process(et, date):
        qs = Weather.objects.filter(
            timestamp__year=date.year,
            timestamp__month=date.month,
            timestamp__day=date.day).order_by('timestamp')
        if qs:
            et.mark_time('obtained qs for %s' % str(date))
            hourly_data(qs, date)
            et.mark_time('processed hourly_data()')

    et = ElapsedTime(totals=True)

    get_and_process(et, date)
    date -= datetime.timedelta(days=1)
    get_and_process(et, date)
    date -= datetime.timedelta(days=1)
    get_and_process(et, date)

    for e in et.list():
        print e.label, e.elapsed

if __name__ == '__main__':
    test()
