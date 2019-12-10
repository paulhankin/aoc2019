import math
import itertools

TESTS = [
('''.#..#
.....
#####
....#
...##'''.split(), 8),
('''......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####'''.split(), 33),
('''#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.'''.split(), 35),
('''.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..'''.split(), 41),

]

import collections

def sgn(x):
	return 1 if x > 0 else -1 if x < 0 else 0

def count(asteroids, y, x):
	mags2 = collections.defaultdict(list)
	for ay, ax in asteroids:
		m = (ax-x)*(ax-x) + (ay-y)*(ay-y)
		mags2[m].append((ay-y, ax-x))
	found = []
	for _, asters in sorted(mags2.items()):
		new_found = []
		for (ay, ax) in asters:
			if ay==ax==0:
				continue
			for (by, bx) in found:
				if ax * by == ay * bx and sgn(ax) == sgn(bx) and sgn(ay) == sgn(by):
					break
			else:
				new_found.append((ay,ax))
		found.extend(new_found)
	return found

def find_best(asteroids):
	best = []
	best_loc = None
	for j, i in asteroids:
		f = count(asteroids, j, i)
		# print('I can see %s from %d,%d' % (f, j, i))
		if len(f) > len(best):
			best = f
			best_loc = j, i
	return len(best), best, best_loc

if 0:
	for i, (tc, want) in enumerate(TESTS):
		asteroids = set((y, x) for y, row in enumerate(tc) for x, c in enumerate(row) if c == '#')
		got, _, best_loc = find_best(asteroids)
		if got != want:
			print('failed %d: got %d@%s want %d' % (i, got, best_loc, want))

with open('day10.txt', 'r') as f:
	rows = f.read().split()

asteroids = set((y, x) for y, row in enumerate(rows) for x, c in enumerate(row) if c == '#')
n, _, (locy, locx) = find_best(asteroids)

def reduce_fraction(dy, dx):
	for i in range(2, max(abs(dx), abs(dy)) + 1):
		while dy%i == 0 and dx%i == 0:
			dy //= i
			dx //= i
	return dy, dx

assert reduce_fraction(4, 2) == (2, 1)
assert reduce_fraction(5, 0) == (1, 0)
assert reduce_fraction(0, -5) == (0, -1)
assert reduce_fraction(4, -3) == (4, -3)

by_theta = collections.defaultdict(list)
for ay, ax in asteroids:
	dy, dx = ay - locy, ax - locx
	if dy == dx == 0:
		continue
	ry, rx = reduce_fraction(dy, dx)
	by_theta[math.fmod(math.pi * 2 + math.pi/2 - math.atan2(-ry, rx), math.pi * 2)].append((dy, dx))

for _, a in by_theta.items():
	a.sort(key=lambda x: -x[0]*x[0] - x[1]*x[1])

print(n)

zapped = 0
by_theta = sorted(by_theta.items())
for _, a in itertools.cycle(by_theta):
	if a:
		zapped += 1
		dy, dx = a[-1]
		a.pop()
		if zapped == 200:
			print(zapped, (dy+locy, dx+locx))
			break

