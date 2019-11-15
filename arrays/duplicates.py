

# O(n) time and O(1) space and in-place
def find_repeating(arr):
    """
    This will print repeated number more than once
    if number exists more than twice
    """
    for i in range(len(arr)):
        if arr[abs(arr[i])] >= 0:
            arr[abs(arr[i])] = -arr[abs(arr[i])]
        else:
            yield abs(arr[i])


print("Method 1")
arr1 = [1, 2, 3, 1, 3, 6, 6, 6]
for j in find_repeating(arr1):
    print(j)


# O(n) time and O(1) space and in-place
def find_repeating_v2(arr):
    for i in range(len(arr)):
        arr[arr[i] % 10] = arr[arr[i] % 10] + 10

    print(arr)
    for i in range(len(arr)):
        if arr[i] > 19:
            yield i


print("Method 2")
arr1 = [1, 2, 3, 1, 3, 6, 6, 6]
for j in find_repeating_v2(arr1):
    print(j)


# O(n log n) time and O(1) space, not in-place
def find_repeat(arr):
    """Find a duplicate number in list of 1...n """
    left = 1
    right = len(arr) - 1

    while left < right:
        mid = left + ((right - left) // 2)
        lower_range_count = 0
        for i in arr:
            if left <= i < mid + 1:
                lower_range_count += 1

        possible_lower_range_count = mid + 1 - left
        if lower_range_count > possible_lower_range_count:
            left, right = left, mid
        else:
            left, right = mid + 1, right

    return left


print("Find a duplicate number in list")
print(find_repeat([1, 2, 3, 4, 5, 6, 5, 8, 3]))
