import schoolopy
import yaml

with open('example_config.yml', 'r') as f:
    cfg = yaml.load(f)

sc = schoolopy.Schoology(cfg['key'], cfg['secret'])

print('Most recent message:')
print(sc.get_messages()[0])

print('Your schools:')
schools = sc.get_schools()
print(schools)

print('Your first school:')
print(sc.get_school(schools[0].id))

print('Your school\'s buildings:')
print(sc.get_buildings(schools[0].id))

print('The first user:')
users = sc.get_users()
print(users[0])

print('The first user (fetched by ID):')
print(sc.get_user(users[0].id))

print('First group:')
print(sc.get_groups())
