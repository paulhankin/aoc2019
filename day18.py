import itertools
import collections
import heapq

def make_map(lines):
	map = lines
	boring = set('.#')
	syms = dict()
	for y, row in enumerate(map):
		for x, sym in enumerate(row):
			if sym not in boring:
				assert sym not in syms
				syms[sym] = (x, y)
	return map, syms

def heur(x, y):
	return abs(x[0]-y[0]) + abs(x[1]-y[1])

DIRS = [(1,0),(0,1),(-1,0),(0,-1)]
def neighs(map, loc):
	x, y = loc
	for dx, dy in DIRS:
		x2 = x+dx
		y2 = y+dy
		if not(0 <= x2 < len(map[0]) and 0 <= y2 < len(map)):
			continue
		if map[y2][x2] == '#':
			continue
		yield x2, y2


def shortest_path(map, syms, start, end):
	back = dict()
	q = [(heur(start, end), start, [], True)]
	done = set([start])
	while q:
		_, x, doors, adj = heapq.heappop(q)
		if x == end:
			r = [end]
			while r[-1] in back:
				r.append(back[r[-1]])
			return r, doors, adj
		for n in neighs(map, x):
			if n in done:
				continue
			back[n] = x
			done.add(n)
			s = map[n[1]][n[0]]
			ndoors = doors
			nadj = adj
			if 'A' <= s <= 'Z':
				ndoors = doors + [s]
			if ('a' <= s <= 'z') and n != start and n != end:
				nadj = False
			heapq.heappush(q, (heur(n, end), n, ndoors, nadj))
	return None, None, None


with open('day18.txt', 'r') as f:
	lines = f.read().split()

if 0:
	lines = """\
	########################
	#@..............ac.GI.b#
	###d#e#f################
	###A#B#C################
	###g#h#i################
	########################""".split()

if 0:
	lines = """\
	#################
	#i.G..c...e..H.p#
	########.########
	#j.A..b...f..D.o#
	########@########
	#k.E..a...g..B.n#
	########.########
	#l.F..d...h..C.m#
	#################""".split()

if 0:
	lines = """\
	########################
	#...............b.C.D.f#
	#.######################
	#.....@.a.B.c.d.A.e.F.g#
	########################""".split()

map, syms = make_map(lines)
for line in map:
	print(line)
print()

def make_graph(map, syms):
	nodes = sorted(x for x in syms if x == x.lower())
	verts = set()
	edges = collections.defaultdict(dict)
	dists = dict()
	for n1, n2 in itertools.combinations(nodes, 2):
		p, doors, adj = shortest_path(map, syms, syms[n1], syms[n2])
		if p is None:
			continue
		dists[n1,n2] = len(p) - 1
		dists[n2,n1] = len(p) - 1
		if not adj:
			continue
		verts.add(n1)
		verts.add(n2)
		sdoors = ''.join(sorted(doors))
		edges[n1][n2] = (len(p), sdoors)
		edges[n2][n1] = (len(p), sdoors)
	return verts, edges, dists

V, E, D = make_graph(map, syms)

if 0:
	for k, es in E.items():
		print(k, es)

if 0:
	for k, v in sorted(D.items()):
		print(k, v)

all_lower = ''.join(x for x in 'abcdefghijklmnopqrstuvwxyz' if x in syms)
all_lower_set = set(all_lower)

def shortest_key_path(E, D, starts):
	visited = set()
	dists = collections.defaultdict(lambda: 1e9)
	start = (tuple(starts), ''.join(starts))
	dists[start] = 0
	q = [(0, start)]
	prev = dict()
	while q:
		pri, state = heapq.heappop(q)
		if state in visited:
			continue
		visited.add(state)
		x, keys = state
		skeys = set(keys)
		if len(keys) == len(all_lower) + len(starts):
			r = [state]
			while r[-1] in prev:
				r.append(prev[r[-1]])
			s = []
			last = set()
			for _, k in r[::-1]:
				s.append(''.join(sorted(set(k) - last)))
				last = set(k)
			return ''.join(s), dists[state]
		for k in all_lower:
			if k in skeys:
				continue
			if not any(all(d.lower() in skeys for d in E[k_last][k][1]) for k_last in skeys if k in E[k_last]):
				continue
			rn = -1
			for i, pos in enumerate(x):
				if (pos,k) in D:
					rn = i
			assert rn != -1
			nkeys = keys + k
			rpos = list(x)
			rpos[rn] = k
			nstate = (tuple(rpos), ''.join(sorted(nkeys)))
			d = min(D.get((i, k), 1e9) for i in x)
			if dists[nstate] > dists[state] + d:
				heapq.heappush(q, (dists[state] + d, nstate))
				prev[nstate] = state
				dists[nstate] = dists[state] + d

	assert False

print('part 1')
print(shortest_key_path(E, D, '@'))
print('part2')

man_x, man_y = syms['@']
for i in range(3):
	fill = ['1#2', '###', '3#4'][i]
	lines[man_y - 1 + i] = lines[man_y - 1 + i][:man_x - 1] + fill + lines[man_y - 1 + i][man_x + 2:]

map, syms = make_map(lines)
V, E, D = make_graph(map, syms)
print(shortest_key_path(E, D, '1234'))
