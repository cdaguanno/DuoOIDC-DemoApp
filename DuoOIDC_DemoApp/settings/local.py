"""
Local development Django settings for DuoOIDC_DemoApp.
Inherits from base.py and overrides for local development.

Used when running: python manage.py runserver --settings=DuoOIDC_DemoApp.settings.local
"""

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
# This is fine for local dev; will be overridden in production
SECRET_KEY = 'a5a58a23-cb10-475a-abe7-6de4f6f6d259'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow localhost for local development
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

# Local database configuration - SQLite (simple for development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Disable security settings for local development (HTTPS not needed)
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Allow all origins for local development
CORS_ALLOW_ALL_ORIGINS = True

# Logging level for local development (more verbose)
LOGGING['root']['level'] = 'DEBUG'
LOGGING['loggers']['django']['level'] = 'DEBUG'

# Email configuration for local development (console output)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Media configuration for local development (console output)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')