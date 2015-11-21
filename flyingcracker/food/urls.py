from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^i/(?P<slug>[\w_-]+)/$', views.foodstuff_detail,
        name='food-ingredient-detail'),
    url(r'^i/$', views.foodstuff_list,
        name='food-ingredient-list'),
    url(r'^c/(?P<slug>[\w_-]+)/$', views.category_list,
        name='food-category-list'),
    url(r'^(?P<slug>[\w_-]+)/$', views.recipe_detail,
        name='food-recipe-detail'),
    url(r'^$', views.recipe_list,
        name='food-recipe-list'),
]
