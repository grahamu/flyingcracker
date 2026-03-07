from django.db.models.functions import Lower
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
        if kwargs["recipe_type"] == "cocktail":
            kwargs["recipe_type"] = "drink"
        return super(FoodRedirectView, self).get_redirect_url(*args, **kwargs)


class RecipeListRedirectView(FoodRedirectView):

    pattern_name = "food:recipe-list"


class RecipeDetailRedirectView(FoodRedirectView):

    pattern_name = "food:recipe-detail"


class IngredientListRedirectView(FoodRedirectView):

    pattern_name = "food:ingredient-list"


class CategoryListRedirectView(FoodRedirectView):

    pattern_name = "food:category-detail"


def recipe_list(request, recipe_type=""):
    all_recipes, all_foodstuff, all_categories = get_all_lists(recipe_type)
    context = {
        "recipe_list": all_recipes,
        "foodstuff_list": all_foodstuff,
        "category_list": all_categories,
        "matching_recipes": all_recipes,
        "recipe_type": recipe_type,
    }
    return render(request, "food/recipe_list.html", context)


def recipe_detail(request, slug, recipe_type=""):
    r = get_object_or_404(Recipe, slug=slug)
    all_recipes, all_foodstuff, all_categories = get_all_lists(recipe_type)

    ingredient_list = list(
        r.ingredients.all().select_related("foodstuff").order_by("rank")
    )

    recipe_category_slugs = set(r.categories.values_list("slug", flat=True))
    context = {
        "recipe_list": all_recipes,
        "foodstuff_list": all_foodstuff,
        "category_list": all_categories,
        "recipe_type": recipe_type,
        "recipe": r,
        "ingredients": ingredient_list,
        "recipe_category_slugs": recipe_category_slugs,
    }
    return render(request, "food/recipe_detail.html", context)


def foodstuff_list(request, recipe_type=""):
    all_recipes, all_foodstuff, all_categories = get_all_lists(recipe_type)
    context = {
        "recipe_list": all_recipes,
        "foodstuff_list": all_foodstuff,
        "category_list": all_categories,
        "all_foodstuff": all_foodstuff,
        "recipe_type": recipe_type,
    }
    return render(request, "food/foodstuff_list.html", context)


def foodstuff_detail(request, recipe_type, slug):
    f = get_object_or_404(Foodstuff, slug=slug)
    all_recipes, all_foodstuff, all_categories = get_all_lists(recipe_type)

    recipe_list = Recipe.objects.filter(
        ingredients__foodstuff=f, rclass=db_recipe_type(recipe_type)
    ).prefetch_related("categories").order_by(Lower("title"))

    context = {
        "recipe_list": all_recipes,
        "foodstuff_list": all_foodstuff,
        "category_list": all_categories,
        "foodstuff": f,
        "matching_recipes": recipe_list,
        "recipe_type": recipe_type,
    }
    return render(request, "food/foodstuff_detail.html", context)


def category_detail(request, recipe_type, slug):
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return HttpResponseRedirect(
            reverse("food:recipe-list", kwargs={"recipe_type": recipe_type})
        )
    category_recipes = Recipe.objects.filter(
        rclass=db_recipe_type(recipe_type), categories=category
    ).prefetch_related("categories").order_by(Lower("title"))

    all_recipes, all_foodstuff, all_categories = get_all_lists(recipe_type)
    context = {
        "recipe_list": all_recipes,
        "foodstuff_list": all_foodstuff,
        "category_list": all_categories,
        "category": category,
        "matching_recipes": category_recipes,
        "recipe_type": recipe_type,
    }
    return render(request, "food/category_list.html", context)


def get_all_lists(recipe_type):
    all_recipes = Recipe.objects.filter(rclass=db_recipe_type(recipe_type)).prefetch_related("categories").order_by(
        Lower("title")
    )
    all_foodstuffs = (
        Foodstuff.objects.filter(
            ingredients__recipe__rclass=db_recipe_type(recipe_type)
        )
        .distinct()
        .order_by(Lower("title"))
    )
    all_categories = Category.objects.all().order_by("title")
    return all_recipes, all_foodstuffs, all_categories


def db_recipe_type(recipe_type):
    if recipe_type == "drink":
        return Recipe.DRINK_CLASS
    else:
        return Recipe.EAT_CLASS
