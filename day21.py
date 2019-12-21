import intcode


def format_prog(prog, end):
	prog = [line.strip() + "\n" for line in prog.split('\n')]
	prog = [x for x in prog if len(x) > 1]
	prog.append(end + "\n")
	prog = ''.join(prog)
	return [ord(c) for c in prog]

def exec(prog, end):
	run = intcode.Runner(code)
	for c in format_prog(prog, end):
		run.push(c)

	while True:
		try:
			out = run.run()
		except StopIteration:
			return
		if out > 255:
			print('FINAL OUTPUT:', out)
		else:
			print(chr(out), end='')

code = intcode.read('day21.txt')

prog = """
	NOT A J
	NOT B T
	OR T J
	NOT C T
	OR T J
	AND D J
"""

exec(prog, "WALK")

"""
   #?????
123456789

D & !(!E & !H)
D & !(!(E|H))

MUST: #...#
MUST: #???#...#

BAD: .??. > !E&!H
BAD: #.?..
"""

prog2 = """
	OR A T
	AND B T
	AND C T
	NOT T J

	OR E T
	OR H T

	AND T J
	AND D J
"""

exec(prog2, "RUN")
