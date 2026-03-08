from django.http import HttpResponseRedirect
from django.urls import reverse


def home(request):
    return HttpResponseRedirect(reverse("weather:root"))


def about(request):
    return HttpResponseRedirect(reverse("weather:root"))
