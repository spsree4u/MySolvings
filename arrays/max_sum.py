
# Maximum sum such that no two elements are adjacent


def find_max_sum(arr):
    s_incl = 0
    s_excl = 0

    for i in arr:
        new = s_excl if s_excl > s_incl else s_incl

        s_incl = s_excl + i
        s_excl = new

    return s_excl if s_excl > s_incl else s_incl


print(find_max_sum([5, 5, 10, 100, 10, 5]))
print(find_max_sum([12, 9, 7, 33]))
print(find_max_sum([5, 2, 6, 10, 4, 3]))
