import collections

def parse_part(x):
	left, right = x.split(' ')
	return int(left), right

def parse(lines):
	reactions = dict()
	for line in lines:
		if not line.strip():
			continue
		left, right = line.split(' => ')
		lefts = left.split(', ')
		part_n, part_name = parse_part(right)
		reactions[part_name] = (part_n, [parse_part(l) for l in lefts])
	return reactions

def quant(reactions, nfuel):
	spares = collections.defaultdict(int)
	need = collections.deque([('FUEL', nfuel)])
	ores = 0
	while need:
		target, target_n = need.popleft()
		if target == 'ORE':
			ores += target_n
			continue
		if spares[target]:
			use = min(target_n, spares[target])
			spares[target] -= use
			target_n -= use
		if target_n == 0:
			continue
		r_n, parts = reactions[target]
		nreacts = (target_n + r_n - 1) // r_n
		spares[target] += nreacts * r_n - target_n
		for q, c in parts:
			need.append((c, q * nreacts))
	return ores

with open('day14_test.txt', 'r') as f:
	test_reactions = parse(f.read().split('\n'))

print('test:')
print(quant(test_reactions, 1))

with open('day14.txt', 'r') as f:
	reactions = parse(f.read().split('\n'))

print('\npart 1:')
print(quant(reactions, 1))

print('\npart 2:')
minfuel = 0
maxfuel = 1000000000
while maxfuel > minfuel + 1:
	m = (minfuel + maxfuel) // 2
	ores = quant(reactions, m)
	if ores > 1000000000000:
		maxfuel = m
	else:
		minfuel = m
print('%d fuel needs %d ores' % (minfuel, ores))
print(' (and one more fuel needs %d ores)' % (quant(reactions, minfuel+1)))
