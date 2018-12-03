from copy import copy

from .base import *

DEBUG = True

# Copy Installed Apps and Middleware to allow removal of unwanted list items.
INSTALLED_APPS = copy(INSTALLED_APPS)
MIDDLEWARE = copy(MIDDLEWARE)

ENVIRONMENT = 'DEVELOPMENT'

# Required for Django Debug Toolbar
INTERNAL_IPS = '192.168.2.1'

TEMPLATES[0]['APP_DIRS'] = True
del TEMPLATES[0]['OPTIONS']['loaders']
