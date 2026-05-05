import re

text = "My 2 favorite numbers are 19 and 42"

result = re.findall('[0-9]+', text)

print(result)