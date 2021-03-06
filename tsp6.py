"""
Dynammic Programming algorithm applied to
Travelling Salesman Problem
optimizations:
use 2 half tours to find min full tour
ping pong 2 dictionaries
dictionary key: destination city | bitmapped cities
did not implement Gospher's Hack to generate subsets
did not use densely-packed arrays of a single data type

This uses bitarray instead of bit shifting << as in tsp5.py.
This is slower than tsp5.py
Another waste of time!
"""
import math
import numpy as np
import itertools
from collections import defaultdict
from bitarray import bitarray

def defaultValue():
    return np.inf

def distance(cities, i, j):
    """
    returns Euclidean distance
    """
    t = (i, j)
    try:
        x = distances[t]
    except KeyError:
        deltax = cities[i][0] - cities[j][0]
        deltay = cities[i][1] - cities[j][1]
        x = math.sqrt(deltax * deltax + (deltay * deltay))
        distances[t] = x
    return x

def distToDest(A, S, j):
    """
    S: set of vertices
    j: j of s-j shortest path
    visit each vertex in S once
    """
    # j is endpoint
    zmin = np.inf
    u = removeCity(S, j)
    for k in nextCity(u):
        # k is penultimate endpoint
        keyU = genKey(u, k)
        r = A[keyU] + distance(cities, k, j)
        if r < zmin:
            zmin = r
    # shortest path from 1 to j visiting vertices in S
    return zmin

def subsets_int(n, size):
    it = itertools.combinations(range(2, n + 1), size - 1)
    for S in it:
        c.setall(False)
        c[1] = True
        for city in S:
            c[city] = True
        yield c

def complementSet(aset, j):
    """
    returns the complement of the set
    with bit 1 set
    and j set
    """
    acopy = aset.copy()
    acopy.invert()
    acopy[1] = True             # set bit 1
    acopy[0] = False            # reset bit 0
    acopy[j] = True             # set bit j           
    return acopy

def removeCity(aset, city):
    acopy = aset.copy()
    acopy[city] = False
    return acopy

def nextCity(aset):
    """
    returns the bit positions of the cities
    in a set of cities
    aset: set of cities
    """
    pos = 0
    while True:
        try:
            pos = aset.index(True, pos + 1)
            yield pos
        except ValueError:
            return

def genKey(aset, destCity):
    return (aset.tobytes(), destCity)

def fullTour(A, B):
    """
    builds full tours from half tours
    returns min distance of full tour
    """
    it = subsets_int(number_cities, z)
    res = [np.inf] * (number_cities + 1)
    for S in it:
        for j in nextCity(S):
            # j is an endpoint
            if j > 1:
                coS = complementSet(S, j)     # coS includes 1 and j
                keyS = genKey(S, j)
                keycoS = genKey(coS, j)
                if keyS in B and keycoS in A:
                    distToj = B[keyS] + A[keycoS]
                elif keyS in A and keycoS in B:
                    distToj = A[keyS] + B[keycoS]
                elif keyS in B and keycoS in B:
                    distToj = B[keyS] + B[keycoS]
                else:
                    distToj = A[keyS] + A[keycoS]
                if distToj < res[j]:
                    res[j] = distToj
    opt_tour = min(res[2:])
    return opt_tour

    
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

    # initial data structures
    distances = {}
    A = defaultdict(defaultValue)
    B = defaultdict(defaultValue)

    # base case
    BASESET = bitarray(number_cities + 1)
    BASESET.setall(False)
    BASESET[1] = 1
    x = genKey(BASESET, 1)
    A[x] = 0.

    # CONSTANTS
    c = bitarray(number_cities + 1, endian='big')

    # do 2 complementary tours and add together to get tsp
    # z is max size of subset
    z = ((number_cities + 1) // 2) + 1
    for m in range(2, z + 1):
        if m % 2 == 0:
            dict_read = A
            B = defaultdict(defaultValue)
            dict_write = B
        else:
            dict_read = B
            A = defaultdict(defaultValue)
            dict_write = A
        for S in subsets_int(number_cities, m):
            for j in nextCity(S):
                if j > 1:
                    # j is endpoint
                    keyS = genKey(S, j)
                    zmin = distToDest(dict_read, S, j)
                    # shortest path from 1 to j visiting vertices in S
                    dict_write[keyS] = zmin

    # for each j calculate full tour
    # take min of all tours to get optimal tour
    opt_tour = fullTour(A, B)
    print(opt_tour)

     