

# O(n*capacity) time
def knapsack(capacity, values, weights):
    n = len(values)
    knap = [[0 for _ in range(capacity + 1)] for _ in range(n+1)]

    for i in range(n+1):
        for w in range(capacity+1):
            if i == 0 or w == 0:
                knap[i][w] = 0
            elif weights[i-1] <= w:
                knap[i][w] = max(values[i-1] + knap[i-1][w-weights[i-1]],
                                 knap[i-1][w])
            else:
                knap[i][w] = knap[i-1][w]

    return knap[n][capacity]


val = [60, 100, 120]
wt = [10, 20, 30]
W = 50
print(knapsack(W, val, wt))
