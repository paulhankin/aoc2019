def parse_inp(filename):
	with open(filename, 'r') as f:
		a = f.read()
	r = dict()
	for b in a.split():
		x, y = b.split(')')
		if x not in r:
			r[x] = []
		r[x].append(y)
	return r


def sum_depths(x, root, d):
	r = d
	if root in x:
		for c in x[root]:
			r += sum_depths(x, c, d+1)
	return r

def get_parents(x):
	r = dict()
	for a, b in x.items():
		for c in b:
			assert c not in a
			r[c] = a
	return r

def spine(parents, a):
	p = [a]
	while p[-1] in parents:
		p.append(parents[p[-1]])
	return p


def common_parent(parents, a, b):
	sa = spine(parents, a)[::-1]
	sb = spine(parents, b)[::-1]
	com_parents = set(sa) & set(sb)
	print('spine a', sa)
	print('spine b', sb)
	print('shared', com_parents)
	r = 0
	while sa[-1] not in com_parents:
		r += 1
		sa.pop()
	while sb[-1] not in com_parents:
		r += 1
		sb.pop()
	return r - 2

orbits = parse_inp('aoc6.txt')
parents = get_parents(orbits)

print(common_parent(parents, 'YOU', 'SAN'))


print(sum_depths(orbits, 'COM', 0))