import intcode

code = intcode.read('day19.txt')

count = 0

def get(code, i, j):
	assert i >= 0 and j >= 0
	r = intcode.Runner(code)
	r.push(i)
	r.push(j)
	o = r.run()
	return o

def startend(code, j, gs, ge):
	while True:
		o = get(code, gs, j)
		if not o:
			gs += 1
			break
		gs -= 1
	while True:
		o = get(code, gs, j)
		if o:
			break
		gs += 1

	ge = max(gs+1, ge)
	while True:
		o = get(code, ge, j)
		if o:
			ge += 1
			break
		ge -= 1

	while True:
		o = get(code, ge, j)
		if not o:
			break
		ge += 1
	return (gs, ge)



ls, le = 3, 4
for j in range(2, 50):
	count = 1
	ls, le = startend(code, j, ls, le)
	# print(j, ls, le)
	print('.' * ls + '#' * (le - ls) + '.' * (50 - le))
	count += le - ls

print('part1', count)

def find_square():
	record = [(0, 1), (-1, -1), (3, 4)]
	while True:
		j = len(record)
		record.append(startend(code, len(record), record[-1][0], record[-1][1]))
		es, ee = record[-1][0], record[-1][1]
		if j < 100:
			continue
		ps, pe = record[-100][0], record[-100][1]
		if ee - es >= 100 and ps <= es and pe - es >= 100:
			for k in range(j-99, j+1):
				print(k, record[k])
			return es, j - 99

x, y = find_square()
print('result =', x * 10000 + y)

for j in range(y-1, y + 101):
	for i in range(x - 1, x + 101):
		r = intcode.Runner(code)
		r.push(i)
		r.push(j)
		o = r.run()
		if x <= i <= x + 99 and y <= j <= y+99:
			print('.#'[o], end='')
		else:
			print(' @'[o], end='')
	print()


