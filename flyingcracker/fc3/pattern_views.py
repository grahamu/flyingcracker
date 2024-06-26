from django.http import HttpResponse
from django.urls import get_resolver

intro_text = """Named URL patterns for the {% url %} tag
========================================

e.g. {% url pattern-name %}
or   {% url pattern-name arg1 %} if the pattern requires arguments

"""


def show_url_patterns(request):
    patterns = _get_named_patterns()
    r = HttpResponse(intro_text, content_type="text/plain")
    longest = max([len(pair[0]) for pair in patterns])
    for key, value in patterns:
        r.write("%s %s\n" % (key.ljust(longest + 1), value))
    return r


def _get_named_patterns():
    "Returns list of (pattern-name, pattern) tuples"
    resolver = get_resolver(None)
    patterns = sorted(
        [
            (key, value[0][0][0])
            for key, value in list(resolver.reverse_dict.items())
            if isinstance(key, str)
        ]
    )
    return patterns
