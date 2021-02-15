# flake8: noqa #F403

from .helper import getenv

ENVIRONMENT = getenv('DJANGO_ENVIRONMENT', 'local')

if ENVIRONMENT == 'minimal':
    from .minimal import *
else:
    from .standard import *
