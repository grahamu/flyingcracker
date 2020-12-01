from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse


def home(request):
    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or 'iphone' in request.GET:
        c = RequestContext(request)
        return render('home/iphone/home.html', c)
    else:
        return HttpResponseRedirect(reverse('weather:root'))


def about(request):
    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or 'iphone' in request.GET:
        c = RequestContext(request)
        return render('home/iphone/about.html', c)
    else:
        return HttpResponseRedirect(reverse('weather:root'))
