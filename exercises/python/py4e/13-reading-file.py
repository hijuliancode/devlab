handle = open('mrrobot.txt')

# Read as a single line of characters
# inp = handle.read()


# Show text conditionally
# for line in handle:
#   if line.startswith('From:'):
#     print(line)


# Remove unnecesary newline
# for line in handle:
#   line = line.rstrip()
#   print(line)


# Skip a line conveniently
for line in handle:
  line = line.rstrip()
  if not line.startswith('From:'):
    continue
  print(line)