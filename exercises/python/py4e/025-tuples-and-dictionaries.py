# The items() method in dictionaries returns a list of (key, value) tuples


d = dict()
d['pcat'] = 2
d['pdog'] = 4

for (k, v) in d.items():
  print(k, v)

# Esto convierte el retorno del diccionario en una lista de tuplas
tups = d.items()
print('tups >>>:', tups)
