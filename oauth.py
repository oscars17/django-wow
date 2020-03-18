try:
    from django.conf import settings
except ImportError:
    pass
from requests_oauthlib import OAuth2Session
from . import constants


class BattleNetOAuth(object):
    def __init__(self, key=None, secret=None, region=None, redirect_uri=None, access_token=None):
        if key:
            self.BNET_KEY = key
        else:
            try:
                self.BNET_KEY = settings.BNET_KEY
            except (ImportError, AttributeError):
                raise ValueError('Battle.net client key is not found.')

        if secret:
            self.BNET_SECRET = secret
        else:
            try:
                self.BNET_SECRET = settings.BNET_SECRET
            except (AttributeError, ImportError):
                pass
        region = region.upper()

        if region in constants.AVAILABLE_REGIONS:
            self.region = region
        else:
            raise ValueError("Invalid Region provided.  Region must be one of 'us', 'eu', 'kr', or 'tw'.")
        if redirect_uri:
            self.BNET_REDIRECT_URI = redirect_uri
        else:
            try:
                self.BNET_REDIRECT_URI = settings.BNET_REDIRECT_URI
            except (AttributeError, ImportError):
                raise ValueError('Redirect URI is not found.')
        self.scope = 'wow.profile'
        self.access_token = None
        self.oauth = None
        if access_token:
            self._set_access_token(access_token)

    def _set_access_token(self, token, token_type='bearer'):
        self.access_token = token
        if not self.oauth:
            self.oauth = OAuth2Session(
                self.BNET_KEY, redirect_uri=self, token={'access_token': token, 'token_type': token_type}
            )
        else:
            self.oauth.token = token

    def _make_request(self):
        if not self.access_token:
            raise ValueError('No access token available')

    def get_access_token(self):
        pass
