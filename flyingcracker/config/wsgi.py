"""
WSGI config for fc3staging project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import os, sys
import django
django.setup()
from django.core.wsgi import get_wsgi_application

sys.path.append('/home/graham/webapps/fc3staging/src/fc3')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fc3.settings.staging")
application = get_wsgi_application()

