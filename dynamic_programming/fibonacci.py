
from datetime import datetime


def get_time(f):
    def inner(*args):
        start = datetime.now()
        result = f(*args)
        end = datetime.now()
        print(end - start)
        return result
    return inner


# Exponential time T(n) = T(n-1) + T(n-2) and
# O(n) space if we consider the function call stack size, otherwise O(1)
# @get_time
def fib(n):
    if n < 1:
        return 0

    elif n < 2:
        return 1

    return fib(n-1) + fib(n-2)


visited = {}


# O(n) time
# @get_time
def fast_fib(n):
    if n < 1:
        return 0

    elif n < 2:
        return 1

    if n in visited:
        # print("save")
        return visited[n]

    result = fast_fib(n-1) + fast_fib(n-2)
    visited[n] = result

    return result


# O(n) time and O(1) space
@get_time
def fast_iterative_fib(n):
    a = 0
    b = 1
    if n == 0:
        return a
    elif n == 1:
        return b
    else:
        for i in range(2, n+1):
            temp = a + b
            a = b
            b = temp
        return b


# O(log n) time and O(1) space
@get_time
def super_fast_fib(n):
    F = [[1, 1],
         [1, 0]]
    if n == 0:
        return 0

    power(F, n-1)

    return F[0][0]


def power(F, n):
    if n == 0 or n == 1:
        return

    M = [[1, 1],
         [1, 0]]
    power(F, n//2)
    multiply(F, F)

    if n % 2 != 0:
        multiply(F, M)


def multiply(F, M):
    x = (F[0][0] * M[0][0] +
         F[0][1] * M[1][0])
    y = (F[0][0] * M[1][0] +
         F[0][1] * M[1][1])
    z = (F[1][0] * M[0][0] +
         F[1][1] * M[1][0])
    w = (F[1][0] * M[0][1] +
         F[1][1] * M[1][1])

    F[0][0] = x
    F[0][1] = y
    F[1][0] = z
    F[1][1] = w


@get_time
def fib_dp(n):
    if n == 1 or n == 2:
        return 1
    fib_arr = [None] * (n+1)
    fib_arr[1] = fib_arr[2] = 1
    for i in range(3, n+1):
        fib_arr[i] = fib_arr[i-1] + fib_arr[i-2]
    return fib_arr[n]


start = datetime.now()
print(fib(20))
end = datetime.now()
print(end - start)
start = datetime.now()
print(fast_fib(500))
end = datetime.now()
print(end - start)
print(fast_iterative_fib(50000))
print(super_fast_fib(50000))
print(fib_dp(50000))
