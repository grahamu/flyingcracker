from django.conf import settings

def theme_settings(request):
    """
    Make theme settings available to all templates.
    """
    return {
        'theme_version': '1.0.0',
        'tailwind_css': True,
        'debug': settings.DEBUG,
    }