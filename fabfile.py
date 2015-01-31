from __future__ import with_statement

from fabric.api import *
from contextlib import contextmanager as _contextmanager
from fabric.contrib import project, files

"""if this comment shows up in the server, then the deploy function works"""

# globals
staging_server = 'graham.webfactional.com'
local_user = 'johnevans'
user = 'jake'
branch_name = 'master'

# environments
def localhost():
    env.hosts = ['localhost']
    env.user = local_user
    
def run_local_server():
    """ Runs local development Django server """
    local("python manage.py runserver --settings=fc3.settings.dev%(user)s" %env)

def provision_local():
    local("pip install -U -r requirements/local.txt")

def provision():
    with virtualenv():
        run("pip install -U -r requirements/%(settings_name)s.txt" % env)

def staging():
    """get info"""
    env.user = prompt("what is your user name as in <user>@example.webfactional.com?:")
    """use staging server"""
    env.project_name = 'fc3staging'
    env.settings_name = 'staging'
    env.hosts = ['%(user)s@graham.webfactional.com' % (env)]
    env.remote_app_dir = '/home/graham/webapps/%(project_name)s' % (env)
    env.remote_apache_dir = '/home/graham/webapps/%(project_name)s/apache2' % (env)
    env.remote_lib_dir = '/home/graham/webapps/%(project_name)s/lib' % (env)
    env.git_libs = ['django-mailer-2', 'django-notification']
    env.activate = 'source /home/graham/webapps/%(project_name)s/bin/activate' % (env)
    env.branch_name = "staging"

def prod():
    """get info"""
    env.user = prompt("what is your user name as in <user>@example.webfactional.com?:")
    """Use the production webserver"""
    env.project_name = 'fc3'
    env.settings_name = 'prod'
    env.remote_app_dir = '/home/graham/webapps/%(project_name)s' % (env)
    env.remote_apache_dir = '/home/graham/webapps/%(project_name)s/apache2' % (env)
    env.remote_lib_dir = '/home/graham/webapps/%(project_name)s/lib' % (env)
    env.git_libs = ['django-mailer-2', 'django-notification']
    env.activate = 'source /home/graham/webapps/%(project_name)s/bin/activate' % (env)
    env.branch_name = "master"

def setup():
    """Start with a webfaction server setup up with basic shells of apps (one main app, one static)
        This script builds out the rest of the site
        this script also assumes you've set up ssh and you've added the server's ssh to github
        also, please set up the ssh with no password, otherwise this script wont work
    """
    run("easy_install-2.7 pip")
    run("pip install virtualenv")
    run("pip install -e git+ssh://git@github.com/grahamu/flyingcracker.git#egg=fc3")
    run("cd src/fc3")
    run("git pull origin %(branch_name)s" % env) 

    """copy secrets.py files, and static files (eventually) into fc3/settings"""
    put("fc3/settings/secrets.py","%(remote_app_dir)s/src/fc3/fc3/settings" % env)

    """need something to sync fc3.dump to the pstgres db"""

    run("python manage.py collectstatic --noinput")
    run("pip install -U -r requirements/staging.txt")

@_contextmanager
def virtualenv():
    with cd(env.remote_app_dir+"/src/fc3"):
        with prefix(env.activate):
            yield

def deploy():
    """Deploy the site."""
    with virtualenv():
        run('git fetch --all; git reset --hard origin/%(branch_name)s' % env)
        put("fc3/settings/secrets.py","%(remote_app_dir)s/src/fc3/fc3/settings" % env)
        provision()
        run("python manage.py collectstatic --settings=fc3.settings.%(settings_name)s" % env)
    run("%(remote_apache_dir)s/bin/restart" % env)

def update():
    run("cd %(remote_app_dir)s; git pull origin master" % env)
    
def migrate():
    run("cd %(remote_app_dir)s; python2.7 manage.py syncdb" % env)
    run("cd %(remote_app_dir)s; python2.7 manage.py migrate" % env)
    
def restart():
    run("%(remote_apache_dir)s/bin/stop; sleep 1; %(remote_apache_dir)s/bin/start" % env)
    
def debugon():
    """Turn debug mode on for the production server."""
    run("cd %(remote_app_dir)s; sed -i -e 's/DEBUG = .*/DEBUG = True/' fc3/settings/prod.py" % env)
    restart()

def debugoff():
    """Turn debug mode off for the production server."""
    run("cd %(remote_app_dir)s; sed -i -e 's/DEBUG = .*/DEBUG = False/' fc3/settings/prod.py" % env)
    restart()
