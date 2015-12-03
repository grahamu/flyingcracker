from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User


class Doneness(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField()
    doneness = models.IntegerField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['doneness']
        verbose_name_plural = 'Donenesses'

    def get_absolute_url(self):
        return ('grill-doneness-detail', [self.slug])
    get_absolute_url = permalink(get_absolute_url)

    def __unicode__(self):
        return self.title

    def less(self):
        try:
            obj = Doneness.objects.get(doneness=self.doneness - 1)
        except Doneness.DoesNotExist:
            obj = None
        return obj

    def more(self):
        try:
            obj = Doneness.objects.get(doneness=self.doneness + 1)
        except Doneness.DoesNotExist:
            obj = None
        return obj


class Method(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()

    def __unicode__(self):
        return self.title


class Food(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.title


class Hardware(models.Model):
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.make + ' ' + self.model


class Cut(models.Model):
    title = models.CharField(max_length=40)

    def __unicode__(self):
        return self.title


class Grilling(models.Model):
    user = models.ManyToManyField(User)
    doneness = models.ForeignKey(Doneness, on_delete=models.CASCADE)
    method = models.ForeignKey(Method, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    hardware = models.ForeignKey(Hardware, blank=True, null=True,
                                 on_delete=models.CASCADE)
    cut = models.ForeignKey(Cut, blank=True, null=True,
                            on_delete=models.CASCADE)
    details = models.CharField(max_length=100)

    def __unicode__(self):
        return ' : '.join([str(self.food),
                           str(self.cut),
                           str(self.doneness)]) + \
               ' - ' + ' : '.join([str(self.hardware),
                                   str(self.method),
                                   self.details])
