# Fabric configuration file for automated deployment
from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import comment, uncomment, contains, exists, append, sed
import aws

GIT_ORIGIN = 'git@github.com' # git@github.com
GIT_ACCOUNT = 'tygerllc'
GIT_PROJECT = 'tygerapi' # Django Project
GIT_REPO = GIT_ACCOUNT + "/" + GIT_PROJECT + ".git"
GIT_API_TOKEN = '' # get from github

# The AWS Key Pair
AWS_KEY = '/Users/me/Dropbox/Tyger/keypairs/tygerdev.pem'
RSA_LOCATION = '~/.ssh/' # The deploy id_rsa and id_rsa.pub location
CODE_DIR = '/home/ec2-user/tygerapi/'

env.hosts = ['tyger.us']

# import creds from non version controlled file
# try:
#     from creds import *
# except ImportError:
#    pass

# These are the packages we need to install using yum
INSTALL_PACKAGES = [
    "mysql-server", "mysql", "mysql-libs",
    "python-setuptools", "python-devel",
    "php", "libmcrypt", "libmcrypt-devel", "php-mcrypt", "php-mbstring",
    "git", "mercurial", "gcc", "nginx", "MySQL-python"
           ]

#### Environments
def dev():
    "Setup dev settings"
#    env.node = aws.provision_with_boto('dev')
    env.hosts = ['ec2-user@ec2-107-21-120-73.compute-1.amazonaws.com']
    env.repo = ("tygerapi", "origin", "master")
    env.base = "~"
    env.virtualenv, env.parent, env.branch = env.repo
    env.user = "ec2-user"
    env.git_origin = GIT_ORIGIN
    env.git_repo = GIT_REPO
    env.dev_mode = True
    env.key_filename = AWS_KEY
    env.DBname = 'tyger'
    env.mysqluser = 'root'
    env.mysqlpassword = 'tygerdb'
    env.mysqlhost = '127.0.0.1'

#def production():
#    "Setup production settings"
#    env.node = aws.provision_with_boto('prodtyger')
#    env.hosts = [env.node.hostname]
#
#    env.repo = ("env.example.com", "origin", "release")
#    env.virtualenv, env.parent, env.branch = env.repo
#    env.base = "/server"
#    env.user = "ec2-user"
#    env.git_origin = GIT_ORIGIN
#    env.git_repo = GIT_REPO
#    env.dev_mode = False
#    env.key_filename = AWS_KEY
#### End Environments

#### Cutting releases
#def cut_staging():
#    "Cuts the staging branch"
#    local("git checkout stage; git merge master; git push; git checkout master;")

#def cut_release():
#    "Cuts the release branch"
#    local("git checkout release; git merge stage; git push; git checkout master;")

#### End Release

#### Host Bootstrapping

def bootstrap():
    "Bootstraps the AWS environment"
    require('hosts', provided_by=[dev])
#    sub_stop_processes() # Stop everything
    sub_install_packages() # Get the installed packages
    sub_build_packages()   # Configure nginx & gunicorn
#    sub_get_virtualenv()   # Download virtualenv
#    sub_make_virtualenv()  # Build the virtualenv
    sub_setup_ssh()        # Copy the SSH keys over
    sub_git_clone()        # Checkout the repo
    sub_get_requirements() # Get the requirements (pip install)
#    sub_get_admin_media()  # Copy Django admin media over
    config_MySQL()   # Configure MySQL and setup users
    sub_build_tyger() # Copy DB & syncdb
    sub_start_processes()  # Start everything

def sub_install_packages():
    "Installs necessary packages on host"
    sudo("yum -y update")
    package_str = " ".join(INSTALL_PACKAGES)
    sudo("yum -y install "+package_str)

def sub_build_packages():
    "Configure nginx, gunicorn, django"
    sub_config_gunicorn()
    sub_config_nginx()
    sub_config_django()

def sub_config_gunicorn():
    "Install  gunicorn"
    sudo("easy_install gunicorn")

def sub_config_nginx():
    # "Configure NginX"
    put("config/nginx.conf","/etc/nginx/nginx.conf",use_sudo=True)
    sudo("cd /etc/nginx; mkdir -p sites-available sites-disabled sites-enabled")
    put("config/tyger.us", "/etc/nginx/sites-available/tygerus.conf",use_sudo=True)
    sudo("chmod -R 755 /home/ec2-user/; ")
    sudo("ln -f -s /etc/nginx/sites-available/tygerus.conf /etc/nginx/sites-enabled/tygerus.conf")

def sub_config_django():
    # "Install & configure django"
    sudo("wget http://www.djangoproject.com/download/1.3/tarball/")
    sudo("tar xzvf Django-1.3.tar.gz")
    sudo("cd ./Django-1.3; python setup.py install")

#def sub_get_virtualenv():
#    "Fetches the virtualenv package"
#    run("if [ ! -e virtualenv-1.6.1.tar.gz ]; then wget http://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.6.1.tar.gz; fi")
#    run("if [ ! -d virtualenv-1.6.1 ]; then tar xzf virtualenv-1.6.1.tar.gz; fi")
#    run("rm -f virtualenv")
#    run("ln -s virtualenv-1.6.1 virtualenv")

#def sub_make_virtualenv():
#    "Makes the virtualenv"
#    sudo("if [ ! -d %(base)s ]; then mkdir -p %(base)s; chmod 777 %(base)s; fi" % env)
#    run("if [ ! -d %(base)s/%(virtualenv)s ]; then python ~/virtualenv/virtualenv.py --no-site-packages %(base)s/%(virtualenv)s; fi" % env)
#    sudo("chmod 777 %(base)s/%(virtualenv)s" % env)

