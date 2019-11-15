

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


# binary_search(5, [1, 3, 4, 6, 8, 9])


# Search an element in a sorted and rotated array
def search(arr, l, r, val):
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
