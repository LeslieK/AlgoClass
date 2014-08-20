"""
Dynamic median. Design a data type that supports
insert in logarithmic time, find-the-median in
constant time, and remove-the-median in logarithmic time.
"""
"""
2 priority queues:
1 is a MinPQ : min of top half    (right)
1 is a MaxPQ : max of bottom half (left)
to find median: max or min
"""
from indexMinPQ import MinPQ, MaxPQ
from redblacktrees import RedBlackBST

class DynamicMedian(object):
    def __init__(self):
        "Builds a MedPQ data structure"
        self.pq_right = MinPQ()
        self.pq_left = MaxPQ()
        self._N = 0     # number of items on PQ

    def isEmpty(self):
        return self._N == 0

    def size(self):
        return self._N

    def insert(self, x):
        if self.isEmpty():
            self.pq_left.insert(x)
            self._N += 1
        elif x > self.pq_left.peek():
            # insert in right heap
            self.pq_right.insert(x)
            self._N += 1
            #print("inserted in right heap")
        else:
            # insert in left heap
            self.pq_left.insert(x)
            self._N += 1
            #print("inserted in left heap")
        self._rebalance()

    def _isOdd(self, n):
        return n % 2

    def _rebalance(self):
        """
        invariant:
        if size is even: left size == right size
        if size is odd: left size = right size + 1
        """
        if self._isOdd(self._N):
            #print("rebalancing: odd")
            while (self.pq_left.size() - self.pq_right.size()) > 1:
                #print("odd: pop left")
                x = self.pq_left.delMin()
                self.pq_right.insert(x)
            while (self.pq_right.size() - self.pq_left.size() > -1):
                #print("odd: pop right")
                x = self.pq_right.delMin()
                self.pq_left.insert(x)
        else:
            #print("rebalancing: even")
            while (self.pq_right.size() - self.pq_left.size()) > 0:
                #print("even: pop right")
                x = self.pq_right.delMin()
                self.pq_left.insert(x)
            while (self.pq_left.size() - self.pq_right.size()) > 0:
                #print("even: pop left")
                x = self.pq_left.delMax()
                self.pq_right.insert(x)

    def find_the_median(self):
        return self.pq_left.peek()

    def remove_the_median(self):
        "delete and return the median key in PQ"
        if self.isEmpty():
            return "No such element exception"
        else:
            # always delete from left
            self._N -= 1
            m = self.pq_left.delMax()
            self._rebalance()
            return m

###############################
#filename = "C:/Users/lbklein/_COURSES/StanfordAlgorithms/Week6/Median.txt"
filename = "C:/Users/lbklein/_COURSES/StanfordAlgorithms/Week6/algo1-programming_prob-2sum.txt"
NUMBER_OF_VALUES = 10000
sum_of_medians = 0

# using a heap data structure

median = DynamicMedian()
with open(filename, 'r', encoding='ascii') as f:
    lines = (line for line in f)
    for n in lines:
        median.insert(int(n))
        m = median.find_the_median()
        sum_of_medians += m
    
print(sum_of_medians % NUMBER_OF_VALUES)

# using a redblack tree

#rbt = RedBlackBST()
#with open(filename, 'r', encoding='ascii') as f:
#    lines = (line for line in f)
#    for n in lines:
#        rbt.put(int(n), n)
#        m, _ = rbt.select((rbt.size() - 1) // 2)
#        sum_of_medians += m
#print(sum_of_medians % NUMBER_OF_VALUES)
