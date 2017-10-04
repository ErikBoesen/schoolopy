import schoolopy
import yaml


with open('example_config.yml', 'r') as f:
    cfg = yaml.load(f)

sc = schoolopy.Schoology(cfg['key'], cfg['secret'])

for update in sc.get_feed():
    user = sc.get_user(update.uid)
    print('By: ' + user.name_display)
    print(update.body[:40].replace('\r\n', ' ').replace('\n', ' ') + '...')
    print('%d likes\n' % update.likes)
