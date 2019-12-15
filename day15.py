import intcode
import collections

def neighbours(loc):
	x, y = loc
	yield (x-1, y)
	yield (x, y+1)
	yield (x+1, y)
	yield (x, y-1)

def mkpath(start, back, end):
	p = [end]
	while p[-1] != start:
		p.append(back[p[-1]])
	return p[::-1]

class Broken(Exception):
	pass

def shortest_path(map, loc, target):
	back = dict()
	done = set()
	q = collections.deque([])
	q.append(loc)
	done.add(loc)
	while q:
		x = q.popleft()
		if x == target:
			return mkpath(loc, back, target)
		for d in neighbours(x):
			if (d not in done) and (map[d] == '.' or map[d] == 'O' or d == target):
				done.add(d)
				back[d] = x
				q.append(d)
	print('cannot find path from %s to %s' % (loc, target))
	raise Broken


def move_robot(runner, robot, path):
	sym = 'x'
	dirs = {
		(0, 1): 1,
		(0, -1): 2,
		(-1, 0): 3,
		(1,0): 4,
	}
	for pi, p in enumerate(path):
		if pi == 0:
			assert p == robot
			continue
		dx, dy = p[0]-robot[0], p[1]-robot[1]
		ins = dirs[dx, dy]
		runner.push(ins)
		out = runner.run()
		if out == 0:
			assert pi == len(path) - 1
			return '#', robot
		elif out == 1:
			sym = '.'
			robot = p
		elif out == 2:
			sym = 'O'
			robot = p
		else:
			assert False
	assert sym != 'x'
	return sym, robot

def show_map(map, robot):
	mx = min(x for x, y in map.keys())
	Mx = max(x for x, y in map.keys())
	my = min(y for x, y in map.keys())
	My = max(y for x, y in map.keys())
	for y in range(my, My+1):
		for x in range(mx, Mx+1):
			sym = map[x,y] if (x,y)!=robot else 'D'
			print(sym, end='')
		print()



def map_out(runner):
	map = collections.defaultdict(lambda: '?')
	q = collections.deque([])
	robot = (0, 0)
	map[robot] = '.'
	for d in neighbours(robot):
		map[d] = 's'
		q.append(d)

	while q:
		x = q.pop()
		if map[x] != 's':
			continue
		path = shortest_path(map, robot, x)
		target_sym, robot = move_robot(runner, robot, path)
		map[x] = target_sym

		if target_sym != '#':
			for d in neighbours(x):
				if map[d] == '?':
					map[d] = 's'
					q.append(d)
	return map


prog = intcode.read('day15.txt')

map = map_out(intcode.Runner(prog))
show_map(map, (0, 0))
oxygen = next(k for k, v in map.items() if v == 'O')
path = shortest_path(map, (0,0), oxygen)
# part 1
print(len(path) - 1)

# part 2
longest = []
for pos in map.keys():
	if map[pos] != '.':
		continue
	path = shortest_path(map, oxygen, pos)
	if len(path) > len(longest):
		longest = path
		print(len(longest)-1, longest[:10], '...', longest[-10:])