def sub_setup_ssh():
    """
    Copy ssh id_rsa and id_rsa.pub keys if they do not exist and add to github as a deploy key
    """
    # create the deploy host .ssh folder
    run("mkdir -p ~/.ssh/")

    # put the ssh keys on the deploy host
    put('config/deploy_key', '~/.ssh/id_rsa', mode=0600)
    put('config/deploy_key.pub', '~/.ssh/id_rsa.pub', mode=0600)
    # put a preset known_hosts file on the deploy host to make it aware of github for deploys
    put("config/known_hosts", "/home/%(user)s/.ssh/known_hosts" % env, mode=0600)

def sub_git_clone():
    "Clones a repository into the virtualenv at /tygerapi"
    run("cd %(base)s/%(virtualenv)s; git clone %(git_origin)s:%(git_repo)s tygerapi; cd tygerapi; git checkout %(branch)s; git pull %(parent)s %(branch)s" % env)

def sub_get_requirements():
    "Gets the requirements for the project"
    sudo("cd /home/ec2-user/; easy_install django-tagging django-profiles South PIL" % env)
    sudo("cd /home/ec2-user/; hg clone https://bitbucket.org/jespern/django-piston" % env)
    sudo("cd /home/ec2-user/django-piston/; python setup.py install" % env)
    # UPDATE PYTHONPATH
    # PYTHONPATH=${PYTHONPATH}:/home/ec2-user/tyger/lib/python
    # export PYTHONPATH

def sub_get_admin_media():
    "Copies over the required admin media files"
    run("cd %(base)s/%(virtualenv)s/project/public/media; if [ ! -d admin-media ]; then cp -R %(base)s/%(virtualenv)s/lib/python2.6/site-packages/django/contrib/admin/media admin-media; fi" % env)

def sub_build_tyger():
    "Copy DB to tyger db, syncdb, South migration"
    syncdb()
    put("config/tygerdb_backup", "/home/%(user)s/tygerapi/tygerdb.backup" % env)
    sudo("mysql -p -u root tyger < /home/%(user)s/tygerapi/tygerdb.backup" % env)
    # Symlink to django's static admin files
    sudo("ln -s /home/ec2-user/Django-1.3/django/contrib/admin/media/ /home/%(user)s/tygerapi/static/admin" % env)
    # Copy uploaded media to server
    sudo("mkdir -p /home/%(user)s/tygerapi/media/uploads" % env)
    put("media/uploads", "/home/%(user)s/tygerapi/media/" % env, use_sudo=True)

def sub_start_processes():
    "Starts NginX and gUnicorn"
    sudo("nohup nginx")
    sudo("nohup gunicorn_django --workers=2 &")
    sudo("service mysqld start")

def sub_stop_processes():
    "Stops Nginx and gUnicorn"
    with settings(warn_only=True):
        sudo("nginx -s stop")
        sudo("stop gunicorn_django")
        sudo("service mysqld stop")

#### End Host Bootstrapping

#### Deploying new version

def test():
    with settings(warn_only=True):
        result = local('./manage.py test tygerapi', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

def commit():
    local("git add -p && git commit")

def push():
    local("git push")

def prepare_deploy():
    test()
    commit()
    push()

def syncdb():
    "Does a synbdb and a migrate"
    require('hosts', provided_by=[dev])
    run("cd ~/tygerapi; python manage.py syncdb --noinput; python manage.py migrate --noinput;" % env)
    sudo("cd /home/ec2-user/tygerapi; python manage.py collectstatic")

def pull():
    "Does a git pull on all the repositories"
    require('hosts', provided_by=[dev])
    run("cd %(base)s/%(virtualenv)s; git pull %(parent)s %(branch)s" % env)

def deploy():
    pull()
    syncdb()
    reload()

#### End Deploy new version

#### Reloading Python files

def reload():
    "Forces gunicorn/nginx to reload the project"
    require('hosts', provided_by=[dev])
    sudo("killall -HUP gunicorn_django")
    sudo("killall -HUP nginx")
    #TODO: Add mysql
##### End Reloading Python Files

##### Version roll back

def rollback(hash):
    """
    Rollback git repositories to specified hash.
    Usage:
    fab rollback:hash=etcetc123
    """
    require('hosts', provided_by=[dev, staging, production])
    env.hash = hash
    run("cd %(base)s/%(virtualenv)s/project; git reset --hard %(hash)s" % env)

#### End Version roll back

#### Boto AWS EC2 Cleanup

def cleanup(node_name = None):
    config = aws.read_config()
    if node_name:
        if config.has_section(node_name):
            aws.terminate_instance(node_name)
    else:
        for section in config.sections():
            aws.terminate_instance(section)

def destroy():
    aws.terminate_all_instances()

#### End Boto AWS EC2 Cleanup

#### Configure MySQL

def config_MySQL():
    """
    """
    # Reset root password & start MySQL
    sudo("service mysqld start")
    sudo("chkconfig --levels 235 mysqld on")
    sudo("mysql_secure_installation")
    run("mysql -u root -p -e 'CREATE DATABASE %s;'" % env.DBname)
    run("mysql -u root -p")

    # Create tygerdb user manually
    # CREATE user 'tygerdb'@'%' identified by 'tygerdb';
    # GRANT ALL ON tyger.* to 'tygerdb'@'%';
    # FLUSH PRIVILEGES;
    # TODO: Automate this
    
#### End Configure MySQL