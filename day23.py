import intcode

code = intcode.read('day23.txt')

N = 50

def run(part):
	nics = [intcode.Runner(code, ins=[i], nic=True) for i in range(N)]
	network = [[] for _ in range(N)] # data we've received from each nic.

	NAT = None
	lastNAT = None

	while True:
		idle = all((not nic.input) and nic.nic_failed_ins > 2 for nic in nics)
		if idle:
			assert NAT is not None
			nics[0].push(NAT[0])
			nics[0].push(NAT[1])
			if lastNAT and lastNAT[1] == NAT[1]:
				return NAT
			lastNAT = NAT
		for i in range(N):
			try:
				o = nics[i].run()
				network[i].append(o)
			except intcode.Interrupt:
				pass
			if len(network[i]) == 3:
				a, x, y = network[i]
				network[i] = []
				if a == 255:
					if part == 1:
						return x, y
					NAT = (x, y)
				else:
					nics[a].push(x)
					nics[a].push(y)

print('part 1', run(1))

print('part 2', run(2))
