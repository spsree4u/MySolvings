

# Binary search - To search in a sorted array
def binary_search(item, nums):
    left = -1
    right = len(nums)

    while left + 1 < right:
        mid_index = left + ((right - left)//2)
        mid_value = nums[mid_index]

        if mid_value == item:
            print("Found!!")
            return True

        if mid_value > item:
            right = mid_index
        else:
            left = mid_index

    print("Not found!!")
    return False


print("Binary search non-recursive")
binary_search(5, [1, 3, 4, 6, 8, 9])
binary_search(9, [1, 3, 4, 6, 8, 9])
binary_search(1, [1, 3, 4, 6, 8, 9])
binary_search(6, [1, 3, 4, 6, 8, 9])


def binary_search_recursive(item, array, start, end):
    if start <= end:
        mid = (start+end)//2
        if array[mid] == item:
            return mid
        elif item < array[mid]:
            return binary_search_recursive(item, array, start, mid-1)
        else:
            return binary_search_recursive(item, array, mid+1, end)
    else:
        return -1


print("Binary search recursive")
print(binary_search_recursive(5, [1, 3, 4, 6, 8, 9], 0, 5))
print(binary_search_recursive(9, [1, 3, 4, 6, 8, 9], 0, 5))
print(binary_search_recursive(1, [1, 3, 4, 6, 8, 9], 0, 5))
print(binary_search_recursive(6, [1, 3, 4, 6, 8, 9], 0, 5))


# Search an element in a sorted and rotated array
def search(arr, l, r, val):
    print('hello')
    if l > r:
        return -1

    mid = (l + r) // 2
    if arr[mid] == val:
        return mid

    if arr[l] <= arr[mid]:
        if arr[l] <= val < arr[mid]:
            return search(arr, l, mid-1, val)
        return search(arr, mid+1, r, val)
    if arr[mid] < val <= arr[r]:
        return search(arr, mid+1, r, val)
    return search(arr, l, mid-1, val)


print("Search in a sorted rotated array")
arr1 = [4, 5, 6, 7, 8, 9, 1, 2, 3]
key = 6
i = search(arr1, 0, len(arr1)-1, key)
if i != -1:
    print("Index: %d" % i)
else:
    print("Key not found")
arr1 = [5, 6, 7, 8, 9, 10, 1, 2, 3]
n = len(arr1)
key = 3
i = search(arr1, 0, len(arr1)-1, key)
if i != -1:
    print("Index: %d" % i)
else:
    print("Key not found")


def b(i, l):
    s = 0
    e = len(l) - 1
    while s <= e:
        m = (s+e)//2
        if l[m] == i:
            return m
        elif i < l[m]:
            e = m-1
        else:
            s = m+1
    return -1


print("Test binary search")
print(b(9, [1, 3, 4, 6, 8, 9]))
print(b(1, [1, 3, 4, 6, 8, 9]))
print(b(5, [1, 3, 4, 6, 8, 9]))
print(b(4, [1, 3, 4, 6, 8, 9]))


def rotated_array_search(item, array):
    s = 0
    e = len(array)
    while s <= e:
        m = (s + e) // 2
        if array[m] == item:
            return m
        if array[s] < array[m]:
            if array[s] <= item < array[m]:
                e = m-1
            else:
                s = m+1
        else:
            if array[m] < item <= array[e]:
                s = m+1
            else:
                e = m-1
    return -1


print("Search in a sorted rotated array - non-recursive")
print(rotated_array_search(0, [4, 5, 6, 7, 8, 0, 1, 2]))
print(rotated_array_search(4, [4, 5, 6, 7, 8, 0, 1, 2]))
print(rotated_array_search(2, [4, 5, 6, 7, 8, 0, 1, 2]))
print(rotated_array_search(8, [4, 5, 6, 7, 8, 0, 1, 2]))
print(rotated_array_search(6, [4, 5, 6, 7, 8, 0, 1, 2]))
print(rotated_array_search(1, [4, 5, 6, 7, 8, 0, 1, 2]))
