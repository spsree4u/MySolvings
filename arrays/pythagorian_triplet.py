

# O(n^3) time and O(1) space
def triplet(arr):
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            for k in range(j+1, len(arr)):
                x = arr[i]**2
                y = arr[j]**2
                z = arr[k]**2
                if x == y + z or y == x + z or z == x + y:
                    return True
    return False


print(triplet([3, 1, 4, 6, 5]))


# O(n^2) time and O(1) space, in-place
def triplet_v2(arr):
    # O(n) time
    for i in range(len(arr)):
        arr[i] = arr[i] ** 2

    # O(n log n) time, in-place
    arr.sort()
    # O(n^2) time
    for i in range(len(arr)-1, 1, -1):
        left = 0
        right = i - 1
        # O(n) time
        while left < right:
            if arr[left] + arr[right] == arr[i]:
                return True
            else:
                if arr[left] + arr[right] < arr[i]:
                    left += 1
                else:
                    right -= 1

    return False


print(triplet_v2([3, 1, 4, 6, 5]))


# O(n^2) time and O(n) space, not in-place
def triplet_v3(arr):
    # O(n) time
    for i in range(len(arr)):
        arr[i] = arr[i] ** 2

    sum_set = set()
    # O(n^2) time
    for i in arr:

        # O(n) time
        for j in arr:
            if j in sum_set:
                return True
            sum_set.add(i - j)

    return False


print(triplet_v3([3, 1, 4, 6, 5]))
