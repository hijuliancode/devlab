# 9.4 Write a program to read through the mbox-short.txt
# and figure out who has sent the greatest number of mail messages.
# The program looks for 'From ' lines and takes the second word of
# those lines as the person who sent the mail.
# The program creates a Python dictionary that maps the
# sender's mail address to a count of the number of times
# they appear in the file. After the dictionary is produced,
# the program reads through the dictionary using a maximum
# loop to find the most prolific committer.

# output:
# cwen@iupui.edu 5

name = input("Enter file: ")

if len(name) < 1:
    name = "mbox-short.txt"

handle = open(name)
counts = dict()

top_sender = None
top_count = None

for line in handle:
    if not line.startswith('From '):
        continue
    sender = line.split()[1]
    counts[sender] = counts.get(sender, 0) + 1

for sender, count in counts.items():
    if top_sender == None or count > top_count:
        top_sender = sender
        top_count = count

print(top_sender, top_count)