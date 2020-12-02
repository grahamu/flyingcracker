from django.conf import settings


def media_url(request):
    return {'media_url': settings.MEDIA_URL}


def yui_version(request):
    yui = {}
    yui['yui_root'] = 'http://yui.yahooapis.com/'
    yui['yui_version'] = settings.YUI_VERSION
    try:
        yui['yui_path'] = settings.YUI_PATH
    except AttributeError:
        yui['yui_path'] = yui['yui_root'] + settings.YUI_VERSION
    return yui


def miniblog(request):

    # from miniblog.models import Post
    # posts = Post.objects.all().order_by('-pub_date')[0:7]
    return {'miniblog': None}


def system_version(request):
    from django import get_version
    from django.conf import settings

    from fc3 import get_git_tag

    system = {}
    system['system_name'] = settings.SYSTEM_NAME
    system['system_version'] = get_git_tag()
    system['django_version'] = get_version()
    return system
