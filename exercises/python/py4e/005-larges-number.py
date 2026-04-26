
numbers = [-3, -41, -12, -9, -74, -15, -116]

largest = float('-inf')

for number in numbers:
  if number > largest:
    largest = number

print(largest)