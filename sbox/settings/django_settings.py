import socket
from twilio.rest import TwilioRestClient
import os

HERE = os.path.realpath(os.path.dirname(__file__))
PROJECT_PATH, SETTINGS_DIR = os.path.split(HERE)
DJANGO_PATH, APP_NAME = os.path.split(PROJECT_PATH)

ROOT_URLCONF = 'urls'
SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # reversion must go after transaction
    'django.middleware.transaction.TransactionMiddleware',
    'reversion.middleware.RevisionMiddleware',

    'signalbox.middleware.filter_persist_middleware.FilterPersistMiddleware',
    'signalbox.middleware.cms_page_permissions_middleware.CmsPagePermissionsMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',

    'signalbox.middleware.loginformmiddleware.LoginFormMiddleware',
    'signalbox.middleware.adminmenumiddleware.AdminMenuMiddleware',
    'signalbox.middleware.permissiondenied.PermissionDeniedToLoginMiddleware',

    "djangosecure.middleware.SecurityMiddleware",
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

)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

INSTALLED_APPS = [
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
    'adminactions',
    'cms',
    'cmsmenu_redirect',
    'registration',
    'south',
    'mptt',
    'reversion',
    'django_extensions',
    'menus',
    'sekizai',
    'selectable',
    'storages',
    'django_nose',
    'cms.plugins.picture',
    'cms.plugins.file',
    'cms.plugins.snippet',
    'cmsplugin_simple_markdown',
    'compressor',
    'floppyforms',
    'bootstrap-pagination',
    # 'kronos',
]


TEMPLATE_LOADERS = (
    'apptemplates.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
)

# caching enabled because floppyforms is slow otherwise; disable for development
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
)

# REGISTRATION #
AUTH_PROFILE_MODULE = 'signalbox.UserProfile'
ACCOUNT_ACTIVATION_DAYS = 14  # One-week activation window for user accts


# cron jobs for scheduled tasks
KRONOS_MANAGE = os.path.join(DJANGO_PATH, "app/manage.py")

# nose for tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda o: "/accounts/profile/",
}

# SESSION_COOKIE_AGE = 1.5 * 60 * 60  # 1.5 hours in seconds (default is 2 wks)
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
