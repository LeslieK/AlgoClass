def merge_and_count_splitInv(a, b):
    """
    a: (sorted list, number)
    b: (sorted list, number)
    merges 2 sorted lists
    returns (sorted list, number of split inversions)
    """
    left = a[0]
    right = b[0]
    N = len(left) + len(right)
    aux = [None] * N
    ia = 0
    ib = 0
    num_inv = a[1] + b[1]  # sum of left and right inversions
    for k in range(N):
        if ib >= len(right):
            # exhausted list right
            aux[k:] = left[ia:]
            break
        elif ia >= len(left):
            # exhausted list left
            aux[k:] = right[ib:]
            break
        elif right[ib] < left[ia]:
            aux[k] = right[ib]
            ib += 1
            # increment split inversion counter
            num_inv = num_inv + len(left) - ia
        else:
            # a <= b
            aux[k] = left[ia]
            ia += 1
    return aux, num_inv  # total number of inversions in aux

def countInversions(a):
    def sort_and_count(a):
        if len(a) > 1:
            mid = len(a) // 2
            left = a[:mid]
            right = a[mid:]
            a_sorted, count_splitInv = merge_and_count_splitInv(sort_and_count(left),
                                                         sort_and_count(right))
            return (a_sorted, count_splitInv)
        else:
            return (a, 0)
    return sort_and_count(a)[1]

###################################### 

if __name__ == "__main__":
    with open("IntegerArray.txt", 'r', encoding='utf-8') as f:
        input_array = [int(line.strip()) for line in f]
        print(countInversions(input_array))