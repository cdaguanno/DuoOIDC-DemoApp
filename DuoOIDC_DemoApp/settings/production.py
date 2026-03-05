"""
Production Django settings for DuoOIDC_DemoApp.
Inherits from base.py and overrides for production on EC2.

Used when running on EC2 with Gunicorn + Apache.
Reads configuration from .env file.
"""

import os
from .base import *

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
# Load from environment variable (.env file on EC2)
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-production')
if SECRET_KEY == 'change-me-in-production':
    raise ValueError('SECRET_KEY must be set in .env file for production!')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Set allowed hosts from environment variable
# Example in .env: ALLOWED_HOSTS=192.168.1.100,duooidc.internal.local
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS]
CSRF_TRUSTED_ORIGINS = ['https://765-lab-control-center-cl-8204930.ztna.sse.cisco.io']


# Production database configuration - PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'duooidc_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Security settings for production
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False') == 'True'
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False') == 'True'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False') == 'True'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
}

# CORS settings for production (restrict to specific origins)
CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost'
).split(',')
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in CORS_ALLOWED_ORIGINS]

# Static files configuration for Apache reverse proxy
# WhiteNoise handles serving static files efficiently
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Logging level for production (INFO or WARNING)
# Logging level for production (INFO or WARNING)
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': LOG_LEVEL,
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
        },
    },
}

# Email configuration for production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '25'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'False') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')

# Duo OIDC Configuration (if you implement OIDC authentication)
DUO_CLIENT_ID = os.getenv('DUO_CLIENT_ID', '')
DUO_CLIENT_SECRET = os.getenv('DUO_CLIENT_SECRET', '')
DUO_API_HOSTNAME = os.getenv('DUO_API_HOSTNAME', '')
DUO_REDIRECT_URI = os.getenv('DUO_REDIRECT_URI', '')

# Session settings for production
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Media configuration for production
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')