
"""
Just to learn recursion with string - time and space may be worst
"""


def get_permutations(s):

    if len(s) <= 1:
        return set([s])

    last_char = s[-1]
    rem_char = s[:-1]

    perm_rem_char = get_permutations(rem_char)
    perms = set()

    for i in perm_rem_char:
        for pos in range(len(i) + 1):
            p = i[:pos] + last_char + i[pos:]
            perms.add(p)

    return perms


print(len(get_permutations("abcd")))
