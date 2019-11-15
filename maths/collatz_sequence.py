
"""
The Collatz sequence of a number N is defined as:

    If N is Odd then change N to 3*N + 1.
    If N is Even then change N to N / 2.

For example let us have a look at the sequence when N = 13:
13 -> 40 -> 20 -> 10 -> 5 > 16 -> 8 -> 4 -> 2 -> 1
"""


# Find number of steps for an integer to reach 1 using Collatz conditions
def find_count(n):
    if n <= 0:
        return "Invalid input"
    count = 0
    while n != 1:
        if n % 2 == 0:
            n = n/2
        else:
            n = 3*n+1
        count += 1
    return count


print(find_count(9))
print(find_count(3))
print(find_count(0))


# Given an integer N. Find the number in the range from 1 to N-1 which is
# having the maximum number of steps to reach 1 using Collatz conditions
def generate_collatz_map(n, collatz_map):
    if n in collatz_map:
        return collatz_map[n]

    if n == 1:
        collatz_map[n] = 1

    elif n % 2 == 0:
        collatz_map[n] = 1 + generate_collatz_map(n/2, collatz_map)

    else:
        collatz_map[n] = 1 + generate_collatz_map(3*n+1, collatz_map)

    return collatz_map[n]


def find_max_count(n):
    if n <= 0:
        return "Invalid input"
    collatz_map = {}
    generate_collatz_map(n, collatz_map)
    max_count = 0
    number = 0

    for i in range(1, n+1):
        if i not in collatz_map:
            generate_collatz_map(i, collatz_map)

        if collatz_map[i]-1 > max_count:
            max_count = collatz_map[i]-1
            number = i
    return number, max_count


print(find_max_count(10))
