def make_bits():
	bits = dict()
	for i in range(5):
		for j in range(5):
			bits[i,j] = 1<<(j * 5 + i)
	return bits

BITS = make_bits()
DIRS = [(-1,0),(0,1),(1,0),(0,-1)]

def get_grid(g, i, j):
	return bool(g & BITS.get((i,j), 0))

def step(grid):
	v = 0
	for i in range(5):
		for j in range(5):
			s = sum(get_grid(grid, i+di, j+dj) for di, dj in DIRS)
			b = BITS[i,j]
			if get_grid(grid, i, j):
				if s == 1:
					v |= b
			else:
				if s == 1 or s == 2:
					v |= b
	return v

import collections
DIRS2 = collections.defaultdict(list)
for i in range(5):
	for j in range(5):
		if i != 0 and j != 0 and i != 4 and j != 4:
			continue
		if i == 0:
			DIRS2[i,j].append((3, 2, -1))
			DIRS2[3,2].append((i, j, 1))
		if j == 0:
			DIRS2[i,j].append((2, 3, -1))
			DIRS2[2,3].append((i,j, 1))
		if i == 4:
			DIRS2[i,j].append((1, 2, -1))
			DIRS2[1,2].append((i, j, 1))
		if j == 4:
			DIRS2[i,j].append((2, 1, -1))
			DIRS2[2,1].append((i, j, 1))

if False:
	for k, v in DIRS2.items():
		print(k, v)
	stop

def step_inf(grids, levels):
	new_grids = dict()
	for lev in range(-levels, levels+1):
		new_grids[lev] = 0
		for i in range(5):
			for j in range(5):
				if i == 2 and j == 2:
					continue
				adj = 0
				for ai, aj in [(i+1,j), (i-1,j), (i,j-1), (i,j+1)]:
					if 0 <= ai < 5 and 0 <= aj < 5 and (ai != 2 or aj != 2):
						adj += get_grid(grids[lev], ai, aj)

				for ai, aj, dlev in DIRS2[i,j]:
					alev = lev + dlev
					if alev <= -levels or alev >= levels:
						continue
					adj += get_grid(grids[alev], ai, aj)

				b = BITS[i,j]
				if get_grid(grids[lev], i, j):
					if adj == 1:
						new_grids[lev] |= b
				else:
					if adj == 1 or adj == 2:
						new_grids[lev] |= b
	return new_grids

def show_grid(g, inf=False):
	for j in range(5):
		for i in range(5):
			if inf and i == 2 and j == 2:
				print('?', end='')
			else:
				print('#' if get_grid(g, i, j) else '.', end='')
		print()

def parse_grid(lines):
	g = 0
	for j in range(5):
		for i in range(5):
			if lines[j][i] == '#':
				g |= BITS[i,j]
			elif lines[j][i] != '.':
				assert False
	return g

grid = parse_grid('#####\n.#.##\n#...#\n..###\n#.##.'.split())
# grid = parse_grid('....#\n#..#.\n#..##\n..#..\n#....'.split())

got = set()

def bugcount(g):
	return sum(get_grid(g, i, j) for i in range(5) for j in range(5))

print('part 1')
while True:
	if grid in got:
		show_grid(grid)
		print(grid)
		break
	got.add(grid)
	grid = step(grid)

grid = parse_grid('#####\n.#.##\n#...#\n..###\n#.##.'.split())
#grid = parse_grid('....#\n#..#.\n#..##\n..#..\n#....'.split())
LEVS = 210
grids = collections.defaultdict(int)
grids[0] = grid
print('part 2')
for _ in range(200):
	grids = step_inf(grids, LEVS)

if False:
	for lev in range(-LEVS, LEVS+1):
		print('level %d' % lev)
		show_grid(grids[lev], inf=True)
		print()
print('bugs', sum(bugcount(g) for g in grids.values()))
