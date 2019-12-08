import itertools


def valid(x):
	s = str(x)
	return s == ''.join(sorted(s)) and 2 in set(sum(1 for _ in g) for _, g in itertools.groupby(s))

print(sum(valid(i) for i in range(146810, 612565)))

