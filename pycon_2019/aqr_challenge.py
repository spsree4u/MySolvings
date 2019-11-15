

from itertools import zip_longest
# from operator import add, sub, mul, truediv, pow


class ModList(object):

    def __init__(self, lst):
        self.lst = lst

    # def __new__(cls, lst):
    #     return lst

    def __add__(self, other):
        s = None
        if isinstance(other, ModList):
            z = zip_longest(self.lst, other.lst)
            s = list()
            for i in z:
                if i[0] is not None:
                    if i[1] is not None:
                        s.append(i[0] + i[1])
                    else:
                        s.append(i[0])
        elif isinstance(other, int):
            s = list(map(lambda x: x + other, self.lst))

        return s

    def __sub__(self, other):
        d = None
        if isinstance(other, ModList):
            z = zip_longest(self.lst, other.lst)
            d = list()
            for i in z:
                if i[0] is not None:
                    if i[1] is not None:
                        d.append(i[0] - i[1])
                    else:
                        d.append(i[0])
        elif isinstance(other, int):
            d = list(map(lambda x: x - other, self.lst))
        return d

    def __mul__(self, other):
        p = None
        if isinstance(other, ModList):
            z = zip_longest(self.lst, other.lst)
            p = list()
            for i in z:
                if i[0] is not None:
                    if i[1] is not None:
                        p.append(i[0] * i[1])
                    else:
                        p.append(i[0])
        elif isinstance(other, int):
            p = list(map(lambda x: x * other, self.lst))

        return p

    def __truediv__(self, other):
        q = None
        if isinstance(other, ModList):
            z = zip_longest(self.lst, other.lst)
            q = list()
            for i in z:
                if i[0] is not None:
                    if i[1] is not None:
                        q.append(i[0] / i[1])
                    else:
                        q.append(i[0])
        elif isinstance(other, int):
            q = list(map(lambda x: x / other, self.lst))

        return q

    def __pow__(self, other):
        z = list(map(lambda x: pow(x, other), self.lst))
        return z


# a = ModList([3, 2, 5, 1])
# b = ModList([1, 4, 2])
# print(a + b)
# print(a + 2)
# print(b + a)
# print(a - b)
# print(a - 2)
# print(b - a)
# print(a * b)
# print(a * 2)
# print(b * a)
# print(a / b)
# print(a / 2)
# print(b / a)
# # print(a / 0)
# print(a ** 2)
# print(b ** 3)
# c = list()
# d = list()
# c.extend([1, 2, 3])
# d.extend([1, 2])
# print(c + d)


class int(type):
    def __str__(self):
        return "112"

    def __int__(self):
        return "112"

    def __getitem__(self, item):
        return item + 1

    def __new__(type):
        return "abc"

# a = 1
# print(a)


def split_2(arr):
    count = 0
    for i in range(1, len(arr)+1):
        l = sum(arr[:i])
        r = sum(arr[i:])
        if l > r:
            count += 1
    return count


def splitIntoTwo(arr):
    # Write your code here
    count = 0
    prev_left_sum = arr[0]
    prev_right_sum = sum(arr[1:])
    if prev_left_sum > prev_right_sum:
        count += 1
    for i in range(1, len(arr)):
        left_sum = arr[i] + prev_left_sum
        right_sum = prev_right_sum - arr[i]
        prev_left_sum = left_sum
        prev_right_sum = right_sum
        if left_sum > right_sum:
            count += 1
    return count


print(splitIntoTwo([10, -5, 6]))
