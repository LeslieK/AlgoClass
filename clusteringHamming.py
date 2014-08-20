"""
Find the largest value of k such that there is a k-clustering 
with spacing at least 3. 
That is, how many clusters are needed to 
ensure that no pair of nodes with all but 2 bits in common get split 
into different clusters?
distance measure = hamming distance between points
"""
from UnionFind import WeightedQuickUnionUF as UF
import itertools

def hammingDistance(p, q):
    """
    p, q: strings of 1s and 0s
    """
    N = len(p)
    if len(q) != N:
        return "p and q are different lengths"
    return sum(1 for i, j in zip(p, q) if i != j)

def nextNode(p):
    """
    p: a label
    yield a node with hamming distance of 1
    yield a node with hamming distance of 2
    """
    flipBit = {'1': '0', '0': '1'}

    it2 = itertools.combinations(range(number_bits), 2)

    for i in it2:
        x, y = i
        new_node_2 = p[:x] + flipBit[p[x]] + p[x+1:y] + flipBit[p[y]] + p[y+1:]
        if new_node_2 != p and new_node_2 in NodeST:
            yield new_node_2
    for x in range(number_bits):
        new_node_1 = p[:x] + flipBit[p[x]] + p[x+1:]
        if new_node_1 in NodeST:
            yield new_node_1

class DFSCluster(object):
    """
    V: number of nodes
    The graph is complete and implicit
    """
    def __init__(self):
        self.num_nodes = len(NodeST)  # number of unique nodes
        self.uf = UF(self.num_nodes)
        self.generators = [None] * self.num_nodes
        for v in NodeST:
            self.generators[NodeST[v]] = nextNode(v)  # nextNode(v) is a generator
        for v in NodeST:
            i = NodeST[v]
            r = self.uf.find(i)
            if self.uf.size(r) != 1:
                # v is already in a cluster
                continue
            self.dfs_iter(v)

    def dfs_iter(self, v):
        """
        run dfs starting at label v (index i)
        """
        i = NodeST[v]
        stack = []
        stack.append(i)
        while stack != []:
            i = stack[-1]
            try:
                w = self.generators[i].__next__()
            except StopIteration:
                # nextNode(v) is exhausted
                stack.pop()
                continue
            except GeneratorExit:
                self.generators[i].close()
                return
            j = NodeST[w]
            if not self.uf.connected(i, j):
                self.uf.union(i, j)
                stack.append(j)

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
            if node not in NodeST:
                NodeST[node] = i
                i += 1

    kcluster = DFSCluster()
    x = kcluster.count()
    print('x', x)



