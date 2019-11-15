

# Smallest sub-array with sum greater than a given value
# O(n^2) time and O(1) space
def find_smallest_length(arr, s):
    size = len(arr)
    min_length = size + 1

    # if sum(arr) <= s:
    #     return "Not possible"

    for i in range(size):
        sub_sum = arr[i]

        if sub_sum > s:
            return 1  # sub array with only 1 element

        for j in range(i+1, size):
            sub_sum += arr[j]

            if sub_sum > s and j-i+1 < min_length:
                min_length = j-i+1

    if min_length == size + 1:
        return "Not possible"

    return min_length


print(find_smallest_length([1, 4, 45, 6, 10, 19], 51))
print(find_smallest_length([1, 10, 5, 2, 7], 9))
print(find_smallest_length([1, 11, 100, 1, 0, 200, 3, 2, 1, 250], 280))
print(find_smallest_length([- 8, 1, 4, 2, -6], 6))
print(find_smallest_length([1, 2, 4], 8))


# O(n) time and O(1) space
def find_smallest_length_fast(arr, s):
    size = len(arr)
    min_length = size + 1
    sub_sum = 0
    start = end = 0
    while end < size:
        while sub_sum <= s and end < size:
            # Ignore sub-arrays with
            # negative sum if x is
            # positive.
            if sub_sum <= 0 and s > 0:
                start = end
                sub_sum = 0

            sub_sum += arr[end]
            end += 1

        while sub_sum > s and start < size:
            if end - start < min_length:
                min_length = end - start

            sub_sum -= arr[start]
            start += 1

    if min_length == size + 1:
        return "Not possible"

    return min_length


print(find_smallest_length_fast([1, 4, 45, 6, 10, 19], 51))
print(find_smallest_length_fast([1, 10, 5, 2, 7], 9))
print(find_smallest_length_fast([1, 11, 100, 1, 0, 200, 3, 2, 1, 250], 280))
print(find_smallest_length_fast([- 8, 1, 4, 2, -6], 6))
print(find_smallest_length_fast([1, 2, 4], 8))
