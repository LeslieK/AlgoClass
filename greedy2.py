"""
Greedy algorithm for minimizing the weighted
sum of completion times.
"""

class MaxPQ(object):
    "max priority queue; max value removed first"
    def __init__(self):
        "Builds a MaxPQ data structure"
        self._pq = [0]                    # store items at indices 1 to N
        self._N = 0                       # number of items on PQ

    def isEmpty(self):
        return self._N == 0

    def size(self):
        return self._N

    def peek(self):
        return self._pq[1]

    def insert(self, x):
        "add x to PQ; swim it up to maintain heap invariant"
        self._N += 1
        self._pq.append(x)
        self._swim(self._N)

    def delMax(self):
        "delete and return the largest key in PQ"
        if self.isEmpty():
            return "No such element exception"
        else:
            self._exch(1, self._N)
            key = self._pq.pop()
            self._N -= 1
            self._sink(1)
            return key

    # helper functions to restore heap invariant
    def _swim(self, k):
        "move key in position k up to maintain heap invariant"
        while (k > 1 and self._lessthan2(k // 2, k)):
            self._exch(k // 2, k)
            k = k // 2

    def _sink(self, k):
        "move key in position k down to maintain heap invariant"
        while(2 * k <= self._N):
            # consider the children of k
            j = 2 * k
            # get the smallest child
            if (j < self._N and self._lessthan2(j, j + 1)):
                j += 1
            # check that parent k < child j
            if (not self._lessthan2_opt(k, j)):
                break
            self._exch(j, k)
            k = j

    def _exch(self, k1, k2):
            self._pq[k2], self._pq[k1] = self._pq[k1], self._pq[k2]

    #def _lessthan(self, k1, k2):
    #    return self._pq[k1] < self._pq[k2]

    def _lessthan2(self, k1, k2):
        if score(self._pq[k1]) == score(self._pq[k2]):
            return self._pq[k1].weight < self._pq[k2].weight
        return score(self._pq[k1]) < score(self._pq[k2])

    def _lessthan2_opt(self, k1, k2):
        if score_opt(self._pq[k1]) == score_opt(self._pq[k2]):
            return self._pq[k1].weight < self._pq[k2].weight
        return score_opt(self._pq[k1]) < score_opt(self._pq[k2])

    def __repr__(self):
        "Uniquely identifies MaxPQ"
        return "size=%r weights=%r" % (self.size(), [e.weight() for e in self._pq[1:]])

def score(job):
    return job.weight - job.length

def score_opt(job):
    return job.weight / job.length

######################################### 
if __name__ == "__main__":
    from collections import namedtuple

    Job = namedtuple('Job', ['weight', 'length'])
    # put jobs on MaxPQ (priority = score or weight (ties))
    pq = MaxPQ()
    
    with open("c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week7/tinyjobs.txt", 'r', encoding='ascii') as f:
        number_jobs = int(f.readline().strip())
        lines = (line.strip().split() for line in f)
        for line in lines:
            weight, length = int(line[0]), int(line[1])
            pq.insert(Job(weight, length))

        j = pq.delMax()
        total_length = j.length
        total_cost = j.weight * total_length
        while not pq.isEmpty():
            j = pq.delMax()
            total_length += j.length
            total_cost += j.weight * total_length
        print(total_cost)
            
            


