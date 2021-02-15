# flake8: noqa #F403 #E501

from datetime import timedelta

from .base import *
from .helper import getenv

# Google Cloud Project
GCP_PROJECT_ID = getenv('GCP_PROJECT_ID')
GCP_BUCKET = getenv('GCP_BUCKET')

# Recommender Bot
RECOMMENDER_BOT_TOPIC = getenv('RECOMMENDER_BOT_TOPIC')
RECOMMENDER_BOT_TOKEN = getenv('RECOMMENDER_BOT_TOKEN')

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': getenv('DJANGO_DATABASE_NAME'),
        'USER': getenv('DJANGO_DATABASE_USER'),
        'PASSWORD': getenv('DJANGO_DATABASE_PASSWORD'),
        'HOST': getenv('DJANGO_DATABASE_HOST'),
        'PORT': getenv('DJANGO_DATABASE_PORT', None),
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 0,
        'OPTIONS': {
            'charset': 'utf8mb4'
        }
    }
}

# JWT
SECRET_KEY = getenv('DJANGO_SECRET_KEY')
ACCESS_TOKEN_LIFETIME_MINUTES = int(getenv('DJANGO_ACCESS_TOKEN_LIFETIME', 15))

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'AUTH_HEADER_TYPES': 'Bearer',
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'uuid',
    'USER_ID_CLAIM': 'sub',
    'AUTH_TOKEN_CLASSES': ['rest_framework_simplejwt.tokens.AccessToken'],
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Social Auth
GOOGLE_OAUTH_AUDIENCE = getenv('GOOGLE_OAUTH_AUDIENCE')

# Service Tokens can authenticate for access to certain endpoints. They're
# long-lived and used for machine-to-machine authorization.
SERVICE_TOKEN_WHITELIST = [
    RECOMMENDER_BOT_TOKEN,
]
