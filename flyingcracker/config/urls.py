from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views import static as static_views

from fc3 import pattern_views
from food import views as food_views

urlpatterns = [
    # Admin URLs
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    # Application URLs
    url(r'^cam/', include('cam.urls')),
    url(r'^(?P<recipe_type>drink|food)/', include('food.urls')),
    url(r'^ingredient/(?P<slug>[\w_-]+)/$', food_views.foodstuff_detail, name='ingredient-detail'),
    # deprecated urls
    url(r'^(?P<recipe_type>cocktail)/', include('food.redirect_urls')),
    url(r'^weatherstation/', include('weatherstation.urls')),
    url(r'^weather/', include('weather.urls')),
    url(r'^grill/', include('grill.urls')),
    url(r'^', include('home.urls')),
]

if pattern_views and settings.DEBUG:
    urlpatterns += [
        url(r'^patterns/$', pattern_views.show_url_patterns),
    ]

if settings.STATIC_URL[:5] != 'http:':
    urlpatterns += [
        url(
            r'^' + settings.STATIC_URL + '(?P<path>.*)$',
            static_views.serve,
            {'document_root': settings.STATIC_ROOT},
        ),
    ]

if hasattr(settings, 'LOCAL_URL') and hasattr(settings, 'LOCAL_ROOT'):
    urlpatterns += [
        url(
            r'^' + settings.LOCAL_URL + '/(?P<path>.*)$',
            static_views.serve,
            {'document_root': settings.LOCAL_ROOT},
        ),
    ]
