import os
from payline.test_settings import *  # noqa
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DEBUG = True
TEMPLATE_DEBUG = True
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
] + INSTALLED_APPS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'demoshop.db'),
    },
}

PAYLINE_API = 'WebPayment'
PAYLINE_MERCHANT_ID = os.environ.get('PAYLINE_MERCHANT_ID')
PAYLINE_KEY = os.environ.get('PAYLINE_KEY')
PAYLINE_RETURN_URL = 'http://localhost:8000/payment-success/'
PAYLINE_CANCEL_URL = 'http://localhost:8000/payment-cancel/'
PAYLINE_NOTIFICATION_URL = 'http://localhost:8000/payment-notify/'

PAYLINE_VADNBR = os.environ.get('PAYLINE_VADNBR')
ROOT_URLCONF = 'demo.urls'
STATIC_URL = '/static/'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'include_html': True,
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'syslog': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'shop': {
            'handlers': ['mail_admins', 'syslog'],
            'level': 'ERROR',
        },
        'payline': {
            'handlers': ['mail_admins', 'syslog'],
            'level': 'ERROR',
        },
    }
}
