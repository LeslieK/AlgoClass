
def optimalBST(n):
    """
    find optimal BST
    n: number of items
    """
    A = [[0] * (n + 1) for r in range(n + 1)]  # row[i] = [i][j=i], [i][i + 1], ... [i][i + s]

    for s in range(n - 1):  # s represents i - j; j is rightmost index in sequence of items
        for i in range(1, n):  # so i + s plays role of j
            if i + s > n - 1:
                break
            A[i][i + s], root = Cij(A, i, s)
            print(root)

    return A, A[1][n - 1], root  # northwest corner of array

def Cij(A, i, s):
    """
    Cij: weighted search cost of an optimal BST
    i: starting index from items list
    s: number of items in subtree T_ij
    s: size of subtree T_ij = j - i
    """
    m = 1000  # some maximum number

    sum_pk = sum(weights[i:i + s + 1])

    for r in range(i, i + s + 1):
        # for each value of r
        # find optimal cost on left subtree
        if r - i > len(keys) - 1 or i > r - 1:
        #if i > r - 1:
            A_i = 0
        else:
            A_i = A[i][r - 1]

        # find optimal cost on right subtree
        if r + 1 > len(keys) - 1 or r + 1 > i + s:
        #if r + 1 > i + s:
            A_j = 0
        else:
            A_j = A[r + 1][i + s]

        # find cost of current tree
        t = sum_pk + A_i + A_j

        # save min cost over range of r values
        if t < m:
            m = t
            root = r
    return m, root
#####################################
if __name__ == "__main__":

    N = 7
    keys = list(range(N + 1))
    weights = [0, .05, .4, .08, .04, .1, .1, .23]
    #weights = [.2, .05, .17, .1, .2, .03, .25]
    #keys = list(range(N + 1))    # [0, 1, 2, ..., N]
    #weights = [0, 2, 23, 73, 4]  # [0, w1, w2, ..., wN]
    A, cij, root = optimalBST(len(keys))
    print(cij)

    