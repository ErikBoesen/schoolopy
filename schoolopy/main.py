import requests
import time
import random

class Schoology:
    key = ''
    secret = ''

    def _nonce(length=8):
        return ''.join([str(random.randint(0, 9)) for i in range(length)])

    def _oauth_header():
        # TODO: Improve formatting here
        auth = 'OAuth realm="Schoology API",'
        auth += 'oauth_consumer_key="%s",' % key
        auth += 'oauth_token="",'
        auth += 'oauth_nonce="%s",' % nonce()
        auth += 'oauth_timestamp="%d",' % time.time()
        auth += 'oauth_signature_method="PLAINTEXT",'
        auth += 'oauth_version="1.0",'
        auth += 'oauth_signature="%s%%26"' % secret

    def _request(path):
        # FIXME: Returns encoded XML, obviously not final
        return requests.get('https://api.schoology.com/v1/messages/inbox', headers={'Authorization': auth, 'Accept': 'text/xml;q=1.0,application/json;q=0.0;application/php;q=0.0', 'Host': 'api.schoology.com', 'Content-Type': 'text/xml'}).content
