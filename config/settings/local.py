from .base import *

DEBUG = True

# For local development, we can override settings here
ALLOWED_HOSTS = ['*']

# Console backend for emails during development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
