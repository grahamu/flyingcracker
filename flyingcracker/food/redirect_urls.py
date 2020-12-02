from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.RecipeListRedirectView.as_view()),
    re_path(r'^ingredients/$', views.IngredientListRedirectView.as_view()),
    re_path(r'^(?P<slug>[\w_-]+)/$', views.RecipeDetailRedirectView.as_view()),
    re_path(r'^c/(?P<slug>[\w_-]+)/$', views.CategoryListRedirectView.as_view()),
]
