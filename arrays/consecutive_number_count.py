"""
Input: [5,5,5,7,7,3,4,7]
Output: ['5:3', '7:2', 3, 4, 7]
"""


def add_to_map(stack, map_name):
    if len(stack) > 1:
        map_name.append(str(stack[0]) + ':' + str(len(stack)))
    elif len(stack) == 1:
        map_name.append(stack[0])
    else:
        print("Empty stack!!")


def pack_numbers(arr):
    count_map = []
    stack = arr[0:1]
    prev = arr[0]
    for i in arr[1:]:
        if i != prev:
            add_to_map(stack, count_map)
            stack.clear()

        stack.append(i)
        prev = i

    if stack:
        add_to_map(stack, count_map)

    print(count_map)
    return count_map


arr1 = [5, 5, 5, 7, 7, 3, 4, 7, 7, 7, 5, 6]
pack_numbers(arr1)
