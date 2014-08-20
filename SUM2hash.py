"""
The goal of this problem is to implement a variant of the 2-SUM algorithm 
(covered in the Week 6 lecture on hash table applications).
The file contains 1 million integers, both positive and negative 
(there might be some repetitions!).This is your array of integers, 
with the ith row of the file specifying the ith entry of the array.

Your task is to compute the number of target values t in the 
interval [-10000,10000] (inclusive) such that there are distinct numbers x,y 
in the input file that satisfy x+y=t. (NOTE: ensuring distinctness requires 
a one-line addition to the algorithm from lecture.)

Write your numeric answer (an integer between 0 and 20001) in the space provided.
"""
from collections import defaultdict

minval = -10000
maxval = 10000
targets = [False] * (maxval - minval + 1)

###################################
if __name__ == "__main__":
    filename="C:/Users/lbklein/_COURSES/StanfordAlgorithms/Week6/algo1-programming_prob-2sum.txt"
    with open(filename, 'r', encoding='ascii') as f:
        d = defaultdict(set)
        lines = (line for line in f)
        for line in lines:
            value = int(line)
            key = int(value / maxval)
            d[key].add(value)
            
    for x in d:
        lo = -1 - x
        hi = 1 - x
        for y in [lo, -x, hi]: # for x, only need to look up 3 keys in d
            if y in d:
                # do an exhaustive search for pairs from list d[x] and list d[y]
                for a in d[x]:
                    for b in d[y]:
                        if a != b and minval <= (a + b) <= maxval:
                            targets[a + b] = True
                            break
                    if targets[a + b]:
                        break
    count = sum(targets)
    print(count)
    




