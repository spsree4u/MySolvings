
import math


def binary(num):
    bin_result = []
    while num > 0:
        bin_result.append(num % 2)
        num //= 2
    bin_result.reverse()
    return bin_result


# print(binary(742))


def is_prime(n):
    for i in range(2, n):
        for j in range(1, int(math.sqrt(n)) + 1):
            if i * j == n:
                return False
    return True


# print(is_prime(11))


def gcd(m, n):
    if n == 0:
        return m
    return gcd(n, m % n)


# print(gcd(9, 15))


def max_number(base, n):
    """
    Computing the maximum value for a number of
    a specific base consisting of N digits
    """
    # base_map = {2: 1, 8: 7, 10: 9, 16: 'F'}
    return (base ** n) - 1


# print(max_number(8, 4))


def factorial(n):
    if n < 2:
        return 1
    fact = 1
    for i in range(2, n+1):
        fact *= i
    return fact


print(factorial(5))
