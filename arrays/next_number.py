

def add_one(arr):
    size = len(arr)
    result = [0] * size
    carry = 1
    for i in range(size-1, -1, -1):
        value = arr[i] + carry
        if value == 10:
            result[i] = 0
            carry = 1
        else:
            result[i] = value
            carry = 0
    if carry:
        result = [0] * (size+1)
        result[0] = 1

    return result


print(add_one([9, 9, 9]))
print(add_one([1, 9, 9, 9]))
