# Regular Expression Quick Guide

# ^  Matches the "beggining" of a line
# $  Matches the "end" of a line
# .  Matches "any" character
# \s Matches "whitespace"
# \S Matches any "non-whitespace" character
# *  "Repeats" a character zero or more times
# *? "Repeats" a character zero or more times (non-greedy)
# +  "Repeats" a character one or more times
# +? "Repeats" a character one or more times (non-greedy)
# [aeiou]  Matches a single character in the listed "set"
# [^XYZ]   Matches a single character "not in" the listed "set"
# [a-z0-9] The set of characters can include a "range"
# (  Indicates where the string "extraction" is to start
# )  Indicates where the string "extraction" is to end


# Before use regular expression, we must import the library using "import re"
import re

# We can use re.search() to see if a string matches a regular expression (similar to find())

hand = open('mbox-short.txt')

# Using find
for line in hand:
  line = line.rstrip()
  # print(line.find('From:'))
  if line.find('From:') >= 0:
    print(line)

print('--- --- --- ')

hand.seek(0) # Reinicia el puntero, sino, quedaria al final

# Using regex
for line in hand:
  line = line.rstrip()
  # print(line.find('From:'))
  if re.search('From:', line):
    print(line)

# También en lugar de line.startswith('From:')
# podríamos utilizar re.search('^From:', line)

# ^X.*:
# Es igual a:
# ^ Buscara unicamente las lineas que 'al inicio de la linea' tengan una X
# . permite despues de la X cualquier caracter, el . es cualquier caracter
# * significa cero o mas veces, asi que permite cualquier caracter cero o mas veces
# : que haga match con 2 puntos
# entonces hace match con cada uno de los siguientes hasta los 2 puntos :
# X-Sieve: CMU Sieve 2.3
# X-DSPAM-Result: Innocent
# X-DSPAM-Confidence: 0.8475
# X-Content-Type-Message-Body: text/plain

# Aunque se podría mejorar por lo siguiente
# ^X\S+:
# A diferencia del anterior:
# \S filtra los que no sean espacios en blanco
# + filtra cero o mas veces
# Algo como lo siguiente no lo permitiria, y evitariamos un bug:
# X-Plane is behind schedule: two weeks

# We can use re.findall() to extract portions of a string that match our regular expression (similar to find() and slicing: var[5:10])

