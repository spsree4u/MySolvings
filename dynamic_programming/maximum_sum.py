
# Maximum sum such that no two elements are adjacent

"""
1) Choose the current index:
   In this case, the relation will be dp[i] = arr[i] + dp[i+2]
2) Skip the current index:
   Relation will be dp[i] = dp[i+1]
"""


def find_max_sum(arr):
    n = len(arr)
    dp = [0 for _ in range(n)]
    state = [0 for _ in range(n)]
    return find_max_sum_dp(arr, 0, n, dp, state)


def find_max_sum_dp(arr, i, n, dp, state):

    if i >= n:
        return 0

    if state[i]:
        return dp[i]
    state[i] = 1

    dp[i] = max(arr[i] + find_max_sum_dp(arr, i+2, n, dp, state),
                find_max_sum_dp(arr, i+1, n, dp, state))

    return dp[i]


arr1 = [5, 5, 10, 100, 10, 5]
print(find_max_sum(arr1))
arr1 = [12, 9, 7, 33]
print(find_max_sum(arr1))
arr1 = [5, 2, 6, 10, 4, 3]
print(find_max_sum(arr1))
