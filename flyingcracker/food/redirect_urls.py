from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.RecipeListRedirectView.as_view()),
    url(r'^ingredients/$', views.IngredientListRedirectView.as_view()),
    url(r'^(?P<slug>[\w_-]+)/$', views.RecipeDetailRedirectView.as_view()),
    url(r'^c/(?P<slug>[\w_-]+)/$', views.CategoryListRedirectView.as_view()),
]
