"""
Adds virtual source input graph G
Use BellmanFord to find shortest path from virtual source
Shortest path distance equals the shortest shortest i-j path
"""
from bellmanFord import BellmanFordSP
from bellmanFord import DEdge
from collections import Counter

class VirtualSP(object):
    """
    1 invocation of BellmanFord from a virtual source
    """
    def __init__(self, adj):
        self.V = len(adj) - 1
        self.hasNegCycle = False

        # original graph
        self.adj = adj

        self.virtual_src = 0
        #self.virtual_sink = V + 1  # comment out for 1 virtual source

        # connect virtual source to all vertices (edge cost is 0)
        self.modGraph()

        self.bf = BellmanFordSP(self.adj, self.virtual_src)
        if self.bf.hasNegativeCycle():
            self.hasNegCycle = True
        else:
            self.d = self.bf.shortestShortestPath()    #  uncomment  for 1 virtual source
            #self.d = self.bf.distTo[self.virtual_sink]  # comment out for 1 virtual source

    #def modGraph(self):
    #    """
    #    returns graph G' (mutates self.adj)
    #    G': virtual src connected to each vertex with edge cost = 0
    #    virtual sink connected to each vertex with edge cost = 0
    #    """
    #    self.adj[self.virtual_src] = Counter()
    #    self.adj.append(Counter())

    #    for v in range(1, self.V + 1):
    #        e = DEdge(self.virtual_src, v, 0.)
    #        self.adj[self.virtual_src][e] += 1
    #        e = DEdge(v, self.virtual_sink, 0.)
    #        self.adj[v][e] += 1


    def modGraph(self):
        """
        returns graph G' (mutates self.adj)
        G': virtual src connected to each vertex with edge cost = 0
        """
        self.adj[self.virtual_src] = Counter()
        self.adj.append(Counter())
        for v in range(1, self.V + 1):
            e = DEdge(self.virtual_src, v, 0.)
            self.adj[self.virtual_src][e] += 1

    def shortestShortestPath(self):
        if not self.hasNegCycle:
            return self.d

####################################
if __name__ == "__main__":

    filename = "c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week10/large.txt" # ANSWER = -6
    #filename = "c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week10/g3.txt" # ANSWER = -19
    #filename = "c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week10/g1.txt" # ANSWER = negative cycle
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
    vspt = VirtualSP(adj)
    if vspt.hasNegCycle:
        print('negative cycle exists')
        vspt.bf.findNegativeCycle()
        print(vspt.bf.cycle)
    else:
        print(vspt.shortestShortestPath())



