"""
Week 9
Code up the clustering algorithm from lecture 
for computing a max-spacing k-clustering.
"""
from indexMinPQ import MinPQ
from UnionFind import WeightedQuickUnionUF as UF
from decimal import Decimal
_INF = Decimal('infinity')

class Edge(object):
    "defines an undirected, weighted edge"
    def __init__(self, v, w, wt):
        self.v = v
        self.w = w
        self.wt = wt

    def either(self):
        return self.v

    def other(self, v):
        if v == self.v:
            return self.w
        else:
            return self.v

    def __gt__(self, that):
        return self.wt > that.wt

    def __lt__(self, that):
        return self.wt < that.wt

    def __eq__(self, that):
        return self.wt == that.wt

    def weight(self):
        return self.wt

    def __repr__(self):
        "This is everything you need to know about an edge"
        return "Edge(v=%r, w=%r, wt=%r)" % (self.v, self.w, self.wt)

class K_Cluster(object):
    """Find the k-cluster with the max minimum separation
    using Kruskal's algorithm"""
    
    def __init__(self, V, pq, k=4):
        "given a min pq of weighted edges, find the k-cluster with the max minimum separation"
        # list of edges in mst
        self._weight = 0
        self._pq = pq

        # build union-find data structure
        uf = UF(V)
        while (not self._pq.isEmpty() and uf.count() > k):
            # get next edge from PQ
            e = self._pq.delMin()                
            v = e.either()
            w = e.other(v)
            if (not uf.connected(v, w)):        # edge v-w does not create a cycle
                uf.union(v, w)                  # merge components
        if uf.count() == k:
            # get weight of next edge that does not create a cycle
            while True:
                e = self._pq.delMin()               
                v = e.either()
                w = e.other(v)
                if (not uf.connected(v, w)):
                    self.spacing = e.weight()
                    break
        else:
            print("error - pq is empty")


    def separation(self):
        "returns sum of weights of MST"
        return self.spacing

    def __repr__(self):
        "Everything about MST"
        return "edges=%r wt=%r" % ([e for e in self.mst()], self.weight())

######################################### 
if __name__ == "__main__":
    filename = "C:/Users/lbklein/_COURSES/StanfordAlgorithms/Week8/clustering1.txt"
    #filename = "C:/Users/lbklein/_COURSES/StanfordAlgorithms/Week8/hw2_1_tc_10.txt"
    pq = MinPQ()

    with open(filename, 'r', encoding='utf-8') as f:
        V = int(f.readline().strip())
        edges = (edge.strip().split() for edge in f) # [u, v, wt]
        for e in edges:
            EG = Edge(int(e[0]) - 1, int(e[1]) - 1, int(e[2]))  # nodes start from 0
            # add edges to the min priority queue
            pq.insert(EG)

    kcluster = K_Cluster(V, pq)
    s = kcluster.separation()
    print(s)

