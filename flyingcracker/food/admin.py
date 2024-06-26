from django.contrib import admin

from . import models as food


class FoodstuffAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(food.Foodstuff, FoodstuffAdmin)
admin.site.register(food.Attribute)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(food.Category, CategoryAdmin)


class IngredientInline(admin.TabularInline):
    model = food.Ingredient
    extra = 5


class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "teaser",
                    "attributes",
                    "categories",
                    "rclass",
                    "pub_date",
                )
            },
        ),
        (
            "directions, description, credit",
            {"fields": ("directions", "description", "credit")},
        ),
    )
    list_filter = ["rclass"]
    inlines = [
        IngredientInline,
    ]


admin.site.register(food.Recipe, RecipeAdmin)


# class FoodstuffInline(InlineModelAdmin):
#     model = food.Foodstuff


class IngredientAdmin(admin.ModelAdmin):
    pass
    # inlines = [
    #     FoodstuffInline,
    # ]


admin.site.register(food.Ingredient, IngredientAdmin)
admin.site.register(food.Link)
