"""Development settings (imported by default)."""
from .base import *
import os

# Development flags
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']

# Local database: prefer .env Postgres settings, fall back to SQLite for
# local development and test discovery when DATABASE_* is not provided.
db_name = env('DATABASE_NAME', default=None)
if db_name:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DATABASE_NAME'),
            'USER': env('DATABASE_USER'),
            'PASSWORD': env('DATABASE_PASSWORD'),
            'HOST': env('DATABASE_HOST'),
            'PORT': env('DATABASE_PORT'),
            'TEST': {
                'NAME': env('TEST_DATABASE_NAME'),
                'USER': env('DATABASE_USER'),
                'PASSWORD': env('DATABASE_PASSWORD'),
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Media and storage - local filesystem for development
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}

# Use a simple staticfiles storage in development to avoid manifest
# lookup errors when the manifest is not built.
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Email settings for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = env('MY_EMAIL', default='test@example.com')
EMAIL_HOST_PASSWORD = env('EMAIL_PASSWORD', default='test-password')
DEFAULT_FROM_EMAIL = env('MY_EMAIL', default='test@example.com')
EMAIL_TIMEOUT = 30
ADMINS = [('Admin', env('MY_EMAIL', default='test@example.com'))]

# Tailwind NPM path for Windows dev machines
if DEBUG:
    NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"

# Development logging (less verbose to console + file)
import logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'file_uploads.log',
            'formatter': 'detailed',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'formatters': {
        'detailed': {
            'format': '{asctime} {levelname} {name} {message}',
            'style': '{',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'boto3': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'storages.backends.s3boto3': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.utils.autoreload': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
