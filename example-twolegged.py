import schoolopy
import yaml

with open('example_config.yml', 'r') as f:
    cfg = yaml.load(f)

# Instantiate with 'three_legged' set to True for three_legged oauth.
# Make sure to replace 'https://www.schoology.com' with your school's domain.
DOMAIN = 'https://www.schoology.com'

auth = schoolopy.SchoologyAuth(cfg['key'], cfg['secret'])
sc = schoolopy.Schoology(auth)
sc.limit = 10  # Only retrieve 10 objects max

print('Your name is %s' % sc.get_me().name_display)
for update in sc.get_feed():
    user = sc.get_user(update.uid)
    print('By: ' + user.name_display)
    print(update.body[:40].replace('\r\n', ' ').replace('\n', ' ') + '...')
    print('%d likes\n' % update.likes)
