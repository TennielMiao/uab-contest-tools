"""
UAB Competition Programs
by Tenniel Miao and Richard Wohlbold

Number Theory
euclidean algorithm for greatest common divisor (gcd)
least common multiple (lcm)
extended euclidean


Prime Numbers
prime generators: sieve of Eratosthenes, Sieve of Atkin, Sieve of Sundaram, Wheel Factorization
"""


# ======================================================================================================================
# Elementary Number Theory
def euclidean_gcd(a: int, b: int):
    """
    compute the greatest common divisor of two positive integers, a and b, using the Euclidean algorithm
    """
    while b > 0:
        a, b = b, a % b
    return a


def lcm(a: int, b: int):
    """
    return the least common multiple of two integers, a and b.
    """
    return a * b // euclidean_gcd(a, b)


def extended_euclidean_gcd(a: int, b: int):
    """
    extended euclidean algorithm, returning the gcd and two bezout coefficients
    """
    alpha, s, beta, t = 1, 0, 0, 1
    while b > 0:
        a, (q, b) = b, divmod(a, b)
        alpha, s = s, alpha - q * s
        beta, t = t, beta - q * t
    return a, alpha, beta


def modular_inverse(a: int, b: int):
    """
    return the modular inverse of a mod b; NEED extended euclidean algorithm
    """
    d, alpha, beta = extended_euclidean_gcd(a, b)
    # a * alpha + b * beta ==  d
    return alpha % b if d == 1 else None


# bisect, lower_bound
# ======================================================================================================================
def bisect(a, x, lo=0, hi=None, comp=lambda e1, e2: e1 < e2):
    """
    a simplified and generalized version of python's bisect package: https://docs.python.org/3.6/library/bisect.html

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


# ======================================================================================================================
# Prime Number
from math import log
LENGTH_LIMIT = 10**8
default_prime_table = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


def sieve_prime_by_interval(beg=2, end=100, table=default_prime_table):
    """
    generate prime numbers in the interval [beg, end), using a given prime table and the segmented Sieve of Eratosthenes
    """
    if end > table[-1]:
        # need to grow the current prime table
        pos = table[-1] + 1
        while pos < end:
            print("iteration, current pos: {}".format(pos))
            len_sift = min(LENGTH_LIMIT, table[-1] ** 2 - pos, end - pos)
            sift = [True] * len_sift
            # sieve the composite numbers
            for num in table:
                for j in range(-(-pos // num), -(-(pos + len_sift) // num)):  # ceiling division by unary minus
                    sift[j * num - pos] = False
            # append prime numbers to the table
            table.extend([i + pos for i, is_prime in enumerate(sift) if is_prime])
            pos += len_sift
    return table[bisect(table, beg): bisect(table, end, comp=lambda e1, e2: e1 <= e2)]


def sieve_prime_by_index(ibeg=0, iend=20, table=default_prime_table):
    """
    generate prime numbers from [ibeg-th, iend-th) using a given prime table
    notice that ibeg and iend are 0-indexed.
    """

    if iend > len(table):
        # need to grow the prime table
        pos = table[-1] + 1
        while len(table) < iend:
            print("iteration, current pos: {}".format(pos))
            heuristic_len_sift = int((iend - len(table)) * log(table[-1]) + 100)
            len_sift = min(LENGTH_LIMIT, table[-1] ** 2 - pos, heuristic_len_sift)
            sift = [True] * len_sift
            # sieve the composite numbers
            for num in table:
                for j in range(-(-pos // num), -(-(pos + len_sift) // num)):  # ceiling division by unary minus
                    sift[j * num - pos] = False
            # append prime numbers to the table
            table.extend([i + pos for i, is_prime in enumerate(sift) if is_prime])
            pos += len_sift
    return table[ibeg:iend]

