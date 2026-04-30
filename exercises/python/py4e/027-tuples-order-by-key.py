# We can take advantage of the ability to sort a list of tuples
# to get a sorted version of a dictionary

d = { 'a': 10, 'c': 22, 'b': 1 }

# We can do this even more directly using the built-in function sorted
# that takes a sequence as paramether and returns a sorted sequence

for k, v in sorted(d.items()):
  print(k, v)