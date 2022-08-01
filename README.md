# multi-app-django-gunicorn-nginx-postgreSQL

# Introduction
## [Part One: setting up django with postgres, Nginx, and Gunicorn on Ubuntu 22.04](#Part-One)
## [Part Two: serving multiple Django applications with Nginx, Gunicorn and supervisor](#Part-Two)
## [Reference](#Reference)

# Part One
## **Setting Up Django with Postgres, Nginx, and Gunicorn on Ubuntu 22.04**
## Content
[Prerequisites](#Prerequisites)

[Installing the packages from the Ubuntu repositories (python3, postgreSQL-13, Nginx, Supervisor)](#Installing-the-packages-from-the-Ubuntu-repositories)

[Creating a database user and a new database for the app](#Creating-a-database-user-and-a-new-database-for-the-app)

[Creating application user](#Creating-application-user)

[Allowing other users write access to the application directory](#Allowing-other-users-write-access-to-the-application-directory)

[Creating a virtual environment for your app](#Creating-a-virtual-environment-for-your-app)

[Database configuration](#Database-configuration)

[Creating an empty Django project](#Creating-an-empty-Django-project)

[Configuring gunicorn](#Configuring-gunicorn)

[Starting and monitoring with supervisor](#Starting-and-monitoring-with-supervisor)

[Creating a nginx virtual server configuration for Django](#Creating-a-nginx-virtual-server-configuration-for-Django)

[Uninstalling the Django application](#Uninstalling-the-Django-application)

## Prerequisites 
* Ubuntu 22.04 server instance with a basic firewall and a non-root user with `sudo` privileges configured. 
* python 3.10.4

[Content](#Part-One)

## Installing the packages from the Ubuntu repositories
```shell
# 
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc |  apt-key add -
sudo apt-get update 
# install python and related packages
sudo apt-get -y install python3-pip python3-dev python3-venv libpq-dev
# install postgresql-13
sudo apt-get -y install postgresql-13   postgresql-contrib-13 
# install nginx
sudo apt-get -y install nginx
# install other util
sudo apt-get -y install curl
# install supervisor
sudo apt-get -y install supervisor
```
or one-line-command
```shell
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" \
> /etc/apt/sources.list.d/pgdg.list' \
&& wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc |  apt-key add -

sudo apt-get update && apt-get -y install postgresql-13 python3-pip \
               python3-dev libpq-dev  postgresql-contrib-13 nginx curl
```
[Content](#Part-One)

## Creating a database user and a new database for the app
```shell
# should create an DB_init.sql first using Docs/settings/GenDBSQL.sh
sudo  -u postgres psql -f DB_init.sql 
```
[Content](#Part-One)

## Creating application user
```shell
sudo groupadd --system webapps
#useradd --system --gid webapps --shell /bin/bash -m -d /webapps/django_app_one app_one
sudo useradd --system --gid webapps -m -d /webapps/<name-for-the-webapps> <application-user>
```
[Content](#Part-One)

## Allowing other users write access to the application directory
```shell
chown -R app_one:www-data /webapps/hello_django
```
[Content](#Part-One)

## Creating a virtual environment for your app
```shell
python3 -m venv venv
source venv/bin/activate
# use the following cmd to install necessary packages when first working with the development environment
pip install django gunicorn psycopg2-binary
pip freeze > requirements.txt
# use this cmd when deploy to the VPS 
pip install -r requirements.txt
```
[Content](#Part-One)

## Database configuration
```shell
cp settings/env.sh ~/ 
# fill out the Database related information in ~/env.sh
vi ~/env.sh
chmod u+x ~/env.sh
vi ~/.bashrc
# add the following lines to the end of ~/.bashrc
if [ -f ~/env.sh ];then
  . ~/env.sh
fi 

source ~/.bashrc


# locate listen_addresses and change it value to '*', making it like listen_addresses = '*'
sudo vi /etc/postgresql/13/main/postgresql.conf 
# locate the 'IPv4 local connection' and 'IPv6 local connection' session
# and change the 127.0.0.1/32 to 0.0.0.0/0 for IPv4 and ::1/128 to ::0/0 for IPv6
# making it like 
# host	all		all		0.0.0.0/0		md5
# host all 		all 		::0/0			md5
sudo vi /etc/postgresql/13/main/pg_hba.conf  

```
[Content](#Part-One)

## Creating an empty Django project
```shell
# this is done in the development environment
cd <projectdir>
django-admin.py startproject <application-name>
cd <application-dir>
# splitting settings for the application
# refer to the following setting files, 
# -- settings/config/base.py
# -- settings/config/local.py
# -- settings/config/prod.py
# -- settings/settings.py
# replace the settings.py in the application-dir with settings/settings.py and make necessary changes if needed.
# copy settings/config/*

python manage.py makemigrations
python manage.py migrate

python manage.py runserver
# for testing purpose on VPS, 
ufw allow 8000
python manage.py runserver 0.0.0.0:8000
ufw delete allow 8000
# 

python manage.py createspueruser
python manage.py collectstatic

```
[Content](#Part-One)

## Configuring gunicorn
```shell
# testing if gunicorn is running
sudo ufw allow 8001
gunicorn <app>.wsgi:application --bind example.com:8001
sudo ufw delete allow 8001
# make necessary changes to the file
cd ~
vi gunicorn.start.sh
chmod u+x gunicorn.start.sh
```
[Content](#Part-One)

## Starting and monitoring with supervisor
```shell

sudo vi /etc/supervisor/conf.d/<app>.conf
mkdir -p /webapps/<application-home>/logs 
touch /webapps/<application-home>/logs/gunicorn_supervisor.log 
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl  status <app-name>
sudo supervisorctl stop <app-name>
sudo supervisorctl start <app-name>
sudo supervisorctl restart <app-name>
```
[Content](#Part-One)

## Creating a nginx virtual server configuration for Django
```shell
vi /etc/nginx/sites-available/app_one
ln -s /etc/nginx/sites-available/app_one /etc/nginx/sites-enabled/app_one
sudo nginx -t 
sudo systemctl restart nginx
```
[Content](#Part-One)

## Uninstalling the Django application
```shell
sudo rm /etc/nginx/sites-enabled/app_one
sudo systemctl nginx restart
# if you never plan to use this application again, you can remove its config file also
sudo rm /etc/nginx/sites-available/app_one
sudo supervisorctl stop app_one
sudo rm /etc/supervisor/conf.d/hello.conf
# if you never plan to use this application again, you can remove its entire directory
sudo rm -r /webapps/django_app_one
```
[Content](#Part-One)

# Part Two
## Serving multiple Django applications with Nginx, Gunicorn and supervisor
## Content
[Create a virtual environment for each app](#Create-a-virtual-environment-for-each-app)

[Create system accounts for the webapps](#Create-system-accounts-for-the-webapps)

[Create gunicorn start scripts](#Create-gunicorn-start-scripts)

[Create Supervisor configuration files and start the apps](#Create-Supervisor-configuration-files-and-start-the-apps)

[Create Nginx virtual servers](#Create-Nginx-virtual-servers)

[Top](#Introduction)

##Create a virtual environment for each app

[Content](#Part-Two)

##Create system accounts for the webapps
```shell
sudo groupadd --system webapps
sudo useradd --system --gid webapps -m -d /webapps/app_one app_one
sudo useradd --system --gid webapps -m -d /webapps/app_two app_two
sudo chown -R app_one:www-data /webapps/app_one
sudo chown -R app_two:www-data /webapps/app_two
```
[Content](#Part-Two)

##Create gunicorn start scripts
```shell
vi /webapps/app_one/bin/gunicorn.start.sh
vi /webapps/app_two/bin/gunicorn.start.sh
```
[Content](#Part-Two)

##Create Supervisor configuration files and start the apps
```shell
sudo vi /etc/supervisor/conf.d/app_one.conf
sudo vi /etc/supervisor/conf.d/app_two.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start app_one
sudo supervisorctl start app_two
```

[Content](#Part-Two)

##Create Nginx virtual servers
```shell
sudo vi /etc/nginx/sites-available/app_one
sudo vi /etc/nginx/sites-available/app_two
sudo ln -s /etc/nginx/sites-available/app_one /etc/nginx/sites-enabled/app_one
sudo ln -s /etc/nginx/sites-available/app_two /etc/nginx/sites-enabled/app_two
sudo systemctl restart nginx
```
[Content](#Part-Two)


# Reference
[initial server setup with ubuntu](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-22-04)

[how to set up Django with Postgres Nginx and gunicorn on ubuntu 22.04 ](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04)

[splitting up the settings file](https://code.djangoproject.com/wiki/SplitSettings#DevelopmentMachineDependantSettingsConfiguration)

[stack overflow: how to properly runserver on different settings for django](https://stackoverflow.com/questions/49235486/how-to-properly-runserver-on-different-settings-for-django)