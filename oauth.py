try:
    from django.conf import settings
except ImportError:
    pass
from requests_oauthlib import OAuth2Session
from . import constants
from . import error_messages


class BattleNetOAuth(object):

    def __init__(self, version=None, key=None, secret=None, region=None, redirect_uri=None, access_token=None):
        if version:
            try:
                self.namespace = constants.NAMESPACES[version]
            except KeyError:
                raise ValueError(error_messages.NAMESPACES)
        else:
            self.namespace = constants.NAMESPACES['retail']
        if key:
            self.BNET_KEY = key
        else:
            try:
                self.BNET_KEY = settings.BNET_KEY
            except (ImportError, AttributeError):
                raise ValueError(error_messages.BNET_KEY)

        if secret:
            self.BNET_SECRET = secret
        else:
            try:
                self.BNET_SECRET = settings.BNET_SECRET
            except (AttributeError, ImportError):
                raise ValueError(error_messages.BNET_SECRET)
        region = region.upper()

        if region in constants.AVAILABLE_REGIONS:
            self.region = region
        else:
            raise ValueError(error_messages.AVAILABLE_REGION)
        if redirect_uri:
            self.BNET_REDIRECT_URI = redirect_uri
        else:
            try:
                self.BNET_REDIRECT_URI = settings.BNET_REDIRECT_URI
            except (AttributeError, ImportError):
                raise ValueError(error_messages.BNET_REDIRECT_URI_ERROR)
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

    def get_authorization_url(self):
        if not self.BNET_REDIRECT_URI:
            raise ValueError(error_messages.BNET_REDIRECT_URI_ERROR)
        if not self.BNET_KEY:
            raise ValueError(error_messages.BNET_KEY)
        self.oauth = OAuth2Session(self.BNET_KEY, redirect_uri=self.BNET_REDIRECT_URI, scope=self.scope)
        auth_url, state = self.oauth.autorization_url(constants.BNET_AUTH_URL)
        return auth_url, state

    def get_access_token(self, access_code):
        pass
