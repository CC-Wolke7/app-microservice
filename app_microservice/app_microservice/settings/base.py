"""
Django settings for app_microservice project.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

from .helper import getenv, netloc

# Build paths inside the project like this: os.path.join(BASE_DIR, "subdir")
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
# When Debug is enabled, Django will give detailed stack traces when there is
# an error. Should be disabled in production.
DEBUG = getenv('DJANGO_DEBUG', True)

ENVIRONMENT = getenv('DJANGO_ENVIRONMENT', 'local')

# Frontend (Ionic) and Backend (Django) URLs
BACKEND_API_URL = getenv('DJANGO_API_URL', 'http://localhost:8000')
FRONTEND_APP_URL = getenv('DJANGO_FRONTEND_URL', 'http://localhost:8100')

STATIC_URL = f'{BACKEND_API_URL}/static/'

# Only hosts which match this list are allowed to access the site when debug is
# disabled.
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'host.docker.internal',
    netloc(BACKEND_API_URL),
    netloc(FRONTEND_APP_URL),
]

# CORS
CORS_ORIGIN_WHITELIST = [
    FRONTEND_APP_URL,
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'corsheaders',
    'core.apps.CoreConfig',
    'rest_framework',
    'drf_yasg',
    'django_filters',
]

# The order of some of these middleware matters. For example,
# SecurityMiddleware should come first, and CorsMiddleware should be placed
# before any middleware which can generate a response (such as
# CommonMiddleware).
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# The entrypoint for the url mapping
ROOT_URLCONF = 'app_microservice.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

WSGI_APPLICATION = 'app_microservice.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],

    # Backends which are used to validate requests for signed-in users
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],

    # Backends to apply queryset filters to DRF requests
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa
    },
]

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']
AUTH_USER_MODEL = 'core.User'

# This is used to redirect logins for the API documentation views, which can be
# accessed with session-based authentication, but require the user be an admin
# (is_staff=True).
LOGIN_URL = '/internal/admin/login'

# Swagger settings are used by the auto-generated API documentation.
# https://drf-yasg.readthedocs.io/en/stable/security.html#security-definitions
SWAGGER_SETTINGS = {}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'CET'
USE_I18N = True
USE_L10N = True
USE_TZ = True
