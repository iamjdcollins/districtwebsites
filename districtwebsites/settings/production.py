from copy import copy

from .base import *

ENVIRONMENT = 'PRODUCTION'

# Copy Installed Apps and Middleware to allow removal of unwanted list items.
INSTALLED_APPS = copy(INSTALLED_APPS)
MIDDLEWARE = copy(MIDDLEWARE)

# Remove unwanted apps
if 'debug_toolbar' in INSTALLED_APPS:
    INSTALLED_APPS.remove('debug_toolbar')

# Remove unwanted middleware
if 'debug_toolbar.middleware.DebugToolbarMiddleware' in MIDDLEWARE:
    MIDDLEWARE.remove('debug_toolbar.middleware.DebugToolbarMiddleware')
if 'django.middleware.gzip.GZipMiddleware' in MIDDLEWARE:
    MIDDLEWARE.remove('django.middleware.gzip.GZipMiddleware')
