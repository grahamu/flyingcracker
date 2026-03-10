from datetime import timezone as dt_timezone
from zoneinfo import ZoneInfo

from django import template
from django.conf import settings
from django.utils.encoding import smart_str

register = template.Library()


@register.filter
def as_timezone(dt, timezone=None):
    """
    Convert `dt` to the specified timezone.
    If timezone is not provided, converts to settings.TIME_ZONE.
    If `dt` does not have timezone info it is assumed to be UTC.

    Usage:
        {{ datetime|as_timezone }}
        {{ datetime|as_timezone:"US/Mountain" }}
    """
    if timezone is None:
        timezone = settings.TIME_ZONE
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=dt_timezone.utc)
    return dt.astimezone(ZoneInfo(smart_str(timezone)))
