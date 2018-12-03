from .base import *

DEBUG = True

ENVIRONMENT = 'DEVELOPMENT'

# Required for Django Debug Toolbar
INTERNAL_IPS = '192.168.2.1'

TEMPLATES[0]['APP_DIRS'] = True
del TEMPLATES[0]['OPTIONS']['loaders']
