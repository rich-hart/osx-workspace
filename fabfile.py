
from fabric.operations import run, put, sudo
from fabric.context_managers import lcd, path, cd
from fabric.api import local, env, task

#DEPLOY_DIR='/opt'
env.DEPLOY_DIR = '/opt'
env.rcfile="./.fabricrc"
env.BRANCH="remote_install"
#env.REMOTE='karenc'
env.REMOTE="rich-hart"
env.WORKSPACE="/Users/openstax/workspace"
env.use_sudo=True
#env.hosts = ['virtual_machine']
#env.hosts = ['localhost']
env.host_string = 'virtual_machine'
env.use_ssh_config = True
env.ssh_config_path = '.ssh_config'
#env.host = 'virtual_machine'

@task
def test():
    pass

@task
def temp():
    from .openstaxsetup.fabfile import temp
    print("root")
    #temp()
#    deploy()

@task
def load_script(n=0):
    with cd(env.DEPLOY_DIR):
        put("/Users/openstax/workspace/cnx-vagrant/bootstrap_{}.sh".format(n),"boostrap_{}.sh".format(n), use_sudo=True)
        sudo("chmod 755 boostrap_{}.sh".format(n))
        sudo("./boostrap_{}.sh".format(n))
#@task
#def temp():
#    pass
@task
def generate_key():
    with lcd("cnx-vagrant"):
        local("vagrant ssh-config --host virtual_machine > {WORKSPACE}/.ssh_config".format(**env))
@task
def create_vm():
    # create vm
    with lcd("cnx-vagrant"):
        local("vagrant up")
        local("vagrant ssh-config --host virtual_machine > {WORKSPACE}/.ssh_config".format(**env))

def _destroy_vm():
    with lcd("cnx-vagrant"):
        local("vagrant destroy")

def _clone_repos():
    local("git clone -b {BRANCH} --single-branch https://github.com/{REMOTE}/cnx-vagrant.git".format(**env))
    local("git clone -b {BRANCH} --single-branch https://github.com/{REMOTE}/cnx-setup.git".format(**env))
    local("git clone -b {BRANCH} --single-branch https://github.com/{REMOTE}/openstax-setup.git".format(**env))


def _rm_repos():
    local("rm -rf cnx-vagrant")
    local("rm -rf cnx-setup")
    local("rm -rf openstax-setup")

@task
def save(message = "update"):
    with lcd("cnx-vagrant"):
        local("git add -u")
        local("git commit -m {}".format(message))
    with lcd("cnx-setup"):
        local("git add -u")
        local("git commit -m {}".format(message))
    with lcd("openstax-setup"):
        local("git add -u")
        local("git commit -m {}".format(message))

@task
def upload():
    with lcd("cnx-vagrant"):
        local("git push")
    with lcd("cnx-setup"):
        local("git push")
    with lcd("openstax-setup"):
        local("git push")

@task
def destroy():
    _destroy_vm()
    _rm_repos()

#@task
def create():
    _clone_repos()
    create_vm()




def install_openstax():
    #with lcd("openstax-setup"):
    #import sys
    #sys.path.append("/Users/openstax/workspace/openstax-setup")
    #accounts_setup = __import__("openstax-setup.fabfile.accounts_setup")
    import ipdb; ipdb.set_trace()
    import sys
    sys.path.append("/Users/openstax/workspace/openstax-setup/fabfile.py") 
    #from openstaxsetup.fabfile import *
    #accounts_setup = imp.load_source('accounts_setup', '/Users/openstax/workspace/openstax-setup/fabfile.py')
    accounts_setup(https=True)

def dummy():
    #from openstaxsetup.fabfile import * #accounts_setup
    import ipdb; ipdb.set_trace()    
    #with lcd("openstax-setup"):
    env.pwd = local("pwd",capture=True)
    #local("source ./venv/bin/activate")
    run("{pwd}/venv/bin/fab "
          "-H {host_string} "
          "--forward-agent "
          "--abort-on-prompts "
          "-f {pwd}/openstax-setup/fabfile.py "
          "--ssh-config-path={pwd}/.ssh_config "
          "accounts_setup:https=True".format(**env),
          )
#    run(
"""
# Set up facebook and twitter app id and secret
cat >{DEPLOY_DIR}/accounts/config/secret_settings.yml <<EOF
secret_token: 'Hu7aghaiaiPai2ewAix8OoquNoa1cah4'

smtp_settings:
  address: 'localhost'
  port: 25

# Facebook OAuth API settings
facebook_app_id: '114585082701'
facebook_app_secret: '35b6df2c95b8e3bc7bcd46ce47b1ae02'

# Twitter OAuth API settings
twitter_consumer_key: 'wsSnMNS15nbJRDTqDCDc9IxVs'
twitter_consumer_secret: '78OkKbqZbVSGOZcW7Uv6XyTJWKITepl4TeR7rawjkAsBR5pgZ8'

# Google OAuth API settings
google_client_id: '860946374358-7fvpoadjfpgr2c3d61gca4neatsuhb6a.apps.googleusercontent.com'
google_client_secret: '7gr2AYXrs1GneoVm4mKjG98N'
EOF
"""
#""".format(**env))
   
def install_cnx():
    with lcd("cnx-setup"):
        pass
    

def install_programs():
    pass


def link_programs():
    pass

def test_programs():
    pass

def run_programs():
    pass


