
counts = { 'chuck': 1, 'fred': 42, "jan": 100, "valentina": 17 }

for key in counts:
  print(key, counts[key])

print('---')

for aaa, bbb in counts.items(): # Retorna una tupla
  # aaa is the key, bbb is the value
  print(aaa, bbb)