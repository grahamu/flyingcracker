from datetime import date

from django.db import models
from django.urls import reverse


class Foodstuff(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('food:ingredient-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['title']


class Attribute(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Category(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name_plural = "categories"


class Recipe(models.Model):
    title = models.CharField(max_length=50, unique=True, db_index=True)
    slug = models.SlugField()
    pub_date = models.DateField('date published', null=True, default=date.today)
    directions = models.TextField(blank=True)
    description = models.TextField(blank=True)
    teaser = models.CharField(max_length=100, blank=True)
    credit = models.TextField(blank=True)
    attributes = models.ManyToManyField(Attribute)
    categories = models.ManyToManyField(Category)
    DRINK_CLASS = 'D'
    EAT_CLASS = 'E'
    INGREDIENT_CLASS = 'I'
    CLASS_CHOICES = (
        (DRINK_CLASS, 'Drink'),
        (EAT_CLASS, 'Eat'),
        (INGREDIENT_CLASS, 'Ingredient'),
    )
    rclass = models.CharField(max_length=1, choices=CLASS_CHOICES, default=DRINK_CLASS, blank=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.rclass == self.DRINK_CLASS:
            recipe_type = 'drink'
        else:
            recipe_type = 'food'
        return reverse('food:recipe-detail', kwargs={'slug': self.slug, 'recipe_type': recipe_type})

    class Meta:
        ordering = ['title']


class Ingredient(models.Model):
    foodstuff = models.ForeignKey(Foodstuff, related_name="ingredients", on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name="ingredients", on_delete=models.CASCADE)
    quantity = models.CharField(max_length=20, blank=True)
    modifier = models.CharField(max_length=50, blank=True)
    rank = models.IntegerField()

    def __str__(self):
        return self.foodstuff.title

    def _get_title(self):
        return self.foodstuff.title

    title = property(_get_title)

    def _get_slug(self):
        return self.foodstuff.slug

    slug = property(_get_slug)

    class Meta:
        ordering = ['rank']
        verbose_name = "recipe ingredient"
        verbose_name_plural = "recipe ingredients"


class Link(models.Model):
    title = models.CharField(max_length=50, unique=True)
    url = models.CharField(max_length=250)
    rank = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['rank']
