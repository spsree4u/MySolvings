

# O(n log n) time, O(1) space, in-place
def find_length(arr):
    arr.sort()
    result = count = 1
    for i in range(1, len(arr)):
        if arr[i] - arr[i-1] == 1:
            count += 1
        else:
            count = 1
        if count > result:
            result = count
    return result


print(find_length([1, 56, 58, 57, 90, 92, 94, 93, 91, 45]))
print(find_length([10, 12, 11]))
print(find_length([14, 12, 11, 20]))


# O(n^2) time, O(1) space as there are no duplicates, Not in-place
def find_length_2(arr):
    result = 1
    for i in range(len(arr)):
        mn = mx = arr[i]
        for j in range(i+1, len(arr)):
            mn = min(mn, arr[j])
            mx = max(mx, arr[j])
            if mx-mn == j-i:
                result = max(result, mx-mn+1)
    return result


print(find_length_2([1, 56, 58, 57, 90, 92, 94, 93, 91, 45]))
print(find_length_2([10, 12, 11]))
print(find_length_2([14, 12, 11, 20]))
