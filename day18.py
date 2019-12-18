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
def neighs(map, loc, keys_remaining):
	x, y = loc
	for dx, dy in DIRS:
		x2 = x+dx
		y2 = y+dy
		if not(0 <= x2 < len(map[0]) and 0 <= y2 < len(map)):
			continue
		s = map[y2][x2]
		if s == '#' or ('A' <= s <= 'Z' and s.lower() in keys_remaining):
			continue
		yield x2, y2


def shortest_path(map, loc, target, keys_remaining):
	back = dict()
	q = [(heur(loc, target), loc)]
	done = set([loc])
	while q:
		_, x = heapq.heappop(q)
		if x == target:
			r = [target]
			while r[-1] in back:
				r.append(back[r[-1]])
			return r
		for n in neighs(map, x, keys_remaining):
			if n in done:
				continue
			back[n] = x
			done.add(n)
			heapq.heappush(q, (heur(n,target), n))
	return None


with open('day18.txt', 'r') as f:
	lines = f.read().split()

map, syms = make_map(lines)

assert len(syms) == 26*2+1

man = syms['@']

graph_verts = set()
graph_edges = collections.defaultdict(list)

def make_graph(map, sym, loc, keys_remaining):
	skr = sorted(keys_remaining)
	node = (loc, ''.join(skr))
	if node in graph_verts:
		return node
	graph_verts.add(node)
	print(loc, keys_remaining)
	for k in skr:
		p = shortest_path(map, loc, sym[k], keys_remaining)
		if p is None:
			continue
		keys_remaining.remove(k)
		node2 = make_graph(map, sym, sym[k], keys_remaining)
		keys_remaining.add(k)
		graph_edges[node].append((node2, len(p)))
	return node

make_graph(map, syms, man, set(chr(x) for x in range(ord('a'), ord('z')+1)))

print(graph_verts)
for k, v in graph_edges:
	print(k, v)
