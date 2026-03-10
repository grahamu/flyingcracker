import pytz
from django import template
from django.conf import settings
from django.utils.encoding import smart_bytes

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
        dt = pytz.utc.localize(dt)
    return dt.astimezone(pytz.timezone(smart_bytes(timezone)))
