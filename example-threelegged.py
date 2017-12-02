import schoolopy
import yaml
import webbrowser as wb

with open('example_config.yml', 'r') as f:
    cfg = yaml.load(f)

# Instantiate with 'three_legged' set to True for three_legged oauth.
# Make sure to replace 'https://www.schoology.com' with your school's domain.
DOMAIN = 'https://www.schoology.com'

auth = schoolopy.SchoologyAuth(cfg['key'], cfg['secret'], three_legged=True, domain=DOMAIN)
# Request authorization URL to open in another window.
url = auth.request_authorization()

# Open OAuth authorization webpage. Give time to authorize.
if url is not None:
    wb.open(url, new=2)

# Wait for user to accept or deny the request.
input('Press enter when ready.')

# Authorize the SchoologyAuth instance as the user has either accepted or not accepted the request.
# Returns False if failed.

if not auth.authorize():
    raise SystemExit('Account was not authorized.')

# Create a Schoology instance with SchoologyAuth as a parameter.
sc = schoolopy.Schoology(auth)
sc.limit = 10  # Only retrieve 10 objects max

print('Your name is %s' % sc.get_me().name_display)
for update in sc.get_feed():
    user = sc.get_user(update.uid)
    print('By: ' + user.name_display)
    print(update.body[:40].replace('\r\n', ' ').replace('\n', ' ') + '...')
    print('%d likes\n' % update.likes)
