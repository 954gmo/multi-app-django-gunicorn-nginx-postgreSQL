# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

import sys

"""
Django settings for app_one project
"""


import importlib
# Begin: Custom per-env settings
import socket
HOST = socket.gethostname()
configs = {
    'DESKTOP-0UV5SFP': 'local',
    'mail.sixdigit.net': 'prod',
}
config = f'config.{configs[HOST]}'

settings_module = importlib.import_module(config)
try:
    for setting in dir(settings_module):
        # Only fully-uppercase variables are supposed to be settings
        if setting == setting.upper():
            locals()[setting] = getattr(settings_module, setting)
except Exception:
    # could be ignore, the print is for debugging purposes
    print(Exception)

# End: Custom per-env settings

# the rest of the common settings go here
base_settings = importlib.import_module('config.base')
try:
    for setting in dir(base_settings):
        if setting == setting.upper():
            locals()[setting] = getattr(base_settings, setting)
except Exception:
    print(Exception)