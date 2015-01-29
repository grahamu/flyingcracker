from __future__ import with_statement
import contextlib
from fabric.api import env, run, cd, sudo, put, require, settings, hide, puts
from fabric.contrib import project, files

# globals
staging_server = 'graham.webfactional.com'
server_owner = 'graham'
local_user = 'johnevans'
user = 'jake'
branch_name = 'master'
prompts = []
prompts += expect("Enter passphrase for key '/home2/jake/.ssh/id_rsa': ", "factionknockout")

# environments
def localhost():
    env.hosts = ['localhost']
    env.user = local_user
    
def run_local_server():
    """ Runs local development Django server """
    local("python manage.py runserver --settings=fc3.settings.dev%(user)s" %env)

def provision_local():
    local("pip install requirements/local.txt")

def provision_staging():
    run("cd %(remote_app_dir)s; pip install requirements/staging.txt")

def provision_production():
    run("cd %(remote_app_dir)s; pip install requirements/production.txt")

def staging():
    """get info"""
    env.user = prompt("what is your user name as in: <user>@example.webfactional.com?")
    """use staging server"""
    env.project_name = 'fc3staging'
    env.hosts = ['%(user)s@%s.webfactional.com' % (env, server_owner)]
    env.remote_app_dir = '/home/%s/.virtualenvs/%(project_name)s' % (server_owner, env)
    env.remote_apache_dir = '/home/%s/webapps/%(project_name)s/apache2' % (server_owner, env)
    env.remote_lib_dir = '/home/%s/.vertualenvs/%(project_name)s/lib' % (server_owner, env)
    env.git_libs = ['django-mailer-2', 'django-notification']
    branch_name = "staging"

def prod():
    """Use the production webserver"""
    env.project_name = 'fc3'
    env.hosts = ['%s@graham.webfactional.com' %(env.user)]
    env.user = 'graham'
    env.remote_app_dir = '/home/%(user)s/webapps/django/%(project_name)s' % env
    env.remote_apache_dir = '/home2/%(user)s/webapps/django/apache2' % env
    env.remote_lib_dir = '/home2/%(user)s/lib' % env
    env.git_libs = ['django-mailer-2', 'django-notification']
    branch_name = "master"

def setup():
    """Start with a webfaction server setup up with basic shells of apps (one main app, one static)
        This script builds out the rest of the site
        this script also assumes you've set up ssh and you've added the server's ssh to github
        also, please set up the ssh with no password, otherwise this script wont work
    """
    run("easy_install-2.7 pip")
    run("pip install virtualenv; pip install virtualenvwrapper")
    run("mkvirtualenv fc3staging")
    run("workon fc3staging; cdvirtualenv")
    run("pip install -e git+ssh://git@github.com/grahamu/flyingcracker.git#egg=fc3")
    run("cd src/fc3")
    run("git pull origin staging")

    """copy secrets.json files, and static files (eventually) into fc3/settings"""
    put("fc3/settings/secrets.json","%(remote_app_dir)s/src/fc3/fc3/settings" % env)

    """need something to sync fc3.dump to the pstgres db"""

    run("python manage.py collectstatic --noinput")

def deploy():
    require('hosts', provided_by = ['localhost',])
    run("%(remote_apache_dir)s/bin/stop;" % env)
    """Deploy the site."""
    run("cd %(remote_app_dir)s/src/fc3" % env)
    run('git fetch --all; git reset --hard origin/%s' % branch_name)
    put("fc3/settings/secrets.json","%(remote_app_dir)s/src/fc3/fc3/settings" % env)
    run("%(remote_apache_dir)s/bin/start" % env)

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
