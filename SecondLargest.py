import math
from collections import defaultdict
record = defaultdict(list)

def getMaxVal(x, y):
    if x > y:
        record[x].append(y)
        return x
    else:
        record[y].append(x)
        return y

def findLargest_r(a):
    if a is []:
        return None
    if len(a) == 1:
        return a[0]
    mid = len(a) // 2
    left = a[:mid]
    right = a[mid:]
    max_val = getMaxVal(findLargest_r(left), findLargest_r(right))
    return max_val

def findSecondLargest(a):
    largest = findLargest_r(a)
    return findLargest_r(record[largest])

a = [1, 2, 3, 32, 5, 6, 7, 8]
print(findLargest_r(a))
print(findSecondLargest(a))




