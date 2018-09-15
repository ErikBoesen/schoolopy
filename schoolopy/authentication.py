import random
import time
import requests_oauthlib
from requests_oauthlib.oauth1_session import TokenRequestDenied
from oauthlib.common import urldecode

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode



class AuthorizationError(Exception):
    """
    Called when an attempt is made to initialize a Schoology instance with
    an unauthorized Auth instance.
    """
    pass


class Auth:
    def __init__(self, consumer_key, consumer_secret, domain='https://www.schoology.com', three_legged=False,
                 request_token=None, request_token_secret=None, access_token=None, access_token_secret=None):
        self.API_ROOT = 'https://api.schoology.com/v1'
        self.DOMAIN_ROOT = domain

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        self.request_token = request_token
        self.request_token_secret = request_token_secret

        self.access_token = access_token
        self.access_token_secret = access_token_secret

        self.oauth = requests_oauthlib.OAuth1Session(self.consumer_key, self.consumer_secret)
        self.three_legged = three_legged

    def _oauth_header(self):
        auth  = 'OAuth realm="Schoology API",'
        auth += 'oauth_consumer_key="%s",' % self.consumer_key
        auth += 'oauth_token="%s",' % ('' if self.access_token is None else self.access_token)
        auth += 'oauth_nonce="%s",' % ''.join([str(random.randint(0, 9)) for i in range(8)])
        auth += 'oauth_timestamp="%d",' % time.time()
        auth += 'oauth_signature_method="PLAINTEXT",'
        auth += 'oauth_version="1.0",'
        auth += 'oauth_signature="%s%%26%s"' % (self.consumer_secret, self.access_token_secret if self.access_token_secret else '')
        return auth

    def _request_header(self):
        return {
            'Authorization': self._oauth_header(),
            'Accept': 'application/json',
            'Host': 'api.schoology.com',
            'Content-Type': 'application/json'
        }

    def request_authorization(self):
        if self.authorized:
            if not self.three_legged:
                return None
            r = self.oauth.get(url=self.API_ROOT + '/users/me', headers=self._request_header())
            if r.status_code > 400:
                self.access_token = None
                self.access_token_secret = None
            else:
                return None
        if not self.request_token and not self.request_token_secret:
            request_token_url = self.API_ROOT + '/oauth/request_token'
            fetch_response = self._fetch_token(request_token_url, self.oauth)

            self.request_token = fetch_response.get('oauth_token')
            self.request_token_secret = fetch_response.get('oauth_token_secret')

        base_authorization_url = self.DOMAIN_ROOT + '/oauth/authorize'
        return self.oauth.authorization_url(base_authorization_url, request_token=self.request_token) + '&' + urlencode({'oauth_callback': self.DOMAIN_ROOT})

    def authorize(self):
        if self.authorized or not self.three_legged:
            return True
        access_token_url = self.API_ROOT + '/oauth/access_token'
        self.oauth = requests_oauthlib.OAuth1Session(self.consumer_key,
                                                     self.consumer_secret,
                                                     resource_owner_key=self.request_token,
                                                     resource_owner_secret=self.request_token_secret)
        try:
            oauth_tokens = self._fetch_token(access_token_url, self.oauth)
        except TokenRequestDenied:
            return False
        self.access_token = oauth_tokens.get('oauth_token')
        self.access_token_secret = oauth_tokens.get('oauth_token_secret')
        return self.access_token is not None

    @property
    def authorized(self):
        if not self.three_legged:
            if self.consumer_key is not None and self.consumer_secret is not None:
                return True
            return False
        return self.access_token is not None and self.access_token_secret is not None

    def _fetch_token(self, url, oauth_session, **request_kwargs):
        r = oauth_session.get(url, **request_kwargs)
        if r.status_code >= 400:
            error = 'Token request failed with code %s, response was \'%s\'.'
            raise TokenRequestDenied(error % (r.status_code, r.text), r)
        try:
            token = dict(urldecode(r.text.strip()))
        except ValueError as e:
            raise ValueError('Unable to decode token from token response. This is commonly caused by an unsuccessful request where a non urlencoded error message is returned. The decoding error was %s' % e)

        oauth_session._populate_attributes(token)
        return token
