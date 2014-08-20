"""
finds shortest path from single source if no negative cycles are
reachable from src
Graph can contain cycles; Graph can contain negative edges
Does not specify the order in which the vertices are relaxed
"""
import numpy as np
from collections import deque
from collections import Counter

class EdgeWeightedCycleFinder(object):
    """
    returns a cycle, if there is one, in a directed, edge-weighted digraph
    otherwise, returns None
    uses depth-first search
    """
    def __init__(self, G):
        self.V = G.V()
        self.marked = np.zeros(self.V + 1, dtype=bool)
        self.onStack = np.zeros(self.V + 1, dtype=bool)
        self.cycle = []
        self.edgeTo = [None] * (self.V + 1)
        for v in range(1, self.V + 1):
            if (not self.marked[v]):
                self.dfs(G, v)

    def dfs(self, G, v):
        self.onStack[v] = True
        self.marked[v] = True
        for e in G.adj(v):
            w = e.sink()

            if self.cycle != []:
                return

            # found new vertex
            elif (not self.marked[w]):
                self.edgeTo[w] = e
                self.dfs(G, w)

            elif (self.onStack[w]):
                # found a cycle
                while e.src() != w:
                    self.cycle.append(e)
                    e = self.edgeTo[e.src()]
                self.cycle.append(e)

        # done with v
        self.onStack[v] = False

    def hasCycle(self):
        """returns True if cycle exists"""
        return self.cycle != []

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

class BellmanFordSP(object):
    """queue-based Bellman-Ford
    only relax vertices whose distance has changed
    in the last iteration"""

    def __init__(self, adj, source):

        self.V = len(adj) - 1
        self.adj = adj
        self.source = source

        # set up data structures
        self.distTo = np.zeros(self.V + 1, dtype=float)
        self.distTo[:] = np.inf
        self.distTo[source] = 0.
        self.edgeTo = [DEdge(0, 0, 0.)] * (self.V + 1)
        self.cycle = []

        self.onQ = np.zeros(self.V + 1, dtype=bool)
        self.q = deque()
        self.q.append(source)
        self.onQ[source] = True
        self.cost = 0  # number of calls to relax()

        # loop ends as soon as q is empty (no more changes)
        # else it ends after V iterations (when neg cycle is detected)
        while len(self.q) > 0 and not self.hasNegativeCycle():
            v = self.q.popleft()
            self.onQ[v] = False
            self.relax(v)

    def relax(self, v):
        """relax all edges leaving v"""
        for e in self.adj[v]:
            w = e.sink()
            if self.distTo[w] > self.distTo[v] + e.weight():
                self.distTo[w] = self.distTo[v] + e.weight()
                self.edgeTo[w] = e
                if not self.onQ[w]:
                    # put w on queue
                    self.q.append(w)
                    self.onQ[w] = True
        self.cost += 1
        if self.cost % (self.V) == 0:
            # relaxed was called a multiple of V times
            self.findNegativeCycle()

    def findNegativeCycle(self):
        """builds graph using spt and uses dfs to find cycle in spt"""
        spt = EdgeWeightedDigraph(self.V)
        for v in range(1, self.V + 1):
            e = self.edgeTo[v]
            if e.src() > 0:  # 0 is not a valid vertex
                spt.addEdge(e)

        cf = EdgeWeightedCycleFinder(spt)
        self.cycle = cf.cycle

    def hasNegativeCycle(self):
        return self.cycle != []

    def shortestShortestPath(self):
        """returns shortest shortest path from source"""
        m = np.ones(self.V + 1, dtype=bool)
        m[self.source] = False
        return np.min(self.distTo[m])
        #if 1 < source < self.V:
        #    return min(min(self.distTo[1:source]), min(self.distTo[source+1:]))
        #elif source == 1:
        #    return min(self.distTo[2:])
        #elif source == self.V:
        #    return min(self.distTo[:source])

################################################### 
if __name__ == "__main__":
    #with open("tinyEWDigraph.txt", 'r', encoding='utf-8') as f:
    #with open("c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week10/tinyEWDn.txt", 'r', encoding='utf-8') as f:
    #with open("c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week10/tinyEWDnc.txt", 'r', encoding='utf-8') as f:
    #with open("microEWDigraph.txt", 'r', encoding='utf-8') as f:
    #with open("tinyEWDigraph_scc.txt", 'r', encoding='utf-8') as f:
    
    source = 1
    filename = "c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week10/tinyEWDnc_Stanford.txt"

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
            # v, w, wt = int(v), int(w), float(wt) # don't add 1 for Stanford files
            e = DEdge(v, w, wt)
            adj[v][e] += 1

    bf = BellmanFordSP(adj, source)
    if bf.hasNegativeCycle():
        print('test: has negative cycle')
        print(bf.cycle)
    else:
        print('test: no negative cycle')
        print(bf.shortestShortestPath())
