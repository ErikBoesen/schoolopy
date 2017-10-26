import random
import time
import yaml
import requests_oauthlib
import json
from urllib import parse
import requests

class SchoologyAuth:
    def __init__(self, consumer_key, consumer_secret, user_id=None):
        self.API_ROOT = 'https://api.schoology.com/v1'
        self.DOMAIN_ROOT = 'https://fccps.schoology.com'

        self.user_id = user_id
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        self.oauth = requests_oauthlib.OAuth1Session(self.consumer_key, self.consumer_secret)

        if user_id != None:
            with open('auth.yml', 'r+') as f:
                self.config = yaml.load(f)
                self.request_token = self.config['request_token']
                self.request_token_secret = self.config['request_token_secret']
                try:
                    self.access_token = self.config[self.user_id]['access_token']
                except KeyError:
                    self.config[self.user_id]['access_token'] = ''
                    self.config[self.user_id]['access_token_secret'] = ''
                    yaml.dump(self.config, f, default_flow_style=False)
                    self.access_token = self.config[self.user_id]['access_token']
                self.access_token_secret = self.config[self.user_id]['access_token_secret']
            self.authenticateOAuth()

    def _oauth_header(self):
            auth = 'OAuth realm="Schoology API",'
            auth += 'oauth_consumer_key="%s",' % self.consumer_key
            auth += 'oauth_token="%s",' % ('' if self.access_token == None else self.access_token)
            auth += 'oauth_nonce="%s",' % ''.join([str(random.randint(0, 9)) for i in range(8)])
            auth += 'oauth_timestamp="%d",' % time.time()
            auth += 'oauth_signature_method="PLAINTEXT",'
            auth += 'oauth_version="1.0",'
            auth += 'oauth_signature="%s%%26%s"' % (self.consumer_secret, '' if self.access_token_secret == None or self.access_token_secret == '' else self.access_token_secret)
            return auth

    def _request_header(self):
        header = {
            'Authorization': self._oauth_header(),
            'Accept': 'application/json',
            'Host': 'api.schoology.com',
            'Content-Type': 'application/json'
        }
        return header

    def saveAccessTokens(self, uid, oauth_token, oauth_token_secret):
        self.config[uid]['access_token'] = oauth_token
        self.config[uid]['access_token_secret'] = oauth_token_secret
        with open('auth.yml', 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)

    def saveRequestTokens(self, uid, request_token, request_token_secret):
        self.config['request_token'] = request_token
        self.config['request_token_secret'] = request_token_secret
        with open('auth.yml', 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)

    def loadRequestTokens(self):
        return {'request_token': self.config['request_token'],
                'request_token_secret': self.config['request_token_secret']}

    def loadAccessTokens(self, uid):
        return {'access_token': self.config[uid]['access_token'],
                'access_token_secret': self.config[uid]['access_token_secret']}

    def removeAccessTokens(self, uid):
        self.config[uid]['access_token'] = ''
        self.config[uid]['access_token_secret'] = ''
        with open('auth.yml', 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)

    def authenticateOAuth(self):
        if self.access_token != None:
            r = self.oauth.get(url=self.API_ROOT + '/users/me', headers=self._request_header())
            if r.status_code > 400:
                self.removeAccessTokens(self.user_id)
                self.access_token = ''
                self.access_token_secret = ''
                self.authenticateOAuth()
                return
            return
        if self.request_token == None:
            request_token_url = self.API_ROOT + '/oauth/request_token'
            fetch_response = self._fetch_token(request_token_url, self.oauth)


            self.request_token = fetch_response.get('oauth_token')
            self.request_token_secret = fetch_response.get('oauth_token_secret')
            self.saveRequestTokens(self.request_token, self.request_token_secret)
            base_authorization_url = self.DOMAIN_ROOT + '/oauth/authorize'

            authorization_url = self.oauth.authorization_url(base_authorization_url)
            print('Please go here and authorize,', authorization_url + r'&oauth_callback=https%3A%2F%2Ffccps.schoology.com')
            redirect_response = input('Type any character here when done.')
            self.authenticateOAuth()
        else:
            if self.request_token != self.config['request_token']:
                raise yaml.MarkedYAMLError
        access_token_url = self.API_ROOT + '/oauth/access_token'

        oauth = requests_oauthlib.OAuth1Session(self.consumer_key,
                          self.consumer_secret,
                          resource_owner_key=self.request_token,
                          resource_owner_secret=self.request_token_secret)
        oauth_tokens = _fetch_token(access_token_url, oauth)
        self.access_token = oauth_tokens.get('oauth_token')
        self.access_token_secret = oauth_tokens.get('oauth_token_secret')
        self.saveAccessTokens(self.user_id, self.access_token, self.access_token_secret)

    def _fetch_token(self, url, oauth_session, **request_kwargs):
	    r = oauth_session.get(url, **request_kwargs)
	    if r.status_code >= 400:
		    error = "Token request failed with code %s, response was '%s'."
		    raise TokenRequestDenied(error % (r.status_code, r.text), r)

	    try:
		    token = dict(urldecode(r.text.strip()))
	    except ValueError as e:
		    error = ("Unable to decode token from token response. "
				 "This is commonly caused by an unsuccessful request where"
				 " a non urlencoded error message is returned. "
				 "The decoding error was %s""" % e)
		    raise ValueError(error)

	    oauth_session._populate_attributes(token)
	    return token
