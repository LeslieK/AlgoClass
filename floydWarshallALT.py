"""
Problem Set 4, Question 3
Consider a directed graph in which every edge has length 1. Suppose we run the Floyd-Warshall algorithm with the 
following modification: instead of using the recurrence
 
A[i,j,k] = min{A[i,j,k-1], A[i,k,k-1] + A[k,j,k-1]}, 

we use the recurrence
 
A[i,j,k] = A[i,j,k-1] + A[i,k,k-1] * A[k,j,k-1]. 

For the base case, set A[i,j,0] = 1 if (i,j) is an edge and 0 otherwise.
 
What does this modified algorithm compute -- specificially, 
what is A[i,j,n] at the conclusion of the algorithm?

ANSWER: computes the number of i-j paths (counts simple and non-simple paths)
"""

import numpy as np
from indexMinPQ import IndexMinPQ
from collections import Counter

class EdgeWeightedDigraph(object):
    "a directed graph with weighted edges"
    def __init__(self, V):
        # constructs a graph
        self._V = V
        self._E = 0
        self._adj = [None]
        for _ in range(1, self._V + 1):
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

	def __lt__(self, other):
		return self.weight() < other.weight()

	def __repr__(self):
		"This is everything you need to know about a weighted directed edge"
		#Edge(from=%r, to=%r, wt=%r)" % (self._v, self._w, self._wt)
		return "%r -> %r %r " % (self._v, self._w, self._wt)

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

####################################################

if __name__ == "__main__":

    #filename = "tinyEWDigraph_1.txt"
    filename = "testALT_1.txt"

    with open(filename, 'r', encoding='utf-8') as f:
        V, E = list(map(int, f.readline().strip().split()))
        G = EdgeWeightedDigraph(V)

        lines = (line.strip().split() for line in f)
        for line in lines:
            v, w, wt = line
            v, w, wt = int(v), int(w), float(wt)
            G.addEdge(DEdge(v, w, wt))

    apsp = AllpairsShortestpathsALT(G)
    for i in range(1, V + 1):
        for j in range(1, V + 1):
            print(i, j, apsp.A[i, j, V])