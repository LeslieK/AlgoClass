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
            self._adj.append(Counter())  # starts from index 1

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
        for v in range(1, self._V + 1): # starts from 1
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

class DijkSP(object):
    def __init__(self, adj, s, t=None):
        """find the shortest path tree (in a directed graph with non-negative
        weights) from s to every other vertex using Dijkstra's alg"""

        self.V = len(adj) - 1  # adj[0] is None

        self._s = s
        self._distTo = np.zeros(self.V + 1, dtype=float)
        self._distTo[:] = np.inf
        self._distTo[s] = 0.
        # edgeTo[v]: last edge on shortest path from s to v
        # self._edgeTo = np.zeros(self.V + 1, dtype=int)
        self._pq = IndexMinPQ(self.V + 1)  # pq thinks we are using 9 vertices, 0 - 8
        self._pq.insert(s, 0.0)

        while (not self._pq.isEmpty()):
            v = self._pq.delMin()   # add closest vertex to source to Tree
            if t and v == t:
                return
            for e in adj[v]:
                self._relax(e)      # relax(e) updates distTo, edgeTo

    def distanceTo(self, v):
        "distance from src to vertex v"
        return self._distTo[v]

    def hasPathTo(self, v):
        "checks whether path exists from src to vertex v"
        #return self._edgeTo[v] != _SENTINEL
        return self._distTo[v] != np.inf

    #def pathTo(self, v):
    #    "returns path from src to vertex v"
    #    if not self.hasPathTo(v):
    #        return
    #    path = []
    #    e = self._edgeTo[v]                 # last edge of path
    #    while e.src() != self._s:
    #        path.append(e)
    #        e = self._edgeTo[e.src()]
    #    path.append(e)
    #    return path[::-1]

    def _relax(self, edge):
        "relaxes an edge by updating data structures with that edge"
        v = edge.src()
        w = edge.sink()
        if self._distTo[w] > self._distTo[v] + edge.weight():
            # distance to src
            self._distTo[w] = self._distTo[v] + edge.weight()
            #self._edgeTo[w] = edge
            if not self._pq.contains(w):
                self._pq.insert(w, self._distTo[w])
            else:
                self._pq.decreaseKey(w, self._distTo[w])

    def shortestShortestPath(self):
        """returns the length of the shortest shortest path 
        from the source"""
        m = np.ones(self.V + 1, dtype=bool)
        m[self._s] = False
        x = np.min(self._distTo[m])
        return x

    #def __repr__(self):
    #    "print spt built by Dijkstra object"
    #    V = len(self._edgeTo)
    #    spt = EdgeWeightedDigraph(V)
    #    for i in range(1, V + 1):
    #        #if self._edgeTo[i] != _SENTINEL:
    #        if self._edgeTo[i] > 0:
    #            spt.addEdge(self._edgeTo[i])
    #    print(str(spt.edges()))

class DijkAllPairsSP(object):
    def __init__(self, adj):
        """finds shortest path in a directed, edge-weighted graph
        from source s to target t"""

        self.V = len(adj) - 1
        
        self._dijkObjs = [None]
        for s in range(1, self.V + 1):
            self._dijkObjs.append(DijkSP(adj, s))

    def hasPath(self, s, t):
        "checks whether path exists from s to t"
        return self._dijkObjs[s].hasPath(t)

    #def pathTo(self, s, t):
    #    "returns path from src to vertex v"
    #    if not self._dijkObjs[s].hasPathTo(t):
    #        return
    #    return self._dijkObjs[s].pathTo(t)

    def distanceTo(self, s, t):
        "distance from src s to vertex v"
        return self._dijkObjs[s].distanceTo(t)

    def shortestShortestPath(self):
        """returns the shortest shortest path from any source"""
        shortestpaths = np.zeros(self.V + 1, dtype=float)
        shortestpaths[:] = np.inf

        for s in range(1, self.V + 1):
            shortestpaths[s] = self._dijkObjs[s].shortestShortestPath()
        return np.min(shortestpaths)

#####################################################
if __name__ == "__main__":

    source = 1
    filename = "tinyEWDigraph_Stanford.txt"

    with open(filename, 'r', encoding='utf-8') as f:
        V, E = list(map(int, f.readline().strip().split()))
        # adjacency list
        adj = [None]
        for v in range(1, V + 1):
            adj.append(Counter())

        lines = (line.strip().split() for line in f)
        for line in lines:
            v, w, wt = line
            v, w, wt = int(v) + 1, int(w) + 1, float(wt) # add 1 for Princeton files
            #v, w, wt = int(v), int(w), float(wt) # don't add 1 for Stanford files
            e = DEdge(v, w, wt)
            adj[v][e] += 1

    spt = DijkAllPairsSP(adj)
    d = spt.shortestShortestPath()
    print(d)
