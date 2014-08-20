"""
Find the largest value of k such that there is a k-clustering 
with spacing at least 3. 
That is, how many clusters are needed to 
ensure that no pair of nodes with all but 2 bits in common get split 
into different clusters?
distance measure = hamming distance between points
"""

def shiftDict(number_bits):
	"""
	returns list of bit masks
	"""
	d = []
	for i in range(number_bits):
		x = 1 << i
		d.append(x)
		for j in range(i + 1, number_bits):
			y = 1 << j
			d.append(x ^ y)
	return d

def nextNode(p):
	"""
	p: base 2 value of label
	"""
	for m in masks:
		new_node = p ^ m
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
	filename = "C:/Users/lbklein/_COURSES/StanfordAlgorithms/Week8/clustering_big.txt" # ANSWER: 6118

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

	#input('Press any key to continue . . . ')
