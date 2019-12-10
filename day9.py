import intcode

CC = intcode.read('day9.txt')

for i in [1, 2]:
	print('part', i)
	r = intcode.Runner(CC, [i])
	while True:
		try:
			print(r.run())
		except StopIteration:
			break

