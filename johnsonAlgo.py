"""
Johnson's algorithm
1. modify graph G (call it G'): add virtual source and connect to all vertices with weight 0
2. run Bellman-Ford on G'; distTo[v] is p_v (vertex weight) or report negative cycle
3. in graph G: re-weight edge costs: c_e' = c_e + p_u - p_v
4. run n x DijkstraAllPairsSP(u) on G (1x from each source)
5. subtract p_u - p_v from path value for each u-v path in step 4
u -> v
"""
from collections import Counter
from bellmanFord import BellmanFordSP
from dijkstraAllpaths import DijkAllPairsSP

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

class Johnson(object):
    """
    runs Johnson's algo on graph
    """
    def __init__(self, adj):
        self.V = len(adj) - 1
        self.hasNegCycle = False

        # original graph
        self.adj = adj

        self.virtual_src = 0

        # stores graph with reweighted edge costs
        self.adj_prime = None  

        self.modGraph()
        self.bf = BellmanFordSP(self.adj, self.virtual_src)
        if self.bf.hasNegativeCycle():
            self.hasNegCycle = True
        else:
            # builds new graph with adjusted edge costs (in self.adj_prime)
            self.reweightEdgeCosts()

            self.djk = DijkAllPairsSP(self.adj_prime)

            # mutates self.djk
            self.adjustWeights()      

    def hasNegativeCycle(self):
        return self.hasNegCycle

    def shortestShortestPath(self):
        # return shortest of all shortest s-t paths
        d = self.djk.shortestShortestPath()
        return d

    def modGraph(self):
        """
        returns graph G' (mutates self.adj)
        G': virtual src connected to each vertex with edge cost = 0
        """
        self.adj[self.virtual_src] = Counter()
        for v in range(1, self.V + 1):
            e = DEdge(self.virtual_src, v, 0.)
            self.adj[self.virtual_src][e] += 1

    def reweightEdgeCosts(self):
        """
        v -> w
        c' = c + pv - pw
        c': new edge cost (wt)
        c: original edge cost (wt)
        pv: cost of vertex v (tail)
        pw: cost of vertex w (head)
        """
        self.adj_prime = [None]
        for v in range(1, self.V + 1):
            self.adj_prime.append(Counter())

        for v in range(1, self.V + 1):
            for e in self.adj[v]:
                # edge e is leaving vetex v
                w = e.sink()
                #wt = e.weight() + self.bf.distTo[v] - self.bf.distTo[w]
                #self.adj_prime[v][DEdge(v, w, wt)] += 1
                # mutate e._wt (bad practice)
                e._wt = e._wt + self.bf.distTo[v] - self.bf.distTo[w]
                self.adj_prime[v][e] += 1

    def adjustWeights(self):  # shortest paths-all pairs object
        for s in range(1, self.V + 1):
            for t in range(1, self.V + 1):
                # adjustements made with endpoints of path, s and t
                self.djk._dijkObjs[s]._distTo[t] += (self.bf.distTo[t] - self.bf.distTo[s])

###########################################
if __name__ == "__main__":

    #filename = "c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week10/tinyEWDn_Stanford.txt"
    #filename = "c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week10/g1.txt" # has negative cycle
    #filename = "c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week10/g2.txt" # has negative cycle
    #filename = "c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week10/g3.txt" # ANSWER = -19.0
    filename = "c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week10/large.txt" # ANSWER = -6

    with open(filename, 'r', encoding='utf-8') as f:
        V, E = list(map(int, f.readline().strip().split()))

        # adjacency list
        adj = [None]
        for v in range(1, V + 1):
            adj.append(Counter())

        lines = (line.strip().split() for line in f)
        for line in lines:
            v, w, wt = line
            #v, w, wt = int(v) + 1, int(w) + 1, float(wt) # add 1 for Princeton files
            v, w, wt = int(v), int(w), float(wt) # don't add 1 for Stanford files
            e = DEdge(v, w, wt)
            adj[v][e] += 1

    jj = Johnson(adj)
    if jj.hasNegativeCycle():
        print('negative cycle found')
    else:
        d = jj.shortestShortestPath()
        print(d)

