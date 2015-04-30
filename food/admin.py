from django.contrib import admin
from django.contrib.contenttypes import generic
from django.db import models
import food.models as food
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User


class FoodstuffAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    
admin.site.register(food.Foodstuff, FoodstuffAdmin)
user = models.ForeignKey(settings.AUTH_USER_MODEL)
admin.site.register(food.Attribute)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(food.Category, CategoryAdmin)


class IngredientInline(admin.TabularInline):
    model = food.Ingredient
    extra = 5


class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'teaser', 'attributes', 'categories', 'rclass', 'pub_date')}),
        ('directions, description, credit', {'fields' : ('directions', 'description', 'credit')}),
    )
    list_filter = ['rclass']
    inlines = [
        IngredientInline,
    ]

admin.site.register(food.Recipe, RecipeAdmin)


class FoodstuffInline(generic.GenericTabularInline):
    model = food.Foodstuff
    user = generic.GenericForeignKey(settings.AUTH_USER_MODEL)


class IngredientAdmin(admin.ModelAdmin):
    inlines = [
        FoodstuffInline,
    ]
    
admin.site.register(food.Ingredient, IngredientAdmin)

admin.site.register(food.Link)
