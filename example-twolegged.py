import schoolopy
import yaml

with open('example_config.yml', 'r') as f:
    cfg = yaml.load(f)

sc = schoolopy.Schoology(schoolopy.Auth(cfg['key'], cfg['secret']))
sc.limit = 10  # Only retrieve 10 objects max

print('Your name is %s' % sc.get_me().name_display)
for update in sc.get_feed():
    user = sc.get_user(update.uid)
    print('By: ' + user.name_display)
    print(update.body[:40].replace('\r\n', ' ').replace('\n', ' ') + '...')
    print('%d likes\n' % update.likes)
