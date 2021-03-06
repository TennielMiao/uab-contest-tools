"""
misc.py
Miscellaneous tools
by Tenniel Miao and Richard Wohlbold


"""


def building_rainwater(array):
    """
    array is a sequence of nonnegative numbers representing the height of the buildings, each with width 1.
    After rain, how much water can be trapped by the buildings?
    """
    n = len(array)
    left = [0] * n  # max height including itself on the left
    right = [0] * n  # max height including itself on the right

    water = 0

    left[0] = array[0]
    for i in range(1, n):
        left[i] = max(left[i - 1], array[i])
    right[n - 1] = array[n - 1]
    for i in range(n - 2, 0, -1):
        right[i] = max(right[i + 1], array[i])

    for i in range(0, n):
        water += min(left[i], right[i]) - array[i]

    return water


def max_consecutive_sum(array):
    """
    given an array of numbers (positive, negative, or 0)
    return the maximum sum of consecutive numbers
    """
    max_value = max(array)
    running_sum = 0
    for num in array:
        if running_sum < 0:
            running_sum = 0
        running_sum += num
        if running_sum > max_value:
            max_value = running_sum
    return max_value


def greedy_egyptian(x, y):
    """ Greedy algorithm for expanding Egyptian fractions """
    denominators = []
    while True:
        denominators.append(-(-y//x))  # ceiling division
        x, y = -y % x, y * (-(-y//x))
        if x == 0:
            break
    return denominators


def longest_palindromic_substring(s):
    """
    Manacher's algorithm
    """
    T = '#'.join('^{}$'.format(s))
    n = len(T)
    P = [0] * n
    C = R = 0
    for i in range(1, n - 1):
        P[i] = (R > i) and min(R - i, P[2 * C - i])  # equals to i' = C - (i-C)
        # Attempt to expand palindrome centered at i
        while T[i + 1 + P[i]] == T[i - 1 - P[i]]:
            P[i] += 1

        # If palindrome centered at i expand past R,
        # adjust center based on expanded palindrome.
        if i + P[i] > R:
            C, R = i, i + P[i]

    # Find the maximum element in P.
    maxLen, centerIndex = max((n, i) for i, n in enumerate(P))
    return maxLen

