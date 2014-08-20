"""
Weighted Independent Set
Find the max-weight independent set on a graph G
Independent Set: set of vertices such that no two are adjacent
bottom-up (iterative) algorithm
"""

def buildTable(N):
    """
    N: number of vertices
    WT: vertex-indexed list of weights
    return max-wt of IS (independent set)
    """

    M = [None] * (N + 1)
    M[0] = 0
    M[1] = WT[1]
    for j in range(2, N + 1):
        M[j] = max(WT[j] + M[j - 2], M[j - 1])
    return M

def find_solution(j, S):
    """
    returns set of vertices in max-wt IS for graph G
    j: first j vertices of graph G
    """
    if j == 0:
        return S
    elif WT[j] + M[j - 2] >= M[j - 1]:
        # include j in solution set
        S.add(j)
        return find_solution(j - 2, S)
    else:
        # don't include j in solution set
        return find_solution(j - 1, S)


############################################### 
if __name__ == "__main__":
    WT = [0]
    with open("C:/Users/lbklein/_COURSES/StanfordAlgorithms/Week9/pathGraph.txt", 'r', encoding='ascii') as f:
        N = int(f.readline().strip())
        weights = (int(weight.strip()) for weight in f)
        for w in weights:
            WT.append(w)

# N is number of vertices in path graph
M = buildTable(N)
max_wt = M[N]
S = find_solution(N, set())
print(S)

