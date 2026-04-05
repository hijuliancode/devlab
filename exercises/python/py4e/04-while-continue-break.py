print('Type \'quit\' to exit')
print('# at the beginning of a line to comment')
def ask():
	while True:
		line = input('> ')
		if line[0] == '#':
			continue
		if line == 'quit':
			break
		print(line)
	print('bye! ')

ask()
