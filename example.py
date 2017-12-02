import schoolopy
import yaml
import webbrowser as wb
import time

with open('example_config.yml', 'r') as f:
    cfg = yaml.load(f)

# Instantiate with 'three_legged' set to True for three_legged oauth.
# Make sure to REPLACE 'https://www.schoology.com' with your school's domain.
auth = schoolopy.SchoologyAuth(cfg['key'], cfg['secret'], three_legged=True, domain='https://www.schoology.com')
url = auth.request_authorization() # Request authorization URL to open in another window.

# Open oauth authorization webpage. Give time to authorize.
if url != None:
    wb.open(url, new=2)

# Wait for user to accept or deny the request.
input('Press enter when ready.')

# Authorize the SchoologyAuth instance as the user has either accepted or not accepted the request.
# Returns False if failed.

if not auth.authorize():
    raise SystemExit("Account was not authorized.")

request_token = auth.request_token
request_token_secret = auth.request_token_secret

access_token = auth.access_token
access_token_secret = auth.access_token_secret

# Store previous variables somewhere for later use. Can be applied in SchoologyAuth constructor.

# Create a Schoology instance with SchoologyAuth as a parameter.
sc = schoolopy.Schoology(auth)
sc.limit = 10  # Only retrieve 10 objects max

print(sc.get_group(1372119245))
print(sc.get_me())
for update in sc.get_feed():
    user = sc.get_user(update.uid)
    print('By: ' + user.name_display)
    print(update.body[:40].replace('\r\n', ' ').replace('\n', ' ') + '...')
    print('%d likes\n' % update.likes)
