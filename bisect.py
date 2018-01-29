"""
a simplified and generalized version of python's bisect package
https://docs.python.org/3.6/library/bisect.html
"""


def bisect(a, x, lo=0, hi=None, comp=lambda e1, e2: e1 < e2):
    """
    return the index where to insert item x in a list a
    a must be sorted (in ascending order)
    the return value i is such that:
    1. all e in a[:i] have: comp(e, x)
    2. all e in a[i:] have: not comp(e, x)
    if comp is set to <=, the function goes for the rightmost position;
    if comp is set to <, the function goes for the leftmost position.
    """
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if comp(a[mid], x):
            lo = mid + 1
        else:
            hi = mid
    return lo


def insort(a, x, lo=0, hi=None, comp=lambda e1, e2: e1 < e2):
    """
    insert item x into list a; similar to bisect
    """
    i = bisect(a, x, lo, hi, comp)
    a.insert(i, x)
