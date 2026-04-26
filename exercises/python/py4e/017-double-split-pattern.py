words = 'From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008'

# Split
lines = words.split()

email = lines[1]

# Double Split 👻
pieces = email.split('@')

username = pieces[0]
email_provider = pieces[1]

print('words :', words)
print('lines :', lines)
print('email :', email)
print('pieces :', pieces)

print('username :', username)
print('email_provider :', email_provider)
