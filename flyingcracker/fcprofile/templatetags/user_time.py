from datetime import datetime
from pytz import utc

from django import template

register = template.Library()


@register.filter
def user_time(user, dt=None):
    """
    Convert utc `dt` to the current timezone of the user (if `dt` is not
    provided, uses the current date/time.

    Usage:
        {{ user|user_time }}
        {{ user|user_time:utc_aware_time }}
    """
    if not dt:
        dt = datetime.utcnow()
    if not dt.tzinfo:
        dt = datetime(tzinfo=utc, *dt.timetuple()[:7])
    try:
        profile = user.get_profile()
    except Exception:
        profile = None
    if profile and profile.timezone:
        tz = profile.timezone
    else:
        tz = utc
    return dt.astimezone(tz)
