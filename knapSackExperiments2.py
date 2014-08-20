"""
Given (weight, value) for n items and a total weight W, find the 
max-value subset of all the items such that the sum of their weights 
does not exceed W
"""
from collections import defaultdict

class Item(object):
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value
        self.acc_weight = weight  # initial value
        self.acc_value = value   # initial value

    def __eq__(self, that):
        return self.weight == that.weight and self.value == that.value

    def __gt__(self, that):
        if self.weight > that.weight:
            return True
        elif self.weight == that.weight and self.value < that.value:
            return True
        else:
            return False

    def __lt__(self, that):
        if self.weight < that.weight:
            return True
        elif self.weight == that.weight and self.value > that.value:
            return True
        else:
            return False

    def __repr__(self):
        """
        string to eval Item
        """
        return 'Item({}, {})'.format(self.weight, self.value)


#def Subset_Sum_iter(n, W):
#    """
#    return 2D array of optimal solutions to subproblems
#    solve current subproblem from solutions to previous subproblems
#    """
#    M = [[0] * (W + 1) for i in range(n + 1)]  # row[i] = [i][w0], [i][w1], ...
#    for i in range(1, n + 1):
#        for w in range(1, W + 1):
#            if items[i].weight > w:
#                # wt of ith item is too heavy; do not include it
#                M[i][w] = M[i - 1][w]
#            else:
#                M[i][w] = max(M[i - 1][w], M[i - 1][w - items[i].weight] + items[i].value)

#    return M

def Subset_Sum_iter(n, W):
    """
    n: number of items
    W: total capacity of knapsack
    return 2D array of optimal solutions to subproblems
    solve current subproblem from solutions to 2 previous subproblems
    """
    # M is a list of dicts; 1 dict for each item (row of matrix)
    M = [None] * (n + 1)  # for each item, including item 0
    for i in range(n + 1):
        # key: capacity
        # value: value
        # (capacity, value)
        M[i] = dict([(0, (0, 0))])

    cap_i = 0
    for i in range(1, n + 1):
        for c in M[i - 1]:  # c = wt
            value = M[i - 1][c][1]
            cap_i = items[i].weight + c
            if cap_i > W:
                continue
            val_i = items[i].value + value

            if val_i < value:
                # value without item i > value with item i
                # don't take item i
                M[i][c] = (c, value)

            elif not keepItem(i, val_i, cap_i, M):
                # do not take item i; value is worse than what you have
                continue

            else:
                M[i][cap_i] = (cap_i, val_i)
                for z in range(i + 1, n + 1):
                    M[z][cap_i] = (cap_i, val_i)

    return M

def Find_Solution(i, w):
    if i == 0 or items[i].weight > w:
        return
    if M[i - 1][w - items[i].weight] + items[i].value > M[i - 1][w]:
        print(items[i])
        Find_Solution(i - 1, w - items[i].weight)
    else:
        Find_Solution(i - 1, w)

def Subset_Sum_iter2(n, W):
    """
    A is a 1-row matrix; cols are weights
    bottom-up iterative solution
    must make this more efficient
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

        # take all items if w > acc_weight
        if w >= items[i].acc_weight:
            # take all the items
            M[(i, w)] = items[i].acc_value
            stack.pop()
            continue

        # recurse on (i - 1, w) and/or (i - 1, w - items[i].weight)
        if (i - 1, w) not in M:
            stack.append((i - 1, w))
        if (i - 1, w - items[i].weight) not in M:
            stack.append((i - 1, w - items[i].weight))
    print('length: ', len(M))
    return M[(i, w)]
    
def maxValue(M):
    keys = list(M[number_of_items].keys())
    keys.sort(reverse=True)
    print('M[100] len:', len(keys))
    for i in range(len(keys)):
        if keys[i] > W:
            continue
        else:
            max_value = M[number_of_items][keys[i]]
            return max_value

#def maxValue(M):
#    for i in range(len(M[number_of_items]) - 1, -1, -1):
#        if M[number_of_items][i][0] > W:
#            continue
#        else:
#            return M[number_of_items][i][1]

def keepItem(i, val_i, cap_i, M):
    """
    item: index of items
    M: list of dicts, indexed by item
    returns True if item should be inserted into M
    """
    if cap_i in M:
        return val_i > M[i][cap_i][1]

    else:
        for k in M[i]:
            if k <= cap_i and M[i][k][1] >= val_i:
                return False
        return True


#########################################
if __name__ == "__main__":
    import json

    #Item = namedtuple('Item', ['weight', 'value'])
    #items = [Item(0, 0)]
    
    items = [Item(0, 0)]

    #with open("C:/Users/lbklein/_COURSES/StanfordAlgorithms/Week9/knapsack_big.txt", 'r', encoding='ascii') as f:
    with open("C:/Users/lbklein/_COURSES/StanfordAlgorithms/Week9/knapsack1.txt", 'r', encoding='ascii') as f:
    #with open("C:/Users/lbklein/_COURSES/StanfordAlgorithms/Week9/knapSacktiny.txt", 'r', encoding='ascii') as f:
    #with open("C:/Users/lbklein/_COURSES/StanfordAlgorithms/Week9/126.txt", 'r', encoding='ascii') as f:
    #with open("C:/Users/lbklein/_COURSES/StanfordAlgorithms/Week9/knapSacknano.txt", 'r', encoding='ascii') as f:
    #with open("C:/Users/lbklein/_COURSES/StanfordAlgorithms/Week9/finalTest.txt", 'r', encoding='ascii') as f:
        W, number_of_items = list(map(int, f.readline().strip().split()))
        val_weights = (line.strip().split() for line in f)
        for vw in val_weights:  # vw is [value, weight]
            v, w = int(vw[0]), int(vw[1])
            items.append(Item(w, v))
    items.sort()  # sort items by increasing weight, decreasing value

    #for i in range(1, number_of_items + 1):
    #    items[i].acc_weight += items[i - 1].acc_weight
    #    items[i].acc_value += items[i - 1].acc_value

    
    M = Subset_Sum_iter(number_of_items, W)   # iteration using bottom up with sparse 2D matrix
    #max_value = Subset_Sum_iter2(number_of_items, W)  # iteration bottom-up using 1 row of matrix
    #max_value = Subset_Sum(number_of_items, W)         # recursion using an explicit stack
    max_value = maxValue(M)
    #f = open('M2.txt', 'w', encoding='utf-8')
    #json.dump(M, f)
    #f.close()
    #Find_Solution(number_of_items, W)
    print('max val:', max_value)