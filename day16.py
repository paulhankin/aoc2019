
ggg = [0, 1, 0, -1]
def f(i, j):
	return ggg[(j + 1) // (i+1) % 4]


def fft(n, i):
	# print(' + '.join('%d*%d' % (d, f(i, j)) for j, d in enumerate(n)))
	return abs(sum((f(i, j) * d) for j, d in enumerate(n))) % 10


def step(n):
	r = []
	for i, _ in enumerate(n):
		r.append(fft(n, i))
	return r

def step2(n):
	r = [0] * len(n)
	for i, d in enumerate(n):
		for j in range(len(n)):
			if j >= i:
				break
			f = (i+1)//(j+1)%4
			if f == 1:
				r[j] += d
			elif f == 3:
				r[j] -= d
	for i in range(len(n)):
		r[i] = abs(r[i]) % 10
	return r

def step3(n, res, sums, startat=0):
	N = len(n)
	sums[0] = 0
	for i, d in enumerate(n):
		sums[i+1] = sums[i] + d
	for i in range(startat, N):
		res[i] = 0
		sign = 1
		for k in range(N // (i+1) + 1):
			if k % 2 == 0:
				continue
			start = k*(i+1)-1
			end = min(N, (k+1)*(i+1)-1)
			ds = sums[end] - sums[start]
			res[i] += sign * ds
			sign *= -1
		res[i] = abs(res[i]) % 10
	return res


print('test')
seq1 = [int(x) for x in '12345678']
seq3 = list(seq1)
for i in range(11):
	print(seq1, seq3)
	assert seq3 == seq1
	seq1 = step(seq1)
	seq3 = step3(seq3, [0]*len(seq1), [0]*(1+len(seq1)))

DATA = '59750530221324194853012320069589312027523989854830232144164799228029162830477472078089790749906142587998642764059439173975199276254972017316624772614925079238407309384923979338502430726930592959991878698412537971672558832588540600963437409230550897544434635267172603132396722812334366528344715912756154006039512272491073906389218927420387151599044435060075148142946789007756800733869891008058075303490106699737554949348715600795187032293436328810969288892220127730287766004467730818489269295982526297430971411865028098708555709525646237713045259603175397623654950719275982134690893685598734136409536436003548128411943963263336042840301380655801969822'

print('part 1')
seq = [int(x) for x in DATA]
res = [0] * len(seq)
sums = [0] * (1+len(seq))
for s in range(100):
	seq = step3(seq, res, sums)
	# print('steps=', s, ''.join(str(x) for x in seq))
print(''.join(str(x) for x in seq[:8]))

print('part 2')
offset = int(DATA[:7])
print('offset is: %d' % offset)
seq = [int(x) for x in DATA] * 10000
res = [0] * len(seq)
sums = [0] * (len(seq)+1)

print('steps=', 0, ''.join(str(x) for x in seq[:100]))
print('message=%s' % ''.join(str(x) for x in seq[offset:offset+8]))
for s in range(100):
	print('running step3 iteration %d' % (s+1))
	seq = step3(seq, res, sums, startat=offset)
	print('message=%s' % ''.join(str(x) for x in seq[offset:offset+8]))
