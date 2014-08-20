"""
[Posted April 29th] You are a given a unimodal array of n distinct elements,
meaning that its entries are in increasing order up until its maximum element,
 after which its elements are in decreasing order. Give an algorithm to compute
 the maximum element that runs in O(log n) time.
"""

def binarySearch(a, key):
    def helper(a, lo, hi):
        if hi < lo:
            return lo
        mid = lo + (hi - lo) // 2
        if key == a[mid]:
            return mid
        elif key < a[mid]:
            return helper(a, lo, mid - 1)
        else:
            return helper(a, mid + 1, hi)
    return helper(a, 0, len(a) - 1)


def findMax(a):
    """
    a is a unimodal array
    return max
    """
    if a is [] or len(a) < 3:
        return None
    def helper(a, lo, hi):
        if hi < lo:
            return a[hi]
        mid = lo + (hi - lo) // 2
        print(lo, mid, hi)
        if a[0] < a[mid] and a[mid] > a[hi]:
            # search in right half
            return helper(a, mid + 1, hi)
        else:
            return helper(a, lo, mid - 1)
    return helper(a, 0, len(a) - 1)

a = [2, 4, 5, 8, 10, 11, 12, 13, -3]
#a = [2, 4, 5, 8, 10, 9, -1, -2, -3]
print(findMax(a))
