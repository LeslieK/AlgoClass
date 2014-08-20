"""
find a greedy algorithm that maximizes the number of
requests served
n: number of requests
ri = request i
si: start time of ri
ti: end time of ri
"""
from collections import namedtuple

def objective(algo, requests):
    """
    return cost of request schedule
    """
    print(algo.__name__, end=' ')
    res = []
    while len(requests) > 0:
        r = algo(requests)  # returns next request
        res.append(r)
        requests = removeConflicts(requests, r.start, r.end)
        print(r)
    print(len(res))
    print()
    return len(res)

def objective2(requests):
    """
    This uses the optimum greedy algorithm.
    This is the simplest objective code.
    """
    sortByEarliestEnd2(requests)
    res = [requests[0]]
    for r in requests:
        if r.start > res[-1].end:
            res.append(r)
    print(res, len(res))
    return len(res)
    
def sortByEarliestEnd2(requests):
    requests.sort(key=lambda x: x.end)

def selectByLeastTime(requests):
    requests.sort(key=lambda x: x.end - x.start, reverse=True)
    return requests.pop()

def selectByEarliestEnd(requests):
    requests.sort(key=lambda x: x.end, reverse=True)
    return requests.pop()

def selectByEarliestStart(requests):
    requests.sort(key=lambda x: x.start, reverse=True)
    return requests.pop()

def removeConflicts(requests, s, t):
    """remove all requests with start time between s and t"""
    conflicts = set()
    for r in requests:
        if r.start <= s <= r.end or \
           s <= r.start <= t:
            conflicts.add(r)
    requests = set(requests) - conflicts
    return list(requests)
    
################################## 
if __name__ == "__main__":
    Request = namedtuple('Request', ['start', 'end'])

    with open("c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week7/requests.txt",
              'r', encoding='ascii') as f:
        number_requests = int(f.readline().strip())
        requests = [None] * number_requests

        i = 0
        lines = (line.strip().split() for line in f)
        for line in lines:
            s, t = int(line[0]), int(line[1])
            requests[i] = Request(s, t)
            i += 1

    objtime = objective(selectByLeastTime, list(requests))
    objend = objective(selectByEarliestEnd, list(requests))
    objstart = objective(selectByEarliestStart, list(requests))
    objective2(requests)

    print("by least time {} by earliest end {} by earliest start {}".format(objtime, objend, objstart))
    # ANSWER: Earliest end (earliest finish time)

