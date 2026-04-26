# Slicing Strings
# - The second number is one beyond the end of the slice - "up to but no including"
# - If the second number is beyond the end of the string, it stops at the end of the string without an error

text = 'Monty Python'

print(text[0:4])  # 'Mont'
print(text[6:7])  # 'P'
print(text[6:20]) # 'Python'

# - If we leave off the first number or the second number,
# it is assumed to be the beginning or end of the string respectively

print(text[:2]) # 'Mo'
print(text[8:]) # 'thon'
print(text[:])  # 'Monty Python' - the whole string