
from itertools import permutations


def largest_num(arr):
    merged_nums = []
    for i in permutations(arr, len(arr)):
        merged_nums.append("".join(map(str, i)))
    return max(merged_nums)


print(largest_num([54, 546, 548, 60]))


def compare(a, b):
    ab = str(a) + str(b)
    ba = str(b) + str(a)
    return (int(ba) > int(ab)) - (int(ba) < int(ab))


def my_compare(mycmp):
    # Convert a cmp= function into a key= function
    class K(object):
        def __init__(self, obj):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0

    return K


ar = [54, 546, 548, 60, ]
sorted_array = sorted(ar, key=my_compare(compare))
number = "".join([str(i) for i in sorted_array])
print(number)
