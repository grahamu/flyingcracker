import json
from decimal import Decimal

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.utils.functional import Promise


class JsonResponse(HttpResponse):
    def __init__(self, data):
        super(JsonResponse, self).__init__(
            json_encode2(data), content_type="text/javascript"
        )


def json_encode2(data):
    """
    The main issues with django's default json serializer is that
    properties that had been added to an object dynamically are
    being ignored (and it also has problems with some models).
    """

    def _any(data):
        ret = None
        # Oops, we used to check if it is of type list, but that fails
        # i.e. in the case of django.newforms.utils.ErrorList, which extends
        # the type "list". Oh man, that was a dumb mistake!
        if isinstance(data, list):
            ret = _list(data)
        # Same as for lists above.
        elif isinstance(data, dict):
            ret = _dict(data)
        elif isinstance(data, Decimal):
            # json.dumps() cant handle Decimal
            ret = str(data)
        elif isinstance(data, models.query.QuerySet):
            # Actually its the same as a list ...
            ret = _list(data)
        elif isinstance(data, models.Model):
            ret = _model(data)
        # here we need to encode the string as unicode
        # (otherwise we get utf-16 in the json-response)
        elif isinstance(data, str):
            ret = str(data)
        # see http://code.djangoproject.com/ticket/5868
        elif isinstance(data, Promise):
            ret = force_str(data)
        else:
            ret = data
        return ret

    def _model(data):
        ret = {}
        # If we only have a model, we only want to encode the fields.
        for f in data._meta.fields:
            ret[f.attname] = _any(getattr(data, f.attname))
        # And additionally encode arbitrary properties that had been added.
        fields = dir(data.__class__) + list(ret.keys())
        add_ons = [k for k in dir(data) if k not in fields]
        for k in add_ons:
            if k[0] != "_":
                ret[k] = _any(getattr(data, k))
        return ret

    def _list(data):
        ret = []
        for v in data:
            ret.append(_any(v))
        return ret

    def _dict(data):
        ret = {}
        for k, v in list(data.items()):
            ret[k] = _any(v)
        return ret

    ret = _any(data)

    return json.dumps(ret, cls=DjangoJSONEncoder)
