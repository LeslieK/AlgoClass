"""
Find the largest value of k such that there is a k-clustering 
with spacing at least 3. Also, connect each cluster.
That is, how many clusters are needed to 
ensure that no pair of nodes with all but 2 bits in common get split 
into different clusters?
distance measure = hamming distance between points
"""
from UnionFind import RankQuickUnionUF as UF
import itertools
from collections import deque

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

class DFSCluster(object):
    """
    The graph is complete and implicit
    """
    def __init__(self):
        self.num_nodes = len(NodeST)  # number of unique nodes
        self.uf = UF(self.num_nodes)
        self.q = deque()
        for v in NodeST:
            i = NodeST[v]
            r = self.uf.find(i)
            if self.uf.rank(r) != 0:
                # v is already in a cluster
                continue
            self.bfs(v)

    def bfs(self, v):
        """
        find all vertices connected to v
        v: int(label, 2)
        i: index of v"""
        i = NodeST[v]
        self.q.append(v)
        while len(self.q) > 0:
            v = self.q.popleft()
            for w in nextNode(v):
                j = NodeST[w]
                if not self.uf.connected(i, j):
                    self.uf.union(i, j)
                    self.q.append(w)

    def count(self):
        """
        returns the number of clusters
        """
        return self.uf.count()

##############################
if __name__ == "__main__":
    filename = "C:/Users/lbklein/_COURSES/StanfordAlgorithms/Week8/clustering_big.txt" # ANSWER: 6118

    with open(filename, 'r', encoding='utf-8') as f:
        V, number_bits = list(map(int, f.readline().strip().split()))
        NodeST = {}
        nodes = (''.join(node.strip().split()) for node in f)
        i = 0
        for node in nodes:
            n = int(node, 2)
            if n not in NodeST:
                NodeST[n] = i
                i += 1

    masks = shiftDict(number_bits)
    kcluster = DFSCluster()
    x = kcluster.count()
    print('x', x)



