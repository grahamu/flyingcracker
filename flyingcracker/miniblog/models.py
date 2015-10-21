from django.db import models
from django.template.defaultfilters import truncatewords_html
from datetime import datetime

#class Blog(models.Model):
#    title = models.CharField(max_length=50, index=True)
#    slug = models.SlugField()
#    associated_with = generic relation
#    image = image
    
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
        return ('miniblog-detail', [self.pub_date.year, self.pub_date.strftime("%b").lower(), self.pub_date.day, self.slug])
    get_absolute_url = models.permalink(get_absolute_url)

    class Meta:
        get_latest_by = 'pub_date'
        ordering = ('-pub_date',)
