from __future__ import absolute_import

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic.base import RedirectView

from .models import Recipe, Foodstuff, Category


class FoodRedirectView(RedirectView):
    """
    Redirection for old 'cocktail URL paths.
    """
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        if kwargs['recipe_type'] == 'cocktail':
            kwargs['recipe_type'] = 'drink'
        return super(FoodRedirectView, self).get_redirect_url(*args, **kwargs)


class RecipeListRedirectView(FoodRedirectView):

    pattern_name = 'food:recipe-list'


class RecipeDetailRedirectView(FoodRedirectView):

    pattern_name = 'food:recipe-detail'


class IngredientListRedirectView(FoodRedirectView):

    pattern_name = 'food:ingredient-list'


class CategoryListRedirectView(FoodRedirectView):

    pattern_name = 'food:category-list'


def recipe_list(request, recipe_type=""):
    all_recipes, all_foodstuff = get_all_lists(recipe_type)
    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or 'iphone' in request.GET:
        c = RequestContext(request, {'recipe_list': all_recipes,
                                     'foodstuff_list': all_foodstuff,
                                     'recipe_type': recipe_type,
                                     })
        if 'snippet' in request.GET:
            return render_to_response('food/iphone/recipe_snippet.html', c)
        elif 'iui' in request.GET:
            return render_to_response('food/iphone/recipe.html', c)
        else:
            return render_to_response('food/iphone/recipe_initial.html', c)
    else:
        c = RequestContext(request, {'all_recipes': all_recipes,
                                     'recipe_type': recipe_type,
                                     })
        return render_to_response('food/recipe_list.html', c)


def recipe_detail(request, slug, recipe_type=""):
    r = get_object_or_404(Recipe, slug=slug)

    all_recipes, all_foodstuff = get_all_lists(recipe_type)
    all_categories = Category.objects.all().order_by('title')

    # get ingredients for this recipe
    ingredient_list = []
    for ingredient in (r.ingredients.all()
                       .select_related('foodstuff')
                       .order_by('rank')):
        ingredient_list.append(ingredient)

    c = RequestContext(request, {'recipe_list': all_recipes,
                                 'foodstuff_list': all_foodstuff,
                                 'category_list': all_categories,
                                 'recipe_type': recipe_type,
                                 'recipe': r,
                                 'ingredients': ingredient_list,
                                 })

    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or 'iphone' in request.GET:
        if 'snippet' in request.GET:
            return render_to_response('food/iphone/recipe_snippet.html', c)
        elif 'iui' in request.GET:
            return render_to_response('food/iphone/recipe.html', c)
        else:
            return render_to_response('food/iphone/recipe_initial.html', c)
    else:
        return render_to_response('food/recipe_detail.html', c)


def foodstuff_list(request, recipe_type=""):
    all_recipes, all_foodstuff = get_all_lists(recipe_type)
    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or 'iphone' in request.GET:
        c = RequestContext(request, {'recipe_list': all_recipes,
                                     'foodstuff_list': all_foodstuff,
                                     'recipe_type': recipe_type,
                                     })
        if 'snippet' in request.GET:
            return render_to_response('food/iphone/foodstuff_snippet.html', c)
        elif 'iui' in request.GET:
            return render_to_response('food/iphone/foodstuff.html', c)
        else:
            return render_to_response('food/iphone/foodstuff_initial.html', c)
    else:
        c = RequestContext(request, {'all_foodstuff': all_foodstuff,
                                     'recipe_type': recipe_type,
                                     })
        return render_to_response('food/foodstuff_list.html', c)


def foodstuff_detail(request, slug, recipe_type=""):
    f = get_object_or_404(Foodstuff, slug=slug)

    recipe_list = (Recipe.objects.filter(ingredients__foodstuff=f)
                   .order_by('rclass', 'title'))
    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or 'iphone' in request.GET:
        all_recipes, all_foodstuff = get_all_lists(recipe_type)
        c = RequestContext(request, {'recipe_list': all_recipes,
                                     'foodstuff_list': all_foodstuff,
                                     'foodstuff': f,
                                     'recipes': recipe_list,
                                     })
        if 'snippet' in request.GET:
            return render_to_response('food/iphone/foodstuff_snippet.html', c)
        elif 'iui' in request.GET:
            return render_to_response('food/iphone/foodstuff.html', c)
        else:
            return render_to_response('food/iphone/foodstuff_initial.html', c)
    else:
        c = RequestContext(request, {'foodstuff': f,
                                     'recipes': recipe_list,
                                     })
        return render_to_response('food/foodstuff_detail.html', c)


def category_list(request, recipe_type, slug):
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return HttpResponseRedirect(
            reverse('food:recipe-list', kwargs={'recipe_type': recipe_type}))

    category_recipes = Recipe.objects.filter(
        rclass=db_recipe_type(recipe_type),
        categories=category)
    c = RequestContext(request, {'all_recipes': category_recipes,
                                 'recipe_type': recipe_type,
                                 'category': category,
                                 })
    return render_to_response('food/recipe_list.html', c)


def get_all_lists(recipe_type):
    all_recipes = (Recipe.objects.filter(rclass=db_recipe_type(recipe_type))
                   .order_by('title'))
    all_foodstuffs = Foodstuff.objects.filter(
        ingredients__recipe__rclass=db_recipe_type(recipe_type)) \
        .distinct().order_by('title')
    return all_recipes, all_foodstuffs


def db_recipe_type(recipe_type):
    if recipe_type == "drink":
        return Recipe.DRINK_CLASS
    else:
        return Recipe.EAT_CLASS
