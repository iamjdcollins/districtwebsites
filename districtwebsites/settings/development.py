from copy import copy

from .base import *

DEBUG = True

# Copy Installed Apps and Middleware to allow removal of unwanted list items.
INSTALLED_APPS = copy(INSTALLED_APPS)
MIDDLEWARE = copy(MIDDLEWARE)

ENVIRONMENT = 'DEVELOPMENT'

# Required for Django Debug Toolbar
INTERNAL_IPS = '192.168.2.1'

STATIC_URL = 'https://websites-dev.slcschools.org/static/'
