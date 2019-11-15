

# Find the smallest positive integer value that cannot be
# represented as sum of any subset of a given array
def find_smallest(arr):
    res = 1
    for i in range(len(arr)):
        if arr[i] <= res:
            res += arr[i]
        else:
            break
    return res


print(find_smallest([1, 3, 4, 5]))
print(find_smallest([1, 2, 6, 10, 11, 15]))
print(find_smallest([1, 1, 1, 1]))
print(find_smallest([1, 1, 3, 4]))
