import itertools
import intcode

CC = intcode.read('aoc7.txt')
best = -1e9

for ins in itertools.permutations([5, 6, 7, 8, 9]):
	sig = 0
	try:
		for r in itertools.cycle(intcode.Runner(CC, [v]) for v in ins):
			r.push(sig)
			sig = r.run()
	except intcode.HaltException:
		pass
	if sig > best:
		best = sig
print(best)
