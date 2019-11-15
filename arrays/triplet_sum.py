
# Count triplets with sum smaller than a given value

from datetime import datetime


def get_time(f):
    def inner(*args):
        start = datetime.now()
        result = f(*args)
        end = datetime.now()
        print(end - start)
        return result
    return inner


@get_time
def count_triplets(arr, s):
    size = len(arr)
    count = 0
    for i in range(size):
        for j in range(i+1, size):
            for k in range(j+1, size):
                if arr[i] + arr[j] + arr[k] < s:
                    count += 1

    return count


arr1 = [5, 1, 3, 4, 7]
print(count_triplets(arr1, 12))


@get_time
def count_triplets_fast(arr, s):
    arr.sort()
    size = len(arr)
    count = 0
    for i in range(size):
        j = i + 1
        k = size - 1
        while j < k:
            if arr[i] + arr[j] + arr[k] >= s:
                k -= 1
            else:
                count += (k-j)
                j += 1
    return count


arr1 = [5, 1, 3, 4, 7]
print(count_triplets(arr1, 12))
