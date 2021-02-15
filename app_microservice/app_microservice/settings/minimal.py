# flake8: noqa #F403 #E501
# Minimal configuration for doing static file collection

import os

from django.utils.crypto import get_random_string

from .base import BASE_DIR, INSTALLED_APPS, STATIC_URL

ENVIRONMENT = 'minimal'

DEBUG = False
DATABASES = {}
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# This key is one-time use while we generate the static files.  We don't
# necessarily want it to match the production key, since this container
# shouldn't ever be doing any security related work. We want that validation to
# fail.
SECRET_KEY = get_random_string(50)

# Google Cloud Project
GCP_PROJECT_ID = ''
GCP_BUCKET = ''
