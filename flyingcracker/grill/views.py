from __future__ import absolute_import

from django.shortcuts import render_to_response
from django.template import RequestContext

from .models import (
    Food,
    Doneness,
    Grilling,
    Hardware,
)


def grill(request):
    '''
    Passes to the main template:
    `food_list` - a list of all Food items
    `food` - currently selected Food object
    `doneness` - currently selected Doneness object
    `hardware` - currently selected Hardware object
    `less_done` - Doneness id or None
    `more_done` - Doneness id or None
    `grill_items` - list of dicts containing a Cut, Method,
                    and Grilling.details
    '''
    food_list = Food.objects.all()
    hardware_list = Hardware.objects.all()

    if 'snippet' in request.GET:
        # parameters expected
        food_id = request.GET.get('food', 1)
        doneness_id = request.GET.get('doneness', 2)
        hardware_id = request.GET.get('hardware', 1)
    else:
        # no parameters expected, but check for cookies
        food_id = 1
        doneness_id = 2
        hardware_id = 1

    food = Food.objects.get(id=food_id)
    doneness = Doneness.objects.get(id=doneness_id)
    hardware = Hardware.objects.get(id=hardware_id)
    doneness_list = (Doneness.objects.filter(grilling__food=food,
                                             grilling__hardware=hardware)
                     .distinct())
    grill_items = Grilling.objects.filter(food=food, doneness=doneness,
                                          hardware=hardware)
    if not grill_items:
        if doneness_list:
            doneness = doneness_list[0]
            grill_items = Grilling.objects.filter(food=food, doneness=doneness)

    c = RequestContext(request, {'food_list': food_list,
                                 'doneness_list': doneness_list,
                                 'hardware_list': hardware_list,
                                 'food': food,
                                 'doneness': doneness,
                                 'hardware': hardware,
                                 'grill_items': grill_items,
                                 })

    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or 'iphone' in request.GET:
        if 'snippet' in request.GET:
            return render_to_response('grill/iphone/snippet.html', c)
        elif 'iui' in request.GET:
            return render_to_response('grill/iphone/iui.html', c)
        else:
            return render_to_response('grill/iphone/grill.html', c)
    else:
        # BUGBUG 2008-11-13 - Should be using "normal" browser templates,
        #        if they are different from the iPhone templates.
        if 'snippet' in request.GET:
            return render_to_response('grill/iphone/snippet.html', c)
        elif 'iui' in request.GET:
            return render_to_response('grill/iphone/iui.html', c)
        else:
            return render_to_response('grill/iphone/grill.html', c)


def doneness_detail(request, slug):
    doneness = Doneness.objects.get(slug=slug)
    c = RequestContext(request, {'doneness': doneness,
                                 })
    return render_to_response('grill/iphone/doneness_detail.html', c)
