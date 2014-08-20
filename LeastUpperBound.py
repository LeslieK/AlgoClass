"""
[Posted April 29th] Give the best upper bound that you can on the solution
to the following recurrence: T(1)=1 and T(n)<=T([sqrt(n)])+1 for n>1. (Here [x]
denotes the "floor" function, which rounds down to the nearest integer.)
"""
import math

def memoize(f):
    d = {}
    def wrapped_f(x):
        if x in d:
            return d[x]
        else:
            d[x] = f(x)
            return d[x]
    return wrapped_f

@memoize
def T(n):
    if n == 1:
        return 1
    else:
        return T(math.floor(math.sqrt(n))) + 1

for i in range(1, 1024, 1):
    print(T(i))




