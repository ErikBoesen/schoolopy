from .models import *
import requests
import time
import random
import json
from xml.etree.ElementTree import fromstring


class Schoology:
    key = ''
    secret = ''

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def _oauth_header(self):
        auth = 'OAuth realm="Schoology API",'
        auth += 'oauth_consumer_key="%s",' % self.key
        auth += 'oauth_token="",'
        auth += 'oauth_nonce="%s",' % ''.join([str(random.randint(0, 9)) for i in range(8)])
        auth += 'oauth_timestamp="%d",' % time.time()
        auth += 'oauth_signature_method="PLAINTEXT",'
        auth += 'oauth_version="1.0",'
        auth += 'oauth_signature="%s%%26"' % self.secret
        return auth

    def _get(self, path):
        #return fromstring(requests.get('https://api.schoology.com/v1/%s' % path, headers={'Authorization': self._oauth_header()}).content.decode())
        return json.loads(requests.get('https://api.schoology.com/v1/%s' % path, headers={'Authorization': self._oauth_header()}).content.decode())

    def messages(self):
        return [Message(raw) for raw in self._get('messages/inbox')['message']]

    def 
