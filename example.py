import schoolopy

key = ''
secret = ''

sc = schoolopy.Schoology(key, secret)

print('Most recent message:')
print(sc.messages()[0])
