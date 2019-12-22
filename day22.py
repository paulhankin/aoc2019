# computes r * a^n, where a*b is mul(a, b)
def exp(r, a, n, mul):
	while n:
		if n % 2 == 1: r = mul(r, a)
		a = mul(a, a)
		n //= 2
	return r

# idea: represent a shuffle as a pair (a, b) such that the card at
# position i goes to (i*a+b) (modulo deck size).
# This representation is good for cuts, deals, and deck reversals.
# It's also closed under composition.

# do shuffle s1, then shuffle s2 on a deck of the given size.
def compose(s1, s2, DS):
	# card at posn. x goes first to posn s1a*x+b
	# then goes to (s2a*(s1a*x+s1bb) + s2b)
	return (s1[0]*s2[0] % DS, (s2[0]*s1[1] + s2[1]) % DS)

def read_cmds():
	with open('day22.txt') as f:
		lines = f.read().split('\n')
	for parts in (line.strip().split() for line in lines):
		if parts[0] == 'cut': yield (1, -int(parts[-1]))
		elif parts[0] == 'deal' and parts[-1] == 'stack': yield (-1, -1)
		elif parts[0] == 'deal': yield (int(parts[-1]), 0)
		else: raise Exception('bad instruction %r' % parts)


cmds = list(read_cmds())

print('part 1')
DS1 = 10007
shuf = (1, 0)
for cmd in cmds:
	shuf = compose(shuf, cmd, DS1)
print((shuf[0] * 2019 + shuf[1]) % DS1)

print('part 2')
DS2 = 119315717514047
ITERS = 101741582076661
shuf = (1, 0)
for cmd in cmds:
	shuf = compose(shuf, cmd, DS2)
shuf = exp((1, 0), shuf, ITERS, lambda a, b: compose(a, b, DS2))

TARGET = 2020
# DS2 is prime, so the modular inverse of x mod DS2 is pow(x, DS2-2, DS2).
# find loc such that shuf[0] * loc + shuf[1] is TARGET.
loc = (pow(shuf[0], DS2-2, DS2) * (TARGET - shuf[1])) % DS2
print(loc)
assert (shuf[0] * loc + shuf[1]) % DS2 == TARGET
