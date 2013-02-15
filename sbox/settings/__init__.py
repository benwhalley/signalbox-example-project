import string
import os
import imp
import sys
from get_env_variable import get_env_variable
from paths import *
sys.path.append(APP_NAME)

from files_settings import *
from django_settings import *
from secret_settings import *
from database_settings import *
from email_settings import *
from cms_settings import *
from logging_settings import *
from security_settings import *
from signalbox.settings import *
from dev_settings import *

from frontend_name import FRONTEND
exec("from {}.settings import *".format(FRONTEND))
INSTALLED_APPS = [FRONTEND] + INSTALLED_APPS


DEBUG = get_env_variable('DEBUG', int_to_bool=True, required=False, default=False)
TEMPLATE_DEBUG = DEBUG

# turn caching off in debug environment
if DEBUG:
    TEMPLATE_LOADERS = TEMPLATE_LOADERS[0][1]

