"""
Greedy algorithm for minimizing the weighted
sum of completion times.
"""

def score(job):
    """this greedy algorithm is not optimal"""
    return job.weight - job.length

def score_opt(job):
    """this is the optimal greedy algorithm"""
    return job.weight / job.length

def find_dups(alist):
    """
    proc: key used to compare elements
    return list of tuples of (i, j) ranges
    j not inclusive
    """
    N = len(alist)
    i = 0
    j = i + 1
    res = []
    while i < N:
        while j < N and score_opt(alist[i]) == score_opt(alist[j]):
            j += 1
        if j - i > 1:
            res = res + [(i, j)]
        i = j
        j = i + 1
    return res
      
######################################### 
if __name__ == "__main__":
    from collections import namedtuple

    Job = namedtuple('Job', ['weight', 'length'])
    
    with open("c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week7/jobs.txt", 'r', encoding='ascii') as f:
        number_jobs = int(f.readline().strip())
        jobs = [None] * number_jobs
        lines = (line.strip().split() for line in f)
        i = 0
        for line in lines:
            weight, length = int(line[0]), int(line[1])
            jobs[i] = Job(weight, length)
            i += 1

        # sort jobs by score
        jobs.sort(key = score_opt, reverse=True)

        # For score_opt greedy algorithm, tie-breaking is arbitrary

        # find dups
        list_of_dup_ranges = find_dups(jobs)
        for i, j in list_of_dup_ranges:
            jobs[i:j] = sorted(jobs[i:j], key=lambda x: x.weight, reverse=True)
        
        # calculate completion time for each job
        completion_times = [None] * number_jobs
        completion_times[0] = jobs[0].length
        for i in range(1, number_jobs):
            completion_times[i] = completion_times[i - 1] + jobs[i].length

        # calculate weighted sum (cost of schedule)
        total_cost = 0
        #fout = open('c:/Users/lbklein/_COURSES/StanfordAlgorithms/Week7/sorted_jobs.txt', 'w', encoding='ascii')
        for i in range(number_jobs):
            total_cost += jobs[i].weight * completion_times[i]
            #print(jobs[i], score_opt(jobs[i]), file=fout)
        print(total_cost)
        #fout.close()

            

            