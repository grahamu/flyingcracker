from __future__ import with_statement

def prod():
    env.ENV = 'production'

def staging():
    env.ENV = 'staging'

def launch():
    local('ansible-playbook {0}.yml'
          ' -i hosts'
          ' -vv'.format(env.ENV)
          )
