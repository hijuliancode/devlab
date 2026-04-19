data = 'From stephen.marquard@utc.ac.za Sat Jan  5 09:14:16 2008'

atpos = data.find('@')
print(atpos)

sppos = data.find(' ', atpos)
print(sppos)

host = data[atpos + 1 : sppos]
print(host)

# The core idea is to delimit a target substring by locating its start and end boundaries,
# then extract it via index-based slicing.
# In this example, we identify the email host by finding the '@' symbol as the starting point
