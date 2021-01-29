import os

from django.core.exceptions import ImproperlyConfigured


# Singleton used for no data being given to getenv. Required because `None` may
# be a valid default.
class _notset(object):
    pass


def getenv(var_name, default=_notset, split=False):
    """ Get an environment variable for Django settings """
    val = os.environ.get(var_name, default)

    if val is _notset:
        err = 'Missing required environment variable: {}'.format(var_name)
        raise ImproperlyConfigured(err)

    # Optionally support interpreting comma-separated values as a list.
    if split and isinstance(val, str):
        return val.split(',')

    return val
