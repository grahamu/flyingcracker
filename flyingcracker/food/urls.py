from django.conf.urls import (
    patterns,
    url,
    include,
)


app_name = 'food'
urlpatterns = patterns('food.views',
    url(r'^i/(?P<slug>[\w_-]+)/$',         'foodstuff_detail', name='food-ingredient-detail'),
    url(r'^i/$',                           'foodstuff_list', name='food-ingredient-list'),
    url(r'^c/(?P<slug>[\w_-]+)/$',         'category_list', name='food-category-list'),
    url(r'^(?P<slug>[\w_-]+)/$',           'recipe_detail', name='food-recipe-detail'),
    url(r'^$',                             'recipe_list', name='food-recipe-list'),
)
