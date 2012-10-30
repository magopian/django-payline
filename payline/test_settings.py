import os


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

INSTALLED_APPS = [
    'payline',
]

TEST_RUNNER = 'discover_runner.DiscoverRunner'
SECRET_KEY = 'better make this secret'
