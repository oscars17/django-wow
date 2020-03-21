
try:
    from django.conf import settings
except ImportError:
    pass
from django_wow.oauth2 import BattleNetOAuth2
from . import error_messages


class Community(object):
    def __init__(self, key):
        if key:
            self.BNET_KEY = key
        else:
            try:
                self.BNET_KEY = settings.BNET_KEY
            except (AttributeError, ImportError):
                raise ValueError(error_messages.BNET_KEY)

    def get(self):
        pass