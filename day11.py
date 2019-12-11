import intcode
import collections

def robot(prog, startcol):
	out = collections.defaultdict(int)
	painted = set()
	x, y, d = 0, 0, 0
	out[y, x] = startcol
	run = intcode.Runner(prog)
	try:
		while True:
			run.push(out[y, x])
			col = run.run()
			turn = run.run()
			assert col == 0 or col == 1
			assert turn == 0 or turn == 1
			out[y, x] = col
			painted.add((y, x))
			d = (d + 1 if turn == 1 else d - 1) % 4
			y += 1 if d == 2 else -1 if d == 0 else 0
			x += 1 if d == 1 else -1 if d == 3 else 0
	except StopIteration:
		pass
	return out, len(painted)



# part 1
out, n = robot(intcode.read("day11.txt"), 0)

# part 2
out, _ = robot(intcode.read("day11.txt"), 1)
for y in range(6):
	for x in range(41):
		print(('#' if out[y,x] else '.'), end='')
	print()
