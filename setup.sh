#!/bin/bash
#Written by Deborah Venuti

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo '*BEGIN SETUP FOR MAC OSX*'
    echo '*'
    echo '*'
    echo '*INSTALLING VIRTUALENV*'
    pip3 install virtualenv 
    echo '*'
    echo '*'
    echo '*LAUNCHING POSTGRESQL*'
    open -a Postgres
    sleep 1
    echo '*'
    echo '*'
    echo '*SETTING UP DATABASE*'
    if  pgrep -q -x Postgres; then
        psql -f dbsetup.sql
    else
        echo 'Postgres is not running.'
    fi
    echo '*'
    echo '*'
    echo '*SETTING UP VIRTUAL ENVIRONMENT*'
    virtualenv -p python3 steg-venv
    echo '*'
    echo '*'
    echo '*INSTALLING DEPENDENCIES INTO THE VIRTUAL ENVIRONMENT*'
    steg-venv/bin/pip3 install -r requirements.txt
    echo '*'
    echo '*'
    echo '*MIGRATING DATABASE*'
    steg-venv/bin/python3 site/manage.py makemigrations main
    steg-venv/bin/python3 site/manage.py makemigrations
    steg-venv/bin/python3 site/manage.py migrate
    steg-venv/bin/python3 site/manage.py migrate main
    echo '*'
    echo '*'
    echo '*CREATING SUPERUSER FOR ADMIN USE*'
    steg-venv/bin/python3 site/manage.py createsuperuser
    echo '*'
    echo '*'
    echo '*SETUP COMPLETE*'
    echo 'TO LAUNCH STEGASAURUS TYPE make AND OPEN http://127.0.0.1:8000 IN ANY BROWSER'

#------------------------------------------------------------#

elif [[ "$OSTYPE" == "linux-gnu" ]]; then
    echo '*BEGIN SETUP FOR UNIX/LINUX*'
    echo '*'
    echo '*'
    echo '*INSTALLING POSTGRESQL*'
    sudo apt-get update
    sudo apt-get install postgresql postgresql-contrib
    sudo apt-get install postgresql libpq-dev postgresql-client postgresql-client-common
    echo '*'
    echo '*'
    echo '*INSTALLING PIP FOR PYTHON3*'
    sudo apt-get install python3-pip
    echo '*'
    echo '*'
    echo '*INSTALLING VIRTUALENV*'
    pip3 install virtualenv 
    echo '*'
    echo '*'
    echo '*SETTING UP DATABASE*'
    sudo -u postgres psql -f dbsetup.sql
    echo '*'
    echo '*'
    echo '*SETTING UP VIRTUAL ENVIRONMENT*'
    virtualenv -p python3 steg-venv
    echo '*'
    echo '*'
    echo '*INSTALLING DEPENDENCIES INTO THE VIRTUAL ENVIRONMENT*'
    sudo steg-venv/bin/pip3 install -r requirements.txt
    echo '*'
    echo '*'
    echo '*MIGRATING DATABASE*'
    steg-venv/bin/python3 site/manage.py makemigrations main
    steg-venv/bin/python3 site/manage.py makemigrations
    steg-venv/bin/python3 site/manage.py migrate
    steg-venv/bin/python3 site/manage.py migrate main
    echo '*'
    echo '*'
    echo '*CREATING SUPERUSER FOR ADMIN USE*'
    steg-venv/bin/python3 site/manage.py createsuperuser
    echo '*'
    echo '*'
    echo '*SETUP COMPLETE*'
    echo 'TO LAUNCH STEGASAURUS TYPE make AND OPEN http://127.0.0.1:8000 IN ANY BROWSER'
fi
