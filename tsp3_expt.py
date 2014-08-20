"""
Dynammic Programming algorithm applied to
Travelling Salesman Problem
"""
import math
import numpy as np
import matplotlib.pyplot as plt
import itertools
from collections import defaultdict

def defaultValue():
    return [np.inf] * (number_cities + 1)

def defaultPen():
    return [None] * (number_cities + 1) 

def distance(cities, i, j):
    """
    returns Euclidean distance
    """
    x1, y1 = cities[i]
    x2, y2 = cities[j]
    deltax = x1 - x2
    deltay = y1 - y2
    x = math.sqrt(deltax * deltax + (deltay * deltay))
    return x

def subsets(n, size):
    """
    n: item labels range from 1 to n
    size: size of subset
    return a subset of 'size' with items chosen from 1 to n (must include item 1)
    """
    it = itertools.combinations(range(2, n + 1), size - 1)
    for s in it:
        subset = s + (1, )
        yield frozenset(subset)

def delta2():
    add_in = \
        distance(cities_25, 1, 2) + \
        distance(cities_25, 2, 6) + \
        distance(cities_25, 6, 10) + \
        distance(cities_25, 10, 11) + \
        distance(cities_25, 21, 23) + \
        distance(cities_25, 23, 22) + \
        distance(cities_25, 24, 25) + \
        distance(cities_25, 25, 20) + \
        distance(cities_25, 20, 17) + \
        distance(cities_25, 3, 7) + \
        distance(cities_25, 7, 9)


    sub_out = \
        distance(cities_25, 1, 6) + \
        distance(cities_25, 6, 11) + \
        distance(cities_25, 21, 22) + \
        distance(cities_25, 24, 17) + \
        distance(cities_25, 3, 9)

    print('add_in', add_in, 'sub_out', sub_out)

    return add_in - sub_out

def delta3():
    add_in = \
        distance(cities_25, 1, 2) + \
        distance(cities_25, 2, 6) + \
        distance(cities_25, 6, 10) + \
        distance(cities_25, 10, 11) + \
        distance(cities_25, 5, 8) + \
        distance(cities_25, 8, 4) + \
        distance(cities_25, 25, 20) + \
        distance(cities_25, 20, 17) + \
        distance(cities_25, 21, 23) + \
        distance(cities_25, 23, 22)

    sub_out = \
        distance(cities_25, 1, 6) + \
        distance(cities_25, 6, 11) + \
        distance(cities_25, 5, 4) + \
        distance(cities_25, 25, 17) + \
        distance(cities_25, 21, 22)

    print('add_in', add_in, 'sub_out', sub_out)

    return add_in - sub_out

def delta():
    """
    delete 2, 8, 23
    """
    add_in = \
        distance(cities_25, 1, 2) + \
        distance(cities_25, 2, 6) + \
        distance(cities_25, 5, 8) + \
        distance(cities_25, 8, 4) + \
        distance(cities_25, 21, 23) + \
        distance(cities_25, 23, 22)

    sub_out = \
        distance(cities_25, 1, 6) + \
        distance(cities_25, 5, 4) + \
        distance(cities_25, 21, 22)

    print('add_in', add_in, 'sub_out', sub_out)

    return add_in - sub_out

############################ 
if __name__ == "__main__":
    with open("c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week11/tsp.txt", 'r', encoding='utf-8') as f:
        number_cities_25 = int(f.readline().strip())
        cities_25 = np.zeros((number_cities_25 + 1, 2), dtype=float)  # count from 1
        lines = (line.strip().split() for line in f)
        i = 1
        for line in lines:
            x, y = line
            x, y = float(x), float(y)
            cities_25[i] = x, y
            i += 1

    #with open("c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week11/tsp_sorted.txt", 'r', encoding='utf-8') as f:
    with open("c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week11/tinytsp.txt", 'r', encoding='utf-8') as f:
        number_cities = int(f.readline().strip())
        cities = np.zeros((number_cities + 1, 2), dtype=float)  # count from 1
        lines = (line.strip().split() for line in f)
        i = 1
        for line in lines:
            x, y = line
            x, y = float(x), float(y)
            cities[i] = x, y
            i += 1

    plt.grid(b=True)
    fig = plt.gcf()
    ax = fig.add_subplot(111)
    #ax.set_xlim(left=cities[1, 0] - 1000., right=cities[number_cities, 0] + 1000.)
    #ax.plot(cities[:, 0], cities[:, 1], marker='*')
    ax.scatter(cities[1:, 0], cities[1:, 1])
    #ax.plot(cities[1, 0], cities[1, 1], cities[number_cities, 0],  cities[number_cities, 1])
    plt.show()

    A = defaultdict(defaultValue)
    penultimate = defaultdict(defaultPen)
    # base case
    A[frozenset([1])] = [np.inf] * (number_cities + 1)
    A[frozenset([1])][1] = 0
    penultimate[frozenset([1])] = [None] * (number_cities + 1)

    z = ((number_cities + 1) // 2) + 1
    for m in range(2, z + 1):
        for S in subsets(number_cities, m):
            #print(S)
            for j in S:
                # j is endpoint
                if j > 1:
                    zmin = np.inf
                    u = S - set([j])
                    for k in u:
                        # k is penultimate endpoint
                        r = A[u][k] + distance(cities, k, j)
                        if r < zmin:
                            zmin = r
                            kpen = k
                    # shortest path from 1 to j visiting vertices in S
                    A[S][j] = zmin
                    penultimate[S][j] = kpen

    # for each j calculate full tour
    # distTo(j) using set S + distTo(j) using set complement(S)
    # take min of all tours to get optimal tour
    all_cities = frozenset(range(1, number_cities + 1))
    it = subsets(number_cities, z)
    res = [np.inf] * (number_cities + 1)
    for S in it:
        for j in S:
            if j > 1:
                x = set(S) - set([1])
                coS = frozenset((all_cities - x).union(set([j])))
                distToj = A[S][j] + A[coS][j]
                if distToj < res[j]:
                    res[j]  = distToj
    opt_tour = min(res[2:])
    print(opt_tour)


    ## adjust tour distance due to omitting cities
    #x = delta()
    #print('delta', x)
    #print(opt_tour + x)

    ## print out tour
    #tour = [None] * (number_cities + 1)
    #u = all_vertices
    
    #tour[1] = kbest
    #while kbest != 1:
    #    c = penultimate[u][kbest]
    #    tour[kbest] = c
    #    u = u - set([kbest])
    #    kbest = c
    
    #for i in range(1, len(tour)):  
    #    print('to city', i, 'from city', tour[i])

    ## plot tour
    #t = np.zeros((number_cities + 2, 2), dtype=float)
    #t[1] = cities[1]
    #next = tour[1]
    #i = 2
    #while next != 1:
    #    t[i] = cities[next]
    #    next = tour[next]
    #    i += 1
    #t[i] = cities[next]

    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #ax.scatter(t[1:, 0], t[1:, 1])
    #ax.plot(t[1:, 0], t[1:, 1])
    #plt.show()
     