def read_cmds():
	with open('day22.txt') as f:
		lines = f.read().split('\n')
	for line in lines:
		parts = line.strip().split()
		if not parts:
			continue
		elif parts[0] == 'cut':
			yield (1, -int(parts[-1]))
		elif parts[0] == 'deal' and parts[-1] == 'stack':
			yield (-1, -1)
		elif parts[0] == 'deal':
			yield (int(parts[-1]), 0)
		else:
			raise Exception('bad instruction %r' % cmd)

def compose(s1, s2, DS):
	# card at posn. x goes first to posn s1a*x+b
	# then goes to (s2a*(s1a*x+s1bb) + s2b)
	return (s1[0]*s2[0] % DS, (s2[0]*s1[1] + s2[1]) % DS)

def deval(deck, i, DS):
	return (i * deck[0] + deck[1]) % DS

def shuf(cmds, DS):
	deck = 1, 0
	for cmd in cmds:
		deck = compose(deck, cmd, DS)
	return deck

def shuf_pow(M, n, DS):
	R = (1, 0)
	while n:
		if n % 2 == 1: R = compose(R, M, DS)
		M = compose(M, M, DS)
		n //= 2
	return R

def modinv(a, n):
	t, r  = 0, n
	nt, nr = 1, a
	while nr:
		q = r // nr
		t, nt = (nt, t - q*nt)
		r, nr = (nr, r - q*nr)
	assert r == 1
	return t % n

cmds = list(read_cmds())

print('part 1')
DS1 = 10007
deck = shuf(cmds, DS1)
print(deval(deck, 2019, DS1))

print('part 2')
DS2 = 119315717514047
ITERS = 101741582076661
deck = shuf_pow(shuf(cmds, DS2), ITERS, DS2)

TARGET = 2020
loc = (modinv(deck[0], DS2) * (TARGET - deck[1])) % DS2
print(loc)
assert deval(deck, loc, DS2) == 2020
