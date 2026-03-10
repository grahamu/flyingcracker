import datetime
import math

from datetime import timezone as dt_timezone

HOUR_LABELS = [
    "12a", "1a", "2a", "3a", "4a", "5a", "6a", "7a", "8a", "9a", "10a", "11a",
    "12p", "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p", "10p", "11p", "",
]


def periodic_samples(qs, start, fudge, interval, periods):
    """
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

    """
    dataset = []
    utc_tz = dt_timezone.utc

    if len(qs):
        target = start
        end = start + (periods * interval)
        for rec in qs:
            if target >= end:
                break

            # Ensure timestamp is timezone-aware UTC
            if rec.timestamp.tzinfo is None:
                ts = rec.timestamp.replace(tzinfo=utc_tz)
            else:
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
    return periodic_samples(
        qs, start, datetime.timedelta(minutes=5), datetime.timedelta(hours=1), 24 + 1
    )


def halfhour_data(qs, start):
    return periodic_samples(
        qs,
        start,
        datetime.timedelta(minutes=5),
        datetime.timedelta(minutes=30),
        (24 * 2) + 1,
    )


def ten_minute_data(qs, start):
    return periodic_samples(
        qs,
        start,
        datetime.timedelta(minutes=2, seconds=30),
        datetime.timedelta(minutes=10),
        (24 * 6) + 1,
    )


def flex_floor(vals, prev):
    """
    Returns the smallest value of the values in the vals list and prev.
    Formats the result according to the type of the first element in vals.

    """
    vlist = [i for i in vals if i is not None]
    if not vlist:
        return prev
    else:
        if type(vlist[0]) is int:
            return int_floor(vals, prev)
        else:
            return float_floor(vals, prev)


def flex_ceil(vals, prev):
    """
    Returns the largest value of the values in the vals list and prev.
    Formats the result according to the type of the first element in vals.

    """
    vlist = [i for i in vals if i is not None]
    if not vlist:
        return prev
    else:
        if type(vlist[0]) is int:
            return int_ceil(vals, prev)
        else:
            return float_ceil(vals, prev)


def int_floor(vals, prev):
    """
    Returns the smallest value in vals and prev in integer format.

    """
    vlist = [i for i in vals if i is not None]
    vlist.append(prev)
    # Round down to nearest ten
    return int(math.floor(float(min(vlist)) / 10.0) * 10)


def int_ceil(vals, prev):
    """
    Returns the largest value in vals and prev in integer format.

    """
    vlist = [i for i in vals if i is not None]
    vlist.append(prev)
    top = max(vlist)
    # Round up to nearest ten
    return int(math.ceil(float(top) / 10.0) * 10)


def float_floor(vals, prev):
    """
    Returns the smallest value in vals and prev in float format.

    """
    vlist = [i for i in vals if i is not None]
    vlist.append(prev)
    # round down to nearest tenth
    return math.floor(float(min(vlist)) * 10.0) / 10.0


def float_ceil(vals, prev):
    """
    Returns the largest value in vals and prev in float format.

    """
    vlist = [i for i in vals if i is not None]
    vlist.append(prev)
    top = max(vlist)
    # round up to nearest tenth
    return math.ceil(float(top) * 10.0) / 10.0


# def test(date=datetime.datetime.now()):
#     from fc3.utils import ElapsedTime
#     from weatherstation.models import Weather
#
#     def get_and_process(et, date):
#         qs = Weather.objects.filter(
#             timestamp__year=date.year,
#             timestamp__month=date.month,
#             timestamp__day=date.day).order_by('timestamp')
#         if qs:
#             et.mark_time('obtained qs for %s' % str(date))
#             hourly_data(qs, date)
#             et.mark_time('processed hourly_data()')
#
#     et = ElapsedTime(totals=True)
#
#     get_and_process(et, date)
#     date -= datetime.timedelta(days=1)
#     get_and_process(et, date)
#     date -= datetime.timedelta(days=1)
#     get_and_process(et, date)
#
#     for e in et.list():
#         print e.label, e.elapsed
#
# if __name__ == '__main__':
#     test()
