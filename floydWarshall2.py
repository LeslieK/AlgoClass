#from collections import Counter
from collections import deque

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
    returns the i-j path length for each i-j pair
    build 3-D array
    return A[i, j, k=n] for all i, j
    i = source
    j = target
    k = {1, 2, 3, ..., k} internal nodes that can be on i-j path
    """
    #def __init__(self, filename):

    #    with open(filename, 'r', encoding='utf-8') as f:
    #        self.V, self.E = list(map(int, f.readline().strip().split()))

    #        # set up array A
    #        self.A = np.zeros(shape=(self.V + 1, self.V + 1), dtype=float)
    #        self.A[:,:] = np.inf
    #        b = np.eye(self.V + 1, self.V + 1, dtype=bool)
    #        self.A[b] = 0.

    #        # B stores last vertex in i-j path for each (i, j)
    #        # 0: no parent
    #        self.B = np.zeros(shape=(self.V + 1, self.V + 1), dtype=int)

    #        lines = (line.strip().split() for line in f)
    #        for line in lines:
    #            v, w, wt = line
    #            v, w, wt = int(v), int(w), float(wt)
    #            # dont add 1 for Stanford files
    #            self.A[v, w] = wt 
    #            self.B[v, w] = v
    #            # add 1 for Princeton files
    #            #self.A[v + 1, w + 1] = wt 
    #            #self.B[v + 1, w + 1] = v


    #    self.hasNegCycle = False

    #    for k in range(1, self.V + 1):          # set of nodes on path {1, 2, ..., k}
    #        for i in range(1, self.V + 1):      # row
    #            if self.B[i, k] == 0:           # optimization (no edge from i to k)
    #                continue
    #            for j in range(1, self.V + 1):  # col
    #                if self.A[i, j] > self.A[i, k] + self.A[k, j]:
    #                    self.A[i, j] = self.A[i, k] + self.A[k, j]
    #                    self.B[i, j] = self.B[k, j]

    #            # check for negative cycle
    #            if self.A[i][i] < 0.0:
    #                self.hasNegCycle = True
    #                print('has negative cycle')
    #                break
    #        if self.hasNegativeCycle():
    #            break

    def __init__(self, filename):

        with open(filename, 'r', encoding='utf-8') as f:
            self.V, self.E = list(map(int, f.readline().strip().split()))

            # set up array A
            self.A = np.zeros(shape=(self.V + 1, self.V + 1), dtype=float)
            self.A[:,:] = np.inf
            b = np.eye(self.V + 1, self.V + 1, dtype=bool)
            self.A[b] = 0.

            # B stores highest indexed vertex (k) in i-j path for each (i, j)
            # 0: no parent
            self.B = np.zeros(shape=(self.V + 1, self.V + 1), dtype=int)
            self.B[:] = np.inf
            self.B[b] = 0

            lines = (line.strip().split() for line in f)
            for line in lines:
                v, w, wt = line
                v, w, wt = int(v), int(w), float(wt)
                # dont add 1 for Stanford files
                self.A[v, w] = wt 
                self.B[v, w] = 0  # adds max indexed vertex on v-w path
                # add 1 for Princeton files
                #self.A[v + 1, w + 1] = wt 
                #self.B[v + 1, w + 1] = 0


        self.hasNegCycle = False

        for k in range(1, self.V + 1):          # set of nodes on path {1, 2, ..., k}
            for i in range(1, self.V + 1):      # row
                #if self.B[i, k] == np.inf:      # optimization (no edge from i to k)
                #    continue
                for j in range(1, self.V + 1):  # col
                    if self.A[i, j] > self.A[i, k] + self.A[k, j]:
                        self.A[i, j] = self.A[i, k] + self.A[k, j]
                        self.B[i, j] = k

            #    # check for negative cycle
            #    if self.A[i][i] < 0.0:
            #        self.hasNegCycle = True
            #        print('has negative cycle')
            #        break
            #if self.hasNegativeCycle():
            #    break

    def allPaths(self):
        return self.A[:, :]

    def shortestShortestPath(self):
        b = np.eye(self.V + 1, dtype=bool)
        self.A[b] = np.inf
        return np.min(self.A)

    def hasNegativeCycle(self):
        """returns True if neg cycle exists"""
        return self.hasNegCycle

    def hasPath(self, s, t):
        """
        return True if a path exists from s to t
        """
        return self.A[s][t] < np.inf

    def path(self, s, t):
        """
        returns the shortest path from s to t
        """
        if self.hasNegativeCycle():
            raise Exception("Negative cost cycle exists")

        def helper(s, t, res):
            k = self.B[s, t]
            if k > 0:
                res = helper(s, k, res)
                res = helper(k, t, res)
                return res
            else:
                return res + [t]

        if self.hasPath(s, t):
            res = helper(s, t, [s])
            return iter(res)

########################################## 
if __name__ == "__main__":

    #filename = "c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week10/tinyEWDn_Stanford.txt"
    #filename = "c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week10/g1.txt" # has negative cycle
    #filename = "c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week10/g2.txt" # has negative cycle
    #filename = "c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week10/g3.txt"
    #filename = "c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week10/scc_with_nc.txt"
    filename = "test_FloydMagnitude.txt"

    apsp = AllpairsShortestpaths(filename)
    if apsp.hasNegativeCycle():
        print('has negative cycle')
    else:
        ssp = apsp.shortestShortestPath()
        print(ssp)
        src = 1
        dest = apsp.V - 2
        ashortestpath = apsp.path(src, dest)
        if ashortestpath:
            for i in ashortestpath:
                if i != dest:
                    print(i, end=' => ')
                else:
                    print(i)



