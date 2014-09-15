import os


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'south',
    'payline',
]

PAYLINE_MERCHANT_ID = os.environ.get('PAYLINE_MERCHANT_ID')
PAYLINE_KEY = os.environ.get('PAYLINE_KEY')
PAYLINE_VADNBR = os.environ.get('PAYLINE_VADNBR')

SECRET_KEY = 'better make this secret'
