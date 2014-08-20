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

def rank(a, key):
    lo = 0
    hi = len(a) - 1
    while hi >= lo:
        mid = lo + (hi - lo) // 2
        if key == a[mid]:
            return mid
        elif key > a[mid]:
            lo = mid + 1
        else:
            hi = mid - 1
    return lo

def binary_search(a, lo, hi, key):
    while hi >= lo:
        mid = lo + (hi - lo) // 2
        if key == a[mid]:
            return mid
        elif key > a[mid]:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

missingsums = [-9967, -9966, -9874, -9779, -9127, -7730, -4938, -9686, -9222]

def count_2SUM(d, minval, maxval):
    targets = [False] * (maxval - minval + 1)
    t_index = rank(d, minval)  # index of first pos integer
    hi = len(d) - 1
    j = hi
    for i in range(t_index):
        x = d[i]
        y = d[j]
        s = x + y
        if s in missingsums:
            print('x: {}, y: {}, s: {}'.format(x, y, s))
        #print(i, j, s)
        if inInterval(s):
            targets[s] = True
            q = j + 1
            while q < hi:
                s = x + d[q]
                #print("in range, moving j right", i, q, s)
                if inInterval(s):
                    targets[s] = True
                    q += 1
                else:
                    break
            q = j - 1
            while q > t_index:
                s = x + d[q]
                #print("in range, moving j left", i, q, s)
                if inInterval(s):
                    targets[s] = True
                    q -= 1
                else:
                    break 
        elif s < minval:
            # y is too small
            q = j + 1
            while q < hi:
                s = x + d[q]
                #print("too small, moving j right", i, q, s)
                if s < minval:
                    q += 1
                elif inInterval(s):
                    targets[s] = True
                    q += 1
                else:
                    break
        else:
            # s > maxval
            # y is too big
            q = j - 1
            while q > t_index:
                s = x + d[q]
                #print("too big, moving j left", i, q, s)
                if s > maxval:
                    q -= 1
                elif inInterval(s):
                    targets[s] = True
                    q -= 1
                else:
                    #print('reset j')
                    j = q - 1
                    break
    return sum(targets)
    #return targets

minval = -10000
maxval = 10000
target_set = set(range(minval, maxval + 1))    
def inInterval(s):
    return s in target_set

#######################################################
if __name__ == "__main__":

    filename="C:/Users/lbklein/_COURSES/StanfordAlgorithms/Week6/algo1-programming_prob-2sum.txt"
    with open(filename, 'r', encoding='ascii') as f:
        d = set()
        lines = (line for line in f)
        for line in lines:
            d.add(int(line))
    d = list(d)

    minval = -10000
    maxval = 10000
    target_set = set(range(minval, maxval + 1))
    d.sort()
    count = count_2SUM(d, minval, maxval)
    print(count)





