from django.conf import settings


def media_url(request):
    return {"media_url": settings.MEDIA_URL}


def system_version(request):
    from django import get_version
    from django.conf import settings

    from fc3 import get_git_tag

    system = {}
    system["system_name"] = settings.SYSTEM_NAME
    system["system_version"] = get_git_tag()
    system["django_version"] = get_version()
    return system
