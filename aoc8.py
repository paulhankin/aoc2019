def decode(s, w, h):
	layers = []
	for i, c in enumerate(s):
		layer = i // (w * h)
		y = i % (w * h) // w
		x = i % (w * h) % w
		if layer >= len(layers):
			layers.append([])
		if y >= len(layers[-1]):
			layers[-1].append([])
		layers[-1][-1].append(c)
	if 0:
		for l in layers:
			for row in l:
				print(row)
			print()
	return layers

def load(filename, w, h):
	with open(filename, 'r') as f:
		s = f.read()
	return decode(s, w, h)

def count(layer, c):
	return sum(y.count(c) for y in layer)

def compose(layers):
	h = len(layers[0])
	w = len(layers[0][0])
	r = [[None] * w for _ in range(h)]
	print(layers)
	for y in range(h):
		for x in range(w):
			px = '2'
			for layer in layers:
				if px != '2':
					break
				px = layer[y][x]
			r[y][x] = px
	return r

img = load('aoc8.txt', 25, 6)
best = min(img, key=lambda layer: count(layer, '0'))
ones = count(best, '1')
twos = count(best, '2')
print(ones * twos)

if 0:
	for layer in img:
		for row in layer:
			print (''.join(row))
		print()

print('composed')

for row in compose(img):
	print(''.join(row).replace('0', ' '))
