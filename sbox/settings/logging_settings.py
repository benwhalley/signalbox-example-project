import os
import sys
from paths import *

if 'DATABASE_URL' in os.environ: # we are on heroku
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
        'mail_admins': {
        'level': 'ERROR',
        'class': 'django.utils.log.AdminEmailHandler',
        'include_html': False
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': sys.stdout
            },
        },

    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'WARNING',
            'propagate': True,
            },
        'signalbox.cron': {
                'handlers': ['console', ],
                'level': 'INFO',
                'propagate': True,
                }
        }
    }

else:
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
            'mail_admins': {
                        'level': 'ERROR',
                        'class': 'django.utils.log.AdminEmailHandler',
                        'include_html': False
                    },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
                },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.path.join(DJANGO_PATH, 'log/app.log'),
                'formatter': 'verbose'
                },

            'cronlogfile': {
                'level': 'DEBUG',
                'class': 'logging.handlers.WatchedFileHandler',
                'filename': os.path.join(DJANGO_PATH, 'log/cron.log'),
                'formatter': 'simple',
                },
            },
        'loggers': {
            'django': {
                'handlers': ['file', 'mail_admins'],
                'level': 'WARNING',
                'propagate': True,
                },
            'signalbox.cron': {
                    'handlers': ['cronlogfile', ],
                    'level': 'INFO',
                    'propagate': True,
                    },
            }
        }
