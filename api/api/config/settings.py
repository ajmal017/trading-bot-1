"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path

# Django-environ: https://django-environ.readthedocs.io/en/latest/
import environ

env = environ.Env()

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = env("DJANGO_SECRET_KEY")

ENVIRONMENT = env("ENVIRONMENT", default="development")

DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = [
    '127.0.0.1',  # Required for Django Debug Toolbar
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Plugins
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'debug_toolbar',
    'django_celery_beat',
    'celery',
    # My apps
    'api.core',
    'api.users',
    'api.assets'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Plugins
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # My middleware
]

ROOT_URLCONF = 'api.config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'api.config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# POSTGRES_HOST_AUTH_METHOD env is set as 'trust' for localhost development
# environment, and no password is required. Do not do this in production

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DB_NAME", default="tradingbot"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env.int("DB_PORT", default=5432),
        "USER": env("DB_USER", default="tradingbot"),
        "PASSWORD": env("DB_PASSWORD", default=""),
    }
}

# Rest framework configuration

REST_FRAMEWORK = {
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        'rest_framework.authentication.TokenAuthentication',
    ),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ),
}


# Authentication Settings
AUTH_USER_MODEL = "users.User"
ANONYMOUS_USER_NAME = None

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# Logging
# https://docs.djangoproject.com/en/3.1/topics/logging/

LOG_LEVEL = env("LOG_LEVEL", default="ERROR")

# Logging of request's body in development environment
LOG_REQUESTS = env.bool("LOG_REQUESTS", default=False)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    "formatters": {
        "standard": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"}
    },
    'handlers': {
        'file': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), 'debug.log'),
            'maxBytes': 1024*1024*10,  # 10 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard"
        }
    },
    'loggers': {
        "": {
            "level": LOG_LEVEL,
            "handlers": ['console'],
        },
        'django': {
            'level': "ERROR",
            'handlers': ['file'],
            'propagate': True,
        },
        "django.request": {
            "level": "DEBUG" if LOG_REQUESTS else "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# Celery settings
CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
