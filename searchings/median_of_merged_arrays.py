

# Find median of two merged sorted lists


def median(arr):
    n = len(arr)
    if n % 2 == 0:
        return (arr[n//2] + arr[(n//2)-1]) // 2
    else:
        return arr[n//2]


# O(log n) time
def get_merged_median(arr1, arr2, n):
    if n == 0:
        return -1
    elif n == 1:
        return (arr1[0] + arr2[0])//2
    elif n == 2:
        return (max(arr1[0], arr2[0]) + min(arr1[1], arr2[1])) // 2
    else:
        m1 = median(arr1)
        m2 = median(arr2)
        if m1 > m2:
            if n % 2 == 0:
                return get_merged_median(arr1[:(n//2)+1],
                                         arr2[(n//2)-1:],
                                         (n//2)+1)
            else:
                return get_merged_median(arr1[:(n//2)+1],
                                         arr2[(n//2):],
                                         (n//2)+1)
        else:
            if n % 2 == 0:
                return get_merged_median(arr1[(n//2)-1:],
                                         arr2[:(n//2)+1],
                                         (n//2)+1)
            else:
                return get_merged_median(arr1[(n//2):],
                                         arr2[:(n//2)+1],
                                         (n//2)+1)


arr111 = [1, 2, 3, 6]
arr222 = [4, 6, 8, 10]
n1 = len(arr111)
print(int(get_merged_median(arr111, arr222, n1)))
