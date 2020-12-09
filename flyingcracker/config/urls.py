from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import re_path
from django.views import static as static_views

from fc3 import pattern_views
from food import views as food_views

urlpatterns = [
    # Admin URLs
    re_path(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    re_path(r'^admin/', admin.site.urls),
    # Application URLs
    re_path(r'^cam/', include('cam.urls')),
    re_path(r'^(?P<recipe_type>drink|food)/', include('food.urls')),
    re_path(r'^ingredient/(?P<slug>[\w_-]+)/$', food_views.foodstuff_detail, name='ingredient-detail'),
    # deprecated urls
    re_path(r'^(?P<recipe_type>cocktail)/', include('food.redirect_urls')),
    re_path(r'^weatherstation/', include('weatherstation.urls')),
    re_path(r'^weather/', include('weather.urls')),
    re_path(r'^', include('home.urls')),
]

if pattern_views and settings.DEBUG:
    urlpatterns += [
        re_path(r'^patterns/$', pattern_views.show_url_patterns),
    ]

if settings.STATIC_URL[:5] != 'http:':
    urlpatterns += [
        re_path(
            r'^' + settings.STATIC_URL + '(?P<path>.*)$',
            static_views.serve,
            {'document_root': settings.STATIC_ROOT},
        ),
    ]

if hasattr(settings, 'LOCAL_URL') and hasattr(settings, 'LOCAL_ROOT'):
    urlpatterns += [
        re_path(
            r'^' + settings.LOCAL_URL + '/(?P<path>.*)$',
            static_views.serve,
            {'document_root': settings.LOCAL_ROOT},
        ),
    ]
