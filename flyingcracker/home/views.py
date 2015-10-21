from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required


def home(request):
    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or request.GET.has_key('iphone'):
        c = RequestContext(request)
        return render_to_response('home/iphone/home.html', c)
    else:
        return HttpResponseRedirect(reverse('weather-root'))

def about(request):
    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or request.GET.has_key('iphone'):
        c = RequestContext(request)
        return render_to_response('home/iphone/about.html', c)
    else:
        return HttpResponseRedirect(reverse('weather-root'))
