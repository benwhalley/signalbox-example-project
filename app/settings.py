# -*- coding: utf-8 -*-
from django.core.files.storage import FileSystemStorage
from signalbox.configurable_settings import *
from signalbox.utilities.get_env_variable import get_env_variable
from twilio.rest import TwilioRestClient
import imp
import sys
import os
import socket
import string

sys.path.insert(1, os.path.dirname(os.path.realpath(__file__)))

from signalbox.configurable_settings import *
from signalbox.settings import *

HERE = os.path.realpath(os.path.dirname(__file__))
PROJECT_PATH, SETTINGS_DIR = os.path.split(HERE)
DJANGO_PATH, APP_NAME = os.path.split(PROJECT_PATH)

#####  FILEs  #####
USER_UPLOAD_STORAGE_BACKEND = 'signalbox.s3.PrivateRootS3BotoStorage'
MAIN_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'signalbox.s3.MediaRootS3BotoStorage'

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'



##### STANDARD DJANGO STUFF #####
ROOT_URLCONF = 'urls'
SITE_ID = 1
SESSION_ENGINE = "django.contrib.sessions.backends.file"

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',


    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # reversion must go after transaction
    'django.middleware.transaction.TransactionMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'signalbox.middleware.filter_persist_middleware.FilterPersistMiddleware',
    'signalbox.middleware.cms_page_permissions_middleware.CmsPagePermissionsMiddleware',
    'signalbox.middleware.loginformmiddleware.LoginFormMiddleware',
    'signalbox.middleware.adminmenumiddleware.AdminMenuMiddleware',
    'signalbox.middleware.permissiondenied.PermissionDeniedToLoginMiddleware',
    'signalbox.middleware.error_messages_middleware.ErrorMessagesMiddleware',
    "djangosecure.middleware.SecurityMiddleware",
    'django.middleware.locale.LocaleMiddleware',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'cms.context_processors.media',
    'sekizai.context_processors.sekizai',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

INSTALLED_APPS = [
    'frontend',
    'ask',
    'twiliobox',
    'djangosecure',
    'signalbox',
    'django.contrib.auth',
    'django.contrib.redirects',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.markup',
    'django.contrib.humanize',
    'django_admin_bootstrapped',
    'admin_tools.dashboard',
    'django.contrib.admin',
    'cms',
    "compressor",
    'cmsmenu_redirect',
    'registration',
    'south',
    'mptt',
    USE_VERSIONING and 'reversion' or None,
    'django_extensions',
    'menus',
    'sekizai',
    'selectable',
    'storages',
    'cms.plugins.picture',
    'cms.plugins.file',
    'cms.plugins.snippet',
    'cmsplugin_simple_markdown',
    'floppyforms',
    'bootstrap-pagination',
    'kronos',
    'gunicorn',
]
# filter out conditionally-skipped apps (which create None's)
INSTALLED_APPS = filter(bool, INSTALLED_APPS)

TEMPLATE_LOADERS = (
    'apptemplates.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
)

# caching enabled because floppyforms is slow otherwise; disable for development
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
)

# turn off template caching/debugging in debug environment
TEMPLATE_DEBUG = DEBUG
if DEBUG:
    TEMPLATE_LOADERS = TEMPLATE_LOADERS[0][1]

# REGISTRATION #
AUTH_PROFILE_MODULE = 'signalbox.UserProfile'

# cron jobs for scheduled tasks
KRONOS_MANAGE = os.path.join(DJANGO_PATH, "app/manage.py")

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda o: "/accounts/profile/",
}


LANGUAGE_CODE='en-uk'
TIME_ZONE = 'Europe/London'
USE_I18N = False
USE_L10N = False




##### CMS #####

PLACEHOLDER_FRONTEND_EDITING = True
SOUTH_TESTS_MIGRATE = False
CMS_REDIRECTS=True

CMS_TEMPLATES = (
    ('base.html', 'base'),
    ('home.html', 'home'),
    ('two.html', 'two'),
)

LANGUAGES = (
    ('en-uk', 'English'),
)

CMS_LANGUAGES = {
        1: [
            {
                'code': 'en-uk',
                'name': 'English',
                'public': True,
                'hide_untranslated': True,
                'redirect_on_fallback':False,
            },
        ],
        'default': {
            'fallbacks': ['en-uk',],
            'public': False,
            'redirect_on_fallback':True,
            'hide_untranslated': False,
        }
    }




LOGGING = {
    'version': 1,
    'formatters': {
    'verbose': {
        'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
    },
        'simple': {
        'format': '%(levelname)s %(message)s'
        },
    },
'handlers': {
    'null': {
        'level': 'DEBUG',
        'class': 'django.utils.log.NullHandler',
    },
    'console': {
        'level': 'DEBUG',
        'class': 'logging.StreamHandler',
        'formatter': 'simple'
    },
},
'loggers': {
    'django': {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': True,
    },
    'signalbox': {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': True,
    }
}
}
