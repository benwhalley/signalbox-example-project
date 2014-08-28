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

# needed because of a bug in compressor which otherwise crashes the debug view
COMPRESS_JINJA2_GET_ENVIRONMENT="None"


from signalbox.configurable_settings import *
from signalbox.settings import *


# amazon files settings
AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID', default="")
AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY', default="")
AWS_STORAGE_BUCKET_NAME = get_env_variable(
    "AWS_STORAGE_BUCKET_NAME", default="signalbox",
    warning="Specify an S3 bucket name in which to store uploaded files."
)
COMPRESS_ENABLED = get_env_variable('COMPRESS_ENABLED', default=True)
AWS_QUERYSTRING_AUTH = get_env_variable('AWS_QUERYSTRING_AUTH', default=False)

# keep these secret
TWILIO_ID = get_env_variable('TWILIO_ID', required=False)
TWILIO_TOKEN = get_env_variable('TWILIO_TOKEN', required=False)

# DO SOME EXTRA SETUP BASED ON THESE VALUES
# setup twilio based on settings above
try:
    TWILIOCLIENT = TwilioRestClient(TWILIO_ID, TWILIO_TOKEN)
except twilio.TwilioException:
    TWILIOCLIENT = None


GOOGLE_TRACKING_ID = get_env_variable('GOOGLE_TRACKING_ID', default="")


##### EMAIL #####

# # TODO: allow for non-mailgun backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = get_env_variable('MAILGUN_SMTP_SERVER', required=False, warning="Set an smtp hostname.")
EMAIL_PORT = int(get_env_variable('MAILGUN_SMTP_PORT', required=False, default="587", warning="SMTP port defaulting to 465."))
EMAIL_HOST_USER = get_env_variable('MAILGUN_SMTP_LOGIN', required=False, )
EMAIL_HOST_PASSWORD = get_env_variable('MAILGUN_SMTP_PASSWORD', required=False, )



HERE = os.path.realpath(os.path.dirname(__file__))
PROJECT_PATH, SETTINGS_DIR = os.path.split(HERE)
DJANGO_PATH, APP_NAME = os.path.split(PROJECT_PATH)

#####  FILEs  #####
USER_UPLOAD_STORAGE_BACKEND = 'signalbox.s3.PrivateRootS3BotoStorage'
MAIN_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'signalbox.s3.MediaRootS3BotoStorage'

COMPRESS_ROOT = STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

TEMPLATE_STRING_IF_INVALID = ""

from fnmatch import fnmatch



class glob_list(list):
    def __contains__(self, key):
        for elt in self:
            if fnmatch(key, elt):
                return True
        return False

INTERNAL_IPS = glob_list([
    '127.0.0.1',
    '141.163.66.*'
])

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
    USE_VERSIONING and 'reversion.middleware.RevisionMiddleware' or None,
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'signalbox.middleware.filter_persist_middleware.FilterPersistMiddleware',
    'signalbox.middleware.loginformmiddleware.LoginFormMiddleware',
    'signalbox.middleware.adminmenumiddleware.AdminMenuMiddleware',
    # 'signalbox.middleware.permissiondenied.PermissionDeniedToLoginMiddleware',
    # 'signalbox.middleware.error_messages_middleware.ErrorMessagesMiddleware',
    # 'signalbox.middleware.superuser.UserBasedExceptionMiddleware',
    # 'twiliobox.middleware.speak_error_messages_middleware.SpeakErrorMessagesMiddleware',
    "djangosecure.middleware.SecurityMiddleware",
    'django.middleware.locale.LocaleMiddleware',

)

MIDDLEWARE_CLASSES = filter(bool, MIDDLEWARE_CLASSES)

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
    'sekizai.context_processors.sekizai',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'signalbox.context_processors.globals',
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

    'django.contrib.humanize',
    'django_admin_bootstrapped',
    'admin_tools.dashboard',
    'django.contrib.admin',
    "compressor",
    'registration',
    'mptt',
    USE_VERSIONING and 'reversion' or None,
    'django_extensions',
    'menus',
    'sekizai',
    'selectable',
    'storages',
    'floppyforms',
    'bootstrap-pagination',
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

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda o: "/accounts/profile/",
}


LANGUAGE_CODE = 'en'
TIME_ZONE = 'Europe/London'
USE_I18N = False
USE_L10N = False


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}
# COMPRESS_ENABLED=False
