"""
Stanford Algorithms
Programming Assignment 6
2SAT satisfiablity
"""

from collections import Counter, deque

class Digraph(object):
    """defines a directed, unweighted graph"""
    def __init__(self, V):
        self._V = V
        self._adj = [None]     # vertex index starts at 1
        self._adjrev = [None]
        self._E = 0
        for v in range(1, self._V + 1):
            self._adj.append(Counter())
            self._adjrev.append(Counter())

    def addEdge(self, v, w):
        "add edge v - w (parallel edges and self-loops allowed)"
        if v < 0:
            v = abs(v) + number_variables
        if w < 0:
            w = abs(w) + number_variables

        self._adj[v][w] += 1
        self._adjrev[w][v] += 1  # add reverse arc w->v
        self._E += 1
        
    def adj(self, v):
        """return all vertices adjacent to v in G"""
        return self._adj[v]

    def adj_rev(self, v):
        """return all vertices adjacent to v in reverse G"""
        return self._adjrev[v]

    def V(self):
        "number of vertices"
        return self._V

    def E(self):
        "number of edges (incl self-loops and parallel edges)"
        return self._E

    def reverse(self):
        R = Digraph(self._V)
        for v in range(self._V):
            for w in self._adj[v]:
                R.addEdge(w, v)
        return R

    def __repr__(self):
        "Everything you need to know about a digraph"
        return "Digraph(V=%r, E=%r, edges=%r)" % (self.V(), self.E(), self.edges())

class ReversePostOrder(object):
    def __init__(self, G):
        """runs DFS on G
        returns vertices in reverse post order of G reverse"""
        self.V = G.V()
        self._marked = [False] * (self.V + 1)
        self._postorder = deque()
        for v in range(1, self.V + 1):
            if not self._marked[v]:
                self._dfs(G, v)
        del self._marked

    def _dfs(self, G, v):
        """runs dfs on G reverse"""
        self._marked[v] = True
        for w in G.adj_rev(v):
            if not self._marked[w]:
                self._dfs(G, w)
        # done with v
        self._postorder.appendleft(v)

    def postorder(self):
        return iter(self._postorder)

class SCC(object):
    def __init__(self, G):
        self.V = G.V()
        self._marked = [False] * (self.V + 1)
        self._id = [None] * (self.V + 1)  # stores the scc id for each vertex
        self._count = 0  # SCC id
        self._SCC_size = 0

        # pass 1: get reverse post order of G_reverse
        order = ReversePostOrder(G)

        # pass 2: run dfs on G using this order; build pq
        for v in order.postorder():
            if not self._marked[v]:
                self._dfs(G, v)  # all vertices visited from here are in same SCC
                self._count += 1
                self._SCC_size = 0
                         
        del self._marked

    def _dfs(self, G, v):
        self._marked[v] = True
        self._id[v] = self._count  # assign v to a SCC
        self._SCC_size += 1
        for w in G.adj(v):
            if not self._marked[w]:
                self._dfs(G, w)

    def isSatisfiable(self):
        """
        return False if v and not v are in same scc
        (strongly connected component)
        """
        for v in range(1, number_variables + 1):
            if self._id[v] == self._id[v + number_variables]:
                return False
        return True

########################################## 
#filename = "c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week12/tinySAT.txt"
filename = "c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week12/2sat6.txt"

with open(filename, 'r', encoding='utf-8') as f:
    number_variables = int(f.readline().strip())

    # range(1, number_variables + 1): terms (e.g., x1, x2)
    # range(number_variables + 1, number_variables * 2 + 1): not terms (!x1, !x2)
    # 1-1000: positive terms; 1001-2000: not terms
    G = Digraph(number_variables * 2)

    lines = (line.strip().split() for line in f)
    for line in lines:
        t1, t2 = list(map(int, line))
        G.addEdge(-t1, t2)
        G.addEdge(-t2, t1)

    # create strongly connected components (SCCs)
    scc = SCC(G)
    x = scc.isSatisfiable()
    print(x)







