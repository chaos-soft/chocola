from .base import *

DEBUG = True
INSTALLED_APPS += ['debug_toolbar.apps.DebugToolbarConfig']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_PATCH_SETTINGS = False
ROOT_URLCONF = 'config.urls.local'
