"""
Input: ["flower","flow","flight"]
Output: "fl"

Input: ["dog","racecar","car"]
Output: ""
"""


def find_longest_prefix(strs):
    if not strs:
        return ""

    # Time complexity is m*n where m = len(strs[0]) and n = len(strs)
    # Space complexity is O(1)
    for i in range(len(strs[0])):
        for j in range(1, len(strs)):
            if i >= len(strs[j]) or (strs[j][i] != strs[0][i]):
                return strs[0][:i]

    return strs[0]


l1 = ["flower", "flow", "flight"]
l2 = ["dog", "racecar", "car"]
l3 = ["dog", "dog2", "dog45"]
l4 = []
l5 = ["abc"]

print(find_longest_prefix(l1))
print(find_longest_prefix(l2))
print(find_longest_prefix(l3))
print(find_longest_prefix(l4))
print(find_longest_prefix(l5))
