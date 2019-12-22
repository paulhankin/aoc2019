with open('day22.txt') as f:
	cmds = f.read().split('\n')

def compose(s1, s2, DS):
	s1a, s1b = s1
	s2a, s2b = s2
	# card at posn. x goes first to posn s1a*x+b
	# then goes to (s2a*(s1a*x+s1bb) + s2b)
	return (s1a*s2a % DS, (s2a*s1b + s2b) % DS)

def deval(deck, i, DS):
	return (i * deck[0] + deck[1]) % DS

cmds = [cmd.strip() for cmd in cmds]
cmds = [cmd for cmd in cmds if cmd]

deck = 1, 0 # card at position x goes to goes to x*deck[0] + deck[1]
DS = 10007

def shuf(cmds, DS):
	deck = 1, 0
	for cmd in cmds:
		parts = cmd.split()
		if parts[0] == 'cut':
			N = int(parts[-1])
			deck = compose(deck, (1, -N), DS)
		elif parts[0] == 'deal':
			if parts[-1] == 'stack':
				deck = compose(deck, (-1, -1), DS)
			else:
				N = int(parts[-1])
				deck = compose(deck, (N, 0), DS)
		else:
			assert False
	return deck

print('part 1')
deck = shuf(cmds, 10007)
print(deck)
print(deval(deck, 2019, DS))

def mat_mul(A, B, DS):
	R = [[0, 0], [0, 0]]
	for i in range(2):
		for j in range(2):
			for k in range(2):
				R[i][k] += A[i][j] * B[j][k]
				R[i][k] %= DS
	return R

def mat_pow(M, n, DS):
	R = [[1, 0], [0, 1]]
	while n:
		if n % 2 == 1:
			R = mat_mul(R, M, DS)
		M = mat_mul(M, M, DS)
		n //= 2
	return R

def cmd_iter(deck, n, DS):
	M = ((deck[0], deck[1]), (0, 1))
	M = mat_pow(M, n, DS)
	return (M[0][0], M[0][1])

def egcd(a, b):
    lastremainder, remainder = abs(a), abs(b)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if a < 0 else 1), lasty * (-1 if b < 0 else 1)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError('modinv for {} does not exist'.format(a))
    return x % m


print(mat_pow([[1, 1], [0, 1]], 2, 100))

print('part 2')
DS = 119315717514047
deck = shuf(cmds, DS)
# print(cmd_iter(deck, 0, DS))
# print(cmd_iter(deck, 1, DS))
# print(cmd_iter(deck, 2, DS))

deck = cmd_iter(deck, 101741582076661, DS)
loc = (modinv(deck[0], DS) * (2020 - deck[1])) % DS
print(deck)
print(loc)
print(deval(deck, loc, DS))
