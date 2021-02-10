import os
from urllib.parse import urlsplit

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


def netloc(url):
    """ Strip the scheme (http, https) from a URL """
<<<<<<< HEAD
    split = urllib.parse.urlsplit(url)
=======
    split = urlsplit(url)
>>>>>>> 52a5d26aa186a2832a6a779bd24f5f13313e588f

    # If we have a scheme, urlparse will get this right
    if split.scheme:
        return split.netloc

    # Otherwise, manually make sure to get rid of any trailing path components
    url = url.split('/')[0]
    url = url.split('?')[0]
    url = url.split('#')[0]

    return url
