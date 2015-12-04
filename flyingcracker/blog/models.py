from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(help_text='Automatically built from the title.')
    teaser = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Date this post will get published')
    body = models.TextField()
    enable_comments = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/blog/%s/%s/" % (self.pub_date.strftime("%Y/%m/%d").lower(),
                                 self.slug)

    class Meta:
        get_latest_by = 'pub_date'
        ordering = ('-pub_date',)

    def unused(self):
        js = (
            # Utility dependencies
            '/static/js/yui/yahoo-debug.js',
            'http://yui.yahooapis.com/2.3.1/build/yahoo-dom-event/yahoo-dom-event.js',
            'http://yui.yahooapis.com/2.3.1/build/dragdrop/dragdrop-min.js',
            '/static/js/yui/element-debug.js',
            # Needed for Menus, Buttons and Overlays used in the RTE Toolbar
            '/static/js/yui/container_core-debug.js',
            '/static/js/yui/menu-debug.js',
            '/static/js/yui/button-debug.js',
            # Source file for Rich Text Editor
            '/static/js/yui/editor-min.js',
        )
