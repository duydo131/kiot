from .base import *

import os
import logging

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '3@6wj-kujdan+1^cr@$53xiox1=m*!!smls%i-zo2f-ob8r*v6')
ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'kiot_management'),
        'HOST': os.environ.get('DB_HOST', '0.0.0.0'),
        'USER': os.environ.get('DB_USER', 'dev'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'secret'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}

DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"

BLOCK_QUANTITY_PRODUCT = 10
IGNORE_QUANTITY_PRODUCT = 10
BLOCK_DAY = 5
IGNORE_DAY = 5
PRICE_REGISTER_TERMINAL = 100000
PRICE_EXTEND_TERMINAL = 10000
PRICE_PER_BLOCK_PRODUCT = 5000
PRICE_PER_DAY = 2000

PER_CENT_ORDER = 1
CEILING_PRICE = 5000


EXCEL_TEMPLATE_DIR = os.path.join(os.path.dirname(BASE_DIR), "template")
IMPORT_PRODUCT_TEMPLATE = os.path.join(
    EXCEL_TEMPLATE_DIR, "Add_Product_Form.xlsx"
)

USE_LOCAL_WORKBOOK = False

FILE_URL = 'http://0.0.0.0:8080'

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {name} {pathname} {lineno:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'verbose'
        },
        'consumer': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        's6': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'verbose',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'apps': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'propagate': False,
        },
        # 'django.db.backends': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        #     'propagate': False,
        # }
   },
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}
