

# O(n)
def is_palindrome_dsa(s):
    if s == "":
        return "Empty String"
    start = 0
    end = len(s) - 1
    while s[start] == s[end] and start < end:
        start += 1
        end -= 1
    return s[start] == s[end]


print(is_palindrome_dsa("wasiteliotstoiletisaw"))
print(is_palindrome_dsa(""))


"""
Write an efficient function that checks whether 
any permutation of an input string is a palindrome.
O(n) time and O(1) space
"""


def has_palidrome(s):
    chars = set()

    for i in s:
        if i in chars:
            chars.remove(i)
        else:
            chars.add(i)

    return len(chars) <= 1


print(has_palidrome("civil"))
print(has_palidrome("ivicc"))
