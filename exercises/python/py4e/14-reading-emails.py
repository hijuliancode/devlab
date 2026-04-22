
# Reading and filter lines

# fname = open('emails.txt')

# for line in fhand:
#   line = line.rstrip()
#   if not 'From: ' in line:
#     continue
#   print(line)

fname = input('Enter the file name: ')

try: 
  fhand = open(fname)
except:
  print('File cannot be opened:', fname)
  quit()  

count = 0

for line in fhand:
  if line.startswith('Subject: '):
    count = count + 1

print('There were', count, 'subject lines in', fname)