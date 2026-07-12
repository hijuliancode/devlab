# 1. Leer documento
# 2. Crear lista de numeros vacia
# 3. definir un patron para encontrar las lineas de confianza
# 4. iterar a traves de cada linea, filtrando las que coinciden con el patron
# 5. Si coincide, el numero lo agregare a la nusta de numeros
# 6. En una funcion de encontrarPromedio hago lo siguiente (no es necesario metodo en este ejecicio)
# 7. Se recorren los valores sumando todos en un total (python tiene sum no es necesario recorrer)
# 8. Se dividen por el total de la lista
# 9. Retorna este valor

import re

numbers = []

with open('mbox-short.txt') as mbox_file:
  for line in mbox_file:
    line = line.rstrip()
    matches = re.findall(r'X-DSPAM-Confidence: ([0-9]+\.[0-9]+)', line)
    
    if matches:
      numbers.append(float(matches[0]))

  average = sum(numbers) / len(numbers)

  print(f'Cantidad de valores: {len(numbers)}')
  print(f'Promedio de la confianza: {average}')