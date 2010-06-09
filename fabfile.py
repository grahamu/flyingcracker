from __future__ import with_statement
from fabric.api import *

# globals


# environments
def localhost():
    env.hosts = ['localhost']
    env.user = 'grahamullrich'
    
def prod():
    """Use the production webserver"""
    env.project_name = 'fc3'
    env.hosts = ['graham.webfactional.com']
    env.user = 'graham'
    env.remote_app_dir = '/home2/%(user)s/webapps/django/%(project_name)s' % env
    env.remote_apache_dir = '/home2/%(user)s/webapps/django/apache2' % env
    env.remote_lib_dir = '/home2/%(user)s/lib' % env
    env.hg_libs = []
    env.git_libs = ['django-mailer-2', 'django-notification']

def deploy():
    require('hosts', provided_by = ['localhost',])
    """Deploy the site."""
    update()
    migrate()
    restart()

def update():
    run("cd %(remote_app_dir)s; hg pull; hg update" % env)
    for app in env.hg_libs:
        cmd = "cd %(remote_lib_dir)s/" % env
        cmd += "%s; hg pull; hg update" % app
        run(cmd)
    for app in env.git_libs:
        cmd = "cd %(remote_lib_dir)s/" % env
        cmd += "%s; git pull" % app
        run(cmd)
    
def migrate():
    run("cd %(remote_app_dir)s; python2.5 manage.py syncdb" % env)
    run("cd %(remote_app_dir)s; python2.5 manage.py migrate" % env)
    
def restart():
    run("%(remote_apache_dir)s/bin/stop; sleep 1; %(remote_apache_dir)s/bin/start" % env)
    
def debugon():
    """Turn debug mode on for the production server."""
    run("cd %(remote_app_dir)s; sed -i -e 's/DEBUG = .*/DEBUG = True/' settings_local.py" % env)
    restart()

def debugoff():
    """Turn debug mode off for the production server."""
    run("cd %(remote_app_dir)s; sed -i -e 's/DEBUG = .*/DEBUG = False/' settings_local.py" % env)
    restart()
