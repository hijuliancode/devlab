
numbers = [3, 41, 12, 9, 74, -15, 116]

smallest = float('inf')

for number in numbers:
  if number < smallest:
    smallest = number

print("smallest", smallest)