

# Convert array into Zig-Zag fashion


def zigzag(arr):
    for i in range(1, len(arr)):
        if i % 2 != 0:
            if arr[i] < arr[i-1]:
                arr[i-1], arr[i] = arr[i], arr[i-1]
        else:
            if arr[i] > arr[i-1]:
                arr[i - 1], arr[i] = arr[i], arr[i - 1]
    return arr


print(zigzag([4, 3, 7, 8, 6, 2, 1]))
