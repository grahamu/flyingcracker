from django.conf.urls import url

from . import views

app_name = 'food'
urlpatterns = [
    url(r'^ingredients/$', views.foodstuff_list, name='ingredient-list'),
    url(r'^c/(?P<slug>[\w_-]+)/$', views.category_list, name='category-list'),
    url(r'^(?P<slug>[\w_-]+)/$', views.recipe_detail, name='recipe-detail'),
    url(r'^$', views.recipe_list, name='recipe-list'),
]
