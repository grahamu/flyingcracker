from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template.defaultfilters import random
from food.models import Recipe, Foodstuff, Category

def category_list(request, recipe_type, slug):
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return HttpResponseRedirect(
            reverse('food-recipe-list', kwargs={'recipe_type': recipe_type}))
    category_recipes = Recipe.objects.filter(
        rclass=db_recipe_type(recipe_type),
        categories=category).order_by('title')
    c = RequestContext(request, {'all_recipes' : category_recipes,
                                 'recipe_type': recipe_type,
                                 'category': category,
                                })
    return render_to_response('food/recipe_list.html', c)

def recipe_list(request, recipe_type=""):
    all_recipes, all_foodstuff = get_all_lists(recipe_type)
    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or request.GET.has_key('iphone'):
        c = RequestContext(request, {'recipe_list' : all_recipes,
                                     'foodstuff_list': all_foodstuff,
                                     'recipe_type': recipe_type,
                                    })
        if request.GET.has_key('snippet'):
            return render_to_response('food/iphone/recipe_snippet.html', c)
        elif request.GET.has_key('iui'):
            return render_to_response('food/iphone/recipe.html', c)
        else:
            return render_to_response('food/iphone/recipe_initial.html', c)
    else:
        c = RequestContext(request, {'all_recipes' : all_recipes,
                                     'recipe_type': recipe_type,
                                    })
        return render_to_response('food/recipe_list.html', c)

def recipe_detail(request, slug, recipe_type=""):
    r = get_object_or_404(Recipe, slug=slug)

    all_recipes, all_foodstuff = get_all_lists(recipe_type)
    all_categories = Category.objects.all().order_by('title')

    # get ingredients for this recipe
    ingredient_list = []
    for ingredient in r.ingredients.all().order_by('rank'):
        ingredient_list.append(ingredient)

    c = RequestContext(request, {'recipe_list' : all_recipes,
                                 'foodstuff_list': all_foodstuff,
                                 'category_list': all_categories,
                                 'recipe_type': recipe_type,
                                 'recipe' : r,
                                 'ingredients' : ingredient_list,
                                })

    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or request.GET.has_key('iphone'):
        if request.GET.has_key('snippet'):
            return render_to_response('food/iphone/recipe_snippet.html', c)
        elif request.GET.has_key('iui'):
            return render_to_response('food/iphone/recipe.html', c)
        else:
            return render_to_response('food/iphone/recipe_initial.html', c)
    else:
        return render_to_response('food/recipe_detail.html', c)

def foodstuff_list(request, recipe_type=""):
    all_recipes, all_foodstuff = get_all_lists(recipe_type)
    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or request.GET.has_key('iphone'):
        c = RequestContext(request, {'recipe_list' : all_recipes,
                                     'foodstuff_list': all_foodstuff,
                                     'recipe_type': recipe_type,
                                    })
        if request.GET.has_key('snippet'):
            return render_to_response('food/iphone/foodstuff_snippet.html', c)
        elif request.GET.has_key('iui'):
            return render_to_response('food/iphone/foodstuff.html', c)
        else:
            return render_to_response('food/iphone/foodstuff_initial.html', c)
    else:
        c = RequestContext(request, {'all_foodstuff' : all_foodstuff,
                                     'recipe_type': recipe_type,
                                    })
        return render_to_response('food/foodstuff_list.html', c)

def foodstuff_detail(request, slug, recipe_type=""):
    f = get_object_or_404(Foodstuff, slug=slug)

    ingredient_list = f.ingredients.all().order_by('recipe')
    agent = request.META.get('HTTP_USER_AGENT')
    if (agent and agent.find('iPhone') != -1) or request.GET.has_key('iphone'):
        all_recipes, all_foodstuff = get_all_lists(recipe_type)
        c = RequestContext(request, {'recipe_list': all_recipes,
                                     'foodstuff_list' : all_foodstuff,
                                     'foodstuff' : f,
                                     'ingredients' : ingredient_list,
                                     'recipe_type': recipe_type,
                                    })
        if request.GET.has_key('snippet'):
            return render_to_response('food/iphone/foodstuff_snippet.html', c)
        elif request.GET.has_key('iui'):
            return render_to_response('food/iphone/foodstuff.html', c)
        else:
            return render_to_response('food/iphone/foodstuff_initial.html', c)
    else:
        c = RequestContext(request, {'foodstuff' : f,
                                     'ingredients' : ingredient_list,
                                     'recipe_type': recipe_type,
                                    })
        return render_to_response('food/foodstuff_detail.html', c)

def get_all_lists(recipe_type):
    all_recipes = Recipe.objects.filter(rclass=db_recipe_type(recipe_type)).order_by('title')
    all_foodstuffs = Foodstuff.objects.filter(ingredients__recipe__rclass=db_recipe_type(recipe_type)).distinct().order_by('title')
    return all_recipes, all_foodstuffs

def db_recipe_type(recipe_type):
    if recipe_type == "food":
        return Recipe.EAT_CLASS
    else:
        return Recipe.DRINK_CLASS
