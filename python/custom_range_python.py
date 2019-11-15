
#  Implement range function


# def custom_range(start=0, end=None, step=1):
def custom_range(arg1=None, arg2=None, arg3=None):
    if arg1 and not arg2 and not arg3:
        start = 0
        end = arg1
        step = 1
    elif arg1 and arg2 and not arg3:
        start = arg1
        end = arg2
        step = 1
    else:
        start = arg1
        end = arg2
        step = arg3
    if not end:
        raise Exception("end should have a valid value")
    if step == 0:
        raise Exception("step cannot be 0")
    elif step > 0:
        if start > end:
            return
        while start < end:
            yield start
            start += step
    else:
        if start < end:
            return
        while start > end:
            yield start
            start += step


# a = custom_range(0, 4, 1)
a = custom_range(10, 2, -1)
for i in a:
    print(i)
