"""
Find greedy algorithm that minimizes max lateness
lateness = Cj - dj
Cj: completion time
dj: deadline
"""
from collections import namedtuple

def cost(jobs):
    completion_time = 0
    max_lateness = 0
    for j in jobs:
        completion_time += j.proc
        lateness = completion_time - j.deadline
        if lateness > max_lateness:
            max_lateness = lateness
    return max_lateness

def sortByProcTime(jobs):
    jobs.sort(key=lambda x: x.proc)
    return jobs

def sortByDeadline(jobs):
    jobs.sort(key=lambda x: x.deadline)
    return jobs

def sortByMult(jobs):
    jobs.sort(key=lambda x: x.proc * x.deadline)
    return jobs

################################## 
if __name__ == "__main__":
    Job = namedtuple('Job', ['proc', 'deadline'])

    with open("c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week7/lateness.txt",
              'r', encoding='ascii') as f:
        number_jobs = int(f.readline().strip())
        jobs = [None] * number_jobs
        lines = (line.strip().split() for line in f)
        i = 0
        for line in lines:
            p, d = int(line[0]), int(line[1])
            jobs[i] = Job(p, d)
            i += 1

        # find schedule to minimize max lateness
        byproc = cost(sortByProcTime(jobs))
        bydeadline = cost(sortByDeadline(jobs))
        byPxD = cost(sortByMult(jobs))
        print("proc {} by deadline {} by p * d {}".format(byproc, bydeadline, byPxD))
        # ANSWER = by deadline







