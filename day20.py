import collections
import heapq

with open('day20.txt', 'r') as f:
	lines = f.read().split('\n')

def simplify(x):
	return '.' if x == '.' else '#'

def letters(x):
	return x if ('A' <= x <= 'Z') else '.'

map = [[simplify(x) for x in row] for row in lines]
syms = [[letters(x) for x in row] for row in lines]

labels = collections.defaultdict(str)
labloc = collections.defaultdict(list)
W, H = len(map[0]), len(map)

def get(map, i, j):
	if not (0 <= i < W):
		return '#'
	if not (0 <= j < H):
		return '#'
	return map[j][i]

for j in range(H):
	for i in range(W):
		c = get(syms, i, j)
		label = None
		dot = None
		if c == '.':
			continue
		for n in ((i-1,j), (i+1, j), (i, j+1), (i, j-1)):
			d = get(map, *n)
			if d == '.':
				assert not dot
				dot = n
			d = get(syms, *n)
			if d == '.' or d == '#':
				continue
			assert not label
			if n[0]>i or n[1]>j:
				label = d + c
			else:
				label = c + d
		assert label
		if dot:
			labels[dot] = label
			labloc[label].append(dot)
			assert len(labloc[label]) <= 2

for k, v in labloc.items():
	if len(v) == 1:
		print(k, v)

def neighbours(map, labels, labloc, loc):
	x, y = loc
	for x2, y2 in [(x-1,y), (x+1, y), (x, y+1), (x, y-1)]:
		if get(map, x2, y2) == '.':
			yield x2, y2
	lab = labels[loc]
	if lab and len(labloc[lab]) == 2:
		if labloc[lab][0] == loc:
			yield labloc[lab][1]
		elif labloc[lab][1] == loc:
			yield labloc[lab][0]
		else:
			assert False

def outer(map, x, y):
	W = len(map[0])
	H = len(map)
	return not (3 <= x < W - 3 and 3 <= y < H - 3)

def neighbours_layers(map, labels, labloc, loc):
	layer, x, y = loc
	for x2, y2 in [(x-1,y), (x+1, y), (x, y+1), (x, y-1)]:
		if get(map, x2, y2) == '.':
			yield layer, x2, y2
	lab = labels[x, y]
	if not lab:
		return
	out = outer(map, x, y)
	if out and layer == 0:
		return
	if len(labloc[lab]) == 1:
		assert lab == 'AA' or lab == 'ZZ'
		return
	if labloc[lab][0] == (x, y):
		x2, y2 = labloc[lab][1]
	elif labloc[lab][1] == (x, y):
		x2, y2 = labloc[lab][0]
	else:
		assert False
	yield layer + (-1 if out else 1), x2, y2


def shortest_path(map, labels, labloc, start, end, nb):
	visited = set()
	dists = collections.defaultdict(lambda: 1e9)
	dists[start] = 0
	q = [(0, start)]
	prev = dict()
	while q:
		if 0:
			print(u"{}[2J{}[;H".format(chr(27), chr(27)), end='')
			for j in range(H):
				for i in range(W):
					print('@' if (i,j) in visited else map[j][i], end='')
				print()
		pri, loc = heapq.heappop(q)
		if loc in visited:
			continue
		visited.add(loc)

		if loc == end:
			r = [loc]
			while r[-1] in prev:
				r.append(prev[r[-1]])
			return r[::-1]

		for n in nb(map, labels, labloc, loc):
			d2 = dists[loc] + 1
			if d2 < dists[n]:
				dists[n] = d2
				heapq.heappush(q, (d2, n))
				prev[n] = loc
	assert False

start = labloc['AA'][0]
end = labloc['ZZ'][0]

print('part 1')
p = shortest_path(map, labels, labloc, start, end, neighbours)
print(len(p)-1)

for k, v in labloc.items():
	s = 0
	for x in v:
		s += outer(map, *x)
		print(k, x, outer(map, *x))
	assert k == 'AA' or k == 'ZZ' or s == 1

print('part 2')
p = shortest_path(map, labels, labloc, (0, start[0], start[1]), (0, end[0], end[1]), neighbours_layers)
print(len(p)-1)
