from __future__ import absolute_import

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from .models import Post

def special(request, page=[]):

    c = RequestContext(request, {'posts' : Post.objects.all(),
                                })

    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or request.GET.has_key('iphone'):
        if request.GET.has_key('snippet'):
            return render_to_response('miniblog/iphone/miniblog_snippet.html', c)
        elif request.GET.has_key('iui'):
            return render_to_response('miniblog/iphone/miniblog.html', c)
        else:
            return render_to_response('miniblog/iphone/miniblog_initial.html', c)
    else:
        return(404)