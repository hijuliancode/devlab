# Tuples
# Unlinke a list, once we create a tuple, we 'cannot alter' its
# contents - similar to a string

# Tuples are more efficent 

l = list()
print( dir(l) ) # ['append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']

print('\n--- --- --- \n')

t = tuple()
print( dir(t) ) # ['count', 'index']

print('\n\n\n')

# --- Tuples and assigment ---

(j, v) = ('Julian', 'Valentina')
print(v)

(a, b) = (2, 17)
print(a, b)

# Tuplas son comparables de manera lexicográfica,
# igual que los strings: se comparan elemento por elemento
# de izquierda a derecha, y la comparación termina en cuanto
# un par de elementos es diferente.

# Cuando dos elementos son identicos, pasa al siguiente

# 0 < 5, la comparación termina aquí: True
print( (0, 1, 2) < (5, 2, 1) )

# Primer elemento igual (0 == 0), se pasa al segundo: 1 < 3, termina aquí: True
print( (0, 1, 200000) < (0, 3, 4) )

# Con strings funciona igual, usando orden alfabético (basado en ASCII/Unicode).
# 'Jones' == 'Jones', se pasa al segundo: 'Sally' < 'Sam' (compara 'a' vs 'a', luego 'l' vs 'm'): True
print( ('Jones', 'Sally') < ('Jones', 'Sam') )

# 'Jones' > 'Adams' (compara 'J' vs 'A'): True
print( ('Jones', 'Sally') > ('Adams', 'Sam') )