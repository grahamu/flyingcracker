from __future__ import absolute_import

from django.shortcuts import render_to_response
from django.template import RequestContext

from .models import Post


def special(request, page=[]):

    c = RequestContext(request, {'posts': Post.objects.all()})

    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or 'iphone' in request.GET:
        if 'snippet' in request.GET:
            return render_to_response(
                'miniblog/iphone/miniblog_snippet.html', c)
        elif 'iui' in request.GET:
            return render_to_response(
                'miniblog/iphone/miniblog.html', c)
        else:
            return render_to_response(
                'miniblog/iphone/miniblog_initial.html', c)
    else:
        return(404)
