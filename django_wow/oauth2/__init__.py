try:
    from django.conf import settings
except ImportError:
    pass
from requests_oauthlib import OAuth2Session
from django_wow import constants
from . import error_messages
from . import account_urls
import functools


def check_access_token(f):
    @functools.wraps(f)
    def wrapper(self, *args):
        token = args[0]
        if token:
            self._set_access_token(token)
            return f(self, *args)
        else:
            raise ValueError('Access token is not set')
    return wrapper


class BattleNetOAuth2(object):

    def __init__(self, version=None, key=None, secret=None, region=None, redirect_uri=None, access_token=None):
        self.current_namespace = None
        if version:
            try:
                self.namespace_dict = constants.NAMESPACES[version]
            except KeyError:
                raise ValueError(error_messages.NAMESPACES)
        else:
            self.namespace_dict = constants.NAMESPACES['retail']
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
        if region:
            region = region.upper()
        else:
            region = 'EU'
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
                raise ValueError(error_messages.BNET_REDIRECT_URI)
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

    def _make_request(self, endpoint, base_url=None):
        if not self.access_token:
            raise ValueError('No access token available.')
        if not self.oauth:
            self.oauth = OAuth2Session(
                self.BNET_KEY, redirect_uri=self.BNET_REDIRECT_URI)
        if not base_url:
            base_url = constants.BASE_ENDPOINT_URL
        url = base_url % self.region + endpoint[1:]
        r = self.oauth.get(url)
        self.current_namespace = None
        if r.status_code == 200:
            return r.status_code, r.json()
        else:
            return r.status_code, []

    def get_authorization_url(self):
        if not self.BNET_REDIRECT_URI:
            raise ValueError(error_messages.BNET_REDIRECT_URI)
        if not self.BNET_KEY:
            raise ValueError(error_messages.BNET_KEY)
        self.oauth = OAuth2Session(self.BNET_KEY, redirect_uri=self.BNET_REDIRECT_URI, scope=self.scope)
        auth_url, state = self.oauth.authorization_url(constants.BNET_AUTH_URL % (self.region))
        return auth_url, state

    def retrieve_access_token(self, access_code):
        if not access_code:
            raise ValueError(error_messages.ACCESS_CODE)
        if not self.BNET_SECRET:
            raise ValueError(error_messages.BNET_SECRET)

        if not self.BNET_REDIRECT_URI:
            raise ValueError(error_messages.BNET_REDIRECT_URI)
        self.oauth = OAuth2Session(
            self.BNET_KEY, redirect_uri=self.BNET_REDIRECT_URI, scope='wow.profile')
        token_data = self.oauth.fetch_token(
            constants.BNET_TOKEN_URL % self.region,
            code=access_code,
            client_secret=self.BNET_SECRET)
        self.access_token = token_data['access_token']
        return token_data

    @check_access_token
    def get_user_info(self, access_token=None):
        return self._make_request(account_urls.user_info_url)

    @check_access_token
    def check_token(self, access_token=None):
        return self._make_request(account_urls.check_token_url)
