"""Production settings for Render (or other hosts).

Set DJANGO_SETTINGS_MODULE to portfolio_project.settings.prod in production.
"""
from .base import *
import os
import dj_database_url
from boto3 import session

# Production flags
DEBUG = False

SECRET_KEY = env('SECRET_KEY')

# Allowed hosts can be provided via env or fallback to common host
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['portfolio-project-jn1z.onrender.com', 'www.jessevahlfors.com'])

# Database: use dj-database-url for Render-style DATABASE_URL
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}

# AWS / S3 storage (Backblaze B2 via S3 compatible endpoint)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.getenv('B2_APPLICATION_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('B2_APPLICATION_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('B2_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('B2_REGION_NAME', 'us-west-002')
AWS_S3_ENDPOINT_URL = f"https://s3.{AWS_S3_REGION_NAME}.backblazeb2.com"
AWS_S3_ADDRESSING_STYLE = 'virtual'
AWS_QUERYSTRING_AUTH = False
AWS_LOCATION = 'media/'

AWS_REQUEST_CHECKSUM_CALCULATION = os.getenv('AWS_REQUEST_CHECKSUM_CALCULATION', 'WHEN_REQUIRED')
AWS_RESPONSE_CHECKSUM_VALIDATION = os.getenv('AWS_RESPONSE_CHECKSUM_VALIDATION', 'WHEN_REQUIRED')

boto3_session = session.Session()
boto3_session._session.set_config_variable('s3', {
    'checksum_calculation': AWS_REQUEST_CHECKSUM_CALCULATION,
    'checksum_validation': AWS_RESPONSE_CHECKSUM_VALIDATION,
})

STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# Email backend for production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "true").lower() == "true"

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL",
    EMAIL_HOST_USER,  # sensible fallback
)

CONTACT_TO_EMAIL = os.getenv(
    "CONTACT_TO_EMAIL",
    EMAIL_HOST_USER,  # sensible fallback
)

# Production logging
import logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'root': {
        'handlers': ['console', 'mail_admins'],
        'level': 'ERROR',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'boto3': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'botocore': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
