from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from django.core.urlresolvers import reverse
from fc3.miniblog.models import Post

class RssSiteNewsFeed(Feed):
    title = "CracklyFinger.com"
    link = reverse('miniblog-archive')
    description = "Updates on changes and additions to cracklyfinger.com, plus occasional random comments"

    def items(self):
        return Post.objects.order_by('-pub_date')[:5]

class AtomSiteNewsFeed(RssSiteNewsFeed):
    feed_type = Atom1Feed
    subtitle = RssSiteNewsFeed.description

