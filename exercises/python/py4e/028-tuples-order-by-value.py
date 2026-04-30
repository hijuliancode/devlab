# Ordenar un diccionario por valores en lugar de por llaves

# Python no puede ordenar diccionarios directamente por valor,
# pero podemos aprovechar que las listas de tuplas son comparables
# y ordenables.

# La clave: invertir el orden (value, key) en lugar de (key, value),
# así sorted() compara primero por valor.

d = { 'a': 10, 'c': 22, 'b': 1 }
tmp = list()

# Construimos la lista de tuplas con (value, key)
for k, v in d.items():
    tmp.append( (v, k) )

print(tmp)  # [(10, 'a'), (22, 'c'), (1, 'b')]

tmp = sorted( tmp, reverse=True )
print(tmp)  # [(22, 'c'), (10, 'a'), (1, 'b')] -> descendente

tmp = sorted( tmp, reverse=False )
print(tmp)  # [(1, 'b'), (10, 'a'), (22, 'c')] -> ascendente