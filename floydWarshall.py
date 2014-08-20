from collections import Counter

class DEdge(object):
	"defines a directed, weighted edge"
	def __init__(self, v, w, weight):
		self._v = v
		self._w = w
		self._wt = weight

	def src(self):
		return self._v

	def sink(self):
		return self._w

	def weight(self):
		return self._wt

	def compareTo(self, that):
		if (self._wt < that.weight()):
			return -1
		elif (self._wt > that.weight()):
			return 1
		else:
			return 0

	def __repr__(self):
		"This is everything you need to know about a weighted directed edge"
		return "%r -> %r %r " % (self._v, self._w, self._wt)

class EdgeWeightedDigraph(object):
    "a directed graph with weighted edges"
    def __init__(self, V, EG=None):
        # constructs a graph
        self._V = V
        self._E = 0
        self._adj = [None] # placeholder in index 0
        for v in range(1, self._V + 1):
            # bag of weighted edges incident on each v
            self._adj.append(Counter())

    def V(self):
        "returns number of vertices"
        return self._V

    def E(self):
        "returns number of edges"
        return self._E

    def addEdge(self, e):
        "add weighted edge v->w to graph"
        v = e.src()
        self._adj[v][e] += 1
        self._E += 1

    def adj(self, v):
        "return all edges incident on v"
        return self._adj[v]

    def edges(self):
        "returns a list of edges"
        edge_list = []
        for v in range(1, self._V + 1):
            for e in self._adj[v]:
                if self._adj[v][e] > 0:
                    edge_list.append(e)
        return edge_list

    def __repr__(self):
        "Everything you need to know about a weighted digraph"
        return "V=%r, E=%r, edges=%r" % (self._V, self._E, [e for e in
                                         self.edges()])

    def removeEdge(self, e):
        v = e.src()
        self._adj[v][e] = self._adj[v][e] - 1
        if self._adj[v][e] == 0:
            # remove edge from Counter
            del self._adj[v][e]
        self._E -= 1

import numpy as np

class AllpairsShortestpathsALT(object):
    """
    returns the number of paths from i to j
    build 3-D array
    return A[i, j, k=n] for all i, j
    i = source
    j = target
    k = {1, 2, 3, ..., k} internal nodes that can be on i-j path
    """
    def __init__(self, G):
        self.V = G.V()  # number of vertices
        self.E = G.E()

        self.A = np.zeros(shape=(self.V + 1, self.V + 1, self.V + 1), dtype=int)

        for v in range(1, self.V + 1):
            for e in G.adj(v):
                w = e.sink()
                self.A[v, w, 0] = e.weight()
        #for k in range(0, self.V + 1):
        #    print(k, self.A[:, :, k])

        for k in range(1, self.V + 1):
            for i in range(1, self.V + 1):
                for j in range(1, self.V + 1):
                    self.A[i, j, k] = self.A[i, j, k - 1] + self.A[i, k, k - 1] * self.A[k, j, k - 1]

class AllpairsShortestpaths(object):
    """
    returns the number of paths from i to j
    build 3-D array
    return A[i, j, k=n] for all i, j
    i = source
    j = target
    k = {1, 2, 3, ..., k} internal nodes that can be on i-j path
    """
    def __init__(self, G):
        self.V = G.V()  # number of vertices
        self.E = G.E()

        self.A = np.zeros(shape=(self.V + 1, self.V + 1, self.V + 1), dtype=float)
        self.A[:,:,:] = np.inf
        b = np.eye(self.V + 1, self.V + 1, dtype=bool)
        self.A[0][b] = 0
        # B stores last vertex in i-j path for each (i, j)
        self.B = np.zeros(shape=(self.V + 1, self.V + 1), dtype=int)

        for v in range(1, self.V + 1):
            for e in G.adj(v):
                w = e.sink()
                self.A[0, v, w] = e.weight()
                self.B[v, w] = v

        for k in range(1, self.V + 1):          # set of nodes on path {1, 2, ..., k}
            for i in range(1, self.V + 1):      # row
                for j in range(1, self.V + 1):  # col
                    a = self.A[k - 1, i, j]
                    b = self.A[k - 1, i, k]
                    c = self.A[k - 1, k, j]
                    d = b + c
                    if d < a:
                        self.B[i, j] = k
                    self.A[k, i, j] = min(self.A[k - 1, i, j], self.A[k - 1, i, k] + self.A[k - 1, k, j])
        assert (not self.hasNegativeCycle()), print('negative cycle exists')

    def allPaths(self):
        return self.A[self.V, :, :]

    def shortestShortestPath(self):
        return min(self.A[self.V, :, :])

    def hasNegativeCycle(self):
        """returns True if neg cycle exists"""
        b  = np.eye(self.V, self.V, dtype=bool)
        if np.sum(self.A[self.V, 1:, 1:][b]) < 0:
            return True
        else:
            return False


########################################## 
if __name__ == "__main__":
    #with open("tinyEWDigraph.txt", 'r', encoding='utf-8') as f:
    with open("c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week10/tinyEWDn.txt", 'r', encoding='utf-8') as f:
    #with open("c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week10/tinyEWDnc.txt", 'r', encoding='utf-8') as f:
    #with open("microEWDigraph.txt", 'r', encoding='utf-8') as f:
    #with open("tinyEWDigraph_scc.txt", 'r', encoding='utf-8') as f:
        V = int(f.readline().strip())
        E = int(f.readline().strip())
        G = EdgeWeightedDigraph(V)

        lines = (line.strip().split() for line in f)
        for line in lines:
            u, v, wt = line
            G.addEdge(DEdge(int(u) + 1, int(v) + 1, float(wt)))

    apsp = AllpairsShortestpaths(G)
    print(apsp.hasNegativeCycle())
    for i in range(1, V + 1):
        for j in range(1, V + 1):
            print(i - 1, j - 1, apsp.A[V, i, j])



