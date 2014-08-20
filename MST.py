from indexMinPQ import IndexMinPQ
from ewgraph import Edge, EdgeWeightedGraph
from decimal import Decimal
_INF = Decimal('infinity')

"""
Homework Week 8
"""

class EagerPrimMST(object):
	'''
	similar to LazyPrimMST except remove obsolete edges from PQ
	given a connected, undirected, weighted graph, finds an MST and its weight
	key = vertex; priority = weight of edge
	PQ has 1 entry per vertex
	'''
	def __init__(self, EG):
		self._edgeTo = [-1 for _ in range(EG.V())]
		self._distTo = [_INF for _ in range(EG.V()) ]
		self._distTo[0] = 0
		self._pq = IndexMinPQ(EG.V())
		self._mst = [] 							# list of edges in MST
		self._weight = 0
		self._marked = set() 					# set of vertices in MST
		self._pq.insert(0, 0)

		while (not self._pq.isEmpty() and len(self._mst) < EG.V() - 1):
			v = self._pq.delMin()
			if v > 0:
				self._mst.append(self._edgeTo[v])
				self._weight += self._edgeTo[v].weight()
			self._visit(EG, v)

	def _visit(self, EG, v):
		'''
		add v to Tree; add all non-tree vertices adjacent to v to PQ; 
		update priority of edges connecting non-tree vertices to Tree
		'''
		self._marked.add(v)
		for e in EG.adj(v):
			# e is edge connecting w (non-Tree vertex) to Tree
			w = e.other(v)
			if w not in self._marked:
				if self._distTo[w] > e.weight():
					self._edgeTo[w] = e
					self._distTo[w] = e.weight()
					if not self._pq.contains(w):
						# w is not in PQ
						self._pq.insert(w, e.weight())
					else:
						self._pq.decreaseKey(w, e.weight())

	def mst(self):
		"returns edges in MST"
		return self._mst

	def weight(self):
		"returns weight of MST"
		return self._weight

	def __repr__(self):
			"Everything about MST"
			return "edges=%r wt=%r" % (self.mst(), self.weight())

#################################################### 
if __name__ == "__main__":
    with open("c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week7/edges.txt", 'r', encoding='ascii') as f:
        V, E = f.readline().strip().split()
        V, E = int(V), int(E)
        G = EdgeWeightedGraph(V)

        lines = (line.strip().split() for line in f)
        fout = open("mst.txt", 'w', encoding='ascii')
        for line in lines:
            v, w, weight = int(line[0]), int(line[1]), float(line[2])
            # v - 1, w - 1 for class data (class counts from 1)
            G.addEdge(Edge(v - 1, w - 1, weight))  
            print(v + 1, w + 1, weight, file=fout)

        mst = EagerPrimMST(G)
        print(mst.weight())


