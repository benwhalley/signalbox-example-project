import os
from get_env_variable import get_env_variable


DEV = bool(get_env_variable('DEVELOPMENT', required=False, default=False))

if DEV:
    # TEMPLATE_STRING_IF_INVALID = 'INVALID EXPRESSION: %s'
    SECURE_SSL_REDIRECT = False
    MY_SITE_PORT = 8000
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


    # # debug_toolbar settings
    # INTERNAL_IPS = ('127.0.0.1',)
    # MIDDLEWARE_CLASSES += (
    #     # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    #     # 'app.signalbox.middleware.profiling.ProfileMiddleware',
    # )

    # INSTALLED_APPS += (
    #     'debug_toolbar',
    # )

    # DEBUG_TOOLBAR_PANELS = (
    #     # 'debug_toolbar.panels.version.VersionDebugPanel',
    #     'debug_toolbar.panels.timer.TimerDebugPanel',
    #     # 'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    #     # 'debug_toolbar.panels.headers.HeaderDebugPanel',
    #     # 'debug_toolbar.panels.profiling.ProfilingDebugPanel',
    #     # 'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    #     'debug_toolbar.panels.sql.SQLDebugPanel',
    #     # 'debug_toolbar.panels.template.TemplateDebugPanel',
    #     # 'debug_toolbar.panels.cache.CacheDebugPanel',
    #     # 'debug_toolbar.panels.signals.SignalDebugPanel',
    #     # 'debug_toolbar.panels.logger.LoggingPanel',
    # )

    # DEBUG_TOOLBAR_CONFIG = {
    #     'INTERCEPT_REDIRECTS': False,
    # }



