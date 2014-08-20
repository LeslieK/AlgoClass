"""
Given (weight, value) for n items and a total weight W, find the 
max-value subset of all the items such that the sum of their weights 
does not exceed W
"""

def Subset_Sum_iter(n, W):
    """
    return 2D array of optimal solutions to subproblems
    solve current subproblem from solutions to previous subproblems
    """
    M = [[0] * (W + 1) for i in range(n + 1)]  # row[i] = [i][w0], [i][w1], ...
    for i in range(1, n + 1):
        for w in range(1, W + 1):
            if items[i].weight > w:
                # wt of ith item is too heavy; do not include it
                M[i][w] = M[i - 1][w]
            else:
                M[i][w] = max(M[i - 1][w], M[i - 1][w - items[i].weight] + items[i].value)
    return M[n][W]

def Subset_Sum_iter2(n, W):
    """
    A is a 1-row matrix; cols are weights
    solves problem using a 1-row array (memory efficient)
    must make this more time efficient
    """
    # A is weight-indexed array
    A = [0] * (W + 1)
    for i in range(1, n + 1):
        for w in range(W, items[i].weight - 1, -1):
            A[w] = max(A[w], A[w - items[i].weight] + items[i].value)
    return A[W]

def Subset_Sum(i, w):
    """
    recursion using an explicit stack
    stack contains unevaluated cells
    pop a cell: try to evaluate it
    if yes: pop it from stack
    if no: push 1 or 2 other cells onto stack that it needs
    push left-most cell onto stack before the cell in same column
    col: weight
    row: item
    """
    if i == 0 or w == 0:
        return 0

    M = defaultdict(lambda: 0)
    M[(1, items[1].weight)] = items[1].value
    if (i, w) in M:
        return M[(i, w)]

    stack = []
    stack.append((i, w))
    while stack != []:
        # stack contains unevaluated cells
        i, w = stack[-1]

        # case: (i, w) based on 2 previous values
        if (i - 1, w) in M and (i - 1, w - items[i].weight) in M:
            M[(i, w)] = max(M[(i - 1, w)], M[(i - 1, w - items[i].weight)] + items[i].value)
            stack.pop()
            continue

        # base case: i = 0
        if i == 0:
            M[(i, w)]  = 0
            stack.pop()
            continue

        # base case: w = 0
        if w == 0:
            M[(i, 0)] = 0
            stack.pop()
            continue

        # case: boundary condition
        if w < items[i].weight:
            M[(i, w)] = 0
            stack.pop()
            continue

        # base case: extend base case for all w > items[1].weight
        if i == 1 and w >= items[i].weight:
            M[(1, w)] = items[1].value
            stack.pop()
            continue

        # recurse on (i - 1, w) and/or (i - 1, w - items[i].weight)
        if (i - 1, w) not in M:
            stack.append((i - 1, w))
        if (i - 1, w - items[i].weight) not in M:
            stack.append((i - 1, w - items[i].weight))
    print('length: ', len(M))
    return M[(i, w)]
    


#########################################
if __name__ == "__main__":
    from collections import namedtuple, defaultdict

    Item = namedtuple('Item', ['weight', 'value'])
    items = [Item(0, 0)]

    #with open("C:/Users/lbklein/_COURSES/StanfordAlgorithms/Week9/knapsack_big.txt", 'r', encoding='ascii') as f:
    with open("C:/Users/lbklein/_COURSES/StanfordAlgorithms/Week9/knapsack1.txt", 'r', encoding='ascii') as f:
    #with open("C:/Users/lbklein/_COURSES/StanfordAlgorithms/Week9/knapSacktiny.txt", 'r', encoding='ascii') as f:
        W, number_of_items = list(map(int, f.readline().strip().split()))
        val_weights = (line.strip().split() for line in f)
        for vw in val_weights:  # vw is [value, weight]
            v, w = int(vw[0]), int(vw[1])
            items.append(Item(w, v))
        items.sort()  # sort items by increasing weight
 
    max_value = Subset_Sum_iter(number_of_items, W)   # iteration using bottom up with complete 2D matrix
    #max_value = Subset_Sum_iter2(number_of_items, W)  # iteration bottom-up using 1 row of matrix
    #max_value = Subset_Sum(number_of_items, W)         # recursion using an explicit stack
    print('max val:', max_value)