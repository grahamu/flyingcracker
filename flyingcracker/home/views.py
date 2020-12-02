from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def home(request):
    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or 'iphone' in request.GET:
        return render(request, 'home/iphone/home.html')
    else:
        return HttpResponseRedirect(reverse('weather:root'))


def about(request):
    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or 'iphone' in request.GET:
        return render(request, 'home/iphone/about.html')
    else:
        return HttpResponseRedirect(reverse('weather:root'))
