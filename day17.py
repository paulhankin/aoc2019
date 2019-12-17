import intcode

r = intcode.Runner(intcode.read('day17.txt'))

grid = []
while True:
	try:
		c = r.run()
		grid.append(chr(c))
	except StopIteration:
		break

grid = ''.join(grid).split()

def get(grid, i, j):
	if j < 0 or j >= len(grid):
		return '.'
	if i < 0 or i >= len(grid[0]):
		return '.'
	return grid[j][i]

def scaffolding(c):
	return c == '#' or c in rb_dirs

nb = [(1,0), (-1, 0), (0,1), (0,-1)]
rb_dirs = {
	'^': (0,-1),
	'>': (1, 0),
	'<': (-1, 0),
	'v': (0, 1)
}
rb_right = {
	(0, -1): (1, 0),
	(1, 0): (0, 1),
	(0, 1): (-1, 0),
	(-1, 0): (0, -1),
}
rb_left = dict((k, rb_right[rb_right[rb_right[k]]]) for k in rb_right)

M = len(grid)
N = len(grid[0])
rb_loc, rb_dir = None, None
isects = 0
for j in range(M):
	for i in range(N):
		sym = grid[j][i]
		if sym == '^' or c == '>' or c == '<' or c == 'v':
			rb_loc = i, j
			rb_dir = rb_dirs[sym]
		grid[j][i] == '#'
		n = sum(scaffolding(get(grid, i+dx, j+dy)) for dx, dy in rb_dirs.values())
		if scaffolding(get(grid, i, j)) and n == 3 or n == 4:
			sym = 'O'
			isects += i * j
		print(sym, end='')
	print()
print(isects)

path = ['R']
rb_dir = rb_right[rb_dir]
while True:
	i, j = rb_loc
	dx, dy = rb_dir
	ldx, ldy = rb_left[rb_dir]
	rdx, rdy = rb_right[rb_dir]
	# print(rb_loc, rb_dir, dx, dy, ldx, ldy, rdx, rdy)
	if get(grid, i+dx, j+dy) == '#':
		if type(path[-1]) == int:
			path[-1] += 1
		else:
			path.append(1)
		rb_loc = (i+dx, j+dy)
	elif get(grid, i+ldx, j+ldy) == '#':
		path.append('L')
		rb_dir = rb_left[rb_dir]
	elif get(grid, i+rdx, j+rdy) == '#':
		path.append('R')
		rb_dir = rb_right[rb_dir]
	else:
		break

def path_dissect(path, i, seq, parts):
	if i == len(path):
		yield seq, parts
		return
	# print(path, i, seq, parts)
	for pn, p in enumerate(parts):
		if i + len(p) <= len(path) and path[i:i+len(p)] == p:
			seq.append(pn)
			for ys, yp in path_dissect(path, i + len(p), seq, parts):
				yield ys, yp
			seq.pop()
	if len(parts) < 3:
		for j in range(i+1, len(path)):
			seq.append(len(parts))
			parts.append(path[i:j])
			for ys, yp in path_dissect(path, j, seq, parts):
				yield ys, yp
			parts.pop()
			seq.pop()

print(path)
best = None
best_score = None
for seq, parts in path_dissect(path, 0, [], []):
	main_prog = ','.join('ABC'[x] for x in seq)
	progs = [','.join(str(x) for x in p) for p in parts]
	if 0:
		print(main_prog)
		for i, p in enumerate(progs):
			print('ABC'[i], ':', p)
		print()
	score = max(len(x) for x in progs + [main_prog])
	if best is None or score < best_score:
		best, best_score = (main_prog, progs), score

spath = ','.join(str(x) for x in path)
print(len(spath), spath)
print(best_score, best)

main, (a, b, c) = best
indata = main + '\x0a' + a + '\x0a' + b + '\x0a' + c + '\x0a' + 'n' + '\x0a'
print(indata)


prog = intcode.read('day17.txt')
prog[0] = 2
run = intcode.Runner(prog)
for i in indata:
	run.push(ord(i))
while True:
	o = run.run()
	print(o)

