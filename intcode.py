import collections
import os

def read(filename):
	with open(filename, 'r') as f:
		a = f.read()
	a = a.split(',')
	return [int(x) for x in a]

class HaltException(Exception):
	pass

class InputBlockedException(Exception):
	pass

class Memory:
	def __init__(self, code):
		self.M = []
		for i, c in enumerate(code):
			self.set(i, c)

	def get(self, i):
		while i >= len(self.M):
			self.M.append(0)
		return self.M[i]

	def set(self, i, c):
		self.get(i)
		self.M[i] = c


class Runner:
	def __init__(self, code, ins=None):
		self.M = Memory(code)
		self.halted = False
		self.input = collections.deque([])
		self.rel_base = 0
		for v in (ins or []):
			self.push(v)
		self.pc = 0

	def push(self, v):
		self.input.append(v)

	def run(self):
		if self.halted:
			raise HaltException
		M = self.M

		def read(i, mode):
			if mode == 0:
				return M.get(M.get(i))
			if mode == 1:
				return M.get(i)
			if mode == 2:
				return M.get(M.get(i) + self.rel_base)
			assert False, "unknown mode %s" % mode

		def read_addr(i, mode):
			if mode == 0:
				return M.get(i)
			if mode == 2:
				return M.get(i) + self.rel_base
			assert False, "unknown mode %s" % mode

		while True:
			pc = self.pc
			ins = M.get(pc)
			op4m = (ins // 100000) % 10
			op3m = (ins // 10000) % 10
			op2m = (ins // 1000) % 10
			op1m = (ins // 100) % 10
			de = ins % 100


			assert de + 100 * op1m + 1000 * op2m + 10000 * op3m + 100000 * op4m == ins
			if de == 1: # add
				op1 = read(pc+1, op1m)
				op2 = read(pc+2, op2m)
				op3 = read_addr(pc+3, op3m)
				M.set(op3, op1 + op2)
				self.pc += 4
			elif de == 2: # mul
				op1 = read(pc+1, op1m)
				op2 = read(pc+2, op2m)
				op3 = read_addr(pc+3, op3m)
				M.set(op3, op1 * op2)
				self.pc += 4
			elif de == 3: # input
				if not self.input:
					raise InputBlockedException
				op1 = read_addr(pc+1, op1m)
				i = self.input.popleft()
				M.set(op1, i)
				self.pc += 2
			elif de == 4: # output
				op1 = read(pc+1, op1m)
				self.pc += 2
				return op1
			elif de == 5: # jump-if-true
				op1 = read(pc+1, op1m)
				op2 = read(pc+2, op2m)
				if op1:
					self.pc = op2
				else:
					self.pc += 3
			elif de == 6: # jump-if-false
				op1 = read(pc+1, op1m)
				op2 = read(pc+2, op2m)
				if not op1:
					self.pc = op2
				else:
					self.pc += 3
			elif de == 7: # less-than
				op1 = read(pc+1, op1m)
				op2 = read(pc+2, op2m)
				op3 = read_addr(pc+3, op3m)
				M.set(op3, 1 if op1 < op2 else 0)
				self.pc += 4
			elif de == 8: # equals
				op1 = read(pc+1, op1m)
				op2 = read(pc+2, op2m)
				op3 = read_addr(pc+3, op3m)
				M.set(op3,1 if op1 == op2 else 0)
				self.pc += 4
			elif de == 9: # set relative base
				op1 = read(pc+1, op1m)
				self.rel_base += op1
				self.pc += 2
			elif de == 99:
				self.halted = True
				raise HaltException
			else:
				assert False, "unknown instruction %s" % ins


def run(prog, inp):
	r = Runner(prog)
	for i in inp:
		r.push(i)
	outz = []

	while True:
		try:
			outz.append(r.run())
		except HaltException:
			break
	return outz


tests = [
	# input is equal to 8, pos mode
	[[3,9,8,9,10,9,4,9,99,-1,8], [7], [0]],
	[[3,9,8,9,10,9,4,9,99,-1,8], [8], [1]],
	[[3,9,8,9,10,9,4,9,99,-1,8], [123], [0]],

	# input is less than 8, pos mode
	[[3,9,7,9,10,9,4,9,99,-1,8], [-12], [1]],
	[[3,9,7,9,10,9,4,9,99,-1,8], [7], [1]],
	[[3,9,7,9,10,9,4,9,99,-1,8], [8], [0]],
	[[3,9,7,9,10,9,4,9,99,-1,8], [9], [0]],

	# input is equal to 8, imm mode
	[[3,3,1108,-1,8,3,4,3,99], [7], [0]],
	[[3,3,1108,-1,8,3,4,3,99], [8], [1]],
	[[3,3,1108,-1,8,3,4,3,99], [123], [0]],

	# input is less than 8, imm mode
	[[3,3,1107,-1,8,3,4,3,99], [-12], [1]],
	[[3,3,1107,-1,8,3,4,3,99], [7], [1]],
	[[3,3,1107,-1,8,3,4,3,99], [8], [0]],
	[[3,3,1107,-1,8,3,4,3,99], [9], [0]],

	# input non-zero, pos mode
	[[3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [0], [0]],
	[[3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [1], [1]],
	[[3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [-1], [1]],

	# input non-zero, imm mode
	[[3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [0], [0]],
	[[3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [1], [1]],
	[[3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [-1], [1]],

	# 999 if input < 8, 1000 if input == 8, 1001 if input > 8
	[[3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
	  1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
	  999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], [-3], [999]],
	[[3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
	  1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
	  999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], [7], [999]],
	[[3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
	  1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
	  999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], [8], [1000]],
	[[3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
	  1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
	  999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], [9], [1001]],
	[[3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
	  1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
	  999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], [15], [1001]],

	# day9 test cases
	[[109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], [],
	 [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]],
	[[1102,34915192,34915192,7,4,7,99,0], [], [1219070632396864]],
	[[104,1125899906842624,99], [], [1125899906842624]],

]

print('running unit tests:')
failed = 0
count = 0
for C, ins, want in tests:
	count += 1
	try:
		got = run(C[:], ins)
		if got != want:
			print("test(%s) = %s, want %s" % ((C, ins), got, want))
			failed += 1
	except Exception as exp:
		print("test(%s) crashed with exception %s" % ((C, ins), exp))
		failed += 1
print("%d/%d PASSED" %(count - failed, count))
if failed:
	os.exit(1)
