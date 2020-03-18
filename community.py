try:
    from django.conf import settings
except ImportError:
    pass
from . import constants
import requests
import warnings


class Community(object):
    def __init__(self):
        pass
