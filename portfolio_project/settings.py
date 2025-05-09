"""
Django settings for portfolio_project project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import environ
import os
import dj_database_url
import logging


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)


if os.getenv('RENDER') == 'true':  # Check if running on Render
    ALLOWED_HOSTS = ['portfolio-project-jn1z.onrender.com', 'www.jessevahlfors.com']
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'corsheaders',
    'rest_framework',
    'home.apps.HomeConfig',
    'tailwind',
    'theme',
    'storages',
    'json_parser',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.gzip.GZipMiddleware',  
]

if DEBUG: # only add debug toolbar when in debug mode
    INSTALLED_APPS.append('debug_toolbar')
    INSTALLED_APPS.append('django_browser_reload')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    MIDDLEWARE.append('django_browser_reload.middleware.BrowserReloadMiddleware')

if os.getenv('RENDER') == 'true':  # Check if running on Render
    CORS_ALLOWED_ORIGINS = [
        'https://portfolio-project-jn1z.onrender.com',
        'https://www.jessevahlfors.com',
    ]
else:
    CORS_ALLOWED_ORIGINS = [
        'http://localhost:8000',
        'http://localhost:8000',
        'http://127.0.0.1:9000',
    ]

ROOT_URLCONF = 'portfolio_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'portfolio_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if os.getenv('RENDER') == 'true':  # Check if running on Render
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
    }
else:
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


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Helsinki'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

from boto3 import session
from botocore.config import Config

if os.getenv('RENDER') == 'true':
    # Production settings (Render)
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = os.getenv("B2_APPLICATION_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("B2_APPLICATION_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("B2_BUCKET_NAME")
    AWS_S3_REGION_NAME = os.getenv("B2_REGION_NAME", "us-west-002")
    AWS_S3_ENDPOINT_URL = f"https://s3.{AWS_S3_REGION_NAME}.backblazeb2.com"
    AWS_S3_ADDRESSING_STYLE = "virtual"
    AWS_QUERYSTRING_AUTH = False
    AWS_LOCATION = "media/"

    AWS_REQUEST_CHECKSUM_CALCULATION = os.getenv("AWS_REQUEST_CHECKSUM_CALCULATION", "WHEN_REQUIRED")
    AWS_RESPONSE_CHECKSUM_VALIDATION = os.getenv("AWS_RESPONSE_CHECKSUM_VALIDATION", "WHEN_REQUIRED")

    boto3_session = session.Session()
    boto3_session._session.set_config_variable('s3', {
        'checksum_calculation': AWS_REQUEST_CHECKSUM_CALCULATION,
        'checksum_validation': AWS_RESPONSE_CHECKSUM_VALIDATION,
    })

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
else:
    # Local development settings
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    BASE_DIR / "theme/static",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


INTERNAL_IPS = [
    "127.0.0.1",
]

# TailwindCSS settings

if DEBUG:
    NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"  

TAILWIND_APP_NAME = 'theme'

#Email settings
if os.getenv('RENDER') == 'true':  # Check if running on Render
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_HOST_USER = env('MY_EMAIL')
EMAIL_HOST_PASSWORD = env('EMAIL_PASSWORD')

DEFAULT_FROM_EMAIL = env('MY_EMAIL')

EMAIL_TIMEOUT = 30

ADMINS = [('Admin', env('MY_EMAIL'))]  # List of admin email addresses

#Logging settings

import boto3
boto3.set_stream_logger(name="boto3", level=logging.DEBUG)

logging.basicConfig(level=logging.DEBUG)

if os.getenv('RENDER') == 'true':
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
                'level': 'WARNING',  # Change to WARNING to reduce verbosity
                'propagate': False,
            },
            'botocore': {
                'handlers': ['console'],
                'level': 'WARNING',  # Change to WARNING to reduce verbosity
                'propagate': False,
            },
        },
    }
else:
    import boto3
    boto3.set_stream_logger(name="boto3", level=logging.DEBUG)

    logging.basicConfig(level=logging.DEBUG)

    LOGGING = {
        'version': 1,
        "disable_existing_loggers": False,
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',  # Log errors only
                'class': 'django.utils.log.AdminEmailHandler',
            },
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": "file_uploads.log",
                "formatter": "detailed",
            },
             'console': {
                'level': 'INFO',  # Set to INFO to reduce verbosity
                'class': 'logging.StreamHandler',
            },
        },
        'formatters': {
            "detailed": {
                "format": "{asctime} {levelname} {name} {message}",
                "style": "{",
            },
        },
        'loggers': {
            'django': {
                'handlers': ['mail_admins', 'file'],
                'level': 'ERROR',  # Only send error-level logs to admins
                'propagate': True,
            },
            "boto3": {  # Logs B2 API calls
                "handlers": ["file"],
                "level": "DEBUG",
                "propagate": False,
            },
            "storages.backends.s3boto3": {  # Logs django-storages operations
                "handlers": ["file"],
                "level": "DEBUG",
                "propagate": False,
            },
            'django.utils.autoreload': {
                'handlers': ['console'],
                'level': 'INFO',  # Set to INFO to reduce verbosity
                'propagate': False,
            },
        },
    }


