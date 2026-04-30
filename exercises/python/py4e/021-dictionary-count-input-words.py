count = dict()

line = input('Enter your text: ')
# input: the clown ran after the car and the car ran into the tent and the tent fell down on the clown and the car

words = line.split()

print('Counting...')

for word in words:
  count[word] = count.get(word, 0) + 1

print(count)