# Contar la frecuencia de cada palabra en un archivo de texto
# y mostrar las 10 más comunes, ordenadas de mayor a menor.
fhand = open('words.txt')
counts = dict()

# Recorremos cada línea y cada palabra, acumulando el conteo.
# counts.get(word, 0) evita KeyError: si la palabra no existe aún, retorna 0.
for line in fhand:
  words = line.split()
  for word in words:
    counts[word] = counts.get(word, 0) + 1

print(f"counts: {counts}")
print(' \n --- --- --- \n ')

# Convertimos el diccionario a lista de tuplas (val, key) en lugar de (key, val).
# Ese orden invertido nos permite usar sorted() para ordenar por frecuencia,
# ya que la comparación lexicográfica empieza por el primer elemento de la tupla.
lst = list()
for key, val in counts.items():
  newtup = (val, key)
  lst.append( newtup )

# Ordenamos de mayor a menor frecuencia.
lst = sorted(lst, reverse=True)

# Imprimimos solo las 10 palabras más frecuentes.
# Hacemos slicing [:10] antes de iterar para no recorrer toda la lista.
# Al desestructurar (val, key), imprimimos en orden legible: palabra y conteo.
for val, key in lst[:10]:
  print(key, val)
