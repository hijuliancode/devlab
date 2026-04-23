# Write a program that prompts for a file name,
# then opens that file and reads through the file,
# and print the contents of the file in upper case.
# Use the file words.txt to produce the output below.

fname = input('Enter file name: ')

try:
  fh = open(fname)
except:
  print('Sorry, we can\'t find a file with the name:', fname)

for line in fh:
  line = line.upper().rstrip()
  print(line)