from collections import Counter

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

    def compareTo(self, that):
        if (self.wt < that.weight()):
            return -1
        elif (self.wt > that.weight()):
            return 1
        else:
            return 0

    def weight(self):
        return self.wt

    def __repr__(self):
        "This is everything you need to know about an edge"
        return "Edge(v=%r, w=%r, wt=%r)" % (self.v, self.w, self.wt)
    
class EdgeWeightedGraph(object):
    "An undirected graph with weighted edges"
    def __init__(self, V=None, EG=None):
        if V:
            # constructs a graph
            self._V = V
            self._E = 0
            self._adj = []
            for _ in range(self._V):
                # bag of weighted edges incident on each v
                self._adj.append(Counter())
        elif EG:
            # constructs a copy of graph EG
            self._V = EG.V()
            self._E = EG.E()
            self._adj = []
            for v in range(self._V):
                self._adj.append(EG.adj(v))
        else:
            return "Error: missing argument"

    def V(self):
        return self._V

    def E(self):
        return self._E

    def addEdge(self, e):
        "add weighted edge v-w to graph"
        v = e.either()
        w = e.other(v)
        self._adj[v][e] += 1
        self._adj[w][e] += 1
        self._E += 1

    def adj(self, v):
        "return all edges incident on v"
        return self._adj[v]

    def edges(self):
        "returns a list of edges"
        edge_list = []
        for v in range(self._V):
            selfLoops = 0
            for e in self._adj[v]:
                if e.other(v) > v:
                    edge_list.append(e)
                elif e.other(v) == v:
                    if (selfLoops % 2 == 0):
                        edge_list.append(e)
                        selfLoops += 1
        return edge_list

    def __repr__(self):
        "Everything you need to know about a weighted graph"
        return "V=%r, E=%r, edges=%r" % (self._V, self._E, [e for e in
                                         self.edges()])