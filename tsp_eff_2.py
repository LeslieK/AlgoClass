"""
Dynammic Programming algorithm applied to
Travelling Salesman Problem
"""
import math
import numpy as np
import itertools
from collections import defaultdict

def defaultValue():
    return np.inf

def manageMemory(d, keymin, keymax):
    """
    delete keys from dict for keys in range
    """
    pass



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

def subsets_int(n, size):
    """
    n: number of cities to choose from
    size: number of cities to choose
    """
    it = itertools.combinations(range(2, n + 1), size - 1)
    for s in it:
        c = 1 << 1  # all sets include {1}
        for city in s:
            c = c | (1 << city)
        yield c

def genKey(aset, destCity):
    j = destCity << (number_cities + 1)
    return j | aset
    

def removeCity(aset, city):
    mask = ~(1 << city)
    return aset & mask 

def nextCity(aset, size):
    """
    returns the bit positions of the cities
    in a set of cities
    aset: set of cities
    m: size of set
    """
    res = []
    for pos in range(1, number_cities + 1):
        i = (aset >> pos) & 1
        if i == 1:
            res.append(pos)
        if len(res) == size:
            return iter(res)
    return iter(res)

def shortestPathHome(A):
    all_cities = (1 << (number_cities + 1)) - 2

    zmin = np.inf
    for k in range(2, number_cities + 1):
        x = genKey(all_cities, k)
        r = A[x] + distance(cities, k, 1)
        if r < zmin:
            zmin = r
            kbest = k
    return zmin, kbest
    
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

    A = defaultdict(defaultValue)
    # base case
    x = genKey(1 << 1, 1)
    A[x] = 0.

    for m in range(2, number_cities + 1):
        for S in subsets_int(number_cities, m):
            for j in nextCity(S, m):
                # j is endpoint
                if j > 1:
                    zmin = np.inf
                    u = removeCity(S, j)
                    for k in nextCity(u, m):
                        # k is penultimate endpoint
                        x = genKey(u, k)
                        r = A[x] + distance(cities, k, j)
                        if r < zmin:
                            zmin = r
                    # shortest path from 1 to j visiting vertices in S
                    A[genKey(S, j)] = zmin

    opt_tour, kbest = shortestPathHome(A)    
    print(opt_tour, kbest, cities[kbest, :])

    # adjust tour distance due to omitting cities
    #x = delta()
    #print('delta', x)
    #print(opt_tour + x)
     