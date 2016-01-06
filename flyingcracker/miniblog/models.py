from datetime import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import truncatewords_html


class Post(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    body = models.TextField()
    pub_date = models.DateTimeField(default=datetime.now) # , index=True)
    # new fields:
    # up_date = models.DateTimeField(auto_now=True)
    # author = models.ForeignKey(User, related_name='posts')
    # blog = models.ForeignKey(MiniBlog)

    def __unicode__(self):
        return str(self.pub_date) + ' -  "' + truncatewords_html(self.body, 10) + '"'

    def teaser(self):
        return truncatewords_html(self.body, 10)
    teaser = teaser

    def get_absolute_url(self):
        return reverse('miniblog:detail', args=[
            self.pub_date.year,
            self.pub_date.strftime("%b").lower(),
            self.pub_date.day,
            self.slug])

    class Meta:
        get_latest_by = 'pub_date'
        ordering = ('-pub_date',)
