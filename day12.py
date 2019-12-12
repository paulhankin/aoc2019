def sgn(x):
	return -1 if x < 0 else 1 if x > 0 else 0

def sim_step(moons):
	dv = [[0,0,0] for _ in moons]

	for i1, m1 in enumerate(moons):
		for i2, m2 in enumerate(moons):
			if i1 <= i2:
				continue
			pos1, vel1 = m1
			pos2, vel2 = m2
			for i in range(3):
				di = sgn(pos1[i] - pos2[i])
				dv[i1][i] -= di
				dv[i2][i] += di
	# update velocities
	moons = [(m[0], tuple(m[1][i] + dv[j][i] for i in range(3))) for j, m in enumerate(moons)]
	# update positions
	moons = tuple((tuple(m[0][i] + m[1][i] for i in range(3)), m[1]) for m in moons)
	return moons

moons = [(5, 4, 4), (-11, -11, -3), (0, 7, 0), (-13, 2, 10)]
# moons = [(-1,0,2), (2,-10,-7), (4,-8,8), (3,5,-1)]
# moons = [(-8,-10,0), (5,5,10), (2,-7,3), (9,-8,-3)]
moons = [(m, (0,0,0)) for m in moons]

nsteps = 1000
every = 100
for _ in range(nsteps):
	moons = sim_step(moons)
ten = 0
for m in moons:
	pot = sum(abs(x) for x in m[0])
	kin = sum(abs(x) for x in m[1])
	ten += pot * kin
print('total energy =', ten)

def find_repeat(moons):
	prevs = set()
	steps = 0
	while moons not in prevs:
		prevs.add(moons)
		steps += 1
		moons = sim_step(moons)
	return steps, moons


def gcd(x, y):
	x, y = max(x, y), min(x, y)
	while y:
		x, y = y, x % y
	return x 

# part 2
moons = [(5, 4, 4), (-11, -11, -3), (0, 7, 0), (-13, 2, 10)]
# moons = [(-1,0,2), (2,-10,-7), (4,-8,8), (3,5,-1)]
mx = [(m[0],0,0) for m in moons]
my = [(0,m[1],0) for m in moons]
mz = [(0,0,m[2]) for m in moons]

r = 1
for part in (mx,my,mz):
	moons = tuple((m, (0,0,0)) for m in part)
	steps, moons = find_repeat(moons)
	print(steps, moons)
	r = r * steps // gcd(r, steps)
	print(r)
