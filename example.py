import schoolopy
import yaml
import webbrowser as wb
import time

with open('examplee_config.yml', 'r') as f:
    cfg = yaml.load(f)

# Instantiate with a user id for 3-legged-oauth.
auth = schoolopy.SchoologyAuth(cfg['key'], cfg['secret'], user_id=7351247)
url = auth.request_authorization() # Request authorization URL to open in another window.

# Open oauth authorization webpage. Give time to authorize.
wb.open(url, new=1)
time.sleep(seconds=30)

# Authorize the SchoologyAuth instance as the user has either accepted or not accepted the request.
auth.authorize()

# Create a Schoology instance with SchoologyAuth as a parameter.
sc = schoolopy.Schoology(auth)
sc.limit = 10  # Only retrieve 10 objects max

for update in sc.get_feed():
    user = sc.get_user(update.uid)
    print('By: ' + user.name_display)
    print(update.body[:40].replace('\r\n', ' ').replace('\n', ' ') + '...')
    print('%d likes\n' % update.likes)
