import intcode

COMMAND = 'Command?'

import itertools

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

def find_item(target, carried, dropped):
	print(target, carried, dropped)
	for t in dropped:
		if t in target:
			return 'take', t
	for t in carried:
		if t not in target:
			return 'drop', t
	return 'go', None

def advent(code, cmds, items=None):
	commands = []
	r = intcode.Runner(code)
	out = []
	first_cmds = cmds

	need_target = True
	dropped = set()
	carried = set(items if items else [])
	target = None
	targets = powerset(carried)

	while True:
		try:
			o = r.run()
		except StopIteration:
			return commands
		print(chr(o), end='')
		out.append(chr(o))
		if len(out) > 100000:
			return commands
		if len(out) > len(COMMAND) and ''.join(out[-len(COMMAND):]) == COMMAND:
			out = []
			if first_cmds:
				line = first_cmds[0]
				first_cmds = first_cmds[1:]
				print('AUTO>', line)
			elif items is not None:
				if need_target:
					need_target = False
					target = next(targets)
					print('DEBUG: trying set of items', ','.join(target))
				s, i = find_item(target, carried, dropped)
				if s == 'drop':
					line = 'drop ' + i
					dropped.add(i)
					carried.remove(i)
				elif s == 'take':
					line = 'take ' + i
					dropped.remove(i)
					carried.add(i)
				elif s == 'go':
					line = 'west'
					need_target = True
				else:
					print('unknown next_item result', i, s)
					assert False
				print('AUTO CARRY>', line)
			else:
				line = input().strip()
			commands.append(line)
			if line == 'quit':
				return commands
			for x in line + '\n':
				r.push(ord(x))


code = intcode.read('day25.txt')

items = [x for x in """
- asterisk
- ornament
- cake
- space heater
- festive hat
- semiconductor
- food ration
- sand
""".split('\n')]
items = [x for x in items if x]
items = [x.split('- ')[1] for x in items]

commands = ['north', 'take sand', 'north', 'take space heater', 'east', 'take semiconductor', 'west', 'south', 'south', 'west', 'west', 'east', 'north', 'north', 'west', 'south', 'south', 'east', 'east', 'take ornament', 'east', 'west', 'south', 'take festive hat', 'east', 'take asterisk', 'south', 'east', 'take cake', 'west', 'west', 'take food ration', 'east', 'north', 'west', 'west', 'inv', 'east', 'north', 'west', 'west', 'north', 'south', 'west', 'east', 'north', 'north', 'south', 'south', 'east', 'east', 'south', 'east', 'south', 'east', 'west', 'east', 'east', 'south', 'north', 'west', 'west', 'west', 'east', 'north', 'west', 'north', 'west', 'north', 'north', 'east', 'west', 'south', 'south', 'west', 'north', 'north', 'inv', 'west']
while True:
	print('entering the game')
	commands = advent(code, commands, items=items)
	commands.pop()
	print(commands)
