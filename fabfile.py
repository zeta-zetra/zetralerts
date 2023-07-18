"""
Automate deployments, rollbacks and updates 

Author: Zetra
Date  : 2023-07-17
"""

from dotenv import load_dotenv
from fabric import Connection, task
from invoke import Responder
from os import environ, path, getcwd


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


# Get the environment variables
PEM_KEY_DIR      = environ.get("PEM_KEY_DIR")
PEM_KEY          = environ.get("PEM_KEY")
HOST_NAME        = environ.get("HOST_NAME")
ROOT_USERNAME    = environ.get("HOST_USERNAME")
USER_NAME        = environ.get("USERNAME")
GIT_ZETRALERT_URL = environ.get("GIT_ZETRALERT_URL")

print(path.join(PEM_KEY_DIR,PEM_KEY))


def _create_zetralert_user():
    """
    Create a user called zetralert. This user will be used to SSH as opposed to Admin
    """
    with Connection(
        HOST_NAME,
        user=ROOT_USERNAME,
        connect_kwargs={"key_filename": path.join(PEM_KEY_DIR, PEM_KEY)}
    ) as c:

        """
        Create the zetralert user
        """

        c.sudo("mkdir -p /var/zetralert/.ssh", user='zetralert')

        c.sudo("chmod 700 /var/zetralert/.ssh",user='zetralert')

        c.sudo("touch /var/zetralert/.ssh/authorized_keys", user='zetralert')

        c.sudo("chmod 600 /var/zetralert/.ssh/authorized_keys", user="zetralert")

        print("Copying the keys")
        c.run("sudo cp .ssh/authorized_keys /var/zetralert/.ssh/authorized_keys")

        print("==== zetralert User has been setup =====")   
        
        
def _setup_new_instance():
    
    """ 
    Setup the server for the application  
    
    Run updates
    Install Python
    Create the new user
    
    """
    with Connection(
        HOST_NAME,
        user=ROOT_USERNAME,
        connect_kwargs={"key_filename": path.join(PEM_KEY_DIR, PEM_KEY)}
    ) as c:
        
        print("===== STARTING SETUP ========")
        # Run updates
        c.run("sudo apt update -y")
        
        """
        Create the zetralert user
        """
        del_user = c.run("sudo userdel -r zetralert")
        c.run("sudo adduser zetralert --disabled-password --home /var/zetralert --gecos ''")
        _create_zetralert_user()
        
        
        # Install packages
        c.run("sudo apt-get install git build-essential wget python3-dev python3-venv python3  python3-pip libxml2-dev libxslt1-dev libffi-dev zlib1g-dev libssl-dev gettext libpq-dev libmariadb-dev libjpeg-dev libopenjp2-7-dev -y")

        """
        Install Python3.7
        """
        c.run("sudo apt install software-properties-common -y")
        c.run("sudo add-apt-repository ppa:deadsnakes/ppa -y")

        c.run("sudo apt install python3.7 -y")
        c.run("sudo apt-get install python3.7-venv")
        
        print("==== SETUP COMPLETE =====")  
        
        
def _deploy_new_zetralert_instance():
    """ Deploy new instance from Git """
    
    with Connection(
        HOST_NAME,
        user=ROOT_USERNAME,
        connect_kwargs={"key_filename": path.join(PEM_KEY_DIR, PEM_KEY)}
    ) as c:
        
        # Make the virtual env directory
        c.sudo("mkdir -p '/var/zetralert/venvs/' && exit", user='zetralert')
        c.sudo("chmod -R 777 /var/zetralert/venvs/", user='zetralert') 
        
        # Get the latest stable version of Vibin-Pretix
        print("Clone the Zetralert repo")
        c.run("git clone "+ GIT_ZETRALERT_URL + " && exit")
        print("Repo successfully cloned")
        
        # Create the virtual environment
        print("Create the virtual environment")
        c.sudo("python3.7 -m venv /var/zetralert/venvs/venv && exit", user='zetralert')
        print("Virtual environment created")
        
        
        # Install requirments
        print("Install the requirements")
        c.sudo("/var/zetralert/venvs/venv/bin/pip3 install -r /var/zetralert/zetralerts/requirements.txt && exit", user='zetralert') 
        
        # Create the .env file
        print("Uploading the .env file...")
        c.put(path.join(getcwd(),"conf",".env"), ".env")
        c.run("sudo mv .env /var/zetralert/zetralerts/.env && exit")
                
        
        print("==== DEPLOY COMPLETE =====")  
        


@task
def test_zetralert(ctx):
    """Run a simple test """
    with Connection(
        HOST_NAME,
        user=ROOT_USERNAME,
        connect_kwargs={"key_filename": path.join(PEM_KEY_DIR, PEM_KEY)}
    ) as c:
        
        output = c.sudo("/var/zetralert/venvs/venv/bin/python3.7 /var/zetralert/zetralerts/test_zetralert.py")
        print(output.stdout.split("\r\n"))

@task    
def start_zetralert(ctx):
    """ Start Zetralert """
    
    with Connection(
        HOST_NAME,
        user=ROOT_USERNAME,
        connect_kwargs={"key_filename": path.join(PEM_KEY_DIR, PEM_KEY)}
    ) as c:
        
         c.sudo("nohup /var/zetralert/venvs/venv/bin/python3.7 /var/zetralert/zetralerts/main.py & " + " && exit", user='zetralert')
         print("Zetralerts has been started...")
    
@task
def stop_zetralert(ctx):
    """ Stop Zetralert """
    
    with Connection(
        HOST_NAME,
        user=USER_NAME,
        connect_kwargs={"key_filename": path.join(PEM_KEY_DIR, PEM_KEY)}
    ) as c:
        
        c.run("kill -9 `pgrep -f nohup` &")
        c.run("kill -9 `pgrep -f python3` &")


@task
def install_talib(ctx):
    """ Install TA-LIB """    
    
    with Connection(
        HOST_NAME,
        user=ROOT_USERNAME,
        connect_kwargs={"key_filename": path.join(PEM_KEY_DIR, PEM_KEY)}
    ) as c:
         
         print("==== Installing TALIB ======")
         
         # Get the talib tar file
         c.run("sudo wget https://artiya4u.keybase.pub/TA-lib/ta-lib-0.4.0-src.tar.gz")
            
         # Unzip
         c.run("sudo tar -xvf ta-lib-0.4.0-src.tar.gz")
         
         # Configure
         c.run("cd ta-lib/ && ./configure --prefix=/usr")
         
         # make 
         c.run("cd ta-lib/ && make")
         
         # make install
         c.run("cd ta-lib/ && install")
         
         print("==== Installation of TALIB COMPLETE ======")
    
@task
def deploy_zetralerts(ctx):
    """
    Setup and deploy a new instance of Zetralerts
    """
    
    _setup_new_instance()
    
    _deploy_new_zetralert_instance()
    
    
    
