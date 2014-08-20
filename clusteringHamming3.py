"""
Find the largest value of k such that there is a k-clustering 
with spacing at least 3. 
That is, how many clusters are needed to 
ensure that no pair of nodes with all but 2 bits in common get split 
into different clusters?
distance measure = hamming distance between points
"""
import itertools
from collections import deque

def shiftDict(number_bits):
	"""
	returns list of bit masks
    mask: number_bits with either 1 or 2 bits set (distance = 1 or 2)
    mask bit 1: generate new label by flipping bit in current label
    mask bit 0: generate new label with same bit as current label
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
        new_node = p ^ m  # xor
        if new_node in NodeST:
            yield new_node

class DFSCluster(object):
    """
    V: number of nodes
    The graph is complete and implicit
    """
    def __init__(self):
        self.num_nodes = len(NodeST)  # number of unique nodes
        self.q = deque()
        self.marked = set()
        self.count = 0
        for v in NodeST:
            if v in self.marked:
                # v is already in a cluster
                continue
            self.bfs(v)
            self.count += 1

    def bfs(self, v):
        """
        find all vertices connected to v
        v: int(label, 2)
        i: index of v"""
        self.marked.add(v)
        self.q.append(v)
        while len(self.q) > 0:
            v = self.q.popleft()
            for w in nextNode(v):
                if w not in self.marked:
                    self.marked.add(w)
                    self.q.append(w)

    def clusters(self):
        """
        returns the number of clusters
        """
        return self.count

##############################
if __name__ == "__main__":
    filename = "C:/Users/lbklein/_COURSES/StanfordAlgorithms/Week8/clustering_big.txt" # ANSWER: 6118
    with open(filename, 'r', encoding='utf-8') as f:
        V, number_bits = list(map(int, f.readline().strip().split()))
        NodeST = set()
        nodes = (''.join(node.strip().split()) for node in f)
        for node in nodes:
            n = int(node, 2)
            NodeST.add(n)
            #if n not in NodeST:
            #    NodeST.add(n)

    masks = shiftDict(number_bits)
    print('Starting...')
    kcluster = DFSCluster()
    x = kcluster.clusters()
    print('x', x)



