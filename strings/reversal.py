
# Array/String reversal methods


def reverse(s, start, end):
    while start < end:
        s[start], s[end] = s[end], s[start]
        start += 1
        end -= 1
    return s


a = [2, 5, 6]
print(reverse(a, 0, len(a)-1))


def reverse_rec(s, start, end):
    if start >= end:
        return
    s[start], s[end] = s[end], s[start]
    reverse_rec(s, start+1, end-1)


a = [2, 5, 6]
print(reverse(a, 0, len(a)-1))


# Reverse a string without affecting special characters
def reverse_alpha(s):
    arr = list(s)
    end = len(arr)-1
    start = 0

    while start < end:
        if not arr[start].isalpha():
            start += 1
        elif not arr[end].isalpha():
            end -= 1
        else:
            arr[start], arr[end] = arr[end], arr[start]
            start += 1
            end -= 1
    return ''.join(arr)


b = "a!!!b.c.d,e'f,ghi"
print(reverse_alpha(b))
