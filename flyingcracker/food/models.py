from django.db import models
from django.db.models import permalink
from datetime import date


class Foodstuff(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField()
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return ('food-ingredient-detail', [self.slug])
    get_absolute_url = permalink(get_absolute_url)
    
    class Meta:
        ordering = ['title']
    

class Attribute(models.Model):
    title = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ['title']


class Category(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
        verbose_name_plural = "categories"
    
    
class Recipe(models.Model):
    title = models.CharField(max_length=50, unique=True, db_index=True)
    slug = models.SlugField()
    pub_date = models.DateField('date published', null=True, default=date.today)
    directions = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    teaser = models.CharField(max_length=100, blank=True, null=True)
    credit = models.TextField(blank=True, null=True)
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
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return ('food-recipe-detail', [self.slug])
    get_absolute_url = permalink(get_absolute_url)
    
    class Meta:
        ordering = ['title']


class Ingredient(models.Model):
    foodstuff = models.ForeignKey(Foodstuff, related_name="ingredients")
    recipe = models.ForeignKey(Recipe, related_name="ingredients")
    quantity = models.CharField(max_length=20, blank=True, null=True)
    modifier = models.CharField(max_length=50, blank=True, null=True)
    rank = models.IntegerField()
    
    def __unicode__(self):
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
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ['rank']
