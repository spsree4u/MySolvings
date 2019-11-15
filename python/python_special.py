
# Special case observations in Python

# be careful while using * with list of list
a = [[-1]*5 for x in range(5)]
print(a)
a[0][1] = 20
print(a)
b = [[-1] * 5] * 5
print(b)
b[0][1] = 20
print(b)


# check largest_arranged_number.py under arrays for seeing
# behavior of boolean subtraction
