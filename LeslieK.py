"""
Find the largest value of k such that there is a k-clustering 
with spacing at least 3. 
That is, how many clusters are needed to 
ensure that no pair of nodes with all but 2 bits in common get split 
into different clusters?
distance measure = hamming distance between points
"""

import itertools

def shiftDict(number_bits):
	"""
	returns dictionary of bit masks
	"""
	d = {0: 1}
	for i in range(1, number_bits):
		d[i] = d[i - 1] * 2

	it2 = itertools.combinations(range(number_bits), 2)
	for t in it2:
		x, y = t
		d[t] = d[x] | d[y]
	return d

def nextNode(p):
	"""
	p: base 2 value of label
	"""
	for m in masks:
		new_node = p ^ masks[m]
		if new_node in NodeST:
			yield new_node

def DFS():
	cluster_count = 0
	while len(NodeST) > 0:
		v = NodeST.pop()				# starting vertex for new cluster
		cluster_count += 1
		stack = [v]
		while len(stack) > 0:
			w = stack.pop()				# find all its neighbors
			for u in nextNode(w):
				NodeST.discard(u)
				stack.append(u)			# new vertex that was absorbed into the cluster
			
	return cluster_count

##############################
if __name__ == "__main__":
	filename = "../clustering_big.txt" # ANSWER: 6118

	with open(filename, 'r') as f:
		V, number_bits = list(map(int, f.readline().strip().split()))
		NodeST = set()
		nodes = (''.join(node.strip().split()) for node in f)
		for node in nodes:
			n = int(node, 2)
			NodeST.add(n)

	masks = shiftDict(number_bits)

	print('Starting ...')

	x = DFS()
	print('x', x)

	raw_input('Press any key to continue . . . ')
