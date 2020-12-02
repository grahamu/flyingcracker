from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic.base import RedirectView

from .models import Category, Foodstuff, Recipe


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
        context = {
            'recipe_list': all_recipes,
            'foodstuff_list': all_foodstuff,
            'recipe_type': recipe_type,
        }
        if 'snippet' in request.GET:
            return render(request, 'food/iphone/recipe_snippet.html', context)
        elif 'iui' in request.GET:
            return render(request, 'food/iphone/recipe.html', context)
        else:
            return render(request, 'food/iphone/recipe_initial.html', context)
    else:
        context = {
            'all_recipes': all_recipes,
            'recipe_type': recipe_type,
        }
        return render(request, 'food/recipe_list.html', context)


def recipe_detail(request, slug, recipe_type=""):
    r = get_object_or_404(Recipe, slug=slug)

    all_recipes, all_foodstuff = get_all_lists(recipe_type)
    all_categories = Category.objects.all().order_by('title')

    # get ingredients for this recipe
    ingredient_list = []
    for ingredient in r.ingredients.all().select_related('foodstuff').order_by('rank'):
        ingredient_list.append(ingredient)

    context = {
        'recipe_list': all_recipes,
        'foodstuff_list': all_foodstuff,
        'category_list': all_categories,
        'recipe_type': recipe_type,
        'recipe': r,
        'ingredients': ingredient_list,
    }

    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or 'iphone' in request.GET:
        if 'snippet' in request.GET:
            return render(request, 'food/iphone/recipe_snippet.html', context)
        elif 'iui' in request.GET:
            return render(request, 'food/iphone/recipe.html', context)
        else:
            return render(request, 'food/iphone/recipe_initial.html', context)
    else:
        return render(request, 'food/recipe_detail.html', context)


def foodstuff_list(request, recipe_type=""):
    all_recipes, all_foodstuff = get_all_lists(recipe_type)
    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or 'iphone' in request.GET:
        context = {
            'recipe_list': all_recipes,
            'foodstuff_list': all_foodstuff,
            'recipe_type': recipe_type,
        }
        if 'snippet' in request.GET:
            return render(request, 'food/iphone/foodstuff_snippet.html', context)
        elif 'iui' in request.GET:
            return render(request, 'food/iphone/foodstuff.html', context)
        else:
            return render(request, 'food/iphone/foodstuff_initial.html', context)
    else:
        context = {
            'all_foodstuff': all_foodstuff,
            'recipe_type': recipe_type,
        }
        return render(request, 'food/foodstuff_list.html', context)


def foodstuff_detail(request, slug, recipe_type=""):
    f = get_object_or_404(Foodstuff, slug=slug)

    recipe_list = Recipe.objects.filter(ingredients__foodstuff=f).order_by('rclass', 'title')
    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or 'iphone' in request.GET:
        all_recipes, all_foodstuff = get_all_lists(recipe_type)
        context = {
            'recipe_list': all_recipes,
            'foodstuff_list': all_foodstuff,
            'foodstuff': f,
            'recipes': recipe_list,
        }
        if 'snippet' in request.GET:
            return render(request, 'food/iphone/foodstuff_snippet.html', context)
        elif 'iui' in request.GET:
            return render(request, 'food/iphone/foodstuff.html', context)
        else:
            return render(request, 'food/iphone/foodstuff_initial.html', context)
    else:
        context = {
            'foodstuff': f,
            'recipes': recipe_list,
        }
        return render(request, 'food/foodstuff_detail.html', context)


def category_list(request, recipe_type, slug):
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return HttpResponseRedirect(
            reverse('food:recipe-list', kwargs={'recipe_type': recipe_type})
        )

    category_recipes = Recipe.objects.filter(
        rclass=db_recipe_type(recipe_type), categories=category
    )
    context = {
        'all_recipes': category_recipes,
        'recipe_type': recipe_type,
        'category': category,
    }
    return render(request, 'food/recipe_list.html', context)


def get_all_lists(recipe_type):
    all_recipes = Recipe.objects.filter(rclass=db_recipe_type(recipe_type)).order_by('title')
    all_foodstuffs = (
        Foodstuff.objects.filter(ingredients__recipe__rclass=db_recipe_type(recipe_type))
        .distinct()
        .order_by('title')
    )
    return all_recipes, all_foodstuffs


def db_recipe_type(recipe_type):
    if recipe_type == "drink":
        return Recipe.DRINK_CLASS
    else:
        return Recipe.EAT_CLASS
