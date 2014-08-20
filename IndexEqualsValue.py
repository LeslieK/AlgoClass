def IndexEqualsValue(a):
    """
    returns True if there exists an index i s.t.
    a[i] equals i
    """
    def helper(a, lo, hi):
        if hi < lo:
            return False
        mid = lo + (hi - lo) // 2
        if a[mid] == mid:
            return True
        elif mid < a[mid]:
            return helper(a, mid + 1, hi)
        else:
            return helper(a, lo, mid - 1)
    return helper(a, 0, len(a) - 1)

a = [0, 1, 2, 3, 4, 5, 6]
print(IndexEqualsValue(a))