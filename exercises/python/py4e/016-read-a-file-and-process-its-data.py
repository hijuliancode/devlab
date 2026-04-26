# Assignment: Read a File and Process Its Data

# Write a program that prompts for a file name,
# then opens that file and reads through the file,
# looking for lines of the form:
# X-DSPAM-Confidence:    0.8475
# Count these lines and extract the floating point values
# from each of the lines and compute the average of those values
# and produce an output as shown below.
# Do not use the sum() function or a variable named sum in your solution.

# You can download the sample data at http://www.py4e.com/code3/mbox-short.txt when you are testing below enter mbox-short.txt as the file name.

fname = input('Enter file name:')
try:
  fh = open(fname)
except:
  print('Sorry, we cant found a file with the name: ', fname)
  quit()

counter = 0
total = 0
average = 0

for line in fh:
  if not line.startswith('X-DSPAM-Confidence:'):
    continue

  counter += 1

  idx = line.find(':')
  number = float(line[idx + 1:].strip())
  total += number

if counter > 0:
  average = total / counter

print(f'Average spam confidence: {average}')
