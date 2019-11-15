

# Number of substrings divisible by 6 in a string of integer
# DP

def f(i, m, s, visited):
    count = 0
    if i == len(s):
        return 0
    if visited[i][m] != -1:
        return visited[i][m]
    x = ord(s[i]) - ord('0')
    count += (((x + m) % 3 == 0)
              and (x % 2 == 0)) + f(i+1, (x+m) % 3, s, visited)
    visited[i][m] = count
    return count


def count_div_by_6(s):
    n = len(s)
    visited = [[-1] * 3 for _ in range(n+1)]
    count = 0
    for i in range(n):
        if s[i] == '0':
            count += 1
        else:
            count += f(i, 0, s, visited)
    return count


s1 = "4806"
print(count_div_by_6(s1))
