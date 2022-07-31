# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-caebb+zs_ai6s@q#%90%+(p4e78w5khn5k8+9)vlznx+mg9ubl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['sixdigit.net', 'www.sixdigit.net']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE_app_two'),
        'USER': os.getenv('DB_USER_app_two'),
        'PASSWORD': os.getenv('DB_PASS_app_two'),
        'HOST': os.getenv('DB_HOST_app_two'),
        'PORT': os.getenv('DB_PORT_app_two'),
    }
}
