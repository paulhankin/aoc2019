import intcode
import collections

prog = intcode.read('day13.txt')
screen = collections.defaultdict(int)

r = intcode.Runner(prog)

while True:
	try:
		x = r.run()
		y = r.run()
		i = r.run()
		screen[y,x] = i
	except StopIteration:
		break


print(sum(1 for v in screen.values() if v == 2))

prog[0] = 2
r = intcode.Runner(prog)
screen = collections.defaultdict(int)

char = {
	0: ' ',
	1: '!',
	2: '#',
	3: '=',
	4: 'O',
}

def show_screen(screen):
	yM = max(y for y, x in screen.keys())
	xM = max(x for y, x in screen.keys())
	for y in range(yM+1):
		for x in range(xM+1):
			print(char[screen[y,x]], end='')
		print()
	print()


score = 0
while True:
	try:
		x = r.run()
		y = r.run()
		i = r.run()
		if x == -1 and y == 0:
			score = i
		else:
			screen[y,x] = i
	except StopIteration:
		print('final score=', score)
		break
	except IndexError:
		print(u"{}[2J{}[;H".format(chr(27), chr(27)), end='')
		show_screen(screen)
		print('score=', score)
		bx = next(x for (y, x), v in screen.items() if v == 4)
		px = next(x for (y, x), v in screen.items() if v == 3)
		r.push(1 if bx > px else -1 if bx < px else 0)
