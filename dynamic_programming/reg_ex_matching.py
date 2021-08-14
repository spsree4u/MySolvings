
"""
Given an input string s and a pattern p, implement regular expression matching
with support for '.' and '*' where:

'.' Matches any single character.​​​​
'*' Matches zero or more of the preceding element.
The matching should cover the entire input string (not partial).
isMatch("aa","a") → 0
isMatch("aa","aa") → 1
isMatch("aaa","aa") → 0
isMatch("aa", "a*") → 1
isMatch("aa", ".*") → 1
isMatch("ab", ".*") → 1
isMatch("aab", "c*a*b") → 1

Reference:
https://www.youtube.com/watch?v=HAA8mgxlov8
https://www.youtube.com/watch?v=l3hda49XcDE&list=PLrmLmBdmIlpuE5GEMDXWf0PWbBD9Ga1lO
https://leetcode.com/problems/regular-expression-matching/solution/
"""
import profile


def is_match_brute_force(s, p):

    def match(i, j):
        if i >= len(s) and j >= len(p):
            return True

        if j >= len(p):
            return False

        m = i < len(s) and (s[i] == p[j] or p[j] == '.')

        if j+1 < len(p) and p[j+1] == '*':
            return match(i, j+2) or (m and match(i+1, j))

        if m:
            return match(i+1, j+1)

        return False

    return match(0, 0)


def is_match_top_down_memoization(s, p):

    match_map = {}

    def match(i, j):

        if (i, j) in match_map:
            return match_map[(i, j)]

        if i >= len(s) and j >= len(p):
            return True

        if j >= len(p):
            return False

        m = i < len(s) and (s[i] == p[j] or p[j] == '.')

        if j+1 < len(p) and p[j+1] == '*':
            match_map[(i, j)] = match(i, j+2) or (m and match(i+1, j))
            return match_map[(i, j)]

        if m:
            match_map[(i, j)] = match(i+1, j+1)
            return match_map[(i, j)]

        match_map[(i, j)] = False
        return False

    return match(0, 0)


def is_match_bottom_up_dp(s, p):
    match = [[False] * (len(p)+1) for _ in range(len(s) + 1)]
    match[0][0] = True
    for j in range(1, len(p)+1):
        if p[j-1] == '*':
            match[0][j] = match[0][j-2]

    for i in range(1, len(s)+1):
        for j in range(1, len(p)+1):
            if s[i-1] == p[j-1] or p[j-1] == '.':
                match[i][j] = match[i-1][j-1]
            elif p[j-1] == '*':
                match[i][j] = match[i][j-2]
                if p[j-2] == s[i-1] or p[j-2] == '.':
                    match[i][j] = match[i][j] or match[i-1][j]
            else:
                match[i][j] = False

    return match[len(s)][len(p)]


profile.run("is_match_brute_force('aab', 'c*a*b')")
profile.run("is_match_top_down_memoization('aab', 'c*a*b')")
profile.run("is_match_bottom_up_dp('aab', 'c*a*b')")
