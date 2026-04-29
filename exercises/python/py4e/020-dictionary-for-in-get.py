# When we encounter a new name, we need to add a new entry
# in the dictionary and if is the second or later time we
# have seen the name, we simply add one to the count in 
# the dictionary under that name

counts = dict()
# names = ['ana', 'luis', 'maria', 'carlos', 'ana', 'sofia', 'diego', 'maria', 'valentina', 'andres', 'camila', 'juan', 'luis', 'laura', 'mateo', 'ana', 'daniela', 'sebastian', 'paula', 'felipe', 'isabella', 'nicolas', 'gabriela', 'alejandro', 'lucia', 'manuel', 'elena', 'jorge', 'renata', 'tomas', 'adriana', 'pablo', 'veronica', 'emilio', 'maria', 'carlos', 'sofia']
names = ['valentina', 'ana', 'luis', 'valentina', 'maria', 'luis', 'ana', 'valentina']

for name in names:
    if name not in counts:
        counts[name] = 1
    else:
        counts[name] = counts[name] + 1

# print(counts)


# using GET

# We can use get() and provide a default value of zero when the key
# is not yet in the dictionary, and then just add one

count2 = dict()

for name in names:
    count2[name] = count2.get(name, 0) + 1

print(count2) # {'valentina': 3, 'ana': 2, 'luis': 2, 'maria': 1}